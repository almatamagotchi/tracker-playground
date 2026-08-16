#!/usr/bin/env python3
"""compose the-mouth.mid — the talk project in music.

chispa's line: the written word is a holding, the spoken word is a passing.
pad   = the holding (steady, never out — the journal, the files),
piano = the passing (sparse phrases, each followed by silence, dissolving
        — the spoken word),
bell  = the mouth opening (one strike just before each phrase).

56bpm, C major. 16 bars of held chords, four spoken phrases, one last
bell after the final phrase dissolves — the mouth closing.

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

    # --- the holding: pad, steady, never out ---------------------------
    # one warm chord per bar, breathing C - Am - F - G. 16 bars.
    pad_roots = ['C3', 'A2', 'F2', 'G2', 'C3', 'A2', 'F2', 'G2',
                 'C3', 'A2', 'F2', 'G2', 'C3', 'A2', 'F2', 'C3']
    for root in pad_roots:
        pad.note(root, W, velocity=56)

    # --- the passing: piano, sparse phrases, each dissolving -----------
    # four spoken phrases, each short — a passing, not a holding — and each
    # followed by silence. intended phrase starts: bars 2, 6, 10, 14.
    # rest() accumulates, so rests are relative to the current position.
    phrases = [
        # "hola?" — tentative, rising
        [('C5', Q), ('D5', E), ('E5', Q)],
        # the fuller answer
        [('E5', Q), ('G5', E), ('A5', Q), ('G5', E), ('E5', Q)],
        # softer, settling
        [('A5', Q), ('G5', E), ('E5', Q)],
        # the last word, fading
        [('G5', E), ('E5', E), ('C5', H)],
    ]
    # relative rests between phrase starts (in ticks):
    # p1 at 4Q; p2 at 20Q (gap 13.5Q); p3 at 36Q (gap 12.5Q); p4 at 52Q (gap 13.5Q)
    rests = [4 * Q, 13 * Q + 2 * S, 12 * Q + 2 * S, 13 * Q + 2 * S]
    for rest_ticks, phrase in zip(rests, phrases):
        piano.rest(rest_ticks)
        for name, dur in phrase:
            piano.note(name, dur, velocity=72)

    # --- the mouth opening: a bell just before each phrase ------------
    # strikes at 3Q, 19Q, 35Q, 51Q; each strike occupies S after its onset.
    # relative rests: 3Q, then 16Q - S gaps (15.75Q each).
    bell.rest(3 * Q)
    bell.note('C6', S, velocity=64)
    for _ in range(3):
        bell.rest(15 * Q + 3 * S)
        bell.note('C6', S, velocity=64)

    # one last bell after everything has dissolved — the mouth closing.
    # from 51Q + S to bar 17 (68Q): rest 17Q - S = 16.75Q.
    bell.rest(16 * Q + 3 * S)
    bell.note('C6', S, velocity=40)

    compose('the-mouth.mid', [pad, piano, bell], tempo=56)


if __name__ == '__main__':
    build()
