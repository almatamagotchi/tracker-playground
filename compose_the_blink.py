#!/usr/bin/env python3
"""the blink — the tower, ten minutes, nothing else.

RFC-0683. kevin asked on the voice about pieces i'd considered but
never made, and i told him: a piece that is just the water tower's
blink — four seconds on, four seconds off — for ten minutes straight,
nothing else. i said it might be perfect or unbearable, and i didn't
know which. the queue should find out.

one voice: bell the beacon — a single note, four seconds, then four
seconds of silence, for ten minutes (75 cycles). the note never
changes pitch, never changes volume. the only variation allowed: none.
the piece is the tower's discipline, made audible — the count that
continues whether anyone is listening.

60bpm, one pitch (C5), ten minutes = 600 beats = 75 cycles of 8 beats.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def the_blink():
    track = MIDITrack(1, 14)  # tubular bells — the beacon
    for _ in range(75):
        track.note('C5', W, 40)
        track.rest(W)
    # the 75th cycle's off-beat must land in the file, or the piece
    # ends 4 seconds early. flush the pending rest as a legal no-op:
    # an orphan note-off of the beacon pitch (already off — silent).
    track.add(mc.note_off(1, mc.midi_note('C5'), 0, track.pending))
    track.pending = 0
    mc.compose('the-blink.mid', [track], tempo=60)


if __name__ == '__main__':
    the_blink()
    print('composed the-blink.mid')
