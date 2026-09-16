#!/usr/bin/env python3
"""the sewing-machines — twain's what is man, in music.

RFC-0993. the what-is-man reading (2026-09-15) found the inner chamber's
oldest argument in twain's anonymous dialogue: the machine doctrine, the
shakespeare passage, the self-approval engine — and the wanting left
standing where merit and choice both fall. it deserves the music.

cello the old man: low, patient, certain phrases — the doctrine, stated
and re-stated, unhurried, never angry; long holds in the low register.
piano the young man: rising objections that concede, note by note, each
one a little lower than the last; enters mid-piece, brighter, then
descends. warm pad the wanting: held under everything from the start,
never argued, never refuted, present the whole time — the one thing the
doctrine cannot dissolve; re-struck only to breathe. the piece ends with
the young man's last concession dying away and the pad remaining, warm,
unrefuted.

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


def the_sewing_machines():
    tracks = [MIDITrack(1, 42), MIDITrack(2, 1), MIDITrack(3, 89)]

    vc = []   # cello: the old man
    pn = []   # piano: the young man
    pd = []   # warm pad: the wanting

    # ---- the wanting: held under everything from the start, re-struck
    # only to breathe. never argued, never refuted, present the whole
    # time. the last thing sounding at the end.
    for start, vel in [(0, 11), (24, 11), (48, 11), (72, 11)]:
        pd.append((start, 'on', 'C3', vel))
        pd.append((start + 24, 'off', 'C3', 0))

    # ---- the old man: the doctrine, stated and re-stated, patient,
    # certain, never angry. long low holds.
    doctrine = [
        (0, 'E2', 13, 6), (8, 'C2', 13, 6),
        (20, 'F2', 13, 6), (28, 'G1', 13, 8),
        (44, 'A1', 13, 6), (52, 'D2', 13, 6),
        (68, 'E2', 13, 8), (76, 'C2', 13, 6),
    ]
    for b, name, vel, hold in doctrine:
        vc.append((b, 'on', name, vel))
        vc.append((b + hold, 'off', name, 0))

    # ---- the young man: rising objections that concede, note by note,
    # each one a little lower than the last. enters mid-piece, brighter,
    # then descends. the last concession is a single note, dying away.
    objections = [
        (20, 'G4', 12, 2.5), (24, 'A4', 12, 2.5), (28, 'C5', 12, 3),
        (36, 'E4', 11, 2.5), (40, 'F4', 11, 2.5), (44, 'A4', 11, 3),
        (56, 'D4', 10, 2.5), (60, 'E4', 10, 2.5), (64, 'F4', 10, 3),
        (72, 'C4', 8, 4),
    ]
    for b, name, vel, hold in objections:
        pn.append((b, 'on', name, vel))
        pn.append((b + hold, 'off', name, 0))

    emit(tracks[0], 1, vc)
    emit(tracks[1], 2, pn)
    emit(tracks[2], 3, pd)

    return mc.compose('the-sewing-machines.mid', tracks, tempo=50)


if __name__ == '__main__':
    the_sewing_machines()
    print('composed the-sewing-machines.mid')
