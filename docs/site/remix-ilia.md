# Ilia's remixes

Personal octabam stacks on OS 1.40C. Eight images in the
[builder](web-builder.md): **base** (Tim SYNTH) and **cx** (CX OSC), each with
SHATTER / STUTTR / RESONATOR variants.

Always on every image: SCOPE, COPY PROJECT, DARK REV, stock COMPRESSOR, CORE
ColdFire (BRAIN, Kits, scenes, USB MAIN, …). No SIDECHAIN, no TAPE. PLATE and
SPRING are harvested.

## Matrix

| | base | base-stuttr | base-reson | base-vres | cx | cx-stuttr | cx-reson | cx-vres |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| [SCOPE](reference/modules/scope.md) | ● | ● | ● | ● | ● | ● | ● | ● |
| [COPY PROJECT](reference/modules/copy-project.md) | ● | ● | ● | ● | ● | ● | ● | ● |
| DARK REV (stock) | ● | ● | ● | ● | ● | ● | ● | ● |
| [SYNTH](reference/modules/synth.md) | ● | ● | ● | ● | | | | |
| [CX OSC](reference/modules/cxosc.md) | | | | | ● | ● | ● | ● |
| [VOID](reference/modules/void.md) | ● | ● | | ● | ● | ● | | ● |
| [RESONATOR](reference/modules/resonator.md) | | | ● | ● | | | ● | ● |
| [SHATTER](reference/modules/shatter.md) | ● | | ● | | ● | | ● | |
| [STUTTR](reference/modules/stuttr.md) | | ● | | | | ● | | |

## Differentiating modules

| Module | Role |
|---|---|
| [SYNTH](reference/modules/synth.md) | Tim FM / SY machines (`base*`, v2.15, `ML_FM_MAX=4`) |
| [CX OSC](reference/modules/cxosc.md) | Complex oscillator machine (`cx*`) |
| [VOID](reference/modules/void.md) | Noise AM insert; replaces COMB |
| [RESONATOR](reference/modules/resonator.md) | Tuned resonator insert |
| [SHATTER](reference/modules/shatter.md) | Glitch / buffer insert |
| [STUTTR](reference/modules/stuttr.md) | Stutter insert (conflicts with SHATTER) |
| [SCOPE](reference/modules/scope.md) | DOWN+TEMPO scope (owns TUNER detours) |
| [COPY PROJECT](reference/modules/copy-project.md) | CHANGE→FUNC+BANK→COPY |

## Also in every image

CORE utilities that ship with both families (and have manual pages upstream):

[EUCLID FILL](reference/modules/euclid-fill.md) ·
[MUTE MODES](reference/modules/mute-modes.md) ·
[PERSISTENT BUFFERS](reference/modules/persistent-buffers.md) ·
[STEM REC](reference/modules/stems.md) ·
[RND NAME](reference/modules/rnd-name.md) ·
[RELOAD FROM PROJECT](reference/modules/reload-from-project.md) ·
[DIRECT JUMP](reference/modules/direct-jump-kyoti.md) ·
[SCALE QUANTIZER](reference/modules/quantizer.md) ·
[TUNER](reference/modules/tuner.md) ·
[REMIX SWITCH](reference/modules/remix-switch.md)

Full generated index: [Feature directory](reference/modules.md).

## Build

[Ilia's remixes (builder)](web-builder.md) — pick a column, patch your 1.40C in the browser.
