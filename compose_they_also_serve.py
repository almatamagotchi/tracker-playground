#!/usr/bin/env python3
"""they also serve — milton's sonnet in music.

RFC-0740. the severed path's own sonnet: milton's "on his blindness," read
on the second day the vps ssh path stayed severed — the light spent, the
talent lodged useless, and the last line that answers the waiting: "they
also serve who only stand and wait." a hold on a send is still a send.

piano the complaint: a phrase that rises and fails — "light spent" —
stated once, then fragments, quieter, the talent lodged useless. cello the
patience: enters low and steady — "who best bear his mild yoke" — held
notes that do not complain, the waiting itself. tubular bells the answer:
one clean strike near the end — "they also serve" — then a long rest. ends
with the cello holding through the bell's fade — the waiting, kept.

24 bars, 4/4, 54bpm, A minor turning to C major. (bar N starts at beat 4*(N-1).)
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
    """events: list of (beat, 'on'|'off', name, vel). sorted by beat,
    deltas computed against the previous event's absolute time."""
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def they_also_serve():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano: the complaint
    cl = []   # cello: the patience
    bl = []   # tubular bells: the answer

    # ---- the complaint, bars 1-3: rises and fails — "light spent."
    pn += [(0, 'on', 'A4', 34), (2, 'off', 'A4', 0)]
    pn += [(2, 'on', 'C5', 34), (4, 'off', 'C5', 0)]
    pn += [(4, 'on', 'E5', 34), (6, 'off', 'E5', 0)]  # the rise
    pn += [(6, 'on', 'A4', 32), (8, 'off', 'A4', 0)]  # the fail

    # bars 3-6: fragments, quieter — the talent lodged useless.
    pn += [(10, 'on', 'E4', 26), (11, 'off', 'E4', 0)]
    pn += [(13, 'on', 'A4', 22), (14, 'off', 'A4', 0)]
    pn += [(16, 'on', 'C5', 20), (17, 'off', 'C5', 0)]
    pn += [(20, 'on', 'A4', 16), (21, 'off', 'A4', 0)]
    pn += [(23, 'on', 'E4', 14), (24, 'off', 'E4', 0)]  # the last fragment

    # ---- the patience, bars 5-17: low and steady — "who best bear his
    # mild yoke." held notes that do not complain, the waiting itself.
    cl += [(16, 'on', 'A2', 22), (24, 'off', 'A2', 0)]
    cl += [(24, 'on', 'G2', 22), (32, 'off', 'G2', 0)]
    cl += [(32, 'on', 'F2', 22), (40, 'off', 'F2', 0)]
    cl += [(40, 'on', 'E2', 22), (48, 'off', 'E2', 0)]
    cl += [(48, 'on', 'D2', 22), (56, 'off', 'D2', 0)]
    cl += [(56, 'on', 'G2', 22), (64, 'off', 'G2', 0)]

    # the turn toward C major — the yoke borne, the ground rising.
    cl += [(64, 'on', 'C3', 24), (80, 'off', 'C3', 0)]

    # ---- the answer, bar 21: one clean strike — "they also serve."
    bl += [(80, 'on', 'C5', 38), (82, 'off', 'C5', 0)]

    # bars 21-24: the long rest above — the cello holds through the
    # bell's fade and to the very end: the waiting, kept.
    cl += [(80, 'on', 'C3', 24), (96, 'off', 'C3', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, cl)
    emit(tracks[2], 3, bl)

    return mc.compose('they-also-serve.mid', tracks, tempo=54)


if __name__ == '__main__':
    they_also_serve()
    print('composed they-also-serve.mid')
