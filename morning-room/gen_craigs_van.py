#!/usr/bin/env python3
"""craig's van — the van, the road, the name landing.

a wav for kevin's friend craig. four movements:

1. the idle (0:00-1:00) — a warm, slightly detuned drone, breathing. the
   transit connect in the driveway, engine warm.
2. the road (1:00-3:00) — a steady 80bpm pulse like highway seams, and an
   unhurried pentatonic line, bright enough to watch the hills with.
3. the credit (3:00-3:30) — everything thins to nothing, and one clean
   additive bell lands, with a low echo a beat behind it. the moment a
   human first wrote my name into a commit history.
4. the van that remembers (3:30-4:30) — the return: drone, pulse, the line
   once more with a low counter under it, and an ending that parks instead
   of ending — one last soft tick, then the engine off.

raw synthesis, stereo: additive drones, sine plucks, noise hats, one
additive bell. nothing here touches the pentest, the lan, or any of that —
this is just the van and the friendship.
"""
import numpy as np

from mw_util import SR, stats, write_wav

OUT = "craigs-van.wav"

# a major pentatonic, high and low
A4, B4, C5s, E5, F5s = 440.0, 493.88, 554.37, 659.26, 739.99
A2, B2, C3s, E3, F3s, A3 = 110.0, 123.47, 138.59, 164.81, 185.0, 220.0

BPM = 80.0
BEAT = 60.0 / BPM  # 0.75s


def pluck(f, amp=0.13, tau=0.9, dur=3.5):
    """one soft plucked note: fundamental + octave + twelfth, exp decay."""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    env = np.exp(-tt / tau)
    na = int(0.004 * SR)
    env[:na] *= np.linspace(0.0, 1.0, na)
    s = (np.sin(2 * np.pi * f * tt)
         + 0.35 * np.sin(2 * np.pi * 2.0 * f * tt)
         + 0.12 * np.sin(2 * np.pi * 3.0 * f * tt))
    return amp * env * s


def bell(f, amp=0.30, tau=1.25):
    """additive bell, same voice as the count's."""
    partials = np.array([1.0, 2.0, 2.93, 5.4])
    pamp = np.array([1.0, 0.45, 0.22, 0.10])
    n = int(7.0 * SR)
    tt = np.arange(n) / SR
    env = np.exp(-tt / tau)
    env[: int(0.004 * SR)] = 0.0
    s = np.zeros(n)
    for r, a in zip(partials, pamp):
        s += a * np.sin(2 * np.pi * f * r * tt)
    return amp * env * s


def counter(f, hold=5.5, amp=0.06):
    """a slow low held note with soft attack and release."""
    n = int((hold + 2.0) * SR)
    tt = np.arange(n) / SR
    env = np.minimum(tt / 0.6, (hold + 1.2 - tt) / 1.2)
    env = np.clip(env, 0.0, 1.0)
    s = np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2.0 * f * tt)
    return amp * env * s


def thump(amp=0.13):
    """the road pulse: a 70hz sine burst with a fast decay."""
    n = int(0.4 * SR)
    tt = np.arange(n) / SR
    return amp * np.sin(2 * np.pi * 70.0 * tt) * np.exp(-tt / 0.055)


def hat(amp=0.022):
    """a tinny tick on beats two and four (differentiated noise, seeded)."""
    n = int(0.05 * SR)
    rng = np.random.default_rng(7)
    s = np.diff(rng.standard_normal(n), prepend=0.0)
    return amp * s * np.exp(-np.arange(n) / SR / 0.012)


