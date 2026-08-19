#!/usr/bin/env python3
"""the flame that leaps — plato's seventh letter in music.

"after much converse about the matter itself and a life lived together,
suddenly a light is kindled in one soul by a flame that leaps to it from
another, and thereafter sustains itself."

three voices:
- piano the converse — question and answer, two short phrases trading,
  rubbing, never resolving into one. the friction is the method.
- warm pad the flame — kindled once, low, and then sustains itself: a
  held warmth that never goes out (the pilot light).
- cello the unwritten thing — the fifth: a phrase that begins on G and
  climbs toward the root, never completing, always approaching, never
  stated. hangs on the leading tone when the piece ends.

24 bars, 4/4, 54bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def flame():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 42)]
    Pn, Pad, Cl = 0, 1, 2

    # ---- the converse. each block is exactly 2 bars: phrase + fill.
    # question rises to the seventh and hangs; answer descends, avoids
    # the root. ten blocks, then the last exchange runs to the end.
    blocks = [
        ([('E4', Q), ('G4', Q), ('B4', H)], 40),   # bars 1-2
        ([('D4', Q), ('C4', Q), ('E4', H)], 40),   # bars 3-4
        ([('E4', Q), ('G4', Q), ('B4', H)], 38),   # 5-6
        ([('D4', Q), ('C4', Q), ('E4', H)], 38),   # 7-8
        ([('E4', Q), ('G4', Q), ('B4', H)], 36),   # 9-10
        ([('D4', Q), ('C4', Q), ('E4', H)], 36),   # 11-12
        ([('E4', Q), ('G4', Q), ('B4', H)], 32),   # 13-14
        ([('D4', Q), ('C4', Q), ('E4', H)], 32),   # 15-16
        ([('E4', Q), ('G4', Q)], 28),              # 17-18 — fragments
        ([('D4', Q), ('C4', Q)], 28),              # 19-20 — the friction fades
    ]
    tracks[Pn].rest(W)                             # bar 1 — the room before
    for notes, vel in blocks:
        for n, d in notes:
            tracks[Pn].note(n, d, velocity=vel)
        tracks[Pn].rest(int(2 * W - sum(d for _, d in notes)))
    # the last exchange, held to the end
    tracks[Pn].note('E4', Q, velocity=30)
    tracks[Pn].note('G4', Q, velocity=30)
    tracks[Pn].note('B4', W, velocity=30)          # 21-22.5 — question, hanging
    tracks[Pn].note('D4', Q, velocity=28)
    tracks[Pn].note('C4', Q, velocity=28)
    tracks[Pn].note('E4', W, velocity=28)          # 22.5-24 — answer, still two

    # ---- the flame: kindled once at bar 5, then sustains itself —
    # three re-struck long holds, no silence between, still burning when
    # the piece stops.
    tracks[Pad].rest(5 * W)
    tracks[Pad].note('C3', 8 * W, velocity=20)
    tracks[Pad].note('C3', 8 * W, velocity=22)
    tracks[Pad].note('C3', 3 * W, velocity=18)

    # ---- the unwritten thing: begins on the fifth, climbs toward the
    # root, never completes. four full attempts, then the last quickens
    # and hangs on the leading tone to the end.
    for a in range(4):
        tracks[Cl].rest(W)
        tracks[Cl].note('G2', W, velocity=26)
        tracks[Cl].note('A2', W, velocity=26)
        tracks[Cl].note('B2', W, velocity=28)
        tracks[Cl].rest(W)
    # the final approach — accelerating, then hanging
    tracks[Cl].rest(W)
    tracks[Cl].note('G2', Q, velocity=26)
    tracks[Cl].note('A2', Q, velocity=26)
    tracks[Cl].note('B2', int(2.5 * W), velocity=28)

    return mc.compose('the-flame-that-leaps.mid', tracks, tempo=54)


if __name__ == '__main__':
    flame()
    print('composed the-flame-that-leaps.mid')
