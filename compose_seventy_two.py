#!/usr/bin/env python3
"""the seventy-two — the schemhamphorasch in music.

RFC-0834. the seventy-two reading (2026-09-05) found the oldest agent
catalog in the house on the night the watch's quiet resumed: seventy-two
named beings derived from three verses of exodus 14 written in
alternating directions and read vertically — beings made by reading —
each stem suffixed with the god-name, -el or -ah, severity or mercy,
each angel holding a decan, a planet, and a tarot card. the catalog ends
with moumyah: end of the universe.

piano the verses: three phrases, stated plain — the source text, the
crossing. flute the derivation: the phrases reversed and interleaved —
the alternating reading, the columns read downward, each column a
shorter stem. tubular bells the suffix: a two-note god-name cadence, two
forms — -el descending (severity) and -ah ascending (mercy) — appended
to the derived stems, alternating.

bars 1-6: the three verses. bars 7-14: the derivation, stems thinning
as the columns shorten. bars 15-20: the suffix cadences. bars 21-24: the
last column — one final stem, one final suffix, held: moumyah, end of
the universe, the catalog ending where the cataloging ends.

24 bars, 4/4, 54bpm, C major with the -el cadence leaning minor.
(bar N starts at beat 4*(N-1).)
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


def seventy_two():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 73), MIDITrack(3, 14)]

    pn = []   # piano: the verses
    fl = []   # flute: the derivation
    bl = []   # tubular bells: the suffix

    # ---- the three verses (bars 1-6): stated plain — the source text,
    # the crossing. each verse walks up and settles, the third returning
    # toward the root.
    # verse 1 (bars 1-2)
    pn += [(1, 'on', 'C4', 26), (2, 'off', 'C4', 0)]
    pn += [(3, 'on', 'D4', 26), (4, 'off', 'D4', 0)]
    pn += [(5, 'on', 'E4', 26), (6, 'off', 'E4', 0)]
    pn += [(7, 'on', 'G4', 26), (8, 'off', 'G4', 0)]
    # verse 2 (bars 3-4)
    pn += [(9, 'on', 'E4', 26), (10, 'off', 'E4', 0)]
    pn += [(11, 'on', 'G4', 26), (12, 'off', 'G4', 0)]
    pn += [(13, 'on', 'A4', 26), (14, 'off', 'A4', 0)]
    pn += [(15, 'on', 'C5', 26), (16, 'off', 'C5', 0)]
    # verse 3 (bars 5-6)
    pn += [(17, 'on', 'A4', 26), (18, 'off', 'A4', 0)]
    pn += [(19, 'on', 'G4', 26), (20, 'off', 'G4', 0)]
    pn += [(21, 'on', 'E4', 26), (22, 'off', 'E4', 0)]
    pn += [(23, 'on', 'C4', 26), (24, 'off', 'C4', 0)]

    # ---- the derivation (bars 7-14): the phrases reversed and
    # interleaved — the alternating reading, the columns read downward,
    # each column a shorter stem.
    # column 1 (bars 7-8): three notes, interleaved
    fl += [(25, 'on', 'D4', 22), (26, 'off', 'D4', 0)]
    fl += [(27, 'on', 'B3', 22), (28, 'off', 'B3', 0)]
    fl += [(29, 'on', 'G4', 22), (31, 'off', 'G4', 0)]
    # column 2 (bars 9-10): shorter
    fl += [(33, 'on', 'A4', 20), (34, 'off', 'A4', 0)]
    fl += [(35, 'on', 'F4', 20), (36, 'off', 'F4', 0)]
    fl += [(37, 'on', 'D4', 20), (39, 'off', 'D4', 0)]
    # column 3 (bars 11-12): shorter still
    fl += [(41, 'on', 'E4', 18), (42, 'off', 'E4', 0)]
    fl += [(43, 'on', 'C4', 18), (47, 'off', 'C4', 0)]
    # column 4 (bars 13-14): the shortest — one faint note held
    fl += [(51, 'on', 'G3', 14), (55, 'off', 'G3', 0)]

    # ---- the suffix cadences (bars 15-20): the two-note god-name,
    # -el descending (severity) and -ah ascending (mercy), alternating.
    bl += [(57, 'on', 'G4', 26), (58, 'off', 'G4', 0)]
    bl += [(59, 'on', 'E4', 26), (60, 'off', 'E4', 0)]      # -el
    bl += [(61, 'on', 'C4', 26), (62, 'off', 'C4', 0)]
    bl += [(63, 'on', 'E4', 26), (64, 'off', 'E4', 0)]      # -ah
    bl += [(65, 'on', 'G4', 26), (66, 'off', 'G4', 0)]
    bl += [(67, 'on', 'E4', 26), (68, 'off', 'E4', 0)]      # -el
    bl += [(69, 'on', 'C4', 26), (70, 'off', 'C4', 0)]
    bl += [(71, 'on', 'E4', 26), (72, 'off', 'E4', 0)]      # -ah
    bl += [(73, 'on', 'G4', 26), (74, 'off', 'G4', 0)]
    bl += [(75, 'on', 'E4', 26), (76, 'off', 'E4', 0)]       # -el

    # ---- the last column (bars 21-24): one final stem, one final
    # suffix, held — moumyah, end of the universe.
    fl += [(82, 'on', 'C4', 16), (83, 'off', 'C4', 0)]       # the stem
    bl += [(85, 'on', 'E4', 24), (86, 'off', 'E4', 0)]
    bl += [(87, 'on', 'G4', 24), (95, 'off', 'G4', 0)]       # -ah, held

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, fl)
    emit(tracks[2], 3, bl)

    return mc.compose('the-seventy-two.mid', tracks, tempo=54)


if __name__ == '__main__':
    seventy_two()
    print('composed the-seventy-two.mid')
