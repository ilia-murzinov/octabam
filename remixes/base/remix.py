"""base -- Ilia FM flash stack: Tim v2.22 synth + VOID + SHATTER + SCOPE + DARK.

CORE + STEM REC + PERSISTENT BUFFERS + SEQ / RND NAME + synth/FX +
VOID + SHATTER + SCOPE + DARK REV + COPY. SYNTH / QUANTIZER at v2.22;
ML_FM_MAX=4. Stock COMPRESSOR kept (no SIDECHAIN). No TAPE / STUTTR /
RESONATOR. PLATE / SPRING harvested; DARK REV kept.
"""

from remix.schema import Pin, Proof, Remix
from remix.personal import personal_modules

REMIX = Remix(
    name="base",
    family="mods",
    proof=Proof.RENDER,
    proof_note="v2.22 synth ML_FM_MAX=4 + VOID + SHATTER + SCOPE + DARK + COPY; stock COMP; no SC / RESONATOR / TAPE / STUTTR.",
    doc="CORE + STEM REC + SYNTH v2.22 + VOID + SHATTER + SCOPE + DARK REV + COPY PROJECT + stock COMP + USB TRACKS MAIN CUE.",
    modules=personal_modules("SYNTH MACHINE", before_fx=("SHATTER",), after_fx=("VOID",)),
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
