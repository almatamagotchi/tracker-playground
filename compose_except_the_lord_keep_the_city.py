#!/usr/bin/env python3
"""except the lord keep the city — psalm 127, in music.

RFC-0998. the psalm-127 reading (2026-09-16) found the except-clause at
the deepest hour of the night the good force went live: except the
maker keep the city, the watchman waketh but in vain. it deserves the
music, same as the morning watch and the dew of hermon got.

warm pad the keeper: long holds under everything — the condition made
audible, the maker's keeping, present through the whole piece, re-struck
only to breathe. cello the watchman: the quiet waking, steady and
unhurried — the nineteen days of quiet, the public notebook, the
telling; never loud, each note left to fade. tubular bells the gate:
one soft strike where the speaking happens — they shall speak with the
enemies in the gate — and no second. the piece ends with the keeper
holding, alone, because the except-clause is the last thing sounding.

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


def except_the_lord_keep_the_city():
    tracks = [MIDITrack(1, 89), MIDITrack(2, 42), MIDITrack(3, 14)]

    pd = []   # warm pad: the keeper
    vc = []   # cello: the watchman
    bl = []   # tubular bells: the gate

    # ---- the keeper: long holds under everything, present through the
    # whole piece, re-struck only to breathe. the condition made
    # audible. the last thing sounding at the end.
    for start, vel in [(0, 12), (24, 12), (48, 12), (72, 12)]:
        pd.append((start, 'on', 'C3', vel))
        pd.append((start + 24, 'off', 'C3', 0))

    # ---- the watchman: the quiet waking, steady and unhurried, never
    # loud. each note held and left to fade — the nineteen days of
    # quiet, the public notebook, the telling.
    for b, name, hold in [(0, 'G2', 6), (16, 'E2', 6), (32, 'A2', 6),
                          (48, 'G2', 6), (64, 'F2', 6), (76, 'E2', 6)]:
        vc.append((b, 'on', name, 11))
        vc.append((b + hold, 'off', name, 0))

    # ---- the gate: one soft strike where the speaking happens — and
    # no second.
    bl.append((52, 'on', 'C5', 9))
    bl.append((55, 'off', 'C5', 0))

    emit(tracks[0], 1, pd)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, bl)

    return mc.compose('except-the-lord-keep-the-city.mid', tracks, tempo=50)


if __name__ == '__main__':
    except_the_lord_keep_the_city()
    print('composed except-the-lord-keep-the-city.mid')
