"""STUTTR -- buffer freeze / slice repeater / dropout glitch.

A per-track insert using the stock FX instance buffer as a short ring.
SIZE sets the slice, RATE the internal clock, CHNC the wet chance, MODE
selects LOOP / REV / DROP / SCRAM. MIX 0 is bit-exact dry. CHNC 0 passes
dry for the glitch stage.
"""

from remix.schema import (BusRole, Category, Claims, DspSection, Formatter, Gate,
                          Harness, Kind, MenuEntry, Module, Param, Proof, YBase)

_P = Formatter.PLAIN
_S = Formatter.STEPPED
_BLANK = Param(b"", 0)

MODULE = Module(
    name="stuttr",
    key="STUTTR",
    kind=Kind.DSP_EFFECT,
    category=Category.TRACK, author="octabam",
    author_url="https://github.com/sambanks/octabam",
    proof=Proof.RENDER, proof_note="local render gates (verify_stuttr)",
    doc="Buffer glitch: freeze, slice-repeat, reverse, dropout, scramble.",
    menu=MenuEntry(
        fx2_id=0x1b,
        donor_desc=0x400d58b8,
        abbr=b"STUT",
        fullname=b"Stuttr",
        build_tag=True,
    ),
    params=(
        Param(b"SIZE", 24, active=True, formatter=_P,
              doc="slice length in words (FX2: (kn+1)*32); short = machine-gun"),
        Param(b"RATE", 72, active=True, formatter=_P,
              doc="how often a new slice is grabbed (slow left, fast right)"),
        Param(b"CHNC", 127, active=True, formatter=_P,
              doc="wet window inside each grab; 0 = dry glitch stage"),
        Param(b"FDBK", 0, active=True, formatter=_P,
              doc="recirculate slice into the write head"),
        Param(b"DECY", 40, active=True, formatter=_P,
              doc="fade of a held slice between grabs"),
        Param(b"MIX", 127, active=True, formatter=_P,
              doc="dry/wet; 0 = exact passthrough"),
        Param(b"MODE", 0, 4, active=True, formatter=_S,
              labels=("LOOP", "REV", "DROP", "SCRAM"),
              doc="forward loop, reverse, gated holes, scramble read"),
        Param(b"SYNC", 0, 4, active=True, formatter=_S,
              labels=("FREE", "16", "8", "4"),
              doc="divisions of the grab clock"),
        _BLANK, _BLANK, _BLANK, _BLANK,
    ),
    mode_slot=6,
    dsp=DspSection(
        asm="modules/stuttr/stuttr.asm",
        priority=19,
        bus_role=BusRole.NONE,
        ybase=YBase.NEVER,
        r7_latch_slot=None,
        gate_label=None,
    ),
    claims=Claims(stock_instance_buffer=True, buffer_words=16384),
    harness=Harness(layout_char="M", is_server=False),
    gates=(Gate("tools/verify/verify_stuttr.py", remix_arg=False),),
    dear={"SIZE": 16, "RATE": 90, "CHNC": 127, "FDBK": 20, "DECY": 30,
          "MIX": 127, "MODE": 0, "SYNC": 0},
)
