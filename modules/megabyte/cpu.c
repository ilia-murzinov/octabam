/*
 * Megabyte — Caroline-inspired lo-fi delay (lean ColdFire voice).
 *
 * Knob roles (distinct, pedal-shaped):
 *   TIME  delay 50..1200 ms; longer → darker loft
 *   FDBK  stable repeats (≤~0.88 alone)
 *   GAIN  wet preamp into the write (drive + one softclip)
 *   MOD   chorus on the read (~0.5..4 ms); LFO once per block
 *   HAVC  dead <16; else pull feedback toward runaway
 *   MIX   wet over dry; 0 = exact dry
 *
 * Budget: ~Y-class EMAC count. No div/mod in the sample loop.
 * (CX MB Z froze — too many mac.l per sample.)
 */
#include "cpu.h"

#define MB_ONE 0x7fffffff

_Static_assert(sizeof(MbState) == 44, "cpu_hooks.s: 8 x 44 bytes");

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

static int32_t softclip(int32_t x) {
    int32_t a = x < 0 ? -x : x;
    if (a < 0x20000000) return x;
    int32_t x2 = mul31(x, x);
    int32_t x3 = mul31(x2, x);
    return sat_sub(x, mul31(x3, 0x2aaaaaaa));
}

static int32_t time_to_delay(uint32_t time) {
    if (time > 127) time = 127;
    return (int32_t)((2205u + time * 399u + ((time * 72u) >> 7)) << 8);
}

/* GAIN → extra drive Q1.31 (0..ONE): write = softclip(mono + mono·drive). */
static int32_t drive_coeff(uint32_t g) {
    if (g > 127) g = 127;
    return (int32_t)(g * 0x1020408u);
}

static int32_t feedback_coeff(uint32_t f) {
    if (f > 127) f = 127;
    return (int32_t)(f * 0xE20408u);   /* ~0.88 max */
}

static int32_t mix_coeff(uint32_t m) {
    if (m > 127) m = 127;
    return (int32_t)(m * 0x1020408u);
}

/* ~0.5..4 ms depth in samples×256. */
static int32_t mod_depth_coeff(uint32_t m) {
    if (m > 127) m = 127;
    return (int32_t)(m * 353u);
}

static int32_t havoc_amt(uint32_t h) {
    if (h < 16) return 0;
    if (h > 127) h = 127;
    return (int32_t)((h - 16) * 0x125A4E7u);
}

/* Cheap sine once per block. */
static int32_t sine(uint32_t phase) {
    int32_t x = (int32_t)(phase ^ 0x80000000u);
    int32_t x2 = mul31(x, x);
    return sat_sub(x, mul31(mul31(x2, x), 0x15555555));
}

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
    uint32_t i0 = write + MB_RING - (uint32_t)delay;
    if (i0 >= MB_RING) i0 -= MB_RING;
    uint32_t i1 = i0 ? i0 - 1u : MB_RING - 1u;
    return lerp8(ring[2u * i0], ring[2u * i1], frac);
}

void mb_process(MbState *restrict s, const MbParams *restrict p,
                volatile int32_t *restrict ring, uint32_t write,
                int32_t *restrict audio, int32_t *restrict record) {
    int32_t target = time_to_delay(p->time);
    int32_t mix = mix_coeff(p->mix);
    int32_t fb  = feedback_coeff(p->feedback);
    int32_t drv = drive_coeff(p->gain);
    int32_t md  = mod_depth_coeff(p->mod);
    int32_t hv  = havoc_amt(p->havoc);

    if (!s->active) {
        uint32_t *words = (uint32_t *)s;
        for (unsigned j = 0; j < sizeof(*s) / 4; ++j) words[j] = 0;
        s->delay = target;
        s->mix = mix; s->feedback = fb; s->drive = drv;
        s->mod_depth = md; s->havoc = hv;
        s->rng = 0x6d2b79f5u;
    }
    s->active = 1;

    int32_t dm = (mix - s->mix) >> 9;
    int32_t df = (fb  - s->feedback) >> 9;
    int32_t dg = (drv - s->drive) >> 9;
    int32_t dh = (hv  - s->havoc) >> 9;
    int32_t dmod = (md - s->mod_depth) >> 9;
    int32_t dd = (target - s->delay) >> 6;
    if (!dd && target != s->delay) dd = target > s->delay ? 1 : -1;
    if (dd > 512) dd = 512;
    if (dd < -512) dd = -512;

    uint32_t t = p->time > 127 ? 127 : p->time;
    int32_t alpha = (int32_t)(0x2cccccccu - t * 0x57E4E4u);
    /* HAVC opens loft a little (brighter runaway). */
    alpha = sat_add(alpha, mul31(sat_sub(0x40000000, alpha), hv));

    /* LFO once per block — not 16×. */
    s->phase += 16u * 52000u;
    int32_t lfo = sine(s->phase);
    int32_t mod_off = mul31(s->mod_depth ? s->mod_depth : md, lfo);

    const int32_t FB_RUN = 0x7f000000;

    for (unsigned i = 0; i < MB_FRAMES; ++i) {
        s->mix += dm; s->feedback += df; s->drive += dg;
        s->havoc += dh; s->mod_depth += dmod; s->delay += dd;

        int32_t L = audio[2 * i];
        int32_t R = audio[2 * i + 1];
        int32_t mono = (L >> 1) + (R >> 1);

        /* GAIN: one drive stage into softclip. */
        int32_t driven = softclip(sat_add(mono, mul31(mono, s->drive)));

        int32_t delay = s->delay + mod_off;
        if (delay < (1 << 8)) delay = 1 << 8;

        int32_t wet = read_head(ring, write + i, delay, s->valid);
        s->lp_z += mul31(alpha, wet - s->lp_z);
        wet = s->lp_z;

        s->rng = s->rng * 1664525u + 1013904223u;
        wet = sat_add(wet, (int32_t)((int8_t)(s->rng >> 24) << 7));

        /* FDBK stable; HAVC lerps toward near-unity. */
        int32_t fbk = s->feedback;
        if (s->havoc)
            fbk = sat_add(fbk, mul31(sat_sub(FB_RUN, fbk), s->havoc));

        int32_t rec = softclip(sat_add(driven, mul31(fbk, wet)));
        record[2 * i]     = rec;
        record[2 * i + 1] = rec;

        if (!s->mix) {
            /* exact dry */
        } else {
            int32_t w = mul31(wet, s->mix);
            audio[2 * i]     = sat_add(L, w);
            audio[2 * i + 1] = sat_add(R, w);
        }
    }

    if (!mix && s->mix < 512) s->mix = 0;
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
