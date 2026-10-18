"""minimal -- CORE + synth stack + STEM REC + glitch inserts.

octabam-core's ColdFire set (BRAIN, STORE, KITS, …) with the synth/FX
selection from the old minimal remix (SYNTH, TAPE ECHO, sidechain, USB out
TRACKS MAIN CUE) and STEM REC (UP+REC own window). MEMORY for STEM's
DramRegions. SHATTER + STUTTR for glitch. No USB in. STEM no longer owns
the MAIN MENU root, so BRAIN coexists.
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
    "REMIX SWITCH",
)

REMIX = Remix(
    name="minimal",
    family="mods",
    proof=Proof.RENDER,
    proof_note="CORE + Dark Rev, Tape Echo, FM synth, sidechain, SHATTER, STUTTR, USB out TRACKS MAIN CUE, STEM REC.",
    doc="CORE (BRAIN…) + Dark Rev + Tape Echo + SYNTH + sidechain + SHATTER + STUTTR + USB out TRACKS MAIN CUE + STEM REC; no USB in.",
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
