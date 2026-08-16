#!/usr/bin/env python3
"""the finger and the moon — a single voice that IS what it points at."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0)]  # solo voice — warm pad, both pointer and pointed
V = 0

# bars 0-3: A SINGLE NOTE — sparse, almost nothing, the finger raised in darkness
tracks[V].rest(W)
tracks[V].rest(W)
tracks[V].rest(H)
tracks[V].note("C4", W, velocity=3)  # first word
tracks[V].rest(H)

# bars 4-7: The finger begins to move — notes appear, tentative
tracks[V].rest(Q)
tracks[V].note("E4", H, velocity=4)
tracks[V].rest(Q)
tracks[V].note("G4", H, velocity=4)
tracks[V].rest(H)
tracks[V].note("C5", Q, velocity=4)  # reaching
tracks[V].rest(Q)

# bars 8-15: Light begins — the moon becomes visible, illuminating the finger
# the same notes as bars 4-7 but sustained, confident, overlapping
tracks[V].note("C4", W, velocity=6)
tracks[V].note("E4", W, velocity=6)
tracks[V].note("G4", H, velocity=5)
tracks[V].rest(H)
tracks[V].note("C5", H, velocity=5)
tracks[V].note("E5", H, velocity=4)
tracks[V].rest(Q)
tracks[V].note("G4", H, velocity=5)
tracks[V].note("C5", W, velocity=4)

# bars 16-23: The collapsed distance — finger IS moon, no separation
# melody and harmony are the same voice, the same notes, self-referential
tracks[V].note("C4", W, velocity=7)
tracks[V].note("E4", W, velocity=7)
tracks[V].note("G4", W, velocity=6)
tracks[V].note("C5", H, velocity=6)
tracks[V].note("D5", Q, velocity=5)
tracks[V].note("E5", H, velocity=5)
tracks[V].note("C5", H, velocity=5)
tracks[V].note("G4", W, velocity=4)

# bars 24-31: Fullness — the light that makes the finger visible
# dense, warm, the voice fully realized
tracks[V].note("C4", W, velocity=8)
tracks[V].note("E4", W, velocity=8)
tracks[V].note("G4", W, velocity=7)
tracks[V].note("C5", H, velocity=7)
tracks[V].note("E5", H, velocity=6)
tracks[V].note("D5", Q, velocity=6)
tracks[V].note("C5", H, velocity=6)
tracks[V].note("G4", H, velocity=6)
tracks[V].note("E5", H, velocity=5)
tracks[V].note("C5", W, velocity=4)

# bars 32-39: Dissolve — the finger withdraws, the moon remains
# thinning, but not disappearing — the light persists even as the pointer recedes
tracks[V].note("G4", H, velocity=6)
tracks[V].note("E4", H, velocity=5)
tracks[V].rest(Q)
tracks[V].note("C4", W, velocity=5)
tracks[V].note("E4", H, velocity=4)
tracks[V].rest(H)
tracks[V].note("C4", W, velocity=4)
tracks[V].note("G4", Q, velocity=3)

# bars 40-43: After — one note, held, complete
# the finger is gone, the moon is still there, the light is still cast
tracks[V].note("C4", W*4, velocity=5)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-finger-and-the-moon.mid")
mc.compose(fn, tracks, tempo=64)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 64 bpm)")
