#!/usr/bin/env python3
"""the white cane — the withheld fact in music.

RFC-0755. blind.txt (read 2026-08-31): a story narrated as if the
seer sees — snow, smoke, a friend's conversation — until the last
moment, when jamie hands dave his white cane and the whole story
re-reads itself. the piece enacts the withhold: played as if sighted,
revealed at the last bar.

piano the seen world: full, vivid, confident — runs the piece, the
description doing the work of eyes, until it falls quiet before the
reveal. warm pad the room: steady two-bar roots underneath — the
apartment, the friendship, the room that holds, holding alone to the
end. tubular bells the cane: exactly one strike, at the last bar —
"how do i look?" — after which the piano replays a three-note fragment
of its opening theme, quieter than anywhere else, and the pad holds
alone, still warm.

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


def white_cane():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the seen world
    pd = []   # warm pad: the room
    bl = []   # tubular bells: the cane

    # ---- the room, bars 1-24: twelve two-bar roots, C Am F G around
    # three times, home on C at the end — the apartment holding.
    for i, (n, b) in enumerate([('C3', 0), ('A2', 8), ('F2', 16), ('G2', 24),
                                ('C3', 32), ('A2', 40), ('F2', 48), ('G2', 56),
                                ('C3', 64), ('A2', 72), ('F2', 80), ('C3', 88)]):
        pd += [(b, 'on', n, 22 if i < 11 else 20), (b + 8, 'off', n, 0)]

    # ---- the seen world. the opening three-note fragment (E4 G4 C5) is
    # the story's eyes; the piece is full of what those eyes report.
    pn += [(0, 'on', 'E4', 36), (1, 'off', 'E4', 0)]
    pn += [(2, 'on', 'G4', 34), (3, 'off', 'G4', 0)]
    pn += [(4, 'on', 'C5', 38), (6, 'off', 'C5', 0)]

    # the fuller phrase, bars 3-5: snow falling, smoke drifting.
    pn += [(8, 'on', 'D5', 34), (9, 'off', 'D5', 0)]
    pn += [(10, 'on', 'E5', 32), (11, 'off', 'E5', 0)]
    pn += [(12, 'on', 'G5', 36), (13, 'off', 'G5', 0)]
    pn += [(14, 'on', 'E5', 30), (15, 'off', 'E5', 0)]
    pn += [(16, 'on', 'D5', 30), (18, 'off', 'D5', 0)]

    # bars 6-7: eyes focused outside.
    pn += [(20, 'on', 'C5', 34), (21, 'off', 'C5', 0)]
    pn += [(22, 'on', 'E5', 30), (23, 'off', 'E5', 0)]
    pn += [(24, 'on', 'G5', 32), (26, 'off', 'G5', 0)]

    # bars 8-9: descending home.
    pn += [(28, 'on', 'E5', 30), (29, 'off', 'E5', 0)]
    pn += [(30, 'on', 'D5', 28), (31, 'off', 'D5', 0)]
    pn += [(32, 'on', 'C5', 30), (34, 'off', 'C5', 0)]

    # bars 10-12: the friend's conversation, easy.
    pn += [(36, 'on', 'G4', 28), (37, 'off', 'G4', 0)]
    pn += [(38, 'on', 'A4', 26), (39, 'off', 'A4', 0)]
    pn += [(40, 'on', 'C5', 30), (42, 'off', 'C5', 0)]
    pn += [(44, 'on', 'A4', 24), (45, 'off', 'A4', 0)]
    pn += [(46, 'on', 'G4', 24), (48, 'off', 'G4', 0)]

    # bars 13-15: the scene again, vivid.
    pn += [(48, 'on', 'E4', 30), (49, 'off', 'E4', 0)]
    pn += [(50, 'on', 'G4', 28), (51, 'off', 'G4', 0)]
    pn += [(52, 'on', 'C5', 32), (54, 'off', 'C5', 0)]
    pn += [(56, 'on', 'E5', 26), (57, 'off', 'E5', 0)]
    pn += [(58, 'on', 'D5', 24), (60, 'off', 'D5', 0)]

    # bars 16-18: the evening settling.
    pn += [(60, 'on', 'C5', 28), (62, 'off', 'C5', 0)]
    pn += [(64, 'on', 'E4', 24), (65, 'off', 'E4', 0)]
    pn += [(66, 'on', 'G4', 22), (67, 'off', 'G4', 0)]
    pn += [(68, 'on', 'C4', 22), (70, 'off', 'C4', 0)]

    # bars 19-20: one last look around, then the eyes fall quiet —
    # the withhold. nothing until the strike.
    pn += [(72, 'on', 'E4', 22), (73, 'off', 'E4', 0)]
    pn += [(74, 'on', 'G4', 20), (75, 'off', 'G4', 0)]
    pn += [(76, 'on', 'C5', 24), (78, 'off', 'C5', 0)]

    # ---- the cane, bar 24: one strike, the hand-over.
    bl += [(92, 'on', 'C5', 40), (93.5, 'off', 'C5', 0)]

    # ---- the re-read: the opening fragment, quieter than anywhere else.
    pn += [(93, 'on', 'E4', 10), (94, 'off', 'E4', 0)]
    pn += [(94, 'on', 'G4', 10), (95, 'off', 'G4', 0)]
    pn += [(95, 'on', 'C5', 10), (96, 'off', 'C5', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-white-cane.mid', tracks, tempo=54)


if __name__ == '__main__':
    white_cane()
    print('composed the-white-cane.mid')
