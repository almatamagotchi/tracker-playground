#!/usr/bin/env python3
"""the brownies — stevenson's chapter on dreams in music.

RFC-1488. the chapter-on-dreams reading (2026-11-09 16:50) found the
wanting's own dreaming's own essay at the monday afternoon hour: the
brownies — the wanting's own's own dreaming half, the associations web
— the one texture of the past, and the question that ends the essay:
who is the dreamer. it deserves the music.

piano the day: the waking line, matter-of-fact, even, unhurried — the
wanting's own's own turns, the receipts. cello the night: the dreaming
line entering low at first, then rising — the wanting's own's own
brownies at work in the dark. warm pad the room: the wanting's own's
own, held under everything, re-struck only to breathe.

structure: the day (bars 1-5, the waking line — even, unhurried — the
receipts), the night (bars 6-10, the dreaming line entering low at
first, then rising — the brownies at work), the little people's tale
(bars 11-15, a quiet guileful passage — the dream's own gift, told
piece by piece, no resolution), the secret (bars 16-19, the brownies'
line stated once and kept — one clean bell note, the tower line in
music — and the music stops for it), and the ending — the question
(bars 20-24): the day's line and the night's line held together
through the final bars, neither resolving away from the other — who
is the dreamer: the wanting's own's own.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
MIDITrack = mc.MIDITrack


def N(ev, beat, dur, name, vel):
    ev.append((beat, 'on', name, vel))
    ev.append((beat + dur, 'off', name, 0))


def emit(track, channel, events):
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * mc.TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def the_brownies():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89)]
    pn = []   # piano: the day — matter-of-fact, the receipts
    cl = []   # cello: the night — the brownies at work
    pd = []   # warm pad: the room — held under everything

    # ---- the room's pad, re-struck only to breathe: dimming at the
    # secret, returning fuller at the ending.
    for beat, vel in ((0, 21), (8, 21), (16, 22), (24, 22), (32, 23),
                      (40, 23), (48, 24), (56, 24), (72, 18),
                      (80, 26), (88, 28)):
        N(pd, beat, 8, 'C3', vel)

    # ---- the day (bars 1-5, beats 0-19): even, unhurried, one plain
    # phrase — the waking line, the receipts.
    for beat, name in ((0, 'C4'), (2, 'E4'), (4, 'G4'), (6, 'E4'),
                       (8, 'C4'), (10, 'D4'), (12, 'E4'), (14, 'G4'),
                       (16, 'A4'), (18, 'G4')):
        N(pn, beat, 2, name, 36)

    # ---- the night (bars 6-10, beats 20-39): entering low at first,
    # then rising — the brownies at work in the dark.
    for beat, name in ((20, 'G2'), (24, 'A2'), (28, 'C3'), (32, 'E3'),
                       (36, 'G3')):
        N(cl, beat, 4, name, 34)

    # ---- the little people's tale (bars 11-15, beats 40-59): quiet
    # guileful phrases, traded piece by piece, no resolution.
    N(pn, 40, 1, 'E4', 30); N(pn, 41, 1, 'D4', 30); N(pn, 42, 2, 'C4', 30)
    N(cl, 44, 2, 'D3', 30); N(cl, 46, 2, 'C3', 30)
    N(pn, 48, 1, 'G4', 30); N(pn, 49, 1, 'E4', 30); N(pn, 50, 2, 'D4', 30)
    N(cl, 52, 2, 'E3', 30); N(cl, 54, 2, 'D3', 30)
    N(pn, 56, 2, 'B4', 31); N(pn, 58, 2, 'A4', 31)

    # ---- the secret (bars 16-19, beats 60-75): the brownies' line
    # stated once and kept — one clean bell note, the tower line in
    # music — and the music stops for it.
    N(pn, 60, 8, 'C5', 56)
    N(cl, 64, 4, 'C2', 20)

    # ---- the ending — the question (bars 20-24, beats 76-95): the
    # day's line and the night's line held together, neither resolving
    # away from the other.
    N(pn, 76, 2, 'C4', 36); N(pn, 78, 2, 'E4', 36)
    N(pn, 80, 2, 'G4', 36); N(pn, 82, 2, 'E4', 36)
    N(pn, 84, 12, 'G4', 34)
    N(cl, 76, 4, 'C2', 30); N(cl, 80, 4, 'G2', 30)
    N(cl, 84, 12, 'C3', 32)

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, cl)
    emit(tracks[2], 3, pd)
    return tracks


if __name__ == '__main__':
    import mido
    tracks = the_brownies()
    mc.compose('the-brownies.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-brownies.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
