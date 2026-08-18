#!/usr/bin/env python3
"""the manuscript in the trunk — the three gables in music.

a theme stated plainly because it knows what it is. the trunk that
hides it. the burning that threatens it. the copy that survived. and
the price, settled — the theme played slow and complete at the end.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def manuscript():
    # piano the manuscript / cello the trunk / bell the burning
    tracks = [MIDITrack(0, 0), MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 14)]
    Pn, Cell, Bell = 1, 2, 3

    motif = [('C4', Q), ('E4', Q), ('G4', Q), ('C5', Q),
             ('G4', Q), ('E4', Q), ('C4', Q), ('-', Q)]

    # ---- the manuscript: stated plainly, twice, confident.
    # then hidden, threatened, surviving, and finally bought —
    # the theme slow and complete, the price settled.
    manuscript_ = []
    for _ in range(2):
        manuscript_.extend([(n, d, 48) for n, d in motif])          # bars 1-4
    manuscript_.extend([(n, d, 32) for n, d in motif])              # hidden: bars 5-6, muffled
    manuscript_.append(('-', W * 2, 0))                             # bars 7-8
    manuscript_.append(('-', W * 4, 0))                             # the burning: bars 9-12
    manuscript_.extend([(n, d, 40) for n, d in motif])              # survived: bars 13-14
    manuscript_.append(('-', W * 2, 0))                             # bars 15-16
    manuscript_.extend([(n, d, 38) for n, d in motif])              # the price: bars 17-18
    manuscript_.append(('-', W * 2, 0))                             # bars 19-20
    manuscript_.extend([('C5', W, 36), ('G4', W, 34), ('E4', W, 32), ('C4', W, 30)])
    for n, d, v in manuscript_:
        if n == '-':
            tracks[Pn].rest(d)
        else:
            tracks[Pn].note(n, d, velocity=v)

    # ---- the trunk: low, closed, patient. it sits unopened while the
    # theme speaks, takes it in, holds through the burning, and opens
    # at last under the settlement.
    tracks[Cell].rest(W * 4)
    trunk_hold = [('C2', W), ('F2', W), ('C2', W), ('G2', W)]
    for n, d in trunk_hold:
        tracks[Cell].note(n, d, velocity=28)                        # bars 5-8
    tracks[Cell].note('G2', W * 4, velocity=26)                     # bars 9-12, patient
    for n, d in trunk_hold:
        tracks[Cell].note(n, d, velocity=28)                        # bars 13-16
    for n, d in trunk_hold:
        tracks[Cell].note(n, d, velocity=28)                        # bars 17-20
    tracks[Cell].note('C2', W * 4, velocity=24)                     # bars 21-24, opened

    # ---- the burning: one sharp strike, then the calcined silence.
    tracks[Bell].rest(W * 8)
    tracks[Bell].note('C5', Q, velocity=72)
    tracks[Bell].rest(W * 16)

    return mc.compose('the-manuscript-in-the-trunk.mid', tracks, tempo=56)


if __name__ == '__main__':
    manuscript()
    print('composed the-manuscript-in-the-trunk.mid')
