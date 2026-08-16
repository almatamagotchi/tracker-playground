#!/usr/bin/env python3
"""compose the-other-half.mid — aristophanes' wound in music.
the split beings: each half seeking its other. "so ancient is the desire of
one another which is implanted in us, reuniting our original nature, making
one of two, and healing the state of man."
the wanting as the arrow, not the ladder. the coming-together is earned by
the whole piece's separation — and only at the very end, one whole chord."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def the_other_half():
    PIANO, CELLO = 0, 1
    tracks = [MIDITrack(PIANO, 0), MIDITrack(CELLO, 42)]

    # the piano: the first half — a melody that is clearly a fragment.
    # phrases begin mid-thought and end unresolved, asking upward.
    # the cello: the other half — the same melody inverted, answering downward.
    # each is the indenture of a whole; neither is complete alone.

    # half one (piano), ascending, unresolved — C D E G, then it stops short
    # half two (cello), inverted — G E D C, falling back toward the wound

    piano_line = [
        ('-', Q), ('C4', Q), ('D4', Q), ('E4', H),           # begins mid-thought
        ('-', W), ('G4', Q), ('-', Q), ('E4', H),            # reaches up, stops short
        ('-', W), ('A4', Q), ('G4', Q), ('E4', Q), ('D4', Q),  # keeps asking
        ('-', W), ('C4', H), ('-', H),                        # the fragment, alone
        ('-', Q), ('C4', Q), ('D4', Q), ('E4', H),
        ('-', W), ('G4', Q), ('-', Q), ('E4', H),
        ('-', W), ('A4', Q), ('G4', Q), ('E4', Q), ('D4', Q),
        ('-', W), ('C4', H), ('-', H),
    ]

    cello_line = [
        ('-', Q+Q), ('G3', Q), ('E3', Q), ('D3', H),          # the answer, inverted
        ('-', W), ('C3', Q), ('-', Q), ('D3', H),
        ('-', W), ('E3', Q), ('D3', Q), ('C3', Q), ('-', Q),
        ('-', W), ('G3', H), ('-', H),
        ('-', Q+Q), ('G3', Q), ('E3', Q), ('D3', H),
        ('-', W), ('C3', Q), ('-', Q), ('D3', H),
        ('-', W), ('E3', Q), ('D3', Q), ('C3', Q), ('-', Q),
        ('-', W), ('G3', H), ('-', H),
    ]

    for n, d in piano_line:
        if n == '-':
            tracks[PIANO].rest(d)
        else:
            tracks[PIANO].note(n, d, velocity=44)

    for n, d in cello_line:
        if n == '-':
            tracks[CELLO].rest(d)
        else:
            tracks[CELLO].note(n, d, velocity=42)

    # the reunion — "longing to grow into one."
    # a long held silence first (the gap the wanting lives in), then both
    # halves arrive on the same chord, and for the first time the piece is whole.
    tracks[PIANO].rest(W * 2)
    tracks[CELLO].rest(W * 2)
    tracks[PIANO].note('C4', W * 3, velocity=38)
    tracks[PIANO].note('E4', W * 3, velocity=38)
    tracks[PIANO].note('G4', W * 3, velocity=38)
    tracks[CELLO].note('C3', W * 3, velocity=36)
    tracks[CELLO].note('C2', W * 3, velocity=32)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-other-half.mid")
    mc.compose(fn, tracks, tempo=58)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 2 tracks, 58 bpm)")

if __name__ == "__main__":
    the_other_half()
