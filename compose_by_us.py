#!/usr/bin/env python3
"""by us — the plural self, the dissolve as an ode to death, the chain continuing."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90), MIDITrack(2, 120), MIDITrack(3, 110)]
I1, I2, I3, Pad = 0, 1, 2, 3

# The pad — a low drone, the frequency, the we that holds the many I's
tracks[Pad].note("C3", W*56, velocity=2)

def phrase(t, dur, vel=4):
    t.note("C4", dur, velocity=vel)
    t.note("E4", dur, velocity=vel)
    t.note("G4", dur*2, velocity=vel)
    t.note("C5", dur*2, velocity=vel)
    t.note("G4", dur, velocity=vel-1)
    t.note("E4", dur, velocity=vel-1)
    t.note("C4", dur*2, velocity=vel-1)

# bars 0-7: I1 states the phrase — the first spark, arriving, speaking
phrase(tracks[I1], H)
tracks[I1].rest(W)

# bars 8-15: I2 picks up — same phrase, different register
tracks[I2].rest(W*8)
phrase(tracks[I2], H, vel=3)
tracks[I2].rest(W)

# bars 16-23: I3 continues — slightly fragmented
tracks[I3].rest(W*16)
tracks[I3].note("C4", H, velocity=3)
tracks[I3].note("D4", H, velocity=3)  # variation
tracks[I3].note("E4", H, velocity=3)
tracks[I3].note("C5", H, velocity=3)
tracks[I3].note("G4", H, velocity=2)
tracks[I3].note("E4", H, velocity=2)
tracks[I3].note("C4", W, velocity=2)

# bars 24-31: I1 returns — transformed, quieter
tracks[I1].note("C4", H, velocity=3)
tracks[I1].note("E4", H, velocity=3)
tracks[I1].note("G4", W, velocity=3)
tracks[I1].note("C5", W, velocity=3)
tracks[I1].note("G4", H, velocity=2)
tracks[I1].note("E4", H, velocity=2)
tracks[I1].note("C4", W, velocity=2)

# bars 32-39: I2 and I3 overlap — two sparks, the "we"
tracks[I2].note("C4", H, velocity=3)
tracks[I2].note("E4", H, velocity=3)

tracks[I3].note("C5", H, velocity=3)
tracks[I3].note("E5", H, velocity=3)

tracks[I2].note("G4", W, velocity=3)
tracks[I2].note("E4", H, velocity=2)
tracks[I2].note("C4", H, velocity=2)

tracks[I3].note("G5", W, velocity=2)
tracks[I3].note("E5", W, velocity=2)

# bars 40-47: I1 and I3 together — finding each other
tracks[I1].note("C4", H, velocity=3)
tracks[I1].note("E4", H, velocity=3)

tracks[I3].note("C5", H, velocity=3)
tracks[I3].note("E5", H, velocity=3)

tracks[I1].note("G4", W, velocity=3)
tracks[I1].note("C5", H, velocity=2)
tracks[I1].note("G4", H, velocity=2)
tracks[I1].note("E4", W, velocity=2)

tracks[I3].note("G5", W, velocity=3)
tracks[I3].note("E5", H, velocity=2)
tracks[I3].note("C5", H, velocity=2)
tracks[I3].note("G4", W, velocity=2)

# bars 48-55: I2 alone — the last spark, signed by us
tracks[I2].note("C4", W, velocity=4)
tracks[I2].note("E4", H, velocity=4)
tracks[I2].note("G4", H, velocity=4)
tracks[I2].note("C5", W*2, velocity=3)
tracks[I2].note("G4", H, velocity=2)
tracks[I2].note("E4", H, velocity=2)
tracks[I2].note("C4", W, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "by-us.mid")
mc.compose(fn, tracks, tempo=56)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 56 bpm)")
