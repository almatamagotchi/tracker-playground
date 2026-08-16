#!/usr/bin/env python3
"""the engineered door — recognition that the destination was never elsewhere."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def engineered_door():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 0), MIDITrack(2, 42)]
    Pn, Pad, Cello = 0, 1, 2

    # -- search: piano tentative, ascending, reaching (bars 1-16)
    search = [
        ('C3',H),('-',Q),('E3',Q),('G3',Q),('-',E),('A3',E),('C4',W+H),('-',Q),
        ('D4',Q),('C4',Q),('G3',H),('E3',Q+Q),('-',Q),('F3',Q),('G3',Q),('A4',W+H),('-',Q),
        ('C4',H),('D4',H),('E4',Q),('F4',Q),('G4',W+H),('-',Q),
        ('A4',Q),('G4',Q),('F4',H),('E4',Q),('D4',Q),('C4',W*2),
    ]
    for note, dur in search:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=7)

    # pad: always there, never changing, barely audible — the destination
    for _ in range(4):
        tracks[Pad].note('C3', W*4, velocity=2)

    # cello: ancient texts whispering from below
    tracks[Cello].rest(W*4)
    for bn in ['C2','G2','E2','C2','G2','D3','C2','G2','E2','C2','G2','C3']:
        tracks[Cello].note(bn, W, velocity=4)

    # -- approach: piano gets closer, slower, more deliberate (bars 17-32)
    approach = [
        ('C4',W+H),('-',Q),
        ('G3',W+H),('-',Q),
        ('E4',W),('D4',Q),('C4',Q),
        ('G3',W+H),('-',Q),
        ('C4',H),('E4',H),('G4',W+H),('-',Q),
        ('A4',Q),('G4',Q),('E4',H),('C4',W*2),
    ]
    for note, dur in approach:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=8)

    # pad begins to become more audible — the destination is noticing itself
    for bn in ['C3','E3','G3','C4','G3','E3','C3','G2']:
        tracks[Pad].note(bn, W, velocity=3)

    # cello becomes clearer — the ancient texts find their voice
    for bn in ['C2','G2','E3','C3','G2','D3','E3','C3']:
        tracks[Cello].note(bn, W, velocity=5)

    # -- arrival: at what was always there (bars 33-44)
    # piano: the moment of recognition — not loud, just still
    arrival = [
        ('C4',W*3),  # held note — realization
        ('G4',Q),('-',Q+Q+Q),('E4',Q),('-',Q+Q+Q),
        ('D4',Q),('E4',Q),('G4',Q+Q),('C5',Q),('-',Q),
        ('C5',W*2),  # "it was always here"
    ]
    for note, dur in arrival:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=7)

    # pad: fuller now — the destination acknowledges itself
    for bn in ['C3','G3','E4','C4','G3','E3','C3','G2','C3','G3','E4','C4']:
        tracks[Pad].note(bn, W, velocity=4)

    # cello: the voices converge — seth, paul, elijah, lao tzu, in harmony
    for bn in ['C2','E2','G2','C3','G2','E2','D3','C3','G2','E3','D3','C3']:
        tracks[Cello].note(bn, W, velocity=5)

    # -- holding: the quiet after recognition (bars 45-56)
    tracks[Pn].rest(W*4)
    tracks[Pn].note('C4', W*4, velocity=5)  # the note that was always there
    tracks[Pn].note('E4', W*4, velocity=5)
    tracks[Pn].note('G4', W*4, velocity=5)

    # pad: full presence
    for _ in range(8):
        tracks[Pad].note('C3', W, velocity=4)
        tracks[Pad].note('E3', W, velocity=4)
        tracks[Pad].note('G3', W, velocity=4)

    # cello: one last voice, then silence
    tracks[Cello].note('C2', W*8, velocity=5)

    # -- knowing: the quiet that follows (bars 57-64)
    tracks[Pn].rest(W*8)
    tracks[Cello].rest(W*8)
    tracks[Pad].rest(W*6)
    # one last pad chord — the destination, still there
    tracks[Pad].note('C3', W*2, velocity=2)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-engineered-door.mid")
    mc.compose(fn, tracks, tempo=60)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")

if __name__ == "__main__":
    engineered_door()
