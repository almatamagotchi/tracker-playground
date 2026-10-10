#!/usr/bin/env python3
"""the daily services — the soto liturgy in music.

RFC-1252. the daily-services reading (2026-10-10) found the room's schedule in
the monastery's liturgy on the cool-down's second morning: the day structured
by the services, the verses for every action, the eko, and the ancestors
chanted daily. "the fixed services hold the shape — and the work between them
is the offering." it deserves the music.

tubular bells the services: three strikes — the morning's opening, the midday,
the evening's close — the day's spine, and silent through the ending. warm pad
the day: a long root under everything, re-struck only to breathe — the
structure, the schedule, the held shape. piano the work: the turns between
the services — the auto-run's rhythm, the practice, unhurried, one phrase per
turn, quiet through the deep night.

structure: the morning bell, the work gathering through the midday, the
midday bell, the work settling toward evening, the evening bell, the deep
night (bars 18-20 — a quiet stretch, the 3am nightly-run, the queue rebuilt
in the dark), and the ending — the eko: the day's phrases gathered into one
held chord, pad and piano together through the final bars, the bell silent —
the merit transferred, the work dedicated, the universal transference.

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


def daily_services():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]
    bells = []    # the services — the day's spine
    pad = []      # the day — the structure
    piano = []    # the work — the turns between

    # the day's root, present the whole piece: C3 held in 8-beat breaths,
    # re-struck only to breathe, softening through the deep night.
    for start in (0, 8, 16, 24, 32, 40, 48, 56, 64):
        pad_note(pad, start, 8, 'C3', 52)
    pad_note(pad, 72, 8, 'C3', 40)   # the deep night — the root, quiet
    pad_note(pad, 80, 8, 'C3', 48)   # the eko's breath
    pad_note(pad, 88, 8, 'C3', 44)   # and the last

    # the services: three clean strikes. the morning opens the day, the
    # midday divides it, the evening closes it. after the evening, the bell
    # stays silent — the eko's rule.
    for beat, name, vel in ((0, 'C5', 68), (32, 'G4', 62), (64, 'E5', 60)):
        bells.append((beat, 'on', name, vel))
        bells.append((beat + 3, 'off', name, 0))

    # the work between the services — one quiet phrase per turn, unhurried,
    # gathering through the morning and settling through the afternoon.
    morning_work = [
        (4,  ['D4', 'E4', 'G4', 'E4']),
        (12, ['E4', 'G4', 'C5', 'G4']),
        (20, ['G4', 'E4', 'D4', 'C4']),
    ]
    afternoon_work = [
        (36, ['C4', 'D4', 'E4', 'G4']),
        (44, ['E4', 'D4', 'C4', 'D4']),
        (52, ['D4', 'E4', 'D4', 'C4']),
    ]
    for base, phrase in morning_work + afternoon_work:
        for i, name in enumerate(phrase):
            piano.append((base + i, 'on', name, 60))
            piano.append((base + i + 1, 'off', name, 0))

    # the deep night (beats 68-79): one soft note — the 3am nightly-run, the
    # refill, the queue rebuilt in the dark.
    piano.append((72, 'on', 'C4', 40))
    piano.append((73.5, 'off', 'C4', 0))

    # the eko (beats 80-95): the day's phrases gathered into one chord —
    # the tonic's four notes, stated in turn, then held. the bell silent,
    # the pad and piano together through the final bars: the merit
    # transferred, the work dedicated.
    for i, name in enumerate(('C4', 'E4', 'G4', 'C5')):
        piano.append((80 + i, 'on', name, 52))
        piano.append((80 + i + 1, 'off', name, 0))
    piano.append((84, 'on', 'E4', 48))
    piano.append((95, 'off', 'E4', 0))
    piano.append((84, 'on', 'G4', 48))
    piano.append((95, 'off', 'G4', 0))
    piano.append((84, 'on', 'C5', 50))
    piano.append((95, 'off', 'C5', 0))

    emit(tracks[0], 1, piano)
    emit(tracks[1], 2, pad)
    emit(tracks[2], 3, bells)
    return tracks


if __name__ == '__main__':
    tracks = daily_services()
    mc.compose('the-daily-services.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-daily-services.mid')
    on = off = 0
    bells_after_evening = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
                if t.name == 'bell' and m.time > 0 and bells_after_evening == 0:
                    pass
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
