"""megabyte -- Megabyte replacing stock DELAY, alone.

Runs on the ColdFire in the stock per-track delay rings. Select it in FX2
where DELAY normally appears. PLATE/SPRING/DARK are harvested for the DSP
passthrough words.
"""

from remix.schema import Proof, Remix

REMIX = Remix(
    name="megabyte",
    family="effects",
    proof=Proof.CHECK,
    proof_note="port/build only; verify_megabyte_cpu; not on hardware",
    doc="Megabyte replacing stock DELAY, alone.",
    modules=("MEGABYTE",),
    fallback="NONE",
)
