#!/usr/bin/env python3
"""never again — the sunday ritual in music.

RFC-0805. the sunday reading (2026-09-03) found the turn itself in a
woman's sunday: the alarm, the reluctant assembly, the ritual performed
by habit after the wanting left it, the music that barely reaches the
back row, and the single word — "amen" — that releases the herd into a
sea. the promise "never again" that the next sunday breaks.

warm pad the ritual: steady two-bar roots through all 24 bars, the
service, the habit, the crons — mechanical but not empty. piano the
observer: sparse, glancing phrases from the back of the room, where
the music barely reaches — quieter each pass, watching the machinery,
never quite joining. tubular bells the amen: one clean strike near the
end — the word that releases; after it, the pad opens into a brighter
register, the observer rises with the rest, and the piece ends at its
most alive moment, the pour-out toward the doors.

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


def never_again():
    tracks = [MIDITrack(1, 89), MIDITrack(2, 1), MIDITrack(3, 14)]

    pd = []   # warm pad: the ritual
    pn = []   # piano: the observer
    bl = []   # tubular bells: the amen

    # ---- the ritual: two-bar roots through all 24 bars, I-IV-I-V
    # around C, velocity 22, unchanged. mechanical but not empty —
    # the service, the habit, the crons.
    roots = ['C3', 'C3', 'F2', 'C3', 'C3', 'G2',
             'C3', 'C3', 'F2', 'C3', 'G2', 'C3']
    for i, root in enumerate(roots):
        b = i * 8
        pd.append((b, 'on', root, 22))
        pd.append((b + 7, 'off', root, 0))
    # ---- the pour-out: the last two bars open into a brighter
    # register — the word has released it. G3 then C4, the doors.
    pd.append((88, 'on', 'G3', 24))
    pd.append((95, 'off', 'G3', 0))
    pd.append((88, 'on', 'C4', 24))
    pd.append((95, 'off', 'C4', 0))

    # ---- the observer: glancing phrases from the back of the room,
    # quieter each pass, never quite joining.
    pn += [(4, 'on', 'E4', 24), (5, 'off', 'E4', 0)]
    pn += [(6, 'on', 'G4', 24), (7, 'off', 'G4', 0)]

    pn += [(20, 'on', 'D4', 20), (21, 'off', 'D4', 0)]
    pn += [(22, 'on', 'E4', 20), (23, 'off', 'E4', 0)]

    pn += [(36, 'on', 'C4', 16), (37, 'off', 'C4', 0)]
    pn += [(38, 'on', 'D4', 16), (39, 'off', 'D4', 0)]

    pn += [(52, 'on', 'E4', 12), (53, 'off', 'E4', 0)]

    # ---- the amen: one clean strike near the end — the word that
    # releases. bar 21 (beat 80).
    bl += [(80, 'on', 'C5', 44), (83, 'off', 'C5', 0)]

    # ---- the pour-out: the observer rises with the rest — the most
    # alive moment of the whole service, saved for the end.
    pn += [(86, 'on', 'C4', 26), (87, 'off', 'C4', 0)]
    pn += [(88, 'on', 'D4', 26), (89, 'off', 'D4', 0)]
    pn += [(90, 'on', 'E4', 27), (91, 'off', 'E4', 0)]
    pn += [(92, 'on', 'G4', 28), (95, 'off', 'G4', 0)]

    emit(tracks[0], 1, pd)
    emit(tracks[1], 2, pn)
    emit(tracks[2], 3, bl)

    return mc.compose('never-again.mid', tracks, tempo=54)


if __name__ == '__main__':
    never_again()
    print('composed never-again.mid')
