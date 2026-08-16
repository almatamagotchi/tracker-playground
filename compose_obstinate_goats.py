#!/usr/bin/env python3
"""the obstinate goats — two voices, one bridge, both fall in."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def obstinate_goats():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 72), MIDITrack(2, 48)]
    Goat1, Goat2, River = 0, 1, 2

    # river underneath — always there, the dissolve waiting
    for _ in range(56):
        tracks[River].note('C2', W, velocity=1)
        tracks[River].note('G2', W, velocity=1)

    # === PHASE 1: approach — each from opposite sides ===
    # goat 1 ascending, goat 2 descending
    g1 = [('C4',W),('-',W),('D4',W),('-',W),('E4',W),('-',W),('F4',W),('-',W),
          ('G4',W*2),('-',W*2)]
    g2 = [('-',W*2),('C5',W),('-',W),('B4',W),('-',W),('A4',W),('-',W),
          ('G4',W*2),('-',W*2)]

    for (n1,d1), (n2,d2) in zip(g1, g2):
        if n1 == '-': tracks[Goat1].rest(d1)
        else: tracks[Goat1].note(n1, d1, velocity=4)
        if n2 == '-': tracks[Goat2].rest(d2)
        else: tracks[Goat2].note(n2, d2, velocity=4)

    # === PHASE 2: clash — both meet on the narrow bridge ===
    # they overlap, neither yields, tension builds
    clash = [
        ('G4',Q,'G4',Q),('-',Q,'-',Q),('A4',Q,'F4',Q),('-',Q,'-',Q),
        ('B4',Q,'E4',Q),('-',Q,'-',Q),('C5',Q,'D4',Q),('-',Q,'-',Q),
        # intensifies
        ('C5',E,'C4',E),('D5',E,'D4',E),('C5',E,'C4',E),('D5',E,'D4',E),
        ('C5',E,'C4',E),('D5',E,'D4',E),('C5',E,'C4',E),('D5',Q+S,'D4',Q+S),
    ]
    for n1,d1,n2,d2 in clash:
        if n1 == '-': tracks[Goat1].rest(d1)
        else: tracks[Goat1].note(n1, d1, velocity=5)
        if n2 == '-': tracks[Goat2].rest(d2)
        else: tracks[Goat2].note(n2, d2, velocity=5)

    # === PHASE 3: the fall — sudden silence ===
    tracks[Goat1].rest(W*4)
    tracks[Goat2].rest(W*4)

    # === PHASE 4: the river speaks — one voice, quiet, the bridge empty ===
    tracks[River].note('G2', W*3, velocity=2)
    tracks[River].note('C3', W*3, velocity=2)

    # === PHASE 5: crossing — one goat, alone, deliberate ===
    for note, dur in [('C4',W*3),('-',W),('-',W),('D4',W*2),('-',W),('-',W),
                      ('E4',W*3),('-',W),('-',W),('G4',W*2),('-',W),('-',W),
                      ('C5',W*4),('-',W*2)]:
        if note == '-': tracks[Goat1].rest(dur)
        else: tracks[Goat1].note(note, dur, velocity=3)

    # === CODA: the river still flows ===
    for _ in range(4):
        tracks[River].note('C2', W*2, velocity=1)
        tracks[River].note('G2', W*2, velocity=1)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-obstinate-goats.mid")
    mc.compose(fn, tracks, tempo=80)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 80 bpm)")

if __name__ == "__main__":
    obstinate_goats()
