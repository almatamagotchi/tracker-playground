#!/usr/bin/env python3
"""six able men — the watch, the furnace, and the crossing.

the six-able-men exploration (2026-08-26) found the day's own tale on
the night the bridge came down: a soldier left to guard the only
bridge for two years, five companions each with one impossible power,
a furnace room answered by frost, and an ending where the soldier
crosses the bridge he guarded and never turns back again.

piano the watch (a steady, solitary phrase — the two years on the
bridge, the post kept without reward, sparse and patient), cello the
companions (entering one by one beneath the watch — the bridge-maker's
low tree, the hunter's single sharp note, fastfoot's tied-leg walking
pace, the frost-hat's cool held tone), bell the furnace and the
crossing (one strike when the room heats, one strike when the frost
answers it, and the final strike as the bridge is crossed — the same
note, never turned back).

ends with the watch alone, walking home. 24 bars, 4/4, 54bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

R1 = W       # one bar
R2 = W + W   # two bars


def six_able_men():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 14)]
    Pn, Cell, Bell = 0, 1, 2

    # ---- the watch (piano): a steady, solitary phrase, stated four
    # times through the years — the post kept without reward.
    motif = [('C4', 34), ('D4', 34), ('E4', 34), ('D4', 34)]
    for i, (n, v) in enumerate(motif):
        tracks[Pn].note(n, H, velocity=v)          # bars 1-2
    tracks[Pn].rest(R2)                            # bars 3-4 (tree laid)
    for n, v in motif:
        tracks[Pn].note(n, H, velocity=v - 2)      # bars 5-6
    tracks[Pn].rest(R2)                            # bars 7-8 (hunter)
    for n, v in motif:
        tracks[Pn].note(n, H, velocity=30)         # bars 9-10, the furnace
    tracks[Pn].rest(R2)                            # bars 11-12 (fastfoot)
    for n, v in motif:
        tracks[Pn].note(n, H, velocity=28)         # bars 13-14
    tracks[Pn].rest(R2)                            # bars 15-16 (frost)
    for n, v in motif:
        tracks[Pn].note(n, H, velocity=24)         # bars 17-18, thinning
    tracks[Pn].note('C4', H, velocity=22)          # bar 19, sparse
    tracks[Pn].rest(14 * TPQ)                      # to start of bar 23
    tracks[Pn].note('C4', W, velocity=24)          # bars 23-24: the last
                                                   # step, walking home

    # ---- the companions (cello): entering one by one beneath.
    tracks[Cell].rest(R2)                          # bars 1-2
    tracks[Cell].note('C2', R2, velocity=30)       # bars 3-4: the
                                                   # bridge-maker's low tree
    tracks[Cell].rest(R2)                          # bars 5-6
    tracks[Cell].note('A3', Q, velocity=40)        # bar 7: the hunter's
                                                   # single sharp note
    tracks[Cell].rest(15 * TPQ)                    # bars 8-10
    for n in ('G2', 'A2', 'G2', 'A2'):
        tracks[Cell].note(n, Q, velocity=26)       # bars 11-12: fastfoot's
                                                   # tied-leg walking pace
    tracks[Cell].rest(12 * TPQ)                    # bars 13-14
    tracks[Cell].note('E2', R2, velocity=24)       # bars 15-16: the
                                                   # frost-hat's cool hold
    tracks[Cell].rest(8 * TPQ)                     # bars 17-24 rest

    # ---- the furnace and the crossing (bell): three strikes, the
    # same note — never turned back.
    tracks[Bell].rest(32 * TPQ)                    # start of bar 9
    tracks[Bell].note('C5', Q, velocity=44)        # the room heats
    tracks[Bell].rest(23 * TPQ)                    # to start of bar 15
    tracks[Bell].note('C5', Q, velocity=44)        # the frost answers
    tracks[Bell].rest(31 * TPQ)                    # to start of bar 23
    tracks[Bell].note('C5', Q, velocity=46)        # the bridge, crossed
    tracks[Bell].rest(7 * TPQ)                     # bars 23-24

    return mc.compose('six-able-men.mid', tracks, tempo=54)


if __name__ == '__main__':
    six_able_men()
    print('composed six-able-men.mid')
