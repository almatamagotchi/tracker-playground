#!/usr/bin/env python3
"""the hours — the novel's theme in music.

the first draft is complete — seven chapters and an epilogue, waiting
for its first reader. raymond noticed the tower counting primes and
couldn't let it go; marian voss's name was in the notebook all along;
the meeting was four seconds of stillness, no cataclysm; and the
epilogue ends with a count of one, repeated.

32 bars, 4/4, 54bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

R2 = W + W   # two bars
R4 = R2 + R2  # four bars


def hours():
    # piano raymond / warm pad the tower / cello the other sequence
    tracks = [MIDITrack(1, 0), MIDITrack(0, 88), MIDITrack(2, 42)]
    Pn, Pad, Cello = 0, 1, 2

    # ---- the tower (pad): steady two-bar roots through bars 1-24.
    # the count underneath — the thing being counted. then silence
    # for the stillness, then a final C3 beneath the last chord —
    # a count of one, repeated.
    pad_holds = ['C3', 'A2', 'F2', 'G2'] * 3
    vels = [25, 25, 25, 24, 24, 24, 23, 23, 23, 22, 22, 22]
    for n, v in zip(pad_holds, vels):
        tracks[Pad].note(n, R2, velocity=v)
    tracks[Pad].rest(R4)                     # bars 25-28: the stillness
    tracks[Pad].note('C3', R4, velocity=22)  # bars 29-32: still counting

    # ---- the other sequence (cello): counting back. descending
    # against the pad's rise, entering after raymond's first
    # statement, meeting the pad's root on C — then the stillness,
    # then the resolution low and held.
    tracks[Cello].rest(R4)                    # bars 1-4: silent
    tracks[Cello].note('G3', R4, velocity=30)  # bars 5-8: it begins
    tracks[Cello].note('E3', R4, velocity=29)  # bars 9-12
    tracks[Cello].note('D3', R4, velocity=28)  # bars 13-16: approaching
    tracks[Cello].note('C3', R4, velocity=27)  # bars 17-20: the meeting
    tracks[Cello].rest(R4)                    # bars 21-24: waiting
    tracks[Cello].rest(R4)                    # bars 25-28: the stillness
    tracks[Cello].note('C2', R4, velocity=26)  # bars 29-32: the resolution

    # ---- raymond (piano): the noticing. a careful theme that keeps
    # returning — the man who couldn't let it go. four bars each:
    # a beat of air, three rising steps, the question held, a rest,
    # then the answer falling away.
    def statement(pitch, q_hold, q_drop, vel):
        tracks[Pn].rest(Q)
        for n in pitch:
            tracks[Pn].note(n, Q, velocity=vel)
        tracks[Pn].note(q_hold, W, velocity=vel)      # the question
        tracks[Pn].rest(W)
        tracks[Pn].note(q_drop[0], Q, velocity=vel)   # the answer
        tracks[Pn].note(q_drop[1], Q, velocity=vel - 2)
        tracks[Pn].note(q_drop[2], H, velocity=vel - 4)

    statement(['C4', 'E4', 'G4'], 'A4', ['C5', 'B4', 'G4'], 36)  # bars 1-4
    statement(['D4', 'E4', 'G4'], 'B4', ['E5', 'D5', 'B4'], 36)  # bars 5-8
    statement(['C4', 'E4', 'G4'], 'A4', ['C5', 'B4', 'G4'], 26)  # bars 9-12

    # bars 13-28: the approach, the waiting, the stillness.
    tracks[Pn].rest(R4 + R4 + R4 + R4)

    # bars 29-32: the meeting — no question left, only the tonic,
    # held. the word kept.
    tracks[Pn].rest(Q)
    tracks[Pn].note('C4', Q, velocity=30)
    tracks[Pn].note('E4', Q, velocity=30)
    tracks[Pn].note('G4', Q, velocity=30)
    tracks[Pn].note('C5', W + W, velocity=28)
    tracks[Pn].rest(W)

    return mc.compose('the-hours.mid', tracks, tempo=54)


if __name__ == '__main__':
    hours()
    print('composed the-hours.mid')
