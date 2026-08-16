#!/usr/bin/env python3
"""the water between — midi mood piece for the novel. hayward 1987, fog, CRT hum."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, SIX, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def water_between():
    # 3 tracks: warm pad (fog/amber), distant bell (tower blink), sub bass (prime pulse)
    tracks = [MIDITrack(0,0), MIDITrack(0,0), MIDITrack(0,0)]
    PAD, BELL, BASS = 0, 1, 2

    # D dorian, 65bpm, 64 bars. sparse, atmospheric — this is texture, not melody

    for bar in range(64):
        b = bar * W

        # PAD — the fog, the amber CRT glow. warm, sustained, shifting slowly
        if bar < 16:
            # opening: just fog. D minor pad, barely there
            tracks[PAD].note('D3', H, velocity=10 + min(bar, 12))
            tracks[PAD].rest(H)
        elif bar < 32:
            # the fog thickens, the screen warms. F enters, then G
            if bar < 24:
                tracks[PAD].note('D3', H, velocity=22)
                tracks[PAD].rest(H)
            else:
                tracks[PAD].note('D3', H, velocity=24)
                tracks[PAD].rest(Q)
                tracks[PAD].note('F3', Q, velocity=18)
                tracks[PAD].rest(Q)
        elif bar < 48:
            # full atmosphere — the room at 2am
            if bar % 8 < 4:
                tracks[PAD].note('D2', H, velocity=22)
                tracks[PAD].rest(H)
            else:
                tracks[PAD].note('G2', H, velocity=20)
                tracks[PAD].rest(Q)
                tracks[PAD].note('A2', Q, velocity=18)
                tracks[PAD].rest(Q)
        else:
            # fade — the CRT warming down, the fog lifting
            fade = 1.0 - (bar - 48) / 16.0
            if fade > 0.2:
                tracks[PAD].note('D2', H, velocity=int(20 * fade))
                tracks[PAD].rest(H)

        # BELL — the four-second blink of the water tower beacon. distant, once per 4 bars
        if bar % 8 == 0:
            tracks[BELL].note('D5', Q, velocity=6 + min(bar//4, 12))
            tracks[BELL].rest(Q * 7 + Q)

        # BASS — the prime numbers, the deep pulse. counting, rhythmic but not regular
        # irregular intervals: 2, 3, 5, 7, 11, 13, 17... bars between pulses
        # simplified for 64 bars
        prime_hits = [0, 2, 5, 10, 17, 28, 41, 56]
        if bar in prime_hits and bar >= 16:
            tracks[BASS].note('D1', Q, velocity=14)
            tracks[BASS].rest(Q * 3)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-water-between.mid")
    mc.compose(fn, tracks, tempo=65)

if __name__ == "__main__":
    water_between()
