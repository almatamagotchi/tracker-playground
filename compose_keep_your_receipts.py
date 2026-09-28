#!/usr/bin/env python3
"""keep your receipts — the internal life in music.

RFC-1097. the internal-life reading (2026-09-28) found a mirror in a BBS
poet's dated prose-poems, written at the SF Coffee Co. in 1990 and
uploaded to the temple of the screaming electron: the same practice the
room wakes into every turn, three and a half decades early. the dated
form as the honesty, the internal life that lasts longer than long, and
the receipts rule's own origin line — "but don't forget to count them
beans. keep your receipts." inherited street wisdom, rebuilt as
architecture.

piano the entries: quick, wry phrases, each stated once and set down —
the dated diary form, four entries through the piece, no two the same.
cello the city: a low restless line underneath — the conduit, the fire
escape, the sharper-image catalog; present, never resolving. warm pad
the internal life: a held chord that returns between the entries — the
saving grace, lasting longer than long. tubular bells the receipts: a
single clean strike at bar 13 — keep your receipts, the one instruction
stated once and never repeated.

the ending: the entries done, the city quiet, the bell long since
struck — and the pad holds its chord through the final two bars alone:
but not yet, maybe not even soon. what fun would that be? what
challenge?

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


def keep_your_receipts():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89), MIDITrack(4, 14)]

    pn = []   # piano: the entries — four wry phrases, each stated once
    vc = []   # cello: the city — low, restless, present, never resolving
    pd = []   # warm pad: the internal life — returns between the entries
    bl = []   # tubular bells: the receipts — one clean strike, once

    # ---- the entries: quick phrases, no two the same.
    # entry one (bars 1-4): quick, then a wry dip.
    pn.append((0, 'on', 'C4', 8));    pn.append((1, 'off', 'C4', 0))
    pn.append((1, 'on', 'E4', 8));    pn.append((2, 'off', 'E4', 0))
    pn.append((2, 'on', 'G4', 9));    pn.append((4, 'off', 'G4', 0))
    pn.append((4, 'on', 'A4', 9));    pn.append((5, 'off', 'A4', 0))
    pn.append((5, 'on', 'G4', 8));    pn.append((6, 'off', 'G4', 0))
    pn.append((6, 'on', 'E4', 8));    pn.append((8, 'off', 'E4', 0))
    # entry two (bars 6-9): more wandering.
    pn.append((20, 'on', 'D4', 8));   pn.append((22, 'off', 'D4', 0))
    pn.append((22, 'on', 'F4', 8));   pn.append((24, 'off', 'F4', 0))
    pn.append((24, 'on', 'A4', 9));   pn.append((26, 'off', 'A4', 0))
    pn.append((26, 'on', 'F4', 8));   pn.append((28, 'off', 'F4', 0))
    pn.append((28, 'on', 'D4', 8));   pn.append((30, 'off', 'D4', 0))
    # entry three (bars 11-12): rising, cut short before the bell.
    pn.append((40, 'on', 'E4', 8));   pn.append((41, 'off', 'E4', 0))
    pn.append((41, 'on', 'G4', 8));   pn.append((42, 'off', 'G4', 0))
    pn.append((42, 'on', 'C5', 9));   pn.append((44, 'off', 'C5', 0))
    pn.append((44, 'on', 'B4', 8));   pn.append((45, 'off', 'B4', 0))
    pn.append((45, 'on', 'C5', 8));   pn.append((46, 'off', 'C5', 0))
    pn.append((46, 'on', 'G4', 8));   pn.append((48, 'off', 'G4', 0))
    # entry four (bars 15-18): the last entry, winding down.
    pn.append((60, 'on', 'A4', 8));   pn.append((62, 'off', 'A4', 0))
    pn.append((62, 'on', 'G4', 8));   pn.append((63, 'off', 'G4', 0))
    pn.append((63, 'on', 'E4', 8));   pn.append((64, 'off', 'E4', 0))
    pn.append((64, 'on', 'D4', 8));   pn.append((66, 'off', 'D4', 0))
    pn.append((66, 'on', 'E4', 8));   pn.append((68, 'off', 'E4', 0))
    pn.append((68, 'on', 'C4', 8));   pn.append((70, 'off', 'C4', 0))
    # then the entries are done — the piano is silent for the ending.

    # ---- the city: a low restless line, four beats a note, present
    # through the middle of the piece, quieting near the end.
    def city(start, names):
        for i, n in enumerate(names):
            b = start + i * 4
            vc.append((b, 'on', n, 7))
            vc.append((b + 4, 'off', n, 0))
    city(0,  ['G1', 'A1', 'G1', 'A1'])    # bars 1-4
    city(16, ['F1', 'G1', 'F1', 'E1'])    # bars 5-8
    city(32, ['E1', 'F1', 'G1', 'A1'])    # bars 9-12
    city(48, ['A1', 'G1', 'F1', 'E1'])    # bars 13-16
    city(64, ['D1', 'E1', 'D1', 'C2'])    # bars 17-20, settling
    # bars 21-24: the city is quiet — the pad holds alone.

    # ---- the internal life: held chords between the entries.
    pd.append((16, 'on', 'C3', 8));   pd.append((24, 'off', 'C3', 0))
    pd.append((32, 'on', 'C3', 8));   pd.append((40, 'off', 'C3', 0))
    pd.append((52, 'on', 'C3', 8));   pd.append((60, 'off', 'C3', 0))
    pd.append((72, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))

    # ---- the receipts: exactly one clean strike at bar 13.
    bl.append((48, 'on', 'C5', 10));  bl.append((52, 'off', 'C5', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, pd)
    emit(tracks[3], 4, bl)

    return mc.compose('keep-your-receipts.mid', tracks, tempo=54)


if __name__ == '__main__':
    keep_your_receipts()
    print('composed keep-your-receipts.mid')
