# `resonator` — RESONATOR

FX1 station: a Rings-inspired modal resonator bank. Input excites four
pitched modes that ring and decay. BAR / TUBE / PLATE pick the partial
ratios; FREQ / STRU / DECY / BRIT / POS / MIX shape the voice.

Buffer-free (state in r7). `Claims(fx1_only=True)`: FX2 instances dry-pass;
the FX2 chooser hides the row.

## Knobs

| page | slot | name | range | what it does |
|---|---|---|---|---|
| 1 | 0 | FREQ | 0–127 | fundamental ~40 Hz … ~4 kHz exponential |
| 1 | 1 | STRU | 0–127 | structure: body ratios → stretched harmonics |
| 1 | 2 | DECY | 0–127 | decay; high = longer ring |
| 1 | 3 | BRIT | 0–127 | brightness; low damps high modes more |
| 1 | 4 | POS | 0–127 | strike position + stereo across modes |
| 1 | 5 | MIX | 0–127 | dry/wet; 0 = exact passthrough |
| 2 | 6 | BODY | BAR / TUBE / PLATE | ratio set |

## Measured

- Render gates in `tools/verify/verify_resonator.py` (MIX 0 bit-exact, both
  signs, impulse rings, FX2 dry). Not on hardware.

## On the unit

Not flashed.

## Open

- Hear on a unit; cycle price beside the bus stations.
- Tighten float-vs-DSP error if the gate needs a looser tolerance.

## Gates

`tools/verify/verify_resonator.py` (manifest `Gate`).

## Sources

- Mutable Instruments Rings modal resonator (MIT) — design / voicing credit;
  not a line-for-line port. See `THIRD_PARTY.md`.
- JOS two-zero constant-peak-gain resonator / Spectrum VOWL form (MIT).
