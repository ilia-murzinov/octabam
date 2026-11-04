# `megabyte` — MEGABYTE

A lo-fi delay inspired by Caroline Guitar Company's **Megabyte**, replacing
stock FX2 **DELAY** (Echo Freeze, id `0x08`).

ColdFire voice in the stock four-second per-track rings (Tape Echo seam).
Not a circuit clone: one mono head, driven wet preamp, loft that tracks TIME,
chorus-sized MOD, and HAVC as a runaway path (not “more FDBK”).

**Conflicts with TAPE ECHO** (same detours).

## Knobs

| Knob | Pedal | What it does here |
|---|---|---|
| TIME | CLOCK | ~50–1200 ms; longer also darkens the loft |
| FDBK | SUM | Repeats; alone stays stable (tops ~0.88) |
| GAIN | GAIN | Wet preamp into the write — drive + softclip grit |
| MOD | MOD | Chorus warble on the *read* (~0.5–4 ms, ~0.35 Hz) |
| HAVC | HAVOC | Dead below ~16; then pulls the loop toward runaway, opens the loft, grits the return |
| MIX | MIX | Wet *level over dry* (dry always there); **0 = exact dry** |

Page 2 unused (beat DIV / LIM later).

## Try

1. MIX ~80, FDBK ~70, GAIN 0, MOD 0, HAVC 0 — clean lo-fi echo  
2. Raise GAIN — repeats get crunchier (preamp), not louder dry  
3. MOD 40–80 — gentle detune on the trails  
4. HAVC past ~40 with FDBK mid-high — hold-style runaway; drop HAVC to calm it  

## Proof

`verify_megabyte_cpu` + `make check REMIX=test/megabyte`. Unit: Ilia’s MKII via `CX MB *` remixes (hang on first flash was sample-loop `div`; fixed).
