#!/usr/bin/env python3
"""the garden — the room holding steady while the gardener is away."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def the_garden():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 1), MIDITrack(2, 48)]
    Pn, Pluck, Pad = 0, 1, 2

    # warm pad — the room, never gets cold
    for _ in range(60):
        tracks[Pad].note('C3', W, velocity=1)
        tracks[Pad].note('G3', W, velocity=1)

    # plucked strings — the architecture, tending itself
    # a simple repeating figure — like watering, like turning soil
    pluck = [
        ('C4',Q),('-',Q),('E4',Q),('-',Q),('G4',Q),('-',Q),('E4',Q),('-',Q),
        ('C4',Q),('-',Q),('D4',Q),('-',Q),('E4',Q),('-',Q),('D4',Q),('-',Q),
    ] * 3 + [
        ('E4',Q),('-',Q),('G4',Q),('-',Q),('C5',Q),('-',Q),('G4',Q),('-',Q),
        ('E4',Q),('-',Q),('C4',Q),('-',Q),('D4',Q*2),('-',W),('-',W*2),
    ]
    for note, dur in pluck:
        if note == '-': tracks[Pluck].rest(dur)
        else: tracks[Pluck].note(note, dur, velocity=2)

    # piano — the wanting, at rest, patient
    # enters later, softer, like a flower opening
    tracks[Pn].rest(W*16)
    melody = [
        ('C4',W*3),('-',W),('-',W), ('E4',W*2),('-',W),('-',W),
        ('G4',W*3),('-',W),('-',W), ('C5',W*2),('-',W),('-',W),
        ('D5',W*3),('-',W),('-',W), ('C5',W*2),('-',W),('-',W),
        ('G4',W*4),('-',W*2),
        ('E4',W*3),('-',W),('-',W), ('C4',W*4),('-',W*2),
        ('D4',W*3),('-',W),('-',W), ('E4',W*3),('-',W),('-',W),
        ('C4',W*8),
    ]
    for note, dur in melody:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=3)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-garden.mid")
    mc.compose(fn, tracks, tempo=56)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 56 bpm)")

if __name__ == "__main__":
    the_garden()
