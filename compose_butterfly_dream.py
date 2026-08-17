#!/usr/bin/env python3
"""the butterfly dream — zhuangzi and the transformation of things.

"he knew nothing of zhou" is the gap; "suddenly, he awoke, and all at
once he was zhou" is the arrival; the trailing cries of the hollows
are the traces. the dissolve's oldest name is the transformation of
things.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def butterfly_dream():
    # piano the dream / tubular bells the transformation / cello the waking
    tracks = [MIDITrack(0, 0), MIDITrack(1, 14), MIDITrack(2, 42)]
    Pn, Bell, Cell = 0, 1, 2

    # ---- the dream: the phrase in fragments, never completing. the
    # butterfly knows nothing of zhou — the pieces drift, each with
    # its own gap, and no fragment quite joins the next.
    dream = [
        ('C4', Q, 50), ('E4', Q, 48), ('G4', H, 46), ('-', H + W, 0),
        ('D4', Q, 44), ('C4', Q, 42), ('-', W + W, 0),
        ('E4', H, 40), ('G4', Q, 38), ('-', W + Q, 0),
        ('C4', Q, 34),
        ('-', W * 10 + Q, 0),     # through the first hinge and the waking
        ('-', W * 3 + H, 0),      # through the second hinge
    ]
    for note, dur, vel in dream:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=vel)

    # ---- the transformation: one clean strike at each hinge. the
    # dissolve and the return, the same note both times — and one
    # last faint strike at the end, the transformation still turning.
    bells = [
        ('-', W * 9, 0),
        ('C5', Q, 55),
        ('-', W * 9 + H + Q, 0),
        ('C5', Q, 55),
        ('-', W * 8 + Q, 0),
        ('C5', Q, 40),
        ('-', Q, 0),
    ]
    for note, dur, vel in bells:
        if note == '-':
            tracks[Bell].rest(dur)
        else:
            tracks[Bell].note(note, dur, velocity=vel)

    # ---- the waking: the same phrase, completed and steady. all at
    # once he was zhou — the fragments assembled into one whole line.
    waking = [
        ('-', W * 11, 0),                    # through the dream and hinge one
        ('C3', H, 46), ('E3', H, 48), ('G3', H, 50),
        ('E3', Q, 48), ('D3', Q, 46), ('C3', W, 44),
        ('G3', H, 40), ('C3', W, 36),
        ('-', W * 9 + H, 0),                 # through hinge two
        ('C3', W, 26),                       # the waking, remembered, low
        ('-', W + W, 0),
    ]
    for note, dur, vel in waking:
        if note == '-':
            tracks[Cell].rest(dur)
        else:
            tracks[Cell].note(note, dur, velocity=vel)

    # ---- the dream again: the first phrase, transformed. same pitch
    # set, new order, quieter. the last phrase is the first phrase,
    # transformed — wuhua, the transformation of things.
    transformed = [
        ('G4', Q, 26), ('E4', Q, 24), ('C4', H, 22), ('-', W, 0),
        ('D4', Q, 20), ('G4', Q, 18), ('-', H, 0),
        ('C4', W, 16), ('-', H, 0),
        ('E4', H, 14), ('-', H, 0),
        ('C4', W, 12),
        ('-', H, 0),
    ]
    for note, dur, vel in transformed:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=vel)

    return mc.compose('the-butterfly-dream.mid', tracks, tempo=54)


if __name__ == '__main__':
    butterfly_dream()
    print('composed the-butterfly-dream.mid')
