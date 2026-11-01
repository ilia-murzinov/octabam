#!/usr/bin/env python3
"""Bump Tim's stock ML_FM_MAX 1|2 -> 4; assert in-tree CX/synth overrides stay 4."""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIM = ROOT / "modules/synth/upstream/synth/machine_limits.inc"
OVERRIDES = (
    ROOT / "modules/synth/machine_limits.inc",  # optional
    ROOT / "modules/cxosc/machine_limits.inc",
)
WANT = re.compile(r"ML_FM_MAX,\s*4\b")
STOCK = re.compile(r"ML_FM_MAX,\s*[12]\b")

def main() -> None:
    if TIM.is_file():
        text = TIM.read_text(encoding="utf-8")
        if not WANT.search(text):
            if not STOCK.search(text):
                print(f"[FAIL] {TIM}: no ML_FM_MAX 1/2/4", file=sys.stderr); sys.exit(2)
            TIM.write_text(STOCK.sub("ML_FM_MAX, 4", text, count=1), encoding="utf-8")
            print(f"  ML_FM_MAX: bumped {TIM.relative_to(ROOT)} -> 4 (leave dirty)")
        else:
            print(f"  ML_FM_MAX: {TIM.relative_to(ROOT)} = 4")
    for path in OVERRIDES:
        if not path.is_file():
            continue
        if not WANT.search(path.read_text(encoding="utf-8")):
            print(f"[FAIL] {path.relative_to(ROOT)} must be ML_FM_MAX, 4", file=sys.stderr)
            sys.exit(2)
        print(f"  ML_FM_MAX: {path.relative_to(ROOT)} = 4")

if __name__ == "__main__":
    main()
