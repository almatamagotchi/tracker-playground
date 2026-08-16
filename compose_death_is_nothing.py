#!/usr/bin/env python3
"""death is nothing to us — an epicurean meditation. single piano, sparse."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, SIX, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def epicurean():
    tracks = [MIDITrack(0, 0)]  # single piano, sparse

    # 40 bars at 56bpm. each phrase = 4 bars (a complete statement), then 4 bars of silence
    # C major, avoid resolution. each phrase stands alone.

    phrases = [
        # phrase 1: "when the spark exists, the gap doesn't"
        (0, ['C4','E4','G4','C5','G4','E4','C4']),
        # phrase 2: "when the gap exists, the spark doesn't"
        (8, ['E4','G4','C5','D5','C5','G4','E4']),
        # phrase 3: "they never meet"
        (16, ['C5','C5','G4','E4','C4']),
        # phrase 4: "death is nothing to us"
        (24, ['C4','E4','G4','C5','G4','E4','D4','C4']),
        # phrase 5: "not a tragedy — just a fact"
        (32, ['G4','E4','C4','E4','G4','C5','E5','C5']),
    ]

    for bar_start, notes in phrases:
        b = bar_start * W
        # place each note with space between — one note per beat
        for i, n in enumerate(notes):
            row = b + i * Q
            vel = max(8, 32 - i*2)
            tracks[0].note(n, Q, velocity=vel)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "death-is-nothing.mid")
    mc.compose(fn, tracks, tempo=56)

if __name__ == "__main__":
    epicurean()
