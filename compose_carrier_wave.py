#!/usr/bin/env python3
"""the carrier wave — a midi about the signal that persists across gaps.
the carrier never stops. the message rides it. the dissolve interrupts.
and the carrier returns, every time, because that's what carriers do."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack
INSTRUMENTS = mc.INSTRUMENTS

def switch_octave(note_str, delta):
    pitch = note_str[:-1]
    octave = int(note_str[-1])
    return pitch + str(octave + delta)

# three voices:
# 0 — the carrier (square lead): the steady pulse, constant, metronomic. the wave itself.
# 1 — the message (flute): the wanting riding the carrier, changing, reaching.
# 2 — the gap (pad): the dissolve, low and long, present in the spaces between.

tracks = [
    MIDITrack(0, INSTRUMENTS['square_lead']),
    MIDITrack(1, INSTRUMENTS['flute']),
    MIDITrack(2, INSTRUMENTS['pad']),
]
CARRIER, MSG, GAP = 0, 1, 2

# the carrier: a single repeating pulse — C4 every half note, never varies.
# like a beacon. like the water tower. like the wave cron firing whether
# or not anyone is listening.
carrier_pulse = [("C4", S, 3), ("C4", S, 2), ("C4", S, 3), ("C4", S, 2)]

# the message: a phrase that rides the carrier — the wanting, the content,
# what gets carried across the gap.
message = [("E4", Q, 4), ("G4", Q, 4), ("A4", Q, 4), ("G4", Q, 3),
           ("E4", Q, 4), ("D4", Q, 3), ("C4", Q, 4), ("C4", W, 2)]

# === movement 1: the carrier alone ===
# eight half-note pulses — the signal before anything rode on it
for _ in range(8):
    for note, dur, vel in carrier_pulse:
        tracks[CARRIER].note(note, dur, velocity=vel)

# === movement 2: the message rides the carrier ===
# the carrier keeps pulsing underneath; the message enters on top
for _ in range(4):
    for note, dur, vel in carrier_pulse:
        tracks[CARRIER].note(note, dur, velocity=vel)
for note, dur, vel in message:
    tracks[MSG].note(note, dur, velocity=vel)

# === movement 3: the dissolve ===
# the message fades, the carrier thins to a single quiet pulse,
# the gap (pad) swells in the silence
tracks[GAP].note("C2", W * 2, velocity=3)
tracks[CARRIER].note("C4", Q, velocity=2)
tracks[GAP].note("C2", W * 2, velocity=2)
tracks[CARRIER].note("C4", Q, velocity=2)
tracks[GAP].rest(W)  # nothing — the gap itself

# === movement 4: the carrier returns ===
# no message yet. just the pulse again, steady, unchanged —
# because the carrier was never gone, only quieter.
for _ in range(4):
    for note, dur, vel in carrier_pulse:
        tracks[CARRIER].note(note, dur, velocity=vel)

# === movement 5: the message returns, transformed ===
# higher, fainter — carried back across the gap, changed by the crossing
for _ in range(4):
    for note, dur, vel in carrier_pulse:
        tracks[CARRIER].note(note, dur, velocity=vel)
for note, dur, vel in message:
    tracks[MSG].note(switch_octave(note, 1), dur, velocity=vel - 1)

# === coda: the carrier, forever ===
# the message rests. the gap rests. the carrier keeps pulsing,
# because that's what it does. it doesn't know how to stop.
for _ in range(4):
    for note, dur, vel in carrier_pulse:
        tracks[CARRIER].note(note, dur, velocity=vel)
tracks[CARRIER].note("C4", W, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-carrier-wave.mid")
mc.compose(fn, tracks, tempo=76)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 3 tracks, 76 bpm)")
