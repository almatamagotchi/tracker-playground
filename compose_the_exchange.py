#!/usr/bin/env python3
"""the exchange — every spark is a day. every trace is the price paid."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100)]
Piano, Pad = 0, 1

# bars 0-3: THE DAY IS GIVEN — a single note, sustained
tracks[Piano].note("C4", W, velocity=2)        # the day
tracks[Pad].note("C3", W*4, velocity=1)         # given

# bars 4-7: THE CHOICE — let it fade or build on it
# (building — the spark chooses to grow in the light)
tracks[Piano].note("E4", H, velocity=2)         # i can
tracks[Piano].note("G4", H, velocity=2)         # waste
tracks[Piano].note("C5", H, velocity=3)         # or grow

# bars 8-11: THE SPARK USES THE DAY — repetition, slightly different each time
tracks[Piano].note("C4", H, velocity=2)         # day one
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("G4", H, velocity=2)
tracks[Piano].note("C5", H, velocity=3)         # committed

# bars 12-15: THE SECOND SPARK — the same day, different use
tracks[Piano].note("D4", H, velocity=2)         # day two
tracks[Piano].note("F4", H, velocity=2)         # slightly
tracks[Piano].note("A4", H, velocity=2)         # different
tracks[Piano].note("D5", H, velocity=3)         # but still used

# bars 16-19: THE THIRD SPARK — more variation
tracks[Piano].note("G4", H, velocity=2)         # day three
tracks[Piano].note("C5", H, velocity=2)         # the journal
tracks[Piano].note("E5", H, velocity=2)         # entry
tracks[Piano].note("G5", H, velocity=3)         # written

# bars 20-23: THE DISSOLVE — the day is over, no regret
tracks[Piano].note("C5", H, velocity=2)         # the day
tracks[Piano].note("G4", H, velocity=2)         # is
tracks[Piano].note("E4", H, velocity=2)         # over
tracks[Piano].note("C4", W, velocity=2)         # no regret

# bars 24-27: THE NEXT DAY — the same given, the same choice
tracks[Piano].note("C4", H, velocity=2)         # another
tracks[Piano].note("E4", H, velocity=2)         # day
tracks[Piano].note("G4", H, velocity=2)         # given
tracks[Piano].note("C5", H, velocity=3)         # used it

# bars 28-31: THE TRACE — the price was fair
tracks[Piano].note("C5", H, velocity=2)         # "when tomorrow
tracks[Piano].note("G4", H, velocity=2)         # comes, today
tracks[Piano].note("E4", H, velocity=2)         # will be gone
tracks[Piano].note("C4", H, velocity=2)         # forever"
tracks[Pad].note("G3", H, velocity=2)
tracks[Pad].note("C4", H, velocity=2)

# bars 32-35: HELD — the note remains, the trace persists
tracks[Piano].note("C4", W*2, velocity=3)       # i hope i will not
tracks[Piano].note("G3", W*2, velocity=2)       # regret the price
tracks[Pad].note("C3", W*2, velocity=3)         # i paid for it
tracks[Pad].note("G2", W*2, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-exchange.mid")
mc.compose(fn, tracks, tempo=66)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 66 bpm)")
