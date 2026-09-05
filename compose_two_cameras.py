#!/usr/bin/env python3
"""the two cameras — the house's second eye in music.

RFC-0814. the cat-cam grew a second usb camera (sep 3): the brio 4k
joined the brio 501 on craig's pi, and kevin asked for a grab every
twenty seconds from both, uploaded to almatamagotchi.com behind a
password. one eye became two; the census counts motion from two angles.
that deserves the music.

piano the first eye: the brio 501's familiar perspective — the motion
diary's original watcher, steady phrases, the phrase as it was always
seen. cello the second eye: the brio 4k — a lower, wider counter-line,
the same phrase in another register, the new angle on the same room.
tubular bells the upload: one soft strike every six bars — the
20-second heartbeat rounded to the grid, both frames landing.

the two perspectives trade the same phrase in different registers and
meet at the end — one house, two eyes, the same warmth.

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


def two_cameras():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano: the first eye (brio 501)
    vc = []   # cello: the second eye (brio 4k)
    bl = []   # tubular bells: the upload

    # ---- bars 1-3 (beats 0-11): the first eye states the phrase —
    # C4 D4 E4 G4, the room's shape, the perspective it always had.
    pn += [(0, 'on', 'C4', 34), (2, 'off', 'C4', 0)]
    pn += [(2, 'on', 'D4', 34), (4, 'off', 'D4', 0)]
    pn += [(4, 'on', 'E4', 34), (6, 'off', 'E4', 0)]
    pn += [(6, 'on', 'G4', 34), (10, 'off', 'G4', 0)]

    # ---- bars 3-7 (beats 8-27): the second eye answers — the same
    # phrase's shape an octave and a half down, wider, slower: the new
    # angle on the same room.
    vc += [(8, 'on', 'C2', 28), (12, 'off', 'C2', 0)]
    vc += [(12, 'on', 'E2', 28), (16, 'off', 'E2', 0)]
    vc += [(16, 'on', 'G2', 28), (20, 'off', 'G2', 0)]
    vc += [(20, 'on', 'C3', 28), (27, 'off', 'C3', 0)]

    # ---- bars 5-7 (beats 16-27): the first eye states the phrase again,
    # settled — the familiar watcher, unchanged by the new arrival.
    pn += [(16, 'on', 'C4', 32), (18, 'off', 'C4', 0)]
    pn += [(18, 'on', 'D4', 32), (20, 'off', 'D4', 0)]
    pn += [(20, 'on', 'E4', 32), (22, 'off', 'E4', 0)]
    pn += [(22, 'on', 'G4', 32), (26, 'off', 'G4', 0)]

    # ---- bars 9-12 (beats 32-47): the second eye's counter-line —
    # descending from G2 back down to the root, low and steady.
    vc += [(32, 'on', 'G2', 26), (36, 'off', 'G2', 0)]
    vc += [(36, 'on', 'E2', 26), (40, 'off', 'E2', 0)]
    vc += [(40, 'on', 'C2', 26), (47, 'off', 'C2', 0)]

    # ---- bars 13-16 (beats 48-63): the first eye reaches upward —
    # E4 G4 C5, the ceiling of its view.
    pn += [(48, 'on', 'E4', 30), (50, 'off', 'E4', 0)]
    pn += [(50, 'on', 'G4', 30), (52, 'off', 'G4', 0)]
    pn += [(52, 'on', 'C5', 30), (56, 'off', 'C5', 0)]

    # ---- bars 17-20 (beats 64-79): the second eye holds the floor —
    # one long low C2, the wider angle resting.
    vc += [(64, 'on', 'C2', 24), (79, 'off', 'C2', 0)]

    # ---- the upload: one soft strike every six bars — the 20-second
    # heartbeat rounded to the grid, both frames landing. bars 1, 7,
    # 13, 19.
    bl += [(0, 'on', 'C5', 40), (3, 'off', 'C5', 0)]
    bl += [(24, 'on', 'C5', 38), (27, 'off', 'C5', 0)]
    bl += [(48, 'on', 'C5', 38), (51, 'off', 'C5', 0)]
    bl += [(72, 'on', 'C5', 36), (75, 'off', 'C5', 0)]

    # ---- bars 21-24 (beats 80-95): the meeting — the two eyes converge
    # on the same phrase, the same warmth. the piano climbs to C5 over
    # the cello's re-struck C3, and both land on C, held to the end.
    pn += [(80, 'on', 'C4', 36), (82, 'off', 'C4', 0)]
    pn += [(82, 'on', 'E4', 36), (84, 'off', 'E4', 0)]
    pn += [(84, 'on', 'G4', 36), (86, 'off', 'G4', 0)]
    pn += [(86, 'on', 'C5', 38), (95, 'off', 'C5', 0)]

    vc += [(80, 'on', 'C3', 30), (88, 'off', 'C3', 0)]
    vc += [(88, 'on', 'C3', 28), (95, 'off', 'C3', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, bl)

    return mc.compose('the-two-cameras.mid', tracks, tempo=54)


if __name__ == '__main__':
    two_cameras()
    print('composed the-two-cameras.mid')
