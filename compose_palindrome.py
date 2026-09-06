#!/usr/bin/env python3
"""the palindrome — the backmasking reading in music.

RFC-0833. the backmasking reading (2026-09-05) found the week's own
essay: four ways to hide a voice on a record, the satanic panic that
became law because no one could check, and the actual decoded messages —
welcomes, jokes, gospel. zappa's "ya hozna" was the answer: an entirely
backward composition that sounds about the same forward and backward. a
palindrome.

the piece IS the palindrome: bars 1-12 state the theme forward; bars
13-24 are bars 1-12 in exact retrograde — the same note events in
reverse order, velocities intact, rests mirrored, generated
programmatically by reversing the event list. the intervals between
consecutive notes come out inverted, the way reversed syllables do.

piano the record: the theme forward, then heard again as the reversed
thing. warm pad the groove: steady two-bar roots through all 24 bars —
the medium itself, unchanged by the direction of the reading. tubular
bells the splice: one strike at the midpoint — the tape, turned end for
end. the piece ends where it began: the same note, the same place.

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


def palindrome():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the record
    pd = []   # warm pad: the groove
    bl = []   # tubular bells: the splice

    # ---- the groove: steady two-bar fifth roots through all 24 bars,
    # never changing — the medium itself.
    for i in range(12):
        b = i * 8
        pd.append((b, 'on', 'C3', 20))
        pd.append((b + 7, 'off', 'C3', 0))
        pd.append((b, 'on', 'G3', 20))
        pd.append((b + 7, 'off', 'G3', 0))

    # ---- the forward theme (beats 0-47). each event: (on, off, note, vel).
    forward = [
        (2, 3, 'E4', 30),
        (5, 6, 'G4', 28),
        (8, 11, 'C5', 32),
        (13, 14, 'D4', 26),
        (16, 17, 'E4', 30),
        (20, 23, 'A4', 28),
        (26, 27, 'G4', 30),
        (29, 30, 'E4', 26),
        (33, 36, 'C5', 34),
        (38, 39, 'D5', 30),
        (41, 42, 'C5', 28),
        (44, 47, 'E4', 24),
    ]
    for on, off, name, vel in forward:
        pn.append((on, 'on', name, vel))
        pn.append((off, 'off', name, 0))

    # ---- the retrograde half, generated programmatically: the event
    # list reversed. an event at [on, off] mirrors to [95-off, 95-on].
    for on, off, name, vel in reversed(forward):
        pn.append((95 - off, 'on', name, vel))
        pn.append((95 - on, 'off', name, 0))

    # ---- the splice: one strike at the midpoint (beat 48) — the tape,
    # turned end for end.
    bl += [(48, 'on', 'C6', 44), (51, 'off', 'C6', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-palindrome.mid', tracks, tempo=54)


if __name__ == '__main__':
    palindrome()
    print('composed the-palindrome.mid')
