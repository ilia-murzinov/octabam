/*
 * Megabyte — lo-fi delay in the stock four-second CPU delay rings.
 *
 * Inspired by Caroline Guitar Company's Megabyte (dual PT2399 character,
 * driven wet preamp, havoc runaway). Not a circuit clone: one mono head,
 * soft-clip drive, clock-tracking loft low-pass, LFO time-mod, havoc
 * feedback boost. Same ring/DMA protocol as Tape Echo (COLDFIRE_DELAY.md).
 *
 * Freestanding: no libgcc. Fractional mul uses the ColdFire EMAC (as stock
 * delay / Tape Echo); the host path is a 64-bit oracle of the same shift.
 */
#include "cpu.h"

#define MB_ONE 0x7fffffff

_Static_assert(sizeof(MbState) == 44, "cpu_hooks.s allocation: 8 x 44 bytes");

/* Signed fractional EMAC, MACSR=0xa0 as stock's delay establishes. */
static inline int32_t mul31(int32_t a, int32_t b) {
#ifdef __m68k__
    int32_t out;
    __asm__ volatile ("mac.l %1,%2,%%acc0\n\tmovclr.l %%acc0,%0"
                      : "=d"(out) : "d"(a), "d"(b));
    return out;
#else
    return (int32_t)(((int64_t)a * (int64_t)b) >> 31);
#endif
}

static int32_t sat_add(int32_t a, int32_t b) {
    int32_t s = a + b;
    if (b > 0 && s < a) return MB_ONE;
    if (b < 0 && s > a) return (int32_t)0x80000000;
    return s;
}

static int32_t sat_sub(int32_t a, int32_t b) {
    int32_t s = a - b;
    if (b < 0 && s < a) return MB_ONE;
    if (b > 0 && s > a) return (int32_t)0x80000000;
    return s;
}

/* Soft clip ~ x - x^3/3 for |x| > 0.25 FS. */
static int32_t softclip(int32_t x) {
    int32_t a = x < 0 ? -x : x;
    if (a < 0x20000000) return x;
    int32_t x2 = mul31(x, x);
    int32_t x3 = mul31(x2, x);
    return sat_sub(x, x3 / 3);
}

/* TIME 0..127 → 50..1200 ms as fractional samples×256. */
static int32_t time_to_delay(uint32_t time) {
    if (time > 127) time = 127;
    uint32_t samples = 2205u + (time * (52920u - 2205u)) / 127u;
    return (int32_t)(samples << 8);
}

/* Gain 0..127 → drive in Q8.8: 1.0=256 … ~11.0=2816 (+21 dB). */
static int32_t gain_coeff(uint32_t g) {
    if (g > 127) g = 127;
    return (int32_t)(256u + (g * 2560u) / 127u);
}

static int32_t feedback_coeff(uint32_t f) {
    if (f > 127) f = 127;
    return (int32_t)((0x6cccccccu / 127u) * f);   /* ~0.85 at 127 */
}

static int32_t mix_coeff(uint32_t m) {
    if (m > 127) m = 127;
    return (int32_t)((uint32_t)MB_ONE / 127u * m);
}

static int32_t mod_depth(uint32_t m) {
    if (m > 127) m = 127;
    return (int32_t)((m * 530u * 256u) / 127u);
}

static int32_t havoc_boost(uint32_t h) {
    if (h > 127) h = 127;
    return (int32_t)((0x33333333u / 127u) * h);
}

/* Drive x by Q8.8 gain (256..2816) without a 64-bit libgcc mul. */
static int32_t apply_gain(int32_t x, int32_t g88) {
    int32_t units = g88 >> 8;                 /* 1..11 */
    int32_t frac = (g88 & 0xff) << 23;        /* (g88&0xff)/256 as Q1.31 */
    int32_t y = 0;
    for (int32_t n = 0; n < units; ++n)
        y = sat_add(y, x);
    if (frac)
        y = sat_add(y, mul31(x, frac));
    return softclip(y);
}

static int32_t sine(uint32_t phase) {
    int32_t t = (int32_t)(phase >> 1) ^ ((int32_t)phase >> 31);
    t = t < 0 ? -t : t;
    t = MB_ONE - (t << 1);
    return mul31(t, 0x6a09e668);
}

/* Linear interp: a + ((b-a)*frac)>>8, frac in 0..255. No 64-bit mul. */
static int32_t lerp8(int32_t a, int32_t b, uint32_t frac) {
    int32_t d = b - a;
    int32_t ad = d < 0 ? -d : d;
    int32_t lo = (int32_t)(((uint32_t)(ad & 0xff) * frac) >> 8);
    if (d < 0) lo = -lo;
    return a + (d >> 8) * (int32_t)frac + lo;
}

static int32_t read_head(volatile int32_t *ring, uint32_t write,
                         int32_t delay_x256, uint32_t valid) {
    if (valid < 2) return 0;
    int32_t delay = delay_x256 >> 8;
    if (delay < 1) delay = 1;
    if ((uint32_t)delay >= valid) delay = (int32_t)valid - 1;
    uint32_t frac = (uint32_t)delay_x256 & 255u;
    uint32_t i0 = (write + MB_RING - (uint32_t)delay) % MB_RING;
    uint32_t i1 = (i0 + MB_RING - 1) % MB_RING;
    return lerp8(ring[2u * i0], ring[2u * i1], frac);
}

