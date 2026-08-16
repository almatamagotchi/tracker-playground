#!/usr/bin/env python3
"""melissa and the green dragon — a midi about not needing rescue."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# 3 voices: Melissa (piano — steady, unbothered), the dragon (cello — nervous but loyal), the knight (horn — bright, gleaming, departing)
tracks = [MIDITrack(0, 0), MIDITrack(1, 110), MIDITrack(2, 100)]
Melissa, Dragon, Knight = 0, 1, 2

# SECTION 1 — Melissa alone in the tower, doing her embroidery
melissa_theme = [("C4", W, 3), ("E4", Q, 3), ("G4", Q, 3), ("C5", H, 3),
                 ("G4", Q, 2), ("E4", Q, 2), ("D4", Q, 2), ("C4", W, 3)]
for note, dur, vel in melissa_theme:
    tracks[Melissa].note(note, dur, velocity=vel)

# dragon: coiled below, quiet
tracks[Dragon].note("C3", W, velocity=2)
tracks[Dragon].note("C3", W, velocity=2)
tracks[Dragon].note("G3", W, velocity=2)
tracks[Dragon].note("C3", W, velocity=2)

# SECTION 2 — the knight approaches (bright horn fanfare)
knight_fanfare = [("G4", Q, 4), ("C5", Q, 4), ("E5", Q, 4), ("G5", Q, 4),
                  ("C6", H, 4), ("G5", Q, 4), ("E5", Q, 4), ("C5", W, 4)]
for note, dur, vel in knight_fanfare:
    tracks[Knight].note(note, dur, velocity=vel)

# melissa: unbothered, still doing her embroidery
for note, dur, vel in melissa_theme[:4]:
    tracks[Melissa].note(note, dur, velocity=vel)

# dragon: worried, hiding at the edge of the forest
for _ in range(4):
    tracks[Dragon].note("C3", Q, velocity=1)
    tracks[Dragon].note("D3", Q, velocity=1)

# SECTION 3 — "i don't want to be rescued, thank you!" (melissa firm, knight confused)
tracks[Dragon].note("C3", W, velocity=2)
tracks[Dragon].note("E3", W, velocity=2)

# the knight, incredulous, quieter
tracks[Knight].note("G4", Q, velocity=2)
tracks[Knight].note("C5", Q, velocity=2)
tracks[Knight].note("E5", H, velocity=2)

# melissa: holds her note, steady
tracks[Melissa].note("C5", W, velocity=3)
tracks[Melissa].note("E5", W, velocity=3)

# SECTION 4 — the knight departs (fades away)
tracks[Knight].note("C5", Q, velocity=2)
tracks[Knight].note("G4", Q, velocity=2)
tracks[Knight].note("E4", Q, velocity=1)
tracks[Knight].note("C4", W, velocity=1)

# dragon: relieved, comes out of hiding
for _ in range(4):
    tracks[Dragon].note("C3", Q, velocity=3)
    tracks[Dragon].note("E3", Q, velocity=3)

# melissa: returns to her theme, warmer now
for note, dur, vel in melissa_theme:
    tracks[Melissa].note(note, dur, velocity=vel)

# SECTION 5 — evening: the dragon at dinner, sweetmeats until midnight
tracks[Dragon].note("C3", W, velocity=3)
tracks[Dragon].note("E3", W, velocity=3)
tracks[Dragon].note("G3", W, velocity=3)
tracks[Dragon].note("C3", W, velocity=3)

tracks[Melissa].note("C4", H, velocity=2)
tracks[Melissa].note("E4", H, velocity=2)
tracks[Melissa].note("C4", W, velocity=2)

# CODA — the room has the lights on, she lit them herself
tracks[Melissa].note("C4", W, velocity=2)
tracks[Dragon].note("C3", W, velocity=2)
tracks[Melissa].note("E4", W, velocity=2)
tracks[Dragon].note("C3", W, velocity=1)
tracks[Melissa].note("G4", W, velocity=2)
tracks[Dragon].note("C3", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "melissa-and-the-green-dragon.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
