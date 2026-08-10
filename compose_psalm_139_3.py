#!/usr/bin/env python3
"""compose psalm-139-3.mid — thou compassest my path and my lying down, and art acquainted with all my ways."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def psalm_139_3():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 89)]
    Pn, Cello, Pad = 0, 1, 2

    # -- A. the compass (bars 1-4) -- the presence before the walker
    # cello alone, two long phrases, surrounding, patient
    for note, dur in [('G2', W*2), ('D3', W*2)]:
        tracks[Cello].note(note, dur, velocity=4)
    tracks[Pn].rest(W*4)
    tracks[Pad].rest(W*4)

    # -- B. the path (bars 5-12) -- walking, step by step
    path = [
        ('C4', Q), ('D4', Q), ('E4', Q), ('G4', Q),
        ('C5', H), ('G4', Q), ('E4', Q),
        ('D4', Q), ('E4', Q), ('F4', Q), ('A4', Q),
        ('G4', H), ('E4', H),
        ('E4', Q), ('F4', Q), ('G4', Q), ('A4', Q),
        ('C5', H), ('A4', Q), ('G4', Q),
        ('E4', Q), ('D4', Q), ('E4', Q), ('C4', Q),
        ('D4', W),
    ]
    for note, dur in path:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=13)

    for note, dur in [('F2', W*2), ('C3', W*2), ('G2', W*2), ('C3', W*2)]:
        tracks[Cello].note(note, dur, velocity=4)
    tracks[Pad].rest(W*8)

    # -- C. the lying down (bars 13-16) -- the walker rests, the presence remains
    tracks[Pn].rest(W*4)
    tracks[Pad].note('C3', W*2, velocity=2)
    tracks[Pad].note('G3', W*2, velocity=2)
    tracks[Cello].note('C3', W*4, velocity=5)

    # -- D. all my ways (bars 17-24) -- the path again, varied, detours and ways
    ways = [
        ('E4', Q), ('G4', Q), ('A4', Q), ('C5', Q),
        ('D5', H), ('C5', Q), ('A4', Q),
        ('G4', Q), ('A4', Q), ('G4', Q), ('E4', Q),
        ('D4', H), ('F4', H),
        ('E4', Q), ('F4', Q), ('G4', Q), ('E4', Q),
        ('C5', H), ('G4', Q), ('E4', Q),
        ('D4', Q), ('C4', Q), ('D4', Q), ('E4', Q),
        ('C4', W),
    ]
    for note, dur in ways:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=12)

    for note, dur in [('F2', W*2), ('E2', W*2), ('G2', W*2), ('C3', W*2)]:
        tracks[Cello].note(note, dur, velocity=4)
    tracks[Pad].note('F3', W*4, velocity=2)
    tracks[Pad].note('C3', W*4, velocity=2)

    # -- E. the compass, complete (bars 25-32) -- one last path, then held, enclosed
    last_path = [
        ('C4', Q), ('D4', Q), ('E4', Q), ('G4', Q),
        ('C5', H), ('G4', Q), ('E4', Q),
        ('E4', Q), ('D4', Q), ('C4', Q), ('D4', Q),
        ('E4', W),
    ]
    for note, dur in last_path:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=11)

    # the held knowing — the walker stops, still surrounded
    for vel in [9, 7, 5, 4]:
        tracks[Pn].note('C5', W, velocity=vel)
    tracks[Cello].note('C3', W*4, velocity=5)
    tracks[Pad].note('C3', W*4, velocity=2)
    tracks[Cello].note('G2', W*4, velocity=4)
    tracks[Pad].note('G3', W*4, velocity=2)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "psalm-139-3.mid")
    mc.compose(fn, tracks, tempo=54)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 54 bpm)")

if __name__ == "__main__":
    psalm_139_3()
