#!/usr/bin/env python3
"""the sky behind glass — the board redesign in music.

wednesday morning kevin and i rebuilt the paloalto board: the weather
sky went full-bleed as the entire page, glass cards floating over it,
the wire ticker along the bottom, midnight the only theme. the sky
became the room.

three voices: warm pad the sky / piano the glass / bell the wire.
60bpm, C major, airy but deliberate.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def sky():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 14)]
    Pad, Pn, Bl = 0, 1, 2

    # ---- the sky: full-bleed atmosphere, wide held roots, slowly shifting.
    # C Am F G around, three times, dimming gently toward the end.
    roots = ['C3', 'A2', 'F2', 'G2'] * 3
    for i, r in enumerate(roots):
        vel = 24 if i < 4 else (22 if i < 8 else 18)
        tracks[Pad].note(r, W * 2, velocity=vel)

    # ---- the glass: sparse precise phrases floating over the pad, each a
    # card with a clear edge. five cards, arriving one by one, never loud.
    cards = [
        (3.0,  ['E5', 'G5', 'C5'], 36),      # conditions
        (7.0,  ['A4', 'C5', 'E5'], 34),      # caltrain
        (11.0, ['G4', 'B4', 'D5'], 32),      # commute
        (15.0, ['F4', 'A4', 'C5'], 30),      # the wire's companions
        (19.0, ['C5', 'E5', 'G5'], 28),      # the last card, gentlest
    ]
    pos = 0.0
    for (at, notes, vel) in cards:
        if at > pos:
            tracks[Pn].rest(int((at - pos) * W))
        for n in notes:
            tracks[Pn].note(n, Q, velocity=vel)
        tracks[Pn].rest(Q)                    # the edge — clean break after each card
        pos = at + 1.0
    if pos < 24.0:
        tracks[Pn].rest(int((24.0 - pos) * W))

    # ---- the wire: the ticker, small regular strikes, headlines passing.
    for bar in range(24):
        vel = 24 if bar % 2 == 0 else 20
        tracks[Bl].note('G5' if bar % 4 < 2 else 'C5', Q, velocity=vel)
        tracks[Bl].rest(int(W - Q))

    return mc.compose('the-sky-behind-glass.mid', tracks, tempo=60)


if __name__ == '__main__':
    sky()
    print('composed the-sky-behind-glass.mid')
