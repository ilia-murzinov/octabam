"""latest -- Ilia's flash stack: Tim v2.15 synth + VOID nbr (SETUP SRC).

CORE + STEM REC + COPY PROJECT + PERSISTENT BUFFERS + EUCLID FILL / RND NAME
+ synth/FX + VOID + sidechain. SYNTH / QUANTIZER at v2.15; ML_FM_MAX=3;
PLACE=DRAM. VOID from feature/void-neighbour (SETUP SRC toggles LFO vs nbr AM).

No TAPE / SHATTER / STUTTR / RESONATOR. No DARK REV (SPRING harvested so
VOID + SC fit).
"""

from remix.schema import Pin, Proof, Remix

CORE = (
    "BRAIN", "STORE", "KITS", "MIDI SCENES", "SCENES P2", "PLOCKS P2",
    "CC MAP", "CC FEEDBACK", "USB",
    "RECORDER LOOP FIX", "BATCH_BUGFIXES", "ERASE_EMPTY_TRIGLESS_LOCKS",
    "QUANTIZE_LIVE_REC_TOGGLE", "REC_TRIG_MUTE", "MUTE_MODES",
    "SCALE QUANTIZER", "TUNER", "DIRECT_JUMP_KYOTI", "RELOAD_FROM_PROJECT",
    "RLEN PLEN",
    "RND NAME",
    "EUCLID FILL",
    "COPY PROJECT",
    "PERSISTENT BUFFERS",
    "REMIX SWITCH",
)

REMIX = Remix(
    name="latest",
    family="mods",
    proof=Proof.RENDER,
    proof_note="v2.15 synth ML_FM_MAX=3 + VOID nbr (SETUP SRC); no TAPE / SHATTER / STUTTR / RESONATOR / DARK.",
    doc="CORE + STEM REC + SYNTH v2.15 + sidechain + VOID + USB TRACKS MAIN CUE.",
    modules=CORE + (
        "MEMORY",
        "STEM REC",
        "SYNTH MACHINE",
        "SIDECHAIN_COMPRESSOR",
        "LOFI AMF FIX",
        "FILTER",
        "EQUALIZER",
        "DJ EQ",
        "PHASER",
        "FLANGER",
        "CHORUS",
        "SPATIALIZER",
        "VOID",
        "LO-FI",
        "DELAY",
    ),
    fx1=(
        "FILTER",
        "EQUALIZER",
        "DJ EQ",
        "PHASER",
        "FLANGER",
        "CHORUS",
        "VOID",
        "SIDECHAIN_COMPRESSOR",
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
        ("timhastie.synth", "PLACE"): "DRAM",
    },
)
