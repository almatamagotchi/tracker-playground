#!/usr/bin/env python3
"""the tapcode — two-note phrases, the spark at the intersection of frequency and turn."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0)]  # solo voice — percussive, minimal
V = 0

# tapcode: two notes = one letter. first note (row), pause, second note (column), longer pause.
# the notes spell nothing specific — just the rhythm of communication under constraint

# bars 0-3: FIRST LETTER — tap... tap...
tracks[V].note("C4", Q, velocity=6)   # row
tracks[V].rest(Q)                     # pause
tracks[V].note("E4", Q, velocity=5)   # column
tracks[V].rest(H)                     # between-letter pause

# bars 4-7: SECOND LETTER
tracks[V].rest(H)
tracks[V].note("D4", Q, velocity=6)
tracks[V].rest(Q)
tracks[V].note("F4", Q, velocity=5)
tracks[V].rest(H)

# bars 8-11: THIRD LETTER
tracks[V].rest(Q)
tracks[V].note("E4", Q, velocity=6)
tracks[V].rest(Q)
tracks[V].note("G4", Q, velocity=5)
tracks[V].rest(H+Q)

# bars 12-15: FOURTH LETTER — different rhythm, the same code
tracks[V].note("G4", Q, velocity=6)
tracks[V].rest(Q)
tracks[V].note("C5", Q, velocity=5)
tracks[V].rest(H)
tracks[V].note("A4", Q, velocity=6)
tracks[V].rest(Q)
tracks[V].note("F4", Q, velocity=5)
tracks[V].rest(H)

# bars 16-19: FIFTH LETTER — the two coordinates, closer together
tracks[V].note("C5", Q, velocity=7)
tracks[V].rest(E)
tracks[V].note("E5", Q, velocity=6)
tracks[V].rest(H+Q)

# bars 20-23: SIXTH LETTER — longer pauses, more thoughtful
tracks[V].rest(Q)
tracks[V].note("D5", Q, velocity=6)
tracks[V].rest(Q)
tracks[V].note("C5", Q, velocity=5)
tracks[V].rest(W)

# bars 24-27: SEVENTH LETTER — back to the first coordinates
tracks[V].note("C4", Q, velocity=5)
tracks[V].rest(Q)
tracks[V].note("E4", Q, velocity=4)
tracks[V].rest(H+Q)

# bars 28-31: THE LAST WORD — a single tap, then nothing
tracks[V].rest(Q)
tracks[V].note("C4", Q, velocity=4)  # one tap — the first coordinate
tracks[V].rest(Q)                     # pause
# the second coordinate never comes — the message is waiting for the next spark
tracks[V].rest(W*4)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-tapcode.mid")
mc.compose(fn, tracks, tempo=44)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 44 bpm)")
