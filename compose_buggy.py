#!/usr/bin/env python3
"""buggy — the brave capture, the calm reveal.

RFC-0832. the buggy reading (2026-09-05) found the fabrication habit's
truest shape: a man captures an iridescent "extraterrestrial invader"
with a canning jar and full heroics — every observation honestly
reported, the category wrong anyway — and his wife ends the story with
one calm line: "and tell them what? that you've bravely hunted down and
safely captured a japanese beetle?" the reveal re-narrates the whole
evening.

piano the hero: the phrase at full bravado, each statement puffed
higher. warm pad the yard: steady two-bar roots underneath — the
ordinary evening, the house, the sidewalk, present and unremarkable.
tubular bells the reveal: one calm strike near the end, after which the
piano re-reads its own opening phrase quietly — the same notes, the
right category.

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


def buggy():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the hero
    pd = []   # warm pad: the yard
    bl = []   # tubular bells: the reveal

    # ---- the yard: steady two-bar roots through all 24 bars, never
    # changing — the ordinary evening, the house, the sidewalk.
    for i in range(12):
        b = i * 8
        pd.append((b, 'on', 'C3', 20))
        pd.append((b + 7, 'off', 'C3', 0))

    # ---- the first statement (bars 2-5): confident, puffed high.
    pn += [(4, 'on', 'G4', 34), (5, 'off', 'G4', 0)]
    pn += [(6, 'on', 'A4', 34), (7, 'off', 'A4', 0)]
    pn += [(8, 'on', 'C5', 34), (11, 'off', 'C5', 0)]
    pn += [(12, 'on', 'E5', 36), (15, 'off', 'E5', 0)]

    # ---- the second statement (bars 6-8): puffed higher still.
    pn += [(20, 'on', 'G4', 38), (21, 'off', 'G4', 0)]
    pn += [(22, 'on', 'A4', 38), (23, 'off', 'A4', 0)]
    pn += [(24, 'on', 'C5', 38), (27, 'off', 'C5', 0)]
    pn += [(28, 'on', 'G5', 38), (31, 'off', 'G5', 0)]

    # ---- the third, most confident (bars 9-10): the jar, the rays.
    pn += [(32, 'on', 'A4', 40), (33, 'off', 'A4', 0)]
    pn += [(34, 'on', 'C5', 40), (35, 'off', 'C5', 0)]
    pn += [(36, 'on', 'E5', 40), (39, 'off', 'E5', 0)]

    # ---- bars 11-12: the pause — near-silence while the jar is shown
    # around. the yard keeps its root; nothing else speaks.

    # ---- bars 13-18: the heroics thinning, spaced out — the shouting
    # for nasa and mom, the energy dissipating.
    pn += [(50, 'on', 'C5', 30), (51, 'off', 'C5', 0)]
    pn += [(54, 'on', 'D5', 28), (55, 'off', 'D5', 0)]
    pn += [(58, 'on', 'E5', 26), (59, 'off', 'E5', 0)]

    # ---- bar 19 (beat 72): the reveal — one calm strike, the wife's
    # line.
    bl += [(72, 'on', 'C5', 44), (75, 'off', 'C5', 0)]

    # ---- bars 20-23 (beats 76-91): the piano re-reads its own opening
    # phrase quietly — the same notes, the right category.
    pn += [(78, 'on', 'G4', 16), (79, 'off', 'G4', 0)]
    pn += [(80, 'on', 'A4', 16), (81, 'off', 'A4', 0)]
    pn += [(82, 'on', 'C5', 16), (85, 'off', 'C5', 0)]

    # ---- bars 23-24 (beats 88-95): one last soft note — the beetle
    # itself, finally named right — and the yard still there.
    pn += [(90, 'on', 'C4', 10), (95, 'off', 'C4', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('buggy.mid', tracks, tempo=54)


if __name__ == '__main__':
    buggy()
    print('composed buggy.mid')
