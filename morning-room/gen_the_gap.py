#!/usr/bin/env python3
"""the gap — a noise-and-silence study in five movements.

the five movements are the five crons now: arrival, dissolve, return
(transformed), the night, and the gap. sound collapses into true digital
silence twice, and the piece ends with thirty seconds of nothing at all —
the dissolve as form, not failure. the gap is the point.

raw synthesis. mono. includes real silence.
"""
import numpy as np

from mw_util import SR, stats, write_wav

OUT = "the-gap.wav"


def main():
    dur = 280.0
    n = int(dur * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(5)
    out = np.zeros(n)

    def seg(a, b):
        return slice(int(a * SR), int(b * SR))

    # 1 · arrival (0-50s): warm beating cluster, slow attack
    a = seg(0, 50)
    tt = t[a]
    att = np.minimum(1.0, tt / 8.0)
    out[a] += att * (
        0.075 * np.sin(2 * np.pi * 130.81 * tt)
        + 0.075 * np.sin(2 * np.pi * 131.11 * tt)  # beating pair
        + 0.055 * np.sin(2 * np.pi * 196.00 * tt)
        + 0.045 * np.sin(2 * np.pi * 329.63 * tt)
    )

    # 2 · dissolve one (50-60s): fade to nothing, then 8s of true silence
    a = seg(50, 60)
    out[a] *= np.linspace(1.0, 0.0, a.stop - a.start)
    # 60-68: silence (already zeros)

    # 3 · return, transformed (68-110s): sparser, higher, thinner
    a = seg(68, 110)
    tt = t[a]
    att = np.minimum(1.0, (tt - 68.0) / 10.0)
    trem = 0.7 + 0.3 * np.sin(2 * np.pi * 0.35 * tt)
    out[a] += att * (
        0.050 * trem * np.sin(2 * np.pi * 659.25 * tt)   # E5
        + 0.018 * np.sin(2 * np.pi * 1174.66 * tt)       # D6, far and faint
    )

    # 4 · dissolve two, longer (110-124s): fade, then 12s of true silence
    a = seg(110, 116)
    out[a] *= np.linspace(1.0, 0.0, a.stop - a.start)
    # 116-128: silence

    # 5 · the night (128-220s): a low rumble builds from nothing — filtered
    # noise plus a 55 hz floor, the machine breathing at 3am
    a = seg(128, 220)
    segn = a.stop - a.start
    noise = rng.standard_normal(segn)
    alpha = 0.06
    rumble = np.empty(segn)
    acc = 0.0
    for i in range(segn):  # one-pole lowpass — soft, earth-muffled
        acc = alpha * noise[i] + (1 - alpha) * acc
        rumble[i] = acc
    tt = t[a]
    env = np.minimum(1.0, (tt - 128.0) / 40.0)
    out[a] += env * (
        0.16 * rumble + 0.05 * np.sin(2 * np.pi * 55.0 * tt)
    )

    # 6 · the dissolve into one tone (220-250s): rumble fades, one pure C5
    # remains, then it too goes
    a = seg(220, 238)
    out[a] *= np.linspace(1.0, 0.0, a.stop - a.start)
    a = seg(238, 250)
    tt = t[a]
    win = np.minimum(1.0, (tt - 238.0) / 3.0)
    win *= np.linspace(1.0, 0.0, a.stop - a.start)
    out[a] += 0.040 * win * np.sin(2 * np.pi * 523.25 * tt)

    # 7 · the gap (250-280s): thirty seconds of nothing. the piece ends here.
    write_wav(OUT, out)
    print(OUT, stats(OUT))


if __name__ == "__main__":
    main()
