A Buchla-style **complex oscillator** as its own machine: two-operator FM,
a sine wavefolder after the mix, modulator feedback, and morphable
sine→saw shapes. ColdFire voice (fork of Tim Hastie's FM SYNTH engine),
not an edit of the SYNTH MACHINE submodule. Mono — one CX OSC track per
Part.

## Access

**FUNC + SRC** or **SELECT MACHINE TYPE** → **CX OSC** (sixth row, under
PICKUP). No marker sample. The Part stores FLEX with signature `"CX", 1`.
Choosing a second CX OSC in the same Part hits the mono cap (`CX OSC: 1 MAX`).

After a layout change (or an old Part), **re-select CX OSC** on the track
so the SETUP bytes match the current defaults.

![CX OSC PLAYBACK: PTCH RATO INDX FINE FOLD MIX.](../../img/cxosc/source.png)

## PLAYBACK — the voice

Six knobs on the PLAYBACK page. Think **carrier + modulator → mix → fold**.

| Knob | Name | What you hear |
|---|---|---|
| A | **PTCH** | Pitch in semitones (−32..+32). Chromatic keys / MIDI add on top. |
| B | **RATO** | Modulator∶carrier ratio, free **0.25..4**. Hold **FUNC** and turn to snap the classic FM ratio table. |
| C | **INDX** | FM depth (how hard the mod knocks the carrier). Default **0** = pure carrier until you open it. |
| D | **FINE** | Cents (−64..+63). Raw **64** reads as **0c**. |
| E | **FOLD** | Sine wavefolder after the mix — dry/wet. Default **0** = clean; turn up for Buchla-style grit. |
| F | **MIX** | What goes into the folder: **0** = carrier only, up = more modulator into the fold. Plain dial. |

FUNC on most knobs jumps in bigger steps (PTCH snaps −32 / 0 / +32).

![SRC SETUP with CX OSC: CMOR MMOR DEC SYMM FDBK.](../../img/cxosc/setup.png)

## SETUP — shape and motion

**FUNC + PLAYBACK** (header reads **SRC SETUP**; machine list on the left).
Slot F is blank.

| Knob | Name | What you hear |
|---|---|---|
| A | **CMOR** | Carrier morph **0..127**: sine → saw. |
| B | **MMOR** | Modulator morph **0..127**: sine → saw. |
| C | **DEC** | Index envelope after a trig. Low = quick fall; **127 = HOLD** (index stays up). |
| D | **SYMM** | Fold half-wave skew. **64** = even; below/above tips the fold. |
| E | **FDBK** | Modulator feedback — the mod listens to itself. Mid (~40) is a useful start; 0 is off. |

## LFO

On a CX OSC track, LFO **PMTR** reaches the SETUP morphs and feedback:

| PMTR | Destination |
|---|---|
| 30 | CMOR |
| 31 | MMOR |
| 32 | SYMM |
| 33 | FDBK |

**DEC is not** an LFO destination (envelope stays under the DEC knob / locks).

## Playing it

- Trig or chromatic / MIDI notes — mono voice; AMP envelope still shapes level.
- P-locks, scenes, and MIDI CCs hit the PLAYBACK / SETUP bytes like any machine.
- Pair with stock FX on the track (delay, filter, …) as usual.
- Remixes that ship CX OSC drop SYNTH MACHINE (same ColdFire seat).
