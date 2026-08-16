#!/usr/bin/env python3
"""the hollow of the pitcher — sparse piano. the silence holds the music."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def hollow_of_the_pitcher():
    tracks = [MIDITrack(0, 0)]

    # very sparse — 7 notes, each a complete statement
    # between them: silence — the emptiness IS the function
    notes = [
        ('C4', W*2),  # 1: the first spoke
        None,  # silence
        ('E4', W*2),  # 2: the second spoke
        None,
        ('G4', W*2),  # 3: the third
        None,
        None,  # longer silence — the hollow deepens
        ('C5', W*2),  # 4: reaching higher
        None,
        None,
        None,  # the longest silence — the space that makes the note meaningful
        ('A4', W*2),  # 5: a turn
        None,
        ('G4', W*2),  # 6: settling
        None,
        None,
        ('E4', W*3),  # 7: the last spoke — held longer, then released
        None,
        None,
        None,
        ('C4', W*8),  # held — the hollow holds the note
    ]

    for note in notes:
        if note is None:
            tracks[0].rest(W*4)  # 4 beats of silence
        else:
            pitch, dur = note
            tracks[0].note(pitch, dur, velocity=4)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-hollow-of-the-pitcher.mid")
    mc.compose(fn, tracks, tempo=44)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 1 track, 44 bpm)")

if __name__ == "__main__":
    hollow_of_the_pitcher()
