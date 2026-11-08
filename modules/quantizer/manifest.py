"""SCALE QUANTIZER -- SCALE / ROOT / GLIDE + TRACK/FOLLOW (v2.22).

Source: `upstream/` pinned to v2.22 with SYNTH MACHINE. Nothing inside
`upstream/` is edited here.
"""

import dataclasses
import pathlib
import runpy

from remix.schema import Category, Gate, Proof

_UPSTREAM = pathlib.Path(__file__).resolve().parent / "upstream" / "quantizer" / "manifest.py"

MODULE = runpy.run_path(str(_UPSTREAM), run_name="remix_manifest_quantizer")["MODULE"]


def _adapt_unit(_unit):
    if callable(getattr(_unit, "include", None)):
        return dataclasses.replace(
            _unit, include=(lambda modules, remix=None, _inc=_unit.include: _inc(modules)))
    return _unit


MODULE = dataclasses.replace(
    MODULE,
    linked=tuple(_adapt_unit(_u) for _u in MODULE.linked),
    gates=MODULE.gates + (Gate("tools/verify/verify_quantizer_ui.py", once=True, venv=True),),
    category=Category.MACHINES, author="timhastie/octatrick-modules",
    author_url="https://github.com/timhastie/octatrick-modules",
    proof=Proof.HARDWARE,
    proof_note="v2.22 with SYNTH MACHINE on Tim's MKI, 1 Nov 2026",
)
