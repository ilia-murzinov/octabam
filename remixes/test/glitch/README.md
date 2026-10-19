# `glitch` — SHATTER + STUTTR

Glitch inserts beside a stock FX chooser (PLATE REV and SPRING REV harvested
for DSP room; DARK REV kept). `make check REMIX=glitch` builds and runs
`verify_shatter` / `verify_stuttr`.

**Hardware (Ilia's MKII, 19 Oct 2026):** flashed `OCTABAMG4` /
`GLITCH G4.RMX`; every SHATTER and STUTTR knob on both pages exercised.

Do **not** also select TAPE ECHO and SIDECHAIN_COMPRESSOR in the same image:
that quartet stalls the sequencer (`docs/contributing/FAILURE_MODES.md`).
This remix is the safe SHATTER+STUTTR pair only.

Module pages: [`modules/shatter`](../../../modules/shatter/README.md),
[`modules/stuttr`](../../../modules/stuttr/README.md).
