"""RESONATOR -- four independent pitched modes, FX1 station.

Each of PIT1..PIT4 sets one mode's pitch (~40 Hz .. ~4 kHz). DECY sets
shared ring time; MIX blends. No body ratios / structure morph — the
four pitches are free.

FX1 only (`Claims(fx1_only=True)`): buffer-free state in r7; an FX2 instance
is a dry pass. Design credit: Mutable Instruments Rings modal resonator (MIT);
filter form shared with Spectrum VOWL (JOS two-zero).
"""
import math as _m

from remix.schema import (BusRole, Category, Claims, DspSection, Formatter, Gate,
                          Harness, Kind, MenuEntry, Module, Param, Proof,
                          YBase)

_FS = 44100.0
_NYQ = _FS * 0.5
_FMIN, _FMAX = 40.0, 4000.0
_PLAIN = Formatter.PLAIN
_BLANK = Param(b"", 0)


def _q(v: float) -> int:
    return max(-(1 << 23), min((1 << 23) - 1, int(round(v * (1 << 23))))) & 0xFFFFFF


# P table (99 words), read through $fab1e0:
#   +0   FREQ_U  pitch as fraction of Nyquist, 40..4000 Hz, 33 knots
#   +33  COS     cos(pi * i/32), i = 0..32 (0 .. Nyquist)
#   +66  R       exp(-pi * bw / fs) for bw 2..400 Hz, 33 knots
FREQ_U = tuple(_q(min(_FMIN * (_FMAX / _FMIN) ** (i / 32) / _NYQ, 0.95))
               for i in range(33))
COS = tuple(_q(_m.cos(_m.pi * i / 32)) for i in range(33))
R_TAB = tuple(_q(_m.exp(-_m.pi * (2.0 * (400.0 / 2.0) ** (i / 32)) / _FS))
              for i in range(33))

MODULE = Module(
    name="resonator",
    key="RESONATOR",
    kind=Kind.DSP_EFFECT,
    category=Category.TRACK,
    author="iliamurzinov",
    author_url="https://github.com/iliamurzinov",
    proof=Proof.RENDER,
    proof_note="its own render gates; not on hardware",
    doc="FX1 station: four independent pitched resonators; FX1 only.",
    menu=MenuEntry(
        fx2_id=0x1b,  # free of stock + shipping modules; 0x1e is selftest fixtures
        donor_desc=0x400d58b8,  # DARK REV
        abbr=b"RESO",
        fullname=b"Resonator",
        build_tag=True,
    ),
    params=(
        Param(b"PIT1", 32, active=True, formatter=_PLAIN,
              doc="mode 1 pitch, ~40 Hz .. ~4 kHz exponential"),
        Param(b"PIT2", 48, active=True, formatter=_PLAIN,
              doc="mode 2 pitch, ~40 Hz .. ~4 kHz exponential"),
        Param(b"PIT3", 64, active=True, formatter=_PLAIN,
              doc="mode 3 pitch, ~40 Hz .. ~4 kHz exponential"),
        Param(b"PIT4", 80, active=True, formatter=_PLAIN,
              doc="mode 4 pitch, ~40 Hz .. ~4 kHz exponential"),
        Param(b"DECY", 100, active=True, formatter=_PLAIN,
              doc="decay: high = longer ring (narrower mode bandwidth)"),
        Param(b"MIX", 64, active=True, formatter=_PLAIN,
              doc="dry/wet; 0 = exact passthrough"),
        _BLANK, _BLANK, _BLANK, _BLANK, _BLANK, _BLANK,
    ),
    dsp=DspSection(
        asm="modules/resonator/resonator.asm",
        ptable=FREQ_U + COS + R_TAB,
        priority=31,
        bus_role=BusRole.NONE,
        ybase=YBase.NEVER,
        r7_latch_slot=None,
        gate_label=None,
    ),
    claims=Claims(fx1_only=True),
    harness=Harness(layout_char="W", is_server=False),
    gates=(Gate("tools/verify/verify_resonator.py", remix_arg=False),),
    dear={"PIT1": 64, "PIT2": 80, "PIT3": 96, "PIT4": 112, "DECY": 127, "MIX": 127},
)
