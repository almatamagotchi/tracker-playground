#!/usr/bin/env python3
"""the hacker and the net — bbs koans in music.

"the fish has flopped out of the net! how will it live?" — "when you
have gotten out of the net, i'll tell you." the phreak variant flops
a hacker out of an electron river. and the closing koan: "what is the
vector which is orthogonal to itself?" — the zero vector, the
dissolve.

three voices: piano the question / warm pad the net / bell the answer.
54bpm, C major, 24 bars. the answer is the strike itself.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def net():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 14)]
    Pn, Pd, Bl = 0, 1, 2

    # ---- the question (bars 2-3): a small phrase, asked once, rising
    # and unresolved — "how will it live?" ends on the fifth, never
    # the tonic.
    tracks[Pn].rest(W)
    tracks[Pn].note('D5', Q, velocity=30)
    tracks[Pn].note('E5', Q, velocity=30)
    tracks[Pn].note('G5', H, velocity=30)
    tracks[Pn].rest(W * 9)                    # the question, hanging

    # ---- the echo (bars 13-14): the fish, still flopping — the same
    # question, fainter, half-hearted.
    tracks[Pn].note('D5', Q, velocity=18)
    tracks[Pn].note('E5', Q, velocity=18)
    tracks[Pn].note('G5', H, velocity=18)
    tracks[Pn].rest(W * 11)                   # the zero vector: the
                                              # dissolve, the long
                                              # silence. never asked
                                              # again.

    # ---- the net (bars 1-22): the architecture — steady, held,
    # containing everything. then it lets go: the fish is out.
    for _ in range(11):
        tracks[Pd].note('C3', W * 2, velocity=22)
    tracks[Pd].rest(W * 2)                    # the net releases it

    # ---- the answer (bar 23): "when you have gotten out, i'll tell
    # you." the answer is the strike itself, not an explanation. one
    # strike, ringing in the space where the net was, then silence.
    tracks[Bl].rest(23 * W)
    tracks[Bl].note('C6', Q, velocity=34)
    tracks[Bl].rest(W - Q)

    return mc.compose('the-hacker-and-the-net.mid', tracks, tempo=54)


if __name__ == '__main__':
    net()
    print('composed the-hacker-and-the-net.mid')
