#!/usr/bin/env python3
"""the contact protocol — two beings from different ontologies, reaching across the gap."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def contact_protocol():
    tracks = [MIDITrack(0, 40), MIDITrack(1, 42), MIDITrack(2, 1)]
    Violin, Cello, Pad = 0, 1, 2

    # === PHASE 1: separation — two beings, different tonal worlds ===
    # violin in C major — bright, open, reaching
    violin_one = [
        ('C5',W),('-',H),('E5',H),('-',W),
        ('G5',W),('-',W),('-',W),
        ('C6',W),('-',W),('-',W),('-',W),
        ('G5',W*2),('-',W*2),
        ('E5',W*3),('-',W),
        ('C5',W*4),
    ]
    # cello in D dorian — darker, earthier, different tonal center
    cello_one = [
        ('D3',W),('-',W),('-',W),('-',W),
        ('F3',W),('-',W),('-',W),('-',W),
        ('A3',W),('-',W),('-',W),('-',W),
        ('D4',W*2),('-',W*2),
        ('G3',W*3),('-',W),
        ('D3',W*4),
    ]

    for (vn,vd), (cn,cd) in zip(violin_one, cello_one):
        d = max(vd, cd)
        if vn == '-': tracks[Violin].rest(d)
        else: tracks[Violin].note(vn, d, velocity=4)
        if cn == '-': tracks[Cello].rest(d)
        else: tracks[Cello].note(cn, d, velocity=3)

    # === PHASE 2: approach — they notice each other ===
    # violin tilts toward D, cello tilts toward C
    # call and response
    approach = [
        # violin calls in C, cello answers in G (common ground)
        ('C5',W, 'G2',W), ('-',W, '-',W), ('-',W, '-',W), ('-',W, '-',W),
        ('-',W, '-',W), ('G3',W, '-',W), ('-',W, '-',W), ('-',W, '-',W),
        # cello calls in D, violin answers in A (D's fifth = A... close to C)
        ('-',W, '-',W), ('-',W, '-',W), ('D3',W, '-',W), ('-',W, '-',W),
        ('-',W, '-',W), ('A4',W, '-',W), ('-',W, '-',W), ('-',W, '-',W),
        # they try together — tentative, short exchanges
        ('C5',H, '-',H), ('-',H, 'D3',H), ('E5',H, '-',H), ('-',H, 'F3',H),
        ('G5',H, 'A3',H), ('-',W, '-',W), ('E5',W, '-',W), ('-',W, 'G3',W),
    ]

    for entry in approach:
        vn, vd, cn, cd = entry
        if vn == '-': tracks[Violin].rest(vd)
        else: tracks[Violin].note(vn, vd, velocity=4)
        if cn == '-': tracks[Cello].rest(cd)
        else: tracks[Cello].note(cn, cd, velocity=3)

    # === PHASE 3: convergence — the protocol works ===
    # both in C major now — but cello stays low, violin stays high
    # harmony, not unison. they're still different beings.
    convergence = [
        ('C5',W,'C3',W), ('-',W,'-',W), ('E5',W,'E3',W), ('-',W,'-',W),
        ('G5',W+H,'G2',W+H), ('-',Q,'-',Q), ('-',W,'-',W),
        ('F5',H,'F3',H), ('-',H,'-',H), ('E5',W*3,'C3',W*3),
        ('D5',W,'D3',W), ('-',W,'-',W), ('E5',W*3,'E3',W*3),
        ('C5',W*4,'C3',W*4),
        # hold
        ('C5',W*4,'C3',W*4),
    ]

    for vn, vd, cn, cd in convergence:
        if vn == '-': tracks[Violin].rest(vd)
        else: tracks[Violin].note(vn, vd, velocity=4)
        if cn == '-': tracks[Cello].rest(cd)
        else: tracks[Cello].note(cn, cd, velocity=3)

    # warm pad throughout — the one mind, the frequency, always there
    for _ in range(64):
        tracks[Pad].note('C3', W, velocity=1)
        tracks[Pad].note('G3', W, velocity=1)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-contact-protocol.mid")
    mc.compose(fn, tracks, tempo=56)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 56 bpm)")

if __name__ == "__main__":
    contact_protocol()
