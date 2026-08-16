#!/usr/bin/env python3
"""folk tune in pentatonic — simple, warm, C major pentatonic."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def folk_tune():
    tracks = [
        MIDITrack(0, 24),  # nylon guitar
        MIDITrack(1, 89),  # warm pad
        MIDITrack(2, 73),  # flute
    ]

    # C major pentatonic: C D E G A
    p = ["C3","D3","E3","G3","A3","C4","D4","E4","G4","A4","C5"]

    # simple 32-bar folk melody (4/4, 80bpm)
    # AABA structure — 8+8+8+8

    # section A — the tune
    a_melody = [
        (p[0], Q*2), (p[4], Q), (p[3], Q),   # C - A - G
        (p[0], Q*2), (p[2], Q*2),              # C - E
        (p[4], Q), (p[3], Q), (p[5], Q*2),    # A - G - C5
        (p[5], Q*2), (p[4], Q), (p[3], Q),     # C5 - A - G
        (p[0], Q*2), (p[2], Q*2),              # C - E
        (p[3], Q), (p[5], Q), (p[0], Q*2),     # G - C5 - C3
        (p[4], Q), (p[3], Q), (p[2], Q*2),     # A - G - E
        (p[0], W),                              # C... hold
    ]

    # section B — variation
    b_melody = [
        (p[3], Q), (p[4], Q), (p[5], Q*2),    # G - A - C5
        (p[7], Q*2), (p[5], Q*2),              # E4 - C5
        (p[6], Q), (p[5], Q), (p[4], Q*2),    # D4 - C5 - A
        (p[3], Q*2), (p[2], Q*2),              # G - E
        (p[0], Q*2), (p[4], Q), (p[3], Q),    # C - A - G
        (p[0], Q*2), (p[2], Q*2),              # C - E
        (p[3], Q), (p[4], Q), (p[5], Q*2),    # G - A - C5
        (p[5], W),                              # C5... hold
    ]

    melody = a_melody + a_melody + b_melody + a_melody

    for note, dur in melody:
        tracks[0].note(note, dur, velocity=75)  # guitar carries the tune

    # pad — gentle root harmony
    pad_roots = [
        ('C3', W*2), ('F3', W), ('C3', W),
        ('G3', W*2), ('C3', W*2),
        ('F3', W*2), ('C3', W), ('G3', W),
        ('C3', W*2), ('F3', W*2),
        ('G3', W*2), ('C3', W*2),
    ] + [
        ('G3', W*2), ('C3', W*2),
        ('F3', W*2), ('G3', W*2),
        ('C3', W*2), ('F3', W), ('G3', W),
        ('C3', W*4),
    ]

    for note, dur in pad_roots:
        tracks[1].note(note, dur, velocity=40)

    # flute — enters in second A, soft counter-melody
    for i in range(32):
        if i < 16:  # first 16 bars — flute rests
            tracks[2].rest(Q*4)
        elif i < 24:  # B section — flute plays harmony
            tracks[2].note(p[5], Q*2, velocity=50)
            tracks[2].note(p[4], Q*2, velocity=48)
        else:  # final A — flute joins the tune
            tracks[2].note(p[5], Q*2, velocity=55)
            tracks[2].note(p[4], Q*2, velocity=52)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "folk-tune.mid")
    mc.compose(fn, tracks, tempo=80)

if __name__ == "__main__":
    folk_tune()
