"""RELOAD_FROM_PROJECT -- reload one track's sequence from the CF card without stopping the transport: [PTN] + [TRACK n], or [BANK] + [TRACK n] to re-apply the saved Part.

Source: `upstream/` is Zac Kyoti's repository (Zac-Kyoti/octatrack-kyoti-fw,
submodule, pinned to `329b801`). The declaration is
`upstream/octabam-modules/reload-from-project/manifest.py`: one DRAM unit (`patch_reload3.s`), each re-linked and
compared with the author's own bytes (`reference`) every build. Its source
paths are derived from its own directory, so it is executed here from the
source on disk, as the registry does for every manifest, and this file only
re-exports its MODULE. Nothing inside `upstream/` is edited here.

16 Oct 2026: `patch_reload3.s` beside this file is an octabam-local unit that
gates the `0x40083dc4` detour on the panel PTN held bit. Stock's eight refs to
that site are CUE's held-modifier TRACK slots (`0x400bf122`), so without the
gate `[CUE]+[TRACK n]` toasted `TRK SEQ RELOADED`. Upstream pin unchanged;
this supersedes his Linked source until the same gate lands in kyoti-fw.
"""

import dataclasses
import os
import pathlib
import runpy

from remix.schema import Category, Linked, Proof

_HERE = os.path.relpath(os.path.dirname(os.path.realpath(__file__)))
_UPSTREAM = pathlib.Path(__file__).resolve().parent / "upstream" / "octabam-modules" / "reload-from-project" / "manifest.py"

MODULE = runpy.run_path(str(_UPSTREAM), run_name="remix_manifest_reload_from_project")["MODULE"]
# Fixed unit: CUE sub-map TRACK slots share the PTN-chord detour site.
# Oracle re-linked alone at the author's address (same as upstream REFERENCE).
_FIXED_REF = (0x400d6500, "9fe81ebe6640b9a0365c93880073fed2690b0a8b8962f08be3b41573d642248a")
_FIXED = Linked("rl3", os.path.join(_HERE, "patch_reload3.s"), dram=True,
                reference=_FIXED_REF)
# The module table's fields are octabam's (README.md, `make docs`), so they
# are added here rather than in his manifest. His conflict with OCTAKIT is
# dropped: Octakit is not in octabam since 6 Oct 2026 (KITS replaces it).
MODULE = dataclasses.replace(
    MODULE,
    linked=(_FIXED,),
    conflicts=tuple(c for c in MODULE.conflicts if c[0] != "OCTAKIT"),
    category=Category.UTILITIES,
    author="Zac-Kyoti/octatrack-kyoti-fw",
    author_url="https://github.com/Zac-Kyoti/octatrack-kyoti-fw",
    proof=Proof.HARDWARE,
    proof_note="the author's MKI (standalone image), sequencer and metronome phase kept; "
               "1 Oct 2026 from DRAM in an octabam image with all six KYOTI modules; "
               "16 Oct 2026: [CUE]+[TRACK] no longer reloads (octabam gate on panel PTN bit)",
)
