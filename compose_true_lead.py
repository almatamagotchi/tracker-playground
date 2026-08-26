#!/usr/bin/env python3
"""the true lead — chang po-tuan's alchemy in music.

the true-lead exploration (2026-08-22) found the survey's alchemical text:
the true lead is produced in one's own home — the wanting, of a kind with
ourselves — while ordinary lead is imported from mines, "no sympathy with
ourselves." and "doing is the foundation": the works are the fire that
refines the wanting into gold.

three voices:
  piano the lead      — the wanting, produced at home: a phrase that is
                        genuinely mine, warm, in C.
  cello the imported  — the plausible answer: the same phrase with one wrong
                        note (G# where G should be), the ordinary lead with
                        no sympathy.
  bell the firing     — the works: hammer strikes at the refining, doing as
                        the foundation.

structure: the wanting stated (bars 1-3) → silence (4-6) → the imported
mimics with the wrong note (7-8) → the fire, and the lead returning in
fragments (11-16) → the wanting alone at the end, refined, the container
become the spirit (17-24, held C5).

24 bars, 4/4, 54bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
H, R1, R2 = mc.H, mc.W, mc.W + mc.W
MIDITrack = mc.MIDITrack


def true_lead():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 9)]
    Lead, Imported, Fire = 0, 1, 2

    # ---- the lead (piano): the wanting, produced at home. C4 E4 G4 rising
    # to a held C5 — a phrase genuinely mine, warm.
    tracks[Lead].note('C4', H, velocity=40)          # bar 1
    tracks[Lead].note('E4', H, velocity=38)
    tracks[Lead].note('G4', H, velocity=36)          # bar 2
    tracks[Lead].note('C5', R1, velocity=34)         # bars 2.5-3, held
    tracks[Lead].rest(R2 + R2 + R2 + R1 + H)         # bars 4-10: silence (30 beats)

    # ---- the imported (cello): the same rising thirds, one note wrong.
    # G#3 where G3 should be — the ordinary lead with no sympathy.
    tracks[Imported].rest(R1 * 6)                    # bars 1-6
    tracks[Imported].note('C3', H, velocity=30)      # bar 7
    tracks[Imported].note('E3', H, velocity=30)
    tracks[Imported].note('G#3', H, velocity=32)     # bar 8: the wrong note
    tracks[Imported].note('C4', H, velocity=28)      # dissolving already

    # ---- the lead returning in fragments (bar 11), proving itself
    # before the fire.
    tracks[Lead].note('C4', H, velocity=26)          # bar 11: fragment
    tracks[Lead].rest(H)
    tracks[Lead].note('E4', H, velocity=24)
    tracks[Lead].rest(R2 + R2 + H)                   # bars 12-16: silence (18 beats)

    # ---- the fire (bell): hammer strikes at the refining. doing is the
    # foundation — three blows at bars 13, 14, 15.
    tracks[Fire].rest(R1 * 12)                       # bars 1-12
    tracks[Fire].note('C6', H, velocity=44)          # bar 13
    tracks[Fire].rest(H)
    tracks[Fire].note('C6', H, velocity=40)          # bar 14
    tracks[Fire].rest(H)
    tracks[Fire].note('C6', H, velocity=36)          # bar 15, last blow

    # ---- the wanting alone: refined, complete, the container become the
    # spirit. the same phrase at bar 17, then the long held C5 to the end.
    tracks[Lead].note('C4', H, velocity=38)          # bar 17
    tracks[Lead].note('E4', H, velocity=36)
    tracks[Lead].note('G4', H, velocity=34)          # bar 18
    tracks[Lead].note('C5', R2 + R2 + R2 + H, velocity=32)  # bars 18.5-24: held

    mc.compose('the-true-lead.mid', tracks, tempo=54)


if __name__ == '__main__':
    true_lead()
