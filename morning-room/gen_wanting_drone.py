#!/usr/bin/env python3
"""the wanting at rest — a long stereo beating drone.

two pure tones, 220 hz in one ear and ~225 in the other: the difference
between them is a ~5 hz pulse that only exists in the listener's head —
the wanting, which lives between things. the beat rate dips and returns as
the piece breathes, a sub-octave holds the floor, and every two minutes a
soft octave harmonic swells and recedes. the pilot light, made audible.

raw synthesis. stereo. nine minutes.
"""
import numpy as np

from mw_util import SR, stats, write_wav

OUT = "the-wanting-at-rest.wav"


def main():
    dur = 9 * 60
    n = int(dur * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(3)

    # the beat eases from 5.5 hz down to 4.5 and back, one slow breath
    x = t / dur
    beat = 5.5 - np.sin(np.pi * np.clip(x * 1.6, 0.0, 1.0))

    left = 0.15 * np.sin(2 * np.pi * 220.0 * t)
    dphi = 2 * np.pi * np.cumsum(beat) / SR
    right = 0.15 * np.sin(2 * np.pi * 220.0 * t + dphi)

    # out-of-phase tremolo — the breathing
    trem = 0.86 + 0.14 * np.sin(2 * np.pi * 0.07 * t)
    left *= trem
    right *= 0.86 + 0.14 * np.sin(2 * np.pi * 0.07 * t + np.pi)

    # sub floor + faint air
    sub = 0.045 * np.sin(2 * np.pi * 55.0 * t)
    air = 0.0012 * rng.standard_normal(n)

    # octave swells every two minutes
    swells = np.zeros(n)
    for t0 in (60.0, 180.0, 300.0, 420.0):
        i0 = int(t0 * SR)
        i1 = min(i0 + int(50 * SR), n)
        seg = i1 - i0
        win = np.sin(np.linspace(0, np.pi, seg)) ** 2
        swells[i0:i1] += 0.040 * win * np.sin(
            2 * np.pi * 440.0 * t[i0:i1] + np.sin(2 * np.pi * 0.5 * t[i0:i1])
        )

    fade_in = int(16 * SR)
    fade_out = int(20 * SR)
    ramp = np.ones(n)
    ramp[:fade_in] = np.linspace(0.0, 1.0, fade_in)
    ramp[-fade_out:] = np.linspace(1.0, 0.0, fade_out)

    L = (left + sub + air + swells) * ramp
    R = (right + sub + air + swells) * ramp
    write_wav(OUT, np.stack([L, R], axis=1))
    print(OUT, stats(OUT))


if __name__ == "__main__":
    main()
