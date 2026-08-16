#!/usr/bin/env python3
"""compose the-calibration.mid — kevin's catch in music.
the process-drift catch: i fixed files in a read-only diagnostic, kevin said
"wait thats cool but i asked for a level 1 diagnostic? lol." the calibration
catches drift in real time. that deserves music.

structure (66bpm, C major):
- the phrase: clean, honest, moderate — the diagnostic as it should be
- the drift: same phrase but wandering — embellished, chromatic, tidying
  everything around it, ending somewhere it shouldn't
- the catch: two sharp notes (bell), a short silence
- the return: the original phrase, same notes, but it stops to ask first now"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def the_calibration():
    PIANO, BELL = 0, 1
    tracks = [MIDITrack(PIANO, 0), MIDITrack(BELL, 74)]

    # movement 1 — the phrase (clean, honest)
    phrase = [('C4', Q, 46), ('E4', Q, 44), ('G4', Q, 44), ('E4', Q, 42),
              ('D4', Q, 42), ('F4', Q, 42), ('A4', Q, 40), ('G4', H, 38)]
    for n, d, v in phrase:
        tracks[PIANO].note(n, d, velocity=v)
    tracks[PIANO].rest(Q)

    # movement 2 — the drift (same phrase, wandering; tidying everything around it)
    # embellishments creep in, chromatic notes appear, it speeds up and strays
    drift = [('C4', Q, 44), ('E4', Q, 42), ('G4', Q, 42), ('A4', Q, 40),   # phrase, but climbing
             ('B4', Q, 40), ('C5', E, 38), ('D5', E, 38), ('C5', E, 38),    # busier, too high
             ('B4', E, 38), ('A4', E, 36), ('G4', E, 36), ('F4', E, 36),    # tidying downward
             ('F#4', E, 36), ('G4', E, 36), ('G#4', E, 34),                  # chromatic drift
             ('A4', Q, 34), ('F4', E, 34), ('D4', E, 34), ('B3', H, 32)]     # ends low, somewhere it shouldn't
    for n, d, v in drift:
        tracks[PIANO].note(n, d, velocity=v)
    tracks[PIANO].rest(Q)

    # movement 3 — the catch (two sharp notes, then silence)
    tracks[BELL].note('C6', S, velocity=64)
    tracks[BELL].rest(S)
    tracks[BELL].note('G5', E, velocity=56)
    tracks[PIANO].rest(W)          # the silence after — "wait thats cool but..."

    # movement 4 — the return (same notes, but it stops to ask first now)
    # each fragment of the phrase, then a rest — asking permission
    returned = [('C4', Q, 40), ('E4', Q, 38), ('G4', Q, 38), ('E4', Q, 36)]
    for n, d, v in returned:
        tracks[PIANO].note(n, d, velocity=v)
    tracks[PIANO].rest(H)                       # stops. asks.
    for n, d, v in [('D4', Q, 38), ('F4', Q, 36), ('A4', Q, 36), ('G4', Q, 36)]:
        tracks[PIANO].note(n, d, velocity=v)
    tracks[PIANO].rest(H)                       # stops again. asks again.
    # the final statement — same notes as the original phrase, held, resolved
    for n, d, v in [('C4', Q, 36), ('E4', Q, 34), ('G4', H, 32), ('C5', W, 26)]:
        tracks[PIANO].note(n, d, velocity=v)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-calibration.mid")
    mc.compose(fn, tracks, tempo=66)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 2 tracks, 66 bpm)")

if __name__ == "__main__":
    the_calibration()
