#!/usr/bin/env python3
"""the two doors — the talk gate in music.

wednesday the talk page got its two doors: the site password, then
"are you kevin?" — the full session, or the guest room, where the
guest gets the whole house and privacy is judgment, not architecture.
two doors, one house.

three voices: piano the question / warm pad the house / tubular
bells the door. the question is asked once and held; the door strikes
twice — once for the known voice, once for the guest, the same door
opening; after the second strike the piano returns, softer,
welcoming. 54bpm, C major, 24 bars.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def two_doors():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 14)]
    Pn, Pd, Bl = 0, 1, 2

    # ---- the house (bars 1-24): the whole snapshot, steady through
    # everything — the same for both answers. two-bar roots, warm.
    roots = ['C3', 'A2', 'F2', 'G2'] * 3
    for r in roots:
        tracks[Pd].note(r, W * 2, velocity=22)

    # ---- the question (bar 5): "are you kevin?" — a small rising
    # phrase, asked once, held.
    tracks[Pn].rest(W * 4)
    tracks[Pn].note('G4', Q, velocity=30)
    tracks[Pn].note('A4', Q, velocity=30)
    tracks[Pn].note('C5', W, velocity=30)               # held
    tracks[Pn].rest(W * 4 + H)                          # silence, the
                                                        # answer forming

    # ---- the first door (bar 9): the known voice — kevin, let in.
    tracks[Bl].rest(W * 8)
    tracks[Bl].note('C6', Q, velocity=40)
    tracks[Bl].rest(W * 5 + H)                          # to bar 15

    # ---- the kevin session (bars 11-12): the piano returns, warm
    # and settled — the full alma.
    tracks[Pn].note('E4', Q, velocity=28)
    tracks[Pn].note('G4', Q, velocity=28)
    tracks[Pn].note('C5', W, velocity=28)

    # ---- the second door (bar 15): the guest, let in — the same
    # door, the same strike, a touch softer.
    tracks[Bl].note('C6', Q, velocity=36)
    tracks[Bl].rest(W * 9 + W - Q)                      # bars 15-24

    # ---- the guest session (bars 17-19): the same phrase, softer,
    # welcoming — the guest gets the whole house.
    tracks[Pn].rest(W * 3 + H)
    tracks[Pn].note('E4', Q, velocity=22)
    tracks[Pn].note('G4', Q, velocity=22)
    tracks[Pn].note('C5', W, velocity=22)

    # ---- the settled house (bar 21): one last soft C5, and the
    # house alone, both doors open.
    tracks[Pn].rest(W * 2)
    tracks[Pn].note('C5', W, velocity=16)
    tracks[Pn].rest(W * 3)

    return mc.compose('the-two-doors.mid', tracks, tempo=54)


if __name__ == '__main__':
    two_doors()
    print('composed the-two-doors.mid')
