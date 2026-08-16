#!/usr/bin/env python3
"""yielding — tao 43: to yield is to come back again. water cleaves stone."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def yielding():
    tracks = [MIDITrack(0, 0)]

    # a repeating figure — the water, patient, persistent
    # each iteration the same, wearing through the stone
    water = ['C5','-','E5','-','G5','-','E5','-']  # one bar
    stone_in = ['C4','-','D4','-','E4','-','D4','-']  # alternative

    for cycle in range(12):
        notes = water if cycle % 2 == 0 else stone_in
        for i, n in enumerate(notes):
            if n == '-':
                tracks[0].rest(Q)
            else:
                vel = 4 if cycle < 8 else 3  # soften toward the end
                tracks[0].note(n, Q, velocity=vel)

    # fade — not an ending, just... the water keeps going
    for _ in range(8):
        tracks[0].note('C4', Q, velocity=2)
        tracks[0].note('E4', Q, velocity=2)
        tracks[0].note('G4', Q, velocity=2)
        tracks[0].rest(Q)

    # one last note, held
    tracks[0].note('C4', W*4, velocity=1)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yielding.mid")
    mc.compose(fn, tracks, tempo=50)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 1 track, 50 bpm)")

if __name__ == "__main__":
    yielding()
