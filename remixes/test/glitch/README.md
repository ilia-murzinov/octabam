# `glitch` — SHATTER + STUTTR

Glitch inserts beside a stock FX chooser (PLATE REV and SPRING REV harvested
for DSP room; DARK REV kept). `make check REMIX=glitch` builds and runs
`verify_shatter` / `verify_stuttr`.

**Hardware (Ilia's MKII, 19 Oct 2026):** flashed `OCTABAMG4` /
`GLITCH G4.RMX`; every SHATTER and STUTTR knob on both pages exercised.
That BUILD is this module tip’s DSP (FOLD unity, 15,862-word ring, JITR
LFSR fix). STUTTR’s id is now MULTIBCOMP `0x19` so RESONATOR can keep
free `0x1e` (#806); re-select STUTTR on Parts saved under the old `0x1e`.

Module pages: [`modules/shatter`](../../../modules/shatter/README.md),
[`modules/stuttr`](../../../modules/stuttr/README.md).
