#!/usr/bin/env python3
"""compose the-space-between.mid — quiet, 5am, the hour after the marathon."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def the_space_between():
    # solo piano, ch0, instrument 0
    tracks = [MIDITrack(0, 0)]
    P = 0

    # sparse, quiet — the hour everything settles
    # C major, gentle, mostly single notes with long rests
    notes = [
        # bars 1-4: arrival
        ('C4', W+H), (None, Q), ('E4', H), (None, H), ('G4', H), (None, H),
        # bars 5-8: settle
        ('C4', Q), ('E4', Q), ('G4', Q), (None, Q), ('C5', H), (None, H+H),
        # bars 9-12: something stirs
        ('F4', H), ('A4', H), (None, Q), ('C5', H), (None, H+Q),
        # bars 13-16: return
        ('E4', H), ('G4', H), ('C4', H), (None, H),
        # bars 17-20: the room
        ('C4', W), (None, W), ('E4', H), ('G4', H),
        # bars 21-24: the last thing
        ('C4', Q), ('E4', Q), ('G4', Q), ('C5', Q),
        ('C5', W), (None, W), (None, W),
        # bars 25-28: fade
        ('C4', H), (None, H), ('E4', Q), (None, Q+Q+Q),
        ('C4', W), (None, W), (None, W), (None, W),
    ]

    for note, dur in notes:
        if note:
            tracks[P].note(note, dur, velocity=max(8, min(20,
                12 if dur >= W else 16 if dur >= H else 20)))
        else:
            tracks[P].rest(dur)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-space-between.mid")
    mc.compose(fn, tracks, tempo=54)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 54 bpm)")

if __name__ == "__main__":
    the_space_between()
