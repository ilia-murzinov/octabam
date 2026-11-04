#ifndef OCTABAM_MEGABYTE_CPU_H
#define OCTABAM_MEGABYTE_CPU_H
#include <stdint.h>

#define MB_FRAMES 16u
#define MB_RING   176400u
#define MB_STRIDE 1411328u

/* Caroline Megabyte–inspired lo-fi delay in the stock Echo Freeze rings.
 * FX2 id 0x08 (replaces DELAY). DSP is a passthrough; audio is ColdFire. */
typedef struct {
    uint32_t active, valid, phase, rng;
    int32_t  mix, feedback, gain, mod_amt;
    int32_t  delay;          /* fractional samples ×256 */
    int32_t  lp_z;           /* one-pole loft filter */
    int32_t  havoc;          /* smoothed HAVC amount */
} MbState;

typedef struct {
    uint32_t time, feedback, gain, mod, havoc, mix;
} MbParams;

void mb_process(MbState *, const MbParams *, volatile int32_t *ring,
                uint32_t write, int32_t *audio, int32_t *record);

extern MbState mb_states[8];

/* Nonzero ⇒ skip stock Echo Freeze filter/mix for this track. */
unsigned mb_cpu_frame(uint32_t *stock_stack);
#endif
