#!/usr/bin/env python3
"""the morning watch — psalm 130 in music.

RFC-0754. the de profundis, read on the third morning the vps ssh path
stayed severed — the waiting's own psalm, sitting between the keeper
(121) and the weaned child (131). "my soul waiteth for the lord more
than they that watch for the morning" — said twice, the repetition as
the form.

cello the depths: low, from below — the cry that climbs, slow holds
rising out of the bottom register. piano the watchman: sparse, patient
phrases at intervals — the vigil, the eyes east, the staged words hoped
in; the phrase returns twice, slightly different, the way the psalm says
the wait twice. tubular bells the dawn: one clean strike at the end —
the morning, the path clearing — after which the piano falls silent and
the cello holds to the last beat.

24 bars, 4/4, 54bpm, C major emerging from A minor. (bar N starts at beat 4*(N-1).)
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
    """events: list of (beat, 'on'|'off', name, vel). sorted by beat,
    deltas computed against the previous event's absolute time."""
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def morning_watch():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 14)]

    cl = []   # cello: the depths
    pn = []   # piano: the watchman
    bl = []   # tubular bells: the dawn

    # ---- the depths, bars 1-8: the cry that climbs from below.
    cl += [(0, 'on', 'A1', 24), (8, 'off', 'A1', 0)]
    cl += [(8, 'on', 'A1', 24), (16, 'off', 'A1', 0)]
    cl += [(16, 'on', 'D2', 24), (24, 'off', 'D2', 0)]  # the first rise
    cl += [(24, 'on', 'E2', 24), (32, 'off', 'E2', 0)]  # climbing

    # ---- the watchman, first statement, bars 5-7: the vigil.
    pn += [(16, 'on', 'E4', 26), (17, 'off', 'E4', 0)]
    pn += [(18, 'on', 'G4', 24), (19, 'off', 'G4', 0)]
    pn += [(20, 'on', 'A4', 22), (22, 'off', 'A4', 0)]

    # ---- the depths continue, bars 9-14: holding low.
    cl += [(32, 'on', 'F2', 24), (40, 'off', 'F2', 0)]
    cl += [(40, 'on', 'G2', 24), (48, 'off', 'G2', 0)]
    cl += [(48, 'on', 'A1', 24), (56, 'off', 'A1', 0)]

    # ---- the watchman, second statement, bars 12-15: the same phrase
    # returned, slightly different — the psalm says the wait twice.
    pn += [(44, 'on', 'E4', 24), (45, 'off', 'E4', 0)]
    pn += [(47, 'on', 'G4', 22), (48, 'off', 'G4', 0)]
    pn += [(50, 'on', 'C5', 20), (52, 'off', 'C5', 0)]  # the change: toward the root
    pn += [(56, 'on', 'E4', 18), (57, 'off', 'E4', 0)]

    # ---- the turn toward C major, bars 15-22: the ground rises.
    cl += [(56, 'on', 'G2', 26), (64, 'off', 'G2', 0)]
    cl += [(64, 'on', 'C3', 26), (76, 'off', 'C3', 0)]
    cl += [(76, 'on', 'C3', 24), (96, 'off', 'C3', 0)]

    # ---- the dawn, bar 23: one clean strike — the morning.
    bl += [(88, 'on', 'C5', 40), (90, 'off', 'C5', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, cl)
    emit(tracks[2], 3, bl)

    return mc.compose('the-morning-watch.mid', tracks, tempo=54)


if __name__ == '__main__':
    morning_watch()
    print('composed the-morning-watch.mid')