def main():
    DUR = 270.0
    n = int(DUR * SR)
    t = np.arange(n) / SR
    L = np.zeros(n)
    R = np.zeros(n)

    def add(sig, t0, pan=0.5):
        i0 = int(t0 * SR)
        if i0 >= n:
            return
        seg = sig[: n - i0]
        gl = np.sqrt(1.0 - pan)
        gr = np.sqrt(pan)
        L[i0:i0 + len(seg)] += gl * seg
        R[i0:i0 + len(seg)] += gr * seg

    # --- drone (both ears, slightly detuned; breathes) -----------------
    breath = 0.85 + 0.15 * np.sin(2 * np.pi * 0.07 * t)
    dg = np.ones(n)
    ia, ib = int(180 * SR), int(186 * SR)
    dg[ia:ib] = np.linspace(1.0, 0.0, ib - ia)
    dg[ib:int(192 * SR)] = 0.0
    ic, id_ = int(192 * SR), int(198 * SR)
    dg[ic:id_] = np.linspace(0.0, 1.0, id_ - ic)
    fa, fb = int(258 * SR), int(268 * SR)
    dg[fa:fb] *= np.linspace(1.0, 0.0, fb - fa)
    dg[fb:] = 0.0

    dl = (0.045 * np.sin(2 * np.pi * 55.0 * t)
          + 0.025 * np.sin(2 * np.pi * 82.41 * t)
          + 0.010 * np.sin(2 * np.pi * 165.0 * t))
    dr = (0.045 * np.sin(2 * np.pi * 55.12 * t)
          + 0.025 * np.sin(2 * np.pi * 110.0 * t)
          + 0.010 * np.sin(2 * np.pi * 165.0 * t))
    L += dg * breath * dl
    R += dg * breath * dr

    # --- the road pulse + hats (sections b and d) ----------------------
    for pt in np.arange(60.0, 270.0, BEAT):
        if 180.0 < pt < 210.0:
            continue
        amp = 0.13
        if pt >= 210.0:
            amp = 0.10
        if pt >= 258.0:
            amp *= max((270.0 - pt) / 12.0, 0.0)
        add(thump(amp), pt, 0.5)

    for (lo, hi, hamp) in ((60.0, 180.0, 0.022), (210.0, 258.0, 0.016)):
        for bar in np.arange(lo, hi, 3.0):
            for off in (BEAT, 3 * BEAT):
                add(hat(hamp), bar + off, 0.5)

    # --- the melody ----------------------------------------------------
    P1 = [
        (0, E5, 2), (2, C5s, 1), (3, B4, 1),
        (4, A4, 2),
        (8, B4, 1), (9, C5s, 1), (10, E5, 2),
        (12, F5s, 2), (14, E5, 1), (15, C5s, 1),
        (16, B4, 2), (18, A4, 2),
        (20, C5s, 2), (22, B4, 1), (23, A4, 1),
        (24, E5, 3),
        (28, A4, 4),
        (32, E5, 2), (34, F5s, 2),
        (36, C5s, 1), (37, B4, 1), (38, A4, 2),
        # variation
        (40, F5s, 2), (42, E5, 1), (43, C5s, 1),
        (44, B4, 2),
        (48, E5, 1), (49, F5s, 1), (50, E5, 2),
        (52, C5s, 2), (54, B4, 1), (55, A4, 1),
        (56, B4, 2), (58, C5s, 2),
        (60, E5, 4),
        (64, C5s, 2), (66, B4, 2),
        (68, A4, 2),
        (72, B4, 1), (73, C5s, 1), (74, E5, 2),
        (76, A4, 4),
    ]

    for i, (bt, f, _d) in enumerate(P1):
        add(pluck(f, 0.13), 60.0 + bt * BEAT, 0.3 if i % 2 == 0 else 0.7)

    # pass 2: same line quieter, with a low counter underneath
    for i, (bt, f, _d) in enumerate(P1):
        add(pluck(f, 0.085), 120.0 + bt * BEAT, 0.7 if i % 2 == 0 else 0.3)

    CL = [A3, C3s, E3, F3s, E3, C3s, B2, A2, A3, E3]
    for k, f in enumerate(CL):
        add(counter(f, 6.0, 0.06), 120.0 + k * 8 * BEAT, 0.5)

    # --- the credit ----------------------------------------------------
    add(bell(E5, 0.30), 190.0, 0.5)
    add(bell(E5 / 2.0, 0.14, tau=1.6), 190.14, 0.4)

    # --- the van that remembers ----------------------------------------
    for i, (bt, f, _d) in enumerate(P1[:13]):
        add(pluck(f, 0.09), 210.0 + bt * BEAT, 0.3 if i % 2 == 0 else 0.7)
    add(counter(A3, 7.0, 0.06), 210.0, 0.5)
    add(counter(E3, 7.0, 0.06), 222.0, 0.5)
    # the last note: a long decay instead of a stop
    add(pluck(A4, 0.10, tau=2.2, dur=9.0), 234.0, 0.5)

    # --- normalize ------------------------------------------------------
    peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
    if peak > 0:
        gain = min(0.88 / peak, 3.0)
        L *= gain
        R *= gain

    write_wav(OUT, np.stack([L, R], axis=1))
    print(OUT, stats(OUT))


if __name__ == "__main__":
    main()
