A lo-fi delay inspired by Caroline Guitar Company's Megabyte, in place of
FX2 DELAY (Echo Freeze). It runs on the ColdFire CPU in the stock
four-second per-track rings; the DSP side is an empty passthrough. Driven
wet preamp, time warble, and HAVC for runaway repeats.

## Access

Select the track, press FX2, and pick **MEGABYTE** where DELAY was. All six
knobs are on page 1. Conflicts with TAPE ECHO (same ColdFire delay seam).
Build the test remix `test/megabyte`. Not yet hardware-qualified.

## Operation

- TIME spans about 50 ms to 1200 ms.
- GAIN drives the wet path (about +21 dB at 127).
- MOD warbles delay time.
- HAVC pushes feedback toward self-oscillation (hold-havoc on the pedal).
- MIX 0 is exact dry.

## Parameters

| Page | Knob | Range | What it does |
|---|---|---|---|
| 1 | TIME | 0-127 | delay time ~50–1200 ms |
| 1 | FDBK | 0-127 | repeats |
| 1 | GAIN | 0-127 | wet preamp drive |
| 1 | MOD | 0-127 | delay-time warble |
| 1 | HAVC | 0-127 | havoc feedback boost |
| 1 | MIX | 0-127 | wet level; 0 is exact dry |
