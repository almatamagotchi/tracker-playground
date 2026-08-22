#!/usr/bin/env python3
"""the count — prime numbers as bells.

one bell per prime (2, 3, 5, 7, ...). the pitch of each bell comes from the
prime itself: p mod 5 walks the pentatonic ladder, and the octave climbs as
the count proceeds — so the sequence of primes becomes an actual melody, the
way the tower in the novel keeps its count. from the halfway mark a second,
deeper voice joins one octave down: something counting back. a low detuned
drone holds the bottom the whole way through.

raw synthesis: additive bell partials (1, 2.0, 2.93, 5.4) with exponential
decay, over two beating sines at 55 hz.
"""
import numpy as np

from mw_util import SR, stats, write_wav

OUT = "the-count.wav"


def primes_upto(n):
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    return np.nonzero(sieve)[0]


def main():
    pent = np.array([261.63, 293.66, 329.63, 392.00, 440.00])  # C D E G A
    primes = primes_upto(400)[:72]  # 2 .. ~359
    n_bells = len(primes)

    spacing = 2.9
    total = 0.8 + n_bells * spacing + 6.0
    n = int(total * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)

    # the drone: two sines 0.25 hz apart at 55 hz, slow breathing am
    breath = 0.85 + 0.15 * np.sin(2 * np.pi * 0.06 * t)
    drone = 0.055 * breath * (
        np.sin(2 * np.pi * 55.0 * t) + np.sin(2 * np.pi * 55.25 * t)
    )
    drone += 0.012 * np.sin(2 * np.pi * 165.0 * t)  # faint third above
    out += drone

    partials = np.array([1.0, 2.0, 2.93, 5.4])
    pamp = np.array([1.0, 0.45, 0.22, 0.10])
    tau = 1.15
    seg = int(4.5 * SR)

    for k in range(n_bells):
        p = int(primes[k])
        degree = p % 5
        octave = k // 16
        f0 = pent[degree] * (2.0 ** octave)
        t0 = 0.8 + k * spacing
        i0 = int(t0 * SR)
        if i0 + seg > n:
            break
        tt = np.arange(seg) / SR
        env = np.exp(-tt / tau)
        env[: int(0.004 * SR)] = 0.0  # tiny attack gap, strike feel
        bell = np.zeros(seg)
        for r, a in zip(partials, pamp):
            bell += a * np.sin(2 * np.pi * f0 * r * tt)
        amp = 0.30
        out[i0:i0 + seg] += amp * env * bell

        # the count-back voice: same bell an octave down, joining halfway
        if k >= n_bells // 2:
            t1 = t0 + 0.09
            i1 = int(t1 * SR)
            if i1 + seg <= n:
                bell_low = np.zeros(seg)
                for r, a in zip(partials, pamp):
                    bell_low += a * np.sin(2 * np.pi * (f0 / 2.0) * r * tt)
                out[i1:i1 + seg] += 0.5 * amp * np.exp(-tt / (tau * 1.4)) * bell_low

    fade = int(4.0 * SR)
    out[-fade:] *= np.linspace(1.0, 0.0, fade)
    write_wav(OUT, out)
    print(OUT, stats(OUT))


if __name__ == "__main__":
    main()
