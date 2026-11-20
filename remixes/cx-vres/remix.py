"""cx-vres -- cx with RESONATOR instead of SHATTER (VOID kept).

CX OSC + VOID + RESONATOR + SCOPE + DARK + COPY. Stock COMPRESSOR. PHASER harvested.
No SHATTER / STUTTR / SIDECHAIN / SYNTH / TAPE. Stock DELAY kept. PLATE / SPRING harvested.
"""

from remix.schema import Pin, Proof, Remix
from remix.personal import personal_modules

REMIX = Remix(
    name="cx-vres",
    family="mods",
    proof=Proof.RENDER,
    proof_note="CX OSC + VOID + RESONATOR + SCOPE + DARK + COPY; stock DELAY; stock COMP; no SHATTER / STUTTR / SC / SYNTH.",
    doc="CORE + STEM REC + CX OSC + VOID + RESONATOR + SCOPE + DARK REV + DELAY + COPY PROJECT + stock COMP.",
    modules=tuple(m for m in personal_modules("CX OSC", before_fx=("RESONATOR", "VOID")) if m != "PHASER"),
    fx1=(
        "FILTER",
        "EQUALIZER",
        "DJ EQ",
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
