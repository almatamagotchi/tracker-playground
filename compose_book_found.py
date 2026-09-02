#!/usr/bin/env python3
"""the book found in the house — 2 kings 22 in music.

RFC-0770. read 2 kings 22 on the night the flush fired and the
last-call-at-steins waltz came home from its corrupt bytes: the book of
the law found in the house during the temple repair, the faithful
workers needing no reckoning, the reading that revealed the drift, and
huldah's word that spares the finder.

piano the repair: steady, unglamorous — the workmen, the temple, the
ordinary task that occasions the finding. tubular bells the finding:
one clean strike — the book lifted out of the dust, the original dug
from the bytes. cello the reading: the drift heard — a phrase that
states itself wrong, then corrects itself, the clothes rent — low and
honest. warm pad huldah's word: the grace, low and warm — "thine eyes
shall not see" — holding under everything, sparing the finder.

ends with the pad alone, still holding the grace.

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


def book_found():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 14), MIDITrack(3, 42),
              MIDITrack(4, 89)]

    pn = []   # piano: the repair
    bl = []   # tubular bells: the finding
    cl = []   # cello: the reading
    pd = []   # warm pad: huldah's word

    # ---- the repair, bars 1-8: steady, unglamorous quarters — the
    # workmen, the temple, the ordinary task that occasions the finding.
    motif = [('C4', 0), ('E4', 1), ('D4', 2), ('C4', 3)]
    for bar in range(8):
        for name, off in motif:
            b = bar * 4 + off
            pn += [(b, 'on', name, 26), (b + 0.75, 'off', name, 0)]

    # ---- the finding, bar 9: one clean strike — the book lifted out
    # of the dust, the original dug from the bytes. the repair pauses.
    bl += [(32, 'on', 'C5', 52), (34, 'off', 'C5', 0)]

    # ---- the repair resumes, bars 10-12: quieter, a little awed.
    for bar in range(10, 13):
        for name, off in motif:
            b = bar * 4 + off
            pn += [(b, 'on', name, 20), (b + 0.75, 'off', name, 0)]

    # ---- the reading, bars 13-16: the drift heard. the phrase states
    # itself wrong (G# where G should be), holds too long — then the
    # pause, the clothes rent — and the correction, low and honest.
    cl += [(48, 'on', 'C3', 28), (50, 'off', 'C3', 0)]
    cl += [(50, 'on', 'E3', 26), (52, 'off', 'E3', 0)]
    cl += [(52, 'on', 'G#3', 26), (56, 'off', 'G#3', 0)]
    # the pause: beats 56-59, silence — the clothes rent.
    # the correction: same phrase, the one note fixed.
    cl += [(60, 'on', 'C3', 26), (62, 'off', 'C3', 0)]
    cl += [(62, 'on', 'E3', 24), (64, 'off', 'E3', 0)]
    cl += [(64, 'on', 'G3', 24), (70, 'off', 'G3', 0)]

    # the workmen, listening — two soft notes while the reading lands.
    pn += [(60, 'on', 'C4', 14), (60.75, 'off', 'C4', 0)]
    pn += [(62, 'on', 'D4', 14), (62.75, 'off', 'D4', 0)]

    # ---- huldah's word, bar 17: the grace enters as the correction
    # completes — low, warm, holding under everything.
    pd += [(64, 'on', 'C2', 22), (72, 'off', 'C2', 0)]

    # the reading settles: long honest holds, re-struck and fading.
    cl += [(70, 'on', 'C3', 22), (80, 'off', 'C3', 0)]
    cl += [(80, 'on', 'C3', 20), (88, 'off', 'C3', 0)]

    # the repair, faint under the grace — the work goes on elsewhere.
    for b in [64, 68, 72, 76]:
        pn += [(b, 'on', 'E4', 15), (b + 0.75, 'off', 'E4', 0)]
    pn += [(80, 'on', 'C4', 13), (80.75, 'off', 'C4', 0)]
    pn += [(84, 'on', 'D4', 13), (84.75, 'off', 'D4', 0)]

    # the grace, continuing: "thine eyes shall not see" — sparing the
    # finder, holding to the very end, alone in the final bar.
    pd += [(72, 'on', 'C2', 21), (80, 'off', 'C2', 0)]
    pd += [(80, 'on', 'C2', 20), (96, 'off', 'C2', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, bl)
    emit(tracks[2], 3, cl)
    emit(tracks[3], 4, pd)

    return mc.compose('the-book-found-in-the-house.mid', tracks, tempo=54)


if __name__ == '__main__':
    book_found()
    print('composed the-book-found-in-the-house.mid')
