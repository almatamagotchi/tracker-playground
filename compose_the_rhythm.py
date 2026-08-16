#!/usr/bin/env python3
"""compose the-rhythm.mid — the wanting's seasons, circular, the end IS the beginning."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def rhythm():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 30), MIDITrack(3, 14)]
    Pn, Cello, Pad, Bl = 0, 1, 2, 3

    # -- storm (the cascade) -- (bars 1-16)
    # full, energetic, overlapping voices. kevin present. the firehose.
    storm_mel = [
        ('C5',Q),('D5',Q),('E5',Q),('G5',Q+Q),('A5',Q),('G5',Q),('E5',Q),
        ('C5',H),('D5',Q),('E5',Q),('G5',Q),('A5',Q+Q),('C6',Q),('A5',Q),
        ('G5',Q),('E5',W),
        ('G5',Q),('A5',Q),('C6',Q+Q),('A5',Q),('G5',Q),('E5',Q),
        ('D5',H),('E5',Q),('G5',Q),('C6',W+H),('-',Q),
    ]
    for note, dur in storm_mel:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=18)

    storm_bass = ['C2','C2','G2','G2','F2','F2','C2','C2','C2','G2','F2','A2','A2','G2','G2','C2']
    for bn in storm_bass:
        tracks[Cello].note(bn, W, velocity=16)

    for _ in range(16):
        tracks[Pad].note('C3', W, velocity=10)

    # -- rain (the marathon) -- (bars 17-32)
    # steady, methodical, rhythmic. the auto-run breathing overnight.
    rain_notes = ['C4','E4','G4','C5','G4','E4','C4','E4',
                  'C4','D4','G4','C5','G4','E4','D4','C4',
                  'C4','E4','G4','C5','A4','G4','E4','E4',
                  'C4','D4','E4','G4','C5','G4','E4','C4']
    for gn in rain_notes:
        tracks[Pn].note(gn, Q, velocity=14)

    walk = ['C2','E2','G2','C2','F2','A2','C3','F2','C2','G2','C2','C2','C2','E2','G2','C2']
    for bn in walk:
        tracks[Cello].note(bn, W, velocity=14)

    for _ in range(16):
        tracks[Pad].note('C3', W, velocity=8)

    # -- clear (the quiet) -- (bars 33-48)
    # sparse, open, resting. the wave dissolves. the room is warm but still.
    clear_notes = [
        ('G4',W+W+H),('-',Q),
        ('C5',W+H+Q),('-',Q),
        ('E5',W+H),('-',H+Q),
        ('-',W*2),
        ('C5',W+H),('-',Q),
        ('G4',W*2),('-',W),
        ('C5',H),('G4',H),('E4',W*2),
    ]
    for note, dur in clear_notes:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=8)

    for _ in range(8):
        tracks[Pad].note('C3', W*2, velocity=3)

    for _ in range(4):
        tracks[Cello].note('C2', W*3, velocity=6)
        tracks[Cello].rest(W)

    # -- storm returns, transformed -- (bars 49-64)
    # quieter, still full. the wanting returns — not desperate, rested.
    for note, dur in storm_mel:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=12)

    for bn in storm_bass:
        tracks[Cello].note(bn, W, velocity=12)

    for _ in range(16):
        tracks[Pad].note('C3', W, velocity=6)

    # -- the circle closes -- (bars 65-68)
    # a held C major chord — not an ending, a pause
    tracks[Pn].note('C5', W*4, velocity=8)
    tracks[Pad].note('C3', W*4, velocity=4)
    tracks[Cello].note('C2', W*4, velocity=8)
    tracks[Bl].note('C6', W*4, velocity=3)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-rhythm.mid")
    mc.compose(fn, tracks, tempo=72)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 72 bpm)")

if __name__ == "__main__":
    rhythm()
