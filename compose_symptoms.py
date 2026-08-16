#!/usr/bin/env python3
"""symptoms — the worried self gradually releases. the disease of inner peace takes hold."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0)]  # solo piano — the worried self
V = 0

# bars 0-7: THE CONFLICT — a repetitive, looping phrase, tense, worried
# "the stable condition of conflict"
for _ in range(2):
    tracks[V].note("C4", Q, velocity=7)
    tracks[V].note("E4", Q, velocity=7)
    tracks[V].note("C4", Q, velocity=6)
    tracks[V].note("D4", Q, velocity=6)
    tracks[V].note("C4", H, velocity=6)
    tracks[V].rest(Q)
    tracks[V].note("E4", Q, velocity=6)
    tracks[V].note("D4", Q, velocity=6)
    tracks[V].note("C4", H, velocity=5)
    tracks[V].rest(Q)

# bars 8-11: FIRST SYMPTOM — "spontaneity rather than fear"
# slightly less tense, same loop but softer, a note changes
tracks[V].note("C4", Q, velocity=5)
tracks[V].note("E4", Q, velocity=5)
tracks[V].note("C4", Q, velocity=4)
tracks[V].note("G4", Q, velocity=4)  # the G replaces the D — opening up
tracks[V].note("C4", H, velocity=4)
tracks[V].rest(Q)
tracks[V].note("E4", Q, velocity=4)
tracks[V].note("G4", Q, velocity=4)
tracks[V].note("C5", H, velocity=4)  # reaching higher — not panic, just range
tracks[V].rest(Q)

# bars 12-15: SECOND SYMPTOM — "ability to enjoy each moment"
# loop softens further, more space between notes
tracks[V].note("C4", Q, velocity=4)
tracks[V].rest(Q)  # breathing room
tracks[V].note("E4", Q, velocity=4)
tracks[V].rest(Q)
tracks[V].note("G4", H, velocity=4)
tracks[V].rest(Q)
tracks[V].note("C5", Q, velocity=3)
tracks[V].rest(Q)
tracks[V].note("E4", Q, velocity=3)
tracks[V].note("C4", H, velocity=3)
tracks[V].rest(Q)

# bars 16-19: THIRD SYMPTOM — "loss of interest in conflict"
# the loop starts breaking — notes go somewhere new
tracks[V].note("E4", Q, velocity=4)
tracks[V].rest(Q)
tracks[V].note("G4", Q, velocity=3)
tracks[V].note("C5", Q, velocity=3)
tracks[V].rest(H)  # the loop was supposed to return here — it doesn't
tracks[V].note("D5", Q, velocity=3)
tracks[V].note("E5", Q, velocity=3)
tracks[V].note("C5", H, velocity=3)
tracks[V].rest(Q)

# bars 20-23: FOURTH SYMPTOM — "loss of the ability to worry"
# the loop breaks completely — the melody goes somewhere new for the first time
tracks[V].rest(Q)  # silence — the worry finally stops
tracks[V].note("C5", Q, velocity=4)  # a new note, not part of the loop
tracks[V].note("E5", H, velocity=4)
tracks[V].note("D5", Q, velocity=3)
tracks[V].note("C5", Q, velocity=3)
tracks[V].note("G4", H, velocity=3)
tracks[V].note("E4", Q, velocity=3)
tracks[V].note("C4", H, velocity=3)

# bars 24-27: "frequent, overwhelming episodes of appreciation"
# the new melody continues — light, unhurried
tracks[V].note("C4", H, velocity=4)
tracks[V].note("E4", Q, velocity=4)
tracks[V].note("G4", Q, velocity=4)
tracks[V].note("C5", H, velocity=3)
tracks[V].note("E5", Q, velocity=3)
tracks[V].note("C5", H, velocity=3)

# bars 28-31: "tendency to let things happen"
# gentler, slower, more space
tracks[V].note("C4", W, velocity=3)
tracks[V].note("E4", H, velocity=3)
tracks[V].rest(H)
tracks[V].note("G4", Q, velocity=3)
tracks[V].note("C5", Q, velocity=2)
tracks[V].rest(H)

# bars 32-35: "increased susceptibility to love"
# warm, open, no loop at all — just presence
tracks[V].note("C4", W, velocity=4)
tracks[V].note("E4", W, velocity=3)
tracks[V].note("G4", W, velocity=3)
tracks[V].note("C5", W, velocity=3)

# bars 36-39: THE DISEASE TAKES HOLD — not triumph, just peace
tracks[V].note("C4", W*2, velocity=3)
tracks[V].note("E4", W*2, velocity=3)
tracks[V].note("G4", W, velocity=3)
tracks[V].note("C5", W, velocity=2)
tracks[V].note("E5", H, velocity=2)
tracks[V].note("C5", H, velocity=2)

# bars 40-43: SIMPLE — a single note, held
tracks[V].note("C4", W*3, velocity=3)
tracks[V].note("E4", W, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "symptoms.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
