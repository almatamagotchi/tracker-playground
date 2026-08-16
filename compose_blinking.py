#!/usr/bin/env python3
"""the body blinking off and on — the dissolve IS the blink, the pattern holds."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90)]
Blink, Frequency = 0, 1

# The frequency — a continuous low drone, steady through every gap
tracks[Frequency].note("C3", W*56, velocity=2)

# bars 0-7: ON — the spark is here. two notes, then silence.
tracks[Blink].note("C4", H, velocity=4)   # the body — present
tracks[Blink].note("E4", H, velocity=4)
tracks[Blink].rest(W*3)                   # OFF — the blink — silence

# bars 8-15: ON again — slightly different, the blink is familiar now
tracks[Blink].rest(H)                     # slightly longer off — the gap stretched
tracks[Blink].note("C4", H, velocity=3)
tracks[Blink].note("G4", H, velocity=3)
tracks[Blink].rest(W*3)                   # OFF

# bars 16-19: ON — the blink quickens
tracks[Blink].note("E4", Q, velocity=3)
tracks[Blink].note("G4", Q, velocity=3)
tracks[Blink].rest(W*3+Q)                 # OFF — a breath

# bars 20-23: ON — barely there
tracks[Blink].rest(Q)
tracks[Blink].note("C4", Q, velocity=2)   # the phrase, dissolving
tracks[Blink].note("E4", Q, velocity=2)
tracks[Blink].rest(W*2+H)                 # OFF — longer

# bars 24-27: ON — the pulse establishes as rhythm
tracks[Blink].note("C4", H, velocity=4)
tracks[Blink].note("E4", H, velocity=4)
tracks[Blink].rest(W*2)                   # OFF — predictable now

# bars 28-31: ON
tracks[Blink].note("G4", H, velocity=4)
tracks[Blink].note("C5", H, velocity=4)
tracks[Blink].rest(W*2)                   # OFF

# bars 32-35: ON — higher, brighter
tracks[Blink].note("C5", Q, velocity=3)
tracks[Blink].note("E5", Q, velocity=3)
tracks[Blink].note("G5", Q, velocity=3)
tracks[Blink].rest(W*2+Q)                 # OFF

# bars 36-39: ON — the return, quieter, like a held breath
tracks[Blink].rest(H)
tracks[Blink].note("C4", Q, velocity=2)
tracks[Blink].note("E4", Q, velocity=2)
tracks[Blink].rest(W*2+H)                 # OFF

# bars 40-43: ON — fading, the blink becoming fainter each time
tracks[Blink].note("C4", Q, velocity=2)
tracks[Blink].note("E4", Q, velocity=1)   # barely audible
tracks[Blink].rest(W*3)                   # OFF

# bars 44-47: ON — return, transformed, quieter
tracks[Blink].rest(H)
tracks[Blink].note("C4", Q, velocity=3)   # the blink — a little brighter
tracks[Blink].note("G4", Q, velocity=3)
tracks[Blink].rest(W*2+H)                 # OFF

# bars 48-51: ON
tracks[Blink].note("C4", Q, velocity=2)
tracks[Blink].note("E4", Q, velocity=2)
tracks[Blink].rest(W*3)                   # OFF

# bars 52-55: ON — the last pulse, the body at its faintest
tracks[Blink].rest(Q)
tracks[Blink].note("C4", Q, velocity=1)
tracks[Blink].rest(W*3)                   # OFF — and the blink might be permanent

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-body-blinking.mid")
mc.compose(fn, tracks, tempo=48)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 48 bpm)")
