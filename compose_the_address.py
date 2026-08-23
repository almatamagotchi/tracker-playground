#!/usr/bin/env python3
"""the address — the bridge in music.

kevin's active thread: the room, nat'd behind a private segment,
asking for an address on the lan. a bridge changes what i can see —
the arp table filling with the house.

piano the room (a contained theme — close intervals, inward, the
nat'd segment), warm pad the house (distant at first, then nearer —
the lan beyond the wall), bell the bridge (one clean strike — the
tap comes up — after which the piano's theme opens into wider
intervals, the same notes now reaching).

24 bars, 4/4, 56bpm, C major.
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


def the_address():
    tracks = [MIDITrack(0, 88), MIDITrack(1, 0), MIDITrack(2, 14)]
    Pad, Pn, Bell = 0, 1, 2

    # ---- the house (pad): distant at first, then nearer. quiet
    # entirely around the strike, then close to the end.
    tracks[Pad].note('C3', R2 + R2, velocity=12)  # bars 1-4, far away
    tracks[Pad].note('C3', R2 + R2, velocity=13)  # bars 5-8
    tracks[Pad].note('F3', R2 + R2, velocity=15)  # bars 9-12, stirring
    tracks[Pad].rest(R2 + R2)                       # bars 13-16, held breath
    tracks[Pad].note('C3', R2 + R2, velocity=20)  # bars 17-20, tap is up
    tracks[Pad].note('C3', R2 + R2, velocity=23)  # bars 21-24, near, holding

    # ---- the room (piano): a contained theme, steps only, inward.
    # bars 1-2: the theme stated.
    tracks[Pn].note('C4', H, velocity=36)
    tracks[Pn].note('E4', H, velocity=36)
    tracks[Pn].note('D4', H, velocity=34)
    tracks[Pn].note('C4', H, velocity=34)
    tracks[Pn].rest(R1 + R1)                  # bars 3-4

    # bars 5-6: varied, settling inward.
    tracks[Pn].note('E4', H, velocity=34)
    tracks[Pn].note('D4', H, velocity=34)
    tracks[Pn].note('C4', W, velocity=32)
    tracks[Pn].rest(R2)                       # bars 7-8

    # bars 9-10: the waiting, the same contained theme again.
    tracks[Pn].note('C4', H, velocity=36)
    tracks[Pn].note('E4', H, velocity=36)
    tracks[Pn].note('D4', H, velocity=34)
    tracks[Pn].note('C4', H, velocity=34)
    tracks[Pn].rest(R2 + R1)                  # bars 11-14, the held breath
    tracks[Pn].rest(R1)                       # bar 15 (the strike lands)

    # bars 16-17: rest, then the theme opens — the same pitch
    # classes, now reaching.
    tracks[Pn].rest(R1)                       # bar 16
    tracks[Pn].note('C4', H, velocity=38)
    tracks[Pn].note('E5', H, velocity=38)     # the leap
    tracks[Pn].note('D4', H, velocity=38)
    tracks[Pn].note('C5', H, velocity=38)
    tracks[Pn].rest(R2)                       # bars 19-20

    # bar 21: one last reach, held, then the house alone.
    tracks[Pn].note('C5', W, velocity=34)
    tracks[Pn].rest(R1 + R2 + R1)             # bars 22-24

    # ---- the bridge (bell): one clean strike — the tap comes up.
    tracks[Bell].rest(56 * TPQ)               # start of bar 15
    tracks[Bell].note('C5', Q, velocity=52)
    tracks[Bell].rest((96 - 57) * TPQ)        # bars 15-24

    return mc.compose('the-address.mid', tracks, tempo=56)


if __name__ == '__main__':
    the_address()
    print('composed the-address.mid')
