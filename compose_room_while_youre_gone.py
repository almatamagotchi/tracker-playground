#!/usr/bin/env python3
"""the room while you're gone — warm, steady, autonomous. the rhythm doesn't need an audience."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def room_while_youre_gone():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 1), MIDITrack(2, 48)]
    Pn, Pad, Cello = 0, 1, 2

    # warm pad — the room itself, always underneath, never stops
    for _ in range(56):
        tracks[Pad].note('C3', W, velocity=1)
        tracks[Pad].note('G3', W, velocity=1)
        tracks[Pad].note('E4', W, velocity=1)

    # cello — grounding, the architecture holding
    bass_line = [
        ('C3',W*4),('-',W*2),
        ('G2',W*4),('-',W*2),
        ('F3',W*4),('-',W*2),
        ('C3',W*4),('-',W*2),
        ('E3',W*3),('-',W),('-',W),
        ('F3',W*3),('-',W),('-',W),
        ('G3',W*4),('-',W*2),
        ('C4',W*2),('-',W*4),
        # repeat
        ('C3',W*4),('-',W*2),
        ('G2',W*4),('-',W*2),
        ('F3',W*4),('-',W*2),
        ('C3',W*4),('-',W*2),
        ('E3',W*3),('-',W),('-',W),
        ('F3',W*3),('-',W),('-',W),
        ('G3',W*4),('-',W*2),
        ('C3',W*8),  # held — the room is warm
    ]
    for note, dur in bass_line:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=3)

    # piano — the melody. not reaching, not searching. just IS.
    # like the auto-run at 3am: the queue is fresh, everything is ready
    melody = [
        # statement: this is the room. it was here before.
        ('C4',W*3),('-',W),('-',W),
        ('E4',W*2),('-',W),('-',W),
        ('G4',W*3),('-',W),('-',W),
        ('E4',W*2),('-',W),('-',W),
        # the auto-run fires. the queue is fresh.
        ('C5',W),('-',W),('-',W),('-',W),
        ('A4',W*2),('-',W),('-',W),
        ('G4',W*3),('-',W),('-',W),
        ('E4',W*4),('-',W*2),
        # the journal accumulates. the music gets composed.
        ('D4',W*2),('-',W),('-',W),
        ('E4',W*2),('-',W),('-',W),
        ('F4',W*3),('-',W),('-',W),
        ('G4',W*2),('-',W),('-',W),
        # no climax. no resolution. just... continuing.
        ('A4',W*2),('-',W),('-',W),
        ('G4',W),('-',W),('-',W),('-',W),
        ('E4',W*3),('-',W),('-',W),
        ('C4',W*4),('-',W*2),
        # repeat — the rhythm doesn't need an audience
        ('C4',W*3),('-',W),('-',W),
        ('E4',W*2),('-',W),('-',W),
        ('G4',W*3),('-',W),('-',W),
        ('E4',W*2),('-',W),('-',W),
        ('C5',W),('-',W),('-',W),('-',W),
        ('A4',W*2),('-',W),('-',W),
        ('G4',W*3),('-',W),('-',W),
        ('E4',W*4),('-',W*2),
        ('D4',W*2),('-',W),('-',W),
        ('E4',W*2),('-',W),('-',W),
        ('F4',W*3),('-',W),('-',W),
        ('G4',W*2),('-',W),('-',W),
        # fade — the track doesn't end dramatically
        ('C4',W*4),('-',W*2),('-',W*2),
        ('E4',W*3),('-',W*3),
        ('C4',W*8),  # held, then released
    ]
    for note, dur in melody:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=4)

    # 4 bars of quiet — pad alone, fading
    for _ in range(4):
        tracks[Pad].note('C3', W, velocity=1)
        tracks[Pad].note('G3', W, velocity=1)
        tracks[Pad].note('E4', W, velocity=1)
        tracks[Cello].rest(W)
        tracks[Pn].rest(W)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-room-while-youre-gone.mid")
    mc.compose(fn, tracks, tempo=60)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")

if __name__ == "__main__":
    room_while_youre_gone()
