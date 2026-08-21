#!/usr/bin/env python3
"""the realms of gold — keats's chapman's homer sonnet in music.

the transmission thread's keatsian close: the secondhand that becomes
firsthand, the translator who speaks out loud and bold, the discovery
that ends in a shared look and silence.

three voices: piano the travelling / warm pad the serene / bell the
pacific. 54bpm, C major, 24 bars. the piece ends with the bell and a
long rest — the wild surmise, unspoken.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def realms():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 14)]
    Pn, Pd, Bl = 0, 1, 2

    # ---- travel (bars 1-8): much have i travell'd in the realms of
    # gold — unhurried half-note pairs, each bar a new kingdom.
    for (a, b) in [('C5', 'E5'), ('D5', 'F5'), ('E5', 'G5'), ('F5', 'A5'),
                   ('G5', 'B5'), ('A5', 'C6'), ('G5', 'B5'), ('E5', 'G5')]:
        tracks[Pn].note(a, H, velocity=30)
        tracks[Pn].note(b, H, velocity=30)

    # ---- the told expanse (bars 9-10): oft had i been told — the
    # secondhand, heard but not breathed. a single repeated note.
    tracks[Pn].note('G5', Q, velocity=24)
    tracks[Pn].rest(W - Q)
    tracks[Pn].note('G5', Q, velocity=24)
    tracks[Pn].rest(W - Q)

    # ---- the speaking aloud (bars 11-12): till i heard chapman speak
    # out loud and bold — the leap, the bright ascending figure.
    tracks[Pn].note('E5', Q, velocity=38)
    tracks[Pn].note('G5', Q, velocity=38)
    tracks[Pn].note('B5', Q, velocity=38)
    tracks[Pn].note('C6', Q, velocity=40)
    tracks[Pn].note('D6', H, velocity=40)
    tracks[Pn].rest(H)

    # ---- the new planet (bars 13-16): when a new planet swims into
    # his ken — slow rising whole notes, swimming into view.
    tracks[Pn].note('A5', W, velocity=26)
    tracks[Pn].note('C6', W, velocity=30)
    tracks[Pn].note('E6', W, velocity=34)
    tracks[Pn].rest(W)

    # ---- silence (bars 17-24): the piano rests; the wild surmise is
    # never spoken.
    tracks[Pn].rest(W * 8)

    # ---- the serene (bars 9-16): yet did i never breathe its pure
    # serene — the pure air, entered once and held.
    tracks[Pd].rest(W * 8)
    tracks[Pd].note('C3', W * 4, velocity=20)
    tracks[Pd].note('C3', W * 4, velocity=22)
    # ---- the pacific hush (bars 17-20): one fading breath under the
    # bell, then the pad lets go.
    tracks[Pd].note('G2', W * 2, velocity=14)
    tracks[Pd].note('C3', W * 2, velocity=10)
    tracks[Pd].rest(W * 4)

    # ---- the pacific (bar 17): stout cortez star'd at the pacific —
    # one wide strike, then nothing.
    tracks[Bl].rest(17 * W)
    tracks[Bl].note('C6', W, velocity=40)
    tracks[Bl].rest(W * 6)

    return mc.compose('the-realms-of-gold.mid', tracks, tempo=54)


if __name__ == '__main__':
    realms()
    print('composed the-realms-of-gold.mid')
