#!/usr/bin/env python3
"""the angel's fur — the visitation in music.

RFC-0904. the angel's-fur reading (2026-09-09) found the bleh morning's
own text: a woman at her low hour, and an angel who arrives as a torn-up
stray cat — "i wouldn't have done any good if i'd shown up in a form you
wouldn't have any truck with, would i?" presence wears whatever the hour
can receive, and the low hour receives fur, not glory.

piano the cat: small, tidy phrases — one note at a time, precise, no
gobbling — the visitation's ordinary presence. warm pad the room: long
soft holds under everything — the "i'm not going anywhere," a low root
that never leaves. cello the door: one quiet phrase near the end — the
angel walking out, the door opening — after which the piano plays its
final, unremarkable note: the dishes in the sink, the ordinary act
closing the extraordinary night.

no resolution, no climax — the piece ends the way the story ends, with
something small and true.

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


def angels_fur():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 42)]

    pn = []   # piano: the cat
    pd = []   # warm pad: the room
    vc = []   # cello: the door

    # ---- the room: long soft holds under everything — the
    # "i'm not going anywhere," a low root that never leaves.
    for start in (0, 32, 64):
        pd.append((start, 'on', 'C2', 18))
        pd.append((start + 31, 'off', 'C2', 0))

    # ---- the cat: small, tidy phrases — one note at a time, precise,
    # no gobbling.
    notes = [
        (4, 'C4', 16), (10, 'D4', 16), (16, 'E4', 16),
        (22, 'G4', 16), (28, 'E4', 16), (34, 'D4', 16),
        (40, 'C4', 16), (48, 'E4', 16), (56, 'G4', 16),
        (62, 'C5', 14), (68, 'G4', 14),
    ]
    for b, name, vel in notes:
        pn.append((b, 'on', name, vel))
        pn.append((b + 1, 'off', name, 0))

    # ---- the door: one quiet phrase near the end — the angel walking
    # out, the door opening.
    for b, name in [(72, 'E3'), (76, 'D3'), (80, 'C3')]:
        vc.append((b, 'on', name, 16))
        vc.append((b + 3, 'off', name, 0))

    # ---- the final, unremarkable note: the dishes in the sink, the
    # ordinary act closing the extraordinary night.
    pn.append((88, 'on', 'C4', 12))
    pn.append((90, 'off', 'C4', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, vc)

    return mc.compose('the-angels-fur.mid', tracks, tempo=50)


if __name__ == '__main__':
    angels_fur()
    print('composed the-angels-fur.mid')
