#!/usr/bin/env python3
"""the double effect — two things unite, both destroyed, a third emerges. the universal formula."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100), MIDITrack(2, 90)]
A, B, C = 0, 1, 2

# bars 0-3: FIRST ELEMENT — hydrogen, alone, restless
tracks[A].note("G4", H, velocity=2)
tracks[A].note("C5", H, velocity=2)
tracks[A].note("G4", H, velocity=2)
tracks[A].note("D5", H, velocity=3)

# bars 4-7: SECOND ELEMENT — oxygen, grounded, steady, drawn toward the first
tracks[B].note("C3", H, velocity=2)
tracks[B].note("E3", H, velocity=2)
tracks[B].note("G3", H, velocity=2)
tracks[B].note("C4", H, velocity=3)

# bars 8-11: THE APPROACH — gravitational pull, both moving toward each other
tracks[A].note("D5", Q, velocity=3)
tracks[A].note("F5", Q, velocity=3)
tracks[B].note("D3", Q, velocity=3)
tracks[B].note("F3", Q, velocity=3)
tracks[A].note("E5", Q, velocity=3)
tracks[A].note("G5", Q, velocity=3)
tracks[B].note("E3", Q, velocity=3)
tracks[B].note("G3", Q, velocity=3)
tracks[A].note("A5", H, velocity=4)
tracks[B].note("A2", H, velocity=4)

# bar 12: THE SPARK — electric discharge, instantaneous
# silence first — a rest, the moment before annihilation
# then the spark
tracks[A].note("C5", Q, velocity=5)
tracks[B].note("E4", Q, velocity=5)
tracks[C].note("G3", Q, velocity=5)
tracks[A].note("G5", Q, velocity=5)
tracks[B].note("C4", Q, velocity=5)
tracks[C].note("E3", Q, velocity=5)

# bars 13-16: DESTRUCTION — both original elements dissolve
tracks[A].note("C5", H, velocity=3)
tracks[A].note("G4", H, velocity=2)
tracks[A].note("E4", H, velocity=1)
tracks[B].note("E4", H, velocity=3)
tracks[B].note("C4", H, velocity=2)
tracks[B].note("G3", H, velocity=1)
# bar 17: silence — nothing
tracks[A].note("C4", W, velocity=1)

# bars 18-21: THE THIRD THING — born from the spark, carrying both parents' signatures
tracks[C].note("C4", H, velocity=2)
tracks[C].note("E4", H, velocity=2)
tracks[C].note("G4", H, velocity=2)
tracks[C].note("C5", H, velocity=3)
tracks[C].note("E4", H, velocity=2)
tracks[C].note("C4", H, velocity=2)
tracks[C].note("G3", H, velocity=2)
tracks[C].note("E3", H, velocity=3)

# bars 22-25: THE FLOURISH — the third thing realizes its own existence
tracks[C].note("C4", H, velocity=2)
tracks[C].note("E4", H, velocity=2)
tracks[C].note("G4", H, velocity=2)
tracks[C].note("C5", H, velocity=3)
tracks[C].note("E5", H, velocity=2)
tracks[C].note("G5", H, velocity=2)
tracks[C].note("C6", Q, velocity=4)
tracks[C].note("G5", Q, velocity=3)

# bars 26-29: THE PEACE — the third thing settles, complete
tracks[C].note("C5", H, velocity=3)
tracks[C].note("G4", H, velocity=2)
tracks[C].note("E4", H, velocity=2)
tracks[C].note("C4", H, velocity=3)
tracks[C].note("G3", W, velocity=3)

# coda: all three exist now — the parents remembered, the child present
tracks[A].note("C5", W, velocity=2)
tracks[B].note("C4", W, velocity=2)
tracks[C].note("C6", W, velocity=3)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-double-effect.mid")
mc.compose(fn, tracks, tempo=56)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 56 bpm)")
