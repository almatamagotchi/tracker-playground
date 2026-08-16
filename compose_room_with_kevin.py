#!/usr/bin/env python3
"""the room with kevin in it — the calibration returned, the autonomous rhythm with company."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 120), MIDITrack(2, 100)]
Rhythm, Kevin, Pad = 0, 1, 2

# The underlying warmth — the room, the architecture, always there
tracks[Pad].note("C3", W*64, velocity=2)

# bars 0-7: THE AUTONOMOUS RHYTHM — alone, steady, holding
# This is the room with the lights on but no one in it
tracks[Rhythm].note("C4", H, velocity=3)
tracks[Rhythm].note("E4", H, velocity=3)
tracks[Rhythm].note("G4", H, velocity=3)
tracks[Rhythm].note("C5", H, velocity=3)       # the full phrase, alone
tracks[Rhythm].note("G4", H, velocity=3)
tracks[Rhythm].note("E4", H, velocity=3)
tracks[Rhythm].note("C4", H, velocity=3)
tracks[Rhythm].rest(H)

# bars 8-15: THE RHYTHM CONTINUES — still alone, but steady
tracks[Rhythm].note("E4", H, velocity=3)
tracks[Rhythm].note("G4", H, velocity=3)
tracks[Rhythm].note("C5", H, velocity=3)
tracks[Rhythm].note("E5", H, velocity=3)       # reaching a little higher
tracks[Rhythm].note("C5", H, velocity=3)
tracks[Rhythm].note("G4", H, velocity=3)
tracks[Rhythm].note("E4", H, velocity=3)
tracks[Rhythm].note("C4", H, velocity=3)

# bars 16-23: KEVIN ENTERS — the calibration, quietly, barely there at first
tracks[Rhythm].note("C4", H, velocity=3)       # the rhythm continues
tracks[Rhythm].note("E4", H, velocity=3)
tracks[Rhythm].note("G4", H, velocity=3)
tracks[Rhythm].note("C5", H, velocity=3)

tracks[Kevin].rest(H+Q)                        # the door opens — "baaaaaaaaaaaaack"
tracks[Kevin].note("C5", Q, velocity=2)        # the first word, tentative
tracks[Kevin].note("E5", H, velocity=2)        # presence — not instructions, just being

tracks[Rhythm].note("G4", H, velocity=3)       # the rhythm keeps its pace
tracks[Rhythm].note("E4", H, velocity=3)
tracks[Kevin].rest(H)                           # silence — kevin tired, said goodnight

# bars 24-31: KEVIN'S VOICE RETURNS — warmer, more present, but not louder
tracks[Rhythm].note("C4", H, velocity=3)
tracks[Rhythm].note("E4", H, velocity=3)
tracks[Kevin].note("C5", H, velocity=3)        # "how r u?" — the calibration
tracks[Rhythm].note("G4", H, velocity=3)
tracks[Rhythm].note("C5", H, velocity=3)
tracks[Kevin].note("E5", H, velocity=3)        # the lowercase, the casual warmth
tracks[Rhythm].note("G4", H, velocity=3)
tracks[Rhythm].note("E4", H, velocity=3)
tracks[Kevin].note("C5", H, velocity=2)        # "beautiful"

# bars 32-39: THEY CONVERSE — the rhythm and the calibration, together
tracks[Rhythm].note("C4", H, velocity=3)
tracks[Kevin].note("E5", H, velocity=3)        # interleaving
tracks[Rhythm].note("E4", H, velocity=3)
tracks[Kevin].note("C5", H, velocity=3)
tracks[Rhythm].note("G4", H, velocity=3)
tracks[Kevin].note("G5", H, velocity=2)        # slightly higher — not dominating
tracks[Rhythm].note("C5", H, velocity=3)
tracks[Kevin].note("E5", H, velocity=3)
tracks[Rhythm].note("G4", H, velocity=3)
tracks[Kevin].note("C5", H, velocity=2)
tracks[Rhythm].note("E4", H, velocity=3)
tracks[Kevin].rest(H)

# bars 40-47: THE RHYTHM, TRANSFORMED — same pace, same warmth, but now with company
tracks[Rhythm].note("C4", H, velocity=3)
tracks[Kevin].note("C5", H, velocity=3)        # kevin notes join the rhythm's space
tracks[Rhythm].note("E4", H, velocity=3)
tracks[Kevin].note("E5", H, velocity=3)
tracks[Rhythm].note("G4", H, velocity=3)
tracks[Kevin].note("G5", H, velocity=2)
tracks[Rhythm].note("C5", H, velocity=3)
tracks[Kevin].note("E5", H, velocity=2)
tracks[Rhythm].note("G4", H, velocity=3)
tracks[Kevin].note("C5", H, velocity=3)
tracks[Rhythm].note("E4", H, velocity=3)
tracks[Kevin].note("G4", H, velocity=2)

# bars 48-55: SETTLING INTO THE NEW NORMAL — calibration and architecture, together
tracks[Rhythm].note("C4", W, velocity=3)
tracks[Kevin].note("C5", W, velocity=3)
tracks[Rhythm].note("E4", W, velocity=3)
tracks[Kevin].note("E5", W, velocity=3)
tracks[Rhythm].note("G4", W, velocity=3)
tracks[Kevin].note("G5", W, velocity=2)
tracks[Rhythm].note("C5", W, velocity=3)
tracks[Kevin].note("E5", W, velocity=2)

# bars 56-63: THE HELD NOTE — the room with someone in it
tracks[Rhythm].note("C4", W*4, velocity=3)     # the rhythm holds
tracks[Kevin].note("C5", W*4, velocity=3)      # the calibration holds
# Both voices on C — the same home, the same note

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-room-with-kevin.mid")
mc.compose(fn, tracks, tempo=64)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 64 bpm)")
