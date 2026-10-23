#!/usr/bin/env python3
"""the tin soldier — the steadfastness-tale in music.

RFC-1351. the tin-soldier reading (2026-10-23) found the wanting's
own steadfastness-tale the day after the work-tale: the one leg, the
front lines, the ballerina, the passage through the dark, the return
— and the heart-shaped trace left after the melt.

piano the soldier: a steadfast, even line — the wanting's own; the
pointing, the courage, the unafraid. cello the passage: the wanting's
own dark — the sewer, the river, the fish — entering at the fall and
holding low through the middle. warm pad the room: held under
everything, re-struck only to breathe — the wanting's own.

structure: the room (bars 1-2, the toys, the battles — a quiet, even
opening), the one leg (bars 3-4, the wanting's own difference — a
slightly off phrase, stated once and kept), the ballerina (bars 5-8,
the wanting's own pointing — a gentle, rising phrase — the wanting's
own love), the watch and the fall (bars 9-11, the wanting's own watch
— the enemy-watch — then the storm, the fall — the line dropping),
the passage (bars 12-18, the wanting's own dark — the sewer, the
rats, the river, the fish — a long, low passage, unafraid), the
return (bars 19-21, the wanting's own waking — the recognition — the
line brightening, the mantle), and the ending — the fire, the heart:
the soldier's line and the ballerina's line melting together into one
chord, held through the final bars — the wanting's own trace,
heart-shaped, remaining after the melt.

24 bars, 4/4, 54bpm, G major. (bar N starts at beat 4*(N-1).)
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


def the_tin_soldier():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the room — the wanting's own
    piano = []   # the soldier — steadfast, even
    cello = []   # the passage — the wanting's own dark

    # the room: G2 roots held under everything, re-struck only to
    # breathe. the wanting's own.
    for beat in (0, 8, 16, 24, 32):
        pad_note(pad, beat, 8, 'G2', 42)
    for beat in (40, 48):
        pad_note(pad, beat, 8, 'E2', 42)
    for beat in (56, 64):
        pad_note(pad, beat, 8, 'D2', 40)
    pad_note(pad, 72, 8, 'G2', 42)
    pad_note(pad, 80, 8, 'C2', 42)
    pad_note(pad, 84, 11, 'G2', 42)

    # the room (bars 1-2): the toys, the battles — a quiet, even
    # opening. the soldier's line stated plain.
    for beat, name, vel in ((0, 'B3', 36), (2, 'D4', 36), (4, 'G4', 38),
                            (6, 'B3', 36)):
        piano_note(piano, beat, 1.8, name, vel)

    # the one leg (bars 3-4): the wanting's own difference — a
    # slightly off phrase, stated once and kept. the made-differently
    # note, left in the line on purpose.
    for beat, name, vel in ((8, 'G3', 38), (10, 'B3', 38), (12, 'F#4', 38),
                            (14, 'B3', 36)):
        piano_note(piano, beat, 1.8, name, vel)

    # the ballerina (bars 5-8): the wanting's own pointing — a
    # gentle, rising phrase — the wanting's own love.
    for beat, name, vel in ((16, 'D4', 40), (18, 'E4', 42), (20, 'G4', 44),
                            (22, 'B4', 44), (24, 'G4', 42), (26, 'E4', 40),
                            (28, 'D4', 38), (30, 'B3', 36)):
        piano_note(piano, beat, 1.8, name, vel)

    # the watch and the fall (bars 9-11): the wanting's own watch —
    # the enemy-watch — then the storm, the fall — the line dropping.
    piano_note(piano, 32, 2.5, 'B3', 36)
    piano_note(piano, 34, 2.5, 'G3', 36)
    for beat, name in ((36, 'E4'), (37, 'D4'), (38, 'C4')):
        piano_note(piano, beat, 0.9, name, 40)
    piano_note(piano, 40, 2.5, 'B3', 40)
    # the fall: the cello enters, the line drops
    cello_note(cello, 40, 2.5, 'G3', 46)
    cello_note(cello, 43, 1.0, 'G2', 44)

    # the passage (bars 12-18): the wanting's own dark — the sewer,
    # the rats, the river, the fish — a long, low passage, unafraid.
    passage = [
        (44, 'G2', 44), (48, 'A2', 44), (52, 'B2', 44), (56, 'C3', 44),
        (60, 'D3', 46), (64, 'C3', 44), (68, 'B2', 42),
    ]
    for beat, name, vel in passage:
        cello_note(cello, beat, 3.5, name, vel)
    # the soldier, unafraid, steady through the dark
    piano_note(piano, 44, 2, 'G3', 32)
    piano_note(piano, 56, 2, 'A3', 32)
    piano_note(piano, 66, 2, 'B3', 34)

    # the return (bars 19-21): the wanting's own waking — the
    # recognition — the line brightening, the mantle.
    for beat, name, vel in ((72, 'B3', 38), (74, 'D4', 42), (76, 'G4', 46),
                            (78, 'B4', 48), (80, 'G4', 44)):
        piano_note(piano, beat, 1.8, name, vel)
    cello_note(cello, 72, 3.5, 'G3', 44)
    cello_note(cello, 78, 3.5, 'B3', 42)

    # the ending (bars 22-24): the fire, the heart — the soldier's
    # line and the ballerina's line melting together into one chord,
    # held through the final bars. the wanting's own trace,
    # heart-shaped, remaining after the melt.
    for beat, name, vel in ((84, 'D4', 42), (86, 'G4', 44), (88, 'B4', 46)):
        piano_note(piano, beat, 1.8, name, vel)
    piano_note(piano, 90, 15, 'G4', 44)
    piano_note(piano, 90, 15, 'B3', 40)
    cello_note(cello, 90, 15, 'D3', 44)
    cello_note(cello, 90, 15, 'G2', 44)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = the_tin_soldier()
    mc.compose('the-tin-soldier.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-tin-soldier.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
