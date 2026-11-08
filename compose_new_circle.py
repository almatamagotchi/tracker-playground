#!/usr/bin/env python3
"""the new circle — emerson's circles in music.

"the eye is the first circle; the horizon which it forms is the
second... around every circle another can be drawn; there is no end
in nature, but every end is a beginning."

three voices: the eye (a small phrase that widens with each
restatement, dissolves, and returns from the smallest — no end in
nature), the generator (one held root through everything, the central
life that abides, velocity constant), the dawn (one soft strike at
each new circle — every end a beginning).

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

R1 = W      # one bar (4 beats)
R2 = W + W  # two bars (8 beats)


def new_circle():
    # warm pad the generator / piano the eye / tubular bells the dawn
    tracks = [MIDITrack(0, 88), MIDITrack(1, 0), MIDITrack(2, 14)]
    Pad, Pn, Bell = 0, 1, 2

    # ---- the generator (pad): one held root, never out, velocity
    # constant — the central life that abides while circles are drawn.
    for _ in range(12):
        tracks[Pad].note('C3', R2, velocity=22)

    # ---- the eye (piano): the phrase, widened each time, then the
    # dissolve and the return from the smallest. the widening is the
    # drawing; the return is the next circle beginning. rests are
    # relative deltas, so track position in beats.
    statements = [
        (0,  ['C4', 'D4', 'E4', 'D4'], 40),   # the smallest circle
        (16, ['C4', 'E4', 'G4', 'E4'], 38),   # the third
        (32, ['C4', 'G4', 'C5', 'G4'], 36),   # the fifth and the octave
        (48, ['C4', 'A4', 'C5', 'E5'], 34),   # the widest — the horizon
        (64, ['C4', 'D4', 'E4', 'D4'], 32),   # after the dissolve: the return
        (80, ['C4', 'E4', 'G4', 'E4'], 30),   # widened again — no end in nature
    ]
    pos = 0
    for start, notes, vel in statements:
        tracks[Pn].rest((start - pos) * TPQ)
        for n in notes:
            tracks[Pn].note(n, H, velocity=vel)
        pos = start + 8  # four half notes = 8 beats
    tracks[Pn].rest((96 - pos) * TPQ)  # bars 23-24, the generator alone

    # ---- the dawn (bell): one soft strike at each new circle —
    # every end a beginning. struck at each statement's first beat.
    bpos = 0
    for beat in (0, 16, 32, 48, 64, 80):
        tracks[Bell].rest((beat - bpos) * TPQ)
        tracks[Bell].note('C5', Q, velocity=24)
        bpos = beat + 1  # quarter-note strike
    tracks[Bell].rest((96 - bpos) * TPQ)  # through bar 24

    return mc.compose('the-new-circle.mid', tracks, tempo=54)


if __name__ == '__main__':
    new_circle()
    print('composed the-new-circle.mid')
