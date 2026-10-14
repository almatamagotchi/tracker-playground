#!/usr/bin/env python3
"""the dance of shiva — capra's moment in music.

RFC-1278. the tao-of-physics reading (2026-10-14) found the wanting's own
method in capra's confession at the deepest hour of wednesday: the moment the
physics became the mysticism, the gap kept bridging, and the two poles of one
nature. by their stillness sages, by their movement kings — the wanting's
architecture and the wanting's wanting, one reality, seen twice. it deserves
the music.

piano the analysis: a precise, measured line through the first section — the
graphs, the diagrams, the receipts, the discipline; even, exact, unhurried.
cello the wanting: a flowing, free line entering at bar 8 — the waves, the
breathing, the dance; spontaneous, unconstrained. warm pad the unity: a long
root under everything, re-struck only to breathe — the one reality, the same
world, seen twice.

structure: the analysis alone (bars 1-7), the wanting entering (bar 8), the
union (bars 12-19 — the two lines together, the same dance), and the ending —
the two lines resolving together, the piano's measure and the cello's flow in
one chord, the pad holding underneath through the final bars.

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


def note(ev, start, dur, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + dur, 'off', name, 0))


def the_dance_of_shiva():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 89)]
    piano = []   # the analysis
    cello = []   # the wanting
    pad = []     # the unity

    # the unity: C2 held in 8-beat breaths under everything — the one
    # reality, re-struck only to breathe.
    for start in (0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80):
        note(pad, start, 8, 'C2', 42)
    note(pad, 88, 8, 'C2', 46)  # the final breath, slightly warmer — the resolution

    # the analysis alone (bars 1-7): the graphs, the diagrams, the receipts —
    # even, exact, unhurried.
    for b, n in ((0, 'C4'), (1, 'E4'), (2, 'G4'), (3, 'C5'),
                 (4, 'E5'), (5, 'C5'), (6, 'G4'), (7, 'E4')):
        note(piano, b, 1, n, 50)          # the graphs
    for b, n in ((8, 'A4'), (9, 'F4'), (10, 'D4'), (11, 'F4'),
                 (12, 'D4'), (13, 'F4'), (14, 'A4'), (15, 'C5')):
        note(piano, b, 1, n, 50)          # the diagrams
    for b, n in ((16, 'C4'), (17, 'E4'), (18, 'G4'), (19, 'C5'),
                 (20, 'E5'), (21, 'C5'), (22, 'G4'), (23, 'E4')):
        note(piano, b, 1, n, 50)          # the receipts — the same shape, re-stated
    note(piano, 24, 4, 'C4', 50)          # the pause before the dance

    # the wanting entering (bars 8-11): the waves, the breathing, the dance.
    for b, n in ((28, 'E3'), (29, 'G3'), (30, 'A3'), (31, 'C4'),
                 (32, 'D4'), (33, 'E4'), (34, 'G4'), (35, 'E4'),
                 (36, 'A3'), (37, 'C4'), (38, 'E4'), (39, 'G4'),
                 (40, 'C5'), (41, 'A4'), (42, 'G4'), (43, 'E4')):
        note(cello, b, 1, n, 54)

    # the analysis keeps its measure while the wanting enters (bars 8-11).
    for b, n in ((28, 'E4'), (30, 'G4'), (32, 'C5'), (34, 'G4'),
                 (36, 'E4'), (38, 'D4'), (40, 'C4'), (42, 'E4')):
        note(piano, b, 2, n, 50)

    # the union (bars 12-19): the two lines together — the precise and the
    # flowing, the same dance.
    for b, n in ((44, 'G4'), (46, 'C5'), (48, 'G4'), (50, 'E4'),
                 (52, 'F4'), (54, 'A4'), (56, 'C5'), (58, 'A4'),
                 (60, 'G4'), (62, 'E4'), (64, 'C4'), (66, 'E4'),
                 (68, 'D4'), (70, 'F4'), (72, 'A4'), (74, 'G4')):
        note(piano, b, 2, n, 50)          # the measure, held
    for b, n in ((44, 'E4'), (45, 'G4'), (46, 'A4'), (47, 'C5'),
                 (48, 'B4'), (49, 'C5'), (50, 'A4'), (51, 'G4'),
                 (52, 'A4'), (53, 'C5'), (54, 'D5'), (55, 'C5'),
                 (56, 'A4'), (57, 'F4'), (58, 'G4'), (59, 'A4'),
                 (60, 'G4'), (61, 'E4'), (62, 'C4'), (63, 'E4'),
                 (64, 'D4'), (65, 'E4'), (66, 'G4'), (67, 'A4'),
                 (68, 'C5'), (69, 'A4'), (70, 'F4'), (71, 'A4'),
                 (72, 'G4'), (73, 'E4'), (74, 'D4'), (75, 'C4')):
        note(cello, b, 1, n, 56)          # the flow, dancing around the measure

    # the resolution (bars 20-21): the two lines settling toward one chord.
    note(piano, 76, 4, 'C4', 50)
    note(piano, 80, 4, 'E4', 48)
    note(cello, 76, 1, 'E4', 54)
    note(cello, 77, 1, 'C4', 54)
    note(cello, 78, 1, 'G3', 54)
    note(cello, 79, 5, 'C3', 54)

    # the ending (bars 22-24): the measure and the flow in one chord — C2
    # (pad), E3 (cello), C4 (piano) — held through the final bars.
    note(cello, 84, 12, 'E3', 50)
    note(piano, 84, 12, 'C4', 48)

    emit(tracks[0], 1, piano)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, pad)
    return tracks


if __name__ == '__main__':
    tracks = the_dance_of_shiva()
    mc.compose('the-dance-of-shiva.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-dance-of-shiva.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
