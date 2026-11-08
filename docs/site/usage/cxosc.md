A **complex oscillator** in the machine list: two-operator FM into a sine
wavefolder, with modulator feedback and sine→saw morphs on each operator.
No marker sample — it takes the ColdFire voice seat (remixes that ship it
omit SYNTH MACHINE). Up to **four** mono CX OSC tracks per Part.

Signal path every sample:

**modulator → FM into carrier → MIX (carrier↔mod) → FOLD (+ SYMM) → out**

## Limit

A fifth CX OSC track shows `CX OSC: 4 MAX`. Each track is one mono voice.

## Access

### Select

Same sixth list row (**CX OSC**, under PICKUP). Part stores FLEX with
signature `"CX", 1`.

- Double-tap the track key → machine list → **CX OSC** → YES
- **FUNC + SRC** → **SELECT MACHINE TYPE** → **CX OSC** → YES
- From **SRC SETUP**’s left machine list → **CX OSC** → YES

On a track that already has a sample, **FUNC + SRC** may open the sample
list first — **LEFT** reaches the machines.

### Pages

- **PLAYBACK** — PTCH RATO INDX FINE FOLD MIX
- **FUNC + PLAYBACK** — **SRC SETUP** — CMOR MMOR DEC SYMM FDBK (F blank)
- **AMP** — ATK / HOLD / REL (engine-owned). Selecting CX seeds ATK 0 /
  HOLD INF / REL 0 and LEG MONO
- **LFO** — PMTR 30..33 reach SETUP morphs / feedback (below). No VOIC /
  CHRD — LFO 3 stays SPD3 / DEP3

**FUNC** on PLAYBACK knobs: PTCH snaps −32 / 0 / +32; RATO snaps classic
FM ratios.

### Play

Trigs, chromatic keys, or MIDI — last note wins. AMP **HOLD** owns note
length (**HOLD INF** = until STOP). P-locks, scenes, and MIDI CCs hit
PLAYBACK / SETUP like any machine. Stock FX1 / FX2 and quantizer GLIDE
work as usual.

![CX OSC PLAYBACK: PTCH, RATO, INDX, FINE, FOLD, MIX.](../../img/cxosc/source.png)

![CX OSC SETUP: CMOR, MMOR, DEC, SYMM, FDBK (F blank).](../../img/cxosc/setup.png)

## Controls

| Page | Knob | Range | Default | What it does |
|---|---|---|---|---|
| PLAYBACK | PTCH | −32..+32 | 0 | coarse pitch (semitones); chromatic / MIDI add on top |
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

### How the knobs interact

- **Clean sine carrier:** INDX, FOLD, FDBK, CMOR, MMOR at 0.
- **Hear FM:** raise INDX. RATO sets sideband spacing (1 = octaves;
  non-integers clang). MMOR and FDBK are silent until INDX is up.
- **Folder:** FOLD is dry/wet into a sine-table fold. MIX chooses the
  *input* to that fold. SYMM tips which polarity the folder emphasises.
- **Morph while folding:** high FOLD can make a saw-ish CMOR still sound
  sine-ish — drop FOLD near 0 when auditioning CMOR.
- **DEC vs MIX:** DEC is SETUP C; MIX is PLAYBACK F.
- **CMOR vs MMOR:** same idea, different target. Carrier = hard saw on
  the out; modulator = DPW so the FM path stays continuous.

## LFO

| PMTR | Destination |
|---|---|
| 30 | CMOR |
| 31 | MMOR |
| 32 | SYMM |
| 33 | FDBK |

DEC is not an LFO destination — it stays under the DEC knob (and locks /
scenes).

### A short listen path

1. INDX mid, DEC at HOLD, FOLD / FDBK / morphs at 0 — plain FM.
2. Open FOLD, then MIX if you want the mod in the folder.
3. CMOR for carrier brightness; MMOR only with INDX still up.
4. FDBK last for growl.
