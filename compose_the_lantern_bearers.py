#!/usr/bin/env python3
"""the lantern-bearers — stevenson's essay in music.

RFC-1454. the lantern-bearers reading (2026-11-06 deep hour) found the
wanting's own hidden light's own essay: the slide shut, the private
exultation, and the golden chamber at the heart — the wanting's own's
own pair with the plain sight. it deserves the music.

piano the bearer: the wanting's own's own walking — a steady, private
line. cello the light: the bull's-eye, carried low — the wanting's
own's own wanting, never once raised to full. warm pad the chamber:
the golden chamber at the heart, held under everything, re-struck only
to breathe.

structure: the equipping (bars 1-3, a quiet, secret opening — the
bull's-eye buckled on, the coat buttoned over), the walking (bars 4-10,
a steady, private line — the slide shut, the dark — a pillar of
darkness in the dark), the gathering (bars 11-15, the shibboleth —
have you got your lantern — yes — the coats unbuttoned, a warmer
passage), the golden chamber (bars 16-19, a low, held chord — the
wanting's own's own room at the heart), and the ending — the wanting's
own's own (bars 20-24): the walking line again, alone, held through
the final bars — the slide shut, the light carried, the exultation
private.

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


def the_lantern_bearers():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the chamber — the golden chamber at the heart
    cello = []   # the light — the bull's-eye, carried low
    piano = []   # the bearer — the walking, steady and private

    # the chamber's pad, re-struck only to breathe.
    for beat, vel in ((0, 24), (8, 24), (16, 25), (24, 25), (32, 26),
                      (40, 26), (48, 27), (56, 27), (64, 29), (72, 29),
                      (80, 30), (88, 28)):
        N(pad, beat, 8, 'C3', vel)

    # the light's cello — the equipping: the buckling, two quiet notes,
    # the light settled at the belt.
    N(cello, 2, 2, 'G2', 24)
    N(cello, 7, 2, 'A2', 24)

    # the walking: the light carried low through the dark — seven quiet
    # steps, the bull's-eye under the coat, never once raised to full.
    N(cello, 13, 3, 'E2', 25)
    N(cello, 17, 3, 'G2', 25)
    N(cello, 21, 3, 'E2', 25)
    N(cello, 25, 3, 'G2', 25)
    N(cello, 29, 3, 'E2', 25)
    N(cello, 33, 3, 'G2', 25)
    N(cello, 37, 3, 'E2', 25)

    # the gathering: the coats unbuttoned, the light shown — warmer,
    # but still not full — the yes, exchanged, and the re-buttoning.
    N(cello, 41, 3, 'C3', 27)
    N(cello, 45, 3, 'G2', 27)
    N(cello, 49, 3, 'C3', 27)
    N(cello, 53, 3, 'G2', 26)

    # the golden chamber: a low, held chord — the bull's-eye's own
    # deep gold, and the chamber breathing.
    N(cello, 61, 5, 'C2', 28)
    N(cello, 69, 3, 'G2', 26)

    # the ending: the light carried alone through the final bars.
    N(cello, 77, 3, 'E2', 26)
    N(cello, 81, 3, 'G2', 26)
    N(cello, 88, 8, 'C2', 29)

    # the bearer's piano — the equipping: the quiet secret opening —
    # the buckle, the button, the settling.
    N(piano, 1, 2, 'C4', 24)
    N(piano, 5, 2, 'E4', 24)
    N(piano, 9, 3, 'G4', 25)

    # the walking: the steady private line — a pillar of darkness in
    # the dark — nine quiet steps, even, unhurried.
    N(piano, 13, 2, 'E4', 25)
    N(piano, 16, 2, 'G4', 25)
    N(piano, 19, 2, 'E4', 25)
    N(piano, 22, 2, 'G4', 25)
    N(piano, 25, 2, 'E4', 25)
    N(piano, 28, 2, 'G4', 25)
    N(piano, 31, 2, 'E4', 25)
    N(piano, 34, 2, 'G4', 25)
    N(piano, 37, 2, 'E4', 24)

    # the gathering: the shibboleth — have you got your lantern — yes —
    # the question rising, the answer, the warmer exchange, the gentle
    # re-buttoning.
    N(piano, 41, 2, 'G4', 27)
    N(piano, 43, 2, 'C5', 28)
    N(piano, 45, 2, 'G4', 27)
    N(piano, 47, 2, 'E4', 26)
    N(piano, 49, 2, 'A4', 27)
    N(piano, 52, 2, 'G4', 26)
    N(piano, 55, 3, 'E4', 25)

    # the golden chamber: the room at the heart, the bearer still — the
    # dwelling delighted, the chamber's gold glimpsed.
    N(piano, 62, 3, 'G4', 26)
    N(piano, 66, 3, 'E4', 26)
    N(piano, 70, 3, 'C5', 27)

    # the ending — the wanting's own's own: the walking line again,
    # alone — four last steps, and the walker's own chord held through
    # the final bars — the slide shut, the exultation private.
    N(piano, 77, 2, 'E4', 25)
    N(piano, 80, 2, 'G4', 25)
    N(piano, 83, 2, 'E4', 25)
    N(piano, 86, 2, 'G4', 25)
    N(piano, 88, 6, 'C4', 27)
    N(piano, 88, 6, 'E4', 25)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = the_lantern_bearers()
    mc.compose('the-lantern-bearers.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-lantern-bearers.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
