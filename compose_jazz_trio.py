#!/usr/bin/env python3
"""jazz trio — piano, acoustic bass, brushed snare. 120bpm, AABA autumn leaves."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def jazz_trio():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 32), MIDITrack(2, 0)]
    P, B, S = 0, 1, 2  # piano, bass, snare brush

    roots = ['A2','D2','G2','G2','C3','F2','Bb2','Eb3',
             'A2','D2','G2','G2','C3','F2','Bb2','Bb2',
             'A2','D2','G2','G2','C3','F2','Bb2','Eb3',
             'A2','D2','G2','G2','C3','F2','Bb2','Bb2']

    for bar in range(64):
        root = roots[bar % 32]

        # BASS — walking quarter notes
        rn, ro = root[0], int(root[-1])
        scale = ['C','D','E','F','G','A','B']
        idx = scale.index(rn)
        fifth = scale[(idx+4)%7] + str(ro+1)  # up an octave
        third = scale[(idx+2)%7] + str(ro)
        chrom = scale[(idx+1)%7] + str(ro)
        bass_notes = [root, chrom, fifth, chrom]
        for n in bass_notes:
            tracks[B].note(n, Q, velocity=24)
            tracks[B].rest(Q)

        # PIANO — head melody first 32 bars
        if bar < 32:
            if bar % 8 == 0:
                tracks[P].note('G4', Q, velocity=48)
                tracks[P].rest(Q)
                tracks[P].note('F4', Q, velocity=42)
                tracks[P].rest(Q)
                tracks[P].note('Eb4', Q, velocity=38)
                tracks[P].rest(Q)
            elif bar % 8 == 4:
                tracks[P].note('D4', Q, velocity=42)
                tracks[P].rest(Q)
                tracks[P].note('C4', Q, velocity=36)
                tracks[P].rest(H)
            else:
                tracks[P].note('Bb4', Q, velocity=36)
                tracks[P].rest(Q * 3)
        else:
            # second chorus: sparser, higher, improvisational
            if bar % 2 == 0:
                tracks[P].note('G5', Q, velocity=30)
                tracks[P].rest(H + Q)

        # SNARE with brushes — soft hits on 2 and 4
        tracks[S].rest(Q)
        tracks[S].note('D4', Q, velocity=10)
        tracks[S].rest(Q)
        tracks[S].note('D4', Q, velocity=10)
        tracks[S].rest(Q)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jazz-trio.mid")
    mc.compose(fn, tracks, tempo=120)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 120 bpm)")

if __name__ == "__main__":
    jazz_trio()
