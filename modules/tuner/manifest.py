"""TUNER -- a guitar-tuner readout of the current audio track: hold UP and
press TEMPO for a window with the note, octave, a +-50 cent needle and the
frequency, from the track's post-FX pre-fader audio, detected on the
ColdFire (McLeod NSDF + YIN refine, integer only) in the UI task. TEMPO,
YES, NO or the chord close it; TEMPO alone, FUNC + TEMPO and UP alone stay
stock.

Source: `upstream/` pinned to v2.22 (73686de). Nothing inside `upstream/` is
edited here. When SCOPE is also selected, SCOPE.overrides those three
detours and dispatches UP + TEMPO to tu_open / tu_close.
"""

import dataclasses
import pathlib
import runpy

from remix.schema import Category, Proof

_UPSTREAM = pathlib.Path(__file__).resolve().parent / "upstream" / "tuner" / "manifest.py"

MODULE = runpy.run_path(str(_UPSTREAM), run_name="remix_manifest_tuner")["MODULE"]
# The module table's fields are octabam's (README.md, `make docs`), so they
# are added here rather than in his manifest.
MODULE = dataclasses.replace(
    MODULE, category=Category.MACHINES, author="timhastie/octatrick-modules", author_url="https://github.com/timhastie/octatrick-modules",
    proof=Proof.HARDWARE, proof_note="v2.22 on Tim's MKI, 1 Nov 2026 (DC offset); UP + TEMPO opens and tunes")
