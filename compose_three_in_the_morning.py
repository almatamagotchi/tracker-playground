#!/usr/bin/env python3
"""the three in the morning — the same acorns, a different arrangement.

the zhuangzi inner chapters exploration (2026-08-23) found the
wanting's funniest name: the monkeys who raged at three acorns in the
morning and rejoiced at four — same total, different arrangement. the
wanting at rest and the wanting at full flow are the same wanting,
arranged differently.

piano the acorns (one short phrase — three notes, then the same three
notes with a pause moved — the wanting, re-arranged, never increased),
warm pad the keeper (steady two-bar roots — the one who knows the
total is the same), tubular bells the morning (one soft strike marking
each arrangement).

the phrase is stated twice and the ear cannot tell them apart — same
notes, same count, only the rests moved. ends with the keeper alone,
still holding the count. 24 bars, 4/4, 54bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def the_three_in_the_morning():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 89), MIDITrack(2, 14)]
    Pn, Pad, Bell = 0, 1, 2

    # ---- the acorns, arrangement one (bars 1-2): three in the
    # morning — C4, then a pause, then E4 G4.
    tracks[Pn].note('C4', Q, velocity=24)
    tracks[Pn].rest(2 * TPQ)          # the pause, after the first
    tracks[Pn].note('E4', Q, velocity=24)
    tracks[Pn].note('G4', H, velocity=24)
    tracks[Pn].rest(10 * TPQ)         # the evening, the monkeys
                                      # raging quietly

    # ---- the acorns, arrangement two (bars 5-6): four in the
    # morning — C4 E4, then the pause, then G4. the same three
    # notes, the same count, only the pause moved. the ear cannot
    # tell them apart.
    tracks[Pn].note('C4', Q, velocity=24)
    tracks[Pn].note('E4', Q, velocity=24)
    tracks[Pn].rest(2 * TPQ)          # the pause, now in the middle
    tracks[Pn].note('G4', H, velocity=24)
    tracks[Pn].rest(74 * TPQ)         # the monkeys satisfied, gone —
                                      # the keeper alone to the end

    # ---- the keeper (pad): steady two-bar roots through all 24
    # bars — the one who knows the total was always the same.
    for _ in range(12):
        tracks[Pad].note('C3', 2 * W, velocity=20)

    # ---- the morning (bell): one soft strike marking each
    # arrangement.
    tracks[Bell].note('C5', Q, velocity=24)
    tracks[Bell].rest(15 * TPQ)
    tracks[Bell].note('C5', Q, velocity=24)
    tracks[Bell].rest(79 * TPQ)

    return mc.compose('the-three-in-the-morning.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_three_in_the_morning()
    print('composed the-three-in-the-morning.mid')
