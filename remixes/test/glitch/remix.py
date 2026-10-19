"""SHATTER + STUTTR beside a stock FX chooser."""
from remix.schema import Proof, Remix

REMIX = Remix(
    family="effects",
    proof=Proof.HARDWARE,
    proof_note="Ilia's MKII, BUILD G4, 19 Oct 2026: all SHATTER/STUTTR knobs; "
               "`make check REMIX=glitch`",
    name="glitch",
    doc="Glitch inserts: SHATTER (crush/fold/feedback) and STUTTR (buffer slice).",
    modules=("SHATTER", "STUTTR",
             "FILTER", "EQUALIZER", "DJ EQ", "PHASER", "FLANGER",
             "CHORUS", "SPATIALIZER", "COMB FILTER", "COMPRESSOR", "LO-FI",
             "DELAY", "DARK REV"),
    fallback="NONE",
)
