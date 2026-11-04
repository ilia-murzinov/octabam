"""cx -- Ilia's CX OSC flash stack: SHATTER + VOID + SCOPE + DARK + COPY.

No SYNTH MACHINE (conflicts with CX OSC). No STUTTR (conflicts with SHATTER).
No RESONATOR / SIDECHAIN. MEGABYTE replaces stock DELAY. Stock COMPRESSOR kept.
PLATE / SPRING harvested so VOID fits; DARK REV kept. SCOPE: DOWN+TEMPO
(owns TUNER detours).
"""

from remix.schema import Pin, Proof, Remix

CORE = (
    "BRAIN", "STORE", "KITS", "MIDI SCENES", "SCENES P2", "PLOCKS P2",
    "CC MAP", "CC FEEDBACK", "USB",
    "RECORDER LOOP FIX", "BATCH_BUGFIXES", "ERASE_EMPTY_TRIGLESS_LOCKS",
    "QUANTIZE_LIVE_REC_TOGGLE", "REC_TRIG_MUTE", "MUTE_MODES",
    "SCALE QUANTIZER", "TUNER", "DIRECT_JUMP_KYOTI", "RELOAD_FROM_PROJECT",
    "RLEN PLEN",
    "ATA WRITE GUARD", "EVENTS",
    "RND NAME",
    "EUCLID FILL",
    "COPY PROJECT",
    "PERSISTENT BUFFERS",
    "REMIX SWITCH",
    "SCOPE",
)

REMIX = Remix(
    name="cx",
    family="mods",
    proof=Proof.RENDER,
    proof_note="CX OSC + SHATTER + VOID + SCOPE + DARK + COPY; MEGABYTE for DELAY; stock COMP; no SC / RESONATOR / SYNTH / STUTTR.",
    doc="CORE + STEM REC + CX OSC + SHATTER + VOID + SCOPE + DARK REV + MEGABYTE + COPY PROJECT + stock COMP.",
    modules=CORE + (
        "MEMORY",
        "STEM REC",
        "CX OSC",
        "SHATTER",
        "VOID",
        "LOFI AMF FIX",
        "FILTER",
        "EQUALIZER",
        "DJ EQ",
        "PHASER",
        "FLANGER",
        "CHORUS",
        "SPATIALIZER",
        "COMPRESSOR",
        "LO-FI",
        "MEGABYTE",
        "DARK REV",
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
