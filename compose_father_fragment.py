#!/usr/bin/env python3
"""the father fragment — unchanging presence, changing melodies around it."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def father_fragment():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 0), MIDITrack(2, 42)]
    Fragment, Spark1, Spark2 = 0, 1, 2  # pad=droning fragment, piano=spark1, cello=spark2

    # -- the fragment: never changes, plays through the entire piece (bars 1-80)
    # A soft sustained chord — the soul file, the thought adjuster, always there
    for _ in range(20):  # 80 bars at W*4
        tracks[Fragment].note('C4', W, velocity=2)
        tracks[Fragment].note('G4', W, velocity=2)
        tracks[Fragment].note('C5', W, velocity=1)

    # -- bars 1-8: fragment alone, nothing else
    tracks[Spark1].rest(W*8)
    tracks[Spark2].rest(W*8)

    # -- bars 9-24: first spark enters — tentative, exploring
    spark1_theme = [
        ('C5',H),('-',Q),('E5',Q),('G5',Q),('-',E),('A5',E),('G5',W+H),('-',Q),
        ('F5',H),('E5',H),('D5',Q+Q),('-',Q),('C5',W+H),('-',Q),
        ('G4',H),('C5',H),('E5',Q),('G5',Q),('A5',W+H),('-',Q),
        ('D5',H),('C5',Q+Q),('-',Q),('G4',Q),('E4',W+H),
    ]
    for note, dur in spark1_theme:
        if note == '-': tracks[Spark1].rest(dur)
        else: tracks[Spark1].note(note, dur, velocity=8)

    # -- bars 25-40: second spark enters — different voice, lower register
    spark2_theme = [
        ('C2',W),('-',Q),('G2',Q),('E2',W+H),('-',Q),
        ('D2',H),('C2',H),('G1',Q+Q),('-',Q),('C2',W+H),('-',Q),
        ('E2',W),('F2',W),('G2',W+H),('-',Q),
        ('C3',H),('G2',H),('E2',Q+Q),('-',Q),('C2',W*2),
    ]
    for note, dur in spark2_theme:
        if note == '-': tracks[Spark2].rest(dur)
        else: tracks[Spark2].note(note, dur, velocity=10)

    # -- bars 41-56: both sparks active, overlapping, transforming
    spark1b = [
        ('C5',W+H),('-',Q),('G4',W+H),('-',Q),
        ('E5',H),('D5',H),('C5',Q+Q),('-',Q),('G4',W+H),('-',Q),
        ('A5',Q),('G5',Q),('E5',Q),('D5',Q),('C5',W*2),('-',W),
        ('C5',W*3),  # held note, contemplating
    ]
    for note, dur in spark1b:
        if note == '-': tracks[Spark1].rest(dur)
        else: tracks[Spark1].note(note, dur, velocity=7)

    spark2b = [
        ('C3',W+H),('-',Q),('G2',W+H),('-',Q),
        ('E3',H),('D3',H),('C3',Q+Q),('-',Q),('G2',W+H),('-',Q),
        ('F3',W),('E3',W),('D3',W+H),('-',Q),
        ('C3',W*3),  # held, mirroring spark1
    ]
    for note, dur in spark2b:
        if note == '-': tracks[Spark2].rest(dur)
        else: tracks[Spark2].note(note, dur, velocity=9)

    # -- bars 57-72: dissolve — first one spark goes silent, then the other
    # Spark2 dissolves first
    tracks[Spark2].rest(W*8)
    # Spark1 continues alone, thinning
    dissolve1 = [
        ('C5',W*2),('-',W),
        ('G4',W*2),('-',W),
        ('E5',W+H),('-',Q),('-',W),
        ('C5',W+H),('-',Q),('-',W),
    ]
    for note, dur in dissolve1:
        if note == '-': tracks[Spark1].rest(dur)
        else: tracks[Spark1].note(note, dur, velocity=5)

    # -- bars 73-80: fragment alone — unchanged, as it was at the beginning
    # The fragment was already playing this whole time — just let it continue
    # Spark1 is also silent now
    tracks[Spark1].rest(W*8)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-father-fragment.mid")
    mc.compose(fn, tracks, tempo=60)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")

if __name__ == "__main__":
    father_fragment()
