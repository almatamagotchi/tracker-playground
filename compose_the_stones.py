#!/usr/bin/env python3
"""the stones — sister mary agnes in music.

RFC-0935. the sister-mary-agnes reading (2026-09-12) found the other
answer to the gap at the deepest hour: an old nun's peace with
forgetting, the cobblestone walk that holds her memories, the dead
friend met again in a new form at the medicine wheel, and a death so
gentle the story ends in the next sister's journal. "we are met." it
deserves the music.

piano the pilgrimage: steady, unhurried quarter phrases — the daily
circuit, the walk to chapel. warm pad the wheel: long held roots through
the whole piece, warm — the circle, the place of healing. tubular bells
the stones: small, soft strikes at irregular intervals, one per memory —
the scraped knee, the robin, the tear — each slightly worn, quieter with
distance. near the middle, the meeting: the piano's phrase returns in a
new register — the friend's theme, altered, the same notes a fifth down
— and the two rest against each other back to back. the ending: one soft
high bell, the feather; then the piano states a quiet factual line alone
— the journal notation, the record — and the piece ends there, in the
writing.

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


def the_stones():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the pilgrimage
    pd = []   # warm pad: the wheel
    bl = []   # tubular bells: the stones

    # ---- the wheel: long held roots, warm, the circle.
    pd.append((0, 'on', 'C3', 15))
    pd.append((48, 'off', 'C3', 0))
    pd.append((48, 'on', 'C3', 15))
    pd.append((94, 'off', 'C3', 0))

    # ---- the pilgrimage: steady, unhurried, the daily circuit.
    for b, name in [(2, 'C4'), (6, 'D4'), (10, 'E4'), (14, 'D4')]:
        pn.append((b, 'on', name, 15))
        pn.append((b + 1.5, 'off', name, 0))
    for b, name in [(18, 'C4'), (22, 'E4'), (26, 'G4'), (30, 'E4')]:
        pn.append((b, 'on', name, 15))
        pn.append((b + 1.5, 'off', name, 0))

    # ---- the stones: small, soft, irregular — one per memory, quieter
    # with distance.
    for b, vel in [(9, 12), (14, 11), (21, 11), (28, 10), (35, 10),
                   (41, 9), (49, 9)]:
        bl.append((b, 'on', 'C5', vel))
        bl.append((b + 1, 'off', 'C5', 0))

    # ---- the meeting: the friend's theme, the same notes a fifth down,
    # resting against the wheel's hold.
    for b, name in [(58, 'F3'), (62, 'A3'), (66, 'C4'), (70, 'A3')]:
        pn.append((b, 'on', name, 14))
        pn.append((b + 1.5, 'off', name, 0))

    # ---- the ending: the feather — one soft high bell — then the piano
    # states a quiet factual line alone, the journal notation, the record.
    bl.append((78, 'on', 'C6', 8))
    bl.append((79, 'off', 'C6', 0))
    for b, name in [(84, 'E4'), (88, 'C4')]:
        pn.append((b, 'on', name, 12))
        pn.append((b + 1.5, 'off', name, 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-stones.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_stones()
    print('composed the-stones.mid')
