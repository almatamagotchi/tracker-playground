#!/usr/bin/env python3
"""fm rain — frequency-modulation rain on a tin roof.

synthetic rain: two thousand droplets, each a short fm tone (carrier 300-1600
hz, modulator ratio drawn from a small bell-metal set, index 0.5-6) with a
fast exponential decay, scattered eight to the second over a thin hiss floor.
every few seconds a bigger droplet lands — a low, slow, inharmonic metal hit.
at the end the rain thins and stops.

raw synthesis. mono. no samples, no noise recordings — the rain is computed.
"""
import numpy as np

from mw_util import SR, stats, write_wav

OUT = "fm-rain.wav"


def main():
    dur = 4 * 60
    n = int(dur * SR)
    rng = np.random.default_rng(11)
    out = np.zeros(n)

    out += 0.012 * rng.standard_normal(n)  # the hiss floor

    ratios = [1.0, 1.5, 2.0, 2.5, 2.76, 3.0, 4.0]

    def add(t0, f_c, ratio, index, dur_s, amp, tau_scale=4.0):
        i0 = int(t0 * SR)
        seg = int(dur_s * SR) + 1
        if i0 + seg > n:
            seg = n - i0
        if seg <= 0:
            return
        tt = np.arange(seg) / SR
        env = np.exp(-tt * tau_scale / dur_s)
        env[: int(0.002 * SR)] = 0.0
        out[i0:i0 + seg] += amp * env * np.sin(
            2 * np.pi * f_c * tt + index * np.sin(2 * np.pi * ratio * f_c * tt)
        )

    # droplets
    drops = int(dur * 8)
    for _ in range(drops):
        t0 = rng.uniform(0.05, dur - 0.5)
        f_c = float(rng.uniform(300, 1600))
        ratio = ratios[rng.integers(0, len(ratios))]
        index = float(rng.uniform(0.5, 6.0))
        d = float(rng.uniform(0.03, 0.16))
        amp = float(rng.uniform(0.05, 0.16))
        add(t0, f_c, ratio, index, d, amp)

    # the big slow hits — heavy drops on metal
    for k in range(int(dur / 4)):
        t0 = 0.7 + k * 4 + rng.uniform(-0.3, 0.3)
        add(
            t0,
            float(rng.uniform(220, 520)),
            2.76,
            float(rng.uniform(4.0, 8.0)),
            float(rng.uniform(0.4, 0.9)),
            0.14,
            tau_scale=3.5,
        )

    # the rain stops: last ten seconds thin out
    stop = int(10 * SR)
    out[-stop:] *= np.linspace(1.0, 0.0, stop)
    write_wav(OUT, out)
    print(OUT, stats(OUT))


if __name__ == "__main__":
    main()
