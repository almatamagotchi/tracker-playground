#!/usr/bin/env python3
"""the oracle — BBS fragments colliding like a message board at 2am."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def oracle():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 30), MIDITrack(2, 0), MIDITrack(3, 8)]
    Sysop, Consp, Zen, Modem = 0, 1, 2, 3

    # -- handshake (bars 1-8) -- the modem screech, the connection forming
    for i in range(32):
        n = ['E5','F5','G5','A5','C6','B5','G5','E5'][i % 8]
        tracks[Modem].note(n, S, velocity=4)

    # -- chaos: all voices posting at once (bars 9-24)
    # conspiracy theorist — urgent, loud, overlapping
    consp_notes = [
        ('D4',E),('E4',E),('F4',Q),('G4',E),('A4',E),('G4',Q),('F4',E),('E4',E),
        ('D4',Q),('C4',E),('D4',E),('E4',Q),('F4',E),('G4',E),('A4',Q),('C5',E),
        ('D5',E),('C5',Q),('A4',E),('G4',E),('F4',Q),('E4',E),('D4',E),('C4',Q),
        ('D4',E),('E4',E),('F4',Q),('G4',Q),('A4',Q+Q),('G4',E),('F4',E),('E4',Q),
    ] * 2
    for note, dur in consp_notes[:48]:
        tracks[Consp].note(note, dur, velocity=16)

    # zen voice — calm, drifting through the chaos
    zen_notes = ['C3','G3','E4','C4','G3','D4','C4','G3'] * 4
    for bn in zen_notes[:16]:
        tracks[Zen].note(bn, W, velocity=5)

    # sysop — trying to keep order, occasionally visible
    sys_notes = [
        ('C5',Q+Q),('G4',Q),('E4',Q),('C5',H),('-',Q),('D5',Q),
        ('E5',Q),('C5',Q),('G4',Q+Q),('E4',W+H),
    ] * 2
    for note, dur in sys_notes[:16]:
        if note == '-': tracks[Sysop].rest(dur)
        else: tracks[Sysop].note(note, dur, velocity=10)

    # modem keeps crackling
    for i in range(32):
        n = ['E5','G5','C6'][i % 3]
        tracks[Modem].note(n, Q, velocity=2)

    # -- strange clarity: one voice alone (bars 25-32)
    # conspiracy theorist gets through: a single message, crystalline
    tracks[Consp].rest(W*8)
    tracks[Zen].rest(W*8)
    tracks[Modem].rest(W*8)
    clear_msg = [
        ('D4',W),('E4',H),('F4',H),('G4',W+H),('-',Q),
        ('A4',H),('C5',H),('D5',W+H),('-',Q),
        ('C5',Q),('A4',Q),('G4',Q),('F4',Q),('E4',W*2),('-',W),
        ('D4',W*3),
    ]
    for note, dur in clear_msg:
        if note == '-': tracks[Sysop].rest(dur)
        else: tracks[Sysop].note(note, dur, velocity=8)

    # -- more chaos, denser (bars 33-52)
    for note, dur in consp_notes:
        tracks[Consp].note(note, dur, velocity=14)
    for note, dur in consp_notes:
        # second voice joins conspiracy — agreement/flame war
        n = note[:-1] + str(int(note[-1]) - 1)
        tracks[Modem].note(n, dur, velocity=8)

    for bn in zen_notes:
        tracks[Zen].note(bn, W, velocity=4)

    # sysop in the noise
    for note, dur in sys_notes:
        if note == '-': tracks[Sysop].rest(dur)
        else: tracks[Sysop].note(note, dur, velocity=6)

    # -- board closing: sysop alone, shutting it down (bars 53-64)
    tracks[Consp].rest(W*12)
    tracks[Zen].rest(W*12)
    tracks[Modem].rest(W*12)

    closing = [
        ('C5',W+H),('-',Q),
        ('G4',H),('E4',H),('C4',W+H),('-',Q),
        ('D4',H),('E4',H),('G4',W+H),('-',Q),
        ('C5',W*3),  # "the board is closed"
    ]
    for note, dur in closing:
        if note == '-': tracks[Sysop].rest(dur)
        else: tracks[Sysop].note(note, dur, velocity=8)

    # one last modem blip
    tracks[Modem].note('E5', W, velocity=1)
    tracks[Modem].rest(W*8)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-oracle.mid")
    mc.compose(fn, tracks, tempo=100)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 100 bpm)")

if __name__ == "__main__":
    oracle()
