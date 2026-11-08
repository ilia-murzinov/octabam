"""base-reson -- base with RESONATOR instead of VOID.

Tim v2.22 synth + RESONATOR + SHATTER + SCOPE + DARK + COPY. Stock COMPRESSOR
+ COMB FILTER. No VOID / SIDECHAIN / STUTTR / TAPE. PLATE / SPRING harvested.
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
    name="base-reson",
    family="mods",
    proof=Proof.RENDER,
    proof_note="v2.22 synth + RESONATOR + SHATTER + SCOPE + DARK + COPY; stock COMP; no VOID / SC / STUTTR.",
    doc="CORE + STEM REC + SYNTH v2.22 + RESONATOR + SHATTER + SCOPE + DARK REV + COPY PROJECT + stock COMP.",
    modules=CORE + (
        "MEMORY",
        "STEM REC",
        "SYNTH MACHINE",
        "SHATTER",
        "RESONATOR",
        "LOFI AMF FIX",
        "FILTER",
        "EQUALIZER",
        "DJ EQ",
        "PHASER",
        "FLANGER",
        "CHORUS",
        "SPATIALIZER",
        "COMB FILTER",
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
