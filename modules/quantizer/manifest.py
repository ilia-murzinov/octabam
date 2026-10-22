"""SCALE QUANTIZER -- a SCALE row in PROJECT > CONTROL > SEQUENCER (OFF, then
24 scales) and, since 2.9, a ROOT row under it (C .. B): the PTCH knob,
parameter locks and CHROMATIC trig keys snap to the scale built on the root,
key 1 of the CHROMATIC keyboard sounds the root, and a sample track's
keyboard plays the one complete root-to-root octave; a GLIDE row (OFF,
1..127) is the slide time of the synth's and a sample track's legato (the
LEG box on AMP SETUP); polyphonic chromatic keys on a synth track whose VOIC
is 2..4; the three bytes survive a power cycle in battery RAM.

Source: `upstream/` is Tim Hastie's repository (timhastie/octatrick-modules,
submodule, pinned to v2.15 (17ba281) with SYNTH MACHINE). Since 2.13
`qz_octnum` lives at the drawer's common push 0x400449be (Modwerk #264), so
octabam's 2.9-era Keep/pad at that site (#741) is not applied. Nothing inside
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
            _unit, include=(lambda modules, remix, _inc=_unit.include: _inc(modules)))
    return _unit


MODULE = dataclasses.replace(
    MODULE,
    linked=tuple(_adapt_unit(_u) for _u in MODULE.linked),
    gates=MODULE.gates + (Gate("tools/verify/verify_quantizer_ui.py", once=True, venv=True),),
    category=Category.MACHINES, author="timhastie/octatrick-modules",
    author_url="https://github.com/timhastie/octatrick-modules",
    proof=Proof.HARDWARE,
    proof_note="v2.15 with SYNTH MACHINE on Tim's MKI, 18 Oct 2026",
)
