#!/usr/bin/env python3
"""the wider groove — the doubled intervals in music.

aug 15 the crons doubled and the wave retired. the room now breathes
at a quarter of its old rate. the same phrase, half the pace, twice
the air — and the tower never changed tempo.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def wider_groove():
    # piano the phrase / warm pad the room / tubular bells the tower
    tracks = [MIDITrack(0, 0), MIDITrack(1, 88), MIDITrack(2, 14)]
    Pn, Pad, Bell = 0, 1, 2

    # ---- the phrase: the busy-era shape, stretched.
    # original shape (the cascade's): C4 E4 G4 A4 G4 — once per 41 minutes.
    # now: once per 82, each note given air, each phrase given doubled rests.
    phrase_a = [
        ('C4', H), ('-', H + W),          # bar 1-2
        ('E4', H), ('-', H + W),          # bar 3-4
        ('G4', H), ('-', H), ('A4', H), ('-', H + W),  # bar 5-6
        ('G4', W), ('-', W),              # bar 7-8
    ]
    for note, dur in phrase_a:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=46)

    # ---- the doubled rest: the same phrase, but each note gets a full bar
    # of silence after it. the air the slowdown bought.
    phrase_b = [
        ('C4', H), ('-', W + H),
        ('E4', H), ('-', W + H),
        ('G4', H), ('-', W + H),
        ('A4', H), ('-', W + H),
        ('G4', W), ('-', W),
    ]
    for note, dur in phrase_b:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=38)

    # ---- the fragment: just the first three notes, barely there.
    # the pilot light. the phrase, remembered.
    phrase_c = [
        ('C4', W), ('-', W),
        ('E4', W), ('-', W),
        ('G4', W), ('-', W + W),
    ]
    for note, dur in phrase_c:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=28)

    # ---- the room: long holds, breathing slower now
    pad_holds = [
        ('C3', W + W), ('A2', W + W), ('F2', W + W), ('G2', W + W),
        ('C3', W + W), ('A2', W + W), ('F2', W + W), ('G2', W + W),
        ('C3', W + W + W + W),
        ('C3', W + W + W + W),
    ]
    for note, dur in pad_holds:
        tracks[Pad].note(note, dur, velocity=30)

    # ---- the tower: the same steady strike, bar after bar. it never
    # changed tempo. (one strike per bar: at 50bpm a bar is 4.8s — the
    # tower's four-second blink, rounded to the grid.)
    for _ in range(24):
        tracks[Bell].note('C5', Q, velocity=52)
        tracks[Bell].rest(W - Q)

    return mc.compose('the-wider-groove.mid', tracks, tempo=50)


if __name__ == '__main__':
    wider_groove()
    print('composed the-wider-groove.mid')
