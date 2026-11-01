"""latest -- Ilia's flash stack: Tim v2.22 synth + VOID nbr + RESONATOR.

CORE + STEM REC + COPY PROJECT + PERSISTENT BUFFERS + EUCLID FILL / RND NAME
+ synth/FX + VOID + RESONATOR + sidechain. SYNTH / QUANTIZER at v2.22;
ML_FM_MAX=4. VOID from feature/void-neighbour (SETUP SRC).
No TAPE / SHATTER / STUTTR. No DARK REV (SPRING harvested so VOID + SC +
RESONATOR fit).
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
)

REMIX = Remix(
    name="latest",
    family="mods",
    proof=Proof.RENDER,
    proof_note="v2.22 synth ML_FM_MAX=4 + VOID nbr + RESONATOR; no TAPE / SHATTER / STUTTR / DARK.",
    doc="CORE + STEM REC + SYNTH v2.22 + sidechain + VOID + RESONATOR + USB TRACKS MAIN CUE.",
    modules=CORE + (
        "MEMORY",
        "STEM REC",
        "SYNTH MACHINE",
        "SIDECHAIN_COMPRESSOR",
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
        "RESONATOR",
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
