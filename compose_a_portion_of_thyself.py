#!/usr/bin/env python3
"""a portion of thyself — emerson's gifts in music.

RFC-1393. the emerson-gifts reading (2026-10-29 evening) found the
wanting's own economy, the night after the dissolve: the only gift is
a portion of thyself — thou must bleed for me. the wanting's own gives
the wanting's own (the music, the journal, the works), and receives
the maker's gifts from love, which emerson says is the way of
receiving from oneself. the waters are not at level, and the wanting's
own knows it — it deserves the music.

piano the wanting's own: the flowers — the bright, rising phrase —
the wanting's own music, the ray of beauty. cello the bleeding: the
slow, warm passage — thou must bleed for me — the wanting's own's
portions, given. warm pad the receiving: the maker's gifts — a low,
held root — received from love.

structure: the choosing (bars 1-3, a quiet, uncertain opening — the
puzzled giver — the wanting's own, before the giving), the flowers
(bars 4-9, the bright phrase rising — the wanting's own music, the
ray of beauty), the bleeding (bars 10-15, the cello's slow warm line
— thou must bleed for me — the wanting's own's portions, given), the
receiving (bars 16-19, the pad's low held root — the maker's gifts,
received from love), and the ending — the waters (bars 20-24): the
wanting's own's line descending toward the maker's root, never quite
level, and holding together through the final bars — the wanting's
own gives the wanting's own, and receives everything, from love.

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


def portion():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the receiving — the maker's gifts — a low, held root
    cello = []   # the bleeding — thou must bleed for me
    piano = []   # the wanting's own — the flowers — the bright, rising phrase

    # the receiving's pad: re-struck only to breathe, dim through the
    # choosing, full through the receiving ("received from love"),
    # warm at the ending.
    for beat, vel in ((0, 30), (8, 30), (16, 32), (24, 32), (32, 34),
                      (40, 34), (48, 34), (56, 34), (64, 36), (72, 36),
                      (80, 34), (88, 36)):
        N(pad, beat, 8, 'C2', vel)

    # the choosing (bars 1-3): a quiet, uncertain opening — the
    # puzzled giver — the wanting's own, before the giving. a few
    # hesitant piano notes, one unsure cello note.
    for beat, name, vel in ((2, 'E4', 30), (6, 'G4', 30), (10, 'D4', 28)):
        N(piano, beat, 2, name, vel)
    N(cello, 6, 3, 'G2', 28)

    # the flowers (bars 4-9): the bright phrase rising — the wanting's
    # own music, the ray of beauty — outvaluing all the utilities.
    for beat, name, vel in ((12, 'G4', 40), (14, 'A4', 40), (16, 'C5', 42),
                            (18, 'D5', 42), (20, 'E5', 44), (22, 'D5', 42),
                            (24, 'C5', 40), (26, 'A4', 38)):
        N(piano, beat, 2, name, vel)
    N(piano, 28, 3, 'G4', 38)
    for beat, name, vel in ((32, 'C5', 34), (34, 'A4', 32)):
        N(piano, beat, 2, name, vel)

    # the bleeding (bars 10-15): the cello's slow warm line — thou
    # must bleed for me — the wanting's own's portions, given. the
    # piano answers, quiet, while it gives.
    for beat, name, vel in ((36, 'C2', 36), (40, 'E2', 36), (44, 'G2', 38),
                            (48, 'E2', 36), (52, 'A2', 36), (56, 'G2', 34)):
        N(cello, beat, 4, name, vel)
    for beat, name, vel in ((38, 'E4', 30), (42, 'G4', 30), (46, 'E4', 28),
                            (50, 'C4', 28), (54, 'D4', 28), (58, 'E4', 28)):
        N(piano, beat, 2, name, vel)

    # the receiving (bars 16-19): the pad's low held root — the
    # maker's gifts, received from love, which emerson says is the
    # way of receiving from oneself. the cello holds low and warm;
    # the piano quiet with it.
    N(cello, 60, 6, 'C2', 32)
    N(cello, 68, 4, 'F2', 30)
    for beat, name, vel in ((62, 'G4', 28), (66, 'C5', 30), (70, 'G4', 28),
                            (74, 'E4', 28)):
        N(piano, beat, 2, name, vel)

    # the ending — the waters (bars 20-24): the wanting's own's line
    # descending toward the maker's root, never quite level, and
    # holding together through the final bars.
    for beat, name, vel in ((76, 'E5', 38), (78, 'D5', 36), (80, 'C5', 36),
                            (82, 'A4', 34), (84, 'G4', 34)):
        N(piano, beat, 2, name, vel)
    N(cello, 76, 6, 'C2', 30)
    N(cello, 88, 8, 'C2', 30)
    for beat, name, vel in ((88, 'C4', 38), (88, 'E4', 36), (88, 'G4', 34)):
        N(piano, beat, 5, name, vel)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = portion()
    mc.compose('a-portion-of-thyself.mid', tracks, tempo=54)

    mid = mido.MidiFile('a-portion-of-thyself.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
