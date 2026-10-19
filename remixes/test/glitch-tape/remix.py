"""glitch-tape -- SHATTER + STUTTR + TAPE ECHO (no SIDECHAIN_COMPRESSOR).

Working triple for the TAPE+SC+SHATTER+STUTTR quartet stall
(docs/contributing/FAILURE_MODES.md). TAPE replaces SPRING REV.
"""

from remix.schema import Proof, Remix

REMIX = Remix(
    name="glitch-tape",
    family="effects",
    proof=Proof.RENDER,
    proof_note="working triple: omit SC from the quartet",
    doc="SHATTER + STUTTR + TAPE ECHO (no SIDECHAIN_COMPRESSOR).",
    modules=(
        "SHATTER", "STUTTR", "TAPE ECHO",
        "FILTER", "EQUALIZER", "DJ EQ", "PHASER", "FLANGER",
        "CHORUS", "SPATIALIZER", "COMB FILTER", "COMPRESSOR", "LO-FI",
        "DELAY", "DARK REV",
    ),
    fallback="NONE",
)
