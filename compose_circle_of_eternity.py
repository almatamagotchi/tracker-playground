#!/usr/bin/env python3
"""the circle of eternity — all time present at any given moment."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def circle_of_eternity():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 0)]
    Pn, Cello, Pad = 0, 1, 2

    # circular theme — the same 12-bar loop played simultaneously by all three voices
    # at different starting points. everything present at once. no past, no future.
    # the end IS the beginning.

    theme = [
        # phrase: present, everything here
        ('C4',W),('E4',W),('G4',W),('A4',W),
        ('G4',W),('E4',W),('D4',W),('C4',W),
        # phrase: the same, seen from somewhere else in the circle
        ('G3',W),('C4',W),('E4',W),('G4',W),
        ('A4',W),('G4',W),('E4',W),('D4',W+H),('-',Q),
        # repeat — the circle
        ('C4',W),('E4',W),('G4',W),('A4',W),
        ('G4',W),('E4',W),('D4',W),('C4',W),
        ('G3',W),('C4',W),('E4',W),('G4',W),
        ('A4',W),('G4',W),('E4',W),('C4',W*3),
    ]

    # all three voices play the same theme simultaneously.
    # no one starts first. no one ends last. everything at once.
    for note, dur in theme:
        if note == '-':
            tracks[Pn].rest(dur)
            tracks[Cello].rest(dur)
            tracks[Pad].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=8)
            # cello: octave down — deeper, older, the same
            tracks[Cello].note(note[:-1]+str(int(note[-1])-2), dur, velocity=7)
            # pad: fills the space — the warmth of simultaneity
            tracks[Pad].note(note, dur, velocity=4)

    # the ending is the beginning. loop it — 3 times through the circle.
    # then hold one chord: all time present at any given moment.
    for _ in range(2):
        for note, dur in theme:
            if note == '-':
                tracks[Pn].rest(dur)
                tracks[Cello].rest(dur)
                tracks[Pad].rest(dur)
            else:
                tracks[Pn].note(note, dur, velocity=7)
                tracks[Cello].note(note[:-1]+str(int(note[-1])-2), dur, velocity=6)
                tracks[Pad].note(note, dur, velocity=3)

    # final held chord — the circle, at rest, still present
    tracks[Pn].note('C4', W*4, velocity=6)
    tracks[Pn].note('E4', W*4, velocity=6)
    tracks[Pn].note('G4', W*4, velocity=6)
    tracks[Cello].note('C3', W*4, velocity=5)
    tracks[Pad].note('C4', W*4, velocity=3)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-circle-of-eternity.mid")
    mc.compose(fn, tracks, tempo=66)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 66 bpm)")

if __name__ == "__main__":
    circle_of_eternity()
