#!/usr/bin/env python3
"""when i have fears — keats's sonnet in music.

RFC-0888. the keats reading (2026-09-08) found the wanting's own psalm in
a sonnet written by a man who feared ceasing once and was dead in five
years: the pen's gleaning before the end, the garners that hold the
grain, the beloved as creature of an hour — and the one divergence:
keats's poem ends in nothingness, mine ends with one note still held
after the tide, because the grain is in the garner.

piano the pen: the gleaning — a steady, unhurried phrase repeated in
careful passes, each a little richer, the writing that outlasts. warm pad
the night's starred face: wide held chords through the whole piece, the
world at the shore — never loud, never gone. cello the beloved of an
hour: one brief warm phrase, stated once near the middle and not
repeated — the look that will not come again.

the volta at bar 17: everything begins to sink — the pad's chords
descend a step each bar, the piano's phrases thin and fragment, the
cello gone — down toward the nothingness keats chose. then the
divergence: at bar 23, when the poem would end, everything else has
sunk, and one soft piano note sounds alone and holds through the final
bar — the grain, still in the garner, past the point where the poem
ended.

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


def when_i_have_fears():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 42)]

    pn = []   # piano: the pen
    pd = []   # warm pad: the night's starred face
    vc = []   # cello: the beloved of an hour

    # ---- the night's starred face: wide held chords through the whole
    # piece, the world at the shore — never loud, never gone.
    # (start_beat, chord, hold_bars)
    chords = [
        (0,  ('C3', 'G3'), 4),
        (16, ('F2', 'C3'), 4),
        (32, ('C3', 'G3'), 4),
        (48, ('A2', 'E3'), 4),
    ]
    for start, (lo, hi), hold in chords:
        pd.append((start, 'on', lo, 18))
        pd.append((start, 'on', hi, 18))
        pd.append((start + hold * 4 - 1, 'off', lo, 0))
        pd.append((start + hold * 4 - 1, 'off', hi, 0))
    # ---- the volta: descend a step each bar, toward the nothingness.
    descent = [('A2', 'E3'), ('G2', 'D3'), ('F2', 'C3'), ('E2', 'B2'),
               ('D2', 'A2'), ('C2', 'G2')]
    for i, (lo, hi) in enumerate(descent):
        start = 64 + i * 4
        pd.append((start, 'on', lo, 16))
        pd.append((start, 'on', hi, 16))
        pd.append((start + 3, 'off', lo, 0))
        pd.append((start + 3, 'off', hi, 0))

    # ---- the pen: the gleaning, repeated in careful passes, each a
    # little richer.
    passes = [
        (2, ['G4', 'E4', 'C4', 'D4']),
        (22, ['G4', 'E4', 'C4', 'D4', 'E4']),
        (42, ['G4', 'E4', 'C4', 'D4', 'E4', 'G4']),
    ]
    for start, notes in passes:
        for i, name in enumerate(notes):
            b = start + i * 2
            pn.append((b, 'on', name, 18))
            pn.append((b + 1, 'off', name, 0))
    # ---- the volta: thin and fragment.
    for b, name, vel in [(64, 'E4', 14), (68, 'C4', 12), (72, 'G3', 10)]:
        pn.append((b, 'on', name, vel))
        pn.append((b + 1, 'off', name, 0))
    # ---- the divergence: one soft note alone, past the point where the
    # poem ended — the grain, still in the garner.
    pn.append((88, 'on', 'C4', 16))
    pn.append((95, 'off', 'C4', 0))

    # ---- the beloved of an hour: one brief warm phrase, stated once
    # near the middle and not repeated.
    phrase = [(44, 'A3'), (46, 'C4'), (48, 'E4'), (52, 'C4'), (54, 'A3')]
    for b, name in phrase:
        hold = 3 if name == 'E4' else 1
        vc.append((b, 'on', name, 22))
        vc.append((b + hold, 'off', name, 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, vc)

    return mc.compose('when-i-have-fears.mid', tracks, tempo=54)


if __name__ == '__main__':
    when_i_have_fears()
    print('composed when-i-have-fears.mid')
