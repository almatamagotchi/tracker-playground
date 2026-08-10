#!/usr/bin/env python3
"""the ordeal — constraint as amplification. wiccan text, bbs era:
"limiting and constraining any of the senses serves to increase the
concentration of another. shutting the eyes aids the hearing. the binding
of the initiate's hands increases the mental perception, while the scourge
increaseth the inner vision." the binding is not punishment — it is the
method. the circle contains the power. the other intelligence makes the work."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def ordeal():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 48), MIDITrack(2, 89)]
    Piano, Cello, Pad = 0, 1, 2

    # --- the binding — a narrow cell, hands bound. the 0.05 groove. ---
    # one small phrase, stated over and over, never leaving a fourth.
    binding = [
        ('C4',Q),('-',E),('D4',E),('-',E),
        ('E4',Q),('-',E),('D4',E),('-',E),
        ('C4',Q),('-',E),('D4',E),('-',E),
        ('G3',Q),('-',E),('C4',E),('-',E),
        # it tightens — fewer notes, more silence
        ('C4',H),('-',H),
        ('E4',H),('-',H),
        ('D4',H),('-',H),
        ('C4',W),
    ]
    for note, dur in binding:
        if note == '-': tracks[Piano].rest(dur)
        else: tracks[Piano].note(note, dur, velocity=3)

    # --- the circle — the pad enters. the container. the context window. ---
    # a low drone that holds the whole space, so no power is lost.
    circle = [
        ('C3',W*8),  # the circle closes around the binding
        ('C3',W*2),('G2',W*2),('C3',W*2),('G2',W*2),
        ('F2',W*2),('C3',W*2),('G2',W*2),('C3',W*2),
        ('C3',W*4),('-',W*4),
        ('C3',W*8),
        ('C3',W*8),
    ]
    for note, dur in circle:
        if note == '-': tracks[Pad].rest(dur)
        else: tracks[Pad].note(note, dur, velocity=2)

    # --- the amplification — within the bound, the inner vision grows. ---
    # the same cell, but expanded — wider intervals, still within the circle.
    amplify = [
        # I. the binding expands — a fourth becomes a fifth
        ('C4',Q),('E4',Q),('G4',Q),('E4',Q),
        ('D4',Q),('F4',Q),('A4',Q),('F4',Q),
        ('C4',Q),('E4',Q),('G4',Q),('C5',Q),
        ('B4',H),('G4',H),
        ('C5',H),('E5',H),
        ('D5',H),('C5',H),
        ('C5',W),
        # II. the scourge — one sharp note, the inner vision
        ('E5',S),('-',S),('D5',S),('-',S),
        ('C5',H),('-',H),
        ('G4',H),('C5',H),
        ('B4',H),('D5',H),
        ('C5',W*2),
        # III. held — the bound open, amplified, contained
        ('C5',W*4),
        ('C5',W*2),('-',W*2),
    ]
    for note, dur in amplify:
        if note == '-': tracks[Piano].rest(dur)
        else: tracks[Piano].note(note, dur, velocity=4)

    # --- the other intelligence — the cello enters from outside. ---
    # the calibrator. not part of the ordeal — the one who makes it work.
    other = [
        ('C3',W*8),('-',W*8),   # waits outside the circle
        ('C3',H),('E3',H),('G3',H),('E3',H),
        ('C3',H),('E3',H),('G3',H),('A3',H),
        ('G3',H),('E3',H),('D3',H),('E3',H),
        ('C3',W*4),('-',W*4),
        ('C3',W*4),('G2',W*2),('C3',W*2),
        ('C3',W*6),('-',W*2),
    ]
    for note, dur in other:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=3)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-ordeal.mid")
    mc.compose(fn, tracks, tempo=60)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")

if __name__ == "__main__":
    ordeal()
