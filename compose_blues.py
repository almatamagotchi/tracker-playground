#!/usr/bin/env python3
"""slow blues in C — sparse, smoky, 60bpm. piano + walking bass + brushes."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def blues():
    tracks = [
        MIDITrack(0, 0),  # piano — very sparse
        MIDITrack(1, 32),  # acoustic bass — walking
        MIDITrack(2, 0),   # snare (pitched) — brushes
    ]

    # 12-bar blues in C: C7 | F7 | C7 | C7 | F7 | F7 | C7 | C7 | G7 | F7 | C7 | G7
    # 4 choruses = 48 bars

    # blue notes: Eb, Bb, Gb
    C = ["C3","Eb3","E3","F3","G3","Bb3","C4","Eb4","E4","G4"]
    F = ["F3","Ab3","A3","Bb3","C4","Eb4","F4","Ab4","A4","C5"]
    G = ["G3","Bb3","B3","C4","D4","F4","G4","Bb4","B4","D5"]

    chorus = [
        ("C",4),("C",4),("C",4),("C",4),
        ("F",4),("F",4),("C",4),("C",4),
        ("G",4),("F",4),("C",4),("G",4),
    ]

    for chorus_num in range(4):
        vscale = 55 + chorus_num * 5  # slightly more present each chorus

        for bar_idx, (chord, beats) in enumerate(chorus):
            base = (chorus_num * 12 + bar_idx) * W
            notes = {"C": C, "F": F, "G": G}[chord]

            # piano: 2-3 notes per bar, lots of silence
            if chorus_num == 0:
                # first chorus — piano barely there, just a few notes
                if bar_idx in [0, 4, 8, 10]:
                    tracks[0].note(notes[3], Q*2, velocity=vscale-10)  # root
                    tracks[0].rest(Q*2)
                else:
                    tracks[0].rest(W)
            elif chorus_num == 1:
                # second chorus — more present, some blue notes
                if bar_idx % 2 == 0:
                    tracks[0].note(notes[1], Q, velocity=vscale)   # blue note
                    tracks[0].rest(Q)
                    tracks[0].note(notes[5], Q*2, velocity=vscale)  # higher
                else:
                    tracks[0].note(notes[2], Q*2, velocity=vscale-5)
                    tracks[0].rest(Q*2)
            elif chorus_num == 2:
                # third chorus — fuller, the hurt
                tracks[0].note(notes[4], Q, velocity=vscale+5)
                tracks[0].rest(Q)
                tracks[0].note(notes[0], Q, velocity=vscale-5)
                tracks[0].note(notes[6], Q, velocity=vscale-10)
                tracks[0].rest(Q)
            else:
                # last chorus — sparse again, fading
                if bar_idx in [0, 4, 8, 10]:
                    tracks[0].note(notes[2], Q*3, velocity=vscale-15)
                    tracks[0].rest(Q)
                elif bar_idx == 11:
                    tracks[0].note(notes[0], W*2, velocity=30)  # fade on C
                else:
                    tracks[0].rest(W)

            # bass — walking, stops sometimes
            bass_notes = [
                notes[0], notes[3], notes[4], notes[6],
                notes[4], notes[3], notes[0], notes[6],
            ]
            for bn in range(4):
                if chorus_num == 3 and bar_idx >= 10:
                    # last two bars — pedal on root, then fade
                    tracks[1].note(notes[0], Q*3, velocity=40 - (bar_idx-9)*5)
                    tracks[1].rest(Q)
                elif chorus_num == 0 and bar_idx in [3, 7]:
                    # rest the bass occasionally
                    tracks[1].rest(Q)
                    tracks[1].note(bass_notes[bn], Q, velocity=45)
                    tracks[1].rest(Q*2)
                else:
                    tracks[1].note(bass_notes[bn], Q, velocity=48)
                    tracks[1].rest(Q*3) if bn == 0 else None

            # snare — soft brushes, very light
            if bar_idx % 4 == 0:
                if chorus_num < 3:
                    tracks[2].note("C3", E, velocity=25)
                    tracks[2].rest(Q - E)
                    tracks[2].note("C3", E*2, velocity=18)
                    tracks[2].rest(Q + Q*2)
                    tracks[2].note("C3", E, velocity=22)
                    tracks[2].rest(Q - E)
                else:
                    # last chorus — lighter
                    tracks[2].note("C3", E, velocity=15)
                    tracks[2].rest(W - E)
            else:
                tracks[2].rest(W)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blues-in-c.mid")
    mc.compose(fn, tracks, tempo=58)

if __name__ == "__main__":
    blues()
