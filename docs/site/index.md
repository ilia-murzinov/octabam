# ilia · octabam

`base*` / `cx*` stacks for Octatrack OS 1.40C.
Fork of [octabam](https://github.com/sambanks/octabam)
([Sam Banks](https://github.com/sambanks) + contributors).
Remixer + most of every image: theirs. This site docs
[these modules](reference/modules.md) and the [builder](web-builder.md).

| Upstream | [sambanks/octabam](https://github.com/sambanks/octabam) |
| Fork | [ilia-murzinov/octabam](https://github.com/ilia-murzinov/octabam) |

Unofficial — not Elektron. MIT
([LICENSE](https://github.com/sambanks/octabam/blob/main/LICENSE)).
No Elektron firmware in the repo; you supply 1.40C.

- **CX OSC** — Tim Hastie’s FM SYNTH engine (not an edit of SYNTH MACHINE). Tim’s SYNTH / QUANTIZER / TUNER on `base*`.
- **SCOPE** — overlays TUNER’s DOWN+TEMPO; TUNER stays Tim’s.
- Stock FX — Elektron.

## Shipped in `base*` / `cx*`

--8<-- "reference/_credits-shipped.md"

## Safety

Not supported by Elektron. Flashing can brick until you reinstall stock.
Need: working Startup Menu, DIN MIDI, your own `OCTATRACK_OS1.40C.syx`.

### Stock over MIDI

1. Power off. FUNC + power → STARTUP MENU.
2. TRIG 3 → MIDI UPGRADE.
3. Send stock `.syx` over DIN MIDI (or `make midi-flash PORT=… SYX=downloads/extracted/OCTATRACK_OS1.40C.syx`).
4. Wait through PREPARING / UPDATING FLASH. Do not power off.

USB DISK MODE can also take a stock `.bin` on the CF root. The OT USB port cannot send an OS upgrade.

TRIG 2 → EMPTY RESET clears battery-backed RAM/settings, not the card.

### Saved-data warning (page-2 / Kits / scenes)

**NO** keeps the file. **YES** then LEVEL:

| Choice | Effect |
|---|---|
| KEEP FILE / SKIP | File untouched; data unused this session |
| START FRESH / REPLACE | Next save replaces the file |
| BACKUP THEN FRESH | Next save copies original to `.bak` first |

### FAQ

**Official?** No.

**Does flash wipe projects?** No. Exceptions: Kits writes `kits.work` into loaded projects; BRAIN writes its own card files.

**MKI / MKII?** Same 1.40C; both flash.

**Why no downloadable image?** A built `.bin`/`.syx` contains Elektron's OS — you build from your copy.

**Failures:** [register](https://github.com/sambanks/octabam/blob/main/docs/contributing/FAILURE_MODES.md).
