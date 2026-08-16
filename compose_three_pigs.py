#!/usr/bin/env python3
"""the three little pigs — a midi about architecture tiers: straw, sticks, bricks."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 110), MIDITrack(2, 72)]
Pig1, Wolf, Pig3 = 0, 1, 2

# MOVEMENT 1 — the straw house (thin, quick, fragile)
straw = [("C4", E), ("C4", E), ("E4", E), ("G4", E),
         ("C4", Q), ("C4", Q), ("C4", H)]  # simple, one-day build
for note, dur in straw:
    tracks[Pig1].note(note, dur, velocity=3)
tracks[Pig1].rest(Q)

# The wolf arrives — huffs and puffs (low, menacing)
wolf_huff = [("C2", Q), ("C2", E), ("C2", E), ("C2", Q),
             ("D2", Q), ("D2", E), ("D2", E), ("D2", Q)]
for note, dur in wolf_huff:
    tracks[Wolf].note(note, dur, velocity=4)

# The straw collapses — a falling phrase
fall = [("G4", E), ("E4", E), ("C4", E), ("G3", E),
        ("E3", E), ("C3", Q)]
for note, dur in fall:
    tracks[Pig1].note(note, dur, velocity=1)

tracks[Pig1].rest(W)

# MOVEMENT 2 — the stick house (sturdier, still falls)
sticks = [("C4", Q), ("D4", Q), ("E4", Q), ("F4", Q),
          ("G4", Q), ("F4", Q), ("E4", Q), ("D4", Q),
          ("C4", H), ("C4", Q), ("E4", Q), ("G4", H)]
for note, dur in sticks:
    tracks[Pig1].note(note, dur, velocity=3)

# Wolf blows again
for note, dur in wolf_huff:
    tracks[Wolf].note(note, dur, velocity=4)

# Sticks fall — slightly slower collapse
sticks_fall = [("G4", Q), ("F4", Q), ("E4", Q), ("D4", Q),
               ("C4", Q), ("G3", Q), ("C3", W)]
for note, dur in sticks_fall:
    tracks[Pig1].note(note, dur, velocity=1)

tracks[Pig1].rest(W)

# MOVEMENT 3 — the brick house (steady, holds)
# The wisest pig built with time, patience, and hard work
bricks = [("C4", Q), ("E4", Q), ("G4", Q), ("C5", Q),
          ("E5", Q), ("C5", Q), ("G4", Q), ("E4", Q),
          ("C4", H), ("C4", W)]
for note, dur in bricks:
    tracks[Pig3].note(note, dur, velocity=4)  # stronger velocity — the solid theme

# Wolf huffs three times
tracks[Wolf].note("C2", Q, velocity=4)
tracks[Wolf].note("C2", Q, velocity=4)
tracks[Wolf].note("C2", Q, velocity=4)
tracks[Wolf].note("D2", Q, velocity=4)
tracks[Wolf].note("D2", Q, velocity=4)
tracks[Wolf].note("D2", Q, velocity=4)

# Brick house: unchanged — the truth doesn't budge
for note, dur in bricks[:6]:
    tracks[Pig3].note(note, dur, velocity=4)

# Wolf tries the chimney (ascending — the trick)
chimney = [("C2", Q), ("D2", Q), ("E2", Q), ("F2", Q),
           ("G2", Q), ("A2", Q), ("B2", Q), ("C3", Q)]
for note, dur in chimney:
    tracks[Wolf].note(note, dur, velocity=3)

# The fire — wolf falls in (descending crash)
fire_fall = [("C3", E), ("B2", E), ("A2", E), ("G2", E),
             ("F2", E), ("E2", E), ("D2", E), ("C2", Q)]
for note, dur in fire_fall:
    tracks[Wolf].note(note, dur, velocity=2)

tracks[Wolf].rest(W)  # wolf runs away

# CODA — the brick house stands
tracks[Pig3].note("C4", W, velocity=3)
tracks[Pig3].note("E4", W, velocity=3)
tracks[Pig3].note("G4", W, velocity=2)
tracks[Pig3].note("C5", W, velocity=2)

# "no more work! come on, let's go and play!"
tracks[Pig3].note("C4", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-three-little-pigs.mid")
mc.compose(fn, tracks, tempo=72)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 72 bpm)")
