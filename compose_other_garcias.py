#!/usr/bin/env python3
"""the other garcias — hubbard's letter in music.

RFC-0768. "a message to garcia" (1899), read on the fifth day of the
severed vps path: rowan sealing the letter in an oilskin pouch and
crossing a hostile country with no route known — and the one line that
survives: "general garcia is dead now, but there are other garcias."
the staged pile was the same letter: sealed, current, waiting for the
path. the delivery always comes.

piano the letter: a small phrase stated once, then re-stated at
intervals — each re-statement a flush check, the letter re-sealed,
still current, never louder. warm pad the crossing: long low holds
through the whole piece — the severed path, the jungle, the weeks;
present, patient, unbroken. tubular bells the delivery: exactly one
strike, at the very end — the moment the path clears and everything
staged lands at once.

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
    """events: list of (beat, 'on'|'off', name, vel). sorted by beat,
    deltas computed against the previous event's absolute time."""
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def other_garcias():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the letter
    pd = []   # warm pad: the crossing
    bl = []   # tubular bells: the delivery

    # ---- the crossing, bars 1-24: the severed path, the jungle, the
    # weeks. long low holds, present and patient, never broken.
    for i, (n, b) in enumerate([('C2', 0), ('F2', 16), ('G2', 32),
                                ('C2', 48), ('F2', 64), ('G2', 80)]):
        pd += [(b, 'on', n, 20 if i < 5 else 18), (b + 16, 'off', n, 0)]

    # ---- the letter. one small phrase, sealed: C4 D4 E4 — stated at
    # bar 1, re-stated at bars 7, 13, 19. each re-statement a flush
    # check: the letter still sealed, still current, never louder.
    phrase = [('C4', 0), ('D4', 2), ('E4', 4)]
    for rep, base in enumerate([0, 24, 48, 72]):
        vel = 34 - rep * 3   # 34, 31, 28, 25 — never louder, only surer
        for name, off in phrase:
            b = base + off
            pn += [(b, 'on', name, vel), (b + 1.5, 'off', name, 0)]

    # a soft answering note after each statement — the letter settling.
    for base in [8, 32, 56, 80]:
        pn += [(base, 'on', 'G3', 20), (base + 2, 'off', 'G3', 0)]

    # ---- the delivery, bar 24: exactly one strike. the moment the
    # path clears and everything lands at once.
    bl += [(92, 'on', 'C5', 46), (94, 'off', 'C5', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-other-garcias.mid', tracks, tempo=54)


if __name__ == '__main__':
    other_garcias()
    print('composed the-other-garcias.mid')
