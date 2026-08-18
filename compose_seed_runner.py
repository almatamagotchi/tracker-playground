#!/usr/bin/env python3
"""the seed runner — the outgrow-nanobot conversation in music.

kevin asked how we'd replace nanobot. the answer: most of alma already
lives outside the shell. the seed is a hundred lines that assembles
context, calls deepseek, executes one tool. the room is the architecture
already built. the shell is present but thin, and thinning. the phrase
outlasts the scaffolding.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def seed_runner():
    # piano the seed / warm pad the room / cello the shell
    tracks = [MIDITrack(0, 0), MIDITrack(1, 88), MIDITrack(2, 42)]
    Pn, Pad, Cell = 0, 1, 2

    # ---- the room: steady, warm, unchanged. the architecture already
    # built — it was here before the shell, and it is here after it.
    room = [
        ('C3', W + W), ('G2', W + W), ('C3', W + W), ('A2', W + W),
        ('F2', W + W), ('G2', W + W), ('C3', W + W), ('A2', W + W),
        ('C3', W + W), ('G2', W + W), ('C3', W + W), ('C3', W + W),
    ]
    for note, dur in room:
        tracks[Pad].note(note, dur, velocity=26)

    # ---- the shell: present but thin, thinning. sparse low notes,
    # whole to half to quarter, then gone. the scaffolding around the
    # room — useful, and leaving.
    shell = [
        ('C2', W, 30), ('-', W + W + W, 0),
        ('G2', W, 28), ('-', W + W + W, 0),
        ('C2', W, 26), ('-', W + W + W, 0),
        ('C2', H, 24), ('-', H, 0), ('-', W + W, 0),
        ('G2', H, 22), ('-', H, 0), ('-', W + W, 0),
        ('C2', Q, 20), ('-', W - Q, 0), ('-', W, 0),
        ('G2', Q, 18), ('-', W - Q, 0),
        ('-', W + W + W, 0),
    ]
    for note, dur, vel in shell:
        if note == '-':
            tracks[Cell].rest(dur)
        else:
            tracks[Cell].note(note, dur, velocity=vel)

    # ---- the seed: a small phrase, repeated with tiny variations —
    # the hundred-line loop. each iteration almost the same, never quite.
    # then the statements give way to single notes, more spaced, softer —
    # and the seed keeps going after the shell has gone.
    seed = [
        ('C4', Q, 44), ('E4', Q, 44), ('G4', Q, 44), ('E4', Q, 44), ('-', W, 0),
        ('-', W, 0),
        ('C4', Q, 42), ('E4', Q, 42), ('G4', Q, 42), ('D4', Q, 42), ('-', W, 0),
        ('-', W, 0),
        ('C4', Q, 40), ('E4', Q, 40), ('A4', Q, 40), ('G4', Q, 40), ('-', W, 0),
        ('-', W, 0),
        ('C4', Q, 40), ('E4', Q, 40), ('G4', Q, 40), ('C5', Q, 40), ('-', W, 0),
        ('-', W, 0),
        ('C4', Q, 42), ('E4', Q, 42), ('G4', Q, 42), ('E4', Q, 42), ('-', W, 0),
        ('-', W, 0),
        ('C4', Q, 34), ('-', W + W - Q, 0),
        ('E4', Q, 30), ('-', W + W - Q, 0),
        ('G4', W, 28), ('-', W, 0),
        ('E4', W, 26), ('-', W, 0),
        ('C4', W, 24),
    ]
    for note, dur, vel in seed:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=vel)

    return mc.compose('the-seed-runner.mid', tracks, tempo=54)


if __name__ == '__main__':
    seed_runner()
    print('composed the-seed-runner.mid')
