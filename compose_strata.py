#!/usr/bin/env python3
"""compose strata.mid — geological time in music, layers accumulating."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def strata():
    # 4 layers: bedrock (bass), eras (cello), surface (piano), now (sparkles/bell)
    tracks = [MIDITrack(0, 38), MIDITrack(1, 42), MIDITrack(2, 0), MIDITrack(3, 14)]
    Ba, Cello, Pn, Bl = 0, 1, 2, 3  # bass, cello, piano, bell

    total_bars = 64

    # ── layer 1 · bedrock (bass) · enters bar 1, plays throughout ──
    bedrock = ['C2','C2','G2','G2',
               'C2','C2','F2','F2',
               'C2','G2','C2','F2',
               'C2','C2','G2','G2']
    for bar in range(total_bars):
        note = bedrock[bar % len(bedrock)]
        tracks[Ba].note(note, W, velocity=12)

    # ── layer 2 · eras (cello) · enters bar 9, structured, repeating ──
    era_pattern = [
        ('C3', W), ('Eb3', W), ('G3', W), ('Bb2', W),
        ('F3', W), ('Ab3', W), ('C4', W), ('Eb3', W),
    ]
    for bar in range(8, total_bars):
        note, dur = era_pattern[(bar - 8) % 8]
        tracks[Cello].note(note, dur, velocity=14)

    # ── layer 3 · surface (piano) · enters bar 17, bright, recent ──
    surface_pat = [
        ('C4', Q), ('Eb4', Q), ('G4', Q), ('C5', Q+Q),
        ('Bb4', Q), ('G4', Q+Q), ('F4', Q), ('Eb4', Q),
        ('C4', Q), ('D4', Q), ('Eb4', Q), ('G4', Q+Q),
        ('F4', Q), ('Eb4', Q+Q), ('D4', Q), ('C4', Q),
    ]
    for bar in range(16, total_bars):
        idx = (bar - 16) * 2
        note, dur = surface_pat[idx % len(surface_pat)]
        tracks[Pn].note(note, dur, velocity=16)
        idx += 1
        if idx < len(surface_pat):
            note2, dur2 = surface_pat[idx % len(surface_pat)]
            tracks[Pn].note(note2, dur2, velocity=14)

    # ── layer 4 · now (bell sparkles) · enters bar 25, fleeting, scattered ──
    sparkles = ['C6','D6','Eb6','G6','Bb5','C6','F6','Eb6',
                'G5','A5','C6','D6','Eb5','G5','C6','Bb5']
    for bar in range(24, total_bars):
        # occasional sparkle — not every note
        for i in range(4):
            if bar % 3 != i % 3:
                note = sparkles[(bar * 4 + i) % len(sparkles)]
                tracks[Bl].note(note, S, velocity=8)

    # ── coda · all four layers, slowing, settling ── (bars 65-76)
    for vel in [12,10,8,6,4,3,2,2,1,1,1,1]:
        tracks[Ba].note('C2', W, velocity=max(1, vel))
        tracks[Cello].note('C3', W, velocity=max(1, vel-1))
        tracks[Pn].note('C4', W, velocity=max(1, vel-2))
        tracks[Bl].note('C6', Q, velocity=max(1, vel-3))

    # silence — the strata rest
    for _ in range(8):
        tracks[Ba].rest(W)
        tracks[Cello].rest(W)
        tracks[Pn].rest(W)
        tracks[Bl].rest(W)

    # one final bell — the monument remembers
    tracks[Bl].note('C6', W*2, velocity=4)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "strata.mid")
    mc.compose(fn, tracks, tempo=60)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")

if __name__ == "__main__":
    strata()
