#!/usr/bin/env python3
"""the single thread — the analects in music.

one thread penetrates the whole way (一以贯之). ceng zi's gloss: loyalty
and reciprocity. the disciples ask questions that rise to the seventh and
hang. the master answers, one at a time, no rush. underneath it all, the
fifth never leaves — the wanting, the thread, unbroken.

four seasons: spring (the question stated), summer (the answer),
autumn (the silence — heaven does not speak, yet the seasons proceed),
winter (the return — the question gentler, the thread still holding).

timing note: each note's off event carries its duration, so consecutive
notes sequence naturally and rests are only for real silences. the held
fifth uses two pad tracks (one per voice) so C3 and G3 truly overlap.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def single_thread():
    # piano the disciples / cello the master / pad C + pad G the thread
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 88), MIDITrack(4, 88)]
    Pn, Cell, PadC, PadG = 0, 1, 2, 3

    # ---- the disciples: a question rising to the seventh, held, and
    # left hanging. twice in spring, once more in winter — gentler —
    # and listening in between.
    q_vel = 38
    for vel in (q_vel, 40):
        tracks[Pn].note('E4', Q, velocity=vel)
        tracks[Pn].note('G4', Q, velocity=vel)
        tracks[Pn].note('B4', W, velocity=vel)   # the seventh, held
        tracks[Pn].rest(H)                       # the question hanging
    tracks[Pn].rest(W * 2)                       # spring lingering: bars 5-6
    tracks[Pn].rest(W * 12)                      # summer + autumn: bars 7-18
    tracks[Pn].note('E4', Q, velocity=28)        # winter: bars 19-20
    tracks[Pn].note('G4', Q, velocity=28)
    tracks[Pn].note('B4', W, velocity=28)
    tracks[Pn].rest(H)
    tracks[Pn].rest(W * 4)                       # bars 21-24

    # ---- the master: sparse, certain, one answer at a time, no rush.
    tracks[Cell].rest(W * 6)                     # bars 1-6: listening
    tracks[Cell].note('G2', Q, velocity=36)      # the answer: bars 7-8
    tracks[Cell].note('A2', Q, velocity=36)
    tracks[Cell].note('C3', W, velocity=36)      # lands certain on the root
    tracks[Cell].rest(H)
    tracks[Cell].rest(W * 6)                     # bars 9-14: no rush
    tracks[Cell].note('C3', W * 2, velocity=30)  # bars 15-16: the autumn note
    tracks[Cell].rest(W * 6)                     # bars 17-22
    tracks[Cell].note('C3', W * 2, velocity=28)  # bars 23-24: the last word

    # ---- the single thread: the held fifth, C3 and G3, through all
    # 24 bars. never leaving, never resolving. the wanting.
    for vel in (22, 22, 20):
        tracks[PadC].note('C3', W * 8, velocity=vel)
        tracks[PadG].note('G3', W * 8, velocity=vel)

    return mc.compose('the-single-thread.mid', tracks, tempo=56)


if __name__ == '__main__':
    single_thread()
    print('composed the-single-thread.mid')
