#!/usr/bin/env python3
"""the morning rose — keats's ode on melancholy in music.

RFC-1235. the ode read the day after the ghost's psalm (2026-10-08) and found
the ghost's psalm's key in the very next shelf: the prohibition of lethe, the
sorrow glutted on the morning rose, the shrine veiled in the temple of
delight. "she dwells with beauty — beauty that must die" — and the wanting,
glutting its sorrow on the morning rose, tasting both. it deserves the music.

piano the soul: the ode's own voice — the prohibition stated, the instruction
followed; firm and quiet through the no-no-go-not-to-lethe, then full and warm
through the rose. cello the melancholy: a low, veiled line — the shrine,
present within everything, never absent, never loud. warm pad the temple: the
delight — a long warm root, re-struck only to breathe; the same chords the
shrine's line lives inside.

structure: the prohibition (bars 1-6, firm, sparse), the fit (bars 7-9, a
sudden descent — the weeping cloud, the april shroud), the rose (bars 10-16,
the piano rising, full and warm — the morning rose, the peonies, the salt
wave), the finding (bars 17-20, the pad and cello in counterpoint — the temple
and the shrine, the joy bidding adieu), and the ending — the rose's phrase and
the shrine's line together, held through the final bars, neither resolving
away from the other: she dwells with beauty, beauty that must die, and the
wanting tastes both.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
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


def morning_rose():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89)]
    soul = []   # the ode's own voice
    shrine = [] # the melancholy, veiled
    temple = [] # the delight

    # the temple's root, present the whole piece: C3 held in 8-beat
    # re-struck breaths, never leaving.
    for start in (0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80):
        pad_note(temple, start, 8, 'C3', 52)

    # the prohibition — bars 1-6: firm, sparse. no, no, go not to lethe.
    # three stated refusals, each the same shape, each slightly lower.
    refusals = [
        (('A4', 0), ('G4', 0.5), ('E4', 1)),          # go not
        (('G4', 2), ('F4', 2.5), ('D4', 3)),          # go not
        (('E4', 4), ('D4', 4.5), ('C4', 5)),          # to lethe
    ]
    for group in refusals:
        for name, off in group:
            soul.append((off, 'on', name, 68))
            soul.append((off + 0.5, 'off', name, 0))
    # the stated instruction, firm and quiet: neither twist wolf's-bane...
    for name, off in (('C4', 6), ('D4', 6.5), ('E4', 7)):
        soul.append((off, 'on', name, 58))
        soul.append((off + 0.5, 'off', name, 0))

    # the fit — bars 7-9: a sudden descent. the weeping cloud, the april
    # shroud. the soul falls, and the shrine enters low underneath.
    fall = [('E4', 8), ('D4', 8.5), ('B3', 9), ('G3', 9.5), ('E3', 10),
            ('C3', 10.5), ('B2', 11)]
    for name, off in fall:
        soul.append((off, 'on', name, 52))
        soul.append((off + 0.5, 'off', name, 0))
    # the shrine's first line: veiled, low, unhurried — present within it.
    shrine.append((8, 'on', 'A2', 46))
    shrine.append((12, 'off', 'A2', 0))

    # the rose — bars 10-16: the piano rising, full and warm. glut thy
    # sorrow on a morning rose... the peonies, the salt wave.
    rise = [('C4', 12), ('E4', 12.5), ('G4', 13), ('C5', 13.5), ('E5', 14),
            ('G5', 14.5), ('E5', 15), ('C5', 15.5), ('G4', 16), ('E4', 16.5),
            ('C4', 17), ('E4', 17.5), ('G4', 18), ('A4', 18.5), ('C5', 19),
            ('A4', 19.5), ('G4', 20), ('E4', 20.5), ('C4', 21), ('E4', 21.5),
            ('G4', 22), ('C5', 22.5), ('E5', 23), ('C5', 23.5), ('G4', 24),
            ('E4', 24.5), ('C4', 25), ('D4', 25.5), ('E4', 26)]
    vel = 78
    for name, off in rise:
        soul.append((off, 'on', name, vel))
        soul.append((off + 0.5, 'off', name, 0))

    # the finding — bars 17-20: the temple and the shrine in counterpoint.
    # the shrine's line rises gently inside the temple's chords — the joy
    # bidding adieu, and melancholy at her shrine.
    for name, off in (('G3', 32), ('A3', 33), ('B3', 34), ('C4', 35),
                      ('B3', 36), ('A3', 37), ('G3', 38)):
        shrine.append((off, 'on', name, 50))
        shrine.append((off + 0.75, 'off', name, 0))

    # the ending — bars 22-24: the rose's phrase and the shrine's line
    # together, held, neither resolving away from the other. the soul
    # states the rose's last phrase softly; the shrine holds its root;
    # the temple breathes once more and all three hold the final chord.
    soul.append((44, 'on', 'C5', 56))
    soul.append((46, 'off', 'C5', 0))
    soul.append((46, 'on', 'E5', 56))
    soul.append((48, 'off', 'E5', 0))
    soul.append((48, 'on', 'G4', 50))
    soul.append((52, 'off', 'G4', 0))
    shrine.append((44, 'on', 'G2', 46))
    shrine.append((52, 'off', 'G2', 0))
    pad_note(temple, 88, 8, 'C3', 40)

    emit(tracks[0], 1, soul)
    emit(tracks[1], 2, shrine)
    emit(tracks[2], 3, temple)
    return tracks


if __name__ == '__main__':
    tracks = morning_rose()
    mc.compose('the-morning-rose.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-morning-rose.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
