"""glitch-quartet -- TAPE + SC + SHATTER + STUTTR.

Probe for the retracted stall claim (FAILURE_MODES). Harvest PLATE+SPRING
(DARK kept) so SC+SHATTER+STUTTR fit with TAPE.
"""

from remix.schema import Proof, Remix

REMIX = Remix(
    name="glitch-quartet",
    family="effects",
    proof=Proof.RENDER,
    proof_note="port: 200 frames REACHED on RIG (20 Oct 2026); stall claim retracted",
    doc="TAPE ECHO + SIDECHAIN_COMPRESSOR + SHATTER + STUTTR (stall probe).",
    modules=(
        "SHATTER", "STUTTR", "SIDECHAIN_COMPRESSOR", "TAPE ECHO",
        "FILTER", "EQUALIZER", "DJ EQ", "PHASER", "FLANGER",
        "CHORUS", "SPATIALIZER", "COMB FILTER", "LO-FI",
        "DELAY", "DARK REV",
    ),
    fallback="NONE",
)
