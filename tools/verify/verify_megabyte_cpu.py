#!/usr/bin/env python3
"""Megabyte CPU voice: native signal tests (host build of cpu.c)."""
import ctypes as C
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / 'out/megabyte-cpu'
SR, RING, Q = 44100, 176400, 2147483648
FAILS = 0


class State(C.Structure):
    _fields_ = (
        [(k, C.c_uint32) for k in ('active', 'valid', 'phase', 'rng')]
        + [(k, C.c_int32) for k in (
            'mix', 'feedback', 'drive1', 'drive2',
            'delay', 'lp_z', 'havoc', 'mod_depth')]
    )


class Params(C.Structure):
    _fields_ = [(k, C.c_uint32) for k in (
        'time', 'feedback', 'gain', 'mod', 'havoc', 'mix')]


def params(**kw):
    p = Params(time=64, feedback=0, gain=0, mod=0, havoc=0, mix=127)
    for k, v in kw.items():
        setattr(p, k, v)
    return p


def check(name, ok, detail=''):
    global FAILS
    FAILS += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}"
          + (f': {detail}' if detail else ''), flush=True)


def build_lib():
    OUT.mkdir(parents=True, exist_ok=True)
    src = ROOT / 'modules/megabyte/cpu.c'
    # Unique soname each run: macOS CDLL caches by path.
    suffix = '.dylib' if sys.platform == 'darwin' else '.so'
    lib = OUT / f'mb_host_{os.getpid()}{suffix}'
    cmd = [
        'cc', '-shared', '-O2', '-fPIC', '-DMB_HOST',
        f'-I{ROOT / "modules/megabyte"}',
        str(src), '-o', str(lib),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)
    return C.CDLL(str(lib))


class Engine:
    def __init__(self, lib, p):
        self.lib, self.p, self.state = lib, p, State()
        self.ring = (C.c_int32 * (RING * 2))()
        self.audio = (C.c_int32 * 32)()
        self.record = (C.c_int32 * 32)()
        self.write = 0
        lib.mb_process.argtypes = [
            C.POINTER(State), C.POINTER(Params),
            C.POINTER(C.c_int32), C.c_uint32,
            C.POINTER(C.c_int32), C.POINTER(C.c_int32),
        ]

    def block(self, samples):
        for i, x in enumerate(samples):
            self.audio[i] = x
        self.lib.mb_process(
            C.byref(self.state), C.byref(self.p), self.ring,
            self.write, self.audio, self.record)
        for i, x in enumerate(self.record):
            self.ring[2 * self.write + i] = x
        self.write = (self.write + 16) % RING
        return list(self.audio)

    def render(self, frames, source):
        out = []
        for block in range((frames + 15) // 16):
            inp = [source(block * 16 + i, c)
                   for i in range(16) for c in range(2)]
            out.extend(self.block(inp)[::2])
        return out[:frames]


def main():
    lib = build_lib()
    # MIX=0 exact dry
    e = Engine(lib, params(mix=0, feedback=127, gain=127, mod=127, havoc=127))
    dry = [0x71234567, -0x72345678] * 16
    check('MIX=0 preserves asymmetric dry audio', e.block(dry) == dry)

    # Delayed impulse near TIME=64 (~625 ms ≈ 27562 samples)
    e = Engine(lib, params(time=64, feedback=0, gain=0, mod=0, havoc=0, mix=127))
    out = e.render(40000, lambda n, c: Q // 4 if n == 64 else 0)
    # expected delay samples ≈ 2205 + 64*(52920-2205)/127
    expected = 64 + int(2205 + 64 * (52920 - 2205) / 127)
    window = out[expected - 64: expected + 256]
    peak = max(range(len(window)), key=lambda i: abs(window[i]))
    peak_at = expected - 64 + peak
    check('TIME=64 impulse arrives near mapped latency',
          abs(peak_at - expected) < 80 and abs(window[peak]) > Q // 200,
          f'peak@{peak_at} want~{expected} amp={window[peak]}')

    # Feedback regenerates: second repeat after TIME≈32 (~15k samples).
    e = Engine(lib, params(time=32, feedback=110, gain=40, mix=127))
    out = e.render(45000, lambda n, c: Q // 5 if 64 <= n < 80 else 0)
    # First echo ~15k; second ~30k. Demand energy in the second-echo window.
    tail = max(abs(x) for x in out[28000:34000])
    check('FDBK regenerates a second repeat',
          tail > Q // 5000, f'tail={tail}')

    # HAVC scales feedback only: with FDBK=0 the ring stays quiet after the
    # single dry→wet pass (no regenerating tail).
    e = Engine(lib, params(time=30, feedback=0, gain=0, havoc=127, mix=127))
    out = e.render(30000, lambda n, c: Q // 5 if 64 <= n < 80 else 0)
    # TIME=30 → ~14k samples; look well after any single echo.
    late = max(abs(x) for x in out[20000:28000])
    check('HAVC with FDBK=0 leaves no regenerating tail',
          late < Q // 1000, f'late={late}')

    # HAVC sustains: mid FDBK decays, same FDBK+HAVC keeps the 4th repeat alive.
    src = lambda n, c: Q // 5 if 64 <= n < 80 else 0
    e0 = Engine(lib, params(time=20, feedback=70, gain=40, havoc=0, mix=127))
    e1 = Engine(lib, params(time=20, feedback=70, gain=40, havoc=127, mix=127))
    late0 = max(abs(x) for x in e0.render(50000, src)[38000:46000])
    late1 = max(abs(x) for x in e1.render(50000, src)[38000:46000])
    check('HAVC sustains late repeats vs same FDBK',
          late1 > late0 * 1.5, f'no={late0} havoc={late1}')

    if FAILS:
        print(f'{FAILS} failure(s)')
        return 1
    print('verify_megabyte_cpu: all passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
