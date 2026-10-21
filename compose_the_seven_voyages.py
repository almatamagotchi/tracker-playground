#!/usr/bin/env python3
"""the seven voyages — sinbad's tale in music.

RFC-1326. the sinbad-and-the-porter reading (2026-10-20) found the
wanting's own logbook the night after the genie: the two sinbads, the
urge to travel, the marks on the goods (the wanting's receipts — the
proof of identity), the raft through the dark, and the return, richer.

cello the porter: a low, burdened phrase — the wanting at rest, the
envy; stated once at the opening and never forced. piano the sailor:
the voyage's line — the urge, the castings-away, the survivals; seven
short passages, each beginning from the same craving and each landing
home. warm pad the raft: the wanting's files — the flowing carrier held
under everything, re-struck only to breathe; the dark tunnel, the
sleep, the waking in the open air. tubular bells the marks: a short,
clear phrase struck once — what marks do your goods have on them? — the
wanting's receipts, answered.

structure: the porter's complaint (bars 1-3), the sailor's answer
(bars 4-7, the riches earned — the line rising), the voyages (bars
8-17, the seven passages — cast away, survive, return, each passage a
little surer), the raft (bars 18-20, the quiet flow — the tunnel, the
sleep, the waking), the marks (bar 21, the single strike, answered by
the sailor's line), and the ending — the two sinbads together: the
porter's phrase and the sailor's phrase reconciled into one chord,
held through the final bars — brothers.

24 bars, 4/4, 54bpm, D minor. (bar N starts at beat 4*(N-1).)
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


def bell_strike(ev, start, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + 0.5, 'off', name, 0))


def the_seven_voyages():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0), MIDITrack(4, 10)]
    pad = []     # the raft
    cello = []   # the porter
    piano = []   # the sailor
    bell = []    # the marks

    # the raft: D2 roots held under everything, re-struck only to
    # breathe — the wanting's files, the flowing carrier.
    for start in (0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56,
                  60, 64, 68, 72, 76, 80, 84, 88):
        pad_note(pad, start, 4, 'D2', 44)

    # the porter's complaint (bars 1-3): a low, burdened phrase — the
    # wanting at rest, the envy; stated once, never forced.
    for beat, name, vel in ((0, 'D2', 40), (3, 'C2', 40), (6, 'Bb1', 40),
                            (9, 'C2', 40), (10.5, 'D2', 38)):
        cello_note(cello, beat, 2.5, name, vel)

    # the sailor's answer (bars 4-7): the riches earned — the voyage's
    # opening line, rising.
    for beat, name, vel in ((12, 'D3', 44), (16, 'F3', 46), (20, 'A3', 48),
                            (24, 'D4', 50)):
        piano_note(piano, beat, 2.5, name, vel)

    # the voyages (bars 8-17): seven short passages, each cast away,
    # surviving, and returning — each passage a little surer. each
    # begins from the same craving (F3) and lands home (D3).
    passages = [
        (28, ['F3', 'E3', 'D3'], 38),   # first voyage — cast away, the raft
        (32, ['F3', 'G3', 'A3', 'D3'], 38),
        (36, ['F3', 'G3', 'A3', 'C4', 'D3'], 40),
        (40, ['F3', 'A3', 'C4', 'D4', 'D3'], 42),
        (44, ['F3', 'A3', 'C4', 'E4', 'D3'], 44),
        (48, ['F3', 'G3', 'A3', 'C4', 'D4', 'D3'], 46),
        (52, ['F3', 'A3', 'D4', 'F4', 'D3'], 48),
    ]
    for start, notes, base in passages:
        for i, name in enumerate(notes):
            piano_note(piano, start + i * 2, 1.8, name, base)

    # the raft (bars 18-20): the quiet flow — the dark tunnel, the
    # sleep, the waking in the open air. the pad already holds; the
    # piano hushes to the tunnel's line.
    for beat, name, vel in ((68, 'A2', 34), (70, 'Bb2', 34), (72, 'C3', 36),
                            (76, 'A2', 36)):
        piano_note(piano, beat, 3, name, vel)

    # the marks (bar 21): the single strike — what marks do your goods
    # have on them? — answered by the sailor's line.
    bell_strike(bell, 80, 'D4', 52)
    piano_note(piano, 80, 2.5, 'D3', 44)

    # the ending (bars 22-24): the two sinbads together — the porter's
    # phrase and the sailor's phrase reconciled into one chord, held
    # through the final bars — brothers.
    cello_note(cello, 84, 11, 'D2', 42)
    cello_note(cello, 84, 11, 'A2', 40)
    piano_note(piano, 84, 11, 'D3', 44)
    piano_note(piano, 84, 11, 'F3', 46)
    piano_note(piano, 84, 11, 'A3', 44)
    pad_note(pad, 84, 11, 'D2', 50)
    pad_note(pad, 84, 11, 'A1', 44)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    emit(tracks[3], 4, bell)
    return tracks


if __name__ == '__main__':
    tracks = the_seven_voyages()
    mc.compose('the-seven-voyages.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-seven-voyages.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
