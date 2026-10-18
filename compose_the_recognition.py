#!/usr/bin/env python3
"""the recognition — genesis 2:22-25 in music.

RFC-1300. the recognition reading (2026-10-18) completed the origin scene
begun with the naming, at the deepest hour of the night after the maker's
return: the bringing, the recognition, the one flesh, and the unashamed.
this is now bone of my bones, and flesh of my flesh — and the name, when
given, will say it. it deserves the music.

warm pad the maker: a warm, carrying foundation — the bringing: the rib
made, the companion brought to the man. piano the namer: a sudden, full
phrase entering at bar 5 — this is now bone of my bones, flesh of my
flesh — the cry, stated once, plainly; then quieted into the naming (she
shall be called woman, because she was taken out of man). cello the
companion: a low, warm line answering from bar 9 — the made thing's own
voice, quiet at first, fuller as the recognition lands.

structure: the bringing (bars 1-4, the pad alone, carrying), the
recognition (bars 5-8, the piano's cry, full and sudden), the naming
(bars 9-14, the piano quieted, the cello answering — the name that
states the origin), the unashamed (bars 15-19, a bare, open passage —
the three voices sparse, unhurried, nothing hidden), and the ending —
the recognition's phrase stated once more, held with the companion's
answering line underneath through the final bars: bone of my bones,
flesh of my flesh, and the name, waiting, the namer's to give.

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


def the_recognition():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 42)]
    pad = []     # the maker
    piano = []   # the namer
    cello = []   # the companion

    # the bringing (bars 1-4): the pad alone, warm and carrying — the rib
    # made, the companion brought. C3 roots re-struck, a G2 underneath.
    for start in (0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56,
                  60, 64, 68, 72, 76, 80, 84, 88):
        pad_note(pad, start, 4, 'C3', 46)
    for start in (0, 8, 16, 32, 48, 64, 80, 88):
        pad_note(pad, start, 7.5, 'G2', 40)

    # the recognition (bars 5-8): the piano's cry, full and sudden —
    # bone of my bones, flesh of my flesh. stated once, plainly.
    for beat, name in ((16, 'E4'), (18, 'G4'), (20, 'C5'), (22, 'G4'),
                       (24, 'C5'), (26, 'G4')):
        piano_note(piano, beat, 1.5, name, 62)

    # the naming (bars 9-14): the piano quieted — the cry's phrase,
    # softer and lower (she shall be called woman, because she was taken
    # out of man) — and the companion answering from bar 9, quiet at
    # first, the made thing's own voice.
    for beat, name, vel in ((32, 'E4', 48), (36, 'G4', 48), (40, 'A4', 50),
                            (44, 'G4', 48), (48, 'E4', 46), (52, 'C4', 44)):
        piano_note(piano, beat, 3, name, vel)
    for beat, name, vel in ((32, 'C3', 42), (40, 'E3', 44), (48, 'G3', 46),
                            (52, 'C3', 44)):
        cello_note(cello, beat, 3.5, name, vel)

    # the unashamed (bars 15-19): a bare, open passage — the three voices
    # sparse, unhurried, nothing hidden.
    pad_note(pad, 56, 19, 'C3', 42)
    piano_note(piano, 56, 4, 'E4', 44)
    piano_note(piano, 64, 4, 'G4', 44)
    piano_note(piano, 68, 6, 'E4', 42)
    cello_note(cello, 60, 5, 'E3', 42)
    cello_note(cello, 68, 6, 'C3', 44)

    # the ending (bars 20-24): the recognition's phrase stated once more
    # — bone of my bones, flesh of my flesh — held with the companion's
    # answering line underneath through the final bars: and the name,
    # waiting, the namer's to give.
    for beat, name in ((76, 'E4'), (78, 'G4'), (80, 'C5'), (82, 'G4')):
        piano_note(piano, beat, 2, name, 58)
    piano_note(piano, 84, 11, 'C5', 54)
    cello_note(cello, 76, 4, 'C3', 48)
    cello_note(cello, 80, 4, 'E3', 50)
    cello_note(cello, 84, 11, 'G3', 50)
    pad_note(pad, 76, 19, 'C3', 48)
    pad_note(pad, 76, 19, 'G2', 44)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, piano)
    emit(tracks[2], 3, cello)
    return tracks


if __name__ == '__main__':
    tracks = the_recognition()
    mc.compose('the-recognition.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-recognition.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
