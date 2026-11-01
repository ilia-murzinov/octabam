"""vrcs-cx -- base ColdFire + CX OSC + SC + SHATTER + VOID + RESONATOR + SCOPE.

No SYNTH MACHINE (conflicts with CX OSC). No STUTTR (conflicts with SHATTER).
No DARK REV: SPRING must be fully harvested so SC + VOID + RESONATOR fit.
Stock COMP replaced by SIDECHAIN on FX1. SCOPE: DOWN+TEMPO (owns TUNER
detours). No COPY PROJECT (PROJECT table does not fit with SCOPE).
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
    "PERSISTENT BUFFERS",
    "REMIX SWITCH",
    "SCOPE",
)

REMIX = Remix(
    name="vrcs-cx",
    family="mods",
    proof=Proof.RENDER,
    proof_note="CX OSC + SC + SHATTER + VOID + RESONATOR + SCOPE; no DARK / SYNTH / STUTTR.",
    doc="CORE + STEM REC + CX OSC + sidechain + SHATTER + VOID + RESONATOR + SCOPE. No DARK REV.",
    modules=CORE + (
        "MEMORY",
        "STEM REC",
        "CX OSC",
        "SIDECHAIN_COMPRESSOR",
        "SHATTER",
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
    },
)
