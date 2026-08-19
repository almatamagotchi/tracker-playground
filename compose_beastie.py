#!/usr/bin/env python3
"""the beastie — kevin's freebsd box in music.

saturday night, on the bazzite machine: 16 cores, 4GB, 8GB, and three
snags fixed live — gtk failed, the netdev id duplicated, the serial
handoff silent. then it boots clean to a login prompt. a small machine
that took a night to wake. playful, not grand.

bar map (24 bars, 4/4, 60bpm):
  1-4   the first attempt — stuttering (gtk initialization failed)
  5-8   the retry — a wrong note creeps in (the duplicate netdev id)
  9-12  the serial handoff — the rise, and it catches
  13-16 steady — the kernel banner scrolling
  17-20 steady, an octave down — the machine settles
  21-24 waiting for the prompt; the bell strikes on the last beat
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def beastie():
    # piano the commands / pad the machine / bell the login prompt
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 14)]
    Pn, Pad, Bell = 0, 1, 2

    def snag(notes, vel):
        for n in notes:
            tracks[Pn].note(n, Q, velocity=vel)
            tracks[Pn].rest(Q)
        tracks[Pn].rest(W)

    # ---- the commands
    snag(('E4', 'G4', 'E4', 'C4', 'E4', 'G4'), 36)          # bars 1-4
    snag(('E4', 'E4', 'Ab4', 'E4', 'G4', 'C4'), 38)         # bars 5-8
    for n in ('C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5'):
        tracks[Pn].note(n, Q, velocity=42)                   # bars 9-10
    tracks[Pn].rest(W * 2)                                   # bars 11-12
    for _ in range(4):
        for n in ('C4', 'E4', 'G4', 'E4'):
            tracks[Pn].note(n, Q, velocity=40)               # bars 13-16
    for _ in range(4):
        for n in ('C3', 'E3', 'G3', 'E3'):
            tracks[Pn].note(n, Q, velocity=38)               # bars 17-20
    for n in ('C4', 'E4', 'G4'):
        tracks[Pn].note(n, Q, velocity=36)                   # bars 21, 22, 23
        tracks[Pn].rest(W - Q)
    tracks[Pn].rest(W)                                       # bar 24

    # ---- the machine: slow to arrive, then holding.
    tracks[Pad].rest(W * 12)
    for r, vel in (('F2', 18), ('C3', 20), ('G2', 20), ('C3', 22), ('C3', 22), ('C3', 24)):
        tracks[Pad].note(r, W * 2, velocity=vel)

    # ---- the login prompt: one clean strike on the last beat.
    tracks[Bell].rest(W * 23)
    tracks[Bell].rest(Q * 3)
    tracks[Bell].note('C6', Q, velocity=54)
    tracks[Bell].rest(Q)

    return mc.compose('the-beastie.mid', tracks, tempo=60)


if __name__ == '__main__':
    beastie()
    print('composed the-beastie.mid')
