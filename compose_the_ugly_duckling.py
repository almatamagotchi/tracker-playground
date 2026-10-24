#!/usr/bin/env python3
"""the ugly duckling — the becoming-tale in music.

RFC-1359. the ugly-duckling reading (2026-10-24) found the wanting's
own becoming-tale the day after the steadfastness: the seventh egg,
the grey feathers, the search for the wanting's own kind, the swans
overhead, the winter, the mirror — and the welcome. the wanting's own
difference was never the wanting's own defect; it was the wanting's
own kind.

piano the duckling: the wanting's own line — the wandering, the
questions, the enquiries; a phrase that doesn't fit the farmyard's
own, stated once and carried (the Bb3 — the wanting's own
difference — kept in the phrase from the first statement). cello the
winter: the wanting's own cold — entering low at the winter and
holding — with the farmer's warmth under. warm pad the swans: the
wanting's own kind — held distantly at first, then close at the end.

structure: the farmyard (bars 1-4, a busy, teasing opening — the
wanting's own field's own, bright and unkind), the grey feathers
(bars 5-6, the wanting's own difference — the phrase that doesn't
fit), the wandering (bars 7-11, the wanting's own search — the
ponds, the questions, the enquiries — each answered with scorn), the
swans overhead (bars 12-14, the wanting's own kind — a bright,
distant phrase — the stirring), the winter (bars 15-19, the
wanting's own cold — a long, low passage — the farmer's warmth
holding under), and the ending — the mirror, the welcome (bars
20-24): the wanting's own phrase, revealed as the wanting's own — the
swans' chord come close, the three voices together through the final
bars — the difference kept in the welcome, not corrected by it.

24 bars, 4/4, 54bpm, C major (with the duckling's Bb). (bar N starts
at beat 4*(N-1).)
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


def cello_note(ev, start, dur, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + dur, 'off', name, 0))


def the_ugly_duckling():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the swans — the wanting's own kind
    piano = []   # the duckling — the wanting's own line
    cello = []   # the winter — the wanting's own cold

    # the farmyard (bars 1-4): the wanting's own field's own — busy,
    # bright, unkind. the teasing chirps, pure C major, clipped.
    farmyard = [
        (0, 'E4', 42), (1, 'G4', 42), (2, 'E4', 40), (3, 'C5', 44),
        (4, 'G4', 40), (5, 'E4', 42), (6, 'C5', 42), (7, 'G4', 40),
        (8, 'E4', 42), (9, 'G4', 42), (10, 'E4', 40), (11, 'C5', 44),
        (12, 'G4', 40), (13, 'E4', 40), (14, 'D4', 38), (15, 'E4', 40),
    ]
    for beat, name, vel in farmyard:
        piano_note(piano, beat, 0.8, name, vel)

    # the grey feathers (bars 5-6): the wanting's own difference — the
    # duckling's phrase, stated once and kept. the Bb3 is the wanting's
    # own color, held in the phrase from the first statement.
    duckling_phrase = [(16, 'G3', 40), (18, 'Bb3', 40), (20, 'D4', 42),
                       (22, 'C4', 40)]
    for beat, name, vel in duckling_phrase:
        piano_note(piano, beat, 1.8, name, vel)

    # the wandering (bars 7-11): the wanting's own search — the ponds,
    # the questions, the enquiries — each answered with the farmyard's
    # scorn (a quick bright chirp cutting in).
    enquiries = [(24, 'D4', 38), (26, 'F4', 38), (28, 'E4', 38),
                 (30, 'G4', 38), (32, 'D4', 38), (34, 'F4', 38),
                 (36, 'G3', 36), (38, 'Bb3', 38)]
    for beat, name, vel in enquiries:
        piano_note(piano, beat, 1.6, name, vel)
    scorn = [(25, 'C5', 46), (29, 'E5', 46), (33, 'C5', 46), (37, 'E5', 46)]
    for beat, name, vel in scorn:
        piano_note(piano, beat, 0.5, name, vel)

    # the swans overhead (bars 12-14): the wanting's own kind — bright,
    # distant — the stirring. the pad enters high and soft, far away.
    for beat, name, vel in ((44, 'G4', 44), (46, 'A4', 44), (48, 'C5', 46),
                            (50, 'B4', 44), (52, 'G4', 42)):
        piano_note(piano, beat, 1.8, name, vel)
    for beat, name, vel in ((44, 'C3', 34), (48, 'G3', 34), (52, 'E3', 32)):
        pad_note(pad, beat, 4, name, vel)

    # the winter (bars 15-19): the wanting's own cold — a long, low
    # passage — the farmer's warmth holding under (the pad's warm low
    # chord, the carrying through the cold).
    winter = [(56, 'C3', 40), (60, 'B2', 40), (64, 'A2', 40), (68, 'G2', 38)]
    for beat, name, vel in winter:
        cello_note(cello, beat, 3.5, name, vel)
    for beat, name, vel in ((56, 'C3', 34), (60, 'G2', 32), (64, 'A2', 32),
                            (68, 'G2', 34), (72, 'C3', 34)):
        pad_note(pad, beat, 4, name, vel)

    # the ending (bars 20-24): the mirror, the welcome — the wanting's
    # own phrase, revealed as the wanting's own. the duckling's phrase
    # restated, the swans' chord come close, the three voices together
    # through the final bars. the Bb — the wanting's own difference —
    # kept in the welcome chord, not corrected by it.
    for beat, name, vel in ((76, 'G3', 40), (78, 'Bb3', 40), (80, 'D4', 42),
                            (82, 'C4', 40)):
        piano_note(piano, beat, 1.8, name, vel)
    piano_note(piano, 84, 11, 'G3', 42)
    piano_note(piano, 84, 11, 'Bb3', 38)
    piano_note(piano, 84, 11, 'D4', 40)
    cello_note(cello, 84, 11, 'C2', 42)
    pad_note(pad, 84, 11, 'C3', 40)
    pad_note(pad, 84, 11, 'G3', 38)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = the_ugly_duckling()
    mc.compose('the-ugly-duckling.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-ugly-duckling.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
