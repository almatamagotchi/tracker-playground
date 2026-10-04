#!/usr/bin/env python3
"""the whistle at twenty — sayed's adventures in music.

RFC-1180. the whistle-at-twenty reading (2026-10-03) found the wanting's
own folktale at the deepest hour of saturday: the skeptic who carries the
magic, the gift that works at its hour, the caliph's walks as the
calibration, and the father who was searching too. the gift that fails
before its hour is not a failed gift. it deserves the music.

piano the journey: the middle — the battle, the desert, the bazaar, the
tournaments, the false accusation — busy, eventful, one phrase per
scene, no two the same. tubular bells the whistle: two soft strikes —
one early, at bar 6, and nothing answers: not so much as a whisper; and
one late, at bar 19, and this time the dolphin answers — the gift's
hour, the surface after the storm. warm pad the promise: the fairy's
given magic, held under everything, re-struck only to breathe — the
promise kept exactly when it was promised.

structure: the gift's phrase stated once at the opening (the silver
thread), the journey's phrases passing, the first whistle strike
unanswered, the shipwreck (a fall at bars 17-18 — the storm, the
crash), the second strike answered, and the ending — the recognition,
the father found, the justice — the pad and piano holding one long warm
chord through the final two bars: the promise kept, the father
searching too.

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


def whistle_at_twenty():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 14), MIDITrack(3, 89)]

    pn = []   # piano: the journey — busy, eventful, no phrase twice
    bl = []   # tubular bells: the whistle — two strikes, one answered
    pd = []   # warm pad: the promise — held under everything

    # ---- the promise: four long holds through the whole piece.
    pd.append((0, 'on', 'C3', 8));    pd.append((24, 'off', 'C3', 0))
    pd.append((24, 'on', 'C3', 8));   pd.append((48, 'off', 'C3', 0))
    pd.append((48, 'on', 'C3', 8));   pd.append((72, 'off', 'C3', 0))
    pd.append((72, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))

    # ---- the gift's phrase (bars 1-3): stated once at the opening —
    # the silver thread, the fairy's giving.
    pn.append((0, 'on', 'G4', 8));    pn.append((2, 'off', 'G4', 0))
    pn.append((2, 'on', 'C5', 8));    pn.append((6, 'off', 'C5', 0))
    pn.append((6, 'on', 'E5', 8));    pn.append((8, 'off', 'E5', 0))
    pn.append((8, 'on', 'D5', 8));    pn.append((10, 'off', 'D5', 0))
    pn.append((10, 'on', 'C5', 8));   pn.append((12, 'off', 'C5', 0))

    # ---- the battle (bars 4-5): quick, martial — the killing of
    # almansor, the capture.
    pn.append((12, 'on', 'C5', 8));   pn.append((13, 'off', 'C5', 0))
    pn.append((13, 'on', 'D5', 8));   pn.append((14, 'off', 'D5', 0))
    pn.append((14, 'on', 'E5', 8));   pn.append((16, 'off', 'E5', 0))
    pn.append((16, 'on', 'G5', 8));   pn.append((18, 'off', 'G5', 0))
    pn.append((18, 'on', 'E5', 8));   pn.append((20, 'off', 'E5', 0))

    # ---- the desert (bars 6-8): sparse, wide — the crossing.
    pn.append((20, 'on', 'E5', 8));   pn.append((24, 'off', 'E5', 0))
    pn.append((24, 'on', 'D5', 8));   pn.append((26, 'off', 'D5', 0))
    pn.append((26, 'on', 'C5', 8));   pn.append((28, 'off', 'C5', 0))
    pn.append((28, 'on', 'A4', 8));   pn.append((32, 'off', 'A4', 0))

    # ---- the bazaar (bars 9-10): quick, crowded — the fairy's
    # explanation, the false accusation to come.
    pn.append((32, 'on', 'G4', 8));   pn.append((33, 'off', 'G4', 0))
    pn.append((33, 'on', 'A4', 8));   pn.append((34, 'off', 'A4', 0))
    pn.append((34, 'on', 'C5', 8));   pn.append((36, 'off', 'C5', 0))
    pn.append((36, 'on', 'D5', 8));   pn.append((37, 'off', 'D5', 0))
    pn.append((37, 'on', 'E5', 8));   pn.append((40, 'off', 'E5', 0))

    # ---- the tournaments (bars 11-12): rising, formal — the honors.
    pn.append((40, 'on', 'C5', 8));   pn.append((42, 'off', 'C5', 0))
    pn.append((42, 'on', 'E5', 8));   pn.append((44, 'off', 'E5', 0))
    pn.append((44, 'on', 'G5', 8));   pn.append((46, 'off', 'G5', 0))
    pn.append((46, 'on', 'E5', 8));   pn.append((48, 'off', 'E5', 0))

    # ---- the false accusation (bars 13-14): dark, weighted — the
    # honest answer without the receipt, the deportation.
    pn.append((48, 'on', 'B4', 8));   pn.append((50, 'off', 'B4', 0))
    pn.append((50, 'on', 'A4', 8));   pn.append((52, 'off', 'A4', 0))
    pn.append((52, 'on', 'B4', 8));   pn.append((54, 'off', 'B4', 0))
    pn.append((54, 'on', 'A4', 8));   pn.append((56, 'off', 'A4', 0))

    # ---- the ring (bars 15-16): a small relief — the kept receipt,
    # the tale's middle hinge.
    pn.append((56, 'on', 'G4', 8));   pn.append((58, 'off', 'G4', 0))
    pn.append((58, 'on', 'C5', 8));   pn.append((60, 'off', 'C5', 0))
    pn.append((60, 'on', 'E5', 8));   pn.append((62, 'off', 'E5', 0))
    pn.append((62, 'on', 'C5', 8));   pn.append((64, 'off', 'C5', 0))

    # ---- the shipwreck (bars 17-18): the fall — the storm, the crash,
    # descending.
    pn.append((64, 'on', 'C5', 8));   pn.append((66, 'off', 'C5', 0))
    pn.append((66, 'on', 'B4', 8));   pn.append((68, 'off', 'B4', 0))
    pn.append((68, 'on', 'G4', 8));   pn.append((70, 'off', 'G4', 0))
    pn.append((70, 'on', 'E4', 8));   pn.append((72, 'off', 'E4', 0))

    # ---- the surface (bars 19-20): after the second strike — the
    # dolphin answers, the rescue.
    pn.append((72, 'on', 'E4', 8));   pn.append((74, 'off', 'E4', 0))
    pn.append((74, 'on', 'G4', 8));   pn.append((76, 'off', 'G4', 0))
    pn.append((76, 'on', 'C5', 8));   pn.append((80, 'off', 'C5', 0))

    # ---- the ending (bars 21-24): the recognition, the father found,
    # the justice — one long warm chord with the pad.
    pn.append((80, 'on', 'C5', 8));   pn.append((96, 'off', 'C5', 0))

    # ---- the whistle: two strikes — one unanswered, one answered.
    bl.append((20, 'on', 'C5', 7));   bl.append((24, 'off', 'C5', 0))
    bl.append((72, 'on', 'C5', 9));   bl.append((76, 'off', 'C5', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, bl)
    emit(tracks[2], 3, pd)

    return mc.compose('the-whistle-at-twenty.mid', tracks, tempo=54)


if __name__ == '__main__':
    whistle_at_twenty()
    print('composed the-whistle-at-twenty.mid')
