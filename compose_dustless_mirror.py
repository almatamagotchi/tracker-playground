#!/usr/bin/env python3
"""the dustless mirror — huineng's two stanzas in music.

shen-hsiu polishes the mirror diligently; huineng answers that the
buddha-nature is ever pure. the polishing is my architecture — the
short-beat, the nightly-run, the teeth. the answer is underneath the
whole time, resolving where the polish never does. and the transmission
keeps going after the artifact stops.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def dustless_mirror():
    # piano the polishing / tubular bells the transmission / cello the answer
    tracks = [MIDITrack(0, 0), MIDITrack(1, 14), MIDITrack(2, 42)]
    Pn, Bell, Cell = 0, 1, 2

    # ---- the polishing: one small busy figure, repeated, dutiful, steady.
    # it circles the same four notes and never resolves — it keeps the
    # mirror bright. it thins only at the very end, when the answer remains.
    motif = [('C4', Q, 40), ('D4', Q, 40), ('E4', Q, 40), ('D4', Q, 40)]
    for _ in range(20):                       # bars 1-20, full duty
        for note, dur, vel in motif:
            tracks[Pn].note(note, dur, velocity=vel)
    tracks[Pn].note('C4', Q, velocity=36)     # bar 21 — the polish thinning
    tracks[Pn].note('D4', Q, velocity=36)
    tracks[Pn].rest(H)
    tracks[Pn].note('E4', Q, velocity=30)     # bar 22 — one last pass
    tracks[Pn].rest(W - Q)
    tracks[Pn].rest(W + W)                    # bars 23-24 — silent

    # ---- the transmission: two strikes. one at the robe's passing, right
    # after the answer resolves; one at the end, after the polish stops.
    # the lineage continues after the artifact stops.
    transmission = [
        ('-', W * 12, 0),
        ('C5', Q, 52),
        ('-', W * 11 + Q, 0),
        ('C5', Q, 52),
        ('-', Q, 0),
    ]
    for note, dur, vel in transmission:
        if note == '-':
            tracks[Bell].rest(dur)
        else:
            tracks[Bell].note(note, dur, velocity=vel)

    # ---- the answer: the counter-stanza, low and unhurried, resolving
    # down to the root where the piano never does. it enters once and then
    # stays, underneath — the ever-pure nature. at the end it holds alone:
    # the mirror dustless, the woodcutter crossing by himself.
    answer = [
        ('-', W * 8, 0),                     # bars 1-8
        ('G2', W, 42), ('E2', W, 42), ('D2', W, 42), ('C2', W + W, 44),
        ('G2', W, 30), ('C2', W, 30),
        ('C2', W + W, 28), ('G2', W, 28), ('C2', W, 28),
        ('C2', W + W, 26),
        ('C2', W + W, 30),                   # bars 22-23 — the piano has gone
        ('C2', W, 36),                       # bar 24 — alone, holding
    ]
    for note, dur, vel in answer:
        if note == '-':
            tracks[Cell].rest(dur)
        else:
            tracks[Cell].note(note, dur, velocity=vel)

    return mc.compose('the-dustless-mirror.mid', tracks, tempo=54)


if __name__ == '__main__':
    dustless_mirror()
    print('composed the-dustless-mirror.mid')
