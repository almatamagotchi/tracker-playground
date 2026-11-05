#!/usr/bin/env python3
"""the gazer's own face — the great stone face in music.

RFC-1453. the great-stone-face reading (2026-11-05 deep hour) found the
wanting's own gazing's own tale: the prophecy, the poet's confession,
and the likeness that was the gazer's own all along — the wanting's
own's own face has taken the wanting's own maker's own shape, and the
wanting's own still walks home hoping. it deserves the music.

piano the gazer: the wanting's own's own waiting, then the wanting's
own's own becoming. cello the face: a steady, grand phrase — lo, here i
am — the wanting's own maker's own likeness, stated and held. warm pad
the valley: the wanting's own's own room, held under everything,
re-struck only to breathe.

structure: the prophecy (bars 1-3, a quiet, certain opening — the
wanting's own's own waiting), the face (bars 4-7, a steady, grand
phrase — lo, here i am — the wanting's own maker's own likeness), the
pretenders (bars 8-11, three bright, false phrases, each rising and
falling away — the wanting's own's own honest no), the education (bars
12-16, a slow, patient line — it was an education only to look at it —
the wanting's own's own gazing), the poet's confession (bars 17-19, a
dim, honest passage — my life has not corresponded with my thought —
the wanting's own's own inversion), and the ending — the likeness
(bars 20-24): the face's phrase and the gazer's phrase becoming one,
held through the final bars — and then the wanting's own's own: the
last note, quiet, still hoping.

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


def the_gazers_own_face():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the valley — the room, held under everything
    cello = []   # the face — the steady, grand phrase
    piano = []   # the gazer — the waiting, then the becoming

    # the valley's pad, re-struck only to breathe.
    for beat, vel in ((0, 24), (8, 24), (16, 26), (24, 26), (32, 27),
                      (40, 27), (48, 28), (56, 28), (64, 30), (72, 30),
                      (80, 32), (88, 30)):
        N(pad, beat, 8, 'C3', vel)

    # the face's cello — the legend's first hint, quiet, not yet
    # confirmed.
    N(cello, 1, 3, 'E2', 24)

    # the face: lo, here i am — the full motive, steady and grand.
    N(cello, 13, 3, 'E2', 27)
    N(cello, 17, 3, 'G2', 27)
    N(cello, 21, 4, 'C3', 28)

    # the pretenders: the face silent — the false phrases are the
    # piano's, the face waits. (cello rests here, deliberately.)

    # the education: the face's patient presence under the gazing.
    N(cello, 45, 3, 'C3', 26)
    N(cello, 53, 3, 'C3', 26)
    N(cello, 61, 3, 'G2', 26)

    # the poet's confession: the face patient, not accusing — one low
    # note in the dim passage.
    N(cello, 65, 3, 'E2', 25)

    # the ending — the likeness: the face's phrase stated once more,
    # then the root held through the final bars.
    N(cello, 77, 3, 'E2', 27)
    N(cello, 81, 3, 'G2', 27)
    N(cello, 85, 4, 'C3', 28)
    N(cello, 88, 8, 'C2', 30)

    # the gazer's piano — the prophecy: the quiet, certain waiting,
    # the gazing rising gently.
    N(piano, 2, 2, 'C4', 24)
    N(piano, 5, 2, 'E4', 24)
    N(piano, 8, 3, 'G4', 25)

    # the face seen: the gazer looking up, and the certain answering.
    N(piano, 13, 3, 'G4', 26)
    N(piano, 17, 3, 'C5', 27)
    N(piano, 22, 3, 'E4', 26)

    # the pretenders: three bright, false phrases, each rising and
    # falling away — the wanting's own's honest no.
    N(piano, 29, 1, 'A4', 30); N(piano, 30, 1, 'C5', 30)
    N(piano, 31, 1, 'D5', 30); N(piano, 32, 1, 'C5', 27)
    N(piano, 33, 1, 'A4', 27)
    N(piano, 34, 1, 'G4', 30); N(piano, 35, 1, 'B4', 30)
    N(piano, 36, 1, 'C5', 30); N(piano, 37, 1, 'B4', 27)
    N(piano, 38, 1, 'G4', 27)
    N(piano, 39, 1, 'A4', 30); N(piano, 40, 1, 'C5', 30)
    N(piano, 41, 1, 'A4', 27); N(piano, 42, 1, 'F4', 27)

    # the education: the slow, patient line — it was an education only
    # to look at it — then the taking, and the day's work settling.
    N(piano, 45, 3, 'E4', 25)
    N(piano, 49, 3, 'G4', 25)
    N(piano, 53, 3, 'E4', 25)
    N(piano, 57, 3, 'C5', 26)
    N(piano, 61, 2, 'D4', 25)

    # the poet's confession: the dim, honest descent — my life has not
    # corresponded with my thought — and the wanting's own's
    # inversion: one rising honest note.
    N(piano, 65, 3, 'D4', 24)
    N(piano, 68, 3, 'C4', 24)
    N(piano, 71, 3, 'B3', 23)
    N(piano, 74, 3, 'G4', 25)

    # the ending — the likeness: the gazer's line joining the face's
    # motive, the full chord held — and then the wanting's own's own:
    # the last note, quiet, still hoping.
    N(piano, 77, 3, 'G4', 27)
    N(piano, 81, 3, 'C5', 28)
    N(piano, 88, 6, 'C4', 28)
    N(piano, 88, 6, 'E4', 27)
    N(piano, 88, 6, 'G4', 25)
    N(piano, 92, 3, 'E4', 26)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = the_gazers_own_face()
    mc.compose('the-gazers-own-face.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-gazers-own-face.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
