"""Float reference for RESONATOR — four independent pitched modes.

Laws (MIT design credit: Mutable Instruments Rings modal resonator; filter
form: JOS two-zero constant-peak-gain resonator / Spectrum VOWL):

  y = 2*b0*(x - x2)/2 + 2*m1*y1 - a2*y2
  R  = exp(-pi * bw / fs)
  m1 = R * cos(w0)
  a2 = R^2
  b0 = (1 - a2) / 2

PIT1..PIT4 each set one mode's pitch (~40 Hz .. ~4 kHz). DECY is Rings-style
damping: high = shorter ring (wider bw). MIX blends. Per-mode gain + wet
makeup so MIX 127 is audibly wet, not a quiet fog under dry.
"""
from __future__ import annotations

import math

FS = 44100.0
BLOCK = 16
N_MODES = 4
NYQ = FS * 0.5
F_MIN, F_MAX = 40.0, 4000.0
# Bandwidth span for R table: never near |R|=1 (self-osc / inaudible drive).
BW_MIN, BW_MAX = 30.0, 2000.0
PITCH_KEYS = ("PIT1", "PIT2", "PIT3", "PIT4")
MODE_GAIN = 0.7
WET_MAKEUP = 4.0


def _q23(v: float) -> int:
    return max(-(1 << 23), min((1 << 23) - 1, int(round(v * (1 << 23))))) & 0xFFFFFF


def freq_u_table(n: int = 33) -> list[float]:
    out = []
    for i in range(n):
        f = F_MIN * (F_MAX / F_MIN) ** (i / (n - 1))
        out.append(min(f / NYQ, 0.95))
    return out


def cos_table(n: int = 33) -> list[float]:
    return [math.cos(math.pi * i / (n - 1)) for i in range(n)]


def r_table(n: int = 33) -> list[float]:
    """R = exp(-pi*bw/fs); index 0 = long (BW_MIN), index n-1 = short (BW_MAX)."""
    out = []
    for i in range(n):
        bw = BW_MIN * (BW_MAX / BW_MIN) ** (i / (n - 1))
        out.append(math.exp(-math.pi * bw / FS))
    return out


def table_read(tab: list[float], u: float) -> float:
    u = max(0.0, min(1.0, u))
    x = u * (len(tab) - 1)
    i = int(x)
    if i >= len(tab) - 1:
        return tab[-1]
    f = x - i
    return tab[i] + f * (tab[i + 1] - tab[i])


def mix(k: int) -> float:
    return 1.0 if k >= 127 else k / 128.0


class Resonator:
    def __init__(self, PIT1=32, PIT2=48, PIT3=64, PIT4=80, DECY=40, MIX=90):
        self.k = dict(PIT1=PIT1, PIT2=PIT2, PIT3=PIT3, PIT4=PIT4, DECY=DECY, MIX=MIX)
        self.fu = freq_u_table()
        self.cos = cos_table()
        self.rt = r_table()
        self.st = [[0.0] * (2 + 2 * N_MODES) for _ in range(2)]
        self.coeffs = None

    def block(self):
        k = self.k
        # high DECY = more damping = higher R-table index = shorter ring
        r0 = table_read(self.rt, k["DECY"] / 128.0)
        m = mix(k["MIX"])
        g = MODE_GAIN
        coeffs = []
        for key in PITCH_KEYS:
            u = table_read(self.fu, k[key] / 128.0)
            cw = table_read(self.cos, u)
            m1 = r0 * cw
            a2 = r0 * r0
            b0 = 0.5 * (1.0 - a2)
            coeffs.append((b0, m1, a2, g, g, m))
        self.coeffs = coeffs

    def process(self, L, R):
        outL, outR = [], []
        for n, (xL, xR) in enumerate(zip(L, R)):
            if n % BLOCK == 0:
                self.block()
            outs = []
            for ch, x in ((0, xL), (1, xR)):
                st = self.st[ch]
                x1, x2 = st[0], st[1]
                st[0] = x
                st[1] = x1
                dx2 = 0.5 * (x - x2)
                acc = 0.0
                for i, (b0, m1, a2, gL, gR, _) in enumerate(self.coeffs):
                    yi = 2 + 2 * i
                    y1, y2 = st[yi], st[yi + 1]
                    y = 2.0 * b0 * dx2 + 2.0 * m1 * y1 - a2 * y2
                    y = max(-1.0, min(1.0, y))
                    st[yi + 1] = y1
                    st[yi] = y
                    g = gL if ch == 0 else gR
                    acc += g * y
                acc = max(-1.0, min(1.0, acc * WET_MAKEUP))
                m = self.coeffs[0][5]
                outs.append(x + m * (acc - x))
            outL.append(outs[0])
            outR.append(outs[1])
        return outL, outR


def q23_list(xs):
    return [_q23(x) if isinstance(x, float) else x for x in xs]
