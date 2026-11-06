A Buchla-flavoured complex oscillator as a machine-list machine: two-operator
FM with a sine wavefolder, modulator feedback, and SETUP morph/fine/dec.
Derived from Tim Hastie's FM SYNTH engine (ColdFire voice), not an edit of the
SYNTH MACHINE submodule.

## Access

**FUNC + SRC** or **SELECT MACHINE TYPE** → **CX OSC** (after the stock
five). No marker sample. The Part stores FLEX with signature `"CX", 1`.
At most one CX OSC track per Part.

## Operation

- PLAYBACK reads PTCH RATO INDX FOLD FDBK MIX.
- PLAYBACK SETUP (FUNC + PLAYBACK) reads CMOR MMOR FINE DEC.
- PTCH is semitones (−32..+32). FINE (SETUP C) is cents (64 = 0c).
- RATO is free 0.25..4 on the knob; FUNC snaps the classic ratio table.
- INDX is FM index; DEC (SETUP D) is its envelope (**127 = HOLD**).
- FOLD is a sine waveshape (dry/wet). FDBK is modulator feedback.
- MIX blends carrier↔mod into the fold. CMOR/MMOR morph sine→saw.
- Mono only. Stock LFO page (PMTR 30/31 = CMOR/MMOR).

## Parameters

| Page | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| PLAYBACK | PTCH | RATO | INDX | FOLD | FDBK | MIX |
| PLAYBACK SETUP | CMOR | MMOR | FINE | DEC | — | — |
