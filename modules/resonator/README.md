# `resonator` — RESONATOR

FX1 station: four independent pitched resonators. Each of PIT1..PIT4 sets
one mode's pitch; DECY sets shared ring time; MIX blends dry/wet.

Buffer-free (state in r7). `Claims(fx1_only=True)`: FX2 instances dry-pass;
the FX2 chooser hides the row.

## Knobs

| page | slot | name | range | what it does |
|---|---|---|---|---|
| 1 | 0 | PIT1 | 0–127 | mode 1 pitch ~40 Hz … ~4 kHz exponential |
| 1 | 1 | PIT2 | 0–127 | mode 2 pitch |
| 1 | 2 | PIT3 | 0–127 | mode 3 pitch |
| 1 | 3 | PIT4 | 0–127 | mode 4 pitch |
| 1 | 4 | DECY | 0–127 | decay; high = longer ring |
| 1 | 5 | MIX | 0–127 | dry/wet; 0 = exact passthrough |

## Measured

- Render gates in `tools/verify/verify_resonator.py` (MIX 0 bit-exact, both
  signs, impulse rings, FX2 dry). Not on hardware.

## On the unit

Not flashed (feature branch only until fold asked).

## Open

- Hear on a unit; cycle price beside the bus stations.

## Gates

`tools/verify/verify_resonator.py` (manifest `Gate`).

## Sources

- Mutable Instruments Rings modal resonator (MIT) — design / voicing credit;
  not a line-for-line port. See `THIRD_PARTY.md`.
- JOS two-zero constant-peak-gain resonator / Spectrum VOWL form (MIT).
