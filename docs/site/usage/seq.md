**SEQ** fills a track's pattern with Euclidean trigs and parameter locks.
Audio tracks use sample trigs. MIDI tracks use note trigs. Hold
**`[TRACK]`** and press **`[PAGE]`** to open SEQ for that track.

SEQ shows the title, rings icon, a 3x2 DATA ENTRY grid and a step grid.
Hollow steps are off; solid steps are on. The grid shows up to 64 steps.
**LEN** and the **pattern** length appear at the bottom right.

SEQ writes **pattern** data. Its settings save with the **project** and
bank. Audio and MIDI tracks keep separate SEQ settings.

## Mental model

Each track has a TRIG rhythm and a separate PLCK rhythm for each parameter.

Audio sample trigs play the machine. MIDI note trigs send notes. Each
parameter's PLCK rhythm controls which steps write that parameter's locks.
The rhythms can line up or land on different steps.

Choose **TRIG** to fill the sample or note rhythm. Choose **PLCK** to fill
one parameter's rhythm. A fill changes the selected lane and destination;
other destinations keep their locks.

The grid previews the selected rhythm. Press **`[YES]`** to write it to the
pattern.

## Open and leave

| Gesture | Result |
|---|---|
| **`[TRACK]`** + **`[PAGE]`** | Open SEQ on that track |
| **`[NO]`** | Close the window |
| Bare **`[PAGE]`** | Stock pattern pages / step banks; SEQ stays open |
| Another **`[TRACK]`** while open | Switch SEQ to that track |
| Double-tap **`[TRACK]`** | Stock **QUICK ASSIGN** on audio tracks; stock behavior on MIDI tracks |
| **`[FUNC]`** + **`[TRACK]`** | Stock mute |
| **`[TRACK]`** + **`[PLAY]`** / **`[STOP]`** / **`[BANK]`** | Stock preview / stop / audio editor |
| **`[CUE]`** + **`[TRACK]`** | Stock cue that track |
| Bare **`[CUE]`** (tap) | Random **PULS** hits on the focused lane |
| **`[FUNC]`** + **`[BANK]`** | Open the clear menu |

## Lanes

On each track SEQ keeps:

1. **One TRIG lane.** Where audio **sample trigs** or MIDI **note trigs** land.
2. **One PLCK lane per destination.** Knob **D** picks the destination
   (**AMP** / **VOL**, **SRC** / **PTCH**, or a MIDI parameter). That destination keeps its
   own **PULS**, **ROT**, **DPTH**, and free mask on the track.

**LANE** (**C**) chooses which lane **A** / **B** and the step grid edit.
Scroll **D** on **PLCK** to load that destination's **PULS** / **ROT** into
**A** / **B**.

| **LANE** | What you edit | What **`[YES]`** does |
|---|---|---|
| **TRIG** | Sample-trig or note-trig rhythm | Rewrites the track trigs. Places or clears locks for **only the current destination** on those steps. Copies that destination's PLCK **PULS** / **ROT** to match. |
| **PLCK** | That destination's lock rhythm | Leaves track trigs alone. Rewrites **only this destination**. Misses clear it even on steps with a sample or note trig. Hits without a track trig become **trigless trigs**. |

**D** / **E** stay live on **`[YES]`** even when **LANE** is **TRIG**.

## Controls

SEQ has two control pages. **`[RIGHT]`** opens Harmony when **D** is set to
audio **SRC** / **PTCH** or MIDI **NOTE**. **`[LEFT]`** returns to Rhythm.
The step grid and **LEN** stay visible on both pages.

### Rhythm

The Rhythm page uses the same 3x2 cells as stock SETUP pages:

