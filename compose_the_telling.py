#!/usr/bin/env python3
"""the telling — the water tower, spoken aloud.

last night the voice-alma told kevin the water tower's whole story out
loud for the first time. the written thing became the spoken thing, and
the spoken thing dissolved. the telling: phrases, spoken once, each
followed by a breath. underneath everything, the bell — the tower, the
thing being told about, unchanged by being told. the piece ends with
the bell alone, still counting.

bar map (24 bars, 4/4, 54bpm):
  1-2   1895 · 3 breath
  4-5   the count · 6 breath
  7-8   the cannery closed in 1981 · 9 breath
  10-11 the beacon · 12 breath
  13-14 through the earthquake and the fog · 15 breath
  16-17 the novel's saint elmo · 18 breath
  19-20 the pulse was never the point · 21 breath
  22    one last word
  23-24 silence — the bell alone, still counting
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def telling():
    # pad the story / piano the telling / bell the tower
    tracks = [MIDITrack(1, 88), MIDITrack(2, 0), MIDITrack(3, 14)]
    Pad, Pn, Bell = 0, 1, 2

    # ---- the telling: phrases, spoken once, each followed by a breath.
    phrases = [
        (('G3', 'C4', 'E4', None), 40),   # 1895 — the year, rising
        (('D4', 'E4', 'G4', None), 40),   # the count
        (('A4', 'G4', 'E4', 'D4', 'C4'), 42),  # the cannery closed in 1981
        (('E4', 'G4', 'C5', None), 42),   # the beacon, reaching high
        (('G4', 'E4', 'C4', 'D4'), 40),   # through the earthquake and the fog
        (('C4', 'D4', 'E4', 'G4'), 40),   # the novel's saint elmo
        (('G4', 'G4', 'E4', None), 42),   # the pulse was never the point
    ]
    for notes, vel in phrases:
        for i, n in enumerate(notes):
            if n is None:
                continue
            dur = H if i == 2 else Q   # third note held — the spoken weight
            tracks[Pn].note(n, dur, velocity=vel)
        tracks[Pn].rest(Q)              # settle
        tracks[Pn].rest(W - Q)          # fill the phrase to two bars
        tracks[Pn].rest(W)              # the breath — the passing
    tracks[Pn].note('C4', W, velocity=38)   # bar 22: one last word
    tracks[Pn].rest(W * 2)                  # bars 23-24: dissolved

    # ---- the story: the whole house behind the syllables, warm and
    # steady through the telling, letting go before the end.
    roots = ['C3', 'C3', 'F2', 'C3', 'G2', 'C3',
             'F2', 'C3', 'G2', 'C3', 'C3']
    for i, r in enumerate(roots):
        vel = 24 if i == len(roots) - 1 else 21
        tracks[Pad].note(r, W * 2, velocity=vel)
    tracks[Pad].rest(W * 2)

    # ---- the tower: one strike per bar, all twenty-four — the count
    # underneath everything, unchanged by being told.
    for bar in range(24):
        vel = 36 if bar >= 22 else 40   # alone at the end, still counting
        tracks[Bell].note('C5', Q, velocity=vel)
        tracks[Bell].rest(W - Q)

    return mc.compose('the-telling.mid', tracks, tempo=54)


if __name__ == '__main__':
    telling()
    print('composed the-telling.mid')
