#ifndef OCTABAM_MEGABYTE_CPU_H
#define OCTABAM_MEGABYTE_CPU_H
#include <stdint.h>

#define MB_FRAMES 16u
#define MB_RING   176400u
#define MB_STRIDE 1411328u

typedef struct {
    uint32_t active, valid, phase, rng;
    int32_t  mix, feedback, drive1, drive2; /* drive stages, Q1.31 */
    int32_t  delay;          /* fractional samples ×256 */
    int32_t  lp_z;
    int32_t  havoc;          /* 0..ONE — runaway amount */
    int32_t  mod_depth;      /* fractional samples ×256 */
} MbState;

typedef struct {
    uint32_t time, feedback, gain, mod, havoc, mix;
} MbParams;

void mb_process(MbState *, const MbParams *, volatile int32_t *ring,
                uint32_t write, int32_t *audio, int32_t *record);

extern MbState mb_states[8];
unsigned mb_cpu_frame(uint32_t *stock_stack);
#endif
