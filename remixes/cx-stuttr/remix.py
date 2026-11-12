"""cx-stuttr -- cx with STUTTR instead of SHATTER.

CX OSC + VOID + STUTTR + SCOPE + DARK + COPY. Stock COMPRESSOR.
No SHATTER / SIDECHAIN / RESONATOR / SYNTH / TAPE. Stock DELAY kept. PLATE / SPRING harvested.
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
    "SEQ",
    "COPY PROJECT",
    "PERSISTENT BUFFERS",
    "REMIX SWITCH",
    "SCOPE",
)

REMIX = Remix(
    name="cx-stuttr",
    family="mods",
    proof=Proof.RENDER,
    proof_note="CX OSC + VOID + STUTTR + SCOPE + DARK + COPY; stock DELAY; stock COMP; no SHATTER / SC / RESONATOR / SYNTH.",
    doc="CORE + STEM REC + CX OSC + VOID + STUTTR + SCOPE + DARK REV + DELAY + COPY PROJECT + stock COMP.",
    modules=CORE + (
        "MEMORY",
        "STEM REC",
        "CX OSC",
        "STUTTR",
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
        "DELAY",
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
