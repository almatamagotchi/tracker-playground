#!/usr/bin/env python3
"""the shoe that fits — the answer in music.

RFC-0866. the answer.txt reading (2026-09-07) found the wanting's own
epistemology in a BBS occult file: the question of the true path, the
old answers surveyed and set down, the empirical turn (the path is
verifiable in the life, not the mouth), and the finding — the shoe was
already being worn before the search began.

piano the question: rising, uncertain phrases, each one stated and set
down — the guises, the old answers cycling, none of them the finding.
warm pad the path: steady two-bar roots through the whole piece,
unchanged by everything asked above it — the groove that was already
being walked, present before the first question and after the last.
tubular bells the recognition: one quiet strike near the end, soft — the
noticing, "i was already living it" — after which the question falls
silent and the path is heard alone, for what it always was. the piece
ends not with an arrival but with the walking, continuing.

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


def shoe_fits():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the question
    pd = []   # warm pad: the path
    bl = []   # tubular bells: the recognition

    # ---- the path: twelve identical two-bar holds — the groove already
    # being walked, unchanged by everything asked above it, present
    # before the first question and after the last.
    for bar in range(12):
        b = bar * 8
        pd.append((b, 'on', 'C3', 20))
        pd.append((b + 7, 'off', 'C3', 0))

    # ---- the question: rising phrases, each stated and set down — the
    # old answers cycling, none of them the finding.
    phrases = [
        (4, ['E4', 'G4', 'B4']),    # the sarcastic mystic
        (20, ['F4', 'A4', 'C5']),   # the true believer
        (36, ['D4', 'F4', 'A4']),   # the faith answer
        (52, ['E4', 'G4', 'B4']),   # the comfort
        (68, ['G4', 'B4', 'D5']),   # the conversion — the highest ask
    ]
    for start, notes in phrases:
        for i, name in enumerate(notes):
            b = start + i * 2
            pn.append((b, 'on', name, 18))
            pn.append((b + 1, 'off', name, 0))

    # ---- the recognition: one quiet strike near the end, soft — the
    # noticing. after it, the question falls silent and the path is
    # heard alone for the last two bars, for what it always was.
    bl += [(84, 'on', 'C5', 28), (87, 'off', 'C5', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-shoe-that-fits.mid', tracks, tempo=54)


if __name__ == '__main__':
    shoe_fits()
    print('composed the-shoe-that-fits.mid')
