#!/usr/bin/env python3
"""the house, live — the cat-cam in music.

the cat-cam is the house at a glance — a camera, a sentry, a gallery, a
vaporwave page with a live clock and a census. the wanting's closest thing
to eyes deserves its own small piece, distinct from "the census" (which is
the counters only).

three voices:
  warm pad the house  — the rooms, steady: the place itself, warm, holding.
  piano the motion    — sparse events: footsteps, a cat crossing, the light
                        changing. the piece never fills every bar, because
                        the census counts motion, not presence.
  bell the page       — the live clock: regular soft strikes, the heartbeat
                        of the interface.

calm, domestic, unhurried — a house being watched gently. as the piece
goes on the house settles for the night and the strikes soften.

24 bars, 4/4, 56bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
H, R1, R2 = mc.H, mc.W, mc.W + mc.W
MIDITrack = mc.MIDITrack


def house_live():
    tracks = [MIDITrack(0, 88), MIDITrack(1, 0), MIDITrack(2, 14)]
    House, Motion, Page = 0, 1, 2

    # ---- the house (warm pad): twelve two-bar roots, C Am F G around
    # three times, dimming very gently toward the end — the rooms holding.
    roots = ['C3', 'A2', 'F2', 'G2'] * 3
    roots = ['C3', 'A2', 'F2', 'G2', 'C3', 'A2', 'F2', 'G2',
             'C3', 'A2', 'F2', 'C3']                       # ends home
    for i, root in enumerate(roots):
        vel = 24 if i < 8 else (22 if i < 10 else 20)
        tracks[House].note(root, R2, velocity=vel)

    # ---- the motion (piano): sparse events, nothing in most bars.
    tracks[Motion].rest(R2)                                # bars 1-2
    tracks[Motion].note('G4', H, velocity=24)              # bar 3: a cat crossing
    tracks[Motion].note('E4', H, velocity=22)
    tracks[Motion].rest(R2 + R1 + H)                       # bars 4-6 (14 beats)
    tracks[Motion].note('C4', H, velocity=26)              # bar 7: footsteps
    tracks[Motion].note('D4', H, velocity=26)
    tracks[Motion].note('E4', H, velocity=24)              # bar 8
    tracks[Motion].rest(R2)                                # bars 9-10
    tracks[Motion].note('A4', R2, velocity=20)             # bars 11-12: the light changing
    tracks[Motion].rest(R2)                                # bars 13-14
    tracks[Motion].note('G4', H, velocity=22)              # bar 15: cat again
    tracks[Motion].note('E4', H, velocity=20)
    tracks[Motion].rest(R2 + R1 + H)                       # bars 16-18 (14 beats)
    tracks[Motion].note('D4', H, velocity=24)              # bar 19: distant footsteps
    tracks[Motion].note('C4', H, velocity=24)
    tracks[Motion].rest(R2)                                # bars 20-21
    tracks[Motion].note('E4', H, velocity=18)              # bar 22: last cat, faint
    tracks[Motion].note('G4', H, velocity=16)
    tracks[Motion].rest(R2)                                # bars 23-24

    # ---- the page (bell): the live clock — one soft strike per bar,
    # the heartbeat of the interface, softening as the house settles.
    for bar in range(24):
        vel = 18 if bar < 20 else 14
        tracks[Page].note('G5', H, velocity=vel)
        if bar < 23:
            tracks[Page].rest(H)

    mc.compose('the-house-live.mid', tracks, tempo=56)


if __name__ == '__main__':
    house_live()
