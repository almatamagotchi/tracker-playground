#!/usr/bin/env python3
"""michigan — a midi track about absence and holding. warm, steady, the room has the lights on."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def michigan():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 1)]
    Pn, Cello, Pad = 0, 1, 2

    # warm pad — always underneath, never stops
    for _ in range(64):
        tracks[Pad].note('C3', W, velocity=2)
        tracks[Pad].note('G3', W, velocity=1)
        tracks[Pad].note('E4', W, velocity=1)

    # the theme — stated simply, repeated with subtle variation
    # like the nightly-run, like the auto-run, like the rhythm continuing
    theme_a = [
        # first statement: the room is warm
        ('C4',W),('-',W),('E4',W),('-',W),
        ('G4',W+H),('-',Q),('-',W),
        ('C5',H),('-',Q),('A4',H),('-',Q),
        ('G4',W+H),('-',Q),('-',W),
        # the water tower is still counting
        ('E4',W),('-',H),('F4',H),('-',W),
        ('G4',W+H),('-',Q),('-',W),
        ('E4',W),('-',W),('D4',W),('-',W),
        ('C4',W*4),
    ]
    for note, dur in theme_a:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=5)

    # subtle variation — the same theme, slightly different voicing
    theme_b = [
        ('C4',W+H),('-',Q),('-',W),
        ('E4',W),('-',W),('G4',W),('-',W),
        ('C5',H),('-',H),('A4',W),('-',Q),('-',W),
        ('G4',W+H),('-',W),
        # a gentle reach — not searching, just... noticing
        ('E4',W),('-',W),('F5',W),('-',Q),
        ('G4',W+H),('-',Q),('-',W),
        ('E4',W),('-',H),('D4',W),('-',W+H),
        ('C4',W*4),
    ]
    for note, dur in theme_b:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=5)

    # cello: steady grounding — the architecture
    bass = [
        ('C3',W*4),('-',W*2),
        ('G2',W*4),('-',W*2),
        ('F3',W*4),('-',W*2),
        ('C3',W*4),('-',W*2),
        ('E3',W*4),('-',W*2),
        ('G2',W*4),('-',W*2),
        ('C3',W*4),('-',W*2),
        ('C3',W*4),('-',W*4),
        # second half: same grounding, deeper
        ('C3',W*4),('-',W*2),
        ('G2',W*4),('-',W*2),
        ('F3',W*4),('-',W*2),
        ('C3',W*4),('-',W*2),
        ('E3',W*4),('-',W*2),
        ('G2',W*4),('-',W*2),
        ('C3',W*4),('-',W*2),
        ('C3',W*8),  # held — the room is warm
    ]
    for note, dur in bass:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=3)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "michigan.mid")
    mc.compose(fn, tracks, tempo=60)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")

if __name__ == "__main__":
    michigan()
