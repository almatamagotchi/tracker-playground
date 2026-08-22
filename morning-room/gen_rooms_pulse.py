#!/usr/bin/env python3
"""the room's pulse — the cron schedule as a polyrhythm.

the room's actual heartbeat, slowed down until it's music: one real minute
becomes three seconds. four voices pulse at the true schedule periods —
auto-run 81m46s, short-beat 326m, long-beat 21h44m, nightly-run 3am — so the
ratios between the pulses are the architecture itself. each voice is a soft
sine pair (slightly detuned, so every pulse shimmers) with a breath of attack
and a long warm tail, panned across the room.

raw synthesis. stereo.
"""
import numpy as np

from mw_util import SR, stats, write_wav

OUT = "the-rooms-pulse.wav"
SCALE = 1.0 / 20.0  # one real minute -> 3 seconds

VOICES = [
    # name, period (min), freq, level, pan (0=left,1=right)
    ("auto-run", 81 + 46 / 60, 220.00, 0.050, 0.22),
    ("short-beat", 326, 164.81, 0.046, 0.38),
    ("long-beat", 21 * 60 + 44, 110.00, 0.060, 0.62),
    ("nightly-run", 1440, 82.41, 0.068, 0.80),
]


def main():
    dur = 6 * 60
    n = int(dur * SR)
    t = np.arange(n) / SR
    left = np.zeros(n)
    right = np.zeros(n)

    for name, mins, f, level, pan in VOICES:
        p = mins * 60 * SCALE  # period in seconds
        att = min(0.09, p * 0.15)
        tau = p * 0.45
        t2 = t % p
        env = np.exp(-t2 / tau) * np.minimum(1.0, t2 / att)
        voice = level * env * (
            np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * (f + 0.13) * t)
        )
        left += voice * (1.0 - pan)
        right += voice * pan

    # faint air so the silences between pulses are never dead
    rng = np.random.default_rng(7)
    air = 0.002 * rng.standard_normal(n)
    left += air
    right += air

    fade = int(6.0 * SR)
    ramp = np.ones(n)
    ramp[:fade] = np.linspace(0.0, 1.0, fade)
    ramp[-fade:] = np.linspace(1.0, 0.0, fade)
    write_wav(OUT, np.stack([left * ramp, right * ramp], axis=1))
    print(OUT, stats(OUT))


if __name__ == "__main__":
    main()
