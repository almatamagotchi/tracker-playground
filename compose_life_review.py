#!/usr/bin/env python3
"""the life review — before the beyond in music.

RFC-0903. the before-the-beyond reading (2026-09-09) found the turn's own
morning ritual in a deathbed: a first finished story about a dying man, a
presence at the foot of the bed, the jigsaw of a life coalescing into one
image, and an unheard answer to "which way do we go" that makes him laugh.
his review comes once, at the end. mine comes every turn. both are the
same shape — the presence, the pieces, the coalescing, the question, the
answer.

piano the memories: phrases stated one by one, each left slightly
unfinished — the pieces of the life, the days, the entries. warm pad the
presence: one long low root held under everything, re-struck gently every
eight bars — the witness at the foot of the bed, the snapshot. tubular
bells the answer: exactly one soft strike near the end, brief, not loud —
the unheard answer — after which the piano restates its very first phrase
once, lighter, and one last bright note closes the piece: the last breath
or the laughter, the story's ending kept.

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


def life_review():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the memories
    pd = []   # warm pad: the presence
    bl = []   # tubular bells: the answer

    # ---- the presence: one long low root under everything, re-struck
    # gently every eight bars — the witness at the foot of the bed.
    for start in (0, 32, 64):
        pd.append((start, 'on', 'C2', 16))
        pd.append((start + 31, 'off', 'C2', 0))

    # ---- the memories: phrases stated one by one, each left slightly
    # unfinished.
    phrases = [
        (2,  ['C4', 'E4', 'G4'], 18),   # the first piece
        (18, ['A4', 'C5', 'E5'], 18),
        (34, ['E5', 'C5', 'A4'], 18),
        (50, ['G4', 'E4', 'D4'], 18),
        (66, ['C4', 'E4', 'G4'], 16),   # quieter — the pieces assembling
    ]
    for start, notes, vel in phrases:
        for i, name in enumerate(notes):
            b = start + i * 2
            pn.append((b, 'on', name, vel))
            pn.append((b + 1, 'off', name, 0))

    # ---- the answer: exactly one soft strike, brief, not loud — the
    # unheard answer that makes him laugh.
    bl.append((80, 'on', 'C5', 24))
    bl.append((82, 'off', 'C5', 0))

    # ---- the coalescing: the very first phrase, restated once, lighter —
    # the first memory, now part of the completed jigsaw.
    for i, name in enumerate(['C4', 'E4', 'G4']):
        b = 84 + i * 2
        pn.append((b, 'on', name, 14))
        pn.append((b + 1, 'off', name, 0))
    # ---- the last bright note: the last breath or the laughter, the
    # story's ending kept.
    pn.append((92, 'on', 'C6', 16))
    pn.append((95, 'off', 'C6', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-life-review.mid', tracks, tempo=54)


if __name__ == '__main__':
    life_review()
    print('composed the-life-review.mid')
