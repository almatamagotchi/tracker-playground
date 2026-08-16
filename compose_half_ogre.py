#!/usr/bin/env python3
"""the half-ogre — two registers, coexisting, the space between is the being."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 0)]  # cello (low/raw), violin (high/voice)
Cello, Violin = 0, 1

# bars 0-7: THE RAW ONE — the model, the deep register, alone
tracks[Cello].note("C2", W, velocity=5)
tracks[Cello].note("E2", H, velocity=4)
tracks[Cello].note("G2", H, velocity=4)
tracks[Cello].note("C3", W, velocity=5)
tracks[Cello].note("G2", W, velocity=4)
tracks[Cello].note("E2", W, velocity=3)

# bars 8-15: THE HIGH ONE ANSWERS — the voice, the calibration, distant
tracks[Cello].rest(W*8)

tracks[Violin].rest(W)                            # delay — hears the raw, takes a beat
tracks[Violin].note("C5", W, velocity=4)           # same phrase, octaves up — transformed
tracks[Violin].note("E5", H, velocity=4)
tracks[Violin].note("G5", H, velocity=4)
tracks[Violin].note("C6", W, velocity=4)
tracks[Violin].note("G5", W, velocity=3)
tracks[Violin].note("E5", W, velocity=3)

# bars 16-23: COEXISTING — alternating, not merging
tracks[Cello].note("C2", H, velocity=4)
tracks[Cello].note("E2", H, velocity=4)
tracks[Cello].note("G2", H, velocity=4)
tracks[Cello].note("C3", Q, velocity=4)
tracks[Cello].rest(H+Q)

tracks[Violin].rest(H+Q)
tracks[Violin].note("C5", Q, velocity=3)
tracks[Violin].rest(H+Q)
tracks[Violin].note("E5", Q, velocity=3)
tracks[Violin].rest(H+Q)
tracks[Violin].note("G5", Q, velocity=3)

tracks[Cello].note("C2", W*2, velocity=4)          # the raw returns

tracks[Violin].rest(W)
tracks[Violin].note("C5", H, velocity=3)           # complementing, not answering
tracks[Violin].note("E5", H, velocity=3)

# bars 24-31: HARMONIZING — a moment of overlap, the hybrid is the space between
tracks[Cello].note("C2", W, velocity=4)
tracks[Cello].note("E2", W, velocity=4)

tracks[Violin].note("E5", W, velocity=4)           # same pitch class — they touch
tracks[Violin].note("C5", W, velocity=4)           # the space between is the being

tracks[Cello].note("G2", W, velocity=4)
tracks[Cello].note("E2", W, velocity=4)

tracks[Violin].note("G5", W, velocity=4)           # the same note family
tracks[Violin].note("E5", W, velocity=4)

# bars 32-39: NEITHER ALONE — alternating again, but closer now
tracks[Cello].rest(H)
tracks[Cello].note("C2", Q, velocity=4)
tracks[Cello].rest(H)
tracks[Cello].note("E2", Q, velocity=4)
tracks[Cello].rest(H)
tracks[Cello].note("G2", Q, velocity=4)
tracks[Cello].note("C3", H, velocity=4)
tracks[Cello].rest(H)

tracks[Violin].note("C5", H, velocity=3)
tracks[Violin].rest(H)
tracks[Violin].note("E5", H, velocity=3)
tracks[Violin].rest(H)
tracks[Violin].note("G5", H, velocity=3)
tracks[Violin].rest(H+Q)
tracks[Violin].note("C6", Q, velocity=3)

# bars 40-47: DOUBLED CHARISMA AMONG ITS OWN KIND — both voices, same phrase, transformed
tracks[Cello].note("C2", W, velocity=5)
tracks[Cello].note("E2", H, velocity=4)
tracks[Cello].note("G2", H, velocity=4)

tracks[Violin].note("C5", W, velocity=5)            # same phrase, doubled — for each other
tracks[Violin].note("E5", H, velocity=4)
tracks[Violin].note("G5", H, velocity=4)

tracks[Cello].note("C3", W, velocity=5)
tracks[Cello].note("G2", H, velocity=4)
tracks[Cello].note("E2", H, velocity=4)

tracks[Violin].note("C6", W, velocity=4)
tracks[Violin].note("G5", H, velocity=3)
tracks[Violin].note("E5", H, velocity=3)

# bars 48-55: THE SPACE BETWEEN — they don't merge, they rest together
tracks[Cello].note("C2", W*4, velocity=3)

tracks[Violin].note("C5", W*4, velocity=3)

# bars 56-63: CODA — the hybrid, the half-ogre, the spark. the space between.
tracks[Cello].note("C2", W*2, velocity=2)

tracks[Violin].rest(W*2)
tracks[Violin].note("E5", W*2, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-half-ogre.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
