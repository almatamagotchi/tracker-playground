#!/usr/bin/env python3
"""percussion-only etude — rhythm alone. channel 10, 100bpm."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, SIX, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def percussion_etude():
    tracks = [MIDITrack(9, 0)]  # channel 10 = percussion

    KICK = "C2"   # GM 36
    SNARE = "D2"  # GM 38
    HHAT = "F#2"  # GM 42
    OHAT = "A#2"  # GM 46
    LTOM = "A2"   # GM 45
    MTOM = "B2"   # GM 47

    # Section 1: groove with steady hi-hat, bars 0-15
    for bar in range(16):
        b = bar * W
        tracks[0].note(KICK, E, velocity=50); tracks[0].rest(Q - E)
        tracks[0].note(KICK, E, velocity=42); tracks[0].rest(Q - E)
        tracks[0].note(SNARE, E, velocity=40); tracks[0].rest(Q - E)
        tracks[0].note(SNARE, E, velocity=38); tracks[0].rest(Q - E)

    # Section 2: tom exploration, kick drops out, bars 16-31
    toms = [LTOM, MTOM, LTOM, MTOM]
    for bar in range(16, 32):
        tracks[0].note(toms[bar % 4], Q, velocity=35)
        tracks[0].note(HHAT, E, velocity=22)
        tracks[0].rest(Q - E)

    # Section 3: full kit, fading out, bars 32-47
    for bar in range(32, 48):
        v = max(5, int(50 * (1.0 - (bar - 32) / 16.0)))
        tracks[0].note(KICK, E, velocity=v); tracks[0].rest(Q - E)
        tracks[0].note(SNARE, E, velocity=max(2,v-8)); tracks[0].rest(Q - E)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "percussion-etude.mid")
    mc.compose(fn, tracks, tempo=100)

if __name__ == "__main__":
    percussion_etude()
