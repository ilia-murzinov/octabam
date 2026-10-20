"""glitch-tape -- SHATTER + STUTTR + TAPE ECHO (no SIDECHAIN_COMPRESSOR).

TAPE replaces SPRING REV; DARK REV kept.
"""

from remix.schema import Proof, Remix

REMIX = Remix(
    name="glitch-tape",
    family="effects",
    proof=Proof.RENDER,
    proof_note="builds; DARK kept",
    doc="SHATTER + STUTTR + TAPE ECHO (no SIDECHAIN_COMPRESSOR).",
    modules=(
        "SHATTER", "STUTTR", "TAPE ECHO",
        "FILTER", "EQUALIZER", "DJ EQ", "PHASER", "FLANGER",
        "CHORUS", "SPATIALIZER", "COMB FILTER", "COMPRESSOR", "LO-FI",
        "DELAY", "DARK REV",
    ),
    fallback="NONE",
)
