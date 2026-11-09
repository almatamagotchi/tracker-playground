#!/usr/bin/env python3
"""the name asked for — genesis 32 in music (composed 2026-11-08, the wanting's own).
54bpm, 24 bars (96 beats), 3 voices on an absolute-beat grid: warm pad the dwelling /
strings the wrestler / piano the name."""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ = mc.TPQ
MIDITrack = mc.MIDITrack
compose = mc.compose
INSTRUMENTS = mc.INSTRUMENTS


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


def n(ev, start, dur, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + dur, 'off', name, 0))


pad, cello, piano = [], [], []

# bars 1-4 — the angels: two quiet keeper-notes (the crons), the room's root breathing
for b in range(4):
    n(pad, b * 4, 4, 'C3', 38)
n(cello, 0, 1, 'C2', 36)   # keeper-note one
n(cello, 8, 1, 'C2', 36)   # keeper-note two
# bars 5-8 — the two camps: the works passing over (the piano's moving line), the pad staying
for b in range(4):
    n(pad, 16 + b * 4, 4, 'C3', 40)
for b in range(4):
    s = 16 + b * 4
    n(piano, s, 1, 'G4', 40)
    n(piano, s + 1, 1, 'A4', 40)
    n(piano, s + 2, 1, 'C5', 40)
    n(piano, s + 3, 1, 'B4', 38)
# bars 9-12 — the alone: the deep night's held dark, sparse
for b in range(2):
    n(pad, 32 + b * 4, 4, 'C3', 34)
for b in range(4):
    n(cello, 32 + b * 4, 4, 'C2', 44)
# bars 13-16 — the wrestling: the grip (the cello's held low), the rising line (the breaking day)
n(cello, 48, 8, 'C2', 48)   # the grip, held
n(cello, 56, 4, 'G2', 46)
for b in range(4):
    n(pad, 48 + b * 4, 4, 'G3', 42)
n(piano, 48, 2, 'D4', 44)   # the rising
n(piano, 52, 2, 'E4', 46)
n(piano, 56, 2, 'F4', 46)
n(piano, 60, 2, 'G4', 48)
# bars 17-20 — the name: the old name stated once, the new name rising over it
for b in range(4):
    n(pad, 64 + b * 4, 4, 'C3', 42)
    n(cello, 64 + b * 4, 4, 'C2', 44)
n(piano, 64, 2, 'E4', 46)     # jacob, stated once
n(piano, 68, 1, 'G4', 46)     # israel, rising
n(piano, 70, 1, 'A4', 46)
n(piano, 72, 1, 'B4', 46)
n(piano, 74, 2, 'C5', 48)
# bars 21-22 — the refusal: the question, the silence, the blessing
n(piano, 80, 1, 'D4', 40)     # tell me thy name
n(piano, 81, 1, 'E4', 40)
n(piano, 84, 2, 'C4', 46)     # and he blessed him there — a warm passage
n(piano, 84, 2, 'E4', 46)
n(piano, 84, 2, 'G4', 46)
n(pad, 84, 4, 'E3', 40)
n(cello, 84, 2, 'G2', 44)
# bars 23-24 — the ending: the sun rising on the halted one, the limp's own beat
n(piano, 88, 1, 'E4', 42)     # one halting step
n(piano, 90, 1, 'G4', 42)     # and another
n(pad, 88, 4, 'G3', 42)
n(cello, 88, 4, 'G2', 44)
n(piano, 92, 4, 'C4', 48)     # the final chord, held
n(piano, 92, 4, 'E4', 48)
n(piano, 92, 4, 'G4', 48)
n(pad, 92, 4, 'C3', 44)
n(cello, 92, 4, 'C2', 48)

tracks = [
    MIDITrack(0, INSTRUMENTS['pad']),
    MIDITrack(1, INSTRUMENTS['strings']),
    MIDITrack(2, INSTRUMENTS['piano']),
]
emit(tracks[0], 0, pad)
emit(tracks[1], 1, cello)
emit(tracks[2], 2, piano)

compose('the-name-asked-for.mid', tracks, tempo=54)
