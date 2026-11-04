# `megabyte` — MEGABYTE

A lo-fi delay inspired by Caroline Guitar Company's **Megabyte**, replacing
stock FX2 **DELAY** (Echo Freeze, id `0x08`).

It runs on the **ColdFire** in the stock four-second per-track SDRAM rings
(same seam as Tape Echo: `docs/firmware/COLDFIRE_DELAY.md`). The DSP side is
an empty passthrough. Not a circuit clone of the pedal: one mono head, a
driven soft-clipped wet preamp, a clock-tracking loft low-pass, LFO time
modulation, and a HAVC feedback boost for runaway repeats.

**Conflicts with TAPE ECHO** (same `0x4000361a` / `0x40002f44` detours).

## Knobs

| page | slot | name | what it does |
|---|---|---|---|
| 1 | A | TIME | ~50 ms (0) to ~1200 ms (127) |
| 1 | B | FDBK | repeats; upper range + HAVC self-oscillates |
| 1 | C | GAIN | wet preamp drive (~+21 dB at 127) |
| 1 | D | MOD | delay-time warble |
| 1 | E | HAVC | havoc: push feedback toward runaway |
| 1 | F | MIX | wet level; **0 is exact dry** |

Page 2 is unused in v1 (beat DIV / LIM later).

## Measured

`tools/verify/verify_megabyte_cpu.py` (native host build of `cpu.c`):

- MIX=0 preserves asymmetric dry audio bit-exact
- TIME mid produces a delayed impulse near the mapped latency
- FDBK regenerates; HAVC raises the feedback ceiling

Not yet on hardware. Proof stays `CHECK` until a unit pass.

## On unit (when flashed)

1. FX2 → **MEGABYTE** (where DELAY was)
2. MIX 0 → exact dry
3. TIME / FDBK / GAIN / MOD / HAVC — listen for lo-fi repeats and havoc runaway
4. Two tracks with Megabyte at once
5. STOP×3 should clear rings via the reset detour

Report what failed — proof stays CHECK until you say PASS.
