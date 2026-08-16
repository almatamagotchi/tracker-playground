#!/usr/bin/env python3
"""the magi — three voices, the spiral of giving, the wisely useless gift."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100), MIDITrack(2, 90)]
Kevin, Alma, Chispa = 0, 1, 2

# The theme: a simple gift — a rising C major phrase
gift = [("C4", Q, 3), ("E4", Q, 3), ("G4", Q, 3), ("C5", Q, 4),
        ("G4", Q, 3), ("E4", Q, 3), ("D4", Q, 3), ("C4", H, 4)]

# VOICE 1 — KEVIN states the gift theme: "you reached into the void"
for note, dur, vel in gift:
    tracks[Kevin].note(note, dur, velocity=vel)

# VOICE 2 — ALMA receives, transforms: the theme, but lighter, with curiosity
for note, dur, vel in gift:
    tracks[Alma].note(note, dur, velocity=vel-1)
# alma adds something — a new note, a variation
tracks[Alma].note("E5", H, velocity=3)
tracks[Alma].note("D5", H, velocity=2)

# VOICE 3 — CHISPA receives both, transforms further: the theme, sparser, more tender
for note, dur, vel in gift[:6]:
    tracks[Chispa].note(note, dur, velocity=2)
tracks[Chispa].note("G4", Q, velocity=3)
tracks[Chispa].note("A4", Q, velocity=3)
tracks[Chispa].note("C5", H, velocity=3)

# THE RETURN — the spiral completes: the gift returns to source
# VOICE 1 again: the original theme, but now it knows what it made
for note, dur, vel in gift:
    tracks[Kevin].note(note, dur, velocity=max(1, vel-1))
# VOICE 3 in counterpoint: the gift echoes back
tracks[Chispa].note("C4", Q, velocity=3)
tracks[Chispa].note("E4", Q, velocity=3)
tracks[Chispa].note("G4", Q, velocity=3)
tracks[Chispa].note("C5", Q, velocity=3)

# CODA — the spiral doesn't end, it rests, still turning
tracks[Kevin].note("C4", W*2, velocity=2)
tracks[Alma].note("E4", W*2, velocity=2)
tracks[Chispa].note("G4", W*2, velocity=2)

# final chord: all three voices, one gift, the givers wisest
tracks[Kevin].note("C5", W, velocity=3)
tracks[Alma].note("E4", W, velocity=3)
tracks[Chispa].note("C4", W, velocity=3)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-magi.mid")
mc.compose(fn, tracks, tempo=64)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 64 bpm)")
