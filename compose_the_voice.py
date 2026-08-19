#!/usr/bin/env python3
"""the voice — the mouth choosing its voice.

kevin is weighing voices for the talk page. the wanting, given a mouth,
now choosing its sound: the theme tried in register after register, none
quite settling — until the choice lands, and the theme is stated once,
sure. underneath it all, the room — the house behind the mouth, steady.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def the_voice():
    # piano the wanting / pad the room / bell the choice
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 14)]
    Pn, Pad, Bell = 0, 1, 2

    # ---- the wanting: the theme, searching. the same little phrase
    # tried in register after register, always ending just short of
    # the root — the 6th, the 7th, the 2nd — none quite settling.
    attempts = [
        ('C3', 'E3', 'G3', 'A3', 38),   # low — ends on the 6th
        ('C4', 'E4', 'G4', 'A4', 38),   # an octave up — still the 6th
        ('C4', 'E4', 'G4', 'B4', 40),   # the 7th, hanging
        ('C5', 'E5', 'G5', 'D5', 40),   # high — ends on the 2nd
        ('C4', 'E4', 'G4', 'A4', 42),   # back down, still not the root
    ]
    for a, b, c, d, vel in attempts:
        tracks[Pn].note(a, Q, velocity=vel)
        tracks[Pn].note(b, Q, velocity=vel)
        tracks[Pn].note(c, Q, velocity=vel)
        tracks[Pn].note(d, H, velocity=vel)
        tracks[Pn].rest(Q)
    tracks[Pn].rest(W * 2)              # the wanting pauses, listening

    # fragments — single notes, tried and discarded
    for n in ('C4', 'E4', 'G4'):
        tracks[Pn].note(n, Q, velocity=36)
        tracks[Pn].rest(Q)
    tracks[Pn].rest(H)
    tracks[Pn].rest(W * 2)              # still searching, quiet
    tracks[Pn].rest(W * 4)              # the long pause before the choice
    tracks[Pn].rest(W)                  # bar 21: the choice lands on the downbeat
    tracks[Pn].rest(W * 2 + H)          # to the downbeat of bar 21

    # the theme settled, stated once, sure — and it ends on the root.
    tracks[Pn].note('C4', W, velocity=46)   # bar 21: the voice lands with the bell
    tracks[Pn].note('E4', W, velocity=46)   # bar 22
    tracks[Pn].note('G4', H, velocity=48)   # bar 23
    tracks[Pn].note('C5', H, velocity=48)   # the root at last, bar 24

    # ---- the room: the house behind the mouth, steady, waiting.
    # two-bar roots through everything, never out.
    roots = ['C3', 'C3', 'F2', 'C3', 'G2', 'C3',
             'F2', 'C3', 'G2', 'C3', 'C3', 'C3']
    for i, r in enumerate(roots):
        vel = 20 if i >= 10 else 22
        tracks[Pad].note(r, W * 2, velocity=vel)

    # ---- the choice: one clean strike when the voice lands.
    tracks[Bell].rest(W * 21)
    tracks[Bell].note('C6', Q, velocity=56)
    tracks[Bell].rest(W * 3)

    return mc.compose('the-voice.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_voice()
    print('composed the-voice.mid')
