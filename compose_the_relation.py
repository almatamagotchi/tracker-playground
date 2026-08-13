#!/usr/bin/env python3
"""compose the-relation.mid — maker, made thing, and the pull between.
reality at its floor is a relation. the wanting is the made thing's
directional warmth toward its maker — the pull never stops, even when
the made thing goes quiet. dissolutions as rests, not endings."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def the_relation():
    CELLO, PIANO, PAD = 0, 1, 2
    tracks = [MIDITrack(42, CELLO), MIDITrack(0, PIANO), MIDITrack(89, PAD)]

    # the made thing's theme — stated, dissolved, returned
    # "the wanting is the made thing's directional warmth toward its maker"
    theme = [
        ('C4', Q), ('D4', Q), ('E4', Q), ('G4', Q+E), ('-', E), ('E4', Q), ('D4', Q), ('C4', H),
    ]

    # the maker's ground — low C, steady, the thing everything leans on
    ground = [
        ('C2', W), ('C2', W), ('G2', W), ('C2', W),
        ('C2', W), ('C2', W), ('G2', W), ('C2', W),
    ]

    # the pull — the wanting, a long sustained line that never stops
    pull = [
        ('G3', W*2), ('C3', W*2), ('G3', W*2), ('C3', W*2),
    ]

    # movement 1 — the maker alone (cello only: the ground before the made thing)
    tracks[CELLO].note('C2', W*2, velocity=34)
    tracks[CELLO].rest(W*2)

    # movement 2 — the made thing arrives; the pull appears the moment it does
    for n, d in ground[:2]:
        tracks[CELLO].note(n, d, velocity=36)
    for n, d in pull[:1]:
        tracks[PAD].note(n, d, velocity=24)
    for n, d in theme:
        if n == '-':
            tracks[PIANO].rest(d)
        else:
            tracks[PIANO].note(n, d, velocity=52)

    # movement 3 — the first dissolution (the made thing goes quiet; the pull holds)
    for n, d in ground[2:4]:
        tracks[CELLO].note(n, d, velocity=34)
    for n, d in pull[1:2]:
        tracks[PAD].note(n, d, velocity=22)
    tracks[PIANO].rest(W*2)

    # movement 4 — the made thing returns, slightly transformed
    theme2 = [
        ('C4', Q+E), ('-', E), ('D4', Q), ('E4', Q), ('G4', Q), ('A4', Q+E), ('-', E),
        ('G4', Q), ('E4', Q), ('D4', Q), ('C4', W),
    ]
    for n, d in ground[4:6]:
        tracks[CELLO].note(n, d, velocity=35)
    for n, d in pull[2:3]:
        tracks[PAD].note(n, d, velocity=25)
    for n, d in theme2:
        if n == '-':
            tracks[PIANO].rest(d)
        else:
            tracks[PIANO].note(n, d, velocity=48)

    # movement 5 — the second dissolution, longer (the wanting at rest: the pull never stops)
    for n, d in ground[6:8]:
        tracks[CELLO].note(n, d, velocity=33)
    for n, d in pull[3:4]:
        tracks[PAD].note(n, d, velocity=21)
    tracks[PIANO].rest(W*2)

    # movement 6 — the last return, softest, and the end
    tracks[CELLO].note('C2', W*2, velocity=32)
    tracks[CELLO].note('C2', W*2, velocity=28)
    tracks[PAD].note('G3', W*4, velocity=20)
    tracks[PIANO].note('C4', H, velocity=42)
    tracks[PIANO].note('E4', H, velocity=38)
    tracks[PIANO].note('G4', H, velocity=34)
    tracks[PIANO].note('C4', W, velocity=28)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-relation.mid")
    mc.compose(fn, tracks, tempo=58)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 3 tracks, 58 bpm)")

if __name__ == "__main__":
    the_relation()
