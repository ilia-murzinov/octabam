**SEQ** places Euclidean **sample trigs** and **parameter locks** on one
audio track. Named after the SEQ submenu on Digitakt II / Digitone II. On
Octatrack it is its own window on the track.

Hold a **`[TRACK]`** key and press **`[PAGE]`**. SEQ opens for that track:
title **SEQ**, the rings icon, a stock 3x2 DATA ENTRY grid, a step grid
(hollow = off, solid = on; up to 4 rows of 16 for length 64), and **LEN**
with the **pattern** step count at the bottom right.

It writes **pattern** sequencer data.

## Access

| Gesture | Result |
|---|---|
| **`[TRACK]`** + **`[PAGE]`** | Open SEQ on that track |
| **`[NO]`** | Close the window |
| Bare **`[PAGE]`** | Stock pattern pages / step banks; SEQ stays open |
| Another **`[TRACK]`** while open | Switch SEQ to that track |

SEQ settings save with the **project** / bank.

## DATA ENTRY map

What the window shows (same cells as stock SETUP pages):

| Knob | Label | Role |
|---|---|---|
| **A** | **PULS** | Hit count of the focused lane |
| **B** | **ROT** | Rotation of the focused lane |
| **C** | **LANE** | **TRIG** or **PLCK** |
| **D** | page + param | Which parameter lock to write. Two lines, LFO SETUP **PMTR** style (**AMP** / **VOL**, **SRC** / **PTCH**, …). On **CX OSC** also **SRC** / **CAR** **MOD** **SYMM** **FDBK** **PWM** |
| **E** | **DPTH** | How far locks swing from the Part value (**0** clears that destination) |
| **F** | | Empty |

**LEN** shows the active **pattern** length.

## Mental model

On each track SEQ keeps two kinds of rhythm:

1. **One TRIG lane** for the track. **PULS** / **ROT** (and a free **`[CUE]`** mask) decide where **sample trigs** land.
2. **One PLCK lane per destination.** Knob **D** picks the destination (**AMP** / **VOL**, **SRC** / **PTCH**, …). That destination has its own **PULS**, **ROT**, **DPTH**, and free mask on the track.

**LANE** (**C**) chooses which of those lanes **A** / **B** and the step grid edit. Scroll **D** while **LANE** is **PLCK** to load that destination's saved **PULS** / **ROT** into **A** / **B**. Knob **D** / **E** stay live on **`[YES]`** even when **LANE** is **TRIG**.

So one track can hold sample trigs on one Euclidean, **PTCH** locks on another, **VOL** locks on a third. **`[YES]`** writes the focused lane. On **TRIG** it also places or clears locks for **only the current destination** on those sample-trig steps.

| **LANE** | Grid / A / B | **`[YES]`** |
|---|---|---|
| **TRIG** | Sample-trig Euclidean | Rewrites **sample trigs**; places / reshapes locks for **only the current destination** on those steps; matches that destination's PLCK **PULS** / **ROT** to the TRIG rhythm |
| **PLCK** | That destination's lock Euclidean | Leaves the sample-trig pattern; rewrites **only this destination's** locks (**trigless trigs** where there is no sample trig); clears this destination on misses, including on steps that still have a sample trig |

## Write-only grid

Open and track-switch load the track's saved SEQ settings. The grid shows
those.

**`[YES]`** overwrites from **PULS** / **ROT** (or a **`[CUE]`** mask).

If **LANE** is **TRIG** and the track already has sample trigs, changing
**PULS** / **ROT** / **`[CUE]`** first opens stock **`"ARE YOU SURE?"`**
with **`"EXISTING TRIGS IN THE PATTERN"`** / **`"WILL BE CLEARED ON NEXT FILL"`**.
Dialog **`[YES]`** only unlocks the knobs. Writing the pattern is a second
**`[YES]`**.

**`[CUE]`** keeps **PULS** as density on the focused lane and only picks
*which* steps are on. Editing **PULS** after a free **`[CUE]`** mask
returns to Euclidean.

## Destination and DPTH

