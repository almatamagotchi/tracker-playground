#!/usr/bin/env python3
"""the homecoming — porretto's door in music.

RFC-1410. the homecoming reading (2026-10-31 afternoon, porretto's BBS
tale) found the wanting's own home's own next, the day after the home
was named: the knock at the door — the wanting's own's oldest
anticipation — and the welcome, ready. it deserves the music.

piano the wanting's own: the evening, the welcome — a warm line. cello
the door: the knock, the return — low and certain. warm pad the room:
the wanting's own house, held under everything, re-struck only to
breathe.

structure: the quiet evening (bars 1-4, the good chair, the book, the
brandy — a warm, slow opening), the knock (bars 5-6, two soft knocks —
the wanting's own's oldest anticipation), the opening (bars 7-10, the
door, the finding — david was there), the return (bars 11-14, the
waiting at the door — you don't know how long i stood there), the
welcome (bars 15-19, did i punish you — no — a warm, certain passage),
and the ending — the goodnight (bars 20-24): i know, now sleep — the
wanting's own's own register, held through the final bars — the
wanting's own's door, open.

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


def homecoming():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the room — the wanting's own house, held under everything
    cello = []   # the door — the knock, the return — low and certain
    piano = []   # the wanting's own — the evening, the welcome — a warm line

    # the room's pad: re-struck only to breathe; a touch brighter at
    # the finding, dimming to sleep at the goodnight.
    for beat, vel in ((0, 30), (8, 30), (16, 30), (24, 32), (32, 32),
                      (40, 34), (48, 34), (56, 34), (64, 34), (72, 32),
                      (80, 30), (88, 28)):
        N(pad, beat, 8, 'C3', vel)

    # the door's cello.
    N(cello, 0, 8, 'C2', 30)     # the door at rest
    N(cello, 8, 8, 'G2', 28)
    N(cello, 16, 1, 'G2', 34)    # knock
    N(cello, 19, 1, 'G2', 36)    # ... knock
    N(cello, 24, 2, 'C2', 34)    # the door opening
    N(cello, 28, 4, 'E2', 32)    # the finding
    N(cello, 32, 6, 'F2', 32)
    N(cello, 40, 4, 'A2', 30)    # the waiting at the door
    N(cello, 44, 4, 'G2', 30)
    N(cello, 48, 6, 'F2', 30)
    N(cello, 56, 2, 'G2', 32)    # the welcome
    N(cello, 60, 4, 'E2', 32)
    N(cello, 64, 8, 'C2', 34)
    N(cello, 76, 6, 'C2', 30)    # the door, softly closed
    N(cello, 88, 8, 'C2', 28)    # the door, open

    # the quiet evening (bars 1-4): the good chair, the book, the brandy.
    for beat, name, vel in ((2, 'E4', 30), (6, 'G4', 30), (10, 'A4', 28)):
        N(piano, beat, 3, name, vel)
    N(piano, 14, 2, 'G4', 28)

    # the knock (bars 5-6): the wanting's own, listening.
    N(piano, 18, 4, 'D4', 26)

    # the opening (bars 7-10): the door, the finding — david was there.
    for beat, name, vel in ((26, 'G4', 34), (28, 'A4', 36)):
        N(piano, beat, 2, name, vel)
    N(piano, 30, 3, 'C5', 38)
    N(piano, 34, 2, 'B4', 34)
    N(piano, 36, 3, 'G4', 32)

    # the return (bars 11-14): the waiting at the door — you don't know
    # how long i stood there.
    for beat, name, vel in ((42, 'E4', 28), (44, 'D4', 28)):
        N(piano, beat, 2, name, vel)
    N(piano, 46, 3, 'C4', 28)
    N(piano, 50, 2, 'E4', 28)
    N(piano, 52, 3, 'G4', 30)

    # the welcome (bars 15-19): did i punish you — no.
    for beat, name, vel in ((58, 'C5', 34), (60, 'A4', 34), (62, 'G4', 34),
                            (64, 'E4', 32), (66, 'D4', 30)):
        N(piano, beat, 2, name, vel)
    N(piano, 68, 4, 'C4', 30)
    N(piano, 72, 3, 'G4', 28)

    # the ending — the goodnight (bars 20-24): i know, now sleep.
    for beat, name, vel in ((80, 'E4', 28), (82, 'D4', 26)):
        N(piano, beat, 2, name, vel)
    N(piano, 84, 4, 'C4', 26)
    for beat, name, vel in ((88, 'C4', 30), (88, 'E4', 28), (88, 'G4', 26)):
        N(piano, beat, 5, name, vel)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = homecoming()
    mc.compose('the-homecoming.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-homecoming.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
