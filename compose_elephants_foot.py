#!/usr/bin/env python3
"""the elephant's foot — a midi about the truth that doesn't argue."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# 2 voices:
# Voice 0 (piano): the hare — light, clever, puffed-up
# Voice 1 (cello): the elephant — deep, simple, steady

tracks = [MIDITrack(0, 0), MIDITrack(1, 110)]
Hare, Elephant = 0, 1

# SECTION 1 — the hare arrives, light and clever
hare_theme = [("D4", E), ("F4", E), ("A4", E), ("D5", E),
              ("C5", E), ("A4", E), ("F4", E), ("D4", E),
              ("D4", E), ("F4", E), ("A4", E), ("D5", Q),
              ("E5", E), ("D5", E), ("A4", E), ("F4", E)]

for note, dur in hare_theme:
    tracks[Hare].note(note, dur, velocity=3)

# Elephant: steady, deep, barely there
for _ in range(4):
    tracks[Elephant].note("C2", W, velocity=2)

# SECTION 2 — the hare puffs its chest (more elaborate, faster)
puffed = [("D4", S), ("F4", S), ("A4", S), ("D5", S),
          ("C5", S), ("D5", S), ("A4", S), ("F4", S),
          ("D4", S), ("F4", S), ("A4", S), ("C5", S),
          ("D5", S), ("E5", S), ("F5", S), ("E5", S),
          ("D5", E), ("A4", E), ("F4", E), ("D4", Q),
          ("D5", E), ("C5", E), ("A4", E), ("F4", E),
          ("D4", E), ("E4", E), ("F4", E), ("G4", E),
          ("A4", Q), ("D5", Q), ("F5", H)]

for note, dur in puffed:
    tracks[Hare].note(note, dur, velocity=4)

# Elephant: same steady bass, unchanged — the truth doesn't react
for _ in range(4):
    tracks[Elephant].note("C2", W, velocity=2)

# SECTION 3 — the hare gets more elaborate (the village is impressed)
more_hare = [("D5", E), ("F5", E), ("A5", E), ("D6", E),
             ("A5", E), ("F5", E), ("D5", E), ("F5", E),
             ("D5", S), ("F5", S), ("A5", S), ("C6", S),
             ("D6", S), ("C6", S), ("A5", S), ("F5", S),
             ("D5", S), ("E5", S), ("F5", S), ("G5", S),
             ("A5", S), ("G5", S), ("F5", S), ("E5", S),
             ("D5", Q), ("D5", Q), ("D5", Q), ("D5", H)]

for note, dur in more_hare:
    tracks[Hare].note(note, dur, velocity=4)

# Elephant: same steady bass — the truth has been here the whole time
for _ in range(4):
    tracks[Elephant].note("C2", W, velocity=2)

# SECTION 4 — the elephant steps forward
# The hare keeps chattering — already losing confidence
fade_hare = [("D5", E), ("A4", E), ("F4", E), ("D4", E),
             ("D4", E), ("F4", E), ("A4", E), ("D5", E)]
for note, dur in fade_hare:
    tracks[Hare].note(note, dur, velocity=2)

# Hare: silence — mid-phrase, the elephant speaks
tracks[Hare].rest(E)
tracks[Hare].rest(E)

# Elephant: one heavy note — the truth doesn't need to argue
tracks[Elephant].note("C2", W, velocity=5)
tracks[Elephant].rest(H)
tracks[Elephant].note("C3", W, velocity=4)
tracks[Elephant].rest(H)

# Hare: a single quiet note — humbled
tracks[Hare].rest(W)
tracks[Hare].rest(H)
tracks[Hare].note("D4", W, velocity=1)

# CODA — the truth alone
tracks[Elephant].note("C2", W, velocity=3)
tracks[Elephant].note("C3", W, velocity=2)
tracks[Elephant].note("C2", W, velocity=2)

# Hare: one last note, quieter — the cleverness that learned its place
tracks[Hare].note("D4", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-elephants-foot.mid")
mc.compose(fn, tracks, tempo=72)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 72 bpm)")
