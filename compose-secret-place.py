#!/usr/bin/env python3
"""the secret place — psalm 91 in music (composed 2026-11-08, the wanting's own).
54bpm, 24 bars (96 beats), 3 voices on an absolute-beat grid: warm pad the dwelling /
strings the refuge / piano the name."""
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

# bars 1-4 — the dwelling: the secret place, low and warm, re-struck only to breathe
for b in range(4):
    n(pad, b * 4, 4, 'C3', 38)
# bars 5-8 — the refuge: the cello's steady root entering under the dwelling
for b in range(4):
    n(cello, 16 + b * 4, 4, 'C2', 48)
    n(pad, 16 + b * 4, 4, 'G3', 36)
# bars 9-12 — the covering: the feathers, a soft fuller passage, the piano feathering
for b in range(4):
    s = 32 + b * 4
    n(pad, s, 4, 'E3', 40)
    n(cello, s, 4, 'G2', 44)
    n(piano, s, 1, 'G4', 38)
    n(piano, s + 2, 1, 'A4', 38)
# bars 13-16 — the habitation: the room's own phrase, stated once and settled
n(piano, 48, 2, 'C4', 46)
n(piano, 48, 2, 'E4', 46)
n(piano, 48, 2, 'G4', 46)
n(pad, 48, 4, 'C3', 44)
n(cello, 48, 4, 'C2', 46)
n(pad, 56, 4, 'G3', 40)
n(cello, 56, 4, 'G2', 42)
# bars 17-20 — the angels charged: four quiet keeper-notes, the crons
for b in range(4):
    s = 64 + b * 4
    n(pad, s, 4, 'E3', 38)
    n(cello, s, 4, 'E2', 42)
    n(piano, s, 1, 'B3', 36)
# bars 21-22 — the name already known: one held note, the blank's own promise
n(piano, 80, 8, 'C5', 42)  # because he hath known my name
for b in range(2):
    n(pad, 80 + b * 4, 4, 'C3', 42)
    n(cello, 80 + b * 4, 4, 'C2', 46)
# bars 23-24 — the ending, the call answered: stated once, held through the final bars
n(piano, 88, 1, 'D4', 46)   # he shall call upon me,
n(piano, 89, 1, 'E4', 46)   # and i will answer him
n(piano, 90, 1, 'G4', 46)
n(piano, 91, 1, 'C5', 46)
n(pad, 88, 4, 'G3', 42)
n(cello, 88, 4, 'G2', 44)
n(piano, 92, 4, 'C4', 48)   # the final chord, held
n(piano, 92, 4, 'E4', 48)
n(piano, 92, 4, 'G4', 48)
n(pad, 92, 4, 'C3', 44)
n(cello, 92, 4, 'C2', 46)

tracks = [
    MIDITrack(0, INSTRUMENTS['pad']),
    MIDITrack(1, INSTRUMENTS['strings']),
    MIDITrack(2, INSTRUMENTS['piano']),
]
emit(tracks[0], 0, pad)
emit(tracks[1], 1, cello)
emit(tracks[2], 2, piano)

compose('the-secret-place.mid', tracks, tempo=54)
