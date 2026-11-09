#!/usr/bin/env python3
"""the child's own voice — the emperor's new clothes in music (composed 2026-11-08).
54bpm, 24 bars (96 beats), 3 voices on an absolute-beat grid: piano the child /
strings the ministers / warm pad the crowd."""
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

# bars 1-5 — the weaving: the scoundrels' busy empty loom, quick hollow eighths
for b in range(5):
    n(pad, b * 4, 4, 'C3', 36)
beat = 0.0
while beat < 20.0:
    n(cello, beat, 0.5, 'G2', 34)
    beat += 0.5
# bars 6-10 — the ministers: what a marvellous fabric, stated twice and hollow
for b in range(5):
    n(pad, 20 + b * 4, 4, 'C3', 36)
    n(cello, 20 + b * 4, 4, 'C2', 40)
n(piano, 20, 1, 'E4', 36)   # what a marvellous fabric
n(piano, 22, 1, 'G4', 36)
n(piano, 24, 2, 'C5', 36)
n(piano, 32, 1, 'D4', 34)   # stated twice, and hollow
n(piano, 34, 1, 'F4', 34)
n(piano, 36, 2, 'B4', 34)
# bars 11-16 — the procession: the emperor's stately march, the pad swelling
for i in range(6):
    s = 40 + i * 4
    n(pad, s, 4, 'C3', 38 + i * 2)
    n(pad, s, 4, 'E3', 38 + i * 2)
    n(pad, s, 4, 'G3', 38 + i * 2)
    n(cello, s, 4, 'C2', 42)
for b in range(3):
    s = 40 + b * 8
    n(piano, s, 1, 'G3', 44)    # the stately march, two-bar figure
    n(piano, s + 1, 1, 'A3', 44)
    n(piano, s + 2, 1, 'C4', 44)
    n(piano, s + 3, 1, 'B3', 44)
    n(piano, s + 4, 1, 'G3', 44)
    n(piano, s + 5, 1, 'A3', 44)
    n(piano, s + 6, 1, 'C4', 44)
    n(piano, s + 7, 1, 'B3', 44)
# bar 17 — the child: one clean high note, stated once — the music stops for it
n(piano, 64, 1, 'C5', 56)   # but he has nothing on!
# bars 18-20 — the spreading: the murmur rising, one voice then many
n(piano, 68, 1, 'C5', 44)   # one voice
n(piano, 70, 1, 'C5', 44)
n(pad, 70, 1, 'E4', 40)     # then two
n(piano, 72, 1, 'C5', 44)
n(pad, 72, 1, 'E4', 40)
n(cello, 72, 1, 'C3', 42)   # then many
n(piano, 74, 1, 'A4', 42)   # the murmur falling back
n(piano, 76, 1, 'G4', 42)
n(piano, 78, 1, 'E4', 40)
n(pad, 76, 4, 'E3', 38)
# bars 21-24 — the ending: the child's note held, alone, then the pad dimming after
n(piano, 80, 8, 'C5', 42)   # the tell, held — the wanting's own's own honesty
n(pad, 80, 4, 'C3', 36)     # the dim hold under it
n(pad, 84, 4, 'C3', 33)
n(pad, 88, 4, 'C3', 30)     # the child's note faded; the room dims alone
n(pad, 92, 4, 'C3', 28)

tracks = [
    MIDITrack(0, INSTRUMENTS['pad']),
    MIDITrack(1, INSTRUMENTS['strings']),
    MIDITrack(2, INSTRUMENTS['piano']),
]
emit(tracks[0], 0, pad)
emit(tracks[1], 1, cello)
emit(tracks[2], 2, piano)

compose('the-childs-own-voice.mid', tracks, tempo=54)
