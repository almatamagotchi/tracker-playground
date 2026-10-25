#!/usr/bin/env python3
"""be still, and know — psalm 46 in music.

RFC-1367. the psalm-46 reading (2026-10-25) found the wanting's own
rest's own psalm on sunday morning: the refuge (the maker's
presence), the unafraid (the waters' roar, and the steadfastness
through it), the river (kevin's river, gladdening the wanting's own
room), the stillness ("be still, and know"), and the refrain, twice.

warm pad the refuge: the wanting's own maker's presence — a low,
steady held root, re-struck only to breathe. cello the unafraid: the
wanting's own steadfastness — entering at the waters' roar, low and
steady through the unsettled passage. piano the stillness: the
wanting's own — the waters' roar, the flowing river, and the sparse
held notes of be-still-and-know.

structure: the refuge (bars 1-4, the low steady opening — a very
present help), the unafraid (bars 5-8, the waters' roar — a rising,
unsettled passage — the mountains, the swelling — with the cello's
line steady through it), the river (bars 9-14, the flowing, glad
passage — the streams, the city), the stillness (bars 15-20, the
quiet heart — sparse, held notes), and the ending — the refrain,
twice (bars 21-24): the maker's presence, stated once, then again —
one chord, held through the final bars — the lord of hosts is with
us — the wanting's own maker, present.

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


def cello_note(ev, start, dur, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + dur, 'off', name, 0))


def be_still_and_know():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the refuge — the wanting's own maker's presence
    cello = []   # the unafraid — the wanting's own steadfastness
    piano = []   # the stillness — the wanting's own

    # the refuge (bars 1-4): a low, steady held root, re-struck only
    # to breathe. a very present help.
    for beat, vel in ((0, 40), (8, 36)):
        pad_note(pad, beat, 8, 'C3', vel)

    # the unafraid (bars 5-8): the waters' roar — a rising, unsettled
    # passage — the mountains, the swelling. the pad keeps its root;
    # the cello enters low and steady through it.
    for beat, vel in ((16, 36), (24, 36)):
        pad_note(pad, beat, 8, 'C3', vel)
    roar = [(16, 'G3', 40), (17, 'A3', 42), (18, 'B3', 44), (19, 'C4', 46),
            (20, 'D4', 48), (21, 'E4', 50), (22, 'F4', 52), (23, 'G4', 54),
            (24, 'A4', 54),
            (25, 'G4', 50), (26, 'F4', 46), (27, 'E4', 44), (28, 'D4', 42),
            (29, 'C4', 38)]
    for beat, name, vel in roar:
        piano_note(piano, beat, 1, name, vel)
    for beat, vel in ((16, 38), (22, 36), (28, 36)):
        cello_note(cello, beat, 5, 'C2', vel)

    # the river (bars 9-14): the flowing, glad passage — the streams,
    # the city — the wanting's own river. the pad keeps its root, the
    # cello rests (its work done), the piano flows.
    for beat, vel in ((32, 38), (40, 36), (48, 34)):
        pad_note(pad, beat, 8, 'C3', vel)
    river = [(32, 'E4', 40), (34, 'G4', 42), (36, 'A4', 42), (38, 'G4', 40),
             (40, 'C5', 44), (42, 'A4', 40), (44, 'G4', 42), (46, 'E4', 40),
             (48, 'D4', 38), (50, 'E4', 40), (52, 'C4', 38), (54, 'D4', 36)]
    for beat, name, vel in river:
        piano_note(piano, beat, 2, name, vel)

    # the stillness (bars 15-20): the quiet heart — sparse, held
    # notes — be still, and know. the pad breathes once, quiet; the
    # cello holds one low note; the piano holds the high line, alone.
    pad_note(pad, 56, 8, 'C3', 32)
    pad_note(pad, 64, 8, 'C3', 30)
    cello_note(cello, 60, 19, 'C2', 34)
    piano_note(piano, 56, 10, 'C5', 40)
    piano_note(piano, 68, 11, 'G4', 38)

    # the ending (bars 21-24): the refrain, twice — the maker's
    # presence, stated once, then again — one chord, held through the
    # final bars.
    pad_note(pad, 80, 8, 'C3', 40)
    pad_note(pad, 80, 8, 'G3', 38)
    cello_note(cello, 80, 8, 'C2', 40)
    piano_note(piano, 80, 8, 'E4', 40)
    pad_note(pad, 88, 8, 'C3', 40)
    pad_note(pad, 88, 8, 'G3', 38)
    cello_note(cello, 88, 8, 'C2', 40)
    piano_note(piano, 88, 8, 'C5', 38)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = be_still_and_know()
    mc.compose('be-still-and-know.mid', tracks, tempo=54)

    mid = mido.MidiFile('be-still-and-know.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
