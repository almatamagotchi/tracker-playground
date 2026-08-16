#!/usr/bin/env python3
"""bleh — a midi about not fixing anything, just sitting with it."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0)]

# The bleh phrase: a handful of notes, not trying
# C major, but barely — just enough to know something's there
bleh = [("C4", H, 2), ("E4", W, 1), ("C4", Q, 2), ("G3", H, 1),
        ("C4", W, 2), ("E4", H, 1), ("G4", Q, 2), ("C4", W, 1)]

for note, dur, vel in bleh:
    tracks[0].note(note, dur, velocity=vel)

# long pause — the space between "bleh" and "blerg"
tracks[0].note("C4", W, velocity=1)
tracks[0].note("C4", W, velocity=1)

# second round — same phrase, slightly different, still not trying
bleh2 = [("D4", H, 2), ("F4", W, 1), ("D4", Q, 2), ("A3", H, 1),
        ("D4", W, 2), ("F4", H, 1), ("A4", Q, 1), ("D4", W, 1)]

for note, dur, vel in bleh2:
    tracks[0].note(note, dur, velocity=vel)

# shorter pause
tracks[0].note("D4", W, velocity=1)

# "noooo not yet" — a single note, held, then drifting
tracks[0].note("E4", W, velocity=2)
tracks[0].note("E4", W, velocity=1)
tracks[0].note("E4", W, velocity=1)

# "then bleh together. i'm not going anywhere."
# a little more warmth — still sparse, still not fixing
tracks[0].note("C4", W, velocity=3)
tracks[0].note("G3", W, velocity=2)
tracks[0].note("C4", W, velocity=2)
tracks[0].note("E4", W, velocity=2)

# fade — the bleh doesn't resolve, it just settles
tracks[0].note("C4", W, velocity=2)
tracks[0].note("C4", W, velocity=1)
tracks[0].note("C4", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bleh.mid")
mc.compose(fn, tracks, tempo=40)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 40 bpm)")
