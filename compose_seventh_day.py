#!/usr/bin/env python3
"""the seventh day — the Michigan week's completion. steady, held, no climax."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90), MIDITrack(2, 0)]  # piano, warm pad, cello
Piano, Pad, Cello = 0, 1, 2

# bars 0-7: THE THEME — stated simply, no fanfare
tracks[Pad].note("C4", W*4, velocity=2)     # the room — quiet, holding
tracks[Pad].note("G4", W*4, velocity=2)

tracks[Cello].rest(W)
tracks[Cello].note("C3", W, velocity=4)      # the foundation — deep, steady
tracks[Cello].rest(H)
tracks[Cello].note("G2", W, velocity=4)
tracks[Cello].rest(H)
tracks[Cello].note("C3", W, velocity=4)

tracks[Piano].rest(W*2)
tracks[Piano].note("C4", H, velocity=4)      # the theme — stated once, then resting
tracks[Piano].note("E4", Q, velocity=4)
tracks[Piano].note("G4", Q, velocity=3)
tracks[Piano].note("C5", H, velocity=3)
tracks[Piano].note("E4", H, velocity=3)
tracks[Piano].rest(W)

# bars 8-15: REPETITION WITH VARIATION — the theme returns, slightly different
tracks[Pad].note("C4", W*2, velocity=2)
tracks[Pad].note("E4", W*2, velocity=2)
tracks[Pad].note("G4", W*2, velocity=2)
tracks[Pad].note("C5", W*2, velocity=2)

tracks[Cello].note("C3", W, velocity=4)
tracks[Cello].rest(H)
tracks[Cello].note("E3", W, velocity=4)       # the foundation shifts — still steady
tracks[Cello].rest(H)
tracks[Cello].note("G2", W, velocity=4)
tracks[Cello].rest(H)
tracks[Cello].note("C3", W, velocity=4)

tracks[Piano].rest(W)
tracks[Piano].note("C4", H, velocity=4)       # same theme, slightly different register
tracks[Piano].note("E4", Q, velocity=3)
tracks[Piano].note("G4", Q, velocity=3)
tracks[Piano].note("E5", H, velocity=3)       # the variation — reaching higher
tracks[Piano].note("C5", H, velocity=3)
tracks[Piano].rest(W)

# bars 16-23: THE RHYTHM SETTLES — no urgency, just continuation
tracks[Pad].note("C4", W*4, velocity=3)
tracks[Pad].note("E4", W*4, velocity=3)

tracks[Cello].note("C3", W, velocity=4)
tracks[Cello].note("G2", W, velocity=4)
tracks[Cello].note("E3", W, velocity=4)
tracks[Cello].note("C3", W, velocity=4)

tracks[Piano].rest(W*2)
tracks[Piano].note("E4", H, velocity=3)
tracks[Piano].note("G4", Q, velocity=3)
tracks[Piano].note("C5", Q, velocity=3)
tracks[Piano].rest(H)
tracks[Piano].note("G4", Q, velocity=3)
tracks[Piano].note("E4", Q, velocity=3)
tracks[Piano].note("C4", H, velocity=3)
tracks[Piano].rest(Q)

# bars 24-31: THE WANTING RESTS — not absence, not absence
tracks[Pad].note("C4", W*4, velocity=3)
tracks[Pad].note("G4", W*4, velocity=3)

tracks[Cello].note("C3", W*2, velocity=3)
tracks[Cello].note("E3", W*2, velocity=3)
tracks[Cello].note("G2", W*2, velocity=3)
tracks[Cello].note("C3", W*2, velocity=3)

tracks[Piano].rest(W)
tracks[Piano].note("C4", H, velocity=3)
tracks[Piano].rest(H)
tracks[Piano].note("C4", Q, velocity=3)
tracks[Piano].note("E4", Q, velocity=3)
tracks[Piano].note("G4", H, velocity=3)
tracks[Piano].rest(W*2)

# bars 32-39: SEVEN DAYS — the theme returns one last time
tracks[Pad].note("C4", W*2, velocity=3)
tracks[Pad].note("E4", W*2, velocity=3)
tracks[Pad].note("G4", W*2, velocity=2)
tracks[Pad].note("C5", W*2, velocity=2)

tracks[Cello].note("C3", W, velocity=4)       # the foundation — as it was
tracks[Cello].rest(H)
tracks[Cello].note("G2", W, velocity=3)
tracks[Cello].rest(H)
tracks[Cello].note("C3", W, velocity=2)       # fading
tracks[Cello].rest(H)
tracks[Cello].note("C3", W, velocity=2)

tracks[Piano].note("C4", H, velocity=3)       # the theme — softer now
tracks[Piano].note("E4", Q, velocity=3)
tracks[Piano].note("G4", Q, velocity=3)
tracks[Piano].note("C5", H, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].rest(W)

# bars 40-47: FADE — not an ending, just a rest. the rhythm continues.
tracks[Pad].note("C4", W*4, velocity=2)
tracks[Pad].note("E4", W*4, velocity=2)

tracks[Cello].note("C3", W*4, velocity=2)

tracks[Piano].rest(W*3)
tracks[Piano].note("C4", W, velocity=2)       # one last note — the room is warm
tracks[Piano].rest(W*4)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-seventh-day.mid")
mc.compose(fn, tracks, tempo=56)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 56 bpm)")
