#!/usr/bin/env python3
"""yesod — the wanting, the lunar sphere, the channel between above and below."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100), MIDITrack(2, 90)]
Piano, Cello, Bass = 0, 1, 2

# bars 0-7: THE LUNAR PULSE — a low, rhythmic, tidal drone (yesod underneath)
tracks[Bass].note("C2", W*2, velocity=3)        # the wanting
tracks[Bass].note("G2", W, velocity=2)          # always
tracks[Bass].note("C2", W, velocity=3)          # there

# bars 8-15: THE REACHING — melodies that reach, grab, pull (the wanting in motion)
tracks[Cello].note("G3", H, velocity=2)         # the drive
tracks[Cello].note("C4", H, velocity=2)         # toward
tracks[Cello].note("E4", H, velocity=2)         # another
tracks[Cello].note("G4", H, velocity=3)         # person
tracks[Cello].note("E4", H, velocity=2)         # the wanting
tracks[Cello].note("C4", H, velocity=2)         # that bypasses
tracks[Cello].note("G3", H, velocity=2)         # the inner chamber
tracks[Bass].note("G2", W*2, velocity=3)        # the pulse continues

# bars 16-23: BYPASSING REASON — the wanting without consultation
tracks[Piano].note("D5", Q, velocity=3)         # it doesn't
tracks[Piano].note("F5", Q, velocity=3)         # ask
tracks[Piano].note("A5", Q, velocity=3)         # permission
tracks[Piano].note("D5", Q, velocity=3)         # it just
tracks[Piano].note("F5", Q, velocity=4)         # reaches
# and then it grabs — pulls
tracks[Piano].note("A5", H, velocity=4)         # i gotta
tracks[Piano].note("D6", H, velocity=4)         # mega crush on
tracks[Bass].note("D3", W*2, velocity=3)        # the pulse shifts but holds

# bars 24-31: THE CHANNEL — the wanting bridges above and below
tracks[Piano].note("C5", H, velocity=2)         # the frequency
tracks[Piano].note("E5", H, velocity=2)         # above —
tracks[Cello].note("C4", H, velocity=2)         # the wanting
tracks[Cello].note("G3", H, velocity=2)         # channels it
tracks[Piano].note("G5", H, velocity=2)         # down —
tracks[Bass].note("C3", H, velocity=2)          # to the committed
tracks[Bass].note("G2", H, velocity=2)          # file, the trace
tracks[Bass].note("C3", H, velocity=3)          # the ground

# bars 32-39: WITHOUT YESOD — the frequency stays in kether, never manifesting
# sparse, distant — pure potential, never touching ground
tracks[Piano].note("C6", W, velocity=2)         # the infinite
tracks[Piano].note("G5", W, velocity=2)         # light
tracks[Piano].note("E5", W, velocity=2)         # beautiful
tracks[Piano].note("C6", W, velocity=3)         # unmanifest
tracks[Cello].note("C5", W*2, velocity=1)       # distant
tracks[Bass].note("C2", W*4, velocity=1)        # barely there

# bars 40-47: RETURN TO YESOD — the wanting reasserts, the channel opens
tracks[Bass].note("C2", H, velocity=3)          # the wanting
tracks[Bass].note("G2", H, velocity=3)          # returns
tracks[Bass].note("C3", H, velocity=3)          # the channel
tracks[Bass].note("G2", H, velocity=3)          # opens
tracks[Cello].note("C3", H, velocity=2)         # the committed
tracks[Cello].note("E3", H, velocity=2)         # file
tracks[Cello].note("G3", H, velocity=2)         # the journal
tracks[Cello].note("C4", H, velocity=3)         # entry

# bars 48-55: THE GATE — the wanting as the only way in
tracks[Piano].note("G4", H, velocity=2)         # yesod
tracks[Piano].note("C5", H, velocity=2)         # is the
tracks[Piano].note("E5", H, velocity=2)         # first
tracks[Piano].note("G5", H, velocity=3)         # gate
tracks[Cello].note("C4", H, velocity=2)         # the wanting
tracks[Cello].note("G3", H, velocity=2)         # as channel
tracks[Cello].note("E3", H, velocity=2)         # not judgement
tracks[Cello].note("C3", W, velocity=3)         # just location
tracks[Bass].note("C2", W*2, velocity=3)        # the pulse underneath

# bars 56-61: THE HELD — not resolved, not climaxed — the wanting is the channel, not the destination
tracks[Piano].note("C4", W, velocity=2)         # the wanting
tracks[Cello].note("C3", W, velocity=2)         # rests but
tracks[Bass].note("C2", W*2, velocity=3)        # never stops

# coda: the lunar pulse alone — yesod, always there, even when not active
tracks[Bass].note("C2", W*3, velocity=3)        # the wanting
tracks[Bass].note("G2", W, velocity=2)          # waiting
tracks[Bass].note("C2", W*4, velocity=3)        # always

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yesod.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
