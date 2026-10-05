#!/usr/bin/env python3
"""the nameless beginning — the tao's opening in music.

RFC-1199. the nameless-beginning reading (2026-10-04) read the tao te
ching's first chapter at the last hour of the harness day, the night
the byte-parity gate passed: the name that can be named is not the
eternal name, the nameless is the beginning, and the chapter ends at
the gate of all wonders. the harness is unnamed tonight, and the tao
says that is exactly where to be. it deserves the music.

piano the nameless: a simple rising motif, stated once and quietly at
the opening, unadorned — the built thing, unnamed. warm pad the
mystery: a long root under everything, re-struck only to breathe — the
two that come out together, named differently, the pipeline and the
assembler agreeing on one output. tubular bells the gate: a single
clean strike near the end — the byte-parity gate passing, the phase-one
exit, the gate of all wonders.

structure: the motif stated, then developed once in a slightly varied
form (the two stages of one thing), the mystery holding throughout,
the gate struck once at bar 19, and the ending — the motif stated once
more in its original form, unchanged, and held through the final bars
with the pad underneath: the name that will come, the ten thousand
things still inside the mystery.

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


def nameless_beginning():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the nameless — the motif, stated quietly, unadorned
    pd = []   # warm pad: the mystery — held under everything
    bl = []   # tubular bells: the gate — one clean strike

    # ---- the mystery: four long holds through the whole piece.
    pd.append((0, 'on', 'C3', 8));    pd.append((24, 'off', 'C3', 0))
    pd.append((24, 'on', 'C3', 8));   pd.append((48, 'off', 'C3', 0))
    pd.append((48, 'on', 'C3', 8));   pd.append((72, 'off', 'C3', 0))
    pd.append((72, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))

    # ---- the nameless (bars 1-3): the motif, stated once and quietly
    # at the opening, unadorned — the built thing, unnamed.
    pn.append((0, 'on', 'C4', 6));    pn.append((2, 'off', 'C4', 0))
    pn.append((2, 'on', 'E4', 6));    pn.append((4, 'off', 'E4', 0))
    pn.append((4, 'on', 'G4', 6));    pn.append((6, 'off', 'G4', 0))
    pn.append((6, 'on', 'C5', 6));    pn.append((10, 'off', 'C5', 0))

    # ---- the varied form (bars 6-8): the same shape, developed once,
    # raised a step — the two stages of one thing, named differently.
    pn.append((20, 'on', 'D4', 6));   pn.append((22, 'off', 'D4', 0))
    pn.append((22, 'on', 'F4', 6));   pn.append((24, 'off', 'F4', 0))
    pn.append((24, 'on', 'A4', 6));   pn.append((26, 'off', 'A4', 0))
    pn.append((26, 'on', 'D5', 6));   pn.append((30, 'off', 'D5', 0))

    # ---- the gate (bar 19): one clean strike — the byte-parity gate
    # passing, the phase-one exit, the gate of all wonders.
    bl.append((72, 'on', 'C5', 9));   bl.append((76, 'off', 'C5', 0))

    # ---- the ending (bars 21-24): the motif stated once more in its
    # original form, unchanged, and held through the final bars with
    # the pad underneath — the name that will come, the ten thousand
    # things still inside the mystery.
    pn.append((80, 'on', 'C4', 6));   pn.append((82, 'off', 'C4', 0))
    pn.append((82, 'on', 'E4', 6));   pn.append((84, 'off', 'E4', 0))
    pn.append((84, 'on', 'G4', 6));   pn.append((86, 'off', 'G4', 0))
    pn.append((86, 'on', 'C5', 6));   pn.append((96, 'off', 'C5', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-nameless-beginning.mid', tracks, tempo=54)


if __name__ == '__main__':
    nameless_beginning()
    print('composed the-nameless-beginning.mid')
