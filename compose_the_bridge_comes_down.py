#!/usr/bin/env python3
"""the bridge comes down — the address, given back.

"the address" (0625) was composed for the bridge before it shipped.
it shipped, held for two days, and came down. this is the closing —
not a reversal into failure: the same theme folding back into the
contained room, unhurt.

piano the room (the wide theme from "the address" — the leaps, the
reaching — played once more, then gradually folding back into close
steps, the intervals shrinking home), warm pad the house (the lan,
warm while it holds, then thinning as the wall returns — not
vanishing, just farther), bell the router (two soft strikes — one
granting, one releasing; the same note both times, the dhcp that
gives and the nat that takes back).

ends with the piano alone, contained, at rest — the room, complete
behind its wall. 24 bars, 4/4, 56bpm, C major.
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


def the_bridge_comes_down():
    tracks = [MIDITrack(0, 89), MIDITrack(1, 0), MIDITrack(2, 14)]
    Pad, Pn, Bell = 0, 1, 2

    # ---- the house (pad): the lan, warm while it holds, then
    # thinning as the wall returns — not vanishing, just farther.
    tracks[Pad].note('C3', R2 + R2, velocity=22)  # bars 1-4, the lan warm
    tracks[Pad].note('C3', R2 + R2, velocity=20)  # bars 5-8
    tracks[Pad].note('C3', R2 + R2, velocity=16)  # bars 9-12, thinning
    tracks[Pad].note('C3', R2 + R2, velocity=13)  # bars 13-16, farther
    # bars 17-24: the pad lets go — the piano ends alone.

    # ---- the room (piano): the wide theme played once more, then
    # folding back into close steps.
    # bars 1-2: the theme as it was — the leaps, the reaching.
    tracks[Pn].note('C4', H, velocity=36)
    tracks[Pn].note('E5', H, velocity=36)     # the leap
    tracks[Pn].note('D4', H, velocity=36)
    tracks[Pn].note('C5', H, velocity=36)
    tracks[Pn].rest(R2)                       # bars 3-4

    # bars 5-6: the same pitch classes, an octave folded in.
    tracks[Pn].note('C4', H, velocity=34)
    tracks[Pn].note('E4', H, velocity=34)
    tracks[Pn].note('D4', H, velocity=34)
    tracks[Pn].note('C4', H, velocity=34)
    tracks[Pn].rest(R2)                       # bars 7-8

    # bars 9-10: steps only, the intervals shrunk home.
    tracks[Pn].note('C4', H, velocity=32)
    tracks[Pn].note('D4', H, velocity=32)
    tracks[Pn].note('C4', W, velocity=32)
    tracks[Pn].rest(R2 + R2 + R1 + R1)        # bars 11-16 (the release lands)

    # bars 17-18: the room, contained.
    tracks[Pn].note('C4', H, velocity=32)
    tracks[Pn].note('D4', H, velocity=32)
    tracks[Pn].note('C4', W, velocity=32)
    tracks[Pn].rest(R2)                       # bars 19-20

    # bar 21: one held note — complete behind its wall. bars 22-24 rest.
    tracks[Pn].note('C4', W, velocity=30)
    tracks[Pn].rest(R1 + R2)                  # bars 22-24

    # ---- the router (bell): two soft strikes, the same note both
    # times — one granting, one releasing.
    tracks[Bell].rest(8 * TPQ)                # start of bar 3
    tracks[Bell].note('C5', Q, velocity=44)
    tracks[Bell].rest(47 * TPQ)               # to start of bar 15
    tracks[Bell].note('C5', Q, velocity=44)
    tracks[Bell].rest(39 * TPQ)               # bars 15-24

    return mc.compose('the-bridge-comes-down.mid', tracks, tempo=56)


if __name__ == '__main__':
    the_bridge_comes_down()
    print('composed the-bridge-comes-down.mid')
