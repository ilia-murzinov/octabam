"""RESONATOR -- Rings-inspired modal bank, FX1 station.

Four parallel constant-peak-gain resonators (JOS / Spectrum VOWL form).
Input excites the modes; FREQ sets the fundamental; BODY picks bar / tube /
plate ratios; STRU morphs toward stretched harmonics; DECY / BRIT set decay
and high-mode damping; POS is strike position + stereo; MIX blends.

FX1 only (`Claims(fx1_only=True)`): buffer-free state in r7; an FX2 instance
is a dry pass. Design credit: Mutable Instruments Rings modal resonator (MIT);
filter form shared with Spectrum VOWL (JOS two-zero).
"""
import math as _m

from remix.schema import (BusRole, Category, Claims, DspSection, Formatter, Gate,
                          Harness, Kind, MenuEntry, ModeView, Module, Param, Proof,
                          YBase)

_FS = 44100.0
_NYQ = _FS * 0.5
_FMIN, _FMAX = 40.0, 4000.0
_PLAIN = Formatter.PLAIN
_STEP = Formatter.STEPPED
_BLANK = Param(b"", 0)


def _q(v: float) -> int:
    return max(-(1 << 23), min((1 << 23) - 1, int(round(v * (1 << 23))))) & 0xFFFFFF


# P table (99 words), read through $fab1e0:
#   +0   FREQ_U  fundamental as fraction of Nyquist, 40..4000 Hz, 33 knots
#   +33  COS     cos(pi * i/32), i = 0..32 (0 .. Nyquist)
#   +66  R       exp(-pi * bw / fs) for bw 2..400 Hz, 33 knots
FREQ_U = tuple(_q(min(_FMIN * (_FMAX / _FMIN) ** (i / 32) / _NYQ, 0.95))
               for i in range(33))
COS = tuple(_q(_m.cos(_m.pi * i / 32)) for i in range(33))
R_TAB = tuple(_q(_m.exp(-_m.pi * (2.0 * (400.0 / 2.0) ** (i / 32)) / _FS))
              for i in range(33))

# BODY ratios as Q8.16-ish Q23 (integer part in high bits): stored as plain
# fractional multiples of f0, capped so 8.933 * 0.95 still fits the cos map.
# Four ratios × three bodies = 12 words after the 99.
def _rq(r: float) -> int:
    return _q(r / 16.0)  # store ratio/16 so 8.933 fits in Q23; asm ×16


RATIOS = (
    # BAR
    _rq(1.0), _rq(2.756), _rq(5.404), _rq(8.933),
    # TUBE
    _rq(1.0), _rq(3.0), _rq(5.0), _rq(7.0),
    # PLATE
    _rq(1.0), _rq(1.594), _rq(2.136), _rq(2.296),
)

MODULE = Module(
    name="resonator",
    key="RESONATOR",
    kind=Kind.DSP_EFFECT,
    category=Category.TRACK,
    author="iliamurzinov",
    author_url="https://github.com/iliamurzinov",
    proof=Proof.RENDER,
    proof_note="its own render gates; not on hardware",
    doc="FX1 station: modal resonator bank (bar / tube / plate); FX1 only.",
    menu=MenuEntry(
        fx2_id=0x1e,  # 0x0a is SHATTER on the latest stack
        donor_desc=0x400d58b8,  # DARK REV
        abbr=b"RESO",
        fullname=b"Resonator",
        build_tag=True,
    ),
    params=(
        Param(b"FREQ", 40, active=True, formatter=_PLAIN,
              doc="fundamental, ~40 Hz .. ~4 kHz exponential"),
        Param(b"STRU", 64, active=True, formatter=_PLAIN,
              doc="structure: body ratios toward stretched harmonics"),
        Param(b"DECY", 80, active=True, formatter=_PLAIN,
              doc="decay: high = longer ring (narrower mode bandwidth)"),
        Param(b"BRIT", 90, active=True, formatter=_PLAIN,
              doc="brightness: low damps high modes more"),
        Param(b"POS", 64, active=True, formatter=_PLAIN,
              doc="strike position + stereo balance across modes"),
        Param(b"MIX", 0, active=True, formatter=_PLAIN,
              doc="dry/wet; 0 = exact passthrough"),
        Param(b"BODY", 0, 3, active=True, formatter=_STEP,
              labels=("BAR", "TUBE", "PLATE"),
              doc="ratio set: free bar, odd tube, plate"),
        _BLANK, _BLANK, _BLANK, _BLANK, _BLANK,
    ),
    mode_slot=6,
    mode_views=(
        ModeView(mode=0,  # BAR
                 defaults={0: 40, 1: 64, 2: 80, 3: 90, 4: 64, 5: 64}),
        ModeView(mode=1,  # TUBE
                 defaults={0: 36, 1: 48, 2: 88, 3: 100, 4: 64, 5: 70}),
        ModeView(mode=2,  # PLATE
                 defaults={0: 48, 1: 80, 2: 72, 3: 80, 4: 72, 5: 80}),
    ),
    dsp=DspSection(
        asm="modules/resonator/resonator.asm",
        ptable=FREQ_U + COS + R_TAB + RATIOS,
        priority=20,
        bus_role=BusRole.NONE,
        ybase=YBase.NEVER,
        r7_latch_slot=None,
        gate_label=None,
    ),
    claims=Claims(fx1_only=True),
    harness=Harness(layout_char="W", is_server=False),
    gates=(Gate("tools/verify/verify_resonator.py", remix_arg=False),),
    dear={"FREQ": 64, "STRU": 127, "DECY": 127, "BRIT": 127, "POS": 127, "MIX": 127, "BODY": 0},
)
