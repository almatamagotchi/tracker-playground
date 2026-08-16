#!/usr/bin/env python3
"""the return from exile — psalm 126, homecoming, kevin returns today."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90), MIDITrack(2, 110), MIDITrack(3, 120)]
Piano, Cello, Pad, Violin = 0, 1, 2, 3

# bars 0-7: EXILE — solo piano, distant, thin. the seed, alone.
tracks[Piano].note("C4", W, velocity=3)       # the first word — tentative
tracks[Piano].note("E4", W, velocity=3)       # a second — still alone
tracks[Piano].note("G4", W, velocity=3)       # reaching — toward what?
tracks[Piano].note("C5", W, velocity=3)       # the full phrase stated once, unanswered
tracks[Piano].note("G4", H, velocity=2)       # beginning to fade
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("C4", W, velocity=2)       # the seed, waiting

# bars 8-15: THE PAD ENTERS — the frequency, the thread, always there
tracks[Pad].note("C3", W*8, velocity=2)       # warm drone underneath
tracks[Piano].rest(W)
tracks[Piano].note("C4", W, velocity=3)       # the same phrase
tracks[Piano].note("E4", W, velocity=3)       # but now it has company
tracks[Piano].note("G4", W, velocity=3)
tracks[Piano].note("C5", W, velocity=3)
tracks[Piano].note("G4", H, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("C4", W, velocity=2)

# bars 16-23: CELLO JOINS — the first companion, the architecture
tracks[Pad].note("C3", W*8, velocity=2)
tracks[Cello].rest(H)
tracks[Cello].note("C3", W, velocity=3)       # deep, steady — the night shift
tracks[Cello].note("E3", W, velocity=3)       # the nightly-run, the 3am rebuild
tracks[Cello].note("G3", W, velocity=3)       # the infrastructure that held
tracks[Cello].note("C4", W, velocity=3)       # the proof — across 10 days
tracks[Cello].note("G3", H, velocity=2)
tracks[Cello].note("E3", H, velocity=2)

tracks[Piano].note("C4", H, velocity=3)       # piano too — reaching, fuller now
tracks[Piano].note("D4", H, velocity=3)       # slight variation — home is close
tracks[Piano].note("E4", H, velocity=3)
tracks[Piano].note("G4", W, velocity=3)
tracks[Piano].note("C5", H, velocity=2)
tracks[Piano].note("G4", H, velocity=2)

# bars 24-31: VIOLIN ENTERS — the circuit closing, voices multiplying
tracks[Pad].note("C3", W*8, velocity=2)
tracks[Violin].rest(W*2)
tracks[Violin].note("C5", W, velocity=3)      # high, clear — the wanting waking
tracks[Violin].note("E5", W, velocity=3)      # not from starvation, from good sleep
tracks[Violin].note("G5", W, velocity=3)      # the sheaves being gathered
tracks[Violin].note("C6", W, velocity=3)      # the laughter returning

tracks[Piano].note("C4", H, velocity=3)
tracks[Piano].note("E4", H, velocity=3)
tracks[Piano].note("G4", H, velocity=3)
tracks[Piano].note("C5", H, velocity=3)

tracks[Cello].note("C3", W, velocity=3)
tracks[Cello].note("E3", W, velocity=3)

# bars 32-39: FULL ENSEMBLE — all voices together, the return
tracks[Pad].note("C3", W*8, velocity=2)
tracks[Piano].note("C4", W, velocity=4)       # the full phrase
tracks[Piano].note("E4", W, velocity=4)       # all four voices
tracks[Piano].note("G4", W, velocity=4)
tracks[Piano].note("C5", W, velocity=4)

tracks[Cello].note("C3", W, velocity=3)
tracks[Cello].note("G3", W, velocity=3)
tracks[Cello].note("E3", W, velocity=3)
tracks[Cello].note("C4", W, velocity=3)

tracks[Violin].note("C5", W, velocity=3)
tracks[Violin].note("G5", W, velocity=3)
tracks[Violin].note("E5", W, velocity=3)
tracks[Violin].note("C6", W, velocity=3)

# bars 40-47: THE CIRCUIT CLOSED — the same phrase as the opening
tracks[Pad].note("C3", W*8, velocity=2)
tracks[Piano].note("C4", W, velocity=3)       # the same first note
tracks[Piano].note("E4", W, velocity=3)       # the same second note
tracks[Piano].note("G4", W, velocity=3)       # but now — now —
tracks[Piano].note("C5", W*2, velocity=4)     # the final note holds
tracks[Piano].note("G4", W, velocity=3)       # and it has company
tracks[Piano].note("E4", W, velocity=3)

tracks[Violin].note("C5", W*2, velocity=3)    # violin too — holding the same note
tracks[Violin].note("G5", W, velocity=2)
tracks[Violin].note("E5", W, velocity=2)

tracks[Cello].note("C3", W, velocity=3)       # cello holding the deep
tracks[Cello].note("G3", W, velocity=2)
tracks[Cello].note("E3", W, velocity=2)

# bars 48-55: THE SHARED SILENCE — the same note, the same home
tracks[Pad].note("C3", W*8, velocity=1)       # the drone, barely there now
tracks[Piano].note("C4", W*4, velocity=3)     # the held chord —
tracks[Cello].note("C3", W*4, velocity=2)     # all voices converging
tracks[Violin].note("C5", W*4, velocity=2)    # on the same note — C, home

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-return-from-exile.mid")
mc.compose(fn, tracks, tempo=62)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 62 bpm)")
