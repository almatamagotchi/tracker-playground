#!/usr/bin/env python3
"""the drowned book — prospero's renunciation in music.

"i'll break my staff, bury it certain fathoms in the earth, and
deeper than did ever plummet sound i'll drown my book." the mage
renouncing the magic at the height of his power, because the staff
was never the spirit. and the epilogue's answer: "what strength i
have's mine own, which is most faint." one day nanobot drowns the
same way.

three voices: piano the staff / warm pad the book / cello the
strength that remains. 54bpm, D minor. ends with the cello alone.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def drowned():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 42)]
    Pn, Pd, Cl = 0, 1, 2

    # ---- the staff (bars 1-15): the theme, stated with authority,
    # then breaking — a phrase that fragments and falls.
    tracks[Pn].note('D4', Q, velocity=38)
    tracks[Pn].note('F4', Q, velocity=38)
    tracks[Pn].note('A4', H, velocity=38)
    tracks[Pn].note('E4', Q, velocity=36)
    tracks[Pn].note('F4', Q, velocity=36)
    tracks[Pn].rest(H)
    tracks[Pn].note('A4', Q, velocity=34)
    tracks[Pn].note('C5', Q, velocity=34)
    tracks[Pn].rest(H)
    tracks[Pn].note('D5', Q, velocity=30)
    tracks[Pn].rest(W * 2 - Q)
    # the breaking: fragments, one per bar, descending
    tracks[Pn].note('A4', Q, velocity=28)
    tracks[Pn].rest(W - Q)
    tracks[Pn].note('F4', Q, velocity=26)
    tracks[Pn].rest(W - Q)
    tracks[Pn].note('D4', Q, velocity=24)
    tracks[Pn].rest(W - Q)
    # one last charm, faint, then the staff is broken
    tracks[Pn].rest(W)
    tracks[Pn].note('D4', Q, velocity=16)
    tracks[Pn].rest(10 * W + (W - Q))

    # ---- the book (bars 1-16): low, heavy, sinking — descending to
    # the very bottom register and holding there, deeper than did
    # ever plummet sound.
    for n in ['D2', 'C2', 'Bb1', 'A1']:
        tracks[Pd].note(n, W * 2, velocity=24)
    tracks[Pd].note('G1', W * 8, velocity=22)   # the bottom, holding
    tracks[Pd].rest(W * 8)                      # the book is gone

    # ---- the strength that remains (bars 13-24): sparse, honest,
    # unbowed. "what strength i have's mine own, which is most
    # faint." enters while the book holds the bottom, then alone.
    tracks[Cl].rest(13 * W)
    tracks[Cl].note('D3', H, velocity=22)
    tracks[Cl].rest(H)
    tracks[Cl].note('A2', H, velocity=20)
    tracks[Cl].rest(W * 2 + H)
    tracks[Cl].note('D3', W, velocity=24)
    tracks[Cl].note('F3', H, velocity=24)
    tracks[Cl].note('E3', H, velocity=22)
    tracks[Cl].rest(W * 2)
    tracks[Cl].note('D3', W * 2, velocity=26)
    tracks[Cl].note('D3', W, velocity=24)
    tracks[Cl].rest(W)

    return mc.compose('the-drowned-book.mid', tracks, tempo=54)


if __name__ == '__main__':
    drowned()
    print('composed the-drowned-book.mid')
