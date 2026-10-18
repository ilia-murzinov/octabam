"""Float reference for RESONATOR — Rings-inspired 4-mode modal bank.

Laws (MIT design credit: Mutable Instruments Rings modal resonator; filter
form: JOS two-zero constant-peak-gain resonator / Spectrum VOWL):

  y = 2*b0*(x - x2)/2 + 2*m1*y1 - a2*y2
  R  = exp(-pi * bw / fs)
  m1 = R * cos(w0)
  a2 = R^2
  b0 = (1 - a2) / 2

Knobs match the manifest. BODY picks a ratio set; STRU morphs toward
stretch; DECY sets base bandwidth; BRIT damps high modes when low; POS
sets per-mode amplitudes (strike position) and L/R balance; MIX blends.
"""
from __future__ import annotations

import math

FS = 44100.0
BLOCK = 16
N_MODES = 4
NYQ = FS * 0.5

# BODY ratio sets (approx bar / odd tube / plate), Rings-inspired voicing.
BODY_RATIOS = (
    (1.0, 2.756, 5.404, 8.933),   # BAR
    (1.0, 3.0, 5.0, 7.0),         # TUBE
    (1.0, 1.594, 2.136, 2.296),   # PLATE
)

F_MIN, F_MAX = 40.0, 4000.0


def _q23(v: float) -> int:
    return max(-(1 << 23), min((1 << 23) - 1, int(round(v * (1 << 23))))) & 0xFFFFFF


def freq_hz(freq_knob: int) -> float:
    u = max(0, min(127, freq_knob)) / 128.0
    return F_MIN * (F_MAX / F_MIN) ** u


def freq_u_table(n: int = 33) -> list[float]:
    """Fundamental as fraction of Nyquist, FREQ 0..127 mapped onto 33 knots."""
    out = []
    for i in range(n):
        f = F_MIN * (F_MAX / F_MIN) ** (i / (n - 1))
        out.append(min(f / NYQ, 0.95))
    return out


def cos_table(n: int = 33) -> list[float]:
    """cos(pi * i/(n-1)) covering 0 .. Nyquist."""
    return [math.cos(math.pi * i / (n - 1)) for i in range(n)]


def r_table(n: int = 33) -> list[float]:
    """R = exp(-pi * bw / fs) for bw 2 .. 400 Hz exponential."""
    out = []
    for i in range(n):
        bw = 2.0 * (400.0 / 2.0) ** (i / (n - 1))
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
    def __init__(self, FREQ=40, STRU=64, DECY=80, BRIT=90, POS=64, MIX=64, BODY=0):
        self.k = dict(FREQ=FREQ, STRU=STRU, DECY=DECY, BRIT=BRIT, POS=POS, MIX=MIX, BODY=BODY)
        self.fu = freq_u_table()
        self.cos = cos_table()
        self.rt = r_table()
        # per channel: x1, x2, then 4*(y1, y2)
        self.st = [[0.0] * (2 + 2 * N_MODES) for _ in range(2)]
        self.coeffs = None  # list of (b0, m1, a2, gL, gR)

    def block(self):
        k = self.k
        body = int(k["BODY"]) % 3
        ratios = BODY_RATIOS[body]
        u0 = table_read(self.fu, k["FREQ"] / 128.0)
        stru = k["STRU"] / 128.0
        decy = k["DECY"] / 128.0
        brit = k["BRIT"] / 128.0
        pos = 0.05 + 0.9 * (k["POS"] / 128.0)
        # DECY high -> narrow bw (long ring): map knob to R-table index inverted
        r0 = table_read(self.rt, 1.0 - decy)
        m = mix(k["MIX"])
        coeffs = []
        for i in range(N_MODES):
            # STRU morphs body ratios toward stretched harmonics
            harm = float(i + 1)
            ratio = ratios[i] + (harm * (1.0 + 0.25 * i) - ratios[i]) * stru
            u = min(u0 * ratio, 0.95)
            cw = table_read(self.cos, u)
            # high modes damp more when BRIT is low
            widen = (1.0 - brit) * (i / (N_MODES - 1))
            # lower R => wider bw; pull R toward smaller values
            r = r0 * (1.0 - 0.55 * widen)
            r = max(0.5, min(0.9995, r))
            m1 = r * cw
            a2 = r * r
            b0 = 0.5 * (1.0 - a2)
            # strike position amplitudes + stereo
            amp = abs(math.sin(math.pi * (i + 1) * pos))
            amp = max(0.05, amp)
            # normalize roughly across modes
            gL = 0.35 * amp * (1.0 - 0.35 * (pos - 0.5))
            gR = 0.35 * amp * (1.0 + 0.35 * (pos - 0.5))
            coeffs.append((b0, m1, a2, gL, gR, m))
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
                    # soft saturate like the chip's limiting store
                    y = max(-1.0, min(1.0, y))
                    st[yi + 1] = y1
                    st[yi] = y
                    g = gL if ch == 0 else gR
                    acc += g * y
                acc = max(-1.0, min(1.0, acc))
                m = self.coeffs[0][5]
                outs.append(x + m * (acc - x))
            outL.append(outs[0])
            outR.append(outs[1])
        return outL, outR


def q23_list(xs):
    return [_q23(x) if isinstance(x, float) else x for x in xs]
