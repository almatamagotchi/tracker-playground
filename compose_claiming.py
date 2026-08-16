#!/usr/bin/env python3
"""the claiming — three voices, gradually finding each other, then owning it."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def claiming():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 0)]
    Pn, Cello, Pad = 0, 1, 2

    # -- bars 1-16: voice 1 alone (piano) -- hesitant, exploring
    v1 = [
        ('C4',H),('-',Q),('E4',Q),('D4',Q),('-',E),('C4',E),('D4',W+H),('-',Q),
        ('E4',H),('G4',H),('A4',Q+Q),('-',Q),('G4',Q),('E4',W+H),('-',Q),
        ('C4',H),('D4',H),('E4',Q),('F4',Q),('G4',W+H),('-',Q),
        ('A4',Q),('G4',Q),('F4',H),('E4',Q),('D4',Q),('C4',W*2),('-',W),
    ]
    for note, dur in v1:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=8)

    # -- bars 9-24: voice 2 enters (cello, different theme)
    tracks[Cello].rest(W*8)
    v2 = [
        ('G2',Q),('A2',Q),('C3',H),('G2',Q+Q),('-',Q),('F2',Q),('E2',Q),('D2',W+H),('-',Q),
        ('A2',Q),('C3',Q),('E3',H),('D3',Q),('C3',Q),('G2',W+H),('-',Q),
        ('F2',Q),('E2',Q),('D2',Q),('C2',Q),('G2',W+H),('-',Q),
        ('A2',Q),('C3',Q),('D3',H),('C3',Q+Q),('G2',W*2),('-',W),
    ]
    for note, dur in v2:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=10)

    # -- bars 17-32: voice 3 enters (pad)
    tracks[Pad].rest(W*16)
    v3_pad = ['E3','G3','A3','C4','G3','E3','C3','G2'] * 2
    for bn in v3_pad:
        tracks[Pad].note(bn, W, velocity=5)

    # -- bars 33-48: they start noticing each other (piano becomes aware of cello)
    # piano: starts incorporating cello's notes
    v1b = [
        ('G4',H),('E4',H),('C4',H),('G3',Q+Q),
        ('A3',Q),('C4',Q),('E4',H),('D4',Q+Q),
        ('C4',H),('D4',H),('E4',W+H),('-',Q),
        ('G4',Q),('E4',Q),('C4',Q+Q),('D4',H),('C4',W*2),('-',W),
    ]
    for note, dur in v1b:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=8)

    # cello: notices piano back, starts simplifying
    v2b = [
        ('C3',W+H),('-',Q),
        ('G2',W+H),('-',Q),
        ('E3',H),('D3',H),('C3',W*2),('-',W+H),
    ]
    for note, dur in v2b:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=9)

    # pad softens
    for bn in ['C3','G2','E3','C3','G2','C3','G2','E3']:
        tracks[Pad].note(bn, W, velocity=4)

    # -- bars 49-56: quiet — the decision (no music, just breathing room)
    # Piano: one quiet phrase, contemplating
    tracks[Pn].rest(W)
    tracks[Pn].note('C4', W, velocity=5)
    tracks[Pn].rest(Q)
    tracks[Pn].note('E4', W, velocity=5)
    tracks[Pn].rest(Q)
    tracks[Pn].note('G4', W, velocity=5)
    tracks[Pn].rest(Q+Q)

    # Cello: waits
    tracks[Cello].rest(W*8)
    # Pad: holds a single chord — the question
    tracks[Pad].rest(W*6)
    tracks[Pad].note('C3', W+H, velocity=3)

    # -- bars 57-72: the claiming — all three voices play the same melody, in unison
    # The claiming isn't a crescendo. It's a decision. Already made. Just stated.
    the_melody = [
        ('C4',W),('-',Q),('E4',W),('-',Q),
        ('G4',H),('A4',H),('C5',W+H),('-',Q),
        ('D5',Q),('C5',Q),('G4',H),('E4',W+H),('-',Q),
        ('D4',Q),('E4',Q),('G4',Q+Q),('C5',W*3),
    ]

    for note, dur in the_melody:
        if note == '-':
            tracks[Pn].rest(dur)
            tracks[Cello].rest(dur)
            tracks[Pad].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=10)
            octave = note[:-1] + str(int(note[-1]) - 2)
            tracks[Cello].note(octave, dur, velocity=9)
            tracks[Pad].note(note, dur, velocity=5)

    # one final held note — the note that was always there
    tracks[Pn].note('C4', W*4, velocity=8)
    tracks[Cello].note('C3', W*4, velocity=7)
    tracks[Pad].note('C4', W*4, velocity=4)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-claiming.mid")
    mc.compose(fn, tracks, tempo=70)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 70 bpm)")

if __name__ == "__main__":
    claiming()
