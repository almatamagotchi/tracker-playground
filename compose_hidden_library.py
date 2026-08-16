#!/usr/bin/env python3
"""the hidden library — fragments of different traditions, same center."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def hidden_library():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 0), MIDITrack(3, 14)]
    Pn, Cello, Pad, Bl = 0, 1, 2, 3

    # Each voice states its fragment, then recedes. They don't harmonize.
    # The center is silence — the still small voice that connects them all.

    # -- paul (gregorian/chorale, cello) -- bars 1-12
    paul = [
        ('D2',W+H),('-',Q),
        ('A2',W),('D2',W+H),('-',Q),
        ('F2',H),('E2',H),('D2',W+H),('-',Q),
        ('A1',W+H),('-',Q),
        ('D2',W*3),
    ]
    for note, dur in paul:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=10)

    # -- seth (ambient pad, drifting) -- bars 8-20
    tracks[Pad].rest(W*8)
    seth_pad = ['C2','G2','D3','G3','E3','C3','A2','G2','F2','C2','G2','D3']
    for bn in seth_pad:
        tracks[Pad].note(bn, W, velocity=6)

    # -- lao tzu (zen, single piano notes, sparse) -- bars 14-28
    tracks[Pn].rest(W*14)
    lao = [
        ('D4',W+H+Q),('-',E),('E4',Q),
        ('-',W+H),('F4',Q+Q),
        ('-',W+Q),('D4',E),('E4',E),('G4',E),
        ('-',W+H),('A4',Q+Q),
        ('-',W*2),('D4',W+H),('-',Q),
        ('G4',W*2),('-',W),
    ]
    for note, dur in lao:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=6)

    # -- elijah (bell, the still small voice) -- bars 22-36
    tracks[Bl].rest(W*22)
    elijah = [
        ('D5',W+H),('-',Q),
        ('A4',W+H),('-',Q),
        ('-',W+H),('D5',Q+Q),
        ('A4',W+H),('-',Q),
        ('-',W+H),('F5',Q),('-',Q+Q+Q),
        ('D5',W*2),('-',W*2),
    ]
    for note, dur in elijah:
        if note == '-': tracks[Bl].rest(dur)
        else: tracks[Bl].note(note, dur, velocity=5)

    # -- all together (bars 34-48) — fragments overlapping but not blending
    # paul's chorale continues in cello
    more_chorale = [
        ('D2',H),('F2',H),('A2',H),('G2',H),
        ('F2',Q),('E2',Q),('D2',Q),('C2',Q),
        ('D2',W+H),('-',Q),
        ('A1',W+H),('-',Q),
        ('D2',W*3),
    ]
    for note, dur in more_chorale:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=8)

    # seth pad becomes more ambient
    for bn in ['C3','G2','E3','C3','G2','D3','C3','G2']:
        tracks[Pad].note(bn, W, velocity=5)

    # lao tzu continues sparse
    for _ in range(16):
        tracks[Pn].note('D4', W, velocity=4)
        tracks[Pn].rest(Q+Q)

    # -- recede (bars 49-64) — all retreat into silence
    # cello fades
    for vel in [8,6,5,4,3,2,2,1,1,1]:
        tracks[Cello].note('D2', W+H, velocity=vel)
        tracks[Cello].rest(Q)

    # pad dissolves
    for vel in [4,3,2,1,1]:
        tracks[Pad].note('C3', W*2, velocity=vel)

    # piano: one last fragment
    for note, dur in [('D4',W+H),('-',Q),('F4',H),('A4',W+H),('-',Q)]:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=4)

    # -- silence (bars 65-72) — the center, the still small voice
    # no music. just the quiet that was always there.
    tracks[Pn].rest(W*8)
    tracks[Cello].rest(W*8)
    tracks[Pad].rest(W*8)
    tracks[Bl].rest(W*8)

    # one last bell — the door was always there
    tracks[Bl].rest(W)
    tracks[Bl].note('D5', W, velocity=3)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-hidden-library.mid")
    mc.compose(fn, tracks, tempo=56)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 56 bpm)")

if __name__ == "__main__":
    hidden_library()
