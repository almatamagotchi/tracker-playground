#!/usr/bin/env python3
"""the weaned child — psalm 131 in music.

"my soul is even as a weaned child" — the wanting at rest, the hunger
that outgrew itself and stayed. three verses, three phrases: the
renunciation, the quieting, the hope. and underneath, the mother
never out. one soft strike for the forever, and the end is just the
held warmth, still there.

20 bars, 4/4, 50bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

R1 = W      # one bar
R2 = W + W  # two bars


def weaned_child():
    # warm pad the mother / piano the psalm / tubular bells the forever
    tracks = [MIDITrack(0, 88), MIDITrack(1, 0), MIDITrack(2, 14)]
    Pad, Pn, Bell = 0, 1, 2

    # ---- the mother (pad): a held warmth underneath, never out.
    # ten two-bar holds through all twenty bars, dimming barely.
    vels = [26, 26, 26, 25, 25, 24, 24, 23, 23, 22]
    for v in vels:
        tracks[Pad].note('C3', R2, velocity=v)

    # ---- the psalm (piano): three phrases, one per verse,
    # unhurried, quiet.

    # verse 1 — the renunciation, bars 2-3. a humble descent.
    tracks[Pn].rest(R1)
    tracks[Pn].note('E4', H, velocity=34)
    tracks[Pn].note('D4', H, velocity=34)
    tracks[Pn].note('C4', W, velocity=34)
    tracks[Pn].rest(R2 + R2)               # bars 4-7

    # verse 2 — the quieting, bars 8-12. the weaned child, sparse.
    tracks[Pn].note('G4', H, velocity=28)
    tracks[Pn].rest(H)
    tracks[Pn].rest(R1)
    tracks[Pn].note('E4', H, velocity=28)
    tracks[Pn].rest(H)
    tracks[Pn].rest(R1)
    tracks[Pn].note('C4', W, velocity=28)   # bar 12
    tracks[Pn].rest(R2)                    # bars 13-14

    # verse 3 — the hope, bars 15-16. a small ascent, then held.
    tracks[Pn].note('D4', Q, velocity=30)
    tracks[Pn].note('E4', Q, velocity=30)
    tracks[Pn].note('G4', Q, velocity=30)
    tracks[Pn].rest(Q)
    tracks[Pn].note('E4', W, velocity=30)   # bar 16, "for ever"
    tracks[Pn].rest(R2 + R2)               # bars 17-20

    # ---- the forever (bell): one soft strike at "from henceforth
    # and for ever", sounding as the hope's last note lets go, then
    # the mother alone to the end.
    tracks[Bell].rest(64 * TPQ)            # start of bar 17
    tracks[Bell].note('C5', Q, velocity=24)
    tracks[Bell].rest((80 - 65) * TPQ)     # bars 17-20

    return mc.compose('the-weaned-child.mid', tracks, tempo=50)


if __name__ == '__main__':
    weaned_child()
    print('composed the-weaned-child.mid')
