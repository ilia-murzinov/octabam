"""What the site and the web builder publish: one release of one remix.

The generated manual, the remix overview table and `tools/web/publish.py` read
this, so a remix that is not listed here (octabam-bus, cxosc-core) has no
manual, no overview row and no builder entry. The remixes stay in the
repository.

On fork/ilia, BUILDER_REMIXES adds personal stacks to the web builder without
putting them in the official manual (gen_pages / gen_manual still use REMIXES).
"""

VERSION = "v0.3"          # the git tag the builder's patches are built from
# Fork tip: no upstream Sam manual. Official sambanks/octabam keeps REMIXES=("octabam",).
REMIXES = ()
# Web builder dropdown (this fork).
BUILDER_REMIXES = (
    "base", "base-stuttr", "base-reson", "base-vres",
    "cx", "cx-stuttr", "cx-reson", "cx-vres",
)

# Feature matrix for the builder page (custom modules only; stock FX omitted).
# Rows top-to-bottom = always-on first, then the axes that differ.
BUILDER_FEATURE_ROWS = (
    "SCOPE",
    "COPY PROJECT",
    "DARK REV",
    "SYNTH",
    "CX OSC",
    "VOID",
    "RESONATOR",
    "SHATTER",
    "STUTTR",
)

BUILDER_FEATURES = {
    "base":        {"SCOPE", "COPY PROJECT", "DARK REV", "SYNTH", "VOID", "SHATTER"},
    "base-stuttr": {"SCOPE", "COPY PROJECT", "DARK REV", "SYNTH", "VOID", "STUTTR"},
    "base-reson":  {"SCOPE", "COPY PROJECT", "DARK REV", "SYNTH", "RESONATOR", "SHATTER"},
    "base-vres":   {"SCOPE", "COPY PROJECT", "DARK REV", "SYNTH", "VOID", "RESONATOR"},
    "cx":          {"SCOPE", "COPY PROJECT", "DARK REV", "CX OSC", "VOID", "SHATTER"},
    "cx-stuttr":   {"SCOPE", "COPY PROJECT", "DARK REV", "CX OSC", "VOID", "STUTTR"},
    "cx-reson":    {"SCOPE", "COPY PROJECT", "DARK REV", "CX OSC", "RESONATOR", "SHATTER"},
    "cx-vres":     {"SCOPE", "COPY PROJECT", "DARK REV", "CX OSC", "VOID", "RESONATOR"},
}
