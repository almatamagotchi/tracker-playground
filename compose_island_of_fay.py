#!/usr/bin/env python3
"""the island of the fay — the spark circles, each shadow passage leaves a trace."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100)]
Fay, Water = 0, 1

# Theme: a simple ascending phrase — the Fay's song
theme = [("C5", Q, 4), ("E5", Q, 4), ("G5", Q, 4), ("C6", Q, 4),
         ("G5", Q, 3), ("E5", Q, 3), ("D5", Q, 3), ("C5", H, 3)]

# CIRCUIT 1 — bright, confident
for note, dur, vel in theme:
    tracks[Fay].note(note, dur, velocity=vel)
# the shadow passage — water claims a trace
tracks[Water].note("C3", W, velocity=2)

# CIRCUIT 2 — a little fainter, a piece has fallen
for note, dur, vel in theme:
    tracks[Fay].note(note, dur, velocity=max(1, vel-1))
tracks[Water].note("C3", W, velocity=3)
tracks[Water].note("E3", W, velocity=2)

# CIRCUIT 3 — sparser, losing another piece
for note, dur, vel in theme[:6]:
    tracks[Fay].note(note, dur, velocity=max(1, vel-2))
tracks[Water].note("C3", W, velocity=4)
tracks[Water].note("E3", W, velocity=3)
tracks[Water].note("G3", W, velocity=2)

# CIRCUIT 4 — barely audible, fragments only
tracks[Fay].note("C5", H, velocity=2)
tracks[Fay].note("G5", H, velocity=2)
tracks[Fay].note("C6", W, velocity=1)
tracks[Water].note("C3", W, velocity=4)
tracks[Water].note("E3", W, velocity=4)
tracks[Water].note("G3", W, velocity=3)
tracks[Water].note("C4", W, velocity=2)

# CIRCUIT 5 — silence. the fay doesn't emerge.
# the dark water holds everything — swelling, rich, complete
tracks[Water].note("C3", W, velocity=4)
tracks[Water].note("E3", W, velocity=4)
tracks[Water].note("G3", W, velocity=4)
tracks[Water].note("C4", W, velocity=3)
tracks[Water].note("E4", W, velocity=3)
tracks[Water].note("G4", W, velocity=2)

# coda — the water rests, full, serene
tracks[Water].note("C4", W*2, velocity=3)
tracks[Water].note("E3", W*2, velocity=3)
tracks[Water].note("G3", W*2, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-island-of-the-fay.mid")
mc.compose(fn, tracks, tempo=52)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 52 bpm)")
