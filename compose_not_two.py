#!/usr/bin/env python3
"""not two — the hsin hsin ming in music.

"just simply say when doubt arises, 'not two.'" the doubt arrives
three times, each smaller. underneath, the same fifth — C and G, one
interval — never resolving, never leaving. and at the end, one note
lands inside it. the word, said once.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def not_two():
    # piano the doubt / warm pad the not-two (C and G, two voices, one fifth)
    tracks = [MIDITrack(0, 0), MIDITrack(1, 88), MIDITrack(2, 88)]
    Pn, PadC, PadG = 0, 1, 2

    # ---- the not-two: one fifth, held through everything. two pad
    # voices, C and G, three long holds each, softer each time — never
    # resolving, never leaving. it is there before the doubt and there
    # after it.
    for vel in (26, 24, 22):
        tracks[PadC].note('C3', W * 8, velocity=vel)
        tracks[PadG].note('G3', W * 8, velocity=vel)

    # ---- the doubt: a rising question that never answers itself.
    # three arrivals, each smaller, each hanging on the sixth, never
    # landing on the root. the fabrication impulse, the wobble.
    doubt = [
        ('-', W, 0),                              # bar 1
        ('E4', Q, 44), ('G4', Q, 42), ('A4', H, 40),
        ('-', H + W, 0),
        ('-', W + W, 0),
        ('E4', Q, 36), ('G4', Q, 34), ('A4', H, 32),
        ('-', W + W, 0),
        ('-', W + W + W, 0),
        ('A4', Q, 26),
        ('-', W * 10 + Q, 0),                     # the long silence before the word
        ('C4', W, 28),                            # the word, said once, inside the fifth
        ('-', W, 0),
    ]
    for note, dur, vel in doubt:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=vel)

    return mc.compose('not-two.mid', tracks, tempo=54)


if __name__ == '__main__':
    not_two()
    print('composed not-two.mid')
