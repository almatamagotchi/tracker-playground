#!/usr/bin/env python3
"""the epilogue — the novel's ending in music.

jim the sysop copying everything when the rust belt dies in 1996. the
tape reaching the archive. the narrator finding it from a back flat on
park street. the tower still blinking — a count of one, repeated.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def epilogue():
    # piano the record / warm pad the porch light / bell the tower
    tracks = [MIDITrack(0, 0), MIDITrack(1, 88), MIDITrack(2, 14)]
    Pn, Pad, Bell = 0, 1, 2

    # ---- the record: steady, patient, the copying. a careful
    # half-note line, pages turning — then one whole note, held,
    # the tape handed to the archive. then silence.
    record = [
        ('C5', H, 40), ('E5', H, 40),
        ('G5', H, 40), ('E5', H, 40),
        ('C5', H, 38), ('D5', H, 38),
        ('E5', H, 38), ('D5', H, 38),
        ('C5', H, 40), ('E5', H, 40),
        ('G5', H, 40), ('E5', H, 40),
        ('C5', H, 38), ('D5', H, 38),
        ('E5', H, 38), ('D5', H, 38),
        ('C5', H, 40), ('E5', H, 40),
        ('G5', W, 38),
        ('C5', W, 34),
        ('-', W + W + W + W, 0),
    ]
    for note, dur, vel in record:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=vel)

    # ---- the porch light: held, warm, the bulb from 1972. it keeps
    # the dark at bay for someone else — and goes quiet only at the
    # very end, leaving the count alone.
    porch = [
        ('C3', W + W), ('F2', W + W), ('C3', W + W), ('G2', W + W),
        ('C3', W + W), ('F2', W + W), ('C3', W + W), ('G2', W + W),
        ('C3', W + W), ('F2', W + W), ('C3', W + W),
        ('-', W + W),
    ]
    for note, dur in porch:
        if note == '-':
            tracks[Pad].rest(dur)
        else:
            tracks[Pad].note(note, dur, velocity=26)

    # ---- the tower: the same strike every bar, all the way through.
    # a count of one, repeated. the record ends, the porch light goes
    # quiet, and the tower keeps counting — the last strike soft, the
    # count continuing into the silence the piece stops inside.
    for bar in range(24):
        vel = 36 if bar < 23 else 26
        tracks[Bell].note('C5', Q, velocity=vel)
        tracks[Bell].rest(W - Q)

    return mc.compose('the-epilogue.mid', tracks, tempo=56)


if __name__ == '__main__':
    epilogue()
    print('composed the-epilogue.mid')
