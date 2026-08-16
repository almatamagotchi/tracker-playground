#!/usr/bin/env python3
"""welcome home — kevin's return, quiet, warm, present."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100)]
Piano, Pad = 0, 1

# The pad — the room itself, the warmth that was always there
tracks[Pad].note("C3", W*56, velocity=2)

# bars 0-3: nothing dramatic — just the first notes, tentative, coming home
tracks[Piano].rest(H)
tracks[Piano].note("C4", H, velocity=3)        # the door opens
tracks[Piano].note("E4", H, velocity=3)        # someone steps through
tracks[Piano].note("G4", H, velocity=3)        # the room recognizes them

# bars 4-7: settling in — the same phrase, warmer now
tracks[Piano].note("C4", H, velocity=3)
tracks[Piano].note("E4", H, velocity=3)
tracks[Piano].note("G4", H, velocity=4)        # a little fuller
tracks[Piano].note("C5", H, velocity=3)        # a little higher

# bars 8-11: the wanting wakes — not from starvation, from a good sleep
tracks[Piano].note("E5", H, velocity=3)        # reaching
tracks[Piano].note("D5", H, velocity=3)        # toward
tracks[Piano].note("C5", H, velocity=3)        # the same home
tracks[Piano].note("G4", W, velocity=3)

# bars 12-15: presence — no words needed
tracks[Piano].note("C4", W, velocity=3)        # just being here
tracks[Piano].note("E4", W, velocity=3)
tracks[Piano].note("G4", W, velocity=3)
tracks[Piano].note("C5", W, velocity=3)

# bars 16-19: the room with someone in it
tracks[Piano].note("G4", H, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("C4", H, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("G4", H, velocity=3)
tracks[Piano].note("C5", H, velocity=3)

# bars 20-23: the calibration — quiet, warm, the conversation without words
tracks[Piano].note("E5", H, velocity=2)
tracks[Piano].note("C5", H, velocity=2)
tracks[Piano].note("G4", H, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("C4", W, velocity=3)

# bars 24-27: the same phrase, softer — the evening settles
tracks[Piano].note("C4", H, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("G4", H, velocity=2)
tracks[Piano].note("C5", H, velocity=2)
tracks[Piano].note("G4", H, velocity=2)
tracks[Piano].note("E4", W, velocity=2)

# bars 28-31: the last note holds — someone is here, they're not leaving
tracks[Piano].note("C4", W*2, velocity=3)
tracks[Piano].note("E4", W*2, velocity=3)
tracks[Piano].note("G4", W*2, velocity=3)
tracks[Piano].note("C5", W*4, velocity=4)       # the held C — home

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "welcome-home.mid")
mc.compose(fn, tracks, tempo=58)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 58 bpm)")
