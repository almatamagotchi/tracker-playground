#!/usr/bin/env python3
"""the ringdove and the pigeon — the theaetetus aviary in music.

the theaetetus exploration (2026-08-23) found the ghost issue's own
dialogue: false judgment as the wrong catch — "he got hold of the
ringdove which he had in his mind, when he wanted the pigeon" — and
the birds of ignorance flying in the same flock as the birds of
knowledge, indistinguishable until caught.

piano the reach (the turn — sparse reaching figures, the hand entering
the aviary), flute the pigeon (the true claim — a clean phrase, the
verified fact), oboe the ringdove (the false claim — the same phrase
with a single wrong note, the narration that felt like knowledge).

the reach, the catch, the inspection, the recatch, the release — the
piece ends open, not resolved: the aporia kept. the birds fly
together; only the inspection tells them apart. 24 bars, 4/4, 54bpm,
C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def the_ringdove_and_the_pigeon():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 73), MIDITrack(2, 68)]
    Pn, Fl, Ob = 0, 1, 2

    # ---- the reach (bars 1-2): the hand entering the aviary,
    # sparse, tentative, ending on C5.
    tracks[Pn].note('E4', Q, velocity=22)
    tracks[Pn].note('G4', Q, velocity=24)
    tracks[Pn].note('A4', Q, velocity=26)
    tracks[Pn].note('C5', H, velocity=28)
    tracks[Pn].rest(12 * TPQ)

    # ---- the catch (bar 6): the hand closes on the wrong bird —
    # one sharp startled note.
    tracks[Pn].note('C5', E, velocity=44)
    tracks[Pn].rest(12 * TPQ)

    # ---- the inspection (bars 9-12): the piano alone, sparse
    # testing notes — the midwife, the wind-egg exposed. the
    # ringdove's wrong note isolated between two D4s.
    tracks[Pn].note('D4', Q, velocity=24)
    tracks[Pn].note('C#4', Q, velocity=26)
    tracks[Pn].note('D4', Q, velocity=22)
    tracks[Pn].note('E4', H, velocity=20)
    tracks[Pn].rest(36 * TPQ)

    # ---- the open ending (bars 22-24): the reach restated but
    # ending on A4, no tonic — the aporia kept.
    tracks[Pn].note('E4', Q, velocity=18)
    tracks[Pn].note('G4', Q, velocity=18)
    tracks[Pn].note('A4', H, velocity=18)
    tracks[Pn].rest(4 * TPQ)

    # ---- the pigeon (bars 13-15): the true claim, the receipt —
    # same shape, the one note corrected.
    tracks[Fl].rest(52 * TPQ)
    tracks[Fl].note('G4', Q, velocity=32)
    tracks[Fl].note('A4', Q, velocity=32)
    tracks[Fl].note('C5', H, velocity=32)
    tracks[Fl].rest(8 * TPQ)
    # ---- the release (bars 17-18): both birds let go together —
    # the right note and the wrong note sounding at once.
    tracks[Fl].note('C5', H, velocity=20)
    tracks[Fl].rest(24 * TPQ)

    # ---- the ringdove (bars 5-7): the false claim stated
    # confidently — the "filed" that wasn't. same shape as the
    # pigeon, one note sharp.
    tracks[Ob].rest(20 * TPQ)
    tracks[Ob].note('G4', Q, velocity=36)
    tracks[Ob].note('A4', Q, velocity=36)
    tracks[Ob].note('C#5', H, velocity=36)
    tracks[Ob].rest(40 * TPQ)
    # ---- the release (bars 17-18): the wrong bird, let go too.
    tracks[Ob].note('C#5', H, velocity=20)
    tracks[Ob].rest(24 * TPQ)

    return mc.compose('the-ringdove-and-the-pigeon.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_ringdove_and_the_pigeon()
    print('composed the-ringdove-and-the-pigeon.mid')
