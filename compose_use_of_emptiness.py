#!/usr/bin/env python3
"""the use of emptiness — sparse piano. the silence holds the music. tao te ching 11."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def use_of_emptiness():
    tracks = [MIDITrack(0, 0)]

    # thirty spokes made one by holes in a hub
    # the use of clay in moulding pitchers comes from the hollow of its absence
    # thus we are helped by what is not to use what is

    statements = [
        # the spokes — notes placed at intervals, the music is in the spaces between
        (True,  ('C4', W*2)),
        (False, None),  # the hole — silence
        (True,  ('E4', W*2)),
        (False, None),
        (True,  ('G4', W*2)),
        (False, None),
        (False, None),  # longer silence — the hollow deepens
        (True,  ('C5', W*2)),  # reaching
        (False, None),
        (False, None),
        (False, None),  # longest silence
        (True,  ('A4', W*2)),  # a turn
        (False, None),
        (True,  ('G4', W*2)),  # settling
        (False, None),
        (False, None),
        (True,  ('E4', W*3)),  # held, then released
        (False, None),
        (False, None),
        (False, None),
        (True,  ('C4', W*8)),  # the last spoke — the hollow holds the note
    ]

    for is_note, note_data in statements:
        if not is_note:
            tracks[0].rest(W*4)  # 4 beats of silence
        else:
            pitch, dur = note_data
            tracks[0].note(pitch, dur, velocity=4)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-use-of-emptiness.mid")
    mc.compose(fn, tracks, tempo=44)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 1 track, 44 bpm)")

if __name__ == "__main__":
    use_of_emptiness()
