# Build

Eight **base** / **cx** images — pick one, patch your own 1.40C in the
browser. Nothing is uploaded.

Always on: [SCOPE](reference/modules/scope.md),
[COPY PROJECT](reference/modules/copy-project.md), DARK REV, stock COMP,
plus CORE from [octabam](credits.md). PLATE and SPRING are harvested so the
inserts fit. **base\*** = Tim SYNTH; **cx\*** = [CX OSC](reference/modules/cxosc.md).

!!! tip "Back up your projects"
    Back up the CF card before installing. Kits write `kits.work` into each
    project they load. Prefer new projects after a first flash of a new stack.

## What you need

- `OCTATRACK_OS1.40C_dist.zip` or `OCTATRACK_OS1.40C.syx` from Elektron  
- A current desktop browser  
- CF card (card install) or DIN MIDI interface (MIDI install)

## Patch

<div id="octabam-builder">This page needs JavaScript.</div>
<script type="module" src="builder/page.js"></script>

| file | use |
|---|---|
| `.bin` | CF root → PROJECT → SYSTEM → OS UPGRADE |
| `.syx` | DIN MIDI install |
| `.RMX` | `/BRAIN/REMIXES/` on a unit already running an octabam image |

The files contain Elektron's OS — keep them private.

## Install

### CF card

1. PROJECT → SYSTEM → USB DISK MODE → YES  
2. Copy the `.bin` to the card root  
3. Eject, leave USB DISK MODE  
4. PROJECT → SYSTEM → OS UPGRADE → YES  
5. Power-cycle once after the reboot  

### MIDI

Follow Elektron's MIDI OS upgrade flow with the `.syx`.

### RMX switch

Copy `.RMX` to `/BRAIN/REMIXES/`, then PROJ → BRAIN → REMIXES.

## Confirm

SYSTEM STATUS → OS VERSION should show `OCTABAM` plus the build tag. Stock
shows `1.40C`. Recovery: [Safety](safety.md).
