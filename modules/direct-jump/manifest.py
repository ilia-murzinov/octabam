"""DIRECT JUMP -- CHAIN AFTER's value 1 becomes DIRECT: a pattern selected
while the sequencer runs starts at the next step, at the step count the old
pattern had reached (the Analog Four / Rytm behaviour), instead of at the
old pattern's end or after its CHAIN AFTER length. Off by
default: the value is an existing, unused position of an existing project
setting, so a project that never selects it plays exactly as stock.

Source: `upstream/` pinned to v2.22 (73686de). Sources unchanged since v9.1;
kept in lockstep with the other Tim modules. Nothing inside `upstream/` is
edited here.
"""

import dataclasses
import pathlib
import runpy

from remix.schema import Category, Proof

_UPSTREAM = pathlib.Path(__file__).resolve().parent / "upstream" / "direct-jump" / "manifest.py"

MODULE = runpy.run_path(str(_UPSTREAM), run_name="remix_manifest_direct_jump")["MODULE"]
# The module table's fields are octabam's (README.md, `make docs`), so they
# are added here rather than in his manifest.
MODULE = dataclasses.replace(
    MODULE, category=Category.MACHINES, author="timhastie/octatrick-modules", author_url="https://github.com/timhastie/octatrick-modules",
    proof=Proof.HARDWARE, proof_note="v2.22 pin (sources unchanged since v9.1); hardware with octatrick on Tim's MKI")
