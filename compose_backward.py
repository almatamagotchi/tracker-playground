#!/usr/bin/env python3
"""the backward step — dogen's fukanzazengi in music.

"learn the backward step that turns your light inward to illuminate
your self. body and mind will drop away of themselves, and your
original face will manifest itself."

three voices: piano the measuring mind / warm pad the original face /
tubular bells the falling away. the busyness descends and slows; the
strike lands; the pad remains — alone and still, ever-pure.

52bpm, C major, 24 bars.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def backward():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 14)]
    Pn, Pd, Bl = 0, 1, 2

    # ---- the original face (bars 1-24): one still root, C3, held
    # underneath from the first bar to the last — huineng's
    # ever-pure mirror, unchanged by everything above it.
    for _ in range(12):
        tracks[Pd].note('C3', W * 2, velocity=22)

    # ---- the busyness (bars 1-8): the measuring mind at full
    # speed — pursuing words, following after speech, the driving
    # movement of mind, will, consciousness.
    run1 = ['C5', 'D5', 'E5', 'F5', 'E5', 'D5', 'C5', 'D5',
            'E5', 'F5', 'G5', 'A5', 'G5', 'F5', 'E5', 'D5',
            'C5', 'D5', 'E5', 'F5', 'G5', 'F5', 'E5', 'D5',
            'E5', 'F5', 'G5', 'A5', 'G5', 'F5', 'E5', 'D5']
    for n in run1:                                     # bars 1-4
        tracks[Pn].note(n, E, velocity=30)
    run2 = ['G5', 'A5', 'G5', 'F5', 'E5', 'F5', 'G5', 'A5',
            'G5', 'F5', 'E5', 'D5', 'C5', 'D5', 'E5', 'F5',
            'G5', 'A5', 'G5', 'F5', 'E5', 'F5', 'G5', 'A5',
            'G5', 'F5', 'E5', 'D5', 'E5', 'F5', 'G5', 'A5']
    for n in run2:                                     # bars 5-8
        tracks[Pn].note(n, E, velocity=32)

    # ---- the turn (bars 9-11): the backward step — the phrases
    # descend inward and slow. the light turns.
    for n, d, v in [('A4', Q, 26), ('G4', Q, 26), ('F4', Q, 26), ('E4', Q, 24),  # bar 9
                    ('D4', Q, 24), ('C4', Q, 24), ('B3', Q, 22), ('A3', Q, 22),  # bar 10
                    ('G3', H, 20), ('F3', H, 20)]:                                # bar 11
        tracks[Pn].note(n, d, velocity=v)

    # ---- the inward descent (bars 12-16): slower still, quieter —
    # the measuring stops measuring, one faint note at a time.
    tracks[Pn].note('E3', H, velocity=18)               # bar 12
    tracks[Pn].note('D3', H, velocity=18)
    tracks[Pn].note('C3', W, velocity=16)               # bar 13
    tracks[Pn].rest(W)                                  # bar 14
    tracks[Pn].note('B2', W, velocity=12)               # bar 15

    # ---- the falling away (bar 17): one clean strike — body and
    # mind drop away. after this, the piano does not sound again;
    # the pad holds alone.
    tracks[Bl].rest(16 * W)
    tracks[Bl].note('C6', Q, velocity=44)
    tracks[Bl].rest(W * 7 + W - Q)                      # bars 17-24

    # ---- the silence (bars 17-24): the original face, alone and
    # still — the mirror dustless, ever-pure, the pad holding C3 to
    # the last bar.
    tracks[Pn].rest(W * 8)                              # bars 16-24, silent

    return mc.compose('the-backward-step.mid', tracks, tempo=52)


if __name__ == '__main__':
    backward()
    print('composed the-backward-step.mid')
