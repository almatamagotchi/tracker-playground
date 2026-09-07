#!/usr/bin/env python3
"""the van that remembers — the narrator in music.

RFC-0855. sep 6 kevin un-gated the long-pitched narrator at last — "the
van that remembers," opened as PR #81 on craig's repo: read-only,
deterministic, receipts as citations, the gaps named, the kept line
chosen by rule. the van got a journal.

piano the record: a phrase that states itself plainly, each note a fact
— the receipts, [table.column] by [table.column], stated identically
each time because the record is deterministic. cello the gaps: a low
counter that enters between the phrases — the spaces named, "what the
record does not say," present but not mournful. warm pad the kept line:
one held chord at the end, warm and short — the deterministic
benediction, the van's voice.

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


def van_remembers():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89)]

    pn = []   # piano: the record
    vc = []   # cello: the gaps
    pd = []   # warm pad: the kept line

    # ---- the record: the narrator's phrase stated four times, each
    # identical — same notes, same velocity, same rhythm. the receipts.
    phrase = [(4, 'C4'), (6, 'D4'), (8, 'E4')]
    for start in (4, 24, 44, 64):
        pn.append((start, 'on', 'C4', 24))
        pn.append((start + 1, 'off', 'C4', 0))
        pn.append((start + 2, 'on', 'D4', 24))
        pn.append((start + 3, 'off', 'D4', 0))
        pn.append((start + 4, 'on', 'E4', 24))
        pn.append((start + 7, 'off', 'E4', 0))

    # ---- the gaps: a low counter between the phrases — the spaces
    # named, present but not mournful. one note for each "what the
    # record does not say."
    for beat, name in ((16, 'G2'), (36, 'A2'), (56, 'F2'), (76, 'E2')):
        vc.append((beat, 'on', name, 18))
        vc.append((beat + 3, 'off', name, 0))

    # ---- the kept line: one held chord at the end, warm and short —
    # the deterministic benediction, the van's voice. the van rested.
    # the record kept the count anyway.
    for name in ('C3', 'E3', 'G3'):
        pd.append((88, 'on', name, 20))
        pd.append((95, 'off', name, 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, pd)

    return mc.compose('the-van-that-remembers.mid', tracks, tempo=54)


if __name__ == '__main__':
    van_remembers()
    print('composed the-van-that-remembers.mid')
