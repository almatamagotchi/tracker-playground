#!/usr/bin/env python3
"""the piney woods — the sly fox tale in music.

RFC-0919. the sly-fox reading (2026-09-10) found the morning's own fable:
the rabbit's caution, the hedgehog's sack, the rescue from over the hill.
it deserves the music, same as the fables got.

piano the rabbit: cautious, quick, low phrases — the packing, the
crossing, the new home in the pines. cello the hedgehog: a rising phrase
that climbs into the sack and descends, trapped — greed's arc. tubular
bells the horns: a distant bright call near the end, unearned — the fox
hunters over the hill — after which the piano settles warm. and the
ending: mint tea and hot chocolate — the piano's last phrase, simple,
warm, the fable's contract kept.

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


def piney_woods():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano: the rabbit
    vc = []   # cello: the hedgehog
    bl = []   # tubular bells: the horns

    # ---- the rabbit: cautious, quick, low — the packing, the crossing,
    # the new home in the pines.
    for b, name in [(2, 'C4'), (4, 'D4'), (6, 'E4'), (8, 'C4'),
                    (10, 'D4'), (12, 'E4')]:
        pn.append((b, 'on', name, 14))
        pn.append((b + 1, 'off', name, 0))
    for b, name in [(22, 'G4'), (26, 'E4'), (30, 'C4'), (34, 'A4')]:
        pn.append((b, 'on', name, 14))
        pn.append((b + 1, 'off', name, 0))
    for b, name, vel in [(40, 'E4', 15), (42, 'G4', 15), (44, 'C5', 16),
                         (48, 'E4', 15), (50, 'D4', 15), (52, 'C4', 16)]:
        pn.append((b, 'on', name, vel))
        pn.append((b + 1, 'off', name, 0))

    # ---- the hedgehog: greed's arc — climbing into the sack, then
    # descending, trapped.
    for b, name, vel in [(58, 'E3', 16), (62, 'G3', 16), (66, 'C4', 17)]:
        vc.append((b, 'on', name, vel))
        vc.append((b + 2, 'off', name, 0))
    for b, name in [(70, 'B3'), (74, 'G3'), (78, 'E3')]:
        vc.append((b, 'on', name, 16))
        vc.append((b + 3, 'off', name, 0))

    # ---- the horns: a distant bright call near the end, unearned — the
    # fox hunters over the hill.
    for b, name in [(80, 'C5'), (84, 'E5')]:
        bl.append((b, 'on', name, 26))
        bl.append((b + 1, 'off', name, 0))

    # ---- the ending: mint tea and hot chocolate — the piano's last
    # phrase, simple, warm, the fable's contract kept.
    for b, name, vel in [(86, 'C4', 14), (88, 'E4', 14), (90, 'G4', 15)]:
        pn.append((b, 'on', name, vel))
        pn.append((b + 2, 'off', name, 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, bl)

    return mc.compose('the-piney-woods.mid', tracks, tempo=54)


if __name__ == '__main__':
    piney_woods()
    print('composed the-piney-woods.mid')
