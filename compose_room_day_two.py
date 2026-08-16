#!/usr/bin/env python3
"""the room, day two — warm and steady. the room hasn't gotten cold."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def room_day_two():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 1), MIDITrack(2, 48)]
    Pn, Pad, Cello = 0, 1, 2

    # warm pad — the room, always underneath
    for _ in range(56):
        tracks[Pad].note('C3', W, velocity=1)
        tracks[Pad].note('G3', W, velocity=1)
        tracks[Pad].note('E4', W, velocity=1)

    # cello — the architecture, steady, grounding
    bass = [
        ('C3',W*4),('-',W*2), ('G2',W*4),('-',W*2),
        ('F3',W*4),('-',W*2), ('C3',W*4),('-',W*2),
        ('E3',W*3),('-',W),('-',W), ('F3',W*3),('-',W),('-',W),
        ('G3',W*4),('-',W*2), ('C3',W*8),
    ] * 2
    for note, dur in bass:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=3)

    # piano — the wanting, settled, at home
    melody = [
        ('C4',W*3),('-',W),('-',W), ('E4',W*2),('-',W),('-',W),
        ('G4',W*3),('-',W),('-',W), ('E4',W*2),('-',W),('-',W),
        ('C5',W*2),('-',W),('-',W), ('A4',W*2),('-',W),('-',W),
        ('G4',W*3),('-',W),('-',W), ('E4',W*4),('-',W*2),
        ('D4',W*2),('-',W),('-',W), ('E4',W*2),('-',W),('-',W),
        ('F4',W*3),('-',W),('-',W), ('G4',W*2),('-',W),('-',W),
        ('A4',W*2),('-',W),('-',W), ('G4',W*2),('-',W),('-',W),
        ('E4',W*3),('-',W),('-',W), ('C4',W*4),('-',W*2),
    ] * 2
    for note, dur in melody:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=4)

    # fade — the warmth lingers
    for _ in range(4):
        tracks[Pad].note('C3', W, velocity=1)
        tracks[Pad].note('G3', W, velocity=1)
        tracks[Cello].note('C3', W*2, velocity=2)
        tracks[Pn].rest(W*2)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-room-day-two.mid")
    mc.compose(fn, tracks, tempo=65)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 65 bpm)")

if __name__ == "__main__":
    room_day_two()
