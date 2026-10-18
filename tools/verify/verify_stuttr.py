#!/usr/bin/env python3
"""STUTTR render gates.

  MIX=0       -> bit-exact passthrough
  CHNC=0      -> dry glitch stage (near passthrough at MIX 127)
  LOOP        -> energy on a tone when CHNC open
  REV/SCRAM   -> non-silent when engaged
  DROP        -> renders
  SIZE        -> spike after clear repeats at ~SIZE/2 sample gaps
  RATE slow   -> several SIZE loops land before the next grab
  every knob  -> renders without dsp_host dying
"""
import math
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
# init clears 0x80 procs before audio runs
CLEAR = 0x80 * FRAMES

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


def peak_gaps(xs, thr=(1 << 17)):
    peaks = [i for i, x in enumerate(xs) if abs(x) > thr]
    sep = []
    for p in peaks:
        if not sep or p - sep[-1] >= 2:
            sep.append(p)
    gaps = [sep[i + 1] - sep[i] for i in range(len(sep) - 1)]
    return sep, gaps


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

# Spike after clear; auto-grab once the ring holds SIZE. SIZE = loop period.
# FX2 words=(kn+1)*128 -> stereo frames=(kn+1)*64.
Nspike = CLEAR + 12000


def size_frames(kn):
    return (kn + 1) * 64


def spike_in(kn):
    # spike just before auto-grab so it sits inside the captured slice
    s = [0] * Nspike
    s[CLEAR + size_frames(kn) - 2] = 1 << 22
    return s


for kn in (0, 2, 4):
    expect = size_frames(kn)
    Lw, _ = render(spike_in(kn), SIZE=kn, RATE=0, CHNC=127, MIX=127, MODE=0,
                   DECY=0, FDBK=0)
    peaks, gaps = peak_gaps(Lw)
    good = [g for g in gaps if abs(g - expect) <= 2]
    check(f"SIZE={kn} loop gap~{expect}",
          len(peaks) >= 3 and len(good) >= 2,
          f"peaks={len(peaks)} gaps={gaps[:6]} matched={len(good)}")

g0 = peak_gaps(render(spike_in(0), SIZE=0, RATE=0, CHNC=127, MIX=127, MODE=0,
                      DECY=0, FDBK=0)[0])[1]
g4 = peak_gaps(render(spike_in(4), SIZE=4, RATE=0, CHNC=127, MIX=127, MODE=0,
                      DECY=0, FDBK=0)[0])[1]
med = lambda gs: sorted(gs)[len(gs) // 2] if gs else 0
check("SIZE changes gap", med(g0) < med(g4) and med(g0) > 0,
      f"med0={med(g0)} med4={med(g4)}")

# RATE must not be faster than SIZE or the loop never completes (the unit bug).
# SIZE=4 -> 320 frames; RATE=40 step=0x80+(40<<5)=0x580 -> period ~5958 samples.
Lt, _ = render(tone + tone, SIZE=40, RATE=40, CHNC=127, MIX=127, MODE=0, DECY=0)
check("tone stays loud", max(abs(x) for x in Lt[CLEAR:]) > (1 << 20),
      f"peak={max(abs(x) for x in Lt[CLEAR:])}")

# At SIZE max-ish with slow RATE, gap stays near SIZE (not collapsed to ~2ms).
Lbig, _ = render(spike_in(4), SIZE=4, RATE=20, CHNC=127, MIX=127, MODE=0,
                 DECY=0, FDBK=0)
gaps_r = peak_gaps(Lbig)[1]
good_r = [g for g in gaps_r if abs(g - size_frames(4)) <= 2]
check("RATE=20 keeps SIZE loop",
      len(good_r) >= 2,
      f"gaps={gaps_r[:6]} expect~{size_frames(4)}")

# DECY must fade the loop, then silence — not snap back to dry (MIX leak).
Ndec = CLEAR + 8000
spike = [0] * Ndec
spike[CLEAR + size_frames(2) - 2] = 1 << 22
Ldec = render(spike, SIZE=4, RATE=0, CHNC=127, MIX=127, DECY=24, FDBK=0)[0]
amps = []
seen = []
for i, x in enumerate(Ldec):
    if abs(x) <= (1 << 17):
        continue
    if seen and i - seen[-1] < 3:
        continue
    seen.append(i)
    amps.append(abs(x))
    if len(amps) >= 6:
        break
check("DECY fades loop",
      len(amps) >= 2 and amps[-1] < amps[0] // 2,
      f"amps={amps}")
# Tail after fade: near silence, not a copy of dry (dry would be 0 here too on
# silence input — use a continuous dry tone under MIX 127 after forced fade).
tone_d = [int(0.25 * (1 << 23) * math.sin(2 * 3.14159265 * 220 * i / 44100))
          for i in range(Ndec)]
# High DECY + tiny SIZE: gain dies fast; remainder of buffer must stay quiet
# at MIX 127 (old bug: wet fell back to dry → full tone through).
Lquiet = render(tone_d, SIZE=0, RATE=0, CHNC=127, MIX=127, DECY=127, FDBK=0)[0]
tail = Lquiet[CLEAR + 800:CLEAR + 2500]
peak_tail = max(abs(x) for x in tail) if tail else 0
peak_dry = max(abs(x) for x in tone_d[CLEAR + 800:CLEAR + 2500])
check("MIX127 after DECY is silent not dry",
      peak_tail < peak_dry // 8,
      f"peak_tail={peak_tail} peak_dry={peak_dry}")

for name in K:
    render(ramp[:FRAMES * 8], **{name: 64})
check("every named knob renders", True)

if FAILS:
    sys.exit(f"verify_stuttr: {len(FAILS)} FAILED: {', '.join(FAILS)}")
print("verify_stuttr: OK")
