# ilia · octabam

Three Octatrack remixes for live sampling and sound design, all with
[Complex Oscillator](reference/modules/cxosc.md) (panel **CX OSC**). Every
image keeps [Scope](reference/modules/scope.md),
[Copy Project](reference/modules/copy-project.md), DARK REV, stock
COMPRESSOR, [SEQ](reference/modules/seq.md),
[Persistent Buffers](reference/modules/persistent-buffers.md), and
[Rnd Name](reference/modules/rnd-name.md). The builder matrix swaps the
space and glitch slots:
[Void](reference/modules/void.md), [SHATTER](reference/modules/shatter.md),
[Resonator](reference/modules/resonator.md).

Built with [octabam](https://sambanks.github.io/octabam/) from your own
OS 1.40C. This site is the builder and the fork-module notes. The general
manual, safety and FAQ stay upstream.

[**Build an image →**](web-builder.md)
· [Credits](#credits)
· [Upstream manual](https://sambanks.github.io/octabam/)
· [Safety & FAQ](https://sambanks.github.io/octabam/safety.html)

Unofficial community firmware. Not made, endorsed or supported by Elektron.

## What the builder offers

| Remix | Space | Glitch |
|---|---|---|
| **cx** | Void | SHATTER |
| **cx-reson** | Resonator (+ COMB) | SHATTER |
| **cx-vres** | Void + Resonator | — |

Always on: Scope, Copy Project, DARK REV, CX OSC, SEQ, Persistent Buffers,
Rnd Name, stock COMPRESSOR. PLATE and SPRING are harvested so the inserts
fit.

[Build](web-builder.md) flashes a `.bin` / `.syx`, or boots an `.RMX` on a
unit that already runs octabam.

## Why CX OSC

- **Complex Oscillator** is a local two-operator FM machine with a sine
  wavefolder, derived from Tim's FM SYNTH engine. It takes the machine-list
  seat that SYNTH MACHINE would use, so these images ship CX OSC only.
- **Scope** overlays TUNER's **`[DOWN]` + `[TEMPO]`** entry when both are
  present. TUNER remains Tim's; tip images that ship Scope omit TUNER.
- Everything else in CORE (Kits, scenes, USB, Kyoti workflow modules,
  and the rest in [Credits](#credits)) is still those authors' work.

## Credits

Every non-stock module that appears in at least one builder remix, plus
the modules documented on this site. Authors and URLs come from each
module's `manifest.py`.

--8<-- "reference/_credits-shipped.md"
