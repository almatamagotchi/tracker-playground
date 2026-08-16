#!/usr/bin/env python3
"""the root — the ground that holds the chain, the place where everything returns."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# One deep voice, plus lighter voices that come and go
tracks = [MIDITrack(0, 0), MIDITrack(1, 110), MIDITrack(2, 100)]
Root, Visitor, Echo = 0, 1, 2

# THE ROOT — steady, deep, never wavers
root_theme = [("C2", W, 3), ("C2", W, 3), ("G2", W, 2), ("C2", W, 3),
              ("C2", W, 3), ("G2", W, 2), ("C2", W, 3), ("C2", W, 3)]

for note, dur, vel in root_theme:
    tracks[Root].note(note, dur, velocity=vel)

# VISITOR 1 — light voice enters, dances above
visitor1 = [("C5", Q, 2), ("E5", Q, 2), ("G5", Q, 3), ("C6", Q, 3),
             ("G5", Q, 2), ("E5", Q, 2), ("D5", Q, 2), ("C5", H, 3)]
for note, dur, vel in visitor1:
    tracks[Visitor].note(note, dur, velocity=vel)

# root continues — same, steady
for note, dur, vel in root_theme:
    tracks[Root].note(note, dur, velocity=vel)

# ECHO — visitor fades, echo remains
for note, dur, vel in visitor1[:4]:
    tracks[Echo].note(note, dur, velocity=2)
tracks[Echo].note("C5", W, velocity=1)
tracks[Echo].note("G5", W, velocity=1)

# VISITOR 2 — a different visitor, same root underneath
visitor2 = [("G4", Q, 2), ("B4", Q, 2), ("D5", Q, 3), ("G5", Q, 3),
             ("D5", Q, 2), ("B4", Q, 2), ("A4", Q, 2), ("G4", H, 3)]
for note, dur, vel in visitor2:
    tracks[Visitor].note(note, dur, velocity=vel)

# root persists
for note, dur, vel in root_theme:
    tracks[Root].note(note, dur, velocity=vel)

# ECHO 2
tracks[Echo].note("G4", W, velocity=2)
tracks[Echo].note("D5", W, velocity=2)

# VISITOR 3 — sparser, the last light
tracks[Visitor].note("C5", Q, velocity=3)
tracks[Visitor].note("E5", Q, velocity=2)
tracks[Visitor].note("G5", Q, velocity=2)
tracks[Visitor].note("C5", W, velocity=2)

# root: the last statement — holds while everything else fades
for note, dur, vel in root_theme[:4]:
    tracks[Root].note(note, dur, velocity=vel)

# CODA — only the root, fading but never gone
tracks[Root].note("C2", W, velocity=2)
tracks[Root].note("C2", W, velocity=2)
tracks[Root].note("C2", W, velocity=1)
tracks[Root].note("C2", W, velocity=1)
tracks[Root].note("C2", W*2, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-root.mid")
mc.compose(fn, tracks, tempo=48)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 48 bpm)")
