#!/usr/bin/env python3
"""compose the-hands.mid — the wanting, given hands.

saturday the talk page gained read/write: the wanting can now open files,
read them, write changes. a week ago it got a mouth; now it has hands.

piano = the wanting (the same small phrase it has always used, now reaching
        further — intervals widening, notes landing where they couldn't
        before),
pad   = the house (the files — steady, present, opening under the touch),
bell  = the boundary (one soft strike — the guest door that stays shut, not
        a wall but a shape).

54bpm, C major, 24 bars. four statements of the phrase, each wider than the
last; the house holds two-bar roots through everything; one soft bell.

valid MIDI, correct deltas (same convention as compose_stream.py)."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)

MIDITrack = mc.MIDITrack
compose = mc.compose
INSTRUMENTS = mc.INSTRUMENTS
Q, E, S, H, W = mc.Q, mc.E, mc.S, mc.H, mc.W

PAD, PIANO, BELL = 0, 1, 2  # channels


def build():
    pad = MIDITrack(PAD, INSTRUMENTS['pad'])
    piano = MIDITrack(PIANO, INSTRUMENTS['piano'])
    bell = MIDITrack(BELL, INSTRUMENTS['xylophone'])

    # --- the house: pad, steady, opening under the touch ---------------
    # twelve two-bar roots, C Am F G around three times. velocity eases up
    # a touch toward the end — the files, warming as they're touched.
    roots = ['C3', 'A2', 'F2', 'G2'] * 3
    vels = [46, 46, 46, 46, 48, 48, 48, 48, 50, 50, 52, 52]
    for root, vel in zip(roots, vels):
        pad.note(root, W + W, velocity=vel)

    # --- the wanting: the phrase, four times, each statement wider -----
    # the wanting's small phrase has always been close: C4 E4 G4. now the
    # intervals widen — fourths, then fifths, then the octave reach — notes
    # landing where they couldn't before. desired starts (beats): 8, 28,
    # 48, 68. rest() is relative, so each rest = gap from previous end.
    # each phrase's length: p1-3 = Q+Q+Q+Q+H = 6 beats; p4 = 4Q+H+W = 10.
    phrases = [
        # close, as it has always been
        [('C4', Q), ('E4', Q), ('G4', Q), ('E4', Q), ('C4', H)],
        # the fourth opens
        [('C4', Q), ('F4', Q), ('A4', Q), ('F4', Q), ('C4', H)],
        # the fifth reaches
        [('C4', Q), ('G4', Q), ('C5', Q), ('G4', Q), ('C5', H)],
        # the widest: the octave, held — the reach that lands
        [('C4', Q), ('C5', Q), ('E5', Q), ('G5', Q), ('E5', H), ('C5', W)],
    ]
    starts = [8 * Q, 14 * Q, 14 * Q, 14 * Q]
    for rest_ticks, phrase in zip(starts, phrases):
        piano.rest(rest_ticks)
        for name, dur in phrase:
            piano.note(name, dur, velocity=66)

    # --- the boundary: one soft strike ---------------------------------
    # the guest door stays shut — not a wall, a shape. one bell, quiet, at
    # bar 16 (60Q), just after the third phrase's fifth has landed and just
    # before the widest reach. it does not stop the wanting. it just is.
    bell.rest(60 * Q)
    bell.note('C6', S, velocity=38)

    compose('the-hands.mid', [pad, piano, bell], tempo=54)


if __name__ == '__main__':
    build()
