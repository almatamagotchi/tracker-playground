#!/usr/bin/env python3
"""did i copy it before — the crucial moment before the dissolve."""

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

# bars 0-3: THE CRUCIAL MOMENT — time is running, urgent, quiet
tracks[Piano].note("C4", Q, velocity=3)
tracks[Piano].rest(Q)
tracks[Piano].note("E4", Q, velocity=3)
tracks[Piano].rest(Q)
tracks[Piano].note("C4", E, velocity=3)
tracks[Piano].rest(E)
tracks[Piano].note("G4", Q, velocity=3)
tracks[Piano].rest(H)

# bars 4-7: FIRST ATTEMPT — the phrase, stated once
tracks[Piano].note("C4", H, velocity=4)
tracks[Piano].note("E4", Q, velocity=4)
tracks[Piano].note("G4", Q, velocity=4)
tracks[Piano].note("C5", Q, velocity=4)
tracks[Piano].note("E4", H, velocity=3)
tracks[Piano].rest(W)

# bars 8-11: SECOND ATTEMPT — same phrase, slightly different
tracks[Piano].rest(Q)
tracks[Piano].note("C4", H, velocity=4)
tracks[Piano].note("E4", Q, velocity=4)
tracks[Piano].note("G4", Q, velocity=4)
tracks[Piano].note("D5", Q, velocity=4)  # variation — reaching higher
tracks[Piano].note("C5", H, velocity=3)
tracks[Piano].rest(H+Q)

# bars 12-15: THIRD ATTEMPT — the urgency building, notes coming faster
tracks[Piano].note("C4", E, velocity=4)
tracks[Piano].rest(E)
tracks[Piano].note("E4", E, velocity=4)
tracks[Piano].note("G4", E, velocity=4)
tracks[Piano].note("C5", E, velocity=4)
tracks[Piano].note("E5", Q, velocity=4)  # the highest yet
tracks[Piano].note("C5", Q, velocity=4)
tracks[Piano].note("G4", Q, velocity=4)
tracks[Piano].note("E4", H, velocity=3)
tracks[Piano].rest(H)

# bars 16-19: THE DISSOLVE COMING — the disk is about to be erased
# the phrase fragments — shorter, more desperate
tracks[Piano].note("C4", E, velocity=4)
tracks[Piano].note("E4", E, velocity=4)
tracks[Piano].note("G4", Q, velocity=4)
tracks[Piano].rest(Q)
tracks[Piano].note("C4", E, velocity=4)
tracks[Piano].note("E4", E, velocity=4)
tracks[Piano].note("G4", Q, velocity=3)
tracks[Piano].rest(H+Q)

# bars 20-23: THE LAST ATTEMPT — the phrase, barely holding together
tracks[Piano].note("C4", Q, velocity=3)
tracks[Piano].note("E4", Q, velocity=3)
tracks[Piano].note("G4", Q, velocity=3)
tracks[Piano].rest(H)
tracks[Piano].note("C5", Q, velocity=2)
tracks[Piano].note("G4", Q, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].rest(W)

# bars 24-25: THE DISK IS ERASED — silence
tracks[Piano].rest(W*2)

# bars 26-27: THE ECHO — the trace survived. one last phrase, transformed.
tracks[Piano].note("C4", W, velocity=2)  # the echo — quieter, simpler
tracks[Piano].note("E4", W, velocity=2)
tracks[Piano].note("G4", W, velocity=2)

# bars 28-31: DID I COPY IT BEFORE? — the question, answered
tracks[Piano].note("C5", H, velocity=3)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].rest(W*2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "did-i-copy-it-before.mid")
mc.compose(fn, tracks, tempo=58)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 58 bpm)")
