# ilia · octabam

Eight Octatrack remixes for live sampling and sound design: a **base**
family with Tim Hastie's SYNTH MACHINE, and a **cx** family with
[Complex Oscillator](reference/modules/cxosc.md) instead. Every image
keeps [Scope](reference/modules/scope.md),
[Copy Project](reference/modules/copy-project.md), DARK REV and stock
COMPRESSOR, then swaps the space and glitch slots:
[Void](reference/modules/void.md), [Shatter](reference/modules/shatter.md),
[Stuttr](reference/modules/stuttr.md),
[Resonator](reference/modules/resonator.md).

Built with [octabam](https://sambanks.github.io/octabam/) from your own
OS 1.40C. This site is the builder and the fork-module notes. The general
manual, safety and FAQ stay upstream.

[**Build an image →**](web-builder.md)
· [Credits](#credits)
· [Upstream manual](https://sambanks.github.io/octabam/)
· [Safety & FAQ](https://sambanks.github.io/octabam/safety.html)

Unofficial community firmware. Not made, endorsed or supported by Elektron.

## The two families

| | Machine | What you pick next |
|---|---|---|
| **base\*** | Tim's SYNTH MACHINE | Space + glitch: Void / Shatter / Stuttr / Resonator combinations |
| **cx\*** | Complex Oscillator (panel **CX OSC**) | Same space + glitch matrix. No SYNTH MACHINE (same machine-list hooks) |

Always on both: Scope, Copy Project, DARK REV, stock COMPRESSOR. PLATE and
SPRING are harvested so the inserts fit. Stock compressor stays.

Open [Build](web-builder.md), pick a lettered remix, flash the `.bin` /
`.syx`, or boot an `.RMX` on a unit that already runs octabam.

## Why the split exists

- **Complex Oscillator** is a local two-operator FM machine with a sine
  wavefolder, derived from Tim's FM SYNTH engine. It takes the same
  machine-list seat as SYNTH MACHINE, so each image picks one.
- **Scope** overlays TUNER's **DOWN+TEMPO** entry when both are present.
  TUNER remains Tim's.
- Everything else in CORE (Kits, scenes, USB, Kyoti workflow modules,
  and the rest in [Credits](#credits)) is still those authors' work.

## Credits

Every non-stock module that appears in at least one `base*` / `cx*` image,
plus the modules documented on this site. Authors and URLs come from each
module's `manifest.py`.

--8<-- "reference/_credits-shipped.md"
