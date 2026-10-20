"""glitch-sc -- SHATTER + STUTTR + SIDECHAIN_COMPRESSOR (no TAPE ECHO).

PLATE+SPRING harvested so SHATTER/STUTTR/SC fit; DARK REV kept.
"""

from remix.schema import Proof, Remix

REMIX = Remix(
    name="glitch-sc",
    family="effects",
    proof=Proof.RENDER,
    proof_note="builds; DARK kept (PLATE+SPRING harvested)",
    doc="SHATTER + STUTTR + SIDECHAIN_COMPRESSOR (no TAPE ECHO).",
    modules=(
        "SHATTER", "STUTTR", "SIDECHAIN_COMPRESSOR",
        "FILTER", "EQUALIZER", "DJ EQ", "PHASER", "FLANGER",
        "CHORUS", "SPATIALIZER", "COMB FILTER", "LO-FI",
        "DELAY", "DARK REV",
    ),
    fallback="NONE",
)
