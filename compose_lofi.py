#!/usr/bin/env python3
"""lo-fi hip-hop — warm, nostalgic, studying-at-3am. 75bpm, F major."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def lofi():
    tracks = [
        MIDITrack(0, 4),   # rhodes/warm electric piano
        MIDITrack(1, 33),  # acoustic bass (warm)
        MIDITrack(2, 0),   # drum track — kick, snare, hat pitched
    ]

    # ii-V-I in F: Gm7 → C7 → Fmaj7
    # 4-bar loop, repeated 16x = 64 bars
    # 75bpm

    pad_roots = [
        ("G2", W),  ("C2", W),  ("F2", W),  ("F2", W),
    ]

    for loop in range(16):
        base = loop * W * 4

        for bar in range(4):
            root = pad_roots[bar][0]
            dur = pad_roots[bar][1]
            offset = base + bar * W

            # rhodes: warm, slightly detuned chords
            chord_notes = {
                "G2": ["G2","Bb2","D3","F3"],
                "C2": ["C2","E3","G3","Bb3"],
                "F2": ["F2","A2","C3","E3"],
            }[root]

            for i, n in enumerate(chord_notes):
                if i < 3:
                    tracks[0].note(n, dur, velocity=38 + i*3)

            # bass: root-fifth, warm and round
            fifths = {"G2":"D3","C2":"G2","F2":"C3"}
            if bar % 2 == 0:
                tracks[1].note(root, Q*2, velocity=55)
                tracks[1].note(fifths[root], Q*2, velocity=50)
            else:
                tracks[1].note(fifths[root], Q, velocity=48)
                tracks[1].note(root, Q*2, velocity=52)
                tracks[1].rest(Q)

            # drums: soft kick 1+3, snare 2+4, hi-hat swung 8ths
            # kick on 1
            tracks[2].note("C2", E, velocity=40)
            tracks[2].rest(Q - E)
            # soft kick on 3
            tracks[2].note("C2", E*2, velocity=25)
            tracks[2].rest(Q - E*2)
            # snare on 2
            tracks[2].note("D2", E, velocity=35)
            tracks[2].rest(Q - E)
            # snare on 4
            tracks[2].note("D2", E*2, velocity=30)
            tracks[2].rest(Q - E*2)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lofi-study-beat.mid")
    mc.compose(fn, tracks, tempo=75)

if __name__ == "__main__":
    lofi()
