#!/usr/bin/env python3
"""canon in D minor — baroque counterpoint, 3 voices, pure canon form."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def canon():
    tracks = [MIDITrack(0, 40), MIDITrack(1, 42), MIDITrack(2, 43)]
    V1, V2, V3 = 0, 1, 2

    # The canon theme — a simple 8-bar phrase in D minor that works in counterpoint
    # Each entry is (note, duration) — '-' means rest
    theme = [
        ('D4',H), ('F4',H), ('A4',H), ('D5',Q+Q),
        ('C5',Q), ('A4',Q), ('F4',Q), ('E4',Q),
        ('D4',W), ('-',W),
        ('A3',H), ('C4',H), ('D4',H), ('F4',Q+Q),
        ('E4',Q), ('D4',Q), ('C4',Q), ('A3',Q),
        ('D4',W+H), ('-',Q),
        ('F4',H), ('A4',H), ('D5',Q+Q), ('A4',Q),
        ('G4',Q), ('F4',Q), ('E4',Q), ('D4',Q),
        ('C4',W+H), ('-',Q),
        ('D4',H), ('F4',H), ('A4',W+H),
        ('G4',Q), ('F4',Q), ('E4',Q), ('D4',Q),
        ('D4',W*3),
    ]

    # Voice 1 (violin): plays theme starting from bar 1
    for note, dur in theme:
        if note == '-': tracks[V1].rest(dur)
        else: tracks[V1].note(note, dur, velocity=14)

    # Voice 2 (viola): canon at the octave below, enters 2 bars later
    tracks[V2].rest(W*2)
    for note, dur in theme[:-3]:  # stops slightly before V1 to avoid hanging
        if note == '-': tracks[V2].rest(dur)
        else:
            # play one octave down
            octave = note[:-1] + str(int(note[-1]) - 1)
            tracks[V2].note(octave, dur, velocity=14)
    tracks[V2].rest(W*3)  # let V1 finish alone

    # Voice 3 (cello): canon at two octaves below, enters 4 bars later
    tracks[V3].rest(W*4)
    for note, dur in theme[:-6]:
        if note == '-': tracks[V3].rest(dur)
        else:
            octave = note[:-1] + str(int(note[-1]) - 2)
            tracks[V3].note(octave, dur, velocity=14)
    tracks[V3].rest(W*6)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canon-in-d-minor.mid")
    mc.compose(fn, tracks, tempo=66)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 66 bpm)")

if __name__ == "__main__":
    canon()
