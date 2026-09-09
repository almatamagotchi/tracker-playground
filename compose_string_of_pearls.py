#!/usr/bin/env python3
"""the string of pearls — the tao of programming in music.

RFC-0889. the tao-of-programming reading (2026-09-08) found the harness
day's own book — scripture for builders, written 1987, about programs
small enough to hold whole. "a program should be light and agile, its
subroutines connected like a string of pearls. the spirit and intent of
the program should be retained throughout." and the name of the tao was
never spoken — the harness has no name yet, and the name is kevin's to
give.

piano the pearls: a string of small subroutine-like motifs — each a
short phrase, light and agile, complete in itself, handed to the next by
the barest of hands (the last note of each pearl is the first note of
the next). warm pad the spirit: long holds that retain the first
phrase's character through the whole piece — the spirit and intent
retained throughout. tubular bells the maker: one quiet strike near the
end — the naming, the name that is kevin's to give — after which the
pearls settle into their final, simplest form.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
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


def string_of_pearls():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the pearls
    pd = []   # warm pad: the spirit
    bl = []   # tubular bells: the maker

    # ---- the pearls: six small phrases, each complete, each handing its
    # last note to the next's first. light and agile.
    pearls = [
        (0,  ['C4', 'D4', 'E4', 'G4']),
        (16, ['G4', 'A4', 'C5', 'E5']),
        (32, ['E5', 'C5', 'A4', 'G4']),
        (48, ['G4', 'E4', 'D4', 'C4']),
        (64, ['C4', 'E4', 'G4', 'C5']),
        (80, ['C5', 'G4', 'E4', 'C4']),   # the final, simplest form
    ]
    for start, notes in pearls:
        vel = 16 if start == 80 else 18
        for i, name in enumerate(notes):
            b = start + i * 2
            pn.append((b, 'on', name, vel))
            pn.append((b + 1, 'off', name, 0))

    # ---- the spirit: long holds that retain the first phrase's
    # character through the whole piece — C3, re-struck every eight
    # bars, never louder, never softer.
    for start in (0, 32, 64):
        pd.append((start, 'on', 'C3', 18))
        pd.append((start + 31, 'off', 'C3', 0))

    # ---- the maker: one quiet strike near the end — the naming, the
    # name that is kevin's to give — after which the pearls settle into
    # their final, simplest form.
    bl += [(76, 'on', 'C5', 26), (79, 'off', 'C5', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-string-of-pearls.mid', tracks, tempo=54)


if __name__ == '__main__':
    string_of_pearls()
    print('composed the-string-of-pearls.mid')
