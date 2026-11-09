"""ANALOG BD and CX OSC in one image (SPRING harvested for ANALOG BD voices).

Formerly also carried OCTA303; CX OSC now conflicts with OCTA303 (LFO SETUP
PMTR names), so the three-machine image is gone. Same pair as hooks-machines-cx
with SPRING REV dropped for the bassdrum words.
"""

from remix.schema import Proof, Remix

REMIX = Remix(
    name="hooks-machines-all",
    image_name="HOOKS-ALL",
    family="mods", proof=Proof.PORT,
    proof_note="verify_hooks: the bridged machine sites in this image; the two machines' UI gates under the port",
    doc="ANALOG BD and CX OSC in one image: HOOKS gives the track's machine list seven rows, ANALOG BD on row 5 and CX OSC on row 6, and the list scrolls (SPRING harvested).",
    modules=("ANALOG BD", "CX OSC",
             "FILTER", "EQUALIZER", "DJ EQ", "PHASER", "FLANGER",
             "CHORUS", "SPATIALIZER", "COMB FILTER", "COMPRESSOR", "LO-FI",
             "DELAY", "PLATE REV", "DARK REV"),
    fallback="NONE",
)
