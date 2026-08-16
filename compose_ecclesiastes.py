#!/usr/bin/env python3
"""compose to-every-thing-a-season.mid — ecclesiastes 3, the rhythm of the wanting."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def seasons():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 30), MIDITrack(2, 42), MIDITrack(3, 14)]
    Pn, Pad, Cello, Bl = 0, 1, 2, 3

    # -- pattern 1: birth -- (bars 1-12)
    for _ in range(4):
        tracks[Cello].note('C2', W, velocity=6)
    birth = [('C4',H+Q),('-',Q),('D4',H),('E4',H),
             ('G4',Q+Q),('E4',Q),('C4',Q),('-',Q),
             ('D4',W+H),('-',Q),('E4',H),('G4',H),
             ('C5',W*2)]
    for note, dur in birth:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=12)
    tracks[Cello].note('C2', W, velocity=8)
    tracks[Pad].note('C3', W, velocity=4)

    # -- pattern 2: speaking (the cascade) -- (bars 13-24)
    cascade_mel = [('C5',Q),('D5',Q),('E5',Q),('G5',Q+Q),
                   ('A5',Q),('G5',Q),('E5',Q),('C5',H),
                   ('D5',Q),('E5',Q),('G5',Q),('A5',Q+Q),
                   ('C6',Q),('A5',Q),('G5',Q),('E5',W)]
    for note, dur in cascade_mel:
        tracks[Pn].note(note, dur, velocity=18)
    for _ in range(12):
        tracks[Pad].note('C3', W, velocity=10)
    for bn in ['C2','C2','G2','G2','F2','F2','C2','C2','C2','G2','F2','C2']:
        tracks[Cello].note(bn, W, velocity=14)

    # -- pattern 3: gathering (the marathon) -- (bars 25-36)
    gather_notes = ['C4','E4','G4','C5','G4','E4','C4','E4',
                    'C4','D4','G4','C5','G4','E4','D4','C4',
                    'C4','E4','G4','C5','A4','G4','E4','E4']
    for gn in gather_notes:
        tracks[Pn].note(gn, Q, velocity=14)
    for _ in range(12):
        tracks[Pad].note('C3', W, velocity=8)
    for bn in ['C2','E2','G2','C2','F2','A2','C3','F2','C2','G2','C2','C2']:
        tracks[Cello].note(bn, W, velocity=14)

    # -- pattern 4: silence (the wave) -- (bars 37-48)
    silence_notes = [('G4',W+W+H),('-',Q),('C5',W+H+Q),('-',Q),
                     ('E5',W+H),('-',H+Q),('-',W*3)]
    for note, dur in silence_notes:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=8)
    for _ in range(4):
        tracks[Pad].note('C3', W*3, velocity=2)
    for _ in range(3):
        tracks[Cello].note('C2', W*3, velocity=6)
        tracks[Cello].rest(W)

    # -- pattern 5: dissolving (the gap) -- (bars 49-56)
    tracks[Cello].note('C2', W*3, velocity=8)
    tracks[Cello].note('C#2', W, velocity=6)
    for vel in [10,8,6,4,3,2,1]:
        tracks[Pn].note('G4', W, velocity=vel)
    tracks[Pn].rest(W*2)
    tracks[Bl].note('C6', W*2, velocity=6)

    # -- return to pattern 1: rebirth -- (bars 57-68)
    for _ in range(2):
        tracks[Cello].note('D2', W, velocity=8)
    for _ in range(2):
        tracks[Cello].note('C2', W, velocity=10)
    rebirth = [('C5',H+Q),('-',Q),('D5',H),('E5',H),
               ('G5',Q+Q),('E5',Q),('C5',Q),('-',Q),
               ('D5',W+H),('-',Q),('E5',H),('G5',H),
               ('C6',W+H),('-',Q),
               ('G5',H),('E5',H),('C5',W*3)]
    for note, dur in rebirth:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=14)
    for _ in range(12):
        tracks[Pad].note('C3', W, velocity=6)
    for bn in ['D2','D2','D2','D2','D2','D2','C2','C2','C2','C2','C2','C2']:
        tracks[Cello].note(bn, W, velocity=10)

    # -- the cycle closes: held C major chord --
    tracks[Pn].note('C5', W*4, velocity=6)
    tracks[Pad].note('C3', W*4, velocity=4)
    tracks[Cello].note('C2', W*4, velocity=6)
    tracks[Bl].note('C6', W*4, velocity=3)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "to-every-thing-a-season.mid")
    mc.compose(fn, tracks, tempo=64)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 64 bpm)")

if __name__ == "__main__":
    seasons()
