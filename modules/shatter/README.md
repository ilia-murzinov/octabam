# `shatter` — SHATTER

A per-track crush insert: drive into a wavefolder, hard or soft clip,
combined bit-depth and sample-rate crush, then a feedback loop with a tone
shelf. MODE CHAOS flips feedback polarity from a free-running ramp so the
loop self-modulates into hash and dropouts. MIX 0 is bit-exact dry.

Sits beside CHARACTER (channel-strip dirt) and LOFI2 (modulator + SRR/BRR):
this one is self-modulating destruction.

## Knobs

| page | slot | name | range | what it does |
|---|---|---|---|---|
| 1 | 0 | DRV | 0–127 | pre-gain into the folder; 0 skips drive |
| 1 | 1 | FOLD | 0–127 | wavefolder; 0 skips |
| 1 | 2 | CLIP | 0–127 | clip amount (0 open, 127 brick) |
| 1 | 3 | CRSH | 0–127 | bit + sample-rate crush |
| 1 | 4 | FDBK | 0–127 | feedback around the crush path |
| 1 | 5 | MIX | 0–127 | dry/wet; 0 = exact passthrough |
| 2 | 6 | MODE | HARD / SOFT / CHAOS | clip flavour; CHAOS flips FDBK polarity |
| 2 | 7 | TONE | 0–127 | feedback shelf |
| 2 | 8 | RATE | 0–127 | CHAOS flip rate |

## Measured

Local render gates only (`verify_shatter`). Not flashed.

## On the unit

Not flashed.

## Open

- CHAOS voicing: RATE curve and polarity-flip energy
- How many instances fit on one core at dear settings
- Whether CRSH should split into separate BRR / SRR knobs

## Gates

`tools/verify/verify_shatter.py` (manifest `Gate`): MIX 0 bit-exact; DRV+FOLD
both signs; FDBK raises energy; CHAOS non-silent.
