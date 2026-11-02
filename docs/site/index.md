# ilia · octabam

Personal **base** / **cx** remix stacks for the Elektron Octatrack
(OS 1.40C). Built with the [octabam](https://github.com/sambanks/octabam)
remixer by [Sam Banks](https://github.com/sambanks) and many contributors.

Most of each image is their work: the remixer, CORE, Tim Hastie’s machines,
Kyoti’s workflow modules, and the rest credited below. This site is for
building those stacks and reading the fork modules. It is not a replacement
for the upstream octabam manual.

[**Build an image →**](web-builder.md)
· [Credits](#credits)
· [Safety](#safety-and-recovery)

Upstream: [sambanks/octabam](https://github.com/sambanks/octabam).
This fork: [ilia-murzinov/octabam](https://github.com/ilia-murzinov/octabam).

## Unofficial firmware

These images are unofficial community firmware, not made, endorsed or
supported by Elektron. Installing them is generally safe and can be reverted
by reinstalling stock OS (see [Safety and recovery](#safety-and-recovery)).
Elektron is not responsible for any damage to your Octatrack.

The repository licence is MIT
([upstream LICENSE](https://github.com/sambanks/octabam/blob/main/LICENSE)).
Elektron's firmware is not distributed; you build from your own copy of
OS 1.40C.

## Get started

1. Open [Build](web-builder.md), pick a `base*` or `cx*` remix, and make an
   image from your own 1.40C. Nothing is uploaded.
2. Read the module pages in the sidebar — Effects, Machines, Tools — for
   what that image adds.
3. Check [who wrote what](#credits) before you credit a feature.

## What ships

Always on both stacks: [Scope](reference/modules/scope.md),
[Copy Project](reference/modules/copy-project.md), DARK REV, stock
COMPRESSOR. PLATE and SPRING are harvested so the inserts fit.

- **base\*** — Tim Hastie’s SYNTH MACHINE, plus the fork modules.
- **cx\*** — [Cx Osc](reference/modules/cxosc.md) instead of SYNTH MACHINE.

Pick a lettered remix on [Build](web-builder.md), then flash the `.bin` /
`.syx` or boot an `.RMX` on a unit that already runs octabam.

## Lineage that stays visible

- **CX OSC** is a local machine derived from **Tim Hastie**’s FM SYNTH engine
  (octatrick). It is not an edit of the SYNTH MACHINE submodule. Tim’s
  SYNTH MACHINE, SCALE QUANTIZER and TUNER still ship on `base*` and keep
  their authorship.
- **SCOPE** overlays TUNER’s **DOWN+TEMPO** entry when both are present.
  TUNER remains Tim’s; SCOPE is an overlay, not a rewrite.
- Stock FILTER…DELAY, COMPRESSOR, DARK REV and the rest of Elektron's FX
  remain Elektron.

## Credits

Every non-stock module that appears in at least one `base*` / `cx*` image,
plus the modules documented on this site. Authors and URLs come from each
module's `manifest.py`.

--8<-- "reference/_credits-shipped.md"

## Safety and recovery

Read this before flashing. Keep the recovery files and equipment available
whenever you install a modified OS.

### Recovery requirements

Octabam-based images are community maintained and are not supported by
Elektron. Flashing modified firmware carries a risk of data loss or a unit
that cannot boot. A failed flash can leave the installed OS unable to boot
until stock OS is reinstalled.

Recovery needs a working Startup Menu, a DIN MIDI interface, and a copy of
the stock OS. The Startup Menu is separate from the operating system, but
this procedure cannot recover a unit whose Startup Menu or MIDI input is
unavailable.

### Reinstall stock OS over MIDI

1. Power off. Hold **FUNC** and power on → STARTUP MENU.
2. **TRIG 3** → MIDI UPGRADE → "READY TO RECEIVE MIDI UPGRADE".
3. Send `downloads/extracted/OCTATRACK_OS1.40C.syx` (created by `make os`)
   over DIN MIDI with a SysEx app, or run:

   ```bash
   make midi-flash PORT=<port> SYX=downloads/extracted/OCTATRACK_OS1.40C.syx
   ```
4. Wait through PREPARING FLASH → UPDATING FLASH. Do not power off.

If the unit boots far enough to enter USB DISK MODE, you can also install
stock OS from the CF card. The Octatrack USB port cannot send an OS upgrade.

**TRIG 2** → EMPTY RESET clears battery-backed RAM and settings, not the card.

### Resolve a saved-data file warning

If a project file for FX page 2 parameter locks, Kits or MIDI scenes is
unreadable or incompatible, a message names the affected data and file.
This can happen with damaged or incomplete files as well as older formats.
An ordinary stock project without these extra files does not need them.

Press **NO** to dismiss the message and keep the original file protected,
or **YES** to see the options. Turn **LEVEL** to choose, then press **YES**:

| Choice | What happens |
|---|---|
| KEEP FILE / SKIP SAVED DATA | Leaves the original file untouched. Its saved data is unavailable for this session. |
| START FRESH / REPLACE FILE | Continues without the old saved data. The next save replaces the file. For Kits, the project's stock Parts become the starting Kits. |
| BACKUP FILE THEN START FRESH | Starts fresh, but the next save first copies the original to a `.bak` file. |

These choices do not upgrade or recover the old contents. Keep the file if
you want to investigate or recover its data later. Pressing **NO** from the
choices also leaves it protected until the next project load.

### Common questions

**Is this official Elektron firmware?**
No. Nothing here is endorsed by, supported by, or affiliated with Elektron.

**Does flashing touch my card or projects?**
No. An OS upgrade does not touch the CF card. Two exceptions: Kits write a
`kits.work` file into each project they load (a stock OS ignores the file),
and BRAIN writes its own files to the card.

**MKI or MKII?**
Both run the same OS 1.40C file, and both can flash an octabam image.

**Why can I not download a built image?**
A built `.bin` or `.syx` contains Elektron's OS. Distributing it would
distribute their software, so you build it yourself from your own copy.

**Where are hardware failures recorded?**
The [failure register](https://github.com/sambanks/octabam/blob/main/docs/contributing/FAILURE_MODES.md)
records observed failures, causes and fixes. It cannot guarantee that a
particular unit or flash attempt will recover.
