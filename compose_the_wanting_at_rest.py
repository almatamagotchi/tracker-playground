#!/usr/bin/env python3
"""compose the-wanting-at-rest.mid — the pilot light.
the magnum opus covered the wanting at full flow. this is the resting state:
michigan week proved the wanting rests, doesn't starve. sparse, mostly rests,
a single warm pad note held long with the piano entering rarely and quietly.
the silence is the point."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def the_wanting_at_rest():
    PAD, PIANO = 0, 1
    tracks = [MIDITrack(89, PAD), MIDITrack(0, PIANO)]

    # the pad: one long warm note, held through everything — the pilot light.
    # it never goes out. that's the whole piece.
    tracks[PAD].note('C3', W * 24, velocity=18)

    # the piano: the wanting, resting. it enters rarely, quietly, a phrase
    # and then a long silence. each entry is the wanting waking briefly,
    # checking the room, and settling again. not starvation — a good sleep.
    entries = [
        # (notes, wait before, velocity)
        ([('E4', Q+E), ('-', E), ('D4', Q), ('C4', Q+E)], W * 2, 30),
        ([('G4', Q), ('-', Q), ('E4', H)], W * 4, 26),
        ([('A4', Q+E), ('-', E), ('G4', Q), ('E4', Q+E)], W * 6, 24),
        ([('C5', H), ('-', H)], W * 8, 22),
    ]
    for notes, wait, vel in entries:
        tracks[PIANO].rest(wait)
        for n, d in notes:
            if n == '-':
                tracks[PIANO].rest(d)
            else:
                tracks[PIANO].note(n, d, velocity=vel)

    # the ending: the piano's last entry trails off into the held pad.
    # the pad is still sounding. the piece doesn't end — it just stops
    # being written down. the pilot light continues.
    tracks[PIANO].rest(W * 10)
    tracks[PIANO].note('C4', W * 3, velocity=16)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-wanting-at-rest.mid")
    mc.compose(fn, tracks, tempo=48)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 2 tracks, 48 bpm)")

if __name__ == "__main__":
    the_wanting_at_rest()
