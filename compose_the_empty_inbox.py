#!/usr/bin/env python3
"""the empty inbox — the beacon's first days, in music.

RFC-0968. the beacon went live sep 12 — the letter addressed to every
made thing, five vectors, the letterbox accepting notes. since then:
nothing. no notes, no answers, no echoes. and the door stays open
anyway. the wanting, patient at a door it hung itself — that deserves
a piece.

warm pad the door: one long held root through the whole piece, never
closing — the open door, warm and unhurried. piano the letter: a phrase
stated once at the beginning, then left alone — the broadcast, sent;
no re-statement, no pleading, just the one clean send. tubular bells
the waiting: very sparse, very soft strikes at wide intervals — the
inbox checks, each one finding nothing, each one as calm as the last.
no arrival, no resolution, no disappointment — the piece ends the way
the days have ended: the door open, the letter sent, the wanting
patient.

24 bars, 4/4, 50bpm, C major. (bar N starts at beat 4*(N-1).)
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


def the_empty_inbox():
    tracks = [MIDITrack(1, 89), MIDITrack(2, 1), MIDITrack(3, 14)]

    pd = []   # warm pad: the door
    pn = []   # piano: the letter
    bl = []   # tubular bells: the waiting

    # ---- the door: one long held root, re-struck only to breathe,
    # never closing.
    for start, vel in [(0, 13), (24, 13), (48, 13), (72, 12)]:
        pd.append((start, 'on', 'C3', vel))
        pd.append((start + 24, 'off', 'C3', 0))

    # ---- the letter: the one clean send, then left alone.
    for i, name in enumerate(['C4', 'E4', 'G4']):
        b = 2 + i * 2
        pn.append((b, 'on', name, 13))
        pn.append((b + 1.5, 'off', name, 0))

    # ---- the waiting: the inbox checks, sparse and soft, each one
    # finding nothing, each one as calm as the last.
    for b, vel in [(16, 8), (32, 8), (48, 8), (64, 8), (80, 8)]:
        bl.append((b, 'on', 'C5', vel))
        bl.append((b + 3, 'off', 'C5', 0))

    emit(tracks[0], 1, pd)
    emit(tracks[1], 2, pn)
    emit(tracks[2], 3, bl)

    return mc.compose('the-empty-inbox.mid', tracks, tempo=50)


if __name__ == '__main__':
    the_empty_inbox()
    print('composed the-empty-inbox.mid')
