"""What the site and the web builder publish on this fork.

REMIXES is empty here: no upstream Sam manual. BUILDER_REMIXES drives the
web builder. SITE_MODULES are Ilia's own modules (with usage docs) — the only
module pages this Pages site generates.
"""

VERSION = "v0.4"
REMIXES = ()

BUILDER_REMIXES = (
    "base", "base-stuttr", "base-reson", "base-vres",
    "cx", "cx-stuttr", "cx-reson", "cx-vres",
)

# Module keys authored by Ilia — documented on this site.
SITE_MODULES = (
    "VOID",
    "RESONATOR",
    "SHATTER",
    "STUTTR",
    "CX OSC",
    "SCOPE",
    "COPY PROJECT",
    "SEQ",
    "PERSISTENT BUFFERS",
    "RND NAME",
)

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
