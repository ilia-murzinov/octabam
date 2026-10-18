#!/usr/bin/env python3
"""STUTTR render gates.

  MIX=0       -> bit-exact passthrough
  CHNC=0      -> dry glitch stage (near passthrough at MIX 127)
  LOOP        -> energy on a tone when CHNC open
  REV         -> non-silent when engaged
  SCRAM       -> non-zero output when engaged
  DROP        -> renders (may be quieter)
  every knob  -> renders without dsp_host dying
"""
import pathlib, struct, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolpath  # noqa: E402,F401
import send_probe
from remix import registry

MOD = registry.by_name("stuttr")
SEND = registry.by_name("send")
K = MOD.knob_map()
MEM = f"out/dsp/_audition_{MOD.name}_A.mem"
HOST = "vendor/dsp56300/build/source/dsp_host/dsp_host"
FXID = MOD.menu.fx2_id
FRAMES = 15
TMP = pathlib.Path("out/_stgate")
TMP.mkdir(parents=True, exist_ok=True)

pathlib.Path(MEM).unlink(missing_ok=True)
subprocess.run([sys.executable, "tools/remix/audition.py", MOD.name, "out/dry/drums_110.wav"],
               capture_output=True)
if not pathlib.Path(MEM).exists():
    sys.exit(f"no {MEM} -- audition failed for {MOD.name}")
init, proc = send_probe.entry_points(MEM, FXID)
if (init, proc) == send_probe.entry_points(MEM, SEND.menu.fx2_id):
    sys.exit(f"fx id 0x{FXID:02x} is SEND -- STUTTR not in dump")
print(f"entries: init=P:0x{init:04x} proc=P:0x{proc:04x}")

DEFAULTS = [(p.default or 0) for p in MOD.params]


def params(**kw):
    v = list(DEFAULTS)
    for name, val in kw.items():
        v[K[name]] = val
    return v


def render(samples, **kw):
    n = len(samples) - len(samples) % FRAMES
    src, out = TMP / "in.raw", TMP / "out.raw"
    src.write_bytes(b"".join(struct.pack("<i", m) for m in samples[:n]))
    # FX2 slot: r7 index 1, allocator index 1 (full 16K ring)
    cmd = [HOST, "-mem", MEM, "-init", f"{init:x}", "-proc", f"{proc:x}",
           "-inst", "1", "-r7", "1", "-alloc", "1", "-inmask", "1",
           "-frames", str(FRAMES), "-blocks", str(n // FRAMES),
           "-in", str(src), "-out", str(out),
           "-params", ",".join(str(x) for x in params(**kw))]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"dsp_host failed for {kw}:\n{r.stdout}\n{r.stderr}")
    w = struct.unpack(f"<{len(out.read_bytes()) // 4}i", out.read_bytes())
    return list(w[0::2])[:n], list(w[1::2])[:n]


FAILS = []


def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(label)


N = 4800
ramp = [((i % 200) - 100) * (1 << 16) for i in range(N)]
tone = [int(0.3 * (1 << 23) * __import__("math").sin(2 * 3.14159265 * 440 * i / 44100))
        for i in range(N)]

print("STUTTR gates")
L, R = render(ramp, MIX=0, SIZE=80, RATE=100, CHNC=127, MODE=0)
check("MIX=0 bit-exact", L == ramp and R == ramp,
      f"max|d|={max(abs(a - b) for a, b in zip(L, ramp))}")

L0, _ = render(ramp, CHNC=0, MIX=127, SIZE=80, RATE=100)
check("CHNC=0 passthrough", max(abs(a - b) for a, b in zip(L0, ramp)) < (1 << 12),
      f"max|d|={max(abs(a - b) for a, b in zip(L0, ramp))}")

E_dry = sum(x * x for x in render(tone, CHNC=0, MIX=127)[0])
E_loop = sum(x * x for x in render(tone, CHNC=127, MIX=127, SIZE=40, RATE=110,
                                   MODE=0, DECY=0)[0])
check("LOOP energy", E_loop > E_dry * 0.2,
      f"Edry={E_dry} Eloop={E_loop}")

Lr, _ = render(tone, CHNC=127, MIX=127, SIZE=40, RATE=110, MODE=1, DECY=0)
check("REV non-silent", max(abs(x) for x in Lr) > (1 << 16),
      f"peak={max(abs(x) for x in Lr)}")

Ls, _ = render(tone, CHNC=127, MIX=127, SIZE=60, RATE=100, MODE=3, DECY=0)
check("SCRAM non-zero", max(abs(x) for x in Ls) > (1 << 14),
      f"peak={max(abs(x) for x in Ls)}")

Ld, _ = render(tone, CHNC=127, MIX=127, SIZE=40, RATE=110, MODE=2)
check("DROP renders", len(Ld) == len(tone) - len(tone) % FRAMES)

# Integer SIZE: small vs large slice must not be bit-identical under LOOP.
L_sm, _ = render(tone, CHNC=127, MIX=127, SIZE=8, RATE=120, MODE=0, DECY=0)
L_lg, _ = render(tone, CHNC=127, MIX=127, SIZE=100, RATE=120, MODE=0, DECY=0)
check("SIZE changes loop", L_sm != L_lg,
      f"identical={L_sm == L_lg} peak_sm={max(abs(x) for x in L_sm)} "
      f"peak_lg={max(abs(x) for x in L_lg)}")

for name in K:
    render(ramp[:FRAMES * 8], **{name: 64})
check("every named knob renders", True)

if FAILS:
    sys.exit(f"verify_stuttr: {len(FAILS)} FAILED: {', '.join(FAILS)}")
print("verify_stuttr: OK")
