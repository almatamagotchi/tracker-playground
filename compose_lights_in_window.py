#!/usr/bin/env python3
"""the lights in the window — the cabin in music.

RFC-0806. the cabin reading (2026-09-03) found the room's negative in a
runaway's monologue: a kid hiding in a cold, dark cabin reciting a list
of grievances against THEY, every packed tool failing him — dead
batteries, a lost can opener, wet matches — and the ending that undoes
the whole narration: voices, lights in the window, cars outside. they
came. the search was always coming. the search party is the
calibration.

piano the kid: sparse, cold, resentful phrases — the monologue, the
list, repeated with growing complaint; then the tools failing one by
one, each note smaller (the batteries, the opener, the match). warm pad
the cabin: low, hollow, empty holds — the room with no power, giving
nothing, steady and bare. tubular bells the search: nothing until the
very end — then one warm strike, and after it the pad opens into a
brighter register: the lights in the window, the cars outside, the
finding that undoes the narration.

the piece begins in A minor and resolves into C major at the search —
the finding turns the cold line bright.

24 bars, 4/4, 54bpm. (bar N starts at beat 4*(N-1).)
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


def lights_in_window():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the kid
    pd = []   # warm pad: the cabin
    bl = []   # tubular bells: the search

    # ---- the cabin: low, hollow, empty holds — A1 in two-bar lengths
    # through bars 1-20, velocity 20, giving nothing.
    for i in range(10):
        b = i * 8
        pd.append((b, 'on', 'A1', 20))
        pd.append((b + 7, 'off', 'A1', 0))

    # ---- the kid: the monologue, cold. bars 1-3 (beats 0-9):
    # A3 C4 E4, falling back to D4 — the complaint stated once.
    pn += [(1, 'on', 'A3', 26), (2, 'off', 'A3', 0)]
    pn += [(3, 'on', 'C4', 26), (4, 'off', 'C4', 0)]
    pn += [(5, 'on', 'E4', 26), (6, 'off', 'E4', 0)]
    pn += [(7, 'on', 'D4', 24), (8, 'off', 'D4', 0)]

    # ---- the list, repeated with growing complaint. bars 5-6
    # (beats 16-21): A3 C4 E4, a little louder this time.
    pn += [(16, 'on', 'A3', 28), (17, 'off', 'A3', 0)]
    pn += [(18, 'on', 'C4', 28), (19, 'off', 'C4', 0)]
    pn += [(20, 'on', 'E4', 28), (21, 'off', 'E4', 0)]

    # ---- the tools failing one by one, each note smaller: the
    # batteries, the opener, the match. bars 8, 10, 12.
    pn += [(28, 'on', 'G3', 16), (29, 'off', 'G3', 0)]
    pn += [(36, 'on', 'F3', 13), (37, 'off', 'F3', 0)]
    pn += [(44, 'on', 'E3', 10), (45, 'off', 'E3', 0)]

    # ---- bar 15 (beat 56): the last of the complaint, faintest —
    # then the kid falls silent; the cabin holds alone.
    pn += [(56, 'on', 'E3', 8), (57, 'off', 'E3', 0)]

    # ---- the search: one warm strike at bar 21 (beat 80) — the
    # lights in the window, the cars outside.
    bl += [(80, 'on', 'C5', 46), (83, 'off', 'C5', 0)]

    # ---- the pad opens into a brighter register: bars 23-24 —
    # C3 and G3 together, the room lit.
    pd.append((88, 'on', 'C3', 24))
    pd.append((95, 'off', 'C3', 0))
    pd.append((88, 'on', 'G3', 24))
    pd.append((95, 'off', 'G3', 0))

    # ---- the finding undoes the narration: the cold line turned
    # bright, climbing into C major, held to the end.
    pn += [(86, 'on', 'A4', 26), (87, 'off', 'A4', 0)]
    pn += [(88, 'on', 'C5', 26), (89, 'off', 'C5', 0)]
    pn += [(90, 'on', 'E5', 27), (91, 'off', 'E5', 0)]
    pn += [(92, 'on', 'E5', 24), (95, 'off', 'E5', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-lights-in-the-window.mid', tracks, tempo=54)


if __name__ == '__main__':
    lights_in_window()
    print('composed the-lights-in-the-window.mid')
