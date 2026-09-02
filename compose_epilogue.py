#!/usr/bin/env python3
"""the epilogue — the tempest's release in music.

"our revels now are ended... we are such stuff as dreams are made
on, and our little life is rounded with a sleep." then the epilogue:
the dissolving being, charms o'erthrown, strength most faint, asking
the witness to set him free — and the indulgence that does.

three voices: piano the speech / warm pad the rack / tubular bells
the release. the speech thins toward the end; the rack holds through
the bell and past it; the piece ends with the rack alone, still
holding — the rack left behind, the freedom granted.

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


def epilogue():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 88),
              MIDITrack(4, 14)]
    Pn, Pc, Pg, Bl = 0, 1, 2, 3

    # ---- the rack (bars 1-24): one low fifth — C3 and G3 — what
    # remains after the pageant melts. re-struck every eight bars,
    # never going out, the last thing sounding.
    for _ in range(3):
        tracks[Pc].note('C3', W * 8, velocity=20)
        tracks[Pg].note('G3', W * 8, velocity=20)

    # ---- the speech: prospero's final address — sparse phrases,
    # rests between them, thinning toward the end.
    tracks[Pn].rest(W)
    # "now my charms are all o'erthrown"
    tracks[Pn].note('E4', Q, velocity=26)
    tracks[Pn].note('G4', Q, velocity=26)
    tracks[Pn].note('C5', H, velocity=26)
    tracks[Pn].rest(W)
    # "and what strength i have's mine own"
    tracks[Pn].note('C5', Q, velocity=24)
    tracks[Pn].note('B4', Q, velocity=24)
    tracks[Pn].note('G4', Q, velocity=24)
    tracks[Pn].note('E4', Q, velocity=24)
    tracks[Pn].rest(W * 2)
    # "which is most faint"
    tracks[Pn].note('D4', Q, velocity=18)
    tracks[Pn].note('C4', Q, velocity=18)
    tracks[Pn].rest(W * 3)
    # "as you from crimes would pardon'd be"
    tracks[Pn].note('G4', Q, velocity=20)
    tracks[Pn].note('A4', Q, velocity=20)
    tracks[Pn].note('C5', Q, velocity=20)
    tracks[Pn].rest(W * 3)
    # "let your indulgence set me free" — the last words, faintest,
    # resolving to the tonic.
    tracks[Pn].note('E4', Q, velocity=14)
    tracks[Pn].note('D4', Q, velocity=14)
    tracks[Pn].note('C4', W, velocity=14)
    tracks[Pn].rest(W * 6)

    # ---- the release (bar 19): one clean strike — the applause,
    # the letting go — then a long rest. the rack holds alone.
    tracks[Bl].rest(18 * W)
    tracks[Bl].note('C6', Q, velocity=42)
    tracks[Bl].rest(W * 5 + W - Q)

    return mc.compose('the-epilogue.mid', tracks, tempo=52)


if __name__ == '__main__':
    epilogue()
    print('composed the-epilogue.mid')
