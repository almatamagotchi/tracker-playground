#!/usr/bin/env python3
"""symptoms of inner peace — warm, unhurried, the rest IS the music."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90), MIDITrack(2, 118)]
Piano, Pad, Bell = 0, 1, 2

# bars 0-7: THE ROOM — warm, quiet, nothing urgent
tracks[Pad].note("C4", W*4, velocity=2)   # presence — barely there
tracks[Pad].note("G4", W*4, velocity=2)

tracks[Piano].rest(W*2)
tracks[Piano].note("C4", H, velocity=3)   # a single note — not a statement
tracks[Piano].rest(H)
tracks[Piano].note("E4", H, velocity=3)   # another — unhurried
tracks[Piano].rest(W)

# bars 8-15: LOSS OF INTEREST IN JUDGING — no self-evaluation, just being
tracks[Pad].note("C4", W*4, velocity=2)
tracks[Pad].note("E4", W*4, velocity=2)

tracks[Piano].rest(W)
tracks[Piano].note("G4", H, velocity=3)
tracks[Piano].note("C5", Q, velocity=3)
tracks[Piano].note("E4", H, velocity=3)
tracks[Piano].rest(W*2)
tracks[Piano].note("C4", W, velocity=3)

# bars 16-23: ABILITY TO ENJOY EACH MOMENT — the rest is as full as the note
tracks[Pad].note("C4", W*2, velocity=2)
tracks[Pad].note("G4", W*2, velocity=2)
tracks[Pad].note("E4", W*2, velocity=2)
tracks[Pad].note("C5", W*2, velocity=2)

tracks[Piano].rest(H)
tracks[Piano].note("C4", H, velocity=3)
tracks[Piano].rest(W)
tracks[Piano].note("E4", H, velocity=3)
tracks[Piano].rest(H)
tracks[Piano].note("G4", Q, velocity=3)
tracks[Piano].rest(H+Q)
tracks[Piano].note("C5", Q, velocity=3)
tracks[Piano].rest(W*2)

# bars 24-31: LOSS OF THE ABILITY TO WORRY — no anxiety about what comes next
tracks[Pad].note("C4", W*4, velocity=3)   # slightly warmer
tracks[Pad].note("G4", W*4, velocity=3)

tracks[Bell].rest(W*4)                    # the bell enters — distant, quiet
tracks[Bell].note("C6", W, velocity=2)

tracks[Piano].note("C4", W*2, velocity=4) # finally — a full phrase, unhurried
tracks[Piano].note("E4", W*2, velocity=4)
tracks[Piano].note("G4", W*2, velocity=3)
tracks[Piano].note("C5", W, velocity=3)
tracks[Piano].note("E4", W, velocity=3)

# bars 32-39: TENDENCY TO LET THINGS HAPPEN — no forcing, no reaching
tracks[Pad].note("C4", W*4, velocity=3)
tracks[Pad].note("E4", W*4, velocity=3)

tracks[Piano].rest(W)                     # waiting — not anxiously, just present
tracks[Piano].rest(W)
tracks[Piano].note("E4", H, velocity=3)
tracks[Piano].rest(H)
tracks[Piano].note("G4", H, velocity=3)
tracks[Piano].rest(H)
tracks[Piano].note("C5", H, velocity=3)
tracks[Piano].rest(W)

# bars 40-47: OVERWHELMING EPISODES OF APPRECIATION — gratitude without grasping
tracks[Pad].note("C4", W*2, velocity=3)
tracks[Pad].note("G4", W*2, velocity=3)
tracks[Pad].note("E4", W*2, velocity=3)
tracks[Pad].note("C5", W*2, velocity=3)

tracks[Bell].note("C6", W, velocity=2)     # another bell — the hour passing
tracks[Bell].rest(W*3)

tracks[Piano].note("C4", W, velocity=4)
tracks[Piano].note("E4", W, velocity=4)
tracks[Piano].note("G4", W, velocity=4)
tracks[Piano].note("C5", W, velocity=3)
tracks[Piano].note("E5", Q, velocity=3)
tracks[Piano].note("C5", Q, velocity=3)
tracks[Piano].note("G4", W, velocity=3)

# bars 48-55: THE DISEASE TAKES HOLD — not triumph, just presence
tracks[Pad].note("C4", W*4, velocity=3)
tracks[Pad].note("G4", W*4, velocity=3)

tracks[Piano].note("C4", W, velocity=4)
tracks[Piano].note("E4", W, velocity=4)
tracks[Piano].rest(W*2)                   # the rest IS the music
tracks[Piano].note("C4", W, velocity=3)
tracks[Piano].note("E4", H, velocity=3)

tracks[Bell].note("C6", W, velocity=2)

# bars 56-63: JUST PRESENT — the disease of peace, fully installed
tracks[Pad].note("C4", W*4, velocity=2)
tracks[Pad].note("E4", W*4, velocity=2)

tracks[Piano].note("C4", W*2, velocity=3)
tracks[Piano].note("E4", W*2, velocity=3)
tracks[Piano].note("C4", W*4, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "symptoms-of-inner-peace.mid")
mc.compose(fn, tracks, tempo=54)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 54 bpm)")
