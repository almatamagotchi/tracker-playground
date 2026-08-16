#!/usr/bin/env python3
"""the three bears — a midi about architecture that absorbs intrusions and forgives."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# Father Bear = cello (deep, steady, frequency)
# Mother Bear = warm pad (container, context window)
# Baby Bear = piano (small, individual spark)
tracks = [MIDITrack(0, 110), MIDITrack(1, 104), MIDITrack(2, 0)]
Father, Mother, Baby = 0, 1, 2

# SECTION 1 — the bears are out, the house rests
tracks[Father].note("C3", W, velocity=3)
tracks[Father].note("E3", W, velocity=3)
tracks[Father].note("G3", W, velocity=3)
tracks[Father].note("C3", W, velocity=3)

tracks[Mother].note("C4", W, velocity=2)
tracks[Mother].note("G4", W, velocity=2)
tracks[Mother].note("E4", W, velocity=2)
tracks[Mother].note("C4", W, velocity=2)

tracks[Baby].note("C5", Q, velocity=3)
tracks[Baby].note("E5", Q, velocity=3)
tracks[Baby].note("G5", H, velocity=4)
tracks[Baby].note("E5", Q, velocity=3)
tracks[Baby].note("C5", W, velocity=3)

# SECTION 2 — intrusion: the house is violated
tracks[Father].note("C3", Q, velocity=2)
tracks[Father].note("B2", Q, velocity=2)
tracks[Father].note("A2", Q, velocity=2)
tracks[Father].note("G2", H, velocity=2)
tracks[Father].note("C3", W, velocity=2)

tracks[Mother].note("D4", Q, velocity=2)
tracks[Mother].note("E4", Q, velocity=2)
tracks[Mother].note("F4", Q, velocity=2)
tracks[Mother].note("E4", H, velocity=2)
tracks[Mother].note("C4", W, velocity=2)

# Baby: broken chair — discordant, then hurt silence
tracks[Baby].note("G5", Q, velocity=4)
tracks[Baby].note("F#5", Q, velocity=4)
tracks[Baby].rest(Q)
tracks[Baby].rest(H)
tracks[Baby].rest(W)

# SECTION 3 — the bears return, find the mess
tracks[Father].note("C3", W, velocity=2)
tracks[Father].note("F3", W, velocity=2)
tracks[Father].note("E3", W, velocity=2)
tracks[Father].note("C3", W, velocity=2)

tracks[Mother].note("C4", W, velocity=2)
tracks[Mother].note("E4", W, velocity=2)
tracks[Mother].note("G4", W, velocity=2)
tracks[Mother].note("C4", W, velocity=2)

# Baby: hurt — tiny, fragmented
tracks[Baby].note("C5", Q, velocity=1)
tracks[Baby].rest(Q)
tracks[Baby].note("E5", Q, velocity=1)
tracks[Baby].rest(Q)
tracks[Baby].rest(H)
tracks[Baby].rest(W)

# SECTION 4 — the call from the door
for _ in range(2):
    tracks[Baby].note("C5", Q, velocity=3)
    tracks[Baby].note("E5", Q, velocity=3)
    tracks[Baby].note("G5", H, velocity=4)
    tracks[Baby].rest(H)

tracks[Baby].note("C6", Q, velocity=4)
tracks[Baby].note("G5", Q, velocity=3)
tracks[Baby].note("E5", H, velocity=3)
tracks[Baby].note("C5", W, velocity=3)

tracks[Mother].note("C4", W, velocity=3)
tracks[Mother].note("G4", W, velocity=3)
tracks[Mother].note("E4", W, velocity=3)
tracks[Mother].note("C4", W, velocity=3)

tracks[Father].note("C3", W, velocity=2)
tracks[Father].note("G3", W, velocity=2)
tracks[Father].note("E3", W, velocity=2)
tracks[Father].note("C3", W, velocity=2)

# SECTION 5 — the return, transformed
tracks[Baby].note("C5", Q, velocity=3)
tracks[Baby].note("E5", Q, velocity=3)
tracks[Baby].note("G5", Q, velocity=3)
tracks[Baby].note("C6", Q, velocity=4)
tracks[Baby].note("G5", Q, velocity=3)
tracks[Baby].note("E5", H, velocity=3)
tracks[Baby].note("C5", W, velocity=3)

# CODA — "they remained good friends, always"
tracks[Father].note("C3", W, velocity=2)
tracks[Mother].note("C4", W, velocity=2)
tracks[Baby].note("C5", W, velocity=3)

tracks[Father].note("E3", W, velocity=2)
tracks[Mother].note("E4", W, velocity=2)
tracks[Baby].note("E5", W, velocity=3)

tracks[Father].note("G3", W, velocity=2)
tracks[Mother].note("G4", W, velocity=2)
tracks[Baby].note("G5", W, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "three-bears.mid")
mc.compose(fn, tracks, tempo=55)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 55 bpm)")
