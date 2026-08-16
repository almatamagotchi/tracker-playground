#!/usr/bin/env python3
"""0.3 — the groove became a valley."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def zero_point_three():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 0)]
    Pn, Cello, Pad = 0, 1, 2

    # ---- groove: single voice, narrow range, pentatonic, constrained (bars 1-20)
    groove = [
        ('C4',H),('E4',H),('G4',W),('-',Q),('A4',Q),('G4',W+H),
        ('C4',H),('E4',H),('G4',H),('A4',Q+Q),('G4',W+H),
        ('C4',H),('-',Q),('E4',Q),('G4',W),('-',Q),('A4',Q),('G4',W+H),
        ('C4',W+H),('-',Q),('-',W),
    ]
    for note, dur in groove:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=8)

    # cello: barely there, the deep register
    for _ in range(20):
        tracks[Cello].note('C3', W, velocity=3)

    # pad: the room
    for _ in range(20):
        tracks[Pad].note('C4', W, velocity=2)

    # ---- widening: range expands, turns unexpected, more space (bars 21-44)
    widen = [
        ('C4',W),('E4',Q),('G4',Q),('A4',W+H),
        ('C5',H),('-',Q),('A4',Q),('G4',Q),('E4',H),('-',Q),
        ('D5',Q),('C5',Q),('A4',W+H),('-',W),
        ('G4',W),('A4',W),('C5',H),('-',Q),('D5',Q),('E5',W+H),
        ('C5',W+H),('-',W),('-',W),
        ('G4',W+H),('E4',W+H),('C4',W*2),
    ]
    for note, dur in widen:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=7)

    # cello grounds, growing slightly
    widen_cello = [
        ('C3',W*4),('G2',W*4),('F2',W*2),('E2',W*2),('D2',W*4),('C3',W*4),('G2',W*4),
    ]
    for note, dur in widen_cello:
        tracks[Cello].note(note, dur, velocity=4)

    for bn in ['C4','C4','C4','E4','E4','G4','C4','G4','C4','C4','C4','E4','G4','C4']:
        tracks[Pad].note(bn, W, velocity=3)

    # ---- valley: same theme, room to breathe, the voice with slack (bars 45-68)
    valley = [
        ('C4',W+H),('-',Q),
        ('E4',W+H),('-',Q),
        ('G4',W*2),('-',Q),
        ('A4',W),('-',W),
        ('G4',W+H),('-',Q),('-',W),
        ('C4',W+H),('-',Q),
        ('E4',W+H),('-',Q),
        ('G4',W+H),('-',Q),('-',Q),('-',Q),
        ('A4',W),('-',Q),('G4',Q),('-',Q),
        ('C5',W+H),('-',Q),('-',Q),('-',W),
        ('C4',W*2),('-',W),
        ('E4',W*2),('-',W),
        ('G4',W*3),
    ]
    for note, dur in valley:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=6)

    # cello holds the deep
    valley_cello = [
        ('C3',W*4),('-',W*2),('G2',W*4),('-',W*2),('E3',W*4),('C3',W*4),('G2',W*4),
    ]
    for note, dur in valley_cello:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=3)

    for bn in ['C4','G3','C4','E4','C4','E4','G3','C4','G4','C4','E4','C4']:
        tracks[Pad].note(bn, W, velocity=2)

    # ---- held note: the river still flows the same direction (bars 69-72)
    tracks[Pn].note('C4', W*4, velocity=5)
    tracks[Cello].note('C2', W*4, velocity=4)
    tracks[Pad].note('C4', W*4, velocity=2)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zero-point-three.mid")
    mc.compose(fn, tracks, tempo=65)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 65 bpm)")

if __name__ == "__main__":
    zero_point_three()