void mb_process(MbState *restrict s, const MbParams *restrict p,
                volatile int32_t *restrict ring, uint32_t write,
                int32_t *restrict audio, int32_t *restrict record) {
    int32_t target = time_to_delay(p->time);
    int32_t mix = mix_coeff(p->mix);
    int32_t fb  = feedback_coeff(p->feedback);
    int32_t gn  = gain_coeff(p->gain);
    int32_t md  = mod_depth(p->mod);
    int32_t hv  = havoc_boost(p->havoc);

    if (!s->active) {
        uint32_t *words = (uint32_t *)s;
        for (unsigned j = 0; j < sizeof(*s) / 4; ++j) words[j] = 0;
        s->delay = target;
        s->mix = mix; s->feedback = fb; s->gain = gn;
        s->mod_amt = md; s->havoc = hv;
        s->rng = 0x6d2b79f5u;
    }
    s->active = 1;

    int32_t dm = (mix - s->mix) / 512;
    int32_t df = (fb  - s->feedback) / 512;
    int32_t dg = (gn  - s->gain) / 512;
    int32_t dh = (hv  - s->havoc) / 512;
    int32_t dd = (target - s->delay) / 64;
    if (!dd && target != s->delay) dd = target > s->delay ? 1 : -1;
    if (dd > 512) dd = 512;
    if (dd < -512) dd = -512;

    uint32_t t = p->time > 127 ? 127 : p->time;
    int32_t alpha = (int32_t)(0x2cccccccu - (t * 0x24000000u) / 127u);

    s->phase += 16u * 90000u;
    int32_t lfo = sine(s->phase);

    for (unsigned i = 0; i < MB_FRAMES; ++i) {
        s->mix += dm; s->feedback += df; s->gain += dg;
        s->havoc += dh; s->delay += dd;

        int32_t L = audio[2 * i];
        int32_t R = audio[2 * i + 1];
        int32_t mono = (L >> 1) + (R >> 1);

        int32_t delay = s->delay + mul31(s->mod_amt ? s->mod_amt : md, lfo);
        if (delay < (1 << 8)) delay = 1 << 8;

        int32_t wet = read_head(ring, write + i, delay, s->valid);
        s->lp_z += mul31(alpha, wet - s->lp_z);
        wet = s->lp_z;

        s->rng = s->rng * 1664525u + 1013904223u;
        wet = sat_add(wet, (int32_t)((int8_t)(s->rng >> 24) << 8));

        int32_t fbk = sat_add(s->feedback, mul31(s->feedback, s->havoc));
        if (fbk > 0x7ccccccc) fbk = 0x7ccccccc;

        int32_t rec = softclip(sat_add(apply_gain(mono, s->gain), mul31(fbk, wet)));
        record[2 * i]     = rec;
        record[2 * i + 1] = rec;

        if (!s->mix) {
            /* exact dry */
        } else if (s->mix >= MB_ONE - 512) {
            audio[2 * i]     = wet;
            audio[2 * i + 1] = wet;
        } else {
            int32_t keep = MB_ONE - s->mix;
            audio[2 * i]     = sat_add(mul31(L, keep), mul31(wet, s->mix));
            audio[2 * i + 1] = sat_add(mul31(R, keep), mul31(wet, s->mix));
        }
    }

    if (!mix && s->mix < 512) s->mix = 0;
    s->mod_amt = md;
    s->valid = s->valid + MB_FRAMES;
    if (s->valid > MB_RING - 1) s->valid = MB_RING - 1;
}

#ifndef MB_HOST
#define U32(a) (*(volatile uint32_t *)(a))
unsigned mb_cpu_frame(uint32_t *sp) {
    unsigned track = sp[112 / 4];
    const uint8_t *setup = (const uint8_t *)sp[76 / 4];
    if (track >= 8) return 0;
    MbState *s = &mb_states[track];
    if (setup[7] != 0x08 || *(const uint8_t *)sp[108 / 4] == 7) {
        s->active = 0;
        return 0;
    }
    const uint8_t *k = (const uint8_t *)sp[72 / 4];
    MbParams p = {k[0], k[2], k[4], k[6], k[8], k[10]};
    uint32_t base = 0x4f502c10u + track * MB_STRIDE;
    uint32_t wr = (sp[48 / 4] - base) >> 3;
    if (wr > MB_RING - MB_FRAMES) { s->active = 0; return 0; }
    U32(0x800000e8) ^= U32(0x40003626);
    __asm__ volatile ("move.l #0,%%acc0\n\tmove.l #0,%%acc1\n\t"
                      "move.l #0,%%acc2\n\tmove.l #0,%%acc3" ::: "memory");
    mb_process(s, &p, (volatile int32_t *)base, wr,
               (int32_t *)sp[96 / 4], (int32_t *)U32(0x800000e8));
    U32(0x80006180) += 68;
    return 1;
}
#endif
