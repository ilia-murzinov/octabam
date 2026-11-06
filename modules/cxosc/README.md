# `cxosc` — CX OSC

Buchla-flavoured **complex oscillator** as a machine-list machine (sibling to
SYNTH MACHINE). Local fork of Tim Hastie's FM SYNTH ColdFire engine; not an
edit of the `modules/synth` submodule. Provenance: `NOTICE`, `LICENSE-TIM`,
and the `THIRD_PARTY.md` row.

## Select

**FUNC + SRC** or **SELECT MACHINE TYPE** → **CX OSC** (sixth row). No marker
file. Stored as FLEX with Part signature `"CX", 1`. At most **one CX OSC track
per Part** (`ml_guard` / `ML_FM_MAX 1`).

## PLAYBACK

| Slot | Name | Role |
|------|------|------|
| A | PTCH | Semitones (−32..+32) |
| B | RATO | Mod:carrier ratio (free 0.25..4; FUNC snaps) |
| C | INDX | FM index |
| D | FOLD | Sine fold dry/wet |
| E | FDBK | Modulator feedback |
| F | MIX | Carrier↔mod into fold (0 = carrier) |

### PLAYBACK SETUP (FUNC + PLAYBACK)

| Slot | Name | Role |
|------|------|------|
| A | CMOR | Carrier morph 0..127 (sine → saw) |
| B | MMOR | Modulator morph 0..127 (sine → saw) |
| C | FINE | Cents (−64..+63; raw 64 = 0c) |
| D | DEC | Index envelope; **127 = HOLD** |
| E–F | — | Blank |

LFO PMTR **30 = CMOR**, **31 = MMOR**. Mono only.

## Build

```bash
make check REMIX=cxosc
```
