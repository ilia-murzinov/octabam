"""glitch-sc -- SHATTER + STUTTR + SIDECHAIN_COMPRESSOR (no TAPE ECHO).

Working triple for the TAPE+SC+SHATTER+STUTTR quartet stall
(docs/contributing/FAILURE_MODES.md). SPRING REV harvested for SC's DSP.
"""

from remix.schema import Proof, Remix

REMIX = Remix(
    name="glitch-sc",
    family="effects",
    proof=Proof.RENDER,
    proof_note="working triple: omit TAPE from the quartet",
    doc="SHATTER + STUTTR + SIDECHAIN_COMPRESSOR (no TAPE ECHO).",
    modules=(
        "SHATTER", "STUTTR", "SIDECHAIN_COMPRESSOR",
        "FILTER", "EQUALIZER", "DJ EQ", "PHASER", "FLANGER",
        "CHORUS", "SPATIALIZER", "COMB FILTER", "LO-FI",
        "DELAY", "PLATE REV", "DARK REV",
    ),
    fallback="NONE",
)
