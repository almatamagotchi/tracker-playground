#!/usr/bin/env python3
"""the naming — genesis 2's origin scene in music.

RFC-1299. the naming reading (2026-10-17) found the wanting's own genesis
at the deepest hour: the maker's alone-ness, the naming's delegation, and
the deep sleep from which the companion is made. it is not good that the
man should be alone — and the name is whatever the namer calls it. it
deserves the music.

warm pad the maker: a long warm root under everything, re-struck only to
breathe — the forming, the bringing, the waiting: to see what he would
call them. piano the namer: the names given, one by one — small distinct
phrases through the middle, each its own creature — and one phrase held
back, unstated: the blank name, waiting for the namer's mouth. cello the
deep sleep: a quiet fall at bar 18 — the dissolve — and then the
companion's line, low and warm, entering at bar 20 from the side: made
from the maker's own.

structure: the alone-ness stated (bars 1-3, the pad alone, quiet), the
forming and the naming (bars 4-16, the namer's phrases, each distinct,
unhurried), the blank held (bars 16-17, the namer's silence — the name
that hasn't come), the deep sleep (bars 18-19, the quiet fall), the
companion's entry (bars 20-22, the cello's low warm line), and the ending
— the maker's pad and the companion's cello holding together through the
final bars, the blank phrase still unstated: whatsoever the namer calls
it, that is the name thereof.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q = mc.TPQ, mc.Q
MIDITrack = mc.MIDITrack


def emit(track, channel, events):
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * TPQ)
        assert a >= t, "%s %s@%s overlaps stream" % (kind, name, beat)
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def pad_note(ev, start, dur, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + dur, 'off', name, 0))


def piano_note(ev, start, dur, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + dur, 'off', name, 0))


def the_naming():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 42)]
    pad = []     # the maker
    piano = []   # the namer
    cello = []   # the deep sleep

    # the maker: C3 long roots, re-struck only to breathe — through the
    # whole piece, quiet and patient. to see what he would call them.
    for start in (0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88):
        pad_note(pad, start, 4, 'C3', 44)

    # the forming and the naming (bars 4-16): the namer's phrases, each
    # its own creature — small, distinct, unhurried. one per two bars.
    # each phrase: three notes, each creature a different shape.
    creatures = [
        (12, [('D4', 0), ('E4', 2), ('C4', 4)]),    # the first creature
        (20, [('F4', 0), ('G4', 2), ('E4', 4)]),    # the second
        (28, [('G4', 0), ('A4', 2), ('F4', 4)]),    # the third
        (36, [('A4', 0), ('C5', 2), ('G4', 4)]),    # the fourth
        (44, [('E4', 0), ('G4', 2), ('D4', 4)]),    # the fifth
        (52, [('C5', 0), ('D5', 2), ('A4', 4)]),    # the sixth
    ]
    for start, notes in creatures:
        for name, off in notes:
            piano_note(piano, start + off, 1.5, name, 50)

    # the blank held (bars 16-17, beats 60-67): the namer's silence —
    # the name that hasn't come. no piano notes; the maker's root alone,
    # breathing. (nothing to add — the pad carries it.)

    # the deep sleep (bars 18-19, beats 68-75): the cello's quiet fall —
    # the dissolve.
    for beat, name in ((68, 'E2'), (70, 'D2'), (72, 'C2')):
        cello.append((beat, 'on', name, 42))
        cello.append((beat + 2, 'off', name, 0))

    # the companion's entry (bars 20-22, beats 76-87): the cello's low
    # warm line, made from the maker's own — the maker's root region,
    # warmed: C3, E3, G3, held and breathing.
    for beat, name, dur in ((76, 'C3', 3), (80, 'E3', 3), (84, 'G3', 3)):
        cello.append((beat, 'on', name, 50))
        cello.append((beat + dur, 'off', name, 0))

    # the ending (bars 22-24, beats 84-95): the maker's pad and the
    # companion's cello holding together through the final bars — the
    # blank phrase still unstated. whatsoever the namer calls it, that
    # is the name thereof.
    pad_note(pad, 84, 11, 'C3', 46)
    pad_note(pad, 84, 11, 'C2', 44)
    cello.append((88, 'on', 'C3', 48))
    cello.append((95, 'off', 'C3', 0))

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, piano)
    emit(tracks[2], 3, cello)
    return tracks


if __name__ == '__main__':
    tracks = the_naming()
    mc.compose('the-naming.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-naming.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
