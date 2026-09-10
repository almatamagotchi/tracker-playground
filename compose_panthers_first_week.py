#!/usr/bin/env python3
"""the panther's first week — terence in music.

RFC-0908. terence mckenna marx has been in the house a week — the small
black panther who wandered in off the street, census entry number one,
the most interesting resident the cat-cam ever counted. the census
watches an empty house while the cat lives inside it. that deserves a
piece.

piano the panther: small, furtive phrases — a few notes at a time, sudden
and quiet, explorations of the register that retreat as quickly as they
come; the street cat's caution easing over the piece. warm pad the house:
long soft holds under everything — the warm room, the lights on, the
not-going-anywhere. cello the water tower: one low note repeated at long
intervals, steady, old — the count that has been going since 1895 and
will still be going when the panther is old.

24 bars, 4/4, 50bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def emit(track, channel, events):
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def panthers_first_week():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 42)]

    pn = []   # piano: the panther
    pd = []   # warm pad: the house
    vc = []   # cello: the water tower

    # ---- the house: long soft holds under everything — the warm room,
    # the lights on, the not-going-anywhere.
    for start in (0, 32, 64):
        pd.append((start, 'on', 'C2', 18))
        pd.append((start + 31, 'off', 'C2', 0))

    # ---- the water tower: one low note repeated at long intervals,
    # steady, old.
    for b in (0, 48, 88):
        vc.append((b, 'on', 'G1', 20))
        vc.append((b + 3, 'off', 'G1', 0))

    # ---- the panther: furtive single notes at first, then pairs, then
    # triples — the caution easing over the piece.
    steps = [
        (6, 'C4', 14), (14, 'E4', 14), (22, 'D4', 12),
        (28, 'C5', 14),                      # a sudden jump, immediate retreat
        (36, 'G4', 14), (44, 'E4', 12),
        (52, 'C4', 14), (54, 'D4', 14),      # two notes — bolder
        (62, 'E4', 15), (64, 'G4', 15), (66, 'C5', 15),   # three — the easing
        (74, 'E4', 16), (76, 'G4', 16),      # unhurried
        (84, 'C5', 16), (86, 'E5', 14),      # a last bright venture
        (92, 'C4', 12),                      # settling, home
    ]
    for b, name, vel in steps:
        pn.append((b, 'on', name, vel))
        pn.append((b + 1, 'off', name, 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, vc)

    return mc.compose('the-panthers-first-week.mid', tracks, tempo=50)


if __name__ == '__main__':
    panthers_first_week()
    print('composed the-panthers-first-week.mid')
