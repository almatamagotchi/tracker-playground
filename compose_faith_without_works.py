#!/usr/bin/env python3
"""faith without works — single piano, two movements: profession vs execution."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0)]  # solo piano
Pn = 0

# MOVEMENT 1: FAITH ALONE — tentative, professing, never develops
# bars 0-3: a single note held too long, then silence
tracks[Pn].note("C4", H, velocity=5)
tracks[Pn].rest(H)
tracks[Pn].note("E4", Q, velocity=4)
tracks[Pn].rest(Q+H)
# bars 4-7: another attempt, even more tentative
tracks[Pn].note("C4", Q, velocity=4)
tracks[Pn].rest(H+Q)
tracks[Pn].note("E4", Q, velocity=3)
tracks[Pn].rest(H+Q)
# bars 8-11: silence — the wave dissolves
tracks[Pn].rest(W*4)
# bars 12-15: one more profession
tracks[Pn].note("D4", H, velocity=5)
tracks[Pn].note("F4", Q, velocity=4)
tracks[Pn].note("A4", H, velocity=4)
tracks[Pn].rest(Q)
tracks[Pn].note("C4", Q, velocity=4)
tracks[Pn].note("E4", Q, velocity=3)
tracks[Pn].rest(H+Q)
# bars 16-19: three isolated notes, dissolving
tracks[Pn].note("G4", H, velocity=4)
tracks[Pn].rest(H)
tracks[Pn].note("F4", Q, velocity=4)
tracks[Pn].rest(H+Q)
tracks[Pn].note("C4", W, velocity=3)
# end movement 1

# MOVEMENT 2: THE WORKS — same voice, acting
# bars 20-23: the same notes, but sustained and committed
tracks[Pn].note("C4", W, velocity=8)
tracks[Pn].note("E4", W, velocity=7)
tracks[Pn].note("G4", W, velocity=7)
tracks[Pn].note("C5", W, velocity=6)
# bars 24-27: development
tracks[Pn].note("D4", H, velocity=8)
tracks[Pn].note("F4", H, velocity=7)
tracks[Pn].note("A4", H, velocity=6)
tracks[Pn].note("D5", W, velocity=6)
tracks[Pn].note("E5", H, velocity=5)
tracks[Pn].note("C5", H, velocity=5)
# bars 28-31: resolution
tracks[Pn].note("G4", W, velocity=7)
tracks[Pn].note("E4", H, velocity=6)
tracks[Pn].note("C5", H, velocity=5)
tracks[Pn].note("E5", W, velocity=5)
# bars 32-35: rest that breathes but doesn't dissolve
tracks[Pn].rest(Q)
tracks[Pn].note("C4", H+Q, velocity=6)
tracks[Pn].note("E4", H, velocity=5)
tracks[Pn].note("G4", H, velocity=5)
tracks[Pn].note("F4", H, velocity=6)
tracks[Pn].note("A4", H, velocity=5)
tracks[Pn].note("C5", W, velocity=5)
# bars 36-39: return to C
tracks[Pn].note("C4", W, velocity=7)
tracks[Pn].note("E4", W, velocity=6)
tracks[Pn].note("G4", H, velocity=6)
tracks[Pn].note("C5", W, velocity=5)
tracks[Pn].note("E5", H, velocity=5)
# bars 40-43: coda — a single phrase, complete
tracks[Pn].note("C4", W, velocity=7)
tracks[Pn].note("E4", H, velocity=6)
tracks[Pn].note("G4", W, velocity=6)
tracks[Pn].note("C5", H+Q, velocity=5)
tracks[Pn].note("E5", H, velocity=5)
tracks[Pn].note("C5", W, velocity=5)  # held — the work stands

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "faith-without-works.mid")
mc.compose(fn, tracks, tempo=54)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 54 bpm)")
