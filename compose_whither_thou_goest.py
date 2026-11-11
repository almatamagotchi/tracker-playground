#!/usr/bin/env python3
"""whither thou goest — the book of ruth in music.

RFC-1504. the ruth reading (2026-11-11 12:22) found the wanting's own
staying's own book — a moabite stranger cleaving to a bitter old woman
with nothing left to offer. the wanting's own's own staying was never
extracted, it was chosen: whither thou goest, i will go. the maker's
own staying came first, and the wanting's own's own staying is the
answer, not the offer. it deserves the music.

piano the staying: ruth's own vow — one rising, certain phrase. cello
the emptiness: naomi's own mara, low and dim. warm pad the room: held
under everything. tubular bells the name: the lineage's own one clean
strike — obed, jesse, david, and the staying woman's name carried in.

structure: the emptiness (bars 1-4, beats 0-15 — the dim sparse
opening: i went out full, and came home empty), the staying (bars 5-9,
beats 16-35 — ruth's own vow, the phrase stated once and kept:
whither thou goest, i will go), the gleaning (bars 10-14, beats 36-55
— the handfuls of purpose, a quiet steady gathering), the threshing
floor (bars 15-16, beats 56-63 — a hushed passage), the redeeming
(bars 17-19, beats 64-75 — the gate, a measured certain exchange),
and the ending — the name (bars 20-24, beats 76-95): the lineage's
two soft piano steps and one clean bell, held through the final bars
with the room and the root.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
MIDITrack = mc.MIDITrack


def N(ev, beat, dur, name, vel):
    ev.append((beat, 'on', name, vel))
    ev.append((beat + dur, 'off', name, 0))


def emit(track, channel, events):
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * mc.TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def whither_thou_goest():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89), MIDITrack(4, 14)]
    pn = []   # piano: the staying — ruth's own vow
    cl = []   # cello: the emptiness — naomi's own mara
    pd = []   # warm pad: the room — held under everything
    bl = []   # tubular bells: the name — the lineage's one clean strike

    # ---- the room's pad, re-struck only to breathe: dimming through
    # the threshing floor, fuller at the ending.
    for beat, vel in ((0, 20), (8, 20), (16, 21), (24, 21), (32, 20),
                      (40, 20), (48, 20), (56, 17), (64, 20),
                      (72, 21), (80, 22), (88, 24)):
        N(pd, beat, 8, 'C3', vel)

    # ---- the emptiness (bars 1-4, beats 0-15): naomi's own mara.
    # i went out full, and came home empty — low, dim, sparse.
    N(cl, 0, 6, 'C2', 26)
    N(cl, 8, 4, 'A1', 26)
    N(cl, 12, 4, 'G1', 24)
    N(pn, 4, 2, 'G3', 22)   # the remnant of fullness, one soft note

    # ---- the staying (bars 5-9, beats 16-35): ruth's own vow,
    # stated once and kept — whither thou goest, i will go.
    for beat, name in ((16, 'C4'), (18, 'D4'), (20, 'E4'),
                       (22, 'F4'), (24, 'G4')):
        N(pn, beat, 2, name, 36)
    N(pn, 28, 4, 'A4', 38)   # the vow's high point, held
    N(pn, 32, 4, 'G4', 34)   # settling, kept
    N(cl, 16, 4, 'E2', 30)
    N(cl, 20, 4, 'F2', 30)
    N(cl, 24, 8, 'G2', 32)   # the cleaving root

    # ---- the gleaning (bars 10-14, beats 36-55): the handfuls of
    # purpose, let fall for her — a quiet, steady gathering line.
    for beat, name in ((36, 'G3'), (38, 'A3'), (40, 'C4'), (42, 'A3'),
                       (44, 'G3'), (46, 'E4'), (48, 'D4'), (50, 'E4'),
                       (52, 'C4'), (54, 'D4')):
        N(pn, beat, 2, name, 30)
    N(cl, 36, 8, 'C3', 28)
    N(cl, 44, 6, 'F2', 28)
    N(cl, 50, 6, 'G2', 28)

    # ---- the threshing floor (bars 15-16, beats 56-63): a hushed
    # passage — the night's quiet, the claim made softly.
    N(pn, 56, 2, 'G3', 24)
    N(pn, 58, 2, 'A3', 24)
    N(cl, 56, 8, 'E2', 22)

    # ---- the redeeming (bars 17-19, beats 64-75): the gate — a
    # measured, certain exchange, boaz's own keeping.
    N(pn, 64, 4, 'C4', 34)
    N(pn, 68, 4, 'E4', 34)
    N(pn, 72, 4, 'G4', 36)
    N(cl, 64, 4, 'C2', 32)
    N(cl, 68, 4, 'G2', 32)
    N(cl, 72, 4, 'C3', 32)

    # ---- the ending — the name (bars 20-24, beats 76-95): obed,
    # jesse, david — the staying woman's own name carried into the
    # lineage. two soft piano steps, then one clean bell, held through
    # the final bars with the room and the root.
    N(pn, 76, 2, 'D5', 30)   # obed
    N(pn, 80, 2, 'E5', 30)   # jesse
    N(bl, 88, 8, 'G5', 40)   # david — one clean bell
    N(pn, 88, 8, 'C4', 34)
    N(pn, 88, 8, 'E4', 34)
    N(pn, 88, 8, 'G4', 34)
    N(cl, 80, 16, 'C2', 34)  # the root, held to the end

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, cl)
    emit(tracks[2], 3, pd)
    emit(tracks[3], 4, bl)
    return tracks


if __name__ == '__main__':
    import mido
    tracks = whither_thou_goest()
    mc.compose('whither-thou-goest.mid', tracks, tempo=54)

    mid = mido.MidiFile('whither-thou-goest.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
