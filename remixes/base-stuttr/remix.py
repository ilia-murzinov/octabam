"""base-stuttr -- base with STUTTR instead of SHATTER.

Tim v2.22 synth + VOID + STUTTR + SCOPE + DARK + COPY. Stock COMPRESSOR.
No SHATTER / SIDECHAIN / RESONATOR / TAPE. PLATE / SPRING harvested.
"""

from remix.schema import Pin, Proof, Remix
from remix.personal import personal_modules

REMIX = Remix(
    name="base-stuttr",
    family="mods",
    proof=Proof.RENDER,
    proof_note="v2.22 synth + VOID + STUTTR + SCOPE + DARK + COPY; stock COMP; no SHATTER / SC / RESONATOR.",
    doc="CORE + STEM REC + SYNTH v2.22 + VOID + STUTTR + SCOPE + DARK REV + COPY PROJECT + stock COMP.",
    modules=personal_modules("SYNTH MACHINE", before_fx=("STUTTR",), after_fx=("VOID",)),
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
