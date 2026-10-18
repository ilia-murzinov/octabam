# `stuttr` — STUTTR

A per-track buffer glitch insert. Input is written into the stock FX
instance ring; after the ring fills (or RATE fires) a slice loops, reverses,
drops, or scrambles. CHNC 0 is dry; MIX 0 is bit-exact dry. Re-select the
effect after a flash if an old Part still has CHNC at 0.

## Knobs

| page | slot | name | range | what it does |
|---|---|---|---|---|
| 1 | 0 | SIZE | 0–127 | slice length (FX2: (kn+1)×32 words; FX1: (kn+1)×8) |
| 1 | 1 | RATE | 0–127 | re-grab clock (slow→fast; SIZE loops between grabs) |
| 1 | 2 | CHNC | 0–127 | 0 = dry; any other = stutter after first grab |
| 1 | 3 | FDBK | 0–127 | recirculate into the write head |
| 1 | 4 | DECY | 0–127 | fade between grabs (0 = hold) |
| 1 | 5 | MIX | 0–127 | dry/wet |
| 2 | 6 | MODE | LOOP / REV / DROP / SCRAM | playback flavour |
| 2 | 7 | SYNC | FREE / 16 / 8 / 4 | internal clock divisions |

## Measured

Local render gates (`verify_stuttr`): SIZE sets spike repeat gaps exactly
((kn+1)×16 samples on FX2). RATE re-grabs; between grabs SIZE loops.

## On the unit

Shipped in `rms` (CHNC default was 0 / RATE too fast until the feel retune).

## Open

- Project-BPM tempo sync

## Gates

`tools/verify/verify_stuttr.py`: MIX 0; CHNC 0 passthrough; LOOP / REV /
SCRAM / DROP; SIZE loop gaps; SIZE changes gap.
