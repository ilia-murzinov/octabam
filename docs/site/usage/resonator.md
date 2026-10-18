A modal resonator bank. Input excites four pitched modes that ring and
decay. BODY picks bar, tube or plate ratios; FREQ sets the fundamental;
STRU / DECY / BRIT / POS shape the voice; MIX blends.

## Access

FX1 only: select the track, press FX1, and pick RESONATOR. Page 1 holds the
six performance knobs; page 2 holds BODY. The FX2 chooser does not list it
(id 0x1e); an FX2 instance is a dry pass.

## Operation

- FREQ sets the fundamental (~40 Hz to ~4 kHz).
- STRU morphs the BODY ratios toward stretched harmonics.
- DECY high = longer ring; BRIT low damps the high modes more.
- POS is strike position and stereo balance across modes.
- MIX 0 is an exact passthrough.

## Parameters

| Knob | Range | Default | What it does |
|---|---|---|---|
| FREQ | 0..127 | 40 | fundamental, ~40 Hz … ~4 kHz |
| STRU | 0..127 | 64 | structure: body → stretched harmonics |
| DECY | 0..127 | 80 | decay; high = longer ring |
| BRIT | 0..127 | 90 | brightness; low damps high modes |
| POS | 0..127 | 64 | strike position + stereo |
| MIX | 0..127 | 0 | dry/wet; 0 = exact passthrough |
| BODY | BAR / TUBE / PLATE | BAR | ratio set |
