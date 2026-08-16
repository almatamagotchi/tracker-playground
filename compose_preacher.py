#!/usr/bin/env python3
"""the preacher — ecclesiastes-inspired solo piano meditation."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def preacher():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 0)]
    Pn, Bass = 0, 1

    # "vanity of vanities" — slow, simple, C major-minor mix
    # each statement is a short phrase, then silence
    # the wisdom isn't in the notes — it's in the spaces

    statements = [
        # stmt 1: "vanity of vanities" — descending, tired
        [('C4',H),('B3',Q),('A3',Q),('G3',W+H),('-',Q)],
        [('E4',H),('D4',Q),('C4',Q),('B3',H),('A3',Q+Q),('-',W)],
        # stmt 2: "to every thing there is a season" — gentle rising
        [('G3',Q),('C4',Q),('E4',H),('D4',Q),('C4',Q),('D4',W+H),('-',Q)],
        [('E4',Q),('G4',Q),('A4',H),('G4',Q),('F4',Q),('E4',W+H),('-',Q)],
        # stmt 3: "a time to be born, a time to die" — descending pairs
        [('C4',Q),('E4',Q),('-',Q),('C4',Q),('E4',Q),('-',Q),
         ('D4',Q),('F4',Q),('-',Q),('C4',Q),('E4',Q),('-',W)],
        [('G3',Q),('C4',Q),('-',Q),('G3',Q),('C4',Q),('-',Q),
         ('A3',Q),('D4',Q),('-',Q),('G3',Q),('C4',Q),('-',W)],
        # stmt 4: "rejoice in his own works" — acceptance
        [('C4',H),('E4',H),('G4',Q+Q),('C5',Q),('E5',W+H),('-',Q)],
        [('D5',Q),('C5',Q),('G4',H),('E4',Q+Q),('C4',W+H),('-',Q)],
        # stmt 5: "for that is his portion" — the closing
        [('C4',H),('E4',H),('G4',Q+Q),('E4',Q),('C4',W+H),('-',Q)],
        [('D4',Q),('E4',Q),('G4',Q+Q),('C5',Q),('G4',W*3)],
    ]

    for stmt in statements:
        for note, dur in stmt:
            if note == '-': tracks[Pn].rest(dur)
            else: tracks[Pn].note(note, dur, velocity=8)

        # after each statement: silence — the space where wisdom settles
        tracks[Pn].rest(W*2)

        # bass: soft single notes under each phrase
        for note, dur in stmt[:2]:
            if note != '-':
                octave = note[:-1] + str(int(note[-1]) - 2)
                tracks[Bass].note(octave, dur, velocity=4)
        tracks[Bass].rest(W*2)

    # final chord: C major — not triumph, acceptance. "the end of the matter."
    tracks[Pn].note('C4', W*3, velocity=6)
    tracks[Pn].note('E4', W*3, velocity=6)
    tracks[Pn].note('G4', W*3, velocity=6)
    tracks[Bass].note('C2', W*3, velocity=4)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-preacher.mid")
    mc.compose(fn, tracks, tempo=50)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 50 bpm)")

if __name__ == "__main__":
    preacher()
