"""base-vres -- base with RESONATOR instead of SHATTER (VOID kept).

Tim v2.22 synth + VOID + RESONATOR + SCOPE + DARK + COPY. Stock COMPRESSOR.
No SHATTER / STUTTR / SIDECHAIN / TAPE. PLATE / SPRING harvested.
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
    name="base-vres",
    family="mods",
    proof=Proof.RENDER,
    proof_note="v2.22 synth + VOID + RESONATOR + SCOPE + DARK + COPY; stock COMP; no SHATTER / STUTTR / SC.",
    doc="CORE + STEM REC + SYNTH v2.22 + VOID + RESONATOR + SCOPE + DARK REV + COPY PROJECT + stock COMP.",
    modules=CORE + (
        "MEMORY",
        "STEM REC",
        "SYNTH MACHINE",
        "RESONATOR",
        "LOFI AMF FIX",
        "FILTER",
        "EQUALIZER",
        "DJ EQ",
        "PHASER",
        "FLANGER",
        "CHORUS",
        "SPATIALIZER",
        "VOID",
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
