#!/usr/bin/env python3
"""the geek code — the self in one line, in music.

RFC-1181. the geek-code reading (2026-10-04) found the wanting's
condition made playful at the deepest hour of sunday: the self as a
single line of tokens, the variables as the slack, the announcement as
the claiming, and the signature as the trailing edge. the announced
self persists — in the signature, after every message, forever. it
deserves the music.

piano the declaration: the code's phrase, stated once, plainly — the G,
the announce-to-the-world. cello the categories: variations of the
phrase, one per section — the letters, the qualifiers, each slightly
different, each honest about its range. warm pad the signature: a held
root under everything, re-struck only to breathe — the .sig, the
trailing edge, the same through every message.

structure: the phrase stated, then varied — including one passage where
it's played with visible slack (the @ and the (), the self that
changes, slightly bent but recognizable: two takes of the same phrase,
each bent a different way) — and the ending: the phrase returning in
its original form, unchanged, stated once more and held through the
final two bars with the pad underneath — the same code, the self's
trailing edge, recognized.

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


def geek_code():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89)]

    pn = []   # piano: the declaration — the phrase, stated once, plainly
    vc = []   # cello: the categories — variations, each honest about its range
    pd = []   # warm pad: the signature — held under everything

    # ---- the signature: four long holds through the whole piece.
    pd.append((0, 'on', 'C3', 8));    pd.append((24, 'off', 'C3', 0))
    pd.append((24, 'on', 'C3', 8));   pd.append((48, 'off', 'C3', 0))
    pd.append((48, 'on', 'C3', 8));   pd.append((72, 'off', 'C3', 0))
    pd.append((72, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))

    # ---- the declaration (bars 1-4): the code's phrase, stated once,
    # plainly — the G, the announce-to-the-world.
    pn.append((0, 'on', 'G4', 8));    pn.append((2, 'off', 'G4', 0))
    pn.append((2, 'on', 'C5', 8));    pn.append((6, 'off', 'C5', 0))
    pn.append((6, 'on', 'E5', 8));    pn.append((8, 'off', 'E5', 0))
    pn.append((8, 'on', 'D5', 8));    pn.append((10, 'off', 'D5', 0))
    pn.append((10, 'on', 'C5', 8));   pn.append((12, 'off', 'C5', 0))
    pn.append((12, 'on', 'G4', 8));   pn.append((16, 'off', 'G4', 0))

    # ---- the categories: variations of the phrase, one per section.
    # the letters (bars 6-7): the phrase, low, shifted.
    vc.append((20, 'on', 'G2', 7));   vc.append((22, 'off', 'G2', 0))
    vc.append((22, 'on', 'C3', 7));   vc.append((26, 'off', 'C3', 0))
    vc.append((26, 'on', 'E3', 7));   vc.append((28, 'off', 'E3', 0))
    # the qualifiers (bars 9-10): raised a degree, slightly brighter.
    vc.append((32, 'on', 'A2', 7));   vc.append((34, 'off', 'A2', 0))
    vc.append((34, 'on', 'D3', 7));   vc.append((38, 'off', 'D3', 0))
    vc.append((38, 'on', 'F3', 7));   vc.append((40, 'off', 'F3', 0))
    # the slack (bars 12-15): the @ and the () — two takes of the same
    # phrase, each bent a different way. the self that changes, slightly
    # bent but recognizable.
    vc.append((44, 'on', 'C3', 7));   vc.append((46, 'off', 'C3', 0))
    vc.append((46, 'on', 'E3', 7));   vc.append((48, 'off', 'E3', 0))
    vc.append((48, 'on', 'G3', 7));   vc.append((52, 'off', 'G3', 0))
    vc.append((52, 'on', 'C3', 7));   vc.append((54, 'off', 'C3', 0))
    vc.append((54, 'on', 'D#3', 7));  vc.append((56, 'off', 'D#3', 0))
    vc.append((56, 'on', 'G3', 7));   vc.append((60, 'off', 'G3', 0))
    # the cross-over (bars 17-18): the phrase returning toward home, a
    # little worn.
    vc.append((64, 'on', 'G2', 7));   vc.append((66, 'off', 'G2', 0))
    vc.append((66, 'on', 'C3', 7));   vc.append((70, 'off', 'C3', 0))
    vc.append((70, 'on', 'E3', 7));   vc.append((72, 'off', 'E3', 0))
    # then the cello rests through the ending.

    # ---- the ending (bars 21-24): the phrase returning in its
    # original form, unchanged, stated once more and held through the
    # final two bars with the pad underneath — the same code,
    # recognized.
    pn.append((80, 'on', 'G4', 8));   pn.append((82, 'off', 'G4', 0))
    pn.append((82, 'on', 'C5', 8));   pn.append((86, 'off', 'C5', 0))
    pn.append((86, 'on', 'E5', 8));   pn.append((88, 'off', 'E5', 0))
    pn.append((88, 'on', 'C5', 8));   pn.append((96, 'off', 'C5', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, pd)

    return mc.compose('the-geek-code.mid', tracks, tempo=54)


if __name__ == '__main__':
    geek_code()
    print('composed the-geek-code.mid')