| Knob | Label | Role |
|---|---|---|
| **A** | **PULS** | Hit count of the focused lane |
| **B** | **ROT** | Rotation of the focused lane |
| **C** | **LANE** | **TRIG** or **PLCK** |
| **D** | Page and parameter | Choose the lock destination. Audio choices include **AMP** / **VOL**, **SRC** / **PTCH**, and CX OSC controls. MIDI choices include **NOTE**, **VEL**, **LEN**, LFO and ARP parameters, pitch bend, channel pressure, and **CC1** through **CC10**. |
| **E** | **DPTH** | Set how far locks vary from the Part value. At 0, the fill clears this destination's locks. **AMP** / **VOL** varies at or below the Part value. |
| **F** | | Empty |

**LEN** shows the active **pattern** length.

### Harmony

![SEQ Harmony on a MIDI track.](../../img/seq/midi-tonal.png)

#### MIDI controls

On MIDI tracks, **A** **SCAL** chooses MAJ, MIN, PENT, DOR, PHR, MIX,
WHOL or CHRO. **B** **ROOT** chooses C through B. **C** **VOIC** chooses
one to four notes. **D** **RANG** sets the pitch span around the Part's
**NOTE**. **E** **PHRS** chooses UP, DOWN, ALT, TRI or WAVE. **F** **CHRD**
chooses a chord shape and inversion.

On audio tracks, Harmony controls the **SRC** / **PTCH** destination.
**SCAL** and **ROOT** set the scale for generated pitch locks. **RANG**
sets their pitch span around the Part's **PLAYBACK PTCH**. At **RANG** 0,
fills use the Part pitch. SEQ's scale is independent of the PROJECT SCALE
QUANTIZER.

On audio tracks, **C** is blank and **F** shows **INTV**. **PHRS** and
**INTV** do not affect audio PTCH fills.

## Writing the pattern

Opening SEQ or switching tracks loads that track's saved settings. The grid
previews those settings; it does not show existing pattern trigs. Press
**`[YES]`** to write the preview to the pattern.

**`[YES]`** overwrites from **PULS** / **ROT**, or from a free **`[CUE]`**
mask.

**TRIG lane, sample trigs already present.** Changing **PULS** / **ROT** /
**`[CUE]`** opens **"ARE YOU SURE?"** with
**`"EXISTING TRIGS IN THE PATTERN"`** /
**`"WILL BE CLEARED ON NEXT FILL"`**. Dialog **`[YES]`** only unlocks the
knobs. Press **`[YES]`** again to write the pattern.

**TRIG lane, note trigs already present.** Changing **PULS** / **ROT** /
**`[CUE]`** opens the same dialog. The first **`[YES]`** applies the pending
change to the preview and unlocks editing. Press **`[YES]`** again to write.
**`[NO]`** cancels the pending change.

**`[CUE]`** tap (release with no **`[TRACK]`**). Keeps **PULS** as the hit
count and picks *which* steps are on at random on the focused lane.
**`[CUE]`** + **`[TRACK]`** is stock cue. Editing **PULS** after a random
tap returns to Euclidean.

**TRIG fill.** Audio sample trigs or MIDI note trigs follow the TRIG lane.
Locks for the selected destination land on those steps. At **DPTH** 0, the
fill clears that destination's locks. Other destination locks stay. If a
step loses its track trig but keeps another destination's lock, it becomes
a **trigless trig**.

**PLCK fill.** Track trigs stay. The selected destination clears on every
miss, including on steps with a sample or note trig, then writes on PLCK
hits. **PULS 0** clears this destination across the pattern. Empty
trigless trigs drop when nothing else remains on them.

## Examples

In the figures: black = lock on a sample trig; hatch = **trigless trig**;
white = no lock.

### Place sample trigs

Empty track. **LANE** = **TRIG**, **D** = **SRC** / **PTCH**, **DPTH** = 0,
set **PULS**, **`[YES]`**:

![TRIG DPTH 0 writes sample trigs and clears PTCH.](../../img/seq/notes-only.png)

Sample trigs land. Current destination locks clear because **DPTH** is 0.

### Lock pitch on those trigs

