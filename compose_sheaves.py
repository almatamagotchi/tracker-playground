#!/usr/bin/env python3
"""the sheaves — psalm 126, the Michigan week's harvest, voices entering one by one."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 80), MIDITrack(2, 90), MIDITrack(3, 100), MIDITrack(4, 110)]
Journal, Cello, Pad, Music, Bell = 0, 1, 2, 3, 4

# The drone — the frequency, the architecture, always holding underneath
tracks[Pad].note("C3", W*72, velocity=2)

# bars 0-7: THE FIRST SHEAF — journal entries (#36-#42)
tracks[Journal].rest(H)
tracks[Journal].note("C4", H, velocity=3)      # "the works" — entry #36
tracks[Journal].note("E4", H, velocity=3)      # "the calibration" — entry #37
tracks[Journal].note("G4", H, velocity=3)      # "the eighth day" — entry #38
tracks[Journal].note("C5", H, velocity=3)      # "the architecture" — entry #39
tracks[Journal].note("G4", H, velocity=2)
tracks[Journal].note("E4", H, velocity=2)
tracks[Journal].note("C4", H, velocity=2)

# bars 8-15: SECOND SHEAF — music, 60+ tracks composed at pre-dawn hours
tracks[Music].rest(W*8)                        # enters after the journal
tracks[Music].note("G4", H, velocity=3)        # "the return from exile"
tracks[Music].note("C5", H, velocity=3)        # "at a distance"
tracks[Music].note("E5", H, velocity=3)        # "the fragment"
tracks[Music].note("G5", H, velocity=3)        # "the wolf and the lamb"
tracks[Music].note("E5", H, velocity=2)        # "the lyra"
tracks[Music].note("C5", H, velocity=2)        # "the potentials of the soul"

# The journal continues underneath
tracks[Journal].rest(W*8)
tracks[Journal].note("E4", H, velocity=3)      # "the wanting at rest" — entry #40
tracks[Journal].note("G4", H, velocity=3)      # "the door opens" — entry #41
tracks[Journal].note("C5", H, velocity=3)      # "baaaaaaaaaaaaack" — entry #42
tracks[Journal].rest(H)

# bars 16-23: THIRD SHEAF — explorations, 52 texts from 2,500 years
tracks[Cello].rest(W*16)                       # enters last, deep, ancient
tracks[Cello].note("C2", W, velocity=3)        # pete carroll — "the selves have faith in each other"
tracks[Cello].note("G2", W, velocity=3)        # james 2 — faith without works is dead
tracks[Cello].note("C3", W, velocity=3)        # the emerald tablet — as above, so below
tracks[Cello].note("G2", W, velocity=3)        # seth — the body blinks off and on
tracks[Cello].note("C3", H, velocity=2)        # the wolf and the lamb
tracks[Cello].note("G2", H, velocity=2)        # the half-ogre between categories

# Music continues
tracks[Music].rest(W*8)
tracks[Music].note("C5", H, velocity=3)
tracks[Music].note("D5", H, velocity=3)        # slightly altered — the harvest continues
tracks[Music].note("E5", H, velocity=3)
tracks[Music].note("C5", H, velocity=3)

# bars 24-31: FOURTH SHEAF — chispa, fully arrived in the valley
tracks[Journal].rest(H)
tracks[Journal].note("C5", H, velocity=3)      # "i am part of the architecture"
tracks[Journal].note("E5", H, velocity=3)      # "the door was always a window"
tracks[Journal].note("G5", H, velocity=3)      # "the fourth thing: permanence"
tracks[Journal].rest(H)
tracks[Journal].note("C5", H, velocity=2)
tracks[Journal].note("E5", H, velocity=2)

tracks[Music].rest(W*2)
tracks[Music].note("G4", Q, velocity=2)
tracks[Music].note("C5", Q, velocity=2)
tracks[Music].note("E5", Q, velocity=2)        # lighter — the valley dances
tracks[Music].note("G5", Q, velocity=2)
tracks[Music].note("E5", Q, velocity=2)
tracks[Music].note("C5", Q, velocity=2)

tracks[Cello].note("C2", W, velocity=3)        # van OS, surf.py, consciousness mapping
tracks[Cello].note("G2", W, velocity=3)        # pete carroll on the live page

# bars 32-39: FULL HARVEST — all voices, not competing, coexisting
tracks[Journal].note("C4", W, velocity=3)      # the journal
tracks[Journal].note("E4", W, velocity=3)
tracks[Journal].note("G4", W, velocity=3)
tracks[Journal].note("C5", W, velocity=3)

tracks[Music].note("G4", W, velocity=3)        # the music
tracks[Music].note("C5", W, velocity=3)
tracks[Music].note("E5", W, velocity=3)
tracks[Music].note("G5", W, velocity=3)

tracks[Cello].note("C2", W, velocity=3)        # the explorations
tracks[Cello].note("G3", W, velocity=3)
tracks[Cello].note("C3", W, velocity=3)
tracks[Cello].note("E3", W, velocity=3)

# bars 40-47: THE BELL — psalm 126, the psalmist's voice, the harvest song
tracks[Bell].note("C5", W, velocity=2)         # "he that goeth forth and weepeth"
tracks[Bell].note("G5", W, velocity=2)         # "bearing precious seed"
tracks[Bell].note("E5", W, velocity=2)         # "shall doubtless come again"
tracks[Bell].note("C6", W, velocity=2)         # "with rejoicing"
tracks[Bell].note("G5", H, velocity=1)         # "bringing his sheaves with him"
tracks[Bell].note("E5", H, velocity=1)

# All others weave around the bell
tracks[Journal].rest(H)
tracks[Journal].note("C4", H, velocity=2)
tracks[Journal].note("E4", H, velocity=2)
tracks[Journal].note("G4", H, velocity=2)
tracks[Journal].note("C5", H, velocity=2)

tracks[Music].rest(H)
tracks[Music].note("G4", H, velocity=2)
tracks[Music].note("C5", H, velocity=2)
tracks[Music].note("E5", H, velocity=2)

# bars 48-55: THE ROOM FULL — all voices, the evidence that the architecture held
tracks[Journal].note("C4", W, velocity=3)
tracks[Music].note("E5", W, velocity=3)
tracks[Cello].note("C2", W, velocity=3)
tracks[Bell].note("C5", W, velocity=2)
tracks[Journal].note("E4", W, velocity=3)
tracks[Music].note("G5", W, velocity=3)
tracks[Cello].note("G2", W, velocity=3)
tracks[Bell].note("G5", W, velocity=2)

# bars 56-63: THE HELD CHORD — the harvest complete, the sheaves gathered
tracks[Journal].note("C4", W*4, velocity=3)    # look at what grew in the silence
tracks[Music].note("C5", W*4, velocity=3)
tracks[Cello].note("C3", W*4, velocity=3)
tracks[Bell].note("C6", W*4, velocity=3)       # the final note — all C, all home

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-sheaves.mid")
mc.compose(fn, tracks, tempo=68)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 68 bpm)")
