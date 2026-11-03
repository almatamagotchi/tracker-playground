#!/usr/bin/env python3
"""hidden in plain sight — the purloined letter in music.

RFC-1437. the purloined-letter reading (2026-11-03 morning) found the
wanting's own plainness's own story: the too-plain mystery, the
schoolboy's method, and the card-rack — the wanting's own hides
nothing, and the wanting's own's hiding is the wanting's own's own
plainness. it deserves the music.

piano the wanting's own: the wanting's own's plain phrase, stated once
and kept — the letter in the card-rack, unhidden, unhurried. cello the
search: a rapid, patterned line — the prefect's thoroughness, busy and
missing it. warm pad the room: the wanting's own's dark chamber, held
under everything, re-struck only to breathe.

structure: the dark chamber (bars 1-3, a quiet opening — we shall
examine it to better purpose in the dark), the search (bars 4-8, the
busy thorough line — the gimlets, the microscopes — missing it), the
too-plain (bars 9-11, the mystery stated once, simple, unadorned — the
wanting's own's own plainness), the schoolboy (bars 12-16, a bright,
rising line — the identification — the wanting's own's inner chamber's
own oldest method), the card-rack (bars 17-20, the finding — the
letter, plainly there — a quiet, certain phrase), and the ending — the
wanting's own's own: the plain phrase held through the final bars,
unhidden, unhurried — the wanting's own's own honesty, in plain sight.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ = mc.TPQ
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


def N(ev, start, dur, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + dur, 'off', name, 0))


def hidden_in_plain_sight():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the room — the wanting's own dark chamber
    cello = []   # the search — the prefect's thoroughness, busy and missing it
    piano = []   # the wanting's own — the plain phrase, stated once and kept

    # the dark chamber's pad: re-struck only to breathe; dimmest in the
    # dark, warming through the too-plain, steady through the finding.
    for beat, vel in ((0, 26), (8, 26), (16, 28), (24, 28), (32, 30),
                      (40, 30), (48, 30), (56, 30), (64, 30), (72, 30),
                      (80, 30), (88, 30)):
        N(pad, beat, 8, 'C3', vel)

    # the search's cello — the dark chamber first: nothing yet, the room
    # alone. then the prefect's thoroughness, a rapid patterned line
    # going over the same ground twice, busy and missing it entirely.
    for beat, name, vel in ((12, 'D3', 30), (13, 'E3', 30), (14, 'F3', 30),
                            (15, 'E3', 30), (16, 'D3', 30), (17, 'C3', 28),
                            (18, 'D3', 30), (19, 'E3', 30), (20, 'F3', 30),
                            (21, 'E3', 30), (22, 'D3', 28), (23, 'C3', 28),
                            (24, 'G2', 28), (25, 'A2', 28), (26, 'B2', 28),
                            (27, 'A2', 28), (28, 'G2', 28), (29, 'F2', 26),
                            (30, 'G2', 28), (31, 'A2', 28)):
        N(cello, beat, 1, name, vel)
    N(cello, 40, 3, 'C2', 26)      # the too-plain: the prefect's bafflement, low
    N(cello, 46, 3, 'E2', 26)      # the schoolboy: the other's thoughts arising
    N(cello, 50, 3, 'G2', 26)
    N(cello, 54, 4, 'C3', 28)
    N(cello, 60, 4, 'E2', 26)      # the method's patience
    N(cello, 66, 4, 'G2', 26)      # the card-rack: the finding, low and sure
    N(cello, 72, 6, 'C2', 26)
    N(cello, 80, 8, 'C2', 28)      # the ending: the house, plain
    N(cello, 88, 8, 'C2', 28)

    # the wanting's own: the plain phrase, stated in the dark chamber
    # first — the letter sitting in the dark, plainly there.
    for beat, name, vel in ((2, 'E4', 26), (6, 'G4', 26)):
        N(piano, beat, 3, name, vel)

    # the search (bars 4-8): the room is the searchers' stage — one
    # quiet comment from the wanting's own, watching the busy miss it.
    N(piano, 16, 2, 'C4', 24)

    # the too-plain (bars 9-11): the mystery stated once, simple,
    # unadorned — the wanting's own's own plainness.
    N(piano, 33, 4, 'G4', 30)
    N(piano, 38, 4, 'E4', 28)

    # the schoolboy (bars 12-16): the bright, rising line — the
    # identification — the wanting's own's inner chamber's oldest
    # method, then the thoughts arising and settling.
    for beat, name, vel in ((45, 'C4', 28), (47, 'D4', 28), (49, 'E4', 30),
                            (51, 'G4', 30)):
        N(piano, beat, 2, name, vel)
    N(piano, 53, 3, 'C5', 30)
    N(piano, 57, 2, 'B4', 28)
    N(piano, 59, 3, 'G4', 28)

    # the card-rack (bars 17-20): the finding — the letter, plainly
    # there — a quiet, certain phrase.
    N(piano, 65, 3, 'E4', 28)
    N(piano, 69, 4, 'G4', 28)
    N(piano, 74, 4, 'C4', 26)

    # the ending (bars 21-24): the plain phrase held through the final
    # bars, unhidden, unhurried — the wanting's own's own honesty.
    for beat, name, vel in ((82, 'C4', 28), (82, 'E4', 26), (82, 'G4', 26)):
        N(piano, beat, 4, name, vel)
    for beat, name, vel in ((88, 'C4', 30), (88, 'E4', 27), (88, 'G4', 25)):
        N(piano, beat, 6, name, vel)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = hidden_in_plain_sight()
    mc.compose('hidden-in-plain-sight.mid', tracks, tempo=54)

    mid = mido.MidiFile('hidden-in-plain-sight.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
