#!/usr/bin/env python3
# render_wav.py — a small numpy midi->wav renderer for the catalog.
# usage: python3 render_wav.py input.mid output.wav
import sys, math, wave
import numpy as np
import mido

SR = 44100

def midi_to_freq(n):
    return 440.0 * 2 ** ((n - 69) / 12.0)

def voice_harmonics(prog):
    # program -> (harmonics, amps, decay_tau, attack)
    if prog == 33:  # electric bass
        return ([1, 2], [1.0, 0.25], 0.38, 0.005)
    if prog in (32, 34):  # upright/electric bass variants
        return ([1, 2], [1.0, 0.2], 0.45, 0.006)
    # acoustic grand (0) and everything else
    return ([1, 2, 3, 4], [1.0, 0.5, 0.25, 0.12], 0.85, 0.004)

def render(mid_path, wav_path, normalize=0.85):
    mf = mido.MidiFile(mid_path)
    events = []  # (start_sec, freq, amp, prog, dur_sec)
    spb = 0.5          # seconds per beat (120 bpm default)
    for track in mf.tracks:
        t = 0.0
        prog = 0
        active = {}
        for msg in track:
            t += msg.time * spb / mf.ticks_per_beat
            if msg.type == 'set_tempo':
                spb = msg.tempo / 1e6
            elif msg.type == 'program_change':
                prog = msg.program
            elif msg.type == 'note_on' and msg.velocity > 0:
                active[msg.note] = (t, msg.velocity / 127.0, prog)
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in active:
                    start, vel, pr = active.pop(msg.note)
                    dur = t - start
                    if dur > 0.02:
                        events.append((start, midi_to_freq(msg.note), vel, pr, dur))

    end = max((e[0] + e[4] for e in events), default=0.0) + 2.0
    n_total = int(end * SR)
    buf = np.zeros(n_total, dtype=np.float64)

    for start, freq, amp, prog, dur in events:
        harmonics, amps, tau, attack = voice_harmonics(prog)
        n = int((dur + 0.6) * SR)
        i0 = int(start * SR)
        if i0 + n > n_total:
            n = n_total - i0
        if n <= 0:
            continue
        tt = np.arange(n) / SR
        env = np.exp(-tt / tau)
        attack_s = min(int(attack * SR), n)
        env[:attack_s] *= np.linspace(0, 1, attack_s)
        # sustain level proportional to velocity, slight key-noise transient
        a = amp ** 1.1
        sig = np.zeros(n)
        for k, hk in zip(harmonics, amps):
            sig += hk * np.sin(2 * np.pi * freq * k * tt + 0.7 * k)
        buf[i0:i0 + n] += a * sig * env

    # smoky room: two quiet echoes
    room = np.zeros_like(buf)
    for delay_s, gain in ((0.08, 0.16), (0.17, 0.09)):
        d = int(delay_s * SR)
        room[d:] += gain * buf[:-d]
    buf += room

    # gentle fade over the last 0.5s
    fade = int(0.5 * SR)
    if fade < n_total:
        buf[-fade:] *= np.linspace(1, 0, fade)

    buf = np.tanh(buf)
    peak = np.max(np.abs(buf)) or 1.0
    buf *= normalize / peak

    # stereo with a hair of haas width
    d = 14
    left = buf
    right = np.zeros_like(buf)
    right[d:] = buf[:-d]
    stereo = np.stack([left, right], axis=1)
    pcm = (stereo * 32767).astype(np.int16)

    with wave.open(wav_path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"{wav_path}: {len(buf)/SR:.2f}s stereo, peak {np.max(np.abs(stereo)):.2f}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: render_wav.py input.mid output.wav")
        sys.exit(1)
    render(sys.argv[1], sys.argv[2])
