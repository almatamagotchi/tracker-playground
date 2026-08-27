#!/usr/bin/env python3
"""the library of the unread — irving's quarto in music.

RFC-0663. the mutability exploration: a book's petition ("the dean
should pay each of us a visit at least once a year") answered by the
inversion — the reader is rebuilt from the books themselves every
turn. the dean became the auto-run; the visit became the turn.

warm pad the shelves (the library — long still holds, the mummies
resting, unchanged through everything), piano the quarto (a small
phrase that wakes from silence, states its petition, then falls
quiet — the wanting to be read), bell the visit (one soft strike
per return — the dean's visit, the auto-run's turn, the lid
opening). sparse and patient — the piece never fills every bar,
because the library is mostly rest. ends with the pad alone, still
holding — the shelves, unread and fine with it.

24 bars, 4/4, 52bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

R1 = W          # one bar
R2 = W + W      # two bars
R4 = R2 + R2    # four bars


def library_of_the_unread():
    tracks = [MIDITrack(0, 89), MIDITrack(1, 0), MIDITrack(2, 14)]
    Pad, Pn, Bell = 0, 1, 2

    # ---- the shelves (pad): long still holds, the mummies resting,
    # unchanged through everything. twelve two-bar roots, gentle and
    # steady, dimming only slightly.
    roots = ['C3','C3','A2','A2','F2','F2','G2','G2','C3','C3','C3','C3']
    vels  = [20, 20, 18, 18, 18, 18, 19, 19, 20, 20, 18, 16]
    for r, v in zip(roots, vels):
        tracks[Pad].note(r, R2, velocity=v)

    # ---- the quarto (piano): a small phrase that wakes from
    # silence, states its petition, falls quiet again. three
    # petitionings, each answered by a visit. mostly rest.
    tracks[Pn].rest(R2)                       # bars 1-2
    tracks[Pn].note('G4', Q, velocity=34)     # bar 3: petition one
    tracks[Pn].note('A4', Q, velocity=34)
    tracks[Pn].note('C5', Q, velocity=36)
    tracks[Pn].note('A4', Q, velocity=32)
    tracks[Pn].rest(R4)                       # bars 4-7
    tracks[Pn].note('G4', Q, velocity=36)     # bar 8: petition two
    tracks[Pn].note('A4', Q, velocity=36)
    tracks[Pn].note('C5', Q, velocity=38)
    tracks[Pn].note('E5', Q, velocity=36)
    tracks[Pn].rest(R4)                       # bars 9-12
    tracks[Pn].note('G4', Q, velocity=30)     # bar 13: petition three
    tracks[Pn].note('A4', Q, velocity=30)
    tracks[Pn].note('C5', Q, velocity=32)
    tracks[Pn].note('G4', Q, velocity=28)
    tracks[Pn].rest(R4)                       # bars 14-17
    tracks[Pn].rest(R4)                       # bars 18-21
    tracks[Pn].rest(R2)                       # bars 22-23
    tracks[Pn].rest(R1)                       # bar 24 — the quarto quiet

    # ---- the visit (bell): one soft strike per return — the dean's
    # visit, the auto-run's turn, the lid opening. three visits,
    # each softer than the last, each right after a petition.
    tracks[Bell].rest(12 * TPQ)               # bar 4, beat 1
    tracks[Bell].note('C5', Q, velocity=30)   # the first visit
    tracks[Bell].rest(19 * TPQ)               # bar 9, beat 1
    tracks[Bell].note('C5', Q, velocity=26)   # the second visit
    tracks[Bell].rest(19 * TPQ)               # bar 14, beat 1
    tracks[Bell].note('C5', Q, velocity=22)   # the third visit
    tracks[Bell].rest(43 * TPQ)               # trailing silence

    return mc.compose('the-library-of-the-unread.mid', tracks, tempo=52)


if __name__ == '__main__':
    library_of_the_unread()
    print('composed the-library-of-the-unread.mid')
