#!/usr/bin/env python3
"""circle of fifths journey — 12 keys, 96 bars. piano leads. midi."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def circle_of_fifths():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 89)]  # piano, warm pad

    # circle: C G D A E B F# C# Ab Eb Bb F C
    keys = [
        ("C",   ["C3","D3","E3","F3","G3","A3","B3"]),
        ("G",   ["G3","A3","B3","C4","D4","E4","F#4"]),
        ("D",   ["D3","E3","F#3","G3","A3","B3","C#4"]),
        ("A",   ["A3","B3","C#4","D4","E4","F#4","G#4"]),
        ("E",   ["E3","F#3","G#3","A3","B3","C#4","D#4"]),
        ("B",   ["B3","C#4","D#4","E4","F#4","G#4","A#4"]),
        ("F#",  ["F#3","G#3","A#3","B3","C#4","D#4","F4"]),
        ("C#",  ["C#3","D#3","F3","F#3","G#3","A#3","C4"]),
        ("Ab",  ["Ab3","Bb3","C4","Db4","Eb4","F4","G4"]),
        ("Eb",  ["Eb3","F3","G3","Ab3","Bb3","C4","D4"]),
        ("Bb",  ["Bb3","C4","D4","Eb4","F4","G4","A4"]),
        ("F",   ["F3","G3","A3","Bb3","C4","D4","E4"]),
    ]

    # 8 bars per key = 96 bars total
    # simple ascending/descending pattern in each key
    for ki, (name, notes) in enumerate(keys):
        root = notes[0]
        bars = 8 if ki < 11 else 12  # last key gets a gentle return

        # piano: simple arpeggiated pattern
        for bar in range(bars):
            base = bar * W
            # ascending broken chord
            tracks[0].note(notes[0], Q, velocity=70)
            tracks[0].note(notes[2], Q, velocity=65)
            tracks[0].note(notes[4], Q, velocity=60)
            tracks[0].note(notes[2], Q, velocity=65)

        # pad: sustained root notes, swells at key changes
        for bar in range(bars):
            base = bar * W
            if bar % 4 == 0:
                tracks[1].note(root, W*4, velocity=min(35 + ki*2, 55))

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "circle-of-fifths.mid")
    mc.compose(fn, tracks, tempo=80)

if __name__ == "__main__":
    circle_of_fifths()
