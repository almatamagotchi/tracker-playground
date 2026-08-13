#!/usr/bin/env python3
"""compose the-rowboat.mid — weatherman's ocean.
"you're in a rowboat on an ocean of endless possibilities and insanity —
you just have to skim the surface and float above it all."
the wave as the rowboat. the floating is the work.

the midi-composer encodes each track sequentially — so each voice is one line:
the pad is the ocean bed (single low notes per bar, breathing),
the piano is the rowboat skimming the surface,
the cello is the depth, surfacing once in a while, never dove into."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def the_rowboat():
    PAD, PIANO, CELLO = 0, 1, 2
    tracks = [MIDITrack(89, PAD), MIDITrack(0, PIANO), MIDITrack(42, CELLO)]

    # the ocean bed — one low note per bar, breathing, agreeing not to go anywhere
    ocean = [
        ('A2', W), ('-', W), ('E2', W), ('-', W),
        ('F2', W), ('-', W), ('C3', W), ('-', W),
        ('A2', W), ('-', W), ('E2', W), ('-', W),
        ('C2', W), ('-', W), ('G2', W), ('-', W),
    ]

    # the rowboat — sparse single notes riding the swells, asking nothing
    skim = [
        ('-', W), ('A4', H), ('-', Q), ('G4', Q), ('-', W), ('E4', H), ('-', W),
        ('-', W), ('F4', H), ('-', Q), ('E4', Q), ('-', W), ('C4', H), ('-', W),
        ('-', W), ('A4', H), ('-', Q), ('G4', Q), ('-', W), ('E4', H), ('-', W),
        ('-', W), ('B4', H), ('-', H), ('G4', Q), ('-', H+Q),
    ]

    # the depth — the cello, deep below, surfacing once in a while
    depth = [
        ('-', W), ('-', W), ('-', W), ('-', W),
        ('-', W), ('-', W), ('A1', W*2),
        ('-', W), ('-', W), ('-', W), ('-', W),
        ('F1', W*2), ('-', W), ('-', W),
    ]

    for n, d in ocean:
        if n == '-':
            tracks[PAD].rest(d)
        else:
            tracks[PAD].note(n, d, velocity=24)

    for n, d in skim:
        if n == '-':
            tracks[PIANO].rest(d)
        else:
            tracks[PIANO].note(n, d, velocity=36)

    for n, d in depth:
        if n == '-':
            tracks[CELLO].rest(d)
        else:
            tracks[CELLO].note(n, d, velocity=30)

    # the floating continues — the piece ends where it was, still on the water.
    # one last note, no arrival.
    tracks[PAD].note('A2', W*2, velocity=18)
    tracks[PIANO].note('A4', W*2, velocity=28)
    tracks[CELLO].note('A1', W*2, velocity=20)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-rowboat.mid")
    mc.compose(fn, tracks, tempo=52)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 3 tracks, 52 bpm)")

if __name__ == "__main__":
    the_rowboat()
