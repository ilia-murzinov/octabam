# Build

Build a **cx** / **cx-reson** / **cx-vres** image from your own Octatrack
OS 1.40C in this browser tab. The OS file is read locally. Nothing is
uploaded. See [who wrote what](index.md#credits) before you credit a
feature.

Every build includes [Scope](reference/modules/scope.md),
[Copy Project](reference/modules/copy-project.md), DARK REV,
[Complex Oscillator](reference/modules/cxosc.md),
[SEQ](reference/modules/seq.md),
[Persistent Buffers](reference/modules/persistent-buffers.md),
[Rnd Name](reference/modules/rnd-name.md), and stock COMPRESSOR. PLATE and
SPRING are harvested so the inserts fit. The matrix below only shows what
differs: VOID / SHATTER / RESONATOR.

General install, safety and FAQ:
[upstream Build and Install](https://sambanks.github.io/octabam/web-builder.html),
[Safety & FAQ](https://sambanks.github.io/octabam/safety.html).

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

## Install

Card, MIDI and RMX steps match upstream:
[Build and Install](https://sambanks.github.io/octabam/web-builder.html).
Recovery and FAQ:
[Safety & FAQ](https://sambanks.github.io/octabam/safety.html).

**SYSTEM STATUS → OS VERSION** should show `OCTABAM` plus the build tag.
Stock shows `1.40C`.
