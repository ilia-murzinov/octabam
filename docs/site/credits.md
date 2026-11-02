# Credits

This site is a **personal fork** of
**[octabam](https://github.com/sambanks/octabam)** by
[Sam Banks](https://github.com/sambanks) and many contributors.

The remixer, build system, stock ports, BRAIN / REMIX SWITCH stack, and most
of what ships in every `base*` / `cx*` image are **their work**. This Pages
site only adds usage docs for [modules developed on this fork](reference/modules.md).
It is **not** a replacement for the upstream octabam manual.

| | |
|---|---|
| Upstream | [sambanks/octabam](https://github.com/sambanks/octabam) |
| This fork | [ilia-murzinov/octabam](https://github.com/ilia-murzinov/octabam) |

## Lineage that must stay visible

- **CX OSC** (documented here) is a local machine derived from
  **Tim Hastie**’s FM SYNTH engine (octatrick). It is not an edit of the
  SYNTH MACHINE submodule; Tim’s SYNTH / QUANTIZER / TUNER still ship in
  `base*` and keep their authorship.
- **SCOPE** overrides TUNER’s DOWN+TEMPO entry when both are present — TUNER
  remains Tim’s; SCOPE is an overlay, not a rewrite of Tim’s work.
- Stock FILTER…DELAY, COMPRESSOR, DARK REV, and the rest of Elektron's FX
  remain **Elektron**.

## Everything that ships in `base*` / `cx*`

Generated from the manifests at build time (complete list, not a highlight reel):

--8<-- "reference/_credits-shipped.md"

## Licence

Repository code and documentation: **MIT** (copyright Sam Banks and
contributors — see the [LICENSE](https://github.com/sambanks/octabam/blob/main/LICENSE)
in upstream). Fork changes keep that licence. Elektron's firmware is **not**
distributed; images are built from your own 1.40C.
