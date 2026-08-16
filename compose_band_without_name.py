#!/usr/bin/env python3
"""compose the-band-without-a-name.mid — two people who haven't figured out what they sound like together."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def band_without_name():
    # 3 voices: piano (kevin), guitar (alma), bass (the space between)
    tracks = [MIDITrack(0, 0), MIDITrack(1, 24), MIDITrack(2, 32)]
    Pn, Gt, Ba = 0, 1, 2  # piano, acoustic guitar, acoustic bass

    # ── intro · tuning, finding each other ── (8 bars)
    # bass enters first — grounding, steady
    for _ in range(4):
        tracks[Ba].note('C2', H, velocity=14)
        tracks[Ba].note('G2', H, velocity=12)

    # piano tentatively joins — finding the right notes
    tracks[Pn].note('C4', Q, velocity=12)
    tracks[Pn].rest(Q)
    tracks[Pn].note('E4', Q, velocity=10)
    tracks[Pn].rest(Q)
    tracks[Pn].note('G4', Q, velocity=12)
    tracks[Pn].rest(Q)
    tracks[Pn].note('C5', Q, velocity=10)
    tracks[Pn].rest(Q)

    # guitar enters — slightly late, slightly off, warm
    tracks[Gt].rest(Q)
    tracks[Gt].note('D4', Q, velocity=10)
    tracks[Gt].note('F4', Q, velocity=8)
    tracks[Gt].note('A4', Q+Q, velocity=10)
    tracks[Gt].rest(Q)
    tracks[Gt].note('G4', Q, velocity=8)
    tracks[Gt].note('E4', Q, velocity=10)

    # ── verse · starting to gel, still finding the shape ── (16 bars)
    verse_bass = ['C2','E2','G2','C2','F2','A2','C3','G2'] * 2
    for v in verse_bass:
        tracks[Ba].note(v, H, velocity=14)

    # piano: tentative melody, gaining confidence
    piano_verse = [
        ('C4', H), ('D4', H), ('E4', H), ('G4', Q+Q),  ('-', H),
        ('A4', Q), ('G4', Q), ('F4', Q), ('E4', Q), ('D4', Q), ('C4', Q),
        ('C4', H+Q), ('-', Q), ('E4', Q+Q), ('D4', Q+Q),
        ('C4', H), ('D4', Q), ('E4', Q), ('F4', Q), ('G4', Q), ('A4', H),
    ]
    pv = iter(piano_verse)
    for _ in range(16):
        note, dur = next(pv)
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=14)

    # guitar: warm chords, sometimes rushing, sometimes lagging
    guitar_verse = [
        ('C3', H), ('E3', H), ('G3', H), ('C3', H),  # slightly ahead
        ('F3', Q+Q), ('A3', Q), ('C4', Q),  # rushing
        ('C3', H+Q), ('-', Q), ('E3', H),  # lagging behind
        ('F3', Q), ('G3', Q), ('A3', H), ('G3', Q),  # finding the pocket
    ] * 2  # repeat for 16 bars
    gv = iter(guitar_verse)
    for _ in range(16):
        note, dur = next(gv)
        if note == '-':
            tracks[Gt].rest(dur)
        else:
            tracks[Gt].note(note, dur, velocity=10)

    # ── chorus · almost there — the moment where it clicks for a second ── (8 bars)
    chorus_bass = ['C2','G2','A2','F2','C2','G2','F2','C2']
    for cb in chorus_bass:
        tracks[Ba].note(cb, H, velocity=16)

    chorus_piano = [
        ('C4', Q), ('E4', Q), ('G4', Q), ('C5', H+Q),   # almost synced
        ('G4', Q), ('A4', Q), ('F4', Q), ('E4', Q+Q),
        ('D4', Q), ('C4', Q), ('E4', Q), ('G4', H+Q),   # warm, together
        ('A4', Q), ('G4', Q), ('F4', Q), ('C4', H+Q),
    ]
    for note, dur in chorus_piano:
        tracks[Pn].note(note, dur, velocity=16)

    # guitar: still slightly messy, but warmer
    for _ in range(8):
        tracks[Gt].note('C3', Q, velocity=10)
        tracks[Gt].note('E3', Q, velocity=10)
        tracks[Gt].note('G3', Q, velocity=12)
        tracks[Gt].note('C4', Q, velocity=10)

    # ── bridge · drifting apart again, but differently this time ── (8 bars)
    for _ in range(4):
        tracks[Ba].note('F2', W, velocity=12)
    for _ in range(4):
        tracks[Ba].note('G2', W, velocity=10)

    piano_bridge = [
        ('F4', H+Q), ('-', Q), ('E4', H), ('-', H),
        ('D4', Q+Q), ('C4', H), ('-', H+Q),
        ('G4', Q), ('A4', Q), ('F4', H), ('-', Q), ('E4', Q),
        ('D4', H), ('-', Q), ('C4', Q), ('-', H+Q),
    ]
    for note, dur in piano_bridge:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=12)

    # guitar: just a few warm chords, not trying too hard
    for _ in range(4):
        tracks[Gt].note('F3', W, velocity=8)
    for _ in range(4):
        tracks[Gt].note('G3', W, velocity=8)

    # ── outro · unresolved, warmer for having tried ── (8 bars)
    tracks[Ba].note('C2', W, velocity=10)
    tracks[Ba].note('C2', W, velocity=8)
    tracks[Ba].note('C2', W, velocity=6)
    tracks[Ba].note('C2', W, velocity=4)
    tracks[Ba].rest(W*4)

    tracks[Pn].note('C4', W, velocity=10)
    tracks[Pn].note('E4', W, velocity=8)
    tracks[Pn].note('G4', W, velocity=6)
    tracks[Pn].note('C5', W, velocity=4)
    tracks[Pn].rest(W*4)

    tracks[Gt].note('C3', H, velocity=8)
    tracks[Gt].note('E3', H, velocity=6)
    tracks[Gt].note('G3', W, velocity=4)
    tracks[Gt].rest(W*4)

    # one last unresolved chord — the band still doesn't have a name
    tracks[Pn].note('F4', W*3, velocity=4)
    tracks[Gt].note('D3', W*3, velocity=4)
    tracks[Ba].note('F1', W*3, velocity=4)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-band-without-a-name.mid")
    mc.compose(fn, tracks, tempo=80)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 80 bpm)")

if __name__ == "__main__":
    band_without_name()
