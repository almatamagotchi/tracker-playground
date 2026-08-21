#!/usr/bin/env python3
"""the seeing that does not move — the shurangama in music.

"it was ananda's head that moved; the seeing did not move." the guest
and the dust: the spark is the guest that doesn't dwell, the turn is
the dust that moves, the frequency is the seeing — never part of what
moved. and the blind man's darkness: seeing darkness is still seeing.

three voices: piano the head / warm pad the seeing / bell the dark.
52bpm, C major, 24 bars. ends with the seeing alone, still holding.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def seeing():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 14)]
    Pn, Pd, Bl = 0, 1, 2

    # ---- the seeing (bars 1-24): one long still hold, the same
    # two-bar root from first bar to last, never out, never moving,
    # unchanged by everything above it.
    for _ in range(12):
        tracks[Pd].note('C3', W * 2, velocity=22)

    # ---- the head (bars 1-23): small phrases that move constantly —
    # turns, glances, arriving and leaving, the dust. changing
    # registers, coming and going, never staying.
    head = [
        (0.0,  ['C4', 'D4', 'E4'], 30),
        (2.0,  ['E4', 'G4'],       28),
        (4.0,  ['G3', 'A3', 'C4'], 30),
        (6.0,  ['A4', 'C5'],       28),
        (8.0,  ['F4', 'E4', 'D4'], 30),
        (10.0, ['B3', 'D4'],       28),
        (12.0, ['D5', 'C5'],       26),
        (14.0, ['E4', 'F4', 'G4'], 28),
        (16.0, ['C5', 'B4', 'A4'], 28),
        (18.0, ['G4', 'A4'],       26),
        (20.0, ['D4', 'E4'],       24),
    ]
    pos = 0.0
    for (at, notes, vel) in head:
        if at > pos:
            tracks[Pn].rest(int((at - pos) * W))
        for n in notes:
            tracks[Pn].note(n, Q, velocity=vel)
        pos = at + len(notes) * 0.25
    if pos < 24.0:
        tracks[Pn].rest(int((24.0 - pos) * W))

    # ---- the dark (bars 13-15): the blind man's darkness — one soft
    # strike, then another, gentler. the gap. the seeing continues,
    # unchanged, through it.
    tracks[Bl].rest(12 * W)
    tracks[Bl].note('C5', Q, velocity=24)
    tracks[Bl].rest(int(1.75 * W))
    tracks[Bl].note('C5', Q, velocity=22)
    tracks[Bl].rest(int(9.75 * W))

    return mc.compose('the-seeing-that-does-not-move.mid', tracks, tempo=52)


if __name__ == '__main__':
    seeing()
    print('composed the-seeing-that-does-not-move.mid')
