# Build and Install

Builds a **base** / **cx** remix ([who wrote what](index.md#credits)) from
your own copy of Octatrack OS 1.40C, in this browser tab. The OS file is
read locally and nothing is uploaded.

Always on: [SCOPE](reference/modules/scope.md),
[COPY PROJECT](reference/modules/copy-project.md), DARK REV, stock COMPRESSOR.
PLATE and SPRING are harvested so the inserts fit.
**base\*** includes Tim Hastie’s SYNTH MACHINE;
**cx\*** includes [CX OSC](reference/modules/cxosc.md) instead.

!!! tip "Back up your projects"
    Back up your CF card before installing, or start new projects after
    installing. Kits write a `kits.work` file into each project they load.
    A project created on the unit after installing needs no preparation.

## What you need

- `OCTATRACK_OS1.40C_dist.zip` from Elektron's Octatrack MKI or MKII
  download page, or the `OCTATRACK_OS1.40C.syx` inside it.
- A current desktop browser, such as Chrome.
- A CompactFlash card in the unit for the card install, or a 5-pin DIN MIDI
  interface into the Octatrack's MIDI IN for the MIDI install.

## Build

<div id="octabam-builder">This page needs JavaScript.</div>
<script type="module" src="builder/page.js"></script>

The build takes a few seconds. The page offers three files:

| file | use |
|---|---|
| `.bin` | Card install: copy to the root of the CF card, then **PROJECT → SYSTEM → OS UPGRADE**. |
| `.syx` | DIN MIDI install. |
| `.RMX` | Optional: boots this image from the card without flashing it. Needs a unit already running an octabam image. Copy to `/BRAIN/REMIXES/`, then **PROJ → BRAIN → REMIXES**. |

The files contain Elektron's OS, so keep them to yourself.

## Install the image

### From the CF card

Use this method when the Octatrack boots normally:

1. On the unit, select **PROJECT → SYSTEM → USB DISK MODE → YES**.
2. Copy the `.bin` file to the root of the mounted CF card, not into a
   folder.
3. Eject the card from the computer, then leave USB DISK MODE on the unit.
   This ensures the copy has finished writing.
4. Select **PROJECT → SYSTEM → OS UPGRADE → YES**, then confirm.
5. Wait for the unit to finish and restart. Power-cycle it once more before
   testing; an OS upgrade does not clear DSP RAM.

### Over DIN MIDI

Follow Elektron's MIDI OS upgrade flow with the `.syx`, or the Startup Menu
path in [Safety and recovery](index.md#safety-and-recovery).

### Switch with an RMX file

Copy the `.RMX` to `/BRAIN/REMIXES/` on a unit that already runs an octabam
image, then **PROJ → BRAIN → REMIXES**.

## Confirm the install

**SYSTEM STATUS → OS VERSION** should show `OCTABAM` plus the build tag.
Stock shows `1.40C`. Recovery: [Safety and recovery](index.md#safety-and-recovery).
