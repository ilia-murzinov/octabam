"""SYNTH MACHINE -- Tim Hastie FM synth (octatrick-modules v2.22).

PLAYBACK in DRAM (since 2.21), VOIC/CHRD on PLAYBACK SETUP (since 2.17),
TRACK/FOLLOW (2.22). Octabam appends ML_FM_MAX=4.

CORE coexistence: Tim's fl_* (fmlock companion I/O / step-lock hooks) and
fs_* (SETUP scene/Part companion hooks) claim the same sites as STORE,
KITS, BRAIN, PLOCKS P2, SCENES P2, and EVENTS. Those detours are dropped
here so the tip can compose. VOIC/CHRD remain Part SETUP knobs + LFO
PMTR 30/31; per-step fmlock*.work companions and Tim's dedicated SETUP
scene table are not wired on this pin. Revisit when CORE grows a hook
chain for those sites.

Source: `upstream/` pinned to v2.22 (73686de). Nothing inside `upstream/`
is committed edited (build may dirty-bump Tim's ML_FM_MAX 2→4).
"""

import dataclasses
import pathlib
import runpy

from remix.schema import Category, Proof, Store

_UPSTREAM = pathlib.Path(__file__).resolve().parent / "upstream" / "synth" / "manifest.py"
_HERE = pathlib.Path(__file__).resolve().parent

MODULE = runpy.run_path(str(_UPSTREAM), run_name="remix_manifest_synth")["MODULE"]

# Companion-lock / scene I/O: collide with CORE (STORE/KITS/BRAIN/PLOCKS/SCENES/EVENTS).
_DROP_PREFIXES = ("fl_", "fs_")


def _adapt_include(_inc):
    def _wrapped(modules, remix=None, _inc=_inc):
        text = _inc(modules)
        text += "\n" + (_HERE / "machine_limits.inc").read_text()
        return text
    return _wrapped


def _adapt_unit(_unit):
    if callable(getattr(_unit, "include", None)):
        return dataclasses.replace(_unit, include=_adapt_include(_unit.include))
    return _unit


def _keep_detour(d):
    return not any(d.symbol.startswith(p) for p in _DROP_PREFIXES)


# Tim still ships an empty DELAY-tail Keep + boundary CavePatch at
# 0x400d24d0+16 (overflow cursor). After #1023 stock DELAY keeps
# 0x400d24d0..0x400d2ca8, so those claims collide with DELAY in base*.
# Page is already DRAM (fmpage); drop the markers.
MODULE = dataclasses.replace(
    MODULE,
    linked=tuple(_adapt_unit(_u) for _u in MODULE.linked),
    detours=tuple(d for d in MODULE.detours if _keep_detour(d)),
    keeps=(),
    cf_patches=(),
    store=Store("timhastie.synth"),
    category=Category.MACHINES,
    author="timhastie/octatrick-modules",
    author_url="https://github.com/timhastie/octatrick-modules",
    proof=Proof.HARDWARE,
    proof_note="v2.22 engine on Tim's MKI; octabam drops fl_/fs_ hooks for CORE; ML_FM_MAX=4",
)
