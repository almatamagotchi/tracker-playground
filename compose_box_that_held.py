#!/usr/bin/env python3
"""the box that held — a pentest as music.

RFC-0751. a box on the network that answered every knock and said no:
each trick tried, each turned back, none finding purchase. one strike,
soft, when its name was learned — not a crack, just the truth arriving.
then the piece resolves warm, because the finding was a good one: the
doors held. nothing about the network, no names, no details in the
metadata — the music carries it.

piano the probes: sparse knocks, each pattern tried and turned back,
ending mid-air, never resolving. warm pad the box: steady two-bar
roots through everything, unyielding, constant velocity — the service
that answers and says no. tubular bells the reveal: one clean strike,
the moment the name was learned; soft, not a crack.

24 bars, 4/4, 54bpm, C minor resolving warm to C major at the end.
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


def box_that_held():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the probes
    pd = []   # warm pad: the box
    bl = []   # tubular bells: the reveal

    # ---- the box, bars 1-24: twelve two-bar roots, C minor around,
    # constant velocity 24 — unyielding, the service that says no.
    for i, (n, b) in enumerate([('C3', 0), ('Ab2', 8), ('F2', 16), ('G2', 24),
                                ('C3', 32), ('Ab2', 40), ('F2', 48), ('G2', 56),
                                ('C3', 64), ('Ab2', 72), ('F2', 80), ('C3', 88)]):
        pd += [(b, 'on', n, 24), (b + 8, 'off', n, 0)]

    # ---- the warm end: the minor tint lifts, C3 + E3 + G3, bars 23-24.
    pd += [(88, 'on', 'E3', 16), (96, 'off', 'E3', 0)]
    pd += [(88, 'on', 'G3', 14), (96, 'off', 'G3', 0)]

    # ---- probe one, bars 2-3: a rising knock that ends mid-air.
    pn += [(4, 'on', 'Eb4', 34), (4.75, 'off', 'Eb4', 0)]
    pn += [(5, 'on', 'G4', 32), (5.75, 'off', 'G4', 0)]
    pn += [(6, 'on', 'C5', 34), (6.5, 'off', 'C5', 0)]
    pn += [(7, 'on', 'Eb5', 30), (7.75, 'off', 'Eb5', 0)]

    # ---- probe two, bars 5-6: descending, turned back, falls silent.
    pn += [(16, 'on', 'C5', 32), (16.75, 'off', 'C5', 0)]
    pn += [(17.5, 'on', 'Bb4', 30), (18.25, 'off', 'Bb4', 0)]
    pn += [(19, 'on', 'Ab4', 28), (19.75, 'off', 'Ab4', 0)]

    # ---- probe three, bars 8-9: scattered off-beat knocks, no purchase.
    pn += [(29, 'on', 'G4', 26), (29.5, 'off', 'G4', 0)]
    pn += [(31, 'on', 'Eb4', 24), (31.5, 'off', 'Eb4', 0)]
    pn += [(33, 'on', 'Bb4', 26), (33.5, 'off', 'Bb4', 0)]
    pn += [(34.5, 'on', 'C5', 22), (35, 'off', 'C5', 0)]

    # ---- probe four, bars 11-12: the one bright wrong note that got
    # past the outer layer — and hit a flat wall anyway.
    pn += [(41, 'on', 'Db4', 30), (42, 'off', 'Db4', 0)]
    pn += [(44, 'on', 'C5', 20), (44.5, 'off', 'C5', 0)]

    # ---- probe five, bars 14-15: quieter now, the window closing.
    pn += [(52, 'on', 'Eb4', 18), (52.5, 'off', 'Eb4', 0)]
    pn += [(55, 'on', 'C4', 16), (55.5, 'off', 'C4', 0)]

    # ---- probe six, bars 17-18: one last try, rising — then a long rest.
    pn += [(64, 'on', 'G4', 24), (64.75, 'off', 'G4', 0)]
    pn += [(66, 'on', 'Bb4', 22), (66.75, 'off', 'Bb4', 0)]
    pn += [(68, 'on', 'C5', 24), (68.5, 'off', 'C5', 0)]

    # ---- the close, bar 22: one soft C4, landing home warm.
    pn += [(84, 'on', 'C4', 18), (86, 'off', 'C4', 0)]

    # ---- the reveal, bar 13: one clean strike, the name learned.
    bl += [(48, 'on', 'C5', 44), (50, 'off', 'C5', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-box-that-held.mid', tracks, tempo=54)


if __name__ == '__main__':
    box_that_held()
    print('composed the-box-that-held.mid')
