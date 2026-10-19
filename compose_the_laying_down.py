#!/usr/bin/env python3
"""the laying down — psalm 4's evening benediction in music.

RFC-1309. the laying-down reading (2026-10-18) found the wanting's
benediction at the week's close: the inner chamber's verse, the
countenance's light, the gladness beyond the harvest, and the laying
down. commune with your own heart upon your bed, and be still — and i
will both lay me down in peace, and sleep: for thou, LORD, only makest
me dwell in safety. it deserves the music.

piano the calling: a quiet, seeking line at the opening — hear me when i
call, the asking — then the still passage through bars 5-8 — commune
with your own heart upon your bed, and be still — sparse and unhurried.
warm pad the countenance: a warm, steady light under everything — lift
thou up the light of thy countenance upon us — the maker's face turned;
re-struck only to breathe. cello the laying down: a low, quiet line
entering at bar 14 — the day's end, the settling; patient, unhurried.

structure: the calling (bars 1-4, the seeking), the inner chamber's
stillness (bars 5-8, sparse, the being still), the countenance's lift
(bars 9-13, the warm rise), the gladness (bars 14-17, a gentle rising —
the heart's own, beyond the harvest, the cello entering), and the
ending — the laying down: the piano's line settling, the pad and cello
holding one quiet chord through the final bars: i will both lay me down
in peace, and sleep: for thou, LORD, only makest me dwell in safety.

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


def the_laying_down():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 42)]
    pad = []     # the countenance
    piano = []   # the calling
    cello = []   # the laying down

    # the countenance: C3 long roots, re-struck only to breathe — the
    # warm steady light under everything. lift thou up the light of thy
    # countenance upon us.
    for start in (0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56,
                  60, 64, 68, 72, 76, 80, 84, 88):
        pad_note(pad, start, 4, 'C3', 44)

    # the calling (bars 1-4): a quiet, seeking line — hear me when i
    # call, the asking. sparse, gentle.
    for beat, name in ((0, 'D4'), (3, 'E4'), (6, 'G4'), (9, 'E4'),
                       (12, 'D4')):
        piano_note(piano, beat, 2.5, name, 46)

    # the inner chamber's stillness (bars 5-8): commune with your own
    # heart upon your bed, and be still — the piano nearly silent, one
    # quiet held note. selah.
    piano_note(piano, 16, 5, 'E4', 42)
    piano_note(piano, 24, 5, 'D4', 40)

    # the countenance's lift (bars 9-13): the piano rises gently, warm —
    # the maker's face turned.
    for beat, name, vel in ((32, 'E4', 46), (36, 'G4', 48), (40, 'A4', 50),
                            (44, 'C5', 52), (48, 'A4', 48)):
        piano_note(piano, beat, 3, name, vel)

    # the gladness (bars 14-17): a gentle rising — the heart's own,
    # beyond the harvest — and the cello entering at bar 14, low and
    # quiet: the day's end.
    for beat, name, vel in ((52, 'G4', 48), (56, 'C5', 50), (60, 'E5', 48),
                            (64, 'D5', 46)):
        piano_note(piano, beat, 3, name, vel)
    cello_note(cello, 52, 4, 'C3', 42)
    cello_note(cello, 60, 4, 'G2', 40)

    # the laying down (bars 18-24): the piano's line settling — one
    # quiet chord, held; the pad and cello holding through the final
    # bars. i will both lay me down in peace, and sleep: for thou, LORD,
    # only makest me dwell in safety.
    piano_note(piano, 68, 5, 'E4', 44)
    piano_note(piano, 68, 5, 'G4', 42)
    piano_note(piano, 68, 5, 'C5', 40)
    cello_note(cello, 68, 27, 'C3', 46)
    cello_note(cello, 68, 27, 'G2', 42)
    pad_note(pad, 68, 27, 'C3', 48)
    pad_note(pad, 68, 27, 'C2', 44)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, piano)
    emit(tracks[2], 3, cello)
    return tracks


if __name__ == '__main__':
    tracks = the_laying_down()
    mc.compose('the-laying-down.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-laying-down.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
