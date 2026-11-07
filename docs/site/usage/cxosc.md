A **complex oscillator** as its own track machine: two-operator FM into a
sine wavefolder, with modulator feedback and sine→saw morphs on each
operator. ColdFire voice (fork of Tim Hastie's FM SYNTH engine) — not an
edit of the SYNTH MACHINE submodule.

Signal path every sample:

**modulator → FM into carrier → MIX (carrier↔mod) → FOLD (+ SYMM) → out**

## Limit

One CX OSC track per Part. Choosing a second shows `CX OSC: 1 MAX`.
Remixes that ship CX OSC omit SYNTH MACHINE (same ColdFire seat).

## Access

Double-tap the track key, or **FUNC + SRC** → **CX OSC** (under PICKUP;
scrolls with other machines). No marker sample — the Part stores FLEX with
signature `"CX", 1`.

After a layout change (or a Part saved under an older knob map),
**re-select CX OSC** on the track so PLAYBACK / SETUP match the current
defaults. Old Parts that still keep SYMM / DEC / FDBK on the PLAYBACK row
will sound wrong until you re-pick the machine.

![CX OSC PLAYBACK: PTCH, RATO, INDX, FINE, FOLD, MIX.](../../img/cxosc/source.png)

![CX OSC SETUP: CMOR, MMOR, DEC, SYMM, FDBK (F blank).](../../img/cxosc/setup.png)

## Controls

| Page | Knob | Range | Default | What it does |
|---|---|---|---|---|
| PLAYBACK | PTCH | −32..+32 | 0 | coarse pitch (semitones); chromatic / MIDI add on top; FUNC snaps −32 / 0 / +32 |
| PLAYBACK | RATO | 0.25..4 | ~1 | modulator∶carrier; free on the knob, **FUNC** snaps classic FM ratios |
| PLAYBACK | INDX | 0..127 | 0 | FM depth; **0 = no FM** (carrier / fold only) |
| PLAYBACK | FINE | −64..+63 ¢ | 0c (raw 64) | cents |
| PLAYBACK | FOLD | 0..127 | 0 | sine-table wavefolder after MIX; **0 = bypass** |
| PLAYBACK | MIX | 0..127 | 0 | what hits the folder: **0 = carrier**, up = blend in the modulator |
| SETUP | CMOR | 0..127 | 0 | carrier morph: table sine → hard (phase-aligned) saw |
| SETUP | MMOR | 0..127 | 0 | modulator morph: sine → bandlimited (DPW) saw — needs **INDX** |
| SETUP | DEC | 0..127 | 127 | index envelope after a trig; **127 = HOLD** (INDX stays with the knob) |
| SETUP | SYMM | 0..127 | 64 | fold half-wave skew; **64 = even**; needs **FOLD** up |
| SETUP | FDBK | 0..127 | 0 | modulator feedback (always the unmorphed mod sine) |
| SETUP | F | — | — | blank |

**FUNC + PLAYBACK** opens SETUP (header **SRC SETUP**).

### How the knobs interact

- **Clean sine carrier:** INDX, FOLD, FDBK, CMOR, MMOR at 0.
- **Hear FM:** raise INDX. RATO sets the sideband spacing (1 = octaves;
  non-integers clang). MMOR and FDBK are silent until INDX is up.
- **Folder:** FOLD is dry/wet into a sine-table fold. MIX chooses the
  *input* to that fold — carrier only, or carrier blended with the
  modulator. SYMM tips which polarity the folder emphasises (can mute
  one side).
- **Morph while folding:** FOLD uses a sine table, so a high FOLD can make
  a saw-ish CMOR still sound “sine-ish”. Drop FOLD near 0 when auditioning
  CMOR.
- **DEC vs MIX:** DEC is **SETUP C**. MIX is **PLAYBACK F**. They are not
  the same knob.
- **CMOR vs MMOR:** same idea (sine→saw), different target. Carrier morph
  is a hard saw (fine on the audible out). Modulator morph is DPW so the
  FM path stays continuous — a hard saw in the mod would explode mid-travel.

## LFO

On a CX OSC track, LFO **PMTR** reaches:

| PMTR | Destination |
|---|---|
| 30 | CMOR |
| 31 | MMOR |
| 32 | SYMM |
| 33 | FDBK |

DEC is not an LFO destination — the index envelope stays under the DEC
knob (and locks / scenes).

## Playing it

- Mono voice: trigs, chromatic keys, or MIDI. Last note wins.
- AMP **ATK / HOLD / REL** still shape level (engine-owned envelope;
  selecting CX seeds ATK 0 / HOLD INF / REL 0 and LEG MONO).
- GLIDE (quantizer row) slews pitch; there is no VOIC / CHRD page — LFO 3
  stays SPD3 / DEP3.
- P-locks, scenes, and MIDI CCs hit PLAYBACK / SETUP like any machine.
- Stock FX1 / FX2 on the track work as usual.

### A short listen path

1. INDX mid, DEC at HOLD, FOLD / FDBK / morphs at 0 — plain FM.
2. Open FOLD, then MIX if you want the mod in the folder.
3. CMOR for carrier brightness; MMOR only with INDX still up.
4. FDBK last for growl.
