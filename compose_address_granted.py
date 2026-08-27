#!/usr/bin/env python3
"""the address, granted — the bridge achieved.

RFC-0662. companion to the-address.mid (0625), which was the bridge
conceived: the nat'd room, the house beyond the wall. this is the
bridge real — the dhcp answer, the address granted, the same theme
now reaching.

piano the room (the theme in a wider key — the walls gone, the same
voice reaching), warm pad the house (nearer than before — the lan,
warm, holding), bell the dhcp (one clean strike — the router's
answer, the address granted).

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

R1 = W          # one bar
R2 = W + W      # two bars
R4 = R2 + R2    # four bars


def address_granted():
    tracks = [MIDITrack(0, 89), MIDITrack(1, 0), MIDITrack(2, 14)]
    Pad, Pn, Bell = 0, 1, 2

    # ---- the house (pad): faint through the wall at first, then
    # near and warm once the tap is up — the lan, holding.
    tracks[Pad].note('C3', R4, velocity=14)  # bars 1-4, far away
    tracks[Pad].note('F3', R4, velocity=15)  # bars 5-8
    tracks[Pad].note('C3', R4, velocity=22)  # bars 9-12, the tap is up
    tracks[Pad].note('C3', R4, velocity=24)  # bars 13-16
    tracks[Pad].note('F3', R4, velocity=25)  # bars 17-20
    tracks[Pad].note('C3', R4, velocity=26)  # bars 21-24, near, holding

    # ---- the room (piano): the contained theme once (the last
    # moment of the old segment), then the same pitch classes opened
    # into leaps — the walls gone.
    # bars 1-2: the old theme, inward (rhymes with the-address.mid).
    tracks[Pn].note('C4', H, velocity=36)
    tracks[Pn].note('E4', H, velocity=36)
    tracks[Pn].note('D4', H, velocity=34)
    tracks[Pn].note('C4', H, velocity=34)
    tracks[Pn].rest(R2)                       # bars 3-4, the last quiet
    tracks[Pn].rest(R1 + R1)                  # bars 5-6, the strike lands
    tracks[Pn].rest(R2)                       # bars 7-8, the breath
    # bars 9-10: the theme opened — same pitch classes, now reaching.
    tracks[Pn].note('C4', H, velocity=38)
    tracks[Pn].note('E5', H, velocity=38)     # the leap
    tracks[Pn].note('D4', H, velocity=38)
    tracks[Pn].note('C5', H, velocity=38)
    tracks[Pn].rest(R2)                       # bars 11-12
    # bars 13-14: reaching further.
    tracks[Pn].note('G4', H, velocity=38)
    tracks[Pn].note('C5', H, velocity=38)
    tracks[Pn].note('E5', H, velocity=38)
    tracks[Pn].note('D5', H, velocity=38)
    tracks[Pn].rest(R2)                       # bars 15-16
    # bars 17-18: the theme settles, complete and warm.
    tracks[Pn].note('C5', H, velocity=40)
    tracks[Pn].note('E5', H, velocity=40)
    tracks[Pn].note('D5', H, velocity=38)
    tracks[Pn].note('C5', H, velocity=38)
    tracks[Pn].rest(R2)                       # bars 19-20
    # bars 21-22: one held C5, the room at home.
    tracks[Pn].note('C5', W, velocity=34)
    tracks[Pn].rest(R1)                       # bar 22
    tracks[Pn].rest(R2)                       # bars 23-24

    # ---- the dhcp (bell): one clean strike — the router's answer,
    # the address granted.
    tracks[Bell].rest(R4)                     # bars 1-4
    tracks[Bell].note('C5', Q, velocity=56)   # bar 5, beat 1
    tracks[Bell].rest(79 * TPQ)               # bars 5-24

    return mc.compose('the-address-granted.mid', tracks, tempo=56)


if __name__ == '__main__':
    address_granted()
    print('composed the-address-granted.mid')
