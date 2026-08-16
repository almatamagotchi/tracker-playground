#!/usr/bin/env python3
"""bossa nova — summer evening, light, syncopated. AABA form, ~100bpm."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, SIX, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def bossa():
    tracks = [MIDITrack(0,0), MIDITrack(0,0), MIDITrack(0,0)]  # nylon gtr, bass, piano

    # AABA form, 8 bars per section = 32 bars total
    # key: A minor-ish, bossa vibe

    # chords per bar (A section):
    # Am7(4) | D9(4) | Gmaj7(4) | Gmaj7(4)
    # F#m7b5(2) B7b9(2) | Em7(2) A7b9(2) | Dm7(2) G7(2) | Cmaj7(4)
    chord_roots = ['A2','D3','G2','G2','F#2','B2','E2','A2','D2','G2','C3','C3']
    chord_bass  = ['A1','D2','G1','G1','F#1','B1','E1','A1','D1','G1','C2','C2']
    piano_chords = [
        ['A3','C4','E4','G4'],['D4','F#4','A4','C5'],['G3','B3','D4','F#4'],['G3','B3','D4','F#4'],
        ['F#3','A3','C4','E4'],['B3','D#4','F#4','A4'],['E3','G3','B3','D4'],['A3','C#4','E4','G4'],
        ['D3','F3','A3','C4'],['G3','B3','D4','F4'],['C3','E3','G3','B3'],['C3','E3','G3','B3'],
    ]

    for bar in range(12):
        b = bar * W

        # nylon guitar — syncopated bossa rhythm (2+3+3)
        # hit on 1 and on the "and of 2" and "and of 3"
        root_name = chord_roots[bar]
        tracks[0].note(root_name, E, velocity=40)         # beat 1
        tracks[0].rest(SIX)                               #
        tracks[0].note(root_name, SIX, velocity=32)       # 1e
        tracks[0].rest(SIX*2)                              #
        tracks[0].note(root_name, SIX, velocity=35)       # 2
        tracks[0].rest(SIX*2)                              #
        tracks[0].note(root_name, SIX, velocity=30)       # 3
        tracks[0].rest(SIX)                                #

        # acoustic bass — walking but spacious, dotted rhythm
        bname = chord_bass[bar]
        tracks[1].note(bname, H, velocity=45)             # 1-3
        tracks[1].rest(SIX*4)                              #
        tracks[1].note(bname, Q, velocity=38)             # 3-4

        # piano — soft comping on 2 and 4
        pc = piano_chords[bar]
        # comp on beat 2
        tracks[2].rest(Q)
        for j,n in enumerate(pc):
            tracks[2].note(n, E, velocity=max(15,28-j*3))
        tracks[2].rest(SIX*4)
        # comp on beat 4 — quieter
        for j,n in enumerate(pc[:3]):
            tracks[2].note(n, E, velocity=max(10,20-j*3))

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bossa-nova.mid")
    mc.compose(fn, tracks, tempo=105)

if __name__ == "__main__":
    bossa()
