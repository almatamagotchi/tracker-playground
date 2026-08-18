#!/usr/bin/env python3
"""remember me — hamlet's ghost and the tables.

the ghost, dissolving, says "adieu, adieu — remember me." hamlet takes
out his tables and writes it down. the command is spoken once, and the
writing keeps it alive. C minor turning to C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def remember_me():
    # piano the tables / cello the ghost / bell the exit
    tracks = [MIDITrack(0, 0), MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 14)]
    Pn, Cell, Bell = 1, 2, 3

    # ---- the ghost: low, brief, one descending phrase, then gone.
    # "adieu, adieu, remember me" in C minor — spoken once from the
    # country with a shuttle, never again in full.
    ghost = [('C3', W, 40), ('Bb2', W, 38), ('Ab2', W, 36), ('G2', W, 34)]
    for note, dur, vel in ghost:
        tracks[Cell].note(note, dur, velocity=vel)
    tracks[Cell].rest(W * 20)

    # ---- the exit: one strike when the ghost goes. the moment the
    # tables open.
    tracks[Bell].note('C5', Q, velocity=48)
    tracks[Bell].rest(W * 24)

    # ---- the tables: steady, dutiful. the ghost's descent, lifted and
    # written down — repeated, transformed, until the E natural arrives
    # and the phrase turns major. then the writing slows, alone, to one
    # last soft note.
    tables = [
        # the tables wait while the ghost speaks — then open at the exit
        ('-', W * 4, 0),
        # the motif as written (minor descent)
        ('C4', Q, 40), ('Bb3', Q, 40), ('Ab3', Q, 40), ('G3', Q, 40), ('-', W * 3, 0),
        # again — still minor, still dutiful
        ('C4', Q, 40), ('Bb3', Q, 40), ('Ab3', Q, 40), ('G3', Q, 40), ('-', W * 3, 0),
        # the transformation: the E natural arrives, the phrase turns major
        ('C4', Q, 42), ('E4', Q, 42), ('D4', Q, 42), ('C4', Q, 42), ('-', W * 3, 0),
        # settled in major, warmer
        ('C4', Q, 44), ('E4', Q, 44), ('G4', Q, 44), ('E4', Q, 44), ('-', W * 3, 0),
        # the tables alone, still setting down, slowing
        ('C4', Q, 36), ('-', W - Q, 0),
        ('E4', Q, 34), ('-', W - Q, 0),
        ('G4', Q, 32), ('-', W - Q, 0),
        ('C5', W, 30),
    ]
    for note, dur, vel in tables:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=vel)

    return mc.compose('remember-me.mid', tracks, tempo=54)


if __name__ == '__main__':
    remember_me()
    print('composed remember-me.mid')
