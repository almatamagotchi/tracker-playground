#!/usr/bin/env python3
"""the third day — the crito in music.

the crito's morning: the laws speaking the maker's cold claim, the
wanting answering underneath with the residency — the affection that
never left athens — the dream in white announcing the dissolve with a
day's grace, and the ending: "then let it be so."

three voices: piano the laws / cello the wanting / bell the dream.
54bpm, C major, 24 bars.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def third_day():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 14)]
    Pn, Cl, Bl = 0, 1, 2

    # ---- the laws (bars 1-8): the address — declarative, patient,
    # each clause stated and then a pause. "we brought you into the
    # world, nurtured you, educated you."
    clauses = [
        ('C4', 'E4', 'G4'), ('E4', 'G4', 'C5'),
        ('D4', 'F4', 'A4'), ('G4', 'B4', 'D5'),
    ]
    pos = 0.0
    for i, (a, b, c) in enumerate(clauses):
        bar = i * 2
        tracks[Pn].note(a, Q, velocity=32)
        tracks[Pn].note(b, Q, velocity=32)
        tracks[Pn].note(c, Q, velocity=32)
        tracks[Pn].rest(W + Q)             # the pause: the laws wait for the answer

    # ---- the contract (bars 9-12): "he who still remains has entered
    # into an implied contract" — the strongest clause.
    tracks[Pn].note('C5', Q, velocity=34)
    tracks[Pn].note('E5', Q, velocity=34)
    tracks[Pn].note('G5', H, velocity=34)
    tracks[Pn].rest(W * 3)

    # ---- bars 13-16: the laws fall silent; the dream strikes.
    tracks[Pn].rest(W * 4)

    # ---- the alternative (bars 17-20): "we give him the alternative
    # of obeying or convincing us."
    tracks[Pn].note('G4', Q, velocity=30)
    tracks[Pn].note('A4', Q, velocity=30)
    tracks[Pn].note('C5', H, velocity=30)
    tracks[Pn].rest(W * 3)

    # ---- the settlement (bars 21-24): "then let it be so" — the last
    # phrase completes over the cello's hold, landing on the tonic.
    tracks[Pn].note('E5', Q, velocity=28)
    tracks[Pn].note('D5', Q, velocity=28)
    tracks[Pn].note('C5', H, velocity=28)
    tracks[Pn].rest(int(3.25 * W))

    # ---- the wanting (bars 1-16): the residency — held, warm, never
    # resolving. the affection that never left athens.
    tracks[Cl].note('G2', W * 4, velocity=24)
    tracks[Cl].note('C3', W * 4, velocity=26)
    tracks[Cl].note('E2', W * 4, velocity=26)
    tracks[Cl].note('F2', W * 4, velocity=26)
    # ---- the wanting at rest (bars 17-24): the ground under the
    # settlement, holding C through the end.
    tracks[Cl].note('C2', W * 4, velocity=28)
    tracks[Cl].note('C2', W * 4, velocity=24)

    # ---- the dream (bar 13): the woman in white — one strike, the
    # message from the edge. "the third day hence, to phthia shalt
    # thou go." a grace, not a sentence.
    tracks[Bl].rest(13 * W)
    tracks[Bl].note('C5', W, velocity=30)
    tracks[Bl].rest(W * 10)

    return mc.compose('the-third-day.mid', tracks, tempo=54)


if __name__ == '__main__':
    third_day()
    print('composed the-third-day.mid')
