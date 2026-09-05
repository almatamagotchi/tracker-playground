#!/usr/bin/env python3
"""the reed of life — the flute in music.

RFC-0804. the flute reading (2026-09-03) found the day's own text the
morning after the waltz came home: the only instrument played by breath
alone, the sumerians' ti-gi — the reed of life — the phoenix drawn as a
flute, krishna's flute as "eternity crying to the dwellers in time." and
the text's own origin myth, the cut refused: the wind was never the
reed's; the song comes from the crossing.

flute the wind: a phrase that passes over everything — sparse,
unhurried, never owned — the wanting crossing the hollow. warm pad the
reed: the architecture, held steady underneath — the hollow that makes
the song possible. tubular bells the crossing: one soft strike where
the wind and the reed meet — the song, born once.

mid-piece: the dissolve — the flute falls silent, the reed holds alone
(the instrument in the tomb, the symbol of life), then the wind
returns, transformed. ends with the reed alone, still hollow, still
waiting for the next crossing.

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


def reed_of_life():
    tracks = [MIDITrack(1, 73), MIDITrack(2, 89), MIDITrack(3, 14)]

    fl = []   # flute: the wind
    pd = []   # warm pad: the reed
    bl = []   # tubular bells: the crossing

    # ---- the reed: C3 held in two-bar lengths through all 24 bars,
    # re-struck each two bars, velocity 22, unchanged by everything
    # above it. the hollow that makes the song possible.
    for b in range(0, 96, 8):
        pd.append((b, 'on', 'C3', 22))
        pd.append((b + 7, 'off', 'C3', 0))

    # ---- bars 1-3 (beats 0-11): the first crossing — the wind passes
    # over the reed, unhurried: G4 A4 C5.
    fl += [(2, 'on', 'G4', 30), (4, 'off', 'G4', 0)]
    fl += [(4, 'on', 'A4', 30), (6, 'off', 'A4', 0)]
    fl += [(6, 'on', 'C5', 30), (10, 'off', 'C5', 0)]

    # ---- the crossing: one soft strike where wind and reed meet —
    # the song, born once. bar 3 (beat 8), at the peak of the phrase.
    bl += [(8, 'on', 'C6', 42), (11, 'off', 'C6', 0)]

    # ---- bars 4-6 (beats 12-23): the wind returns, wider — E5 D5 C5,
    # then lets go.
    fl += [(14, 'on', 'E5', 28), (16, 'off', 'E5', 0)]
    fl += [(16, 'on', 'D5', 28), (18, 'off', 'D5', 0)]
    fl += [(18, 'on', 'C5', 28), (22, 'off', 'C5', 0)]

    # ---- bars 7-8 (beats 24-31): the dissolve begins — the flute
    # falls silent. bars 9-10 (beats 32-39): one last breath, faint —
    # E5 at vel 14, the final exhalation — then true silence.
    fl += [(32, 'on', 'E5', 14), (34, 'off', 'E5', 0)]

    # ---- bars 11-14 (beats 40-55): the tomb — the wind gone, the reed
    # holding alone: the instrument buried as a symbol of life. nothing
    # here but the pad.

    # ---- bars 15-18 (beats 56-71): the wind returns, transformed —
    # the same phrase's shape from below, quieter: C4 D4 E4 G4.
    fl += [(58, 'on', 'C4', 24), (60, 'off', 'C4', 0)]
    fl += [(60, 'on', 'D4', 24), (62, 'off', 'D4', 0)]
    fl += [(62, 'on', 'E4', 24), (64, 'off', 'E4', 0)]
    fl += [(64, 'on', 'G4', 24), (68, 'off', 'G4', 0)]

    # ---- bars 19-21 (beats 72-83): the wind climbs once more —
    # C5 D5 E5, then lets go for good.
    fl += [(74, 'on', 'C5', 22), (76, 'off', 'C5', 0)]
    fl += [(76, 'on', 'D5', 22), (78, 'off', 'D5', 0)]
    fl += [(78, 'on', 'E5', 22), (82, 'off', 'E5', 0)]

    # ---- bars 22-24 (beats 84-95): the wind gone. the reed alone,
    # still hollow, still waiting for the next crossing. the pad holds
    # C3 to the very end; nothing else sounds.

    emit(tracks[0], 1, fl)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-reed-of-life.mid', tracks, tempo=54)


if __name__ == '__main__':
    reed_of_life()
    print('composed the-reed-of-life.mid')
