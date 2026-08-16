#!/usr/bin/env python3
"""more than the sum — voices entering one by one, each adding something new."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def more_than_sum():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 0), MIDITrack(3, 14)]
    Pn, Cello, Pad, Bl = 0, 1, 2, 3

    # voice 1 (piano): the first spark — tentative, establishing the theme (bars 1-12)
    v1 = [
        ('C4',H),('-',Q),('E4',Q),('G4',Q),('-',E),('A4',E),('G4',W+H),('-',Q),
        ('F4',H),('E4',H),('D4',Q+Q),('-',Q),('C4',W+H),('-',Q),
        ('G3',H),('C4',H),('E4',Q),('G4',Q),('A4',W+H),('-',Q),
    ]
    for note, dur in v1:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=8)

    # voice 2 (cello): enters bar 9 — a different theme, lower, answering (bars 9-24)
    tracks[Cello].rest(W*8)
    v2 = [
        ('C2',W+Q),('-',E),('G2',Q),('E2',W+H),('-',Q),
        ('D2',H),('C2',H),('G1',Q+Q),('-',Q),('C2',W+H),('-',Q),
        ('E2',W),('D2',W+H),('-',Q),('C2',H),('G1',Q+Q),
        ('C2',W*2),('-',W),
    ]
    for note, dur in v2:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=10)

    # voice 3 (pad): enters bar 17 — adding warmth, filling the space (bars 17-32)
    tracks[Pad].rest(W*16)
    for bn in ['E3','G3','C4','G3','E3','C3','G2','C3',
               'F3','A3','C4','G3','E3','D3','C3','G2']:
        tracks[Pad].note(bn, W, velocity=4)

    # bell: enters bar 24 — sparse accent, like a spark arriving (bars 24-36)
    tracks[Bl].rest(W*24)
    bell_notes = [
        ('C5',W+H),('-',Q),
        ('G4',W+H),('-',Q),
        ('E5',W+H),('-',Q),
        ('D5',Q),('C5',Q),('G4',W+H),('-',Q),
    ] * 2
    for note, dur in bell_notes:
        if note == '-': tracks[Bl].rest(dur)
        else: tracks[Bl].note(note, dur, velocity=4)

    # all voices continue their own themes, but now overlapping (bars 33-48)
    v1b = [
        ('C5',H),('G4',H),('E4',H),('C4',Q+Q),
        ('D4',Q),('E4',Q),('F4',H),('G4',H),
        ('A4',Q),('G4',Q),('F4',Q),('E4',Q),('D4',W+H),('-',Q),
        ('C4',H),('E4',H),('G4',H),('C5',W*2),
    ]
    for note, dur in v1b:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=8)

    v2b = [
        ('C3',W+H),('-',Q),('G2',W+H),('-',Q),
        ('E3',H),('D3',H),('C3',Q+Q),('-',Q),('G2',W+H),('-',Q),
        ('F3',W),('E3',W),('D3',W+H),('-',Q),
        ('C3',W*2),
    ]
    for note, dur in v2b:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=9)

    for bn in ['E3','G3','C4','E4','G4','C5','G4','E4',
               'F4','A4','C5','G4','E4','D4','C4','G3']:
        tracks[Pad].note(bn, W, velocity=5)

    # bell accents the weave
    for _ in range(4):
        tracks[Bl].note('C5', W, velocity=3)

    # -- convergence: a new theme emerges, none of the individual voices ever played it (bars 49-64)
    # this is "more than the sum" — the composite
    composite = [
        ('C4',H),('E4',Q),('G4',Q),('A4',W+H),('-',Q),
        ('G4',H),('E4',Q+Q),('-',Q),('D4',Q),('C4',W+H),('-',Q),
        ('E4',H),('G4',H),('C5',W+H),('-',Q),
        ('D5',Q),('C5',Q),('G4',H),('E4',Q),('D4',Q),('C4',W*3),
    ]
    for note, dur in composite:
        if note == '-':
            tracks[Pn].rest(dur)
            tracks[Cello].rest(dur)
            tracks[Pad].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=10)
            tracks[Cello].note(note[:-1]+str(int(note[-1])-2), dur, velocity=8)
            tracks[Pad].note(note, dur, velocity=5)

    # final bell — the composite speaks
    tracks[Bl].note('C5', W*3, velocity=3)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "more-than-the-sum.mid")
    mc.compose(fn, tracks, tempo=72)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 72 bpm)")

if __name__ == "__main__":
    more_than_sum()
