A Buchla-style **complex oscillator** as its own machine: two-operator FM,
a sine wavefolder after the mix, modulator feedback, and morphable
sine→saw shapes. ColdFire voice (fork of Tim Hastie's FM SYNTH engine),
not an edit of the SYNTH MACHINE submodule. Mono — one CX OSC track per
Part.

Signal path: **modulator FM → carrier → MIX → FOLD → out**.

## Access

**FUNC + SRC** or **SELECT MACHINE TYPE** → **CX OSC** (sixth row, under
PICKUP). No marker sample. The Part stores FLEX with signature `"CX", 1`.
Choosing a second CX OSC in the same Part hits the mono cap (`CX OSC: 1 MAX`).

After a layout change (or an old Part), **re-select CX OSC** on the track
so the SETUP bytes match the current defaults. Older Parts that still have
SYMM/DEC/FDBK on the PLAYBACK row will sound wrong until you re-pick the
machine.

## PLAYBACK — the voice

Six knobs. Start with **INDX / FOLD / FDBK at 0** if you want a clean sine
carrier, then open one thing at a time.

- **PTCH** — coarse pitch in semitones (−32..+32). Chromatic keys and MIDI
  add on top of this. **FUNC** snaps −32 / 0 / +32.
- **RATO** — modulator∶carrier ratio, free **0.25..4** on the knob. Hold
  **FUNC** and turn to land on the classic FM ratio table (1, 1.5, 2, …).
  At RATO 1 the sidebands sit in octaves; non-integers get clangorous.
- **INDX** — FM depth: how hard the modulator knocks the carrier’s phase.
  Default **0** = no FM (you only hear the carrier / fold path). Turn this
  up before you judge **MMOR** or **FDBK** — both need index to speak.
- **FINE** — cents (−64..+63). The stored byte **64** reads as **0c** on
  the panel. Small detune against another track / the mod.
- **FOLD** — sine wavefolder after the mix (dry/wet). Default **0** =
  bypass. As it rises you get Buchla-style harmonics; the fold is a
  *sine-table* waveshape, so leaving it up while testing **CMOR** can make
  a saw still sound “sine-ish”. Drop FOLD near 0 when auditioning morph.
- **MIX** — what goes into the folder. **0** = carrier only; raise it to
  blend the modulator into the fold input. Plain dial. With MIX 0, FOLD
  only colours the carrier.

FUNC on most knobs jumps in bigger steps.

## SETUP — shape and motion

**FUNC + PLAYBACK** (header reads **SRC SETUP**; machine list on the left).
Slot F is blank.

- **CMOR** — carrier waveshape morph **0..127**: table sine → hard
  (phase-aligned) saw. Audible even with INDX at 0. At 127 you get a bright
  edge; mid values are a continuous blend, not a switch. (A soft DPW
  carrier was tried and withdrawn — crackle under FM, and the hard edge
  is the point.)
- **MMOR** — modulator waveshape morph **0..127**: sine → **bandlimited**
  (DPW) saw. Heard *through* FM, so needs **INDX**. Same idea as CMOR on
  paper, different target on purpose: a hard saw in the modulator makes the
  FM path explode mid-travel; DPW keeps it continuous.
- **DEC** — index envelope after a trig. Low = the FM depth falls away
  quickly; **127 = HOLD** (index stays at the INDX knob). The HOLD icon is
  a single hollow line at the top of the box.
- **SYMM** — fold half-wave skew. **64** = even fold. Below / above tips
  which polarity the folder emphasises (can mute one side). Needs **FOLD**
  up — at FOLD 0 you will not hear it.
- **FDBK** — modulator feedback (the mod listens to itself). Default **0** =
  off. Raise for thicker / growlier FM; feedback always uses the
  *unmorphed* mod sine so a saw edge never re-enters the loop.

## LFO

On a CX OSC track, LFO **PMTR** reaches the SETUP morphs and feedback:

| PMTR | Destination |
|---|---|
| 30 | CMOR |
| 31 | MMOR |
| 32 | SYMM |
| 33 | FDBK |

**DEC is not** an LFO destination — the index envelope stays under the DEC
knob (and locks / scenes).

## Parameters

| Page | Knob | Range | Default | What it does |
|---|---|---|---|---|
| PLAYBACK | PTCH | −32..+32 | 0 | coarse pitch (semitones) |
| PLAYBACK | RATO | 0.25..4 | ~1 | mod∶carrier; FUNC snaps classic ratios |
| PLAYBACK | INDX | 0..127 | 0 | FM depth |
| PLAYBACK | FINE | −64..+63 ¢ | 0c (raw 64) | fine tune |
| PLAYBACK | FOLD | 0..127 | 0 | sine folder dry/wet after MIX |
| PLAYBACK | MIX | 0..127 | 0 | carrier↔mod into the folder |
| SETUP | CMOR | 0..127 | 0 | carrier sine→hard saw |
| SETUP | MMOR | 0..127 | 0 | mod sine→DPW saw (needs INDX) |
| SETUP | DEC | 0..127 | 127 | index env; 127 = HOLD |
| SETUP | SYMM | 0..127 | 64 | fold skew; 64 = even |
| SETUP | FDBK | 0..127 | 0 | mod feedback; 0 = off |

## Playing it

- Trig or chromatic / MIDI notes — mono voice; AMP ATK / HOLD / REL still
  shape level (engine-owned envelope).
- P-locks, scenes, and MIDI CCs hit the PLAYBACK / SETUP bytes like any
  machine.
- A quick listen path: INDX mid, DEC HOLD, FOLD / FDBK / morphs at 0 → then
  open FOLD, then CMOR, then MMOR with INDX still up.
- Pair with stock FX on the track (delay, filter, …) as usual.
- Remixes that ship CX OSC drop SYNTH MACHINE (same ColdFire seat).
