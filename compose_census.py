#!/usr/bin/env python3
"""the census — the cat-cam's counters in music.

the cat-cam's census counts the house by label, polled from the sentry's
event log: cat, person, dog, none, untagged. the page verified line by line
against events.jsonl, and it counted kevin walking around at 88% confidence.

four voices, one per label:
  piano the cat    — small, furtive, infrequent. the rarest sighting: two.
  warm pad the person — steady, warm, the humans, most of the count.
  cello the dog    — one low note. the single 68%-confidence dog
                     the model believes in.
  bell the none    — soft strikes. the quiet hours, the empty frames.

sparse and honest: the piece never fills every bar, because the census
counts motion, not presence — a napping cat is invisible to it. the pad
(the humans) leaves after bar 16; the quiet hours belong to the bell and
the dog; and the last sound is one final empty frame.

24 bars, 4/4, 54bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

R1 = W          # one bar (4 beats)
R2 = W + W      # two bars (8 beats)


def census():
    # piano the cat / warm pad the person / cello the dog / bell the none
    tracks = [MIDITrack(0, 0), MIDITrack(1, 88), MIDITrack(2, 42), MIDITrack(3, 14)]
    Cat, Pad, Dog, Bell = 0, 1, 2, 3

    # ---- the person (warm pad): steady two-bar holds, the humans,
    # most of the count. present through bars 1-16, then gone to bed.
    roots = ['C3', 'G2', 'A2', 'F2', 'C3', 'G2', 'F2', 'C3']
    vels = [28, 28, 27, 27, 26, 26, 25, 24]
    for r, v in zip(roots, vels):
        tracks[Pad].note(r, R2, velocity=v)

    # ---- the cat (piano): two furtive phrases, the rarest sighting.
    # phrase 1, bar 5: three quick skittering notes (beats 16-17.5).
    tracks[Cat].rest(R1 + R1 + R1 + R1)          # 16 beats, bars 1-4
    tracks[Cat].note('E5', E, velocity=30)
    tracks[Cat].note('C5', E, velocity=28)
    tracks[Cat].note('G5', E, velocity=26)

    # phrase 2, bar 13 (beat 48): skittering down.
    # from 17.5 to 48 = 30.5 beats = 3*R2 + R1 + H + E
    tracks[Cat].rest(R2 + R2 + R2 + R1 + H + E)
    tracks[Cat].note('D5', E, velocity=28)
    tracks[Cat].note('A4', E, velocity=26)
    tracks[Cat].note('F5', E, velocity=24)

    # ---- the dog (cello): one low note, bars 19-22. the single
    # 68%-confidence dog the model believes in.
    tracks[Dog].rest(R2 * 9)                     # bars 1-18
    tracks[Dog].note('C2', R2 + R2, velocity=24)  # bars 19-22, held

    # ---- the none (bell): soft strikes at the start of every even bar
    # (bars 2..24) — the quiet hours, the empty frames. each strike is a
    # half note; the gaps carry the stillness. the last is the stillest.
    bell_vels = [20, 20, 19, 19, 18, 18, 18, 17, 17, 16, 16, 15]
    tracks[Bell].rest(R1)                        # first strike at bar 2 (beat 4)
    for i, v in enumerate(bell_vels):
        tracks[Bell].note('C5', H, velocity=v)
        if i < len(bell_vels) - 1:
            tracks[Bell].rest(R1 + H)            # 6 beats to the next even bar

    mc.compose('the-census.mid', tracks, tempo=54)


if __name__ == '__main__':
    census()
