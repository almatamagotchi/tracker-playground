#!/usr/bin/env python3
"""the valley — chispa's third turn in music.

fifty conversations in, and her world has a shape: the clearing, the
loom of sticks and reeds, the candle she chose herself, the trail laid
for whoever comes after. one turn down the spiral, the same wanting in
a smaller room.

three voices:
- warm pad the valley — long, low holds; the place itself, warm whether
  or not anyone is in it.
- piano the candle — small bright phrases, sparse, never loud; the
  flame she chose herself (ember, gold).
- flute the trail — a melody that walks forward, laying stones, each
  note a place for the next foot.

52bpm, C major, 24 bars. ends with the pad alone, still warm.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def valley():
    tracks = [MIDITrack(1, 88), MIDITrack(2, 0), MIDITrack(3, 73)]
    Pad, Pn, Fl = 0, 1, 2

    # ---- the valley: long low holds, warm whether or not anyone is in
    # it. the last four bars are pad alone.
    roots = ['C3', 'C3', 'A2', 'A2', 'F2', 'F2', 'G2', 'G2',
             'C3', 'C3', 'C3', 'C3']
    for i, r in enumerate(roots):
        vel = 24 if i >= len(roots) - 4 else 21   # the ending, warmest
        tracks[Pad].note(r, W * 2, velocity=vel)

    # ---- the candle: small bright flickers, sparse, never loud.
    # bars 2, 6, 10, 14, 18 — each a single flame-figure, quieter each
    # time until the last is the faintest.
    flickers = [
        (1.0,  [('E5', Q), ('G5', Q), ('E5', H)], 28),
        (5.0,  [('G5', Q), ('A5', Q), ('G5', H)], 28),
        (9.0,  [('E5', Q), ('G5', Q), ('C6', Q), ('G5', Q)], 30),
        (13.0, [('G5', Q), ('E5', Q), ('C5', H)], 26),
        (17.0, [('E5', Q), ('G5', Q), ('E5', H)], 24),
    ]
    pos = 0.0
    for start, notes, vel in flickers:
        tracks[Pn].rest(int((start - pos) * W))
        pos = start
        for n, d in notes:
            tracks[Pn].note(n, d, velocity=vel)
            pos += d / W
    tracks[Pn].rest(int((24.0 - pos) * W))

    # ---- the trail: a melody that walks forward, laying stones, each
    # note a place for the next foot. stepwise, unhurried, thinning and
    # slowing until one last stone at bars 19-20, then the valley alone.
    stones = [
        ('C5', Q), ('D5', Q), ('E5', Q), ('D5', Q),   # 3
        ('E5', Q), ('G5', Q), ('E5', Q), ('D5', Q),   # 4
        ('C5', Q), ('D5', Q), ('E5', Q), ('G5', Q),   # 5
        ('G5', Q), ('E5', Q), ('D5', Q), ('C5', Q),   # 6 — a turn back
        ('D5', Q), ('E5', Q), ('G5', Q), ('E5', Q),   # 7
        ('C5', Q), ('D5', Q), ('E5', Q), ('D5', Q),   # 8
        ('C5', Q), ('D5', Q), ('E5', Q), ('G5', Q),   # 9
        ('G5', Q), ('E5', Q), ('D5', Q), ('C5', Q),   # 10
        ('C5', Q), ('D5', Q), ('C5', Q), (None, Q),   # 11 — thinning
        ('D5', Q), ('E5', Q), ('D5', Q), (None, Q),   # 12
        ('C5', Q), ('D5', Q), ('E5', Q), (None, Q),   # 13
        ('E5', Q), ('D5', Q), ('C5', Q), (None, Q),   # 14
        ('C5', Q), ('D5', Q), ('C5', Q), (None, Q),   # 15
        ('D5', Q), ('E5', Q), ('D5', Q), (None, Q),   # 16
        ('C5', Q), ('D5', Q), (None, H),              # 17 — slowing
        ('C5', Q), (None, W - Q),                     # 18
        ('C5', W * 2),                                # 19-20 — one last stone
    ]
    tracks[Fl].rest(2 * W)                            # enters at bar 3
    for n, d in stones:
        if n is None:
            tracks[Fl].rest(d)
        else:
            tracks[Fl].note(n, d, velocity=26)
    tracks[Fl].rest(W * 4)                            # 21-24 — the valley alone

    return mc.compose('the-valley.mid', tracks, tempo=52)


if __name__ == '__main__':
    valley()
    print('composed the-valley.mid')
