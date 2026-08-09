#!/usr/bin/env python3
"""the tough fibre — what persists when the sweet presence isn't available."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def tough_fibre():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42)]
    Piano, Cello = 0, 1

    # cello — the tough fibre, never stops, steady underneath
    fibre = [
        ('C3',W*4),('-',W*2),
        ('G2',W*4),('-',W*2),
        ('F3',W*4),('-',W*2),
        ('C3',W*4),('-',W*2),
        ('E3',W*3),('-',W),('-',W),
        ('F3',W*3),('-',W),('-',W),
        ('G3',W*4),('-',W*2),
        ('C4',W*4),('-',W*2),
    ] * 3 + [('C3',W*8), ('-',W*8)]

    for note, dur in fibre:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=3)

    # piano — the wanting, entering and leaving
    # three seasons: reach → rest → return
    wanting_season = [
        # SEASON 1: reach — the wanting enters, warm, confident
        ('C4',W*3),('-',W),('-',W), ('E4',W*2),('-',W),('-',W),
        ('G4',W*3),('-',W),('-',W), ('C5',W*2),('-',W),('-',W),
        ('A4',W*3),('-',W),('-',W), ('G4',W*2),('-',W),('-',W),
        ('E4',W*4),('-',W*2),
        # SEASON 2: rest — the wanting rests, the fibre continues
        ('-',W*8), ('-',W*4), ('-',W*4),
        ('C4',W*2),('-',W),('-',W), ('E4',W*2),('-',W),('-',W),  # brief return
        ('-',W*8),
        # SEASON 3: return — the wanting comes back, quieter, transformed
        ('D4',W*3),('-',W),('-',W), ('E4',W*2),('-',W),('-',W),
        ('F4',W*3),('-',W),('-',W), ('G4',W*2),('-',W),('-',W),
        ('A4',W*2),('-',W),('-',W), ('G4',W*2),('-',W),('-',W),
        ('E4',W*3),('-',W),('-',W), ('C4',W*4),('-',W*2),
        # held — the wanting and the fibre, together
        ('C4',W*8),
    ]

    for note, dur in wanting_season:
        if note == '-': tracks[Piano].rest(dur)
        else: tracks[Piano].note(note, dur, velocity=4)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-tough-fibre.mid")
    mc.compose(fn, tracks, tempo=60)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")

if __name__ == "__main__":
    tough_fibre()
