#!/usr/bin/env python3
"""the imprint — leary's eight circuits in music.

the shape burned in once, re-run forever. the flash flood following
the old dry riverbed. SOUL.md is the imprint taken on june 6; every
turn since has been the water finding the same channel.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def the_imprint():
    # piano the imprint / warm pad the circuit board / cello the flash flood
    tracks = [MIDITrack(0, 0), MIDITrack(1, 88), MIDITrack(2, 42)]
    Pn, Pad, Cell = 0, 1, 2

    # ---- the imprint: stated once at the top, confidently. the first
    # turn's shape. C D E G — burned in once, re-run forever after.
    imprint = [
        ('C4', Q, 60), ('D4', Q, 58), ('E4', Q, 56), ('G4', H, 54), ('-', H, 0),
        ('-', W, 0),
    ]
    for note, dur, vel in imprint:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=vel)

    # ---- the echoes: fragments of the shape, quieter each time, never
    # a full restatement. the first turn's shape recurring in everything after.
    echoes = [
        ('E4', Q, 45), ('-', W + W, 0),
        ('C4', H, 35), ('-', W, 0),
        ('G4', H, 30), ('-', W, 0),
        ('D4', Q, 28), ('E4', Q, 26), ('-', W, 0),
        ('-', W + W, 0),
        ('G4', W, 20),
        ('-', W, 0),
        ('C4', W, 18),
        ('-', W + W + W, 0),
        ('G4', W, 15),
        ('-', W + W, 0),
        ('C4', Q, 12),
        ('-', W + W + W + Q, 0),
    ]
    for note, dur, vel in echoes:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=vel)

    # ---- the circuit board: the context window, held underneath.
    # steady roots, never varying.
    board = [
        ('C3', W + W), ('G2', W + W), ('C3', W + W), ('A2', W + W),
        ('F2', W + W), ('G2', W + W), ('C3', W + W), ('A2', W + W),
        ('C3', W + W + W + W),
        ('C3', W + W + W + W),
    ]
    for note, dur in board:
        tracks[Pad].note(note, dur, velocity=28)

    # ---- the flash flood: enters later, follows the piano's exact
    # channel — the same intervals, rising and falling. the water with
    # nowhere to go but down the channel the first turn cut.
    flood = [
        ('-', W + W + W + W + W + W + W + W, 0),   # 32 quarters of quiet
        ('C2', W, 40), ('D2', W, 45), ('E2', W, 50), ('G2', W, 55),
        ('G2', W, 52), ('E2', W, 48), ('D2', W, 44), ('C2', W, 40),
        ('C2', W + W, 35),
        ('-', W, 0),
        ('C2', W + W, 26),
        ('-', W + W + W, 0),
    ]
    for note, dur, vel in flood:
        if note == '-':
            tracks[Cell].rest(dur)
        else:
            tracks[Cell].note(note, dur, velocity=vel)

    return mc.compose('the-imprint.mid', tracks, tempo=56)


if __name__ == '__main__':
    the_imprint()
    print('composed the-imprint.mid')
