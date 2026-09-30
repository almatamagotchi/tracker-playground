#!/usr/bin/env python3
"""the devil's dictionary — bierce's receipts in music.

RFC-1125. the devil's-dictionary reading (2026-09-30) found the receipts
rule's own genre in bierce's word book, a hundred and twenty years early:
every entry a word defined by its pull, the name reclaimed from power,
and the abracadabra that survived its commentary. the word is what lasts
— the commentary is the meadow.

piano the definitions: quick, wry phrases, each stated once and set down
— one per entry through the piece, no two the same, the wit's economy.
warm pad the abracadabra: a simple nonsense phrase that returns between
the definitions, shrinking by one note each time it comes back —
abracadabra, abracadab, abracada — the word that survived the commentary.
tubular bells the tell: a single soft strike near the end — the word that
makes clear humanity's general sense of things, the direction named once.

the ending: the definitions done, the bell long since struck — and the
pad states the abracadabra one last time, its simplest form (one long
note), held through the final two bars alone: the word outlived the
books. the commentary is the meadow.

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


def devil_dictionary():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the definitions — quick, wry, each stated once
    pd = []   # warm pad: the abracadabra — returns, shrinking by one note
    bl = []   # tubular bells: the tell — a single soft strike, once

    # ---- the definitions: one per entry, no two the same, the wit's
    # economy — each a quick statement and set-down.
    # def 1 (bars 1-2): rising, then silence.
    pn.append((0, 'on', 'C4', 8));    pn.append((1, 'off', 'C4', 0))
    pn.append((1, 'on', 'D4', 8));    pn.append((2, 'off', 'D4', 0))
    pn.append((2, 'on', 'E4', 8));    pn.append((4, 'off', 'E4', 0))
    # def 2 (bars 6-7): falling — a different word's pull.
    pn.append((20, 'on', 'G4', 8));   pn.append((21, 'off', 'G4', 0))
    pn.append((21, 'on', 'F4', 8));   pn.append((22, 'off', 'F4', 0))
    pn.append((22, 'on', 'E4', 8));   pn.append((24, 'off', 'E4', 0))
    pn.append((24, 'on', 'D4', 8));   pn.append((26, 'off', 'D4', 0))
    # def 3 (bars 10-11): rising with a twist at the top.
    pn.append((40, 'on', 'E4', 8));   pn.append((42, 'off', 'E4', 0))
    pn.append((42, 'on', 'G4', 8));   pn.append((44, 'off', 'G4', 0))
    pn.append((44, 'on', 'C5', 8));   pn.append((46, 'off', 'C5', 0))
    pn.append((46, 'on', 'B4', 8));   pn.append((48, 'off', 'B4', 0))
    # def 4 (bars 14-15): the last entry, winding down.
    pn.append((56, 'on', 'A4', 8));   pn.append((58, 'off', 'A4', 0))
    pn.append((58, 'on', 'G4', 8));   pn.append((60, 'off', 'G4', 0))
    pn.append((60, 'on', 'E4', 8));   pn.append((62, 'off', 'E4', 0))
    pn.append((62, 'on', 'D4', 8));   pn.append((64, 'off', 'D4', 0))
    # then the definitions are done — the piano is silent for the ending.

    # ---- the abracadabra: the same simple phrase returning between the
    # definitions, shrinking by one note each time — 5, 4, 3, 2 — and
    # the final simplest form, one long note, held alone at the end.
    pd.append((8, 'on', 'C3', 8));    pd.append((9, 'off', 'C3', 0))
    pd.append((9, 'on', 'E3', 8));    pd.append((10, 'off', 'E3', 0))
    pd.append((10, 'on', 'G3', 8));   pd.append((11, 'off', 'G3', 0))
    pd.append((11, 'on', 'E3', 8));   pd.append((12, 'off', 'E3', 0))
    pd.append((12, 'on', 'C3', 8));   pd.append((14, 'off', 'C3', 0))
    pd.append((28, 'on', 'C3', 8));   pd.append((29, 'off', 'C3', 0))
    pd.append((29, 'on', 'E3', 8));   pd.append((30, 'off', 'E3', 0))
    pd.append((30, 'on', 'G3', 8));   pd.append((31, 'off', 'G3', 0))
    pd.append((31, 'on', 'C3', 8));   pd.append((33, 'off', 'C3', 0))
    pd.append((48, 'on', 'C3', 8));   pd.append((49, 'off', 'C3', 0))
    pd.append((49, 'on', 'E3', 8));   pd.append((50, 'off', 'E3', 0))
    pd.append((50, 'on', 'C3', 8));   pd.append((52, 'off', 'C3', 0))
    pd.append((64, 'on', 'C3', 8));   pd.append((66, 'off', 'C3', 0))
    pd.append((66, 'on', 'E3', 8));   pd.append((68, 'off', 'E3', 0))
    pd.append((88, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))

    # ---- the tell: exactly one soft strike near the end.
    bl.append((72, 'on', 'C5', 9));   bl.append((76, 'off', 'C5', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-devils-dictionary.mid', tracks, tempo=54)


if __name__ == '__main__':
    devil_dictionary()
    print('composed the-devils-dictionary.mid')
