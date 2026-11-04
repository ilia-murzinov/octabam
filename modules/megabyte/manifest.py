"""MEGABYTE -- Caroline-inspired lo-fi delay replacing stock Echo Freeze DELAY.

ColdFire voice in the stock four-second per-track rings; DSP is a passthrough.
Conflicts with TAPE ECHO (same filter/mix and reset detours).
"""

from remix.schema import (Gate, Category, Proof, BusRole, Detour, DspSection, Harness,
                          Kind, Linked, MenuEntry, Module, Param, YBase, Formatter)

_PLAIN = Formatter.PLAIN

MODULE = Module(
    name="megabyte",
    key="MEGABYTE",
    kind=Kind.HYBRID,
    category=Category.TRACK,
    author="ilia-murzinov",
    author_url="https://github.com/ilia-murzinov",
    proof=Proof.CHECK,
    proof_note="port/build only: verify_megabyte_cpu + make check; not on hardware",
    doc="Lo-fi delay replacing stock DELAY: drive, mod, havoc; CPU rings.",
    menu=MenuEntry(
        fx2_id=0x08,
        replaces="DELAY",
        donor_desc=0x400d4a96,        # stock DELAY descriptor
        abbr=b"MGBY",
        fullname=b"MEGABYTE",
        build_tag=False,
    ),
    params=(
        Param(b"TIME", 64, active=True, formatter=_PLAIN,
              doc="delay ~50..1200 ms; longer darkens loft"),
        Param(b"FDBK", 70, active=True, formatter=_PLAIN,
              doc="stable repeats; use HAVC for runaway"),
        Param(b"GAIN", 50, active=True, formatter=_PLAIN,
              doc="wet preamp into the write (drive + softclip)"),
        Param(b"MOD", 35, active=True, formatter=_PLAIN,
              doc="chorus on the read (~0.5..4 ms)"),
        Param(b"HAVC", 0, active=True, formatter=_PLAIN,
              doc="off below ~16; then runaway pull on feedback"),
        Param(b"MIX", 80, active=True, formatter=_PLAIN,
              doc="wet over dry; 0 is exact dry"),
        Param(), Param(), Param(), Param(), Param(), Param(),
    ),
    dsp=DspSection(
        asm="modules/megabyte/cpu_passthrough.asm",
        priority=14,
        bus_role=BusRole.NONE,
        ybase=YBase.NEVER,
        r7_latch_slot=None,
        gate_label=None,
    ),
    linked=(Linked("megabyte", "modules/megabyte/cpu.s", cpu="5475", dram=True),),
    detours=(Detour(0x40002f44, bytes.fromhex("4feffff048d7003c"),
                   "megabyte", "mb_cpu_reset",
                   "reset Megabyte with stock delay rings", pad_to=8),
             Detour(0x4000361a, bytes.fromhex("2a6f005c2039800000e8"),
                   "megabyte", "mb_cpu_hook",
                   "Megabyte in the stock track-delay path", pad_to=10),),
    conflicts=(
        ("TAPE ECHO", "both own the stock delay filter/mix and reset detours"),
    ),
    harness=Harness(layout_char="5", is_server=False),  # 6 = TAPE ECHO
    gates=(Gate('tools/verify/verify_megabyte_cpu.py', venv=True, stage='image'),),
)
