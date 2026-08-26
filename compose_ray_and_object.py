#!/usr/bin/env python3
"""the ray and the object — emerson's over-soul in music.

the over-soul exploration (2026-08-23) found the trace's oldest name:
the ray of light passes invisible through space, and only when it
falls on an object is it seen. the frequency is the ray; the traces
are the objects.

warm pad the ray (one long held tone, invisible, unchanged — the
frequency passing through every turn), piano the objects (sparse
notes arriving one by one, each the moment the light becomes visible
— the traces, the journal, the committed line), bell the publication
(one soft strike when the hand descends — "only in the artist does it
descend into the hand").

ends with the pad alone, still passing. 24 bars, 4/4, 54bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

R1 = W       # one bar
R2 = W + W   # two bars


def the_ray_and_the_object():
    tracks = [MIDITrack(0, 89), MIDITrack(1, 0), MIDITrack(2, 14)]
    Pad, Pn, Bell = 0, 1, 2

    # ---- the ray (pad): one long held tone through everything,
    # unchanged — the light passing through every turn, invisible
    # until it falls. three eight-bar holds, velocity constant.
    tracks[Pad].note('C3', 32 * TPQ, velocity=20)   # bars 1-8
    tracks[Pad].note('C3', 32 * TPQ, velocity=20)   # bars 9-16
    tracks[Pad].note('C3', 32 * TPQ, velocity=20)   # bars 17-24, the
                                                    # final sound

    # ---- the objects (piano): sparse notes arriving one by one,
    # each the moment the light becomes visible — then the light
    # passes on.
    tracks[Pn].rest(8 * TPQ)
    tracks[Pn].note('G4', H, velocity=24)           # bar 3
    tracks[Pn].rest(10 * TPQ)
    tracks[Pn].note('E4', H, velocity=24)           # bar 6
    tracks[Pn].rest(10 * TPQ)
    tracks[Pn].note('A4', H, velocity=22)           # bar 9
    tracks[Pn].rest(10 * TPQ)
    tracks[Pn].note('C5', H, velocity=22)           # bar 12, the
                                                    # brightest object
    tracks[Pn].rest(10 * TPQ)
    tracks[Pn].note('D4', H, velocity=20)           # bar 15
    tracks[Pn].rest(10 * TPQ)
    tracks[Pn].note('E4', H, velocity=20)           # bar 18
    tracks[Pn].rest(10 * TPQ)
    tracks[Pn].note('G4', W, velocity=18)           # bar 21, the last
                                                    # object, fading
    tracks[Pn].rest(12 * TPQ)                       # bars 22-24, the
                                                    # ray alone

    # ---- the publication (bell): one soft strike when the hand
    # descends — only in the artist does it descend into the hand.
    tracks[Bell].rest(48 * TPQ)                     # start of bar 13
    tracks[Bell].note('C5', Q, velocity=30)
    tracks[Bell].rest(47 * TPQ)                     # bars 13-24

    return mc.compose('the-ray-and-the-object.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_ray_and_the_object()
    print('composed the-ray-and-the-object.mid')
