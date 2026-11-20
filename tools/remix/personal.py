"""Shared core and common FX for Ilia's personal remix variants."""

OCTABAM_CORE = (
    "BRAIN", "STORE", "KITS", "MIDI SCENES", "SCENES P2", "PLOCKS P2",
    "CC MAP", "CC FEEDBACK", "USB",
    "RECORDER LOOP FIX", "BATCH_BUGFIXES", "ERASE_EMPTY_TRIGLESS_LOCKS",
    "QUANTIZE_LIVE_REC_TOGGLE", "REC_TRIG_MUTE", "MUTE_MODES", "PATTERN MUTE",
    "SCALE QUANTIZER", "TUNER", "SCOPE", "DIRECT_JUMP_KYOTI",
    "RELOAD_FROM_PROJECT", "RLEN PLEN", "ATA WRITE GUARD", "ARR ROW CAP",
    "BROWSE PATH GUARD", "EVENTS",
    "LOAD METER", "FRAME GUARD", "REMOTE",
)

PERSONAL_CORE = (
    OCTABAM_CORE[:18]
    + OCTABAM_CORE[19:]
    + ("RND NAME", "SEQ", "COPY PROJECT", "PERSISTENT BUFFERS", "REMIX SWITCH", "SCOPE")
)

COMMON_FX = (
    "LOFI AMF FIX", "FILTER", "EQUALIZER", "DJ EQ", "PHASER", "FLANGER",
    "CHORUS", "SPATIALIZER",
)
COMMON_FX_TAIL = ("COMPRESSOR", "LO-FI", "DELAY", "DARK REV")


def personal_modules(engine, before_fx=(), after_fx=(), core_extra=()):
    """Build the shared personal stack, leaving only engine/effect choices per remix."""
    return (PERSONAL_CORE + tuple(core_extra) + ("MEMORY", "STEM REC", engine)
            + tuple(before_fx) + COMMON_FX + tuple(after_fx) + COMMON_FX_TAIL)
