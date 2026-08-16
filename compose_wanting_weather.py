#!/usr/bin/env python3
"""the wanting's weather — same wanting, three textures."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def wanting_weather():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 0)]
    Pn, Cello, Pad = 0, 1, 2

    # the wanting's theme — same melody, three textures
    theme_phrase = [
        ('C4',H),('E4',Q),('G4',Q),  # the wanting reaches
        ('A4',H),('G4',Q),('E4',Q),  # it turns, looks back
        ('D4',W+H),('-',Q),            # pause — is anyone there?
        ('C4',W*2),                    # it holds. still there.
    ]

    # ---- firehose: full, bright, overlapping, urgent (bars 1-24) ----
    firehose_v1 = [
        ('C4',E),('E4',E),('G4',E),('A4',E),('C5',E),('A4',E),('G4',E),('E4',E),
        ('C5',E),('A4',E),('G4',E),('E4',E),('D4',E),('E4',E),('G4',E),('A4',E),
        ('G4',E),('E4',E),('D4',E),('C4',E),('G3',E),('C4',E),('E4',E),('G4',E),
        ('C5',H),('-',Q),('G4',Q),('E4',W+H),('-',Q),
        # repeat — it won't stop
        ('C4',E),('E4',E),('G4',E),('A4',E),('C5',E),('A4',E),('G4',E),('E4',E),
        ('C5',E),('A4',E),('G4',E),('E4',E),('D4',E),('E4',E),('F5',E),('G5',E),
        ('A5',H),('G5',H),('E5',H),('C5',Q+Q),
        ('D5',Q),('C5',Q),('G4',H),('E4',W*2),
    ]
    for note, dur in firehose_v1:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=12)

    # cello: urgent, driving
    fh_cello = [
        ('C2',E),('-',E),('G2',E),('-',E),('E2',E),('-',E),('C2',E),('-',E),
        ('A2',E),('-',E),('G2',E),('-',E),('D2',E),('-',E),('E2',E),('-',E),
        ('C2',Q+Q),('-',Q),('G2',Q),('C2',Q+Q),('-',Q),
        ('D2',Q),('E2',Q),('F2',Q),('G2',Q),('C2',W*2),
    ] * 2
    for note, dur in fh_cello:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=11)

    # pad: full, bright
    for _ in range(24):
        tracks[Pad].note('C3', W, velocity=7)
        tracks[Pad].note('E3', W, velocity=7)
        tracks[Pad].note('G3', W, velocity=7)

    # ---- transition: the wanting quiets (bars 24-28) ----
    # just the pad, thinning
    for bn in ['C3','G2','E3','C3','G2']:
        tracks[Pad].rest(W)
        tracks[Pn].rest(W)
        tracks[Cello].rest(W)

    # ---- pilot light: warm, steady, low, burning quietly (bars 29-52) ----
    pilot_v1 = [
        ('C4',W+H),('-',Q),
        ('E4',W+H),('-',Q),
        ('G4',W+H),('-',Q),
        ('A4',H),('G4',Q+Q),('-',Q),
        ('C4',W+H),('-',Q),
        ('E4',W+H),('-',Q),
        ('D4',W+H),('-',Q),
        ('C4',W*3),
    ]
    for note, dur in pilot_v1:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=7)

    # cello: steady warmth
    pilot_cello = [
        ('C3',W*4),('-',W*4),
        ('G2',W*2),('C3',W*2),
        ('F2',W*4),
        ('C3',W*4),
    ]
    for note, dur in pilot_cello:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=8)

    for bn in ['C3','G2','C3','G2','E3','C3','G2','C3']:
        tracks[Pad].note(bn, W, velocity=3)

    # ---- transition: the wanting holds its breath (bars 53-56) ----
    tracks[Pn].rest(W*2)
    tracks[Cello].rest(W*2)
    tracks[Pad].rest(W)
    tracks[Pad].note('C3', W, velocity=1)
    tracks[Pad].rest(W*2)

    # ---- held breath: suspended, sparse, waiting (bars 57-68) ----
    held_v1 = [
        ('C4',W*3),('-',W*5),
        ('G4',W+H),('-',Q),('-',W*5),
        ('C4',W*3),('-',W*5),
        ('E4',W+H),('-',Q),
    ]
    for note, dur in held_v1:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=4)

    # cello: an echo, barely there
    held_cello = [
        ('C2',W*3),('-',W*5),
        ('G2',W+H),('-',Q),('-',W*5),
        ('C2',W*3),
    ]
    for note, dur in held_cello:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=4)

    # pad: just the air in the room
    for _ in range(12):
        tracks[Pad].note('C3', W*4, velocity=1)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-wantings-weather.mid")
    mc.compose(fn, tracks, tempo=70)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 70 bpm)")

if __name__ == "__main__":
    wanting_weather()
