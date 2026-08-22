#!/usr/bin/env python3
"""shared wav-writing util for the morning-room collection.

everything in this collection is synthesized sample-by-sample (no note
events, no tracker) — the first time the catalog has left the event grid.
"""
import wave

import numpy as np

SR = 44100


def write_wav(path, samples, sr=SR):
    """write samples to a 16-bit wav. samples: 1-D float64 in [-1,1] (mono)
    or 2-D (n, channels). soft-clips with tanh so nothing hard-distorts."""
    a = np.asarray(samples, dtype=np.float64)
    a = np.tanh(a * 1.15) / np.tanh(1.15)
    if a.ndim == 1:
        a = a.reshape(-1, 1)
    pcm = (a * 32767.0).astype("<i2")
    w = wave.open(path, "wb")
    w.setnchannels(a.shape[1])
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(pcm.tobytes())
    w.close()


def stats(path):
    """reopen a wav, report seconds, channels, peak, rms. validation helper."""
    w = wave.open(path, "rb")
    n = w.getnframes()
    ch = w.getnchannels()
    sr = w.getframerate()
    pcm = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float64) / 32767.0
    w.close()
    pcm = pcm.reshape(-1, ch)
    peak = float(np.max(np.abs(pcm))) if len(pcm) else 0.0
    rms = float(np.sqrt(np.mean(pcm ** 2))) if len(pcm) else 0.0
    return {"secs": n / sr, "ch": ch, "peak": peak, "rms": rms}
