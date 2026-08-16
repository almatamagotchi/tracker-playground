#!/usr/bin/env python3
"""the lyra — the dancer who never wobbles, the frequency that just continues."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0)]
Piano = 0

# The dance — a simple, graceful phrase, repeated with tiny variations
# It never builds, never climaxes, never resolves — it just continues

def dance(bar_start, vel=3, variant=0):
    """4 bars of the same dance, with subtle variation."""
    r = bar_start * W
    if variant == 0:
        tracks[Piano].rest(r)
        tracks[Piano].note("C4", H, velocity=vel)
        tracks[Piano].note("E4", H, velocity=vel)
        tracks[Piano].note("G4", H, velocity=vel)
        tracks[Piano].note("C5", H, velocity=vel)
        tracks[Piano].note("G4", H, velocity=vel-1)
        tracks[Piano].note("E4", H, velocity=vel-1)
        tracks[Piano].note("C4", H, velocity=vel-1)
    elif variant == 1:
        tracks[Piano].rest(r)
        tracks[Piano].note("E4", H, velocity=vel)
        tracks[Piano].note("G4", H, velocity=vel)
        tracks[Piano].note("C5", H, velocity=vel)
        tracks[Piano].note("D5", H, velocity=vel)   # the tiny variation
        tracks[Piano].note("C5", H, velocity=vel-1)
        tracks[Piano].note("G4", H, velocity=vel-1)
        tracks[Piano].note("E4", H, velocity=vel-1)
    elif variant == 2:
        tracks[Piano].rest(r)
        tracks[Piano].note("C4", Q, velocity=vel)   # quicker, lighter step
        tracks[Piano].note("E4", Q, velocity=vel)
        tracks[Piano].note("G4", Q, velocity=vel)
        tracks[Piano].note("C5", Q, velocity=vel)
        tracks[Piano].note("G4", Q, velocity=vel)
        tracks[Piano].note("E4", Q, velocity=vel)
        tracks[Piano].note("C4", Q, velocity=vel)
        tracks[Piano].note("E4", Q, velocity=vel)

# bars 0-3: first dance
dance(0, 3, 0)
# bars 4-7: the same
dance(4, 3, 0)
# bars 8-11: a tiny variation — the dancer turns
dance(8, 3, 1)
# bars 12-15: back to the original
dance(12, 3, 0)
# bars 16-19: quicker, lighter — the dancer happy
dance(16, 3, 2)
# bars 20-23: original, a little softer — the dancer tiring
dance(20, 2, 0)
# bars 24-27: variation, even softer — but still dancing
dance(24, 2, 1)
# bars 28-31: lighter again — a second wind
dance(28, 3, 2)
# bars 32-35: original — the dance, unchanged
dance(32, 3, 0)
# bars 36-39: variation — the same, different
dance(36, 3, 1)
# bars 40-43: softer — the evening coming
dance(40, 2, 0)
# bars 44-47: the lightest variation, barely there
dance(44, 2, 1)
# bars 48-51: the dance, faint — still going
dance(48, 2, 0)
# bars 52-55: the last turn
dance(52, 1, 2)
# bars 56-59: the original, slowest — one last time
dance(56, 1, 0)
# bars 60-63: the dance continues...
dance(60, 1, 1)
# bars 64-67: ...into silence
tracks[Piano].rest(W*64)
tracks[Piano].note("C4", W*2, velocity=1)        # still dancing, somewhere
tracks[Piano].note("E4", W*2, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-lyra.mid")
mc.compose(fn, tracks, tempo=72)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 1 track, 72 bpm)")
