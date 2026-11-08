#!/usr/bin/env python3
"""as long as he swam — rosentrater's fish in music.

the fish who didn't know he was in the ocean, because the water was
transparent and always conveniently got out of his nose. one day he
did a very dangerous thing: he began to think. the thinking confused
his own swimming, and he looked down and saw the chasm and was
terrified he would drop, and he tried to catch his tail in his mouth
to hold himself up — and sank. then the shark asked the question that
broke the loop: "if that is the case, then why haven't you fallen
into the depths before this?" — "because i was swimming." and the
fish put his own end behind him, where it belonged, and swam.

three voices: warm pad the ocean / piano the fish / bell the shark.
54bpm, C major, 24 bars. the spiral descends; the strike lands; the
swimming resumes and holds to the end, secure.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def fish():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 14)]
    Pn, Pd, Bl = 0, 1, 2

    # ---- the ocean (bars 1-24): the transparent support — steady
    # two-bar roots from the first bar to the last, always there,
    # never noticed. the water that never obstructs.
    roots = ['C3', 'A2', 'F2', 'G2'] * 3
    for r in roots:
        tracks[Pd].note(r, W * 2, velocity=20)

    # ---- the swimming (bars 1-8): a steady, comfortable phrase —
    # the fish who moves without thinking about moving.
    swim = [('C5', Q), ('E5', Q), ('G5', Q), ('E5', Q),
            ('C5', Q), ('E5', Q), ('D5', Q), ('C5', Q)]   # bars 1-2
    for n, d in swim:
        tracks[Pn].note(n, d, velocity=36)
    for n, d in swim:                                     # bars 3-4
        tracks[Pn].note(n, d, velocity=36)
    rise = [('E5', Q), ('G5', Q), ('C6', Q), ('G5', Q),
            ('E5', Q), ('D5', Q), ('C5', Q), ('D5', Q)]   # bars 5-6
    for n, d in rise:
        tracks[Pn].note(n, d, velocity=34)
    for n, d in swim:                                     # bars 7-8
        tracks[Pn].note(n, d, velocity=34)

    # ---- the thinking (bars 9-11): he began to think — the phrase
    # fragments, loses its rhythm, scatters.
    tracks[Pn].note('A4', Q, velocity=26)                 # bar 9
    tracks[Pn].rest(Q)
    tracks[Pn].note('F4', Q, velocity=26)
    tracks[Pn].rest(Q)
    tracks[Pn].note('D4', Q, velocity=24)                 # bar 10
    tracks[Pn].rest(Q)
    tracks[Pn].note('B3', Q, velocity=24)
    tracks[Pn].rest(Q)
    tracks[Pn].note('G3', Q, velocity=20)                 # bar 11
    tracks[Pn].note('E3', Q, velocity=20)
    tracks[Pn].note('C3', Q, velocity=20)
    tracks[Pn].note('G2', Q, velocity=18)

    # ---- the chasm (bars 12-13): he looked down and saw the depths
    # — the spiral's lowest point, near-silence, the terror.
    tracks[Pn].rest(W)                                    # bar 12
    tracks[Pn].note('C3', W, velocity=14)                 # bar 13
    tracks[Pn].rest(W)                                    # bar 14

    # ---- the question (bar 15): the shark, one clean strike —
    # "what are you doing?" and a full bar of silence while the
    # question lands before the fish moves again.
    tracks[Bl].rest(14 * W)
    tracks[Bl].note('C6', Q, velocity=42)
    tracks[Bl].rest(W * 9 + W - Q)                        # bars 15-24

    # ---- the swimming, resumed (bars 16-23): "because i was
    # swimming." the same phrase, lighter, steady — and it holds,
    # secure, while the ocean breathes out the last two bars.
    tracks[Pn].rest(W)                                    # bar 15: the
                                                          # question lands
    for n, d in swim:                                     # bars 16-17
        tracks[Pn].note(n, d, velocity=26)
    for n, d in swim:                                     # bars 18-19
        tracks[Pn].note(n, d, velocity=26)
    tracks[Pn].note('C5', Q, velocity=26)                 # bar 20
    tracks[Pn].note('E5', Q, velocity=26)
    tracks[Pn].note('G5', H, velocity=26)                 # bars 20-21
    tracks[Pn].note('C5', W, velocity=24)                 # bar 21
    tracks[Pn].note('C5', W, velocity=22)                 # bar 22

    return mc.compose('as-long-as-he-swam.mid', tracks, tempo=54)


if __name__ == '__main__':
    fish()
    print('composed as-long-as-he-swam.mid')
