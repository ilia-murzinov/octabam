"""cx -- Ilia's CX OSC flash stack: SHATTER + VOID + SCOPE + SCREEN + DARK + COPY.

No SYNTH MACHINE (conflicts with CX OSC). No STUTTR (conflicts with SHATTER).
No RESONATOR / SIDECHAIN. Stock DELAY kept. Stock COMPRESSOR kept.
PLATE / SPRING harvested so VOID fits; DARK REV kept. SCOPE: DOWN+TEMPO
(owns TUNER detours). SCREEN: Elektron screenshot SysEx on MIDI OUT.
"""

from remix.schema import Pin, Proof, Remix
from remix.personal import personal_modules

REMIX = Remix(
    name="cx",
    family="mods",
    proof=Proof.RENDER,
    proof_note="CX OSC + SHATTER + VOID + SCOPE + SCREEN + DARK + COPY; stock DELAY; stock COMP; no SC / RESONATOR / SYNTH / STUTTR.",
    doc="CORE + STEM REC + CX OSC + SHATTER + VOID + SCOPE + SCREEN + DARK REV + DELAY + COPY PROJECT + stock COMP.",
    modules=personal_modules(
        "CX OSC", before_fx=("SHATTER", "VOID"), core_extra=("SCREEN",)
    ),
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
