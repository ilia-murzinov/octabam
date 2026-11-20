"""cx-reson -- cx with RESONATOR instead of VOID.

CX OSC + RESONATOR + SHATTER + SCOPE + DARK + COPY. Stock COMPRESSOR + COMB.
No VOID / SIDECHAIN / STUTTR / SYNTH / TAPE. Stock DELAY kept. PLATE / SPRING harvested.
"""

from remix.schema import Pin, Proof, Remix
from remix.personal import personal_modules

REMIX = Remix(
    name="cx-reson",
    family="mods",
    proof=Proof.RENDER,
    proof_note="CX OSC + RESONATOR + SHATTER + SCOPE + DARK + COPY; stock DELAY; stock COMP; no VOID / SC / STUTTR / SYNTH.",
    doc="CORE + STEM REC + CX OSC + RESONATOR + SHATTER + SCOPE + DARK REV + DELAY + COPY PROJECT + stock COMP.",
    modules=personal_modules(
        "CX OSC",
        before_fx=("SHATTER", "RESONATOR"),
        after_fx=("COMB FILTER",),
    ),
    fx1=(
        "FILTER",
        "EQUALIZER",
        "DJ EQ",
        "PHASER",
        "FLANGER",
        "CHORUS",
        "RESONATOR",
        "COMPRESSOR",
        "LO-FI",
    ),
    fallback="NONE",
    settings={
        ("octabam.usb", "TRACKS"): "OFF",
        ("octabam.usb", "MAIN"): 1,
        ("octabam.usb", "CUE"): 0,
        ("octabam.usb", "MASTER"): 0,
        ("octabam.usb", "IN"): "OFF",
        ("kyoti.mute-modes", "PLACE"): Pin("DRAM"),
    },
)
