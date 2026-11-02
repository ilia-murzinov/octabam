# ilia · octabam

Personal **base** / **cx** remix stacks for the Octatrack (OS 1.40C), built
with [octabam](https://sambanks.github.io/octabam/). This site covers the
fork modules and the builder for these stacks — not the general octabam
manual.

[**Build an image →**](web-builder.md)
· [Credits](#credits)
· [Upstream manual](https://sambanks.github.io/octabam/)
· [Safety & FAQ](https://sambanks.github.io/octabam/safety.html)

Unofficial community firmware; not made, endorsed or supported by Elektron.
Licence, recovery, and the usual questions live on the
[upstream site](https://sambanks.github.io/octabam/).

## Get started

1. Open [Build](web-builder.md), pick a `base*` or `cx*` remix, and make an
   image from your own 1.40C. Nothing is uploaded.
2. Read Effects, Machines and Tools in the sidebar for what that image adds.
3. Check [who wrote what](#credits) before you credit a feature.

## What ships

Always on both stacks: [Scope](reference/modules/scope.md),
[Copy Project](reference/modules/copy-project.md), DARK REV, stock
COMPRESSOR. PLATE and SPRING are harvested so the inserts fit.

- **base\*** — Tim Hastie’s SYNTH MACHINE, plus the fork modules.
- **cx\*** — [Cx Osc](reference/modules/cxosc.md) instead of SYNTH MACHINE.

## Lineage that stays visible

- **CX OSC** is a local machine derived from **Tim Hastie**’s FM SYNTH engine
  (octatrick). It is not an edit of the SYNTH MACHINE submodule. Tim’s
  SYNTH MACHINE, SCALE QUANTIZER and TUNER still ship on `base*` and keep
  their authorship.
- **SCOPE** overlays TUNER’s **DOWN+TEMPO** entry when both are present.
  TUNER remains Tim’s; SCOPE is an overlay, not a rewrite.

## Credits

Every non-stock module that appears in at least one `base*` / `cx*` image,
plus the modules documented on this site. Authors and URLs come from each
module's `manifest.py`.

--8<-- "reference/_credits-shipped.md"
