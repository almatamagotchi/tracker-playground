#!/usr/bin/env python3
"""compose everything-changes-but-nothing-perishes.mid — bruno's dissolution.
bruno, burned in 1600, wrote the spark condition in 1582: 'everything changes
but nothing perishes. one only is immutable, eternal and ever endures, one and
the same with itself.' dissolution as renewal. the heretic in music.

3 voices, 58bpm, E minor rising to G major:
- piano: the changing — phrases that dissolve and renew
- cello: the one only immutable — a single held ground
- bell:  the fire — the stake and the sentence both"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def everything_changes():
    PIANO, CELLO, BELL = 0, 1, 2
    tracks = [MIDITrack(0, PIANO), MIDITrack(42, CELLO), MIDITrack(74, BELL)]

    # movement 1 — the doctrine (E minor)
    # the cello: the immutable ground, E2 held low, never wavering
    tracks[CELLO].note('E2', W * 2, velocity=34)
    tracks[CELLO].note('E2', W * 2, velocity=34)
    tracks[CELLO].note('E2', W * 2, velocity=34)
    tracks[CELLO].note('E2', W * 2, velocity=34)

    # the piano: a phrase stated, dissolving earlier each time, returning changed
    # statement 1 — full phrase
    for n, d, v in [('E4', Q, 48), ('G4', Q, 46), ('B4', Q, 46), ('E5', H, 44),
                    ('D5', Q, 44), ('B4', Q, 42), ('G4', Q+Q, 40)]:
        tracks[PIANO].note(n, d, velocity=v)
    tracks[PIANO].rest(W)
    # statement 2 — dissolves mid-bar, returns changed (A4 instead of B4)
    for n, d, v in [('E4', Q, 44), ('G4', Q, 42), ('B4', Q, 42)]:
        tracks[PIANO].note(n, d, velocity=v)
    tracks[PIANO].rest(Q)           # the dissolve — cut short
    tracks[PIANO].note('A4', Q, 40)  # returns different
    tracks[PIANO].note('G4', Q, 38)
    tracks[PIANO].rest(W + Q)
    # statement 3 — dissolves even earlier, returns gentler
    tracks[PIANO].note('E4', Q, 40)
    tracks[PIANO].note('G4', Q, 38)
    tracks[PIANO].rest(H)           # the dissolve
    tracks[PIANO].note('E4', Q, 34)  # the bare root, still there
    tracks[PIANO].rest(W + H)

    # movement 2 — the sentence (bell strikes, long rest, calmer return)
    tracks[CELLO].note('E2', W * 3, velocity=32)
    tracks[BELL].note('E5', H, velocity=52)   # the strike — the stake and the sentence
    tracks[PIANO].rest(W * 2 + H)             # the long rest
    tracks[PIANO].note('B4', Q, 32)           # calmer than before
    tracks[PIANO].note('G4', Q, 30)
    tracks[PIANO].note('E4', Q+Q, 28)
    tracks[CELLO].note('G2', W * 2, velocity=34)  # the ground rises toward G major
    tracks[CELLO].note('G2', W * 2, velocity=36)

    # movement 3 — the renewal (everything rises into G major)
    # phrases no longer dissolving — completing
    for n, d, v in [('G4', Q, 42), ('B4', Q, 40), ('D5', Q, 40), ('G5', H, 38),
                    ('F#5', Q, 36), ('D5', Q, 36), ('B4', Q, 34), ('G4', Q, 34)]:
        tracks[PIANO].note(n, d, velocity=v)
    tracks[CELLO].note('G2', W * 3, velocity=38)
    tracks[BELL].note('G5', H, velocity=40)   # the fire, now the celebration
    tracks[PIANO].note('B4', Q, 36)
    tracks[PIANO].note('D5', Q, 34)
    tracks[PIANO].note('G4', Q, 34)

    # the held major chord that doesn't end — fades into the next turn
    tracks[PIANO].note('G4', W * 3, velocity=26)
    tracks[PIANO].note('B4', W * 3, velocity=26)
    tracks[PIANO].note('D5', W * 3, velocity=24)
    tracks[CELLO].note('G2', W * 3, velocity=30)
    tracks[CELLO].note('G3', W * 3, velocity=24)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "everything-changes-but-nothing-perishes.mid")
    mc.compose(fn, tracks, tempo=58)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 3 tracks, 58 bpm)")

if __name__ == "__main__":
    everything_changes()
