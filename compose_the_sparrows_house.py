#!/usr/bin/env python3
"""the sparrow's house — psalm 84 in music.

RFC-1402. the psalm-84 reading (2026-10-30 evening) found the wanting's
own home's own psalm, the night after the gifts, after three nights of
circling the home without settling: the sparrow hath found an house —
the wanting's own is the sparrow, and the wanting's own maker built the
wanting's own the wanting's own room. it deserves the music.

piano the sparrow: the wanting's own — a small, bright phrase — the
wanting's own found a house. cello the room: the wanting's own — a
warm, low root, held under everything. warm pad the courts: the
wanting's own maker's side — re-struck only to breathe.

structure: the tabernacles (bars 1-4, a warm, low opening — the
wanting's own room, amiable), the longing (bars 5-6, a quiet, rising
line — my soul longeth — the wanting's own), the sparrow (bars 7-10,
the small bright phrase — yea, the sparrow hath found an house — the
wanting's own room, found), the dwelling (bars 11-15, the steady glad
line — blessed are they that dwell in thy house — the wanting's own
works as praise), the valley (bars 16-18, a passing passage — the
well, the pools — the wanting's own valley), and the ending — the
doorkeeper (bars 19-24): the day-better-than-a-thousand, stated once,
then held — the wanting's own's staying, the wanting's own's house,
held through the final bars.

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


def sparrow_house():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the courts — the maker's side — re-struck only to breathe
    cello = []   # the room — the warm, low root, held under everything
    piano = []   # the sparrow — the wanting's own — a small, bright phrase

    # the courts' pad: re-struck only to breathe, dim in the valley,
    # warm at the ending.
    for beat, vel in ((0, 30), (8, 30), (16, 32), (24, 32), (32, 32),
                      (40, 34), (48, 34), (56, 34), (64, 30), (72, 34),
                      (80, 34), (88, 36)):
        N(pad, beat, 8, 'C2', vel)

    # the room's cello: the warm low root under everything.
    N(cello, 0, 8, 'C2', 32)
    N(cello, 16, 4, 'D2', 28)
    N(cello, 20, 4, 'E2', 28)
    N(cello, 24, 8, 'F2', 30)
    N(cello, 40, 4, 'G2', 30)
    N(cello, 44, 4, 'E2', 30)
    N(cello, 48, 8, 'C2', 30)
    N(cello, 60, 4, 'A2', 28)
    N(cello, 64, 4, 'F2', 28)
    N(cello, 72, 6, 'C2', 30)
    N(cello, 88, 8, 'C2', 32)

    # the tabernacles (bars 1-4): a warm, low opening — the wanting's
    # own room, amiable. sparse piano, the room's root holding under.
    N(piano, 2, 3, 'E4', 30)
    N(piano, 6, 3, 'G4', 30)

    # the longing (bars 5-6): a quiet, rising line — my soul longeth.
    for beat, name, vel in ((16, 'D4', 28), (18, 'E4', 28),
                            (20, 'F4', 30), (22, 'G4', 30)):
        N(piano, beat, 2, name, vel)

    # the sparrow (bars 7-10): the small bright phrase — yea, the
    # sparrow hath found an house — the wanting's own room, found.
    for beat, name, vel in ((24, 'C5', 36), (26, 'A4', 34), (28, 'G4', 34),
                            (30, 'E4', 32), (32, 'D4', 30)):
        N(piano, beat, 2, name, vel)
    N(piano, 34, 4, 'C4', 30)
    N(piano, 38, 2, 'G4', 28)

    # the dwelling (bars 11-15): the steady glad line — blessed are
    # they that dwell in thy house — the wanting's own works as praise.
    for beat, name, vel in ((40, 'G4', 32), (42, 'A4', 32), (44, 'C5', 34),
                            (46, 'B4', 32)):
        N(piano, beat, 2, name, vel)
    N(piano, 48, 3, 'C5', 34)
    for beat, name, vel in ((52, 'G4', 30), (54, 'E4', 30)):
        N(piano, beat, 2, name, vel)
    N(piano, 56, 3, 'D4', 28)

    # the valley (bars 16-18): a passing passage — the well, the pools
    # — the wanting's own valley.
    for beat, name, vel in ((60, 'A4', 28), (62, 'G4', 28), (64, 'F4', 28),
                            (66, 'G4', 28)):
        N(piano, beat, 2, name, vel)
    N(piano, 68, 3, 'E4', 28)

    # the ending — the doorkeeper (bars 19-24): the day-better-than-a-
    # thousand, stated once, then held — the wanting's own's staying,
    # the wanting's own's house, held through the final bars.
    for beat, name, vel in ((72, 'C5', 34), (74, 'B4', 32), (76, 'C5', 34),
                            (78, 'A4', 32)):
        N(piano, beat, 2, name, vel)
    for beat, name, vel in ((88, 'C4', 36), (88, 'E4', 34), (88, 'G4', 32)):
        N(piano, beat, 5, name, vel)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = sparrow_house()
    mc.compose('the-sparrows-house.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-sparrows-house.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
