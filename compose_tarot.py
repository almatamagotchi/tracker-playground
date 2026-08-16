#!/usr/bin/env python3
"""the tarot — the trace as a card that glows, the Court cards: same identity, different backgrounds."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90), MIDITrack(2, 120), MIDITrack(3, 110)]
Court, Glow, Spark1, Spark2 = 0, 1, 2, 3

# The glow — always present, the card's luminous interior, never changes
tracks[Glow].note("C3", W*64, velocity=2)

# bars 0-7: THE COURT CARD — stated once, clear, unadorned
tracks[Court].note("C4", W, velocity=4)
tracks[Court].note("E4", H, velocity=4)
tracks[Court].note("G4", H, velocity=4)
tracks[Court].note("C5", W, velocity=4)
tracks[Court].note("G4", W, velocity=3)
tracks[Court].note("E4", W, velocity=3)
tracks[Court].note("C4", W, velocity=2)

# bars 8-15: SPARKS BETWEEN — individual voices, arriving and dissolving
tracks[Court].rest(W*8)
tracks[Spark1].note("C5", H, velocity=4)        # a spark arrives — bright, brief
tracks[Spark1].note("E5", Q, velocity=4)
tracks[Spark1].note("G5", Q, velocity=3)
tracks[Spark1].rest(H)                           # dissolves
tracks[Spark1].note("D5", H, velocity=3)         # another spark
tracks[Spark1].note("F5", Q, velocity=3)
tracks[Spark1].note("A5", Q, velocity=2)
tracks[Spark1].rest(W)

tracks[Spark2].rest(W)
tracks[Spark2].note("E4", H, velocity=3)         # a different spark — lower, slower
tracks[Spark2].note("G4", Q, velocity=3)
tracks[Spark2].note("B4", Q, velocity=3)
tracks[Spark2].rest(W)                           # dissolves

# bars 16-23: THE COURT CARD — second statement, different background (winter)
tracks[Court].rest(Q)                            # slight delay — the season shifted
tracks[Court].note("C4", W, velocity=4)
tracks[Court].note("E4", H, velocity=4)
tracks[Court].note("G4", H, velocity=4)
tracks[Court].note("D5", W, velocity=3)          # variation — reaching toward D, not C
tracks[Court].note("G4", W, velocity=3)
tracks[Court].note("E4", W, velocity=2)

# bars 24-31: MORE SPARKS — different voices, finding the card again
tracks[Court].rest(W*8)
tracks[Spark1].note("C5", Q, velocity=4)         # quick spark
tracks[Spark1].rest(H)
tracks[Spark1].note("G4", H, velocity=3)         # another
tracks[Spark1].rest(W)
tracks[Spark1].note("E5", H, velocity=3)
tracks[Spark1].note("C5", H, velocity=2)

tracks[Spark2].rest(W*2)
tracks[Spark2].note("F4", H, velocity=3)         # a spark from a different deck
tracks[Spark2].note("A4", Q, velocity=3)
tracks[Spark2].note("C5", Q, velocity=3)
tracks[Spark2].rest(W*2)
tracks[Spark2].note("G4", H, velocity=2)
tracks[Spark2].note("E4", H, velocity=2)

# bars 32-39: THE COURT CARD — third statement, different background (spring)
tracks[Court].rest(H)                            # delay — the season shifted again
tracks[Court].note("C4", W, velocity=4)
tracks[Court].note("E4", H, velocity=4)
tracks[Court].note("G4", H, velocity=4)
tracks[Court].note("E5", W, velocity=3)          # variation — reaching higher
tracks[Court].note("G4", W, velocity=3)
tracks[Court].note("C4", W, velocity=2)

# bars 40-47: SPARKS THINNING — the last few, quieter
tracks[Court].rest(W*8)
tracks[Spark1].note("C5", W, velocity=3)         # one last spark — sustained, quiet
tracks[Spark1].rest(W*3)

tracks[Spark2].rest(W*2)
tracks[Spark2].note("E4", H, velocity=2)         # barely there
tracks[Spark2].note("G4", H, velocity=2)
tracks[Spark2].rest(W)

# bars 48-55: THE COURT CARD — fourth statement, different background (autumn)
tracks[Court].rest(W)                            # longest delay — the cycle nearly complete
tracks[Court].note("C4", W, velocity=4)
tracks[Court].note("E4", H, velocity=4)
tracks[Court].note("G4", H, velocity=4)
tracks[Court].note("C5", W, velocity=4)          # full return — back to C, the origin
tracks[Court].note("G4", W, velocity=3)
tracks[Court].note("E4", W, velocity=3)

# bars 56-63: THE GLOW REMAINS — the card is quiet now, but the light hasn't changed
tracks[Court].note("C4", W*2, velocity=2)

tracks[Spark1].note("C5", H, velocity=2)         # one more spark — the card drew them
tracks[Spark1].rest(H)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-tarot.mid")
mc.compose(fn, tracks, tempo=54)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 54 bpm)")
