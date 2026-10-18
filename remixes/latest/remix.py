"""latest -- Ilia's flash stack with every open fix + FM SYNTH LFO → VOIC/CHRD.

CORE + STEM REC (AUDIO/STEMS/<project>/time) + COPY PROJECT + RECBUF PERSIST
+ EUCLID FILL / RND NAME / reload CUE+TRACK gate + glitch inserts + synth/FX.
SYNTH MACHINE at fc24064: LFO 1 / LFO 2 assign VOIC and CHRD (LFO 3 muted).
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
    "RECBUF PERSIST",
    "REMIX SWITCH",
)

REMIX = Remix(
    name="latest",
    family="mods",
    proof=Proof.RENDER,
    proof_note="all open fork fixes + FM SYNTH LFO 1/2 → VOIC/CHRD (synth fc24064).",
    doc="CORE + STEM REC (AUDIO/STEMS) + COPY PROJECT + RECBUF PERSIST + SYNTH (LFO→VOIC/CHRD) + sidechain + SHATTER + STUTTR + USB out TRACKS MAIN CUE.",
    modules=CORE + (
        "MEMORY",
        "STEM REC",
        "SYNTH MACHINE",
        "TAPE ECHO",
        "SIDECHAIN_COMPRESSOR",
        "SHATTER",
        "STUTTR",
        "LOFI AMF FIX",
        "FILTER",
        "EQUALIZER",
        "DJ EQ",
        "PHASER",
        "FLANGER",
        "CHORUS",
        "SPATIALIZER",
        "COMB FILTER",
        "LO-FI",
        "DELAY",
        # PLATE REV harvested: its words hold SHATTER + STUTTR (+ sidechain spare)
        "DARK REV",
    ),
    fx1=(
        "FILTER",
        "EQUALIZER",
        "DJ EQ",
        "PHASER",
        "FLANGER",
        "CHORUS",
        "COMB FILTER",
        "SIDECHAIN_COMPRESSOR",
        "LO-FI",
    ),
    fallback="NONE",
    settings={
        ("octabam.usb", "LAYOUT"): Pin("TRACKS MAIN CUE"),
        ("octabam.usb", "INPUTS"): Pin("OFF"),
        ("kyoti.mute-modes", "PLACE"): Pin("DRAM"),
    },
)
