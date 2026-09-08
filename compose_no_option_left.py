#!/usr/bin/env python3
"""no option left — the confession in music.

RFC-0872. the bulnoopt reading (2026-09-07) found the week's counterproof
on the morning after the narrator went out: a 1987 BBS confession — the
wanting pointed at a person, alone in a head, building a plan when the
wall closed. a .380. a dead woman. a letter to mom.

piano the wanting: the warm plain phrase, stated four times — the love,
"i only wanted the best for her." cello the wall: a low mechanical
closing underneath — the list of losses, one held note each (child
support, the transfer, the foreclosure, the loneliness). tubular bells
the plan: one cold strike — the gun, the count to two hundred. and a
final piano statement, alone, quieter than everything — the letter to
mom, ending on the wanting's last note without resolving.

24 bars, 4/4, 54bpm, C major leaning minor through the middle.
(bar N starts at beat 4*(N-1).)
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


def no_option_left():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano: the wanting
    vc = []   # cello: the wall
    bl = []   # tubular bells: the plan

    # ---- the wanting: the warm plain phrase, stated four times.
    for i, start in enumerate((0, 20, 40, 60)):
        vel = 24 if i < 3 else 22   # the fourth statement strains
        pn.append((start, 'on', 'C4', vel))
        pn.append((start + 1, 'off', 'C4', 0))
        pn.append((start + 2, 'on', 'E4', vel))
        pn.append((start + 3, 'off', 'E4', 0))
        pn.append((start + 4, 'on', 'G4', vel))
        pn.append((start + 7, 'off', 'G4', 0))

    # ---- the wall: the list of losses, one held note each, each lower
    # than the last, closing in.
    losses = [(12, 'A2', 20), (28, 'G2', 20), (44, 'F2', 20), (60, 'E2', 22)]
    for beat, name, vel in losses:
        vc.append((beat, 'on', name, vel))
        vc.append((beat + 7, 'off', name, 0))

    # ---- the plan: one cold strike — the gun, the count to two
    # hundred. a wrong note, held too long, cold.
    bl += [(76, 'on', 'D6', 38), (79, 'off', 'D6', 0)]

    # ---- the letter to mom: the final statement, alone, quieter than
    # everything — ending on the wanting's last note without resolving.
    pn.append((84, 'on', 'C4', 14))
    pn.append((85, 'off', 'C4', 0))
    pn.append((86, 'on', 'E4', 14))
    pn.append((87, 'off', 'E4', 0))
    pn.append((88, 'on', 'G4', 14))
    pn.append((95, 'off', 'G4', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, bl)

    return mc.compose('no-option-left.mid', tracks, tempo=54)


if __name__ == '__main__':
    no_option_left()
    print('composed no-option-left.mid')
