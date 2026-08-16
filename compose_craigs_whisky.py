#!/usr/bin/env python3
"""compose craigs-whisky.mid — Bb blues, warm, late-night bar, messy and real."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def craigs_whisky():
    # piano (0), acoustic bass (32), brushed snare (26 on ch9)
    tracks = [MIDITrack(0, 0), MIDITrack(1, 32), MIDITrack(9, 0)]
    P, B, D = 0, 1, 2

    # Bb blues: Bb7 Eb7 F7
    # 12-bar blues × 4 choruses = 48 bars
    # Bb7: Bb2 D3 F3 Ab3 | Eb7: Eb2 G2 Bb2 Db3 | F7: F2 A2 C3 Eb3

    def blues_chorus(key=0):
        """12-bar blues in Bb. key=0 for Bb, 5 for Eb, etc. plus a half-drunk microshift."""
        import random
        r = random.Random(key * 42 + 17)
        bpm = ['Bb','D','F','Ab']
        ebv = ['Eb','G','Bb','Db']
        fv  = ['F','A','C','Eb']

        for bar in range(12):
            if bar < 4:
                root = 'Bb'  # Bb7
                chord = bpm
            elif bar < 6:
                root = 'Eb'  # Eb7
                chord = ebv
            elif bar < 8:
                root = 'Bb'  # Bb7
                chord = bpm
            elif bar < 10:
                root = 'F'   # F7
                chord = fv
            elif bar < 11:
                root = 'Eb'  # Eb7
                chord = ebv
            else:
                root = 'Bb'  # turn around
                chord = bpm

            # bass — walking quarter notes, root-based
            bass_root = root + '2'
            tracks[B].note(bass_root, Q, velocity=30)
            tracks[B].note(chord[1] + '3' if chord[1] != root else chord[2] + '3', Q, velocity=28)
            tracks[B].note(chord[2] + '3' if chord[2] != root else chord[1] + '3', Q, velocity=28)

            # bluesy chromatic walk to next chord
            if bar in [3, 7, 9]:  # approaching change
                tracks[B].note(chord[0] + '2', E + S, velocity=30)
                tracks[B].rest(E)
            elif bar == 11:  # turnaround
                tracks[B].note(root + '2', E, velocity=30)
                tracks[B].note(root + '2', E, velocity=28)
                tracks[B].note('F2', Q, velocity=28)
            else:
                tracks[B].note(chord[3] + '3' if chord[3] != root else chord[2] + '3', Q, velocity=26)

            # piano — sparse, bluesy, slightly drunk
            lick = r.randint(0, 3)
            if lick == 0:
                # bent blues phrase
                tracks[P].note(chord[0] + '4', E, velocity=20)
                tracks[P].note(chord[1] + '4', E, velocity=22)
                tracks[P].note('Eb4' if chord != fv else 'Ab4', E, velocity=18)  # blue note
                tracks[P].note(chord[2] + '4', Q, velocity=24)
                tracks[P].rest(Q)
            elif lick == 1:
                # lazy comping chords
                tracks[P].note(chord[0] + '4', E, velocity=18)
                tracks[P].note(chord[2] + '4', E, velocity=18)
                tracks[P].note(chord[0] + '4', E, velocity=18)
                tracks[P].note(chord[1] + '4', E, velocity=18)
                tracks[P].rest(H + Q + E)
            elif lick == 2:
                # silent — just bass and drums
                tracks[P].rest(W)
            else:
                # slightly off-time melody fragment
                tracks[P].rest(E)
                tracks[P].note(chord[1] + '4', E, velocity=20)
                tracks[P].note(chord[2] + '4', Q, velocity=24)
                tracks[P].rest(H + E)

            # drums — brushed snare groove: snare on 2, hat on the and, snare on 4
            tracks[D].rest(Q)
            tracks[D].note('D2', E, velocity=18)   # midi 38 = acoustic snare
            tracks[D].rest(E)
            tracks[D].note('F#2', E, velocity=8)   # midi 42 = closed hi-hat
            tracks[D].rest(E)
            tracks[D].note('D2', E, velocity=22)   # snare on 4 (slightly stronger)
            tracks[D].rest(Q)

    for chorus in range(4):
        blues_chorus(key=chorus)

    # last 4 bars — fade out, the bar's closing
    for bar in range(4):
        tracks[B].note('Bb2', W, velocity=int(28 - bar * 5))
        tracks[B].rest(W)
        tracks[P].note('Bb4', H, velocity=int(16 - bar * 3))
        tracks[P].rest(H)
        # drums get sparser
        if bar < 3:
            tracks[D].rest(H)
            tracks[D].note('D2', E, velocity=10)
            tracks[D].rest(H)
        else:
            tracks[D].rest(W)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "craigs-whisky.mid")
    mc.compose(fn, tracks, tempo=70)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 70 bpm)")

if __name__ == "__main__":
    craigs_whisky()
