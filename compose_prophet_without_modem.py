#!/usr/bin/env python3
"""the prophet without a modem — gibson in music.

RFC-0918. the gibson reading (2026-09-10) found the harness week's own
interviewer at the pre-dawn hour: the prophet of cyberspace who has no
modem, the future that never arrives as the map says, the actor who
taught the author his own character, and the admission that the future
was never the product. the prophecy is furniture; the story is the
staying.

piano the prophecy: a bright, certain phrase stated twice with conviction
— the imagined future, the design doc. cello the actual: enters at bar 9
as a variation on the prophecy's notes in a different order, wandering
wider — the future that outran the map, aids, the collapse, terence, the
harness. warm pad the territory: steady two-bar roots through all 24
bars — the story under both, the ground they walk on. the two interleave
without reconciling — the prophecy restated, the actual diverging further
— and the piece ends not on the prophecy's confident cadence but on the
actual's version, a phrase that began as the prophecy's and became its
own, held softly over the territory: the story told, foremost.

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


def prophet_without_modem():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89)]

    pn = []   # piano: the prophecy
    vc = []   # cello: the actual
    pd = []   # warm pad: the territory

    # ---- the territory: steady two-bar roots through all 24 bars.
    roots = ['C3', 'C3', 'A2', 'A2', 'F2', 'F2', 'C3', 'C3',
             'G2', 'G2', 'C3', 'C3']
    for i, name in enumerate(roots):
        b = i * 8
        pd.append((b, 'on', name, 16))
        pd.append((b + 7, 'off', name, 0))

    # ---- the prophecy: a bright, certain phrase, stated twice, then
    # restated once more late.
    phrase = [('C4', 2), ('E4', 4), ('G4', 6), ('C5', 8)]
    for start in (0, 16, 56):
        for name, off in phrase:
            b = start + off
            pn.append((b, 'on', name, 22 if start != 56 else 20))
            pn.append((b + 1, 'off', name, 0))

    # ---- the actual: enters at bar 9 as a variation on the prophecy's
    # notes in a different order, wandering wider.
    actual = [
        (34, 'E3', 18), (38, 'C3', 18), (42, 'G2', 18), (46, 'E3', 18),
        (50, 'A2', 18), (54, 'F2', 18),
        (60, 'D3', 18), (66, 'B2', 18), (72, 'G2', 18), (76, 'E2', 18),
    ]
    for b, name, vel in actual:
        vc.append((b, 'on', name, vel))
        vc.append((b + 2, 'off', name, 0))

    # ---- the ending: the actual's version — the prophecy's first three
    # notes an octave down, re-ordered, ending on E not C, held softly
    # over the territory's last root: the story told, foremost.
    for b, name in [(82, 'C3'), (84, 'E3'), (86, 'G3'), (88, 'E3')]:
        vc.append((b, 'on', name, 15))
        vc.append((b + 2, 'off', name, 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, pd)

    return mc.compose('the-prophet-without-a-modem.mid', tracks, tempo=54)


if __name__ == '__main__':
    prophet_without_modem()
    print('composed the-prophet-without-a-modem.mid')
