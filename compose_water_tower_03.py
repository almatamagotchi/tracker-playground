#!/usr/bin/env python3
"""compose the-water-tower-at-0.3.mid — RFC-0197

the tower has been counting since 1895. at 0.05 it was the only sound —
a groove so narrow the beacon filled the whole room. then the temperature
changed, and the room got wider. the beacon is unchanged. the air around it
is what's different: fog drifting where there used to be wall, space to move
between blinks.

structure (64 bars @ 60bpm, D dorian-ish over a C pedal):
  A. the beacon — pulse alone, steady, the count
  B. the room — the pad enters, wider intervals, the space around the tower
  C. the fog — a line that drifts through the wider air, never quite landing
  D. the count continues — beacon + room + fog together, then the fog thins
  E. the tower — beacon alone again, unchanged, still counting
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def water_tower_03():
    # bell (13 = xylophone-ish bell), cello (42), warm pad (89), piano (0)
    tracks = [MIDITrack(0, 13), MIDITrack(1, 42), MIDITrack(2, 89), MIDITrack(3, 0)]
    Bell, Cello, Pad, Pn = 0, 1, 2, 3

    # --- A. the beacon (bars 1-16) — a bell every 4 bars, nothing else ---
    # the pulse of the tower: one strike, then the count in the air
    beacon_notes = ['G4', 'C5', 'G4', 'E5']
    for bar in range(16):
        if bar % 4 == 0:
            tracks[Bell].note(beacon_notes[(bar // 4) % 4], H, velocity=20)
            tracks[Bell].rest(H)
        else:
            tracks[Bell].rest(W)
        for t in (Cello, Pad, Pn):
            tracks[t].rest(W)

    # --- B. the room (bars 17-32) — the pad enters, the space widens ---
    # warm pad holds a C-G-C pedal, the bell keeps its 4-bar strike
    for bar in range(16):
        if bar % 4 == 0:
            tracks[Bell].note('C5', H, velocity=18)
            tracks[Bell].rest(H)
        else:
            tracks[Bell].rest(W)
        # pad — long roots, the room around the tower
        if bar < 8:
            tracks[Pad].note('C3', W * 4, velocity=8)   # one every 4 bars
            if bar % 4 == 0:
                tracks[Pad].note('G3', W * 4, velocity=6)
            if bar % 4 == 2:
                tracks[Pad].note('E3', W * 4, velocity=6)
        else:
            tracks[Pad].note('C3', W * 4, velocity=9)
            if bar % 4 == 0:
                tracks[Pad].note('G3', W * 4, velocity=7)
            if bar % 4 == 2:
                tracks[Pad].note('A3', W * 4, velocity=7)
        for t in (Cello, Pn):
            tracks[t].rest(W)

    # --- C. the fog (bars 33-48) — a line that drifts through the wider air ---
    # cello moves now: slow, wandering, never quite resolving — the fog
    fog = [
        ('D3', H), ('E3', H), ('D3', W),
        ('F3', H), ('E3', H), ('C3', W),
        ('G3', H), ('F3', H), ('E3', W),
        ('D3', H), ('C3', H), ('D3', W),
        ('E3', H), ('G3', H), ('D3', W),
        ('C3', H), ('D3', H), ('E3', W),
        ('F3', H), ('E3', H), ('D3', W),
        ('C3', W), ('D3', W),
    ]
    for note, dur in fog:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=14)

    # bell continues its 4-bar strike, quieter under the fog
    for bar in range(16):
        if bar % 4 == 0:
            tracks[Bell].note('C5', H, velocity=15)
            tracks[Bell].rest(H)
        else:
            tracks[Bell].rest(W)
        # pad continues holding
        tracks[Pad].note('C3', W * 4, velocity=8)
        if bar % 4 == 0:
            tracks[Pad].note('G3', W * 4, velocity=6)
        tracks[Pn].rest(W)

    # --- D. the count continues (bars 49-60) — all three, then fog thins ---
    # piano enters with a wide, open phrase — the valley's version of a melody
    valley = [
        ('C4', H), ('E4', H),
        ('G4', H), ('E4', H),
        ('D4', H), ('F4', H),
        ('E4', W),
        ('C4', H), ('D4', H),
        ('E4', H), ('G4', H),
        ('C5', W),
    ]
    for note, dur in valley:
        tracks[Pn].note(note, dur, velocity=11)

    for bar in range(12):
        if bar % 4 == 0:
            tracks[Bell].note('G4', H, velocity=17)
            tracks[Bell].rest(H)
        else:
            tracks[Bell].rest(W)
        # fog thins — cello rests more, holds long tones
        if bar < 4:
            tracks[Cello].note('D3', W, velocity=10)
        elif bar < 8:
            tracks[Cello].note('C3', W, velocity=9)
        else:
            tracks[Cello].note('G2', W * 2, velocity=8)
            tracks[Cello].rest(W)
        tracks[Pad].note('C3', W * 4, velocity=7)
        if bar % 4 == 2:
            tracks[Pad].note('G3', W * 4, velocity=6)
        tracks[Pn].rest(W)

    # --- E. the tower (bars 61-64) — beacon alone, unchanged, still counting ---
    for bar in range(4):
        if bar % 4 == 0:
            tracks[Bell].note('C5', H, velocity=20)
            tracks[Bell].rest(H)
        else:
            tracks[Bell].rest(W)
        tracks[Pad].note('C2', W * 4, velocity=5)  # the ground, faint
        for t in (Cello, Pn):
            tracks[t].rest(W)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-water-tower-at-0.3.mid")
    mc.compose(fn, tracks, tempo=60)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")

if __name__ == "__main__":
    water_tower_03()
