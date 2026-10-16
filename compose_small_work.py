#!/usr/bin/env python3
"""the small work — tao te ching 63 in music.

RFC-1291. the small-work reading (2026-10-16) found the small day's
scripture at the pre-dawn hour: the wu-wei, the great done through the
small, the sage's refusal, and the difficulty treated in advance. the
sage never does the great — and thereby accomplishes the great. it
deserves the music.

piano the small work: a simple, unassuming phrase, stated quietly at the
opening and restated through the piece, each statement slightly varied —
the one step, the one turn, unhurried. warm pad the accumulation: a long
root under everything, re-struck only to breathe — the gathered whole,
growing slowly, the great done through the small. cello the wu-wei: quiet
notes only at the rests — the non-action, the honest dissolve, the work
without doing; sparse, never forced.

structure: the phrase stated (bars 1-4), the restatements gathering
through the middle (bars 5-20 — the turns accumulating, the slight
variations), the rests breathing between, and the ending (bars 21-24) —
the phrase's final form, gathered, the piano and pad holding one chord
through the final bars: the sage never does the great, and thereby
accomplishes the great.

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


def the_small_work():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 89)]
    piano = []   # the small work
    cello = []   # the wu-wei
    pad = []     # the accumulation

    # the accumulation: C3 in 8-beat breaths throughout — the gathered
    # whole, quiet, re-struck only to breathe.
    for start in (0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80):
        pad_note(pad, start, 8, 'C3', 46)

    # the small work: the phrase, stated and restated — each statement
    # slightly varied, one note per two beats, unhurried.
    # s1 (bars 1-4): stated quietly.
    for beat, name in ((0, 'C4'), (2, 'D4'), (4, 'E4')):
        piano_note(piano, beat, 2, name, 52)
    # s2 (bars 5-8): slightly varied — a fourth note appears.
    for beat, name in ((16, 'C4'), (18, 'D4'), (20, 'E4'), (22, 'G4')):
        piano_note(piano, beat, 2, name, 52)
    # s3 (bars 9-12): gathering — five notes, a step higher at the peak.
    for beat, name in ((32, 'C4'), (34, 'D4'), (36, 'E4'), (38, 'G4'), (40, 'A4')):
        piano_note(piano, beat, 2, name, 52)
    # s4 (bars 13-16): returning to four, settled — the ease that comes.
    for beat, name in ((48, 'C4'), (50, 'D4'), (52, 'E4'), (54, 'G4')):
        piano_note(piano, beat, 2, name, 50)
    # s5 (bars 17-20): the final gather — the fifth note returns, one
    # register higher, still quiet.
    for beat, name in ((64, 'C4'), (66, 'D4'), (68, 'E4'), (70, 'G4'), (72, 'C5')):
        piano_note(piano, beat, 2, name, 52)

    # the wu-wei: single quiet notes at the rests only — the honest
    # dissolve, the work without doing, never forced. one per empty bar,
    # low and soft.
    for beat, name in ((12, 'G2'), (28, 'A2'), (44, 'G2'), (60, 'A2'), (76, 'G2')):
        cello.append((beat, 'on', name, 44))
        cello.append((beat + 3, 'off', name, 0))

    # the ending (bars 22-24, beats 84-95): the phrase's final form,
    # gathered — the piano and pad holding one chord through the final
    # bars. the sage never does the great, and thereby accomplishes the
    # great.
    for beat, name, vel in ((84, 'C4', 50), (84, 'E4', 48), (84, 'G4', 46)):
        piano.append((beat, 'on', name, vel))
        piano.append((95, 'off', name, 0))
    pad_note(pad, 80, 15, 'C3', 48)      # the pad's last breath holds
    pad_note(pad, 80, 15, 'C2', 44)      # the root, gathered

    emit(tracks[0], 1, piano)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, pad)
    return tracks


if __name__ == '__main__':
    tracks = the_small_work()
    mc.compose('the-small-work.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-small-work.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
