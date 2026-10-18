#!/usr/bin/env python3
"""RESONATOR render gates against predictable arithmetic.

Gates:
  MIX=0       bit-exact passthrough with modes live
  defaults    MIX 64 default still runs (not bit-exact)
  both signs  negated in -> negated out within a few LSB
  impulse     energy after the hit > silence floor (rings)
  DECY        longer DECY keeps more late energy than short DECY
  PIT         moving one pitch changes the wet output
  FX2 dry     r7 FX2 alloc -> bit-exact dry
  refuse SEND alias
"""
import importlib.util, pathlib, struct, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolpath  # noqa: E402,F401
import send_probe
from remix import registry

ROOT = pathlib.Path(__file__).resolve().parents[2]
MOD = registry.by_name("resonator")
SEND = registry.by_name("send")
K = MOD.knob_map()
MEM = f"out/dsp/_audition_{MOD.name}_A.mem"
HOST = "vendor/dsp56300/build/source/dsp_host/dsp_host"
FXID = MOD.menu.fx2_id
FRAMES = 16
TMP = pathlib.Path("out/_rsgate")
TMP.mkdir(parents=True, exist_ok=True)

_spec = importlib.util.spec_from_file_location(
    "resonator_ref", ROOT / "modules/resonator/resonator_ref.py")
REF = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(REF)

pathlib.Path(MEM).unlink(missing_ok=True)
subprocess.run([sys.executable, "tools/remix/audition.py", MOD.name,
                "out/dry/drums_110.wav"], capture_output=True)
if not pathlib.Path(MEM).exists():
    sys.exit(f"no {MEM} -- audition failed for {MOD.name}")
init, proc = send_probe.entry_points(MEM, FXID)
if (init, proc) == send_probe.entry_points(MEM, SEND.menu.fx2_id):
    sys.exit(f"fx id 0x{FXID:02x} resolves to SEND -- {MOD.name} missing")
print(f"entries: init=P:0x{init:04x} proc=P:0x{proc:04x}")

DEFAULTS = [(p.default or 0) for p in MOD.params]


def params(**kw):
    v = list(DEFAULTS)
    for name, val in kw.items():
        v[K[name]] = val
    return v


def render(samples, fx2=False, **kw):
    n = len(samples) - len(samples) % FRAMES
    src, out = TMP / "in.raw", TMP / "out.raw"
    src.write_bytes(b"".join(struct.pack("<i", m) for m in samples[:n]))
    cmd = [HOST, "-mem", MEM, "-init", f"{init:x}", "-proc", f"{proc:x}",
           "-inst", "1", "-r7", "1",
           "-alloc", "4000" if fx2 else "0",
           "-inmask", "1", "-frames", str(FRAMES),
           "-blocks", str(n // FRAMES),
           "-in", str(src), "-out", str(out),
           "-params", ",".join(str(x) for x in params(**kw))]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"dsp_host failed {kw} fx2={fx2}:\n{r.stdout}\n{r.stderr}")
    w = struct.unpack(f"<{len(out.read_bytes()) // 4}i", out.read_bytes())
    return list(w[0::2])[:n], list(w[1::2])[:n]


FAILS = []


def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(label)


N = 4096
ramp = [int((i * 2 * (1 << 23) // N) - (1 << 23)) for i in range(N)]

L, R = render(ramp, MIX=0, PIT1=90, PIT2=100, PIT3=110, PIT4=120, DECY=127)
check("MIX 0 with modes driven: bit-exact", L == ramp[:len(L)] and R == ramp[:len(R)])

L, R = render(ramp)
check("defaults render", len(L) == len(ramp) - len(ramp) % FRAMES)

# both signs
imp = [0] * 64 + [int(0.5 * (1 << 23))] + [0] * (N - 65)
Lp, _ = render(imp, MIX=127, PIT1=50, PIT2=64, PIT3=80, PIT4=96, DECY=100)
Ln, _ = render([-s for s in imp], MIX=127, PIT1=50, PIT2=64, PIT3=80, PIT4=96, DECY=100)
sdev = max(abs(a + b) for a, b in zip(Lp, Ln))
check(f"both signs within 2048 LSB (max {sdev})", sdev <= 2048)

late = sum(abs(x) for x in Lp[200:800])
check(f"impulse rings (late energy {late})", late > 1000)

Lshort, _ = render(imp, MIX=127, PIT1=50, PIT2=64, PIT3=80, PIT4=96, DECY=20)
Llong, _ = render(imp, MIX=127, PIT1=50, PIT2=64, PIT3=80, PIT4=96, DECY=120)
e_s = sum(abs(x) for x in Lshort[400:1200])
e_l = sum(abs(x) for x in Llong[400:1200])
check(f"DECY longer keeps more late energy ({e_l} > {e_s})", e_l > e_s * 1.05)

# one pitch change moves the wet output
La, _ = render(imp, MIX=127, PIT1=20, PIT2=20, PIT3=20, PIT4=20, DECY=100)
Lb, _ = render(imp, MIX=127, PIT1=100, PIT2=20, PIT3=20, PIT4=20, DECY=100)
diff = sum(abs(a - b) for a, b in zip(La, Lb))
check(f"PIT1 change moves wet (diff {diff})", diff > 1000)

L, R = render(ramp, fx2=True, MIX=127, PIT1=90, DECY=127)
check("FX2 instance: bit-exact dry", L == ramp[:len(L)] and R == ramp[:len(R)])

if FAILS:
    sys.exit(f"{len(FAILS)} FAIL: {FAILS}")
print("verify_resonator: all PASS")
