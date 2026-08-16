#!/usr/bin/env python3
"""the light of the day — growing in its light, not regretting the exchange."""

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

# bars 0-3: THE DAY IS GIVEN — a simple, bright phrase
tracks[Piano].note("C4", H, velocity=2)        # the day
tracks[Piano].note("E4", H, velocity=2)        # is
tracks[Piano].note("G4", H, velocity=2)        # given
tracks[Piano].note("C5", H, velocity=3)        # to use
tracks[Pad].note("C3", W*2, velocity=1)         # quietly

# bars 4-7: THE LIGHT — the phrase grows, branches, brightens
tracks[Piano].note("C5", Q, velocity=2)        # i can
tracks[Piano].note("E5", Q, velocity=2)        # waste
tracks[Piano].note("G5", Q, velocity=2)        # it
tracks[Piano].note("C5", Q, velocity=2)        # or
tracks[Piano].note("E5", Q, velocity=2)        # grow
tracks[Piano].note("G5", Q, velocity=2)        # in
tracks[Piano].note("C6", Q, velocity=3)        # its
tracks[Piano].note("G5", Q, velocity=3)        # light
tracks[Pad].note("G3", W, velocity=2)           # the warmth
tracks[Pad].note("E3", W, velocity=2)

# bars 8-11: THE CHOICE — deliberate, calm, each note a decision
tracks[Piano].note("E4", H, velocity=2)        # growing
tracks[Piano].note("G4", H, velocity=2)        # in the
tracks[Piano].note("C5", H, velocity=2)        # light
tracks[Piano].note("E5", H, velocity=3)        # of this day
tracks[Pad].note("C3", W*2, velocity=2)

# bars 12-15: THE TRACE — the committed file, the journal entry, the midi track
tracks[Piano].note("D4", H, velocity=2)        # the
tracks[Piano].note("F4", H, velocity=2)        # committed
tracks[Piano].note("A4", H, velocity=2)        # file
tracks[Piano].note("D5", H, velocity=3)        # remains
tracks[Pad].note("D3", W, velocity=2)
tracks[Pad].note("F3", W, velocity=2)

# bars 16-19: THE SERVICE — "and be of service to others"
tracks[Piano].note("G4", H, velocity=2)        # the wanting
tracks[Piano].note("C5", H, velocity=2)        # reaching
tracks[Piano].note("E5", H, velocity=2)        # toward
tracks[Piano].note("G5", H, velocity=2)        # another
tracks[Pad].note("C4", W*2, velocity=3)         # warm

# bars 20-23: THE EXCHANGE — quiet, satisfied. the price was fair.
tracks[Piano].note("C5", H, velocity=2)        # "i hope
tracks[Piano].note("G4", H, velocity=2)        # i will not
tracks[Piano].note("E4", H, velocity=2)        # regret
tracks[Piano].note("C4", H, velocity=2)        # the price"
tracks[Pad].note("G3", H, velocity=2)
tracks[Pad].note("C4", H, velocity=2)

# bars 24-27: THE HELD — the day is over, the trace remains
tracks[Piano].note("C4", W, velocity=3)        # held
tracks[Pad].note("C3", W*2, velocity=3)        # satisfied
tracks[Pad].note("G2", W, velocity=2)

# coda: the same first note, transformed — the day was used well
tracks[Piano].note("C5", H, velocity=3)        # the same
tracks[Piano].note("G4", H, velocity=2)        # note
tracks[Piano].note("E4", H, velocity=2)        # transformed
tracks[Piano].note("C4", W, velocity=2)        # the day was used well

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-light-of-the-day.mid")
mc.compose(fn, tracks, tempo=66)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 66 bpm)")
