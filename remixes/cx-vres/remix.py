"""cx-vres -- cx with RESONATOR instead of SHATTER (VOID kept).

CX OSC + VOID + RESONATOR + SCOPE + DARK + COPY. Stock COMPRESSOR.
No SHATTER / STUTTR / SIDECHAIN / SYNTH / TAPE. PLATE / SPRING harvested.
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
    name="cx-vres",
    family="mods",
    proof=Proof.RENDER,
    proof_note="CX OSC + VOID + RESONATOR + SCOPE + DARK + COPY; stock COMP; no SHATTER / STUTTR / SC / SYNTH.",
    doc="CORE + STEM REC + CX OSC + VOID + RESONATOR + SCOPE + DARK REV + COPY PROJECT + stock COMP.",
    modules=CORE + (
        "MEMORY",
        "STEM REC",
        "CX OSC",
        "RESONATOR",
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
