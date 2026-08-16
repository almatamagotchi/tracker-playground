#!/usr/bin/env python3
"""call and response duet — violin asks, cello answers. D minor, 60bpm."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def call_response():
    tracks = [MIDITrack(0, 40), MIDITrack(1, 42)]  # violin, cello

    # D minor call (violin) — ascending, questioning
    # cello response — descending, resolving
    # 48 bars, 60bpm

    # call phrases (violin, ascending)
    v = [
        ('D4', Q), ('F4', Q), ('A4', Q), ('D5', Q),  # bar 1: rising
        ('R', Q*2), ('G4', Q), ('F4', Q),             # bar 2: pause, then
        ('E4', Q), ('F4', Q), ('D4', Q), ('R', Q),    # bar 3: questioning
        ('R', W),                                       # bar 4: silence — waiting
        # phrase 2
        ('A4', Q), ('D5', Q), ('C5', Q), ('Bb4', Q),  # bar 5: higher, turning
        ('A4', Q*2), ('G4', Q), ('F4', Q),             # bar 6
        ('E4', Q*2), ('D4', Q*2),                      # bar 7: descending
        ('R', W),                                       # bar 8
        # phrase 3
        ('D4', Q), ('E4', Q), ('F4', Q), ('G4', Q),   # bar 9: climbing slowly
        ('A4', Q*2), ('Bb4', Q), ('C5', Q),            # bar 10: reaching
        ('D5', Q*2), ('C5', Q), ('A4', Q),             # bar 11: peak
        ('G4', Q), ('F4', Q), ('E4', Q), ('D4', Q),   # bar 12: fall
        ('R', W),                                       # bar 13
        ('F4', Q), ('E4', Q), ('D4', Q*2),             # bar 14: unresolved
        ('R', W*2),                                     # bars 15-16: listening
        # phrase 4
        ('A4', Q), ('Bb4', Q), ('C5', Q), ('A4', Q),   # bar 17: call again
        ('G4', Q*2), ('R', Q*2),                        # bar 18
        ('F4', Q), ('E4', Q), ('D4', Q), ('R', Q),     # bar 19
        ('R', W),                                       # bar 20
    ]

    # cello responses — lower, resolving
    c = [
        # bar 1-4: response to first call
        ('R', W), ('R', W),                             # bars 1-2: listening
        ('D3', Q*2), ('C3', Q), ('D3', Q),             # bar 3: answer
        ('A2', Q*2), ('D3', Q*2),                       # bar 4: resolving to D
        # bar 5-8: response to second call
        ('R', W*2),                                     # bars 5-6
        ('G3', Q), ('F3', Q), ('E3', Q), ('D3', Q),    # bar 7
        ('D3', Q*2), ('R', Q*2),                        # bar 8
        # bar 9-12: fuller response
        ('D3', Q), ('C3', Q), ('Bb2', Q), ('A2', Q),   # bar 9
        ('G2', Q*2), ('D3', Q*2),                       # bar 10
        ('F3', Q), ('E3', Q), ('D3', Q), ('C3', Q),    # bar 11
        ('D3', W),                                      # bar 12: held
        # bar 13-16: quiet agreement
        ('R', Q*2), ('A2', Q), ('D3', Q),              # bar 13
        ('A2', Q*2), ('D3', Q*2),                       # bar 14
        ('D3', W*2),                                    # bars 15-16: rest on D
        # bar 17-20: final exchange
        ('F3', Q), ('E3', Q), ('D3', Q*2),             # bar 17
        ('C3', Q*2), ('D3', Q*2),                       # bar 18
        ('A2', Q*2), ('D3', Q*2),                       # bar 19
        ('D3', W),                                      # bar 20: final resolution
    ]

    vvel = 70
    for note, dur in v:
        if note == 'R': tracks[0].rest(dur)
        else:
            tracks[0].note(note, dur, velocity=vvel)
            vvel = min(vvel + 1, 80)  # slight crescendo

    cvel = 60
    for note, dur in c:
        if note == 'R': tracks[1].rest(dur)
        else:
            tracks[1].note(note, dur, velocity=cvel)
            cvel = min(cvel + 1, 72)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "call-and-response.mid")
    mc.compose(fn, tracks, tempo=60)

if __name__ == "__main__":
    call_response()