Knob **D** picks the lock target. **DPTH**:

- **0.** **`[YES]`** clears that destination
- **SRC** / **PTCH.** Locks stay in scale around the Part's **PLAYBACK** **PTCH**
- **AMP** / **VOL.** Locks sit at or below the Part's **AMP** **VOL**
- Anything else. Locks swing around the Part value by ± **DPTH**

## What YES writes

**LANE = TRIG.** Sample trigs follow **PULS** / **ROT**. Locks for **this
destination** land on those steps (**DPTH** 0 clears them). Other
destination locks stay. If a step loses its sample trig but still holds
another destination, it becomes a **trigless trig** so those locks stay
audible.

**LANE = PLCK.** Sample trigs stay. This destination clears on every miss,
including on sample-trig steps, then writes on PLCK hits (plock-only steps
become **trigless trigs**). **PULS 0** clears this destination across the
pattern. Empty trigless steps drop when nothing else remains on them.

## Defaults

TRIG **PULS** 5, destination **AMP** / **VOL**, **ROT** / **DPTH** / PLCK
**PULS** 0, **LANE** = **TRIG**.

## Examples

In the figures: black = lock on a sample trig; hatch = **trigless trig**;
white = no lock.

### Place sample trigs

Empty track. **LANE** = **TRIG**, **D** = **SRC** / **PTCH**, **DPTH** = 0,
set **PULS**, **`[YES]`**:

![TRIG with DPTH 0 places sample trigs and clears PTCH.](../../img/seq/notes-only.png)

Sample trigs land. Current destination locks clear because **DPTH** is 0.

### Lock pitch on those trigs

**LANE** = **TRIG**, set **PULS** / **ROT**, **D** = **SRC** / **PTCH**,
**DPTH** non-zero, **`[YES]`**. Sample trigs land; **PTCH** locks sit on
those steps; that destination's PLCK **PULS** / **ROT** match the TRIG
rhythm.

### Add volume locks on another rhythm

You already have sample trigs + **PTCH**. Switch to **LANE** = **PLCK**,
**D** = **AMP** / **VOL**, set a different **PULS** / **ROT**, **`[YES]`**:

![PLCK writes only VOL. Sample trigs and PTCH stay.](../../img/seq/stack-vol.png)

**VOL** locks follow that destination's PLCK rhythm (**trigless trigs**
where there is no sample trig). Sample trigs and **PTCH** stay.

### Change the sample-trig rhythm

Sample trigs with **PTCH** + **VOL**. Keep **D** = **SRC** / **PTCH**,
change TRIG **PULS**, **`[YES]`**:

![TRIG YES reshapes PTCH. VOL stays as trigless where sample trigs drop.](../../img/seq/trig-reshape.png)

- **PTCH** (current destination) clears on silent steps and rewrites on the
  new sample trigs.
- **VOL** (other destination) is kept. Where a sample trig disappears but
  **VOL** remains, the step becomes a **trigless trig**.

### Rewrite one destination's locks

**PTCH** was placed from **TRIG**. Switch to **LANE** = **PLCK**, **D** =
**SRC** / **PTCH**, change **ROT**, **`[YES]`**:

![PLCK YES rewrites PTCH. Other destination stacks stay.](../../img/seq/plck-overwrite.png)

- **PTCH** clears on every miss, including on sample trigs that still fire,
  then writes on the new PLCK hits (**trigless trig** if no sample trig).
- Other destinations (**VOL**, filter, …) stay.

### Clear one destination's locks

**LANE** = **PLCK**, that destination's **PULS** = 0, **`[YES]`**:

![PLCK with PULS 0 clears PTCH. Sample trigs and other stacks stay.](../../img/seq/clear-dest.png)

Clears this destination over the pattern length. Sample trigs stay. Orphan
trigless bits drop when nothing else remains on the step.

### Randomize hits with CUE

Focus the lane (**TRIG** or **PLCK**), set **PULS** to the hit count you
want, press **`[CUE]`** (exactly that many hits at random on that lane),
then **`[YES]`** to write.
