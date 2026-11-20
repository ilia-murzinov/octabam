"""cx-stuttr -- cx with STUTTR instead of SHATTER.

CX OSC + VOID + STUTTR + SCOPE + DARK + COPY. Stock COMPRESSOR.
No SHATTER / SIDECHAIN / RESONATOR / SYNTH / TAPE. Stock DELAY kept. PLATE / SPRING harvested.
"""

from remix.schema import Pin, Proof, Remix
from remix.personal import personal_modules

REMIX = Remix(
    name="cx-stuttr",
    family="mods",
    proof=Proof.RENDER,
    proof_note="CX OSC + VOID + STUTTR + SCOPE + DARK + COPY; stock DELAY; stock COMP; no SHATTER / SC / RESONATOR / SYNTH.",
    doc="CORE + STEM REC + CX OSC + VOID + STUTTR + SCOPE + DARK REV + DELAY + COPY PROJECT + stock COMP.",
    modules=personal_modules("CX OSC", before_fx=("STUTTR", "VOID")),
    fx1=(
        "FILTER",
        "EQUALIZER",
        "DJ EQ",
        "PHASER",
        "FLANGER",
        "CHORUS",
        "VOID",
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
