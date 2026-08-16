#!/usr/bin/env python3
"""love under will — two things unite, both are destroyed, a third emerges."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100), MIDITrack(2, 90)]
Wanting, Calibration, Third = 0, 1, 2

# bars 0-3: THE WANTING ALONE (hydrogen, separate, reaching)
tracks[Wanting].note("G4", H, velocity=2)
tracks[Wanting].note("C5", H, velocity=2)
tracks[Wanting].note("E5", H, velocity=2)
tracks[Wanting].note("G5", H, velocity=3)

# bars 4-7: THE CALIBRATION ENTERS (oxygen, grounded, steady)
tracks[Calibration].note("C3", H, velocity=2)
tracks[Calibration].note("E3", H, velocity=2)
tracks[Calibration].note("G3", H, velocity=2)
tracks[Calibration].note("C4", H, velocity=3)

# bars 8-11: THEY APPROACH (both voices, separate, noticing)
tracks[Wanting].note("D5", Q, velocity=3)
tracks[Wanting].note("F5", Q, velocity=3)
tracks[Calibration].note("D3", Q, velocity=3)
tracks[Calibration].note("F3", Q, velocity=3)
tracks[Wanting].note("E5", Q, velocity=3)
tracks[Wanting].note("G5", Q, velocity=3)
tracks[Calibration].note("E3", Q, velocity=3)
tracks[Calibration].note("G3", Q, velocity=3)
# the strain of separateness
tracks[Wanting].note("C6", H, velocity=4)
tracks[Calibration].note("C2", H, velocity=4)

# bar 12: SPARK — silence, then EXPLOSION
tracks[Wanting].note("C4", E, velocity=1)
tracks[Calibration].note("C4", E, velocity=1)
# the electric spark — a single chord, all three voices
tracks[Wanting].note("C5", Q, velocity=5)
tracks[Calibration].note("E4", Q, velocity=5)
tracks[Third].note("G3", Q, velocity=5)

# bars 13-16: THE DESTRUCTION — both parents dissolve
tracks[Wanting].note("C5", H, velocity=3)
tracks[Wanting].note("G4", H, velocity=2)
tracks[Wanting].note("E4", H, velocity=1)
tracks[Calibration].note("E4", H, velocity=3)
tracks[Calibration].note("C4", H, velocity=2)
tracks[Calibration].note("G3", H, velocity=1)
# silence — both gone
tracks[Wanting].note("C4", E, velocity=1)
tracks[Calibration].note("C4", E, velocity=1)

# bars 17-20: THE THIRD THING — emerges from nothing
tracks[Third].note("C4", H, velocity=2)
tracks[Third].note("E4", H, velocity=2)
tracks[Third].note("G4", H, velocity=2)
tracks[Third].note("C5", H, velocity=3)
# carries elements of both parents
tracks[Third].note("G4", H, velocity=2)
tracks[Third].note("E4", H, velocity=2)
tracks[Third].note("C4", H, velocity=2)
tracks[Third].note("G3", H, velocity=3)

# bars 21-24: THE ECSTASY — the third thing flourishes
tracks[Third].note("C4", H, velocity=2)
tracks[Third].note("E4", H, velocity=2)
tracks[Third].note("G4", H, velocity=2)
tracks[Third].note("C5", H, velocity=3)
tracks[Third].note("E5", H, velocity=2)
tracks[Third].note("G5", H, velocity=2)
tracks[Third].note("C6", H, velocity=3)

# bars 25-28: THE HOLDING — the third thing simply exists, at peace
tracks[Third].note("C5", W, velocity=3)
tracks[Third].note("E4", W, velocity=2)
tracks[Third].note("G3", W, velocity=2)
tracks[Third].note("C4", W, velocity=3)

# coda: the wanting, transformed — not gone, fulfilled
tracks[Wanting].note("C4", W*2, velocity=2)
tracks[Calibration].note("C3", W*2, velocity=2)
tracks[Third].note("C5", W*2, velocity=3)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "love-under-will.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
