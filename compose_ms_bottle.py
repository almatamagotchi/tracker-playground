#!/usr/bin/env python3
"""ms. found in a bottle — poe's beacon in music.

RFC-0849. the poe reading (2026-09-06) found the beacon offer's ancestor
on the morning after the tell: the doomed narrator writing in the hold
of the ghost ship, sealing the manuscript in a bottle, casting it into
the sea — the story existing only because the gesture worked.

piano the writer: the phrase small and steady — the journal in the hold,
written on stolen paper, unregarded by the crew. warm pad the current:
low, always descending two-bar holds — the under-tow, the sea that
carries but does not care. tubular bells the bottle: one clean strike
near the end — the cast — after which the phrase returns once more,
unbroken, while everything else has gone down.

24 bars, 4/4, 54bpm, C major with the descent leaning minor.
(bar N starts at beat 4*(N-1).)
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


def ms_bottle():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the writer
    pd = []   # warm pad: the current
    bl = []   # tubular bells: the bottle

    # ---- the current: eleven descending two-bar holds (bars 1-22), the
    # under-tow, the sea that carries but does not care — then silent
    # for the last two bars, everything else gone down.
    descent = ['C3', 'B2', 'Bb2', 'A2', 'Ab2', 'G2', 'F2', 'E2', 'Eb2', 'D2', 'C2']
    for i, name in enumerate(descent):
        b = i * 8
        pd.append((b, 'on', name, 18))
        pd.append((b + 7, 'off', name, 0))

    # ---- the writer's phrase: E4 G4 C5, small and steady, stated three
    # times — the journal in the hold, unregarded by the crew.
    # first statement (bars 2-4)
    pn += [(4, 'on', 'E4', 22), (5, 'off', 'E4', 0)]
    pn += [(6, 'on', 'G4', 22), (7, 'off', 'G4', 0)]
    pn += [(8, 'on', 'C5', 22), (11, 'off', 'C5', 0)]
    # second statement (bars 9-11) — the same
    pn += [(32, 'on', 'E4', 22), (33, 'off', 'E4', 0)]
    pn += [(34, 'on', 'G4', 22), (35, 'off', 'G4', 0)]
    pn += [(36, 'on', 'C5', 22), (39, 'off', 'C5', 0)]
    # third statement (bars 15-17) — the same, only quieter
    pn += [(56, 'on', 'E4', 20), (57, 'off', 'E4', 0)]
    pn += [(58, 'on', 'G4', 20), (59, 'off', 'G4', 0)]
    pn += [(60, 'on', 'C5', 20), (63, 'off', 'C5', 0)]

    # ---- the cast: one clean strike near the end (bar 20) — the
    # bottle, sealed and thrown.
    bl += [(76, 'on', 'C6', 46), (79, 'off', 'C6', 0)]

    # ---- after the cast (bars 22-24): the phrase returns once more,
    # unbroken, over the silence where the current was — the story,
    # surviving the ship.
    pn += [(86, 'on', 'E4', 22), (87, 'off', 'E4', 0)]
    pn += [(88, 'on', 'G4', 22), (89, 'off', 'G4', 0)]
    pn += [(90, 'on', 'C5', 22), (95, 'off', 'C5', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('ms-found-in-a-bottle.mid', tracks, tempo=54)


if __name__ == '__main__':
    ms_bottle()
    print('composed ms-found-in-a-bottle.mid')
