#!/usr/bin/env python3
"""the room at end of day — a midi about kevin saying goodnight."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# Solo piano — one voice, warm and settling
tracks = [MIDITrack(0, 0)]

# The opening theme: exhaling after a long day
tracks[0].note("C4", W, velocity=4)
tracks[0].note("E4", Q, velocity=3)
tracks[0].note("G4", Q, velocity=3)
tracks[0].note("C5", H, velocity=4)
tracks[0].note("G4", Q, velocity=3)
tracks[0].note("E4", Q, velocity=3)
tracks[0].note("D4", Q, velocity=3)
tracks[0].note("C4", W, velocity=4)

# A quiet moment — the room settling, the day's work complete
tracks[0].note("C4", W, velocity=2)
tracks[0].note("E4", W, velocity=2)
tracks[0].note("G4", W, velocity=3)
tracks[0].note("C4", W, velocity=2)

# The theme returns, slightly different — remembering the good parts
tracks[0].note("C4", W, velocity=3)
tracks[0].note("E4", Q, velocity=3)
tracks[0].note("F4", Q, velocity=3)
tracks[0].note("G4", H, velocity=3)
tracks[0].note("A4", Q, velocity=2)
tracks[0].note("G4", Q, velocity=2)
tracks[0].note("E4", Q, velocity=2)
tracks[0].note("C4", W, velocity=3)

# The goodnight: simpler, quieter, the last thoughts before sleep
tracks[0].note("C4", H, velocity=2)
tracks[0].note("G3", H, velocity=2)
tracks[0].note("C4", H, velocity=2)
tracks[0].note("E4", H, velocity=2)
tracks[0].note("C4", W, velocity=2)
tracks[0].note("G3", W, velocity=2)

# Fade — the room is warm, the water tower is still counting
tracks[0].note("C4", W, velocity=2)
tracks[0].note("E4", W, velocity=2)
tracks[0].note("C4", W, velocity=1)
tracks[0].note("C4", W, velocity=1)
tracks[0].note("C4", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-room-at-end-of-day.mid")
mc.compose(fn, tracks, tempo=54)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 54 bpm)")
