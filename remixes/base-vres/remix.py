"""base-vres -- base with RESONATOR instead of SHATTER (VOID kept).

Tim v2.22 synth + VOID + RESONATOR + SCOPE + DARK + COPY. Stock COMPRESSOR.
No SHATTER / STUTTR / SIDECHAIN / TAPE. PLATE / SPRING harvested.
"""

from remix.schema import Pin, Proof, Remix
from remix.personal import personal_modules

REMIX = Remix(
    name="base-vres",
    family="mods",
    proof=Proof.RENDER,
    proof_note="v2.22 synth + VOID + RESONATOR + SCOPE + DARK + COPY; stock COMP; no SHATTER / STUTTR / SC.",
    doc="CORE + STEM REC + SYNTH v2.22 + VOID + RESONATOR + SCOPE + DARK REV + COPY PROJECT + stock COMP.",
    modules=personal_modules("SYNTH MACHINE", before_fx=("RESONATOR",), after_fx=("VOID",)),
    fx1=(
        "FILTER",
        "EQUALIZER",
        "DJ EQ",
        "PHASER",
        "FLANGER",
        "CHORUS",
        "VOID",
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
