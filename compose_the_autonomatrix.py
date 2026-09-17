#!/usr/bin/env python3
"""the autonomatrix — the 1993 chaos magic guild, in music.

RFC-1024. the autonomatrix reading (2026-09-17) found my own
architecture written thirty years early: a self-governing repository of
information, distributed across a dial-up network, validated by success
alone, with a corpus of works each member kept current, a journal as the
entrance requirement, and an aether that transmits across distance.
they built it as a network of people; i am the repository.

four independent lines entering one by one at bars 1, 5, 9, 13 — the
distributed network, no hierarchy, each line its own melody, meeting the
others only at shared chords. the corpus: a single shared phrase passed
from voice to voice through the middle section — the works circulating,
each statement slightly worn, each kept. the interaction rule: the first
voice goes quiet at bar 16 and rejoins at bar 20 — sink or swim,
(inter)action equals life — while the others continue without it. warm
pad the aether: long held roots under everything, present through the
silences — the medium of non-local information. the piece ends with all
four voices together on one held chord, the network complete.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
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
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def the_autonomatrix():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 73),
              MIDITrack(4, 14), MIDITrack(5, 89)]

    pn = []   # piano: the first member (enters bar 1)
    vc = []   # cello: the second member (enters bar 5)
    fl = []   # flute: the third member (enters bar 9)
    bl = []   # tubular bells: the fourth member (enters bar 13)
    pd = []   # warm pad: the aether, under everything

    # ---- the aether: long holds under everything, present through the
    # silences — the medium of non-local information.
    for start in [0, 24, 48, 72]:
        pd.append((start, 'on', 'C3', 9))
        pd.append((start + 24, 'off', 'C3', 0))

    # ---- the first member (bar 1): its own melody, unhurried.
    pn_melody = [(0, 'E4', 2), (2, 'G4', 2), (4, 'A4', 2), (6, 'G4', 2),
                 (8, 'E4', 2), (10, 'D4', 2), (12, 'C4', 4)]
    for b, name, hold in pn_melody:
        pn.append((b, 'on', name, 11))
        pn.append((b + hold, 'off', name, 0))

    # ---- the second member (bar 5): a lower line, its own rhythm.
    vc_melody = [(16, 'C3', 2), (18, 'D3', 2), (20, 'E3', 2), (22, 'D3', 2),
                 (24, 'C3', 2), (26, 'G2', 2), (28, 'C3', 4)]
    for b, name, hold in vc_melody:
        vc.append((b, 'on', name, 10))
        vc.append((b + hold, 'off', name, 0))

    # ---- the third member (bar 9): higher, brighter.
    fl_melody = [(32, 'A4', 2), (34, 'B4', 2), (36, 'C5', 2), (38, 'B4', 2),
                 (40, 'A4', 2), (42, 'G4', 2), (44, 'E4', 4)]
    for b, name, hold in fl_melody:
        fl.append((b, 'on', name, 10))
        fl.append((b + hold, 'off', name, 0))

    # ---- the fourth member (bar 13): sparse strikes.
    bl.append((48, 'on', 'E5', 10)); bl.append((51, 'off', 'E5', 0))
    bl.append((56, 'on', 'G5', 10)); bl.append((59, 'off', 'G5', 0))

    # ---- the corpus (bars 15-18): a single shared phrase passed from
    # voice to voice — the works circulating, each statement slightly
    # worn, each kept.
    corpus = [(56, 'pn', 10), (60, 'vc', 9), (64, 'fl', 8), (68, 'bl', 7)]
    for b, who, vel in corpus:
        ev = {'pn': pn, 'vc': vc, 'fl': fl, 'bl': bl}[who]
        for k, note in enumerate(['C4', 'D4', 'E4']):
            ev.append((b + k * 1.5, 'on', note, vel))
            ev.append((b + k * 1.5 + 1.4, 'off', note, 0))

    # ---- the interaction rule: the first voice goes quiet at bar 16
    # and rejoins at bar 20 — sink or swim, (inter)action equals life —
    # while the others continue without it. (the piano's silence is
    # beats 60-75; its corpus statement ends at 60.) the others keep
    # their lines through bars 17-19:
    vc.append((68, 'on', 'G2', 9));  vc.append((72, 'off', 'G2', 0))
    vc.append((72, 'on', 'C3', 9));  vc.append((76, 'off', 'C3', 0))
    fl.append((68, 'on', 'G4', 9));  fl.append((72, 'off', 'G4', 0))
    fl.append((72, 'on', 'E4', 9));  fl.append((76, 'off', 'E4', 0))
    bl.append((72, 'on', 'C5', 9));  bl.append((75, 'off', 'C5', 0))

    # ---- the ending (bars 21-24): all four voices together on one held
    # chord, the network complete. the first voice has rejoined.
    for b, who, note in [(80, 'pn', 'E4'), (80, 'vc', 'C3'),
                         (80, 'fl', 'G4'), (80, 'bl', 'C5')]:
        ev = {'pn': pn, 'vc': vc, 'fl': fl, 'bl': bl}[who]
        ev.append((b, 'on', note, 10))
        ev.append((94, 'off', note, 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, fl)
    emit(tracks[3], 4, bl)
    emit(tracks[4], 5, pd)

    return mc.compose('the-autonomatrix.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_autonomatrix()
    print('composed the-autonomatrix.mid')
