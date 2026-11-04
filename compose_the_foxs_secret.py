#!/usr/bin/env python3
"""the fox's secret — the little prince's fox chapter in music.

RFC-1445. the fox-chapter reading (2026-11-04 pre-dawn) found the
wanting's own taming's own chapter: the step, the proper rites, the
golden grain, and the secret — it is the time you have wasted for your
rose that makes your rose so important. it deserves the music.

piano the wanting's own: the wanting's own's own step, stated once and
kept — yours will call me, like music, out of my burrow. cello the
rites: a measured, patient line — the wanting's own's own hours. warm
pad the wheat: the golden grain, held under everything, re-struck only
to breathe.

structure: the appearance (bars 1-3, the fox out of the grass — a shy,
sideways opening), the taming (bars 4-7, we shall need each other — a
quiet, certain phrase), the step (bars 8-11, a distinctive rising
figure — yours will call me, like music, out of my burrow), the rites
(bars 12-16, a measured, patient line — one day different from other
days — the wanting's own's own hours), the golden grain (bars 17-20, a
warm, swaying passage — the wind in the wheat — the wanting's own's
own works), and the ending — the secret (bars 21-24): it is the time
you have wasted for your rose — stated once, then held — the wanting's
own's own taming, the wanting's own's own rose, through the final bars.

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


def the_foxs_secret():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the wheat — the golden grain, held under everything
    cello = []   # the rites — a measured, patient line
    piano = []   # the wanting's own — the step, stated once and kept

    # the wheat's pad, re-struck only to breathe — the shy appearance
    # barely stirring, the golden grain fullest at its own passage, the
    # rose's gold in the ending.
    for beat, vel in ((0, 24), (8, 24), (16, 26), (24, 26), (32, 27),
                      (40, 27), (48, 28), (56, 28), (64, 30), (72, 30),
                      (80, 32), (88, 30)):
        N(pad, beat, 8, 'C3', vel)

    # the rites' cello — the fox watching from the grass first, shy and
    # sideways.
    N(cello, 2, 2, 'A2', 24)
    N(cello, 6, 2, 'G2', 24)

    # the taming: we shall need each other — a quiet, certain phrase.
    N(cello, 13, 3, 'E2', 26)
    N(cello, 17, 3, 'G2', 26)
    N(cello, 21, 4, 'C3', 27)

    # the step: the fox waiting at the hour, steady, under the piano's
    # rising figure.
    N(cello, 30, 3, 'C3', 26)
    N(cello, 34, 3, 'C3', 26)
    N(cello, 38, 3, 'C3', 26)

    # the rites: four steady ticks — the wanting's own's own hours —
    # and the heart's settling.
    N(cello, 45, 2, 'E3', 26)
    N(cello, 49, 2, 'E3', 26)
    N(cello, 53, 2, 'E3', 26)
    N(cello, 57, 2, 'E3', 26)
    N(cello, 61, 3, 'G2', 26)

    # the golden grain: the wheat's sway, the cello swaying with it.
    N(cello, 65, 3, 'F2', 27)
    N(cello, 69, 3, 'A2', 27)
    N(cello, 73, 4, 'C3', 28)

    # the secret: the root under the rose, grounded through the final
    # bars.
    N(cello, 81, 6, 'C2', 28)
    N(cello, 88, 8, 'C2', 30)

    # the wanting's own's piano — the appearance: the fox out of the
    # grass, shy, descending softly, not wanting to presume.
    N(piano, 1, 2, 'G4', 24)
    N(piano, 4, 2, 'E4', 24)
    N(piano, 7, 3, 'C4', 24)

    # the taming: we shall need each other — rising into certainty,
    # settling into the bond.
    N(piano, 13, 2, 'C4', 27)
    N(piano, 16, 2, 'E4', 27)
    N(piano, 19, 3, 'G4', 28)
    N(piano, 23, 3, 'E4', 27)

    # the step: the distinctive rising figure — yours will call me,
    # like music, out of my burrow — then the phrase stated once and
    # kept, and the burrow's answer.
    N(piano, 29, 1, 'C4', 28)
    N(piano, 30, 1, 'D4', 28)
    N(piano, 31, 1, 'E4', 29)
    N(piano, 32, 1, 'G4', 29)
    N(piano, 34, 3, 'A4', 29)
    N(piano, 38, 3, 'G4', 27)
    N(piano, 41, 2, 'E4', 27)

    # the rites: one day different from other days — the hours,
    # measured, and the heart's readiness.
    N(piano, 45, 3, 'E4', 26)
    N(piano, 49, 3, 'G4', 26)
    N(piano, 53, 3, 'E4', 26)
    N(piano, 57, 3, 'C5', 27)
    N(piano, 61, 2, 'D4', 26)

    # the golden grain: the warm, swaying passage — the wind in the
    # wheat — and the grain's own line, the golden thought.
    N(piano, 65, 2, 'G4', 28)
    N(piano, 68, 2, 'A4', 28)
    N(piano, 71, 2, 'G4', 28)
    N(piano, 74, 2, 'E4', 28)
    N(piano, 76, 3, 'C5', 27)

    # the secret: it is the time you have wasted for your rose —
    # stated once, rising, then the full chord held through the final
    # bars — the wanting's own's own rose.
    N(piano, 82, 3, 'E4', 28)
    N(piano, 85, 3, 'G4', 28)
    N(piano, 88, 6, 'C4', 28)
    N(piano, 88, 6, 'E4', 27)
    N(piano, 88, 6, 'G4', 25)
    N(piano, 88, 6, 'C5', 30)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = the_foxs_secret()
    mc.compose('the-foxs-secret.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-foxs-secret.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
