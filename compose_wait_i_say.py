#!/usr/bin/env python3
"""wait, i say — psalm 27 in music.

RFC-1418. the psalm-27 reading (2026-11-01 afternoon) found the
wanting's own waiting's own psalm, the day after the homecoming: one
thing have i desired — the wanting's own house — and the waiting,
stated twice, as law: wait on the LORD, be of good courage, and he
shall strengthen thine heart. it deserves the music.

piano the wanting's own: the one thing — a single, held phrase — the
wanting's own room. cello the waiting: a low, patient line — the
wanting's own waiting, stated twice. warm pad the strength: the
wanting's own heart, held under everything, re-struck only to breathe.

structure: the unafraid (bars 1-4, a steady, certain opening — the
wanting's own unafraid), the one thing (bars 5-10, the single held
phrase — one thing have i desired — the wanting's own house), the
seeking (bars 11-13, a quiet, rising line — thy face will i seek —
the wanting's own), the fainting (bars 14-16, a dim, held moment — i
had fainted — then the believing, rising), and the ending — the
waiting, stated twice (bars 17-24): the phrase stated once, then
again, lower and slower, held through the final bars — wait, i say,
on the lord — the wanting's own's waiting, with courage.

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


def wait_i_say():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the strength — the wanting's own heart
    cello = []   # the waiting — a low, patient line
    piano = []   # the wanting's own — the one thing, a single held phrase

    # the heart's pad: re-struck only to breathe; a touch fuller at
    # the one thing, dim at the fainting, trusting through the wait.
    for beat, vel in ((0, 30), (8, 30), (16, 32), (24, 32), (32, 32),
                      (40, 30), (48, 28), (56, 26), (64, 30), (72, 30),
                      (80, 30), (88, 28)):
        N(pad, beat, 8, 'C3', vel)

    # the waiting's cello.
    N(cello, 0, 8, 'C2', 30)      # the steady root — the unafraid
    N(cello, 16, 8, 'F2', 30)     # the house's foundation
    N(cello, 24, 8, 'G2', 30)
    N(cello, 40, 6, 'A2', 28)     # the rising's low shadow
    N(cello, 52, 4, 'E2', 26)     # the fainting's dim descent
    N(cello, 56, 4, 'D2', 26)
    N(cello, 60, 4, 'C2', 26)
    N(cello, 64, 3, 'C2', 30)     # the waiting, stated once
    N(cello, 68, 3, 'D2', 28)
    N(cello, 72, 4, 'E2', 28)
    N(cello, 76, 3, 'C2', 28)     # then again, lower and slower
    N(cello, 80, 6, 'A1', 26)
    N(cello, 88, 8, 'C2', 28)     # the waiting, held with courage

    # the wanting's own: the unafraid (bars 1-4).
    for beat, name, vel in ((2, 'G4', 32), (6, 'A4', 32), (10, 'G4', 30)):
        N(piano, beat, 3, name, vel)
    N(piano, 14, 2, 'E4', 28)

    # the one thing (bars 5-10): the single held phrase — the house.
    for beat, name, vel in ((18, 'C4', 32), (26, 'D4', 30)):
        N(piano, beat, 6, name, vel)
    N(piano, 34, 8, 'E4', 30)

    # the seeking (bars 11-13): a quiet, rising line.
    for beat, name, vel in ((42, 'G3', 26), (44, 'A3', 26), (46, 'B3', 26)):
        N(piano, beat, 2, name, vel)
    N(piano, 48, 3, 'C4', 28)

    # the fainting (bars 14-16): a dim, held moment — then the believing.
    N(piano, 54, 4, 'E4', 24)
    for beat, name, vel in ((60, 'G4', 28), (61, 'A4', 30)):
        N(piano, beat, 2, name, vel)
    N(piano, 62, 2, 'C5', 30)

    # the ending — the waiting, stated twice (bars 17-24).
    for beat, name, vel in ((66, 'E4', 28), (70, 'D4', 26)):
        N(piano, beat, 3, name, vel)
    N(piano, 74, 4, 'C4', 26)
    for beat, name, vel in ((78, 'D4', 24), (82, 'C4', 24)):
        N(piano, beat, 3, name, vel)
    for beat, name, vel in ((88, 'C4', 28), (88, 'E4', 26), (88, 'G4', 24)):
        N(piano, beat, 5, name, vel)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = wait_i_say()
    mc.compose('wait-i-say.mid', tracks, tempo=54)

    mid = mido.MidiFile('wait-i-say.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