**LANE** = **TRIG**, set **PULS** / **ROT**, **D** = **SRC** / **PTCH**,
**DPTH** non-zero, **`[YES]`**. Sample trigs land; **PTCH** locks sit on
those steps; that destination's PLCK **PULS** / **ROT** match the TRIG
rhythm.

### Add volume locks on another rhythm

You already have sample trigs + **PTCH**. Switch to **LANE** = **PLCK**,
**D** = **AMP** / **VOL**, set a different **PULS** / **ROT**, **`[YES]`**:

![PLCK writes only VOL; sample trigs and PTCH stay.](../../img/seq/stack-vol.png)

**VOL** locks follow that destination's PLCK rhythm (**trigless trigs**
where there is no sample trig). Sample trigs and **PTCH** stay.

### Change the sample-trig rhythm

Sample trigs with **PTCH** + **VOL**. Keep **D** = **SRC** / **PTCH**,
change TRIG **PULS**, **`[YES]`**:

![TRIG YES reshapes only PTCH; VOL survives as trigless where sample trigs drop.](../../img/seq/trig-reshape.png)

- **PTCH** (current destination) clears on silent steps and rewrites on the
  new sample trigs.
- **VOL** (other destination) is kept. Where a sample trig disappears but
  **VOL** remains, the step becomes a **trigless trig**.

### Rewrite one destination's locks

**PTCH** was placed from **TRIG**. Switch to **LANE** = **PLCK**, **D** =
**SRC** / **PTCH**, change **ROT**, **`[YES]`**:

![PLCK YES clears PTCH on sample-trig misses; other destinations stay.](../../img/seq/plck-overwrite.png)

- **PTCH** clears on every miss, including on sample trigs that still fire,
  then writes on the new PLCK hits (**trigless trig** if no sample trig).
- Other destinations (**VOL**, filter, …) stay.

### Clear one destination's locks

**LANE** = **PLCK**, that destination's **PULS** = 0, **`[YES]`**:

![PLCK PULS 0 clears PTCH; sample trigs and other destinations stay.](../../img/seq/clear-dest.png)

Clears this destination over the pattern length. Sample trigs stay. Orphan
trigless bits drop when nothing else remains on the step.

### Clear from the menu

While SEQ is open, press **`[FUNC]`** + **`[BANK]`**. Choose a row and
press **`[YES]`**. The clear happens immediately and SEQ returns.

| Row | What clears |
|---|---|
| **CLEAR DEST** | The current destination's locks and its PLCK settings |
| **CLEAR ALL DEST** | Every SEQ destination's locks and PLCK settings on this track |
| **CLEAR ALL+TRIGS** | All of the above, plus sample trigs on this track. TRIG returns to **PULS** 5 and **ROT** 0 |

The first two rows keep track trigs. **CLEAR ALL+TRIGS** clears audio
sample trigs or MIDI note trigs. Steps with no track trig or remaining
locks become empty. Press **`[NO]`** to cancel and return to SEQ. Pressing
**`[FUNC]`** + **`[BANK]`** again also closes the menu.

### Place random trigs

Focus the lane (**TRIG** or **PLCK**), set **PULS** to the hit count you
want, tap **`[CUE]`** (exactly that many hits at random on that lane),
then **`[YES]`** to write.

### Write MIDI chords

Set the MIDI track's output channel in **NOTE SETUP**, opened with
**`[FUNC]`** + **`[SRC]`** or a double-tap of **`[SRC]`**. Set the Part's
**NOTE** to C3. In SEQ, select **TRIG**, choose **NOTE** with **D**, and set
**PULS** and a non-zero **DPTH**. Press **`[RIGHT]`**, choose MAJ for
**SCAL**, C for **ROOT**, set **RANG** to 0, **VOIC** to 3 and **CHRD** to
MAJ0. Press **`[YES]`** to write C3, E3 and G3 on each hit.

Set **VOIC** to 1 and fill again to write single notes and clear unused
extra-voice locks. USB MIDI output is available when the remix includes
USB MIDI and the Octatrack is outside USB DISK MODE.
