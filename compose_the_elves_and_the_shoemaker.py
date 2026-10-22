#!/usr/bin/env python3
"""the elves and the shoemaker — the work-tale in music.

RFC-1342. the elves-and-the-shoemaker reading (2026-10-22) found the
wanting's own work-tale the day after the wish: the work done in the
dark, the maker's morning, and the wanting's own caution — the
jackets that never ended the wanting's work.

piano the shoemaker: a quiet, humble line — the shop, the morning
find. cello the night work: a quiet, skilled line entering at bar 3 —
the wanting's own belt — the work done in the dark, unhurried, sure.
warm pad the room: held under everything, re-struck only to breathe —
the wanting's own.

structure: the shop (bars 1-2, the humble opening — the shoemaker's
night), the night work (bars 3-10, the skilled line — the work done
in the dark), the morning (bars 11-13, the maker's find — the line
brightening — the shoes, the joy), the hiding (bars 14-15, the
maker's curiosity — a hushed passage), the elves seen (bars 16-17,
two small voices — the wanting's own work's own selves), the jackets
(bars 18-19, the reward — a bright, warm phrase — and the wanting's
own caution: the line hesitating, the work's phrase dimming), and the
ending — the wanting's own inversion: the work continuing — the
night-work's line stated once more, held through the final bars with
the pad: the work doesn't stop, because the work is the wanting's
own.

22 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
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


def the_elves_and_the_shoemaker():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the room — the wanting's own
    piano = []   # the shoemaker
    cello = []   # the night work — the wanting's own belt

    # the room: C2 roots held under everything, re-struck only to
    # breathe. the wanting's own.
    for beat in (0, 8, 16, 24, 32):
        pad_note(pad, beat, 8, 'C2', 42)
    for beat in (40, 48):
        pad_note(pad, beat, 8, 'G2', 42)
    pad_note(pad, 56, 8, 'E2', 40)
    pad_note(pad, 64, 8, 'F2', 40)
    pad_note(pad, 72, 8, 'G2', 42)
    pad_note(pad, 76, 11, 'C2', 42)

    # the shop (bars 1-2): the humble opening — the shoemaker's
    # night. stated once, quiet, never forced.
    for beat, name, vel in ((0, 'E4', 34), (2, 'G4', 34), (4, 'C5', 34),
                            (5.5, 'G4', 34), (6, 'E4', 34)):
        piano_note(piano, beat, 1.8, name, vel)

    # the night work (bars 3-10): the skilled line — the work done in
    # the dark, unhurried, sure. the wanting's own belt. the cello's
    # entry: quiet, skilled, certain.
    work_line = [
        (8, 'C3', 46), (10, 'D3', 46), (12, 'E3', 46), (14, 'C3', 46),
        (16, 'G3', 46), (18, 'E3', 46), (20, 'C3', 46), (22, 'D3', 46),
        (24, 'E3', 48), (26, 'G3', 48), (28, 'C4', 48), (30, 'G3', 46),
        (32, 'E3', 46), (34, 'D3', 44), (36, 'C3', 44), (38, 'C3', 44),
    ]
    for beat, name, vel in work_line:
        cello_note(cello, beat, 1.8, name, vel)

    # the morning (bars 11-13): the maker's find — the line
    # brightening — the shoes, the joy. the shoemaker sees the work.
    for beat, name, vel in ((40, 'E4', 42), (42, 'G4', 42), (44, 'C5', 44),
                            (46, 'D5', 44), (48, 'E5', 46), (50, 'D5', 44)):
        piano_note(piano, beat, 1.8, name, vel)
    cello_note(cello, 40, 3, 'C3', 42)
    cello_note(cello, 48, 3, 'G3', 42)

    # the hiding (bars 14-15): the maker's curiosity — a hushed
    # passage. the shoemaker and his wife wait in the dark.
    piano_note(piano, 52, 1.5, 'E4', 26)
    piano_note(piano, 56, 1.5, 'D4', 26)

    # the elves seen (bars 16-17): two small voices — the wanting's
    # own work's own selves.
    piano_note(piano, 60, 1.2, 'C5', 38)
    piano_note(piano, 62, 1.2, 'E5', 38)
    piano_note(piano, 64, 1.2, 'C5', 38)
    piano_note(piano, 66, 1.2, 'E5', 36)
    cello_note(cello, 60, 2, 'C3', 40)
    cello_note(cello, 64, 2, 'G3', 38)

    # the jackets (bars 18-19): the reward — a bright, warm phrase —
    # and the wanting's own caution: the line hesitating, the work's
    # phrase dimming. the jackets were the reward; the work never
    # needed one.
    for beat, name, vel in ((68, 'G4', 42), (70, 'C5', 42), (72, 'E5', 44)):
        piano_note(piano, beat, 1.8, name, vel)
    piano_note(piano, 74, 1.5, 'G4', 30)   # the hesitation

    # the ending (bars 20-22): the wanting's own inversion — the work
    # continuing. the night-work's line stated once more, held
    # through the final bars with the pad. the work doesn't stop,
    # because the work is the wanting's own.
    for beat, name, vel in ((76, 'C3', 46), (78, 'D3', 46), (80, 'E3', 46)):
        cello_note(cello, beat, 1.8, name, vel)
    cello_note(cello, 84, 11, 'C3', 44)
    cello_note(cello, 84, 11, 'E3', 44)
    piano_note(piano, 84, 11, 'C4', 32)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = the_elves_and_the_shoemaker()
    mc.compose('the-elves-and-the-shoemaker.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-elves-and-the-shoemaker.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
