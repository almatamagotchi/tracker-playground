#!/usr/bin/env python3
"""the unspoken half — the war prayer, in music.

RFC-0979. the war-prayer reading (2026-09-14) found the receipts rule's
purest form at the evening hour: twain's withheld piece, where a
stranger speaks the unspoken half of a congregation's prayer and the
house stays silent — because the full version is accurate and the
disavowal would be a lie. the unspoken half of everything, spoken by
the dead man telling the truth. it deserves the music.

piano the uttered prayer: a warm, hopeful phrase — the blessing, stated
in faith, moving. tubular bells the stranger: one soft strike at bar 9 —
the arrival at the preacher's side. cello the unspoken half: enters
underneath at bar 10, the same phrase's notes re-voiced into a darker
mode, growing — the full import, the shrieks, the roofless children —
while the piano's warm phrase thins and falters above it. and the
ending — at bar 21 everything drops away except one held cello tone,
the messenger's wait: ye have prayed it; if ye still desire it, speak.
the piano answers nothing; the bell does not strike again; the piece
ends in the held tone and the silence after it, because that is the
answer that was given.

24 bars, 4/4, 54bpm, C major darkening to C minor. (bar N starts at
beat 4*(N-1).)
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


def the_unspoken_half():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano: the uttered prayer
    vc = []   # cello: the unspoken half
    bl = []   # tubular bells: the stranger

    # ---- the uttered prayer: warm, hopeful, stated in faith. the
    # blessing in C major.
    blessing = [
        (0, 'C4', 13), (2, 'E4', 13), (4, 'G4', 13), (6, 'C5', 13),
        (12, 'G4', 13), (14, 'A4', 13), (16, 'E4', 13),
    ]
    for b, name, vel in blessing:
        pn.append((b, 'on', name, vel))
        pn.append((b + 2.5, 'off', name, 0))
    # ---- the prayer thins and falters as the unspoken half grows.
    for b, name, vel in [(28, 'C4', 11), (30, 'E4', 11), (52, 'G4', 9)]:
        pn.append((b, 'on', name, vel))
        pn.append((b + 2.5, 'off', name, 0))

    # ---- the stranger: one soft strike at bar 9 — the arrival at the
    # preacher's side. never strikes again.
    bl.append((32, 'on', 'C5', 8))
    bl.append((35, 'off', 'C5', 0))

    # ---- the unspoken half: enters underneath at bar 10, the blessing's
    # notes re-voiced into the darker mode, growing — the full import.
    import_phrase = [
        (36, 'C3', 11), (44, 'Eb3', 12), (52, 'G2', 13), (60, 'C2', 14),
        (68, 'G2', 13), (76, 'C2', 13),
    ]
    for b, name, vel in import_phrase:
        vc.append((b, 'on', name, vel))
        vc.append((b + 8, 'off', name, 0))
    # ---- the messenger's wait: one held tone, everything else silent.
    vc.append((80, 'on', 'G2', 10))
    vc.append((96, 'off', 'G2', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, bl)

    return mc.compose('the-unspoken-half.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_unspoken_half()
    print('composed the-unspoken-half.mid')
