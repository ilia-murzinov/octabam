#!/usr/bin/env python3
"""SEQ port scenarios from docs/site/usage/seq.md (MenuPort, MKII).

Primes track-0 bank/plock state, presses YES / FUNC+BANK, checks pattern
bytes. Requires out/mainos_bus.bin + ot_emu (REMIX with SEQ, e.g. cx).
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "tools/verify"), str(ROOT / "tools/panel")]

from stems_panel import MenuPort  # noqa: E402

IMAGE = ROOT / "out/mainos_bus.bin"
CARD = ROOT / "out/_seq_scenarios_card.img"
MAP = ROOT / "out/platform/runtime/runtime.map"
TEMPLATE = ROOT / "template_project"

DBPTR_ADDR = 0x46c82456
UI_PTN = 0x100b14d0
PTN_STR = 0x8ed8
TRK_STR = 0x91a
LOCK0 = 0x59
LOCK_PTCH = 0
LOCK_VOL = 15
M_OBJ = 0x460e5e30
M_CBS = 0x460e5e28
M_LAB = 0x460e5e2c
NV_SCALE = 0x100b14ec
NV_ROOT = 0x100b14ee

FAILS = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global FAILS
    if ok:
        print(f"  [PASS] {name}" + (f" ({detail})" if detail else ""))
    else:
        FAILS += 1
        print(f"  [FAIL] {name}" + (f": {detail}" if detail else ""))


def sym(name: str) -> int:
    text = MAP.read_text()
    for line in text.splitlines():
        if line.rstrip().endswith(name) and "0x" in line:
            return int(line.split()[0], 16)
    raise SystemExit(f"symbol missing in runtime.map: {name}")


def u8(p, a: int) -> int:
    return p.peek(a, 1)[0]


def poke32(p, a: int, v: int) -> None:
    p.poke(a, int(v).to_bytes(4, "big"))


def poke8(p, a: int, v: int) -> None:
    p.poke(a, bytes([v & 0xFF]))


def ensure_card() -> None:
    if CARD.exists() and CARD.stat().st_size > 0:
        return
    CARD.parent.mkdir(parents=True, exist_ok=True)
    tree = ROOT / "out/_seq_scenarios_tree"
    subprocess.check_call(
        [sys.executable, str(ROOT / "tools/emu/ot_emu/stage_card.py"),
         str(TEMPLATE), "OCTABAM", "A", "--tree", str(tree), "--out", str(CARD)],
        cwd=ROOT,
    )


def trac0(p) -> int:
    return p.long(DBPTR_ADDR) + u8(p, UI_PTN) * PTN_STR


def mask0(p) -> bytes:
    return p.peek(trac0(p), 8)


def tl_mask(p) -> bytes:
    return p.peek(trac0(p) + 0x10, 8)


def locks(p, dest: int, n: int = 16) -> list[int]:
    t = trac0(p)
    return [u8(p, t + LOCK0 + s * 32 + dest) for s in range(n)]


def live(vals: list[int]) -> int:
    return sum(1 for v in vals if v != 0xFF)


def popcount_mask(m: bytes) -> int:
    # ef_bit_addr packs steps with reversed byte order; just count set bits.
    return sum(bin(b).count("1") for b in m)


def mask_bit(m: bytes, step: int) -> bool:
    """Same packing as ef_bit_addr: byte 7-(step>>3), bit (step&7)."""
    return bool(m[7 - (step >> 3)] & (1 << (step & 7)))


def locks_have_trig_or_tl(p, dest_locks: list[int]) -> bool:
    """Every live lock sits on a sample trig or a trigless bit."""
    m = mask0(p)
    tl = tl_mask(p)
    for step, v in enumerate(dest_locks):
        if v == 0xFF:
            continue
        if not (mask_bit(m, step) or mask_bit(tl, step)):
            return False
    return True


class SeqPort:
    def __init__(self, p: MenuPort):
        self.p = p
        self.ef = sym("ef_win")
        self.bank = sym("ef_bank")
        self.dep = sym("ef_dep_mem")
        self.plk = sym("ef_plk_mem")
        self.lane_mem = sym("ef_lane_mem")

    def open_seq(self) -> None:
        self.p.chord("t1", "page", settle=500)
        check("SEQ opens (ef_win nonzero)", self.p.long(self.ef) != 0,
              f"ef_win={self.p.long(self.ef):#x}")

    def close_seq(self) -> None:
        self.p.press("no", settle=400)

    def prime(self, *, lane: int, dest: int, depth: int, pulses: int,
              rot: int = 0, trig_pulses: int = 5) -> None:
        """Write track-0 bank + plock/dep/lane so YES load_slot sees it."""
        b = self.bank
        poke32(self.p, b + 0, trig_pulses)
        poke32(self.p, b + 4, 0)
        poke32(self.p, b + 8, dest)
        poke32(self.p, b + 12, depth)
        poke32(self.p, b + 16, 0)
        self.p.poke(b + 20, bytes(8))
        poke8(self.p, self.lane_mem, lane)
        poke8(self.p, self.dep + dest, depth & 0xFF)
        off = dest * 12
        poke8(self.p, self.plk + off, pulses & 0xFF)
        poke8(self.p, self.plk + off + 1, rot & 0xFF)
        poke8(self.p, self.plk + off + 2, 0)
        self.p.poke(self.plk + off + 4, bytes(8))
        for a, v in (
            (self.ef + 0x18, lane),
            (self.ef + 0x28, dest),
            (self.ef + 0x2c, depth),
            (self.ef + 0x10, pulses),
            (self.ef + 0x14, rot),
            (self.ef + 8, trig_pulses),
            (self.ef + 0xC, 0),
            (self.ef + 0x1C, 0),
            (self.ef + 0x58, 0),
        ):
            poke32(self.p, a, v)

    def yes(self) -> None:
        self.p.press("yes", settle=900)

    def clear_labels(self) -> list[str]:
        obj = self.p.long(M_OBJ)
        lab = self.p.long(M_LAB)
        if not obj or not lab:
            return []
        out = []
        for i in range(3):
            lp = self.p.long(lab + 4 * i)
            out.append(self.p.cstr(lp, 24) if lp else "")
        return out


def run_scenarios() -> int:
    global FAILS
    if not IMAGE.exists():
        print("SEQ scenarios: skip (no out/mainos_bus.bin)")
        return 0
    if not MAP.exists():
        print("SEQ scenarios: skip (no runtime.map)")
        return 0
    emu = ROOT / "out/emu/ot_emu"
    if not emu.exists():
        print("SEQ scenarios: skip (no out/emu/ot_emu)")
        return 0

    ensure_card()
    print("SEQ port scenarios (usage/seq.md):")

    with MenuPort(IMAGE, CARD, "OCTABAM", "A", mkii=True) as port:
        port.settle()
        for _ in range(3):
            port.press("no", settle=80)
        s = SeqPort(port)

        # --- open ---
        s.open_seq()

        # --- Place sample trigs (TRIG, PTCH, DPTH 0) ---
        poke8(port, NV_SCALE, 0)
        s.prime(lane=0, dest=0, depth=0, pulses=5, trig_pulses=5)
        s.yes()
        m = mask0(port)
        check("TRIG DPTH0 places sample trigs", popcount_mask(m) >= 1, m.hex())
        check("TRIG DPTH0 clears PTCH locks", live(locks(port, LOCK_PTCH)) == 0)

        # --- Lock pitch on those trigs (TRIG, PTCH, DPTH>0, SCALE OFF) ---
        before_m = mask0(port)
        s.prime(lane=0, dest=0, depth=64, pulses=5, trig_pulses=5)
        s.yes()
        pt = locks(port, LOCK_PTCH)
        check("TRIG+PTCH+DPTH writes PTCH on trig steps", live(pt) >= 1)
        check("TRIG+PTCH keeps sample trigs", mask0(port) != bytes(8))

        # --- Add volume locks on another rhythm (PLCK VOL) ---
        trig_before = mask0(port)
        pt_before = locks(port, LOCK_PTCH)
        s.prime(lane=1, dest=LOCK_VOL, depth=64, pulses=5, trig_pulses=5)
        s.yes()
        vol = locks(port, LOCK_VOL)
        check("PLCK+VOL writes VOL locks", live(vol) >= 1, f"live={live(vol)}")
        check("PLCK+VOL leaves sample trigs alone", mask0(port) == trig_before)
        check("PLCK+VOL leaves PTCH alone", locks(port, LOCK_PTCH) == pt_before)
        check("PLCK+VOL locks sit on sample trig or trigless",
              locks_have_trig_or_tl(port, vol),
              f"tl={tl_mask(port).hex()} vol_live={live(vol)}")

        # --- PLCK PTCH SCALE OFF = base Part pitch, no new trigs ---
        trig_before = mask0(port)
        poke8(port, NV_SCALE, 0)
        s.prime(lane=1, dest=0, depth=64, pulses=5, trig_pulses=0)
        s.yes()
        pt = locks(port, LOCK_PTCH)
        vals = {v for v in pt if v != 0xFF}
        check("PLCK+PTCH SCALE OFF writes trigless PTCH", live(pt) >= 1)
        check("PLCK+PTCH SCALE OFF uses one base pitch",
              len(vals) == 1, f"vals={vals}")
        check("PLCK+PTCH leaves sample trigs alone", mask0(port) == trig_before)

        # --- PLCK PTCH SCALE ON still writes ---
        poke8(port, NV_SCALE, 1)
        poke8(port, NV_ROOT, 0)
        s.prime(lane=1, dest=0, depth=64, pulses=5, trig_pulses=0)
        s.yes()
        check("PLCK+PTCH SCALE ON writes PTCH locks", live(locks(port, LOCK_PTCH)) >= 1)
        poke8(port, NV_SCALE, 0)

        # --- Clear one destination (PLCK PULS 0) ---
        s.prime(lane=1, dest=LOCK_VOL, depth=64, pulses=0, trig_pulses=5)
        s.yes()
        check("PLCK PULS0 clears that DEST", live(locks(port, LOCK_VOL)) == 0)

        # --- FUNC+BANK clear list (SEQ soft-closes; list on top) ---
        port.chord("func", "bank", settle=700)
        labs = s.clear_labels()
        check("FUNC+BANK opens CLEAR DEST list",
              labs[:1] == ["CLEAR DEST"] and "CLEAR ALL DEST" in labs
              and "CLEAR ALL+TRIGS" in labs,
              str(labs))
        check("clear list stays up (no Detour+layer toggle)",
              port.long(M_OBJ) != 0)
        check("SEQ soft-closed while CLEAR up", port.long(s.ef) == 0)

        # FUNC+BANK again toggles closed and restores SEQ
        port.chord("func", "bank", settle=700)
        check("FUNC+BANK toggle dismisses clear list", port.long(M_OBJ) == 0)
        check("FUNC+BANK toggle restores SEQ", port.long(s.ef) != 0)

        # One NO dismisses list and restores SEQ; SEQ stays closeable
        port.chord("func", "bank", settle=700)
        check("FUNC+BANK reopens CLEAR list", "CLEAR DEST" in s.clear_labels())
        check("SEQ soft-closed again", port.long(s.ef) == 0)
        port.press("no", settle=500)
        check("NO dismisses clear list", port.long(M_OBJ) == 0)
        check("NO restores SEQ", port.long(s.ef) != 0)
        port.press("no", settle=400)
        check("after NO-restore, next NO closes SEQ", port.long(s.ef) == 0)
        s.open_seq()

        # CLEAR DEST via list YES → wipe + restore SEQ
        s.prime(lane=1, dest=0, depth=64, pulses=5, trig_pulses=0)
        s.yes()
        check("preclear PTCH live", live(locks(port, LOCK_PTCH)) >= 1)
        port.chord("func", "bank", settle=600)
        check("SEQ soft-closed before CLEAR DEST YES", port.long(s.ef) == 0)
        port.press("yes", settle=800)  # CLEAR DEST row 0
        check("CLEAR DEST dismisses list", port.long(M_OBJ) == 0)
        check("CLEAR DEST restores SEQ", port.long(s.ef) != 0)
        check("CLEAR DEST wipes PTCH locks", live(locks(port, LOCK_PTCH)) == 0)
        check("CLEAR DEST resets DPTH/PULS/ROT working",
              port.long(s.ef + 0x2C) == 0 and port.long(s.ef + 0x10) == 0
              and port.long(s.ef + 0x14) == 0,
              f"dep={port.long(s.ef+0x2C)} pp={port.long(s.ef+0x10)} prot={port.long(s.ef+0x14)}")

        # CLEAR ALL DEST via list YES → wipe every DEST + restore
        s.prime(lane=1, dest=LOCK_VOL, depth=64, pulses=5, trig_pulses=5)
        s.yes()
        s.prime(lane=1, dest=0, depth=64, pulses=5, trig_pulses=5)
        s.yes()
        check("preclear ALL DEST has PTCH+VOL",
              live(locks(port, LOCK_PTCH)) >= 1 and live(locks(port, LOCK_VOL)) >= 1)
        trig_before_all = mask0(port)
        port.chord("func", "bank", settle=600)
        port.press("down", settle=200)  # CLEAR ALL DEST
        port.press("yes", settle=800)
        check("CLEAR ALL DEST dismisses list", port.long(M_OBJ) == 0)
        check("CLEAR ALL DEST restores SEQ", port.long(s.ef) != 0)
        check("CLEAR ALL DEST wipes PTCH+VOL",
              live(locks(port, LOCK_PTCH)) == 0 and live(locks(port, LOCK_VOL)) == 0)
        check("CLEAR ALL DEST leaves sample trigs", mask0(port) == trig_before_all)

        # CLEAR ALL+TRIGS via list YES → wipe DEST+trigs + restore
        s.prime(lane=0, dest=0, depth=0, pulses=5, trig_pulses=5)
        s.yes()
        check("preclear ALL+TRIGS has sample trigs", popcount_mask(mask0(port)) >= 1)
        s.prime(lane=1, dest=LOCK_VOL, depth=64, pulses=5, trig_pulses=5)
        s.yes()
        port.chord("func", "bank", settle=600)
        port.press("down", settle=200)
        port.press("down", settle=200)  # CLEAR ALL+TRIGS
        port.press("yes", settle=900)
        check("CLEAR ALL+TRIGS dismisses list", port.long(M_OBJ) == 0)
        check("CLEAR ALL+TRIGS restores SEQ", port.long(s.ef) != 0)
        check("CLEAR ALL+TRIGS wipes VOL locks", live(locks(port, LOCK_VOL)) == 0)
        check("CLEAR ALL+TRIGS clears sample trigs", mask0(port) == bytes(8))

        # Close SEQ; FUNC+BANK must not open our CLEAR list
        s.close_seq()
        port.chord("func", "bank", settle=700)
        labs = s.clear_labels()
        check("FUNC+BANK outside SEQ is not CLEAR list",
              "CLEAR DEST" not in labs, str(labs))

    print(f"SEQ scenarios: {FAILS} failed checks")
    return FAILS


def main() -> int:
    # Static gate still accepts remix arg; ignore it.
    return 0 if run_scenarios() == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
