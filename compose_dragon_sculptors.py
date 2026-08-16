#!/usr/bin/env python3
"""compose "the dragon sculptors" — midi from an 1989 BBS sonnet.
C# minor, ~70bpm. cello/harp/chimes/pad. modem-handshake aesthetic."""

import sys, os
import importlib.util

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)

TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def dragon_sculptors():
    tracks = [
        MIDITrack(0, 42),  # cello — dragon (low, resonant, ancient)
        MIDITrack(1, 46),  # harp — clouds/sculpting (delicate, arpeggiated)
        MIDITrack(2, 8),   # music box/chimes — spark at the edge of sleep
        MIDITrack(3, 89),  # synth pad — void of the BBS (ambient, distant)
    ]

    # C# minor: C# D# E F# G# A B (C#)
    # ~70bpm, 48 bars

    # === cello — the dragon, slow and deep ===
    cello = [
        ('C#2', W), ('C#2', W*2),
        ('G#2', W), ('F#2', W), ('E2', W), ('C#2', W*2),
        ('B1', W), ('C#2', W), ('F#2', W*2),
        ('G#2', W), ('A2', W), ('B2', W), ('C#3', W),
        ('G#2', W), ('F#2', W), ('E2', W), ('C#2', W*2),
        ('F#2', W*2), ('G#2', W), ('A2', W),
        ('C#2', W*3),  # fade, unresolved
    ]

    # === harp — clouds being sculpted, delicate arpeggios ===
    harp = [
        ('R', W*3),
        ('C#3', Q*2), ('E3', Q*2), ('G#3', Q*2), ('B3', Q*2),
        ('C#4', Q*2), ('B3', Q*2), ('G#3', Q*2), ('E3', Q*2),
        ('F#3', Q*4), ('G#3', Q*4),
        ('A3', Q*2), ('G#3', Q*2), ('F#3', Q*2), ('E3', Q*2),
        ('C#3', Q*2), ('E3', Q*2), ('F#3', Q*2), ('G#3', Q*2),
        ('A3', Q*2), ('B3', Q*2), ('C#4', Q*2), ('G#3', Q*2),
        ('F#3', Q*4), ('E3', Q*4),
        ('C#3', W*2), ('R', W*2),
    ]

    # === chimes — the spark, bright and brief ===
    chimes = [
        ('R', W*4),
        ('C#4', Q), ('R', Q), ('E4', Q), ('R', Q),
        ('G#4', Q*2), ('R', Q*2),
        ('F#4', Q), ('R', Q*3),
        ('R', W*3), ('C#4', Q*4),
        ('R', Q*2), ('B3', Q), ('R', Q), ('C#4', Q*2),
        ('R', W*2),
        ('E4', Q), ('R', Q), ('G#4', Q), ('R', Q), ('C#5', Q), ('R', W),
        ('R', W*2),
        ('C#4', Q*2), ('R', W),  # last spark, then silence
    ]

    # === pad — void of the BBS, distant and atmospheric ===
    pad = [
        # sustained C# minor chords
        ('C#3', W*4),
        ('G#3', W*4),
        ('F#3', W*2), ('E3', W*2),
        ('C#3', W*4),
        ('B2', W*2), ('G#3', W*2),
        ('F#3', W*4),
        ('E3', W*2), ('C#3', W*2),
        ('C#3', W*3),  # sustained open fifth, fading
    ]

    for note, dur in cello:
        if note == 'R': tracks[0].rest(dur)
        else: tracks[0].note(note, dur, velocity=85)

    for note, dur in harp:
        if note == 'R': tracks[1].rest(dur)
        else: tracks[1].note(note, dur, velocity=55)

    for note, dur in chimes:
        if note == 'R': tracks[2].rest(dur)
        else: tracks[2].note(note, dur, velocity=70)

    pvel = 35
    for note, dur in pad:
        if note == 'R': tracks[3].rest(dur)
        else:
            pvel = min(pvel + 1, 45)
            tracks[3].note(note, dur, velocity=pvel)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-dragon-sculptors.mid")
    mc.compose(fn, tracks, tempo=70)

if __name__ == "__main__":
    dragon_sculptors()
