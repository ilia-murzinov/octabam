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

BUILDER_FEATURE_ROWS = (
    "SCOPE",
    "COPY PROJECT",
    "DARK REV",
    "CX OSC",
    "VOID",
    "RESONATOR",
    "SHATTER",
)

BUILDER_FEATURES = {
    "cx":       {"SCOPE", "COPY PROJECT", "DARK REV", "CX OSC", "VOID", "SHATTER"},
    "cx-reson": {"SCOPE", "COPY PROJECT", "DARK REV", "CX OSC", "RESONATOR", "SHATTER"},
    "cx-vres":  {"SCOPE", "COPY PROJECT", "DARK REV", "CX OSC", "VOID", "RESONATOR"},
}
