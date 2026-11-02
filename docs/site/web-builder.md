# Build

Patch your 1.40C in-browser for a `base*` / `cx*` image. Nothing uploads.
Authors: [Home](index.md).

Always on: [SCOPE](reference/modules/scope.md),
[COPY PROJECT](reference/modules/copy-project.md), DARK REV, stock COMP.
PLATE + SPRING harvested. **base\*** = Tim SYNTH; **cx\*** =
[CX OSC](reference/modules/cxosc.md).

!!! tip "Back up"
    Back up the CF card first. Kits write `kits.work`. Prefer a new project after a first flash of a new stack.

## Need

- `OCTATRACK_OS1.40C_dist.zip` or `.syx` (Elektron)
- Desktop browser
- CF card or DIN MIDI

## Patch

<div id="octabam-builder">This page needs JavaScript.</div>
<script type="module" src="builder/page.js"></script>

| file | use |
|---|---|
| `.bin` | CF root → OS UPGRADE |
| `.syx` | DIN MIDI install |
| `.RMX` | `/BRAIN/REMIXES/` |

Contains Elektron's OS — keep private.

## Install

**CF:** USB DISK MODE → copy `.bin` to root → eject → OS UPGRADE → YES → power-cycle once.

**MIDI:** Elektron's MIDI OS upgrade with the `.syx`.

**RMX:** copy to `/BRAIN/REMIXES/` → PROJ → BRAIN → REMIXES.

## Confirm

STATUS → OS VERSION = `OCTABAM` + tag (stock = `1.40C`). Recovery: [Home § Safety](index.md#safety).
