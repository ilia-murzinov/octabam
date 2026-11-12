"""What the site and the web builder publish on this fork.

REMIXES is empty here: no upstream Sam manual. BUILDER_REMIXES drives the
web builder. SITE_MODULES are Ilia's own modules (with usage docs) — the only
module pages this Pages site generates.
"""

VERSION = "v0.4"
REMIXES = ()

# Web builder offers these only. base* / cx-stuttr stay in remixes/ for local flash.
BUILDER_REMIXES = (
    "cx", "cx-reson", "cx-vres",
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

# Every BUILDER_REMIXES image has these; the matrix does not repeat them.
BUILDER_ALWAYS_ON = (
    "SCOPE",
    "COPY PROJECT",
    "DARK REV",
    "CX OSC",
    "SEQ",
    "PERSISTENT BUFFERS",
    "RND NAME",
)

# What differs across the three offered remixes.
BUILDER_FEATURE_ROWS = (
    "VOID",
    "RESONATOR",
    "SHATTER",
)

BUILDER_FEATURES = {
    "cx":       {"VOID", "SHATTER"},
    "cx-reson": {"RESONATOR", "SHATTER"},
    "cx-vres":  {"VOID", "RESONATOR"},
}
