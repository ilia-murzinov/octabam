"""base-reson -- base with RESONATOR instead of VOID.

Tim v2.22 synth + RESONATOR + SHATTER + SCOPE + DARK + COPY. Stock COMPRESSOR
+ COMB FILTER. No VOID / SIDECHAIN / STUTTR / TAPE. PLATE / SPRING harvested.
"""

from remix.schema import Pin, Proof, Remix
from remix.personal import personal_modules

REMIX = Remix(
    name="base-reson",
    family="mods",
    proof=Proof.RENDER,
    proof_note="v2.22 synth + RESONATOR + SHATTER + SCOPE + DARK + COPY; stock COMP; no VOID / SC / STUTTR.",
    doc="CORE + STEM REC + SYNTH v2.22 + RESONATOR + SHATTER + SCOPE + DARK REV + COPY PROJECT + stock COMP.",
    modules=personal_modules(
        "SYNTH MACHINE",
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
