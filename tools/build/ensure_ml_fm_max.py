#!/usr/bin/env python3
"""Bump Tim's stock ML_FM_MAX 1|2 -> 4; assert synth override=4, CX OSC=4."""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIM = ROOT / "modules/synth/upstream/synth/machine_limits.inc"
SYNTH = ROOT / "modules/synth/machine_limits.inc"
CXOSC = ROOT / "modules/cxosc/machine_limits.inc"
WANT4 = re.compile(r"ML_FM_MAX,\s*4\b")
STOCK = re.compile(r"ML_FM_MAX,\s*[12]\b")

def main() -> None:
    if TIM.is_file():
        text = TIM.read_text(encoding="utf-8")
        if not WANT4.search(text):
            if not STOCK.search(text):
                print(f"[FAIL] {TIM}: no ML_FM_MAX 1/2/4", file=sys.stderr); sys.exit(2)
            TIM.write_text(STOCK.sub("ML_FM_MAX, 4", text, count=1), encoding="utf-8")
            print(f"  ML_FM_MAX: bumped {TIM.relative_to(ROOT)} -> 4 (leave dirty)")
        else:
            print(f"  ML_FM_MAX: {TIM.relative_to(ROOT)} = 4")
    if SYNTH.is_file():
        if not WANT4.search(SYNTH.read_text(encoding="utf-8")):
            print(f"[FAIL] {SYNTH.relative_to(ROOT)} must be ML_FM_MAX, 4", file=sys.stderr)
            sys.exit(2)
        print(f"  ML_FM_MAX: {SYNTH.relative_to(ROOT)} = 4")
    if CXOSC.is_file():
        if not WANT4.search(CXOSC.read_text(encoding="utf-8")):
            print(f"[FAIL] {CXOSC.relative_to(ROOT)} must be ML_FM_MAX, 4",
                  file=sys.stderr)
            sys.exit(2)
        print(f"  ML_FM_MAX: {CXOSC.relative_to(ROOT)} = 4")

if __name__ == "__main__":
    main()
