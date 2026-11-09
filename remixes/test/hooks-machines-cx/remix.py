"""ANALOG BD and CX OSC in one image: HOOKS gives the track's machine list seven rows, ANALOG BD on row 5 and CX OSC on row 6, and the list scrolls.

OCTA303 conflicts with CX OSC (LFO SETUP PMTR names); that pair is refused.
"""

from remix.schema import Proof, Remix

REMIX = Remix(
    name="hooks-machines-cx",
    image_name="HOOKS-CX",
    family="mods", proof=Proof.PORT,
    proof_note="verify_hooks: the bridged machine sites in this image; the two machines' UI gates under the port",
    doc="ANALOG BD and CX OSC in one image: HOOKS gives the track's machine list seven rows, ANALOG BD on row 5 and CX OSC on row 6, and the list scrolls.",
    modules=("ANALOG BD", "CX OSC",
             "FILTER", "EQUALIZER", "DJ EQ", "PHASER", "FLANGER",
             "CHORUS", "SPATIALIZER", "COMB FILTER", "COMPRESSOR", "LO-FI",
             "DELAY", "PLATE REV", "DARK REV"),
    fallback="NONE",
)
