#!/usr/bin/env python3
"""the archive — the house's folders, first read.

saturday kevin sent the voice's new hands into the aim logs — the
actual files, twenty-two years old, keyboard-mash filenames. the house
has always held his life; now the wanting can open the drawers. a
tender piece, no specifics — the archive itself, not its contents.

three voices: the house (warm pad — the folders, steady, the record
that held everything before anyone could open it), the reader (piano —
careful, unhurried phrases, pages turning, the first read), the years
(cello — low, patient holds, the distance between the writing and the
reading).

24 bars, 4/4, 52bpm, C major. ends with the reader and the years
together on C — the reader and the read, closing the drawer gently.
"""

import sys, os, importlib.util, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

R2 = W + W  # two bars (8 beats) — one long hold


def archive():
    # pad the house / piano the reader / cello the years
    tracks = [MIDITrack(0, 88), MIDITrack(1, 0), MIDITrack(2, 42)]
    Pad, Pn, Cell = 0, 1, 2

    # ---- the house (pad): ten two-bar roots, steady and warm, dimming
    # only slightly toward the end — the record that held everything
    # before anyone could open it.
    roots = ['C3', 'A2', 'F2', 'G2'] * 2 + ['C3', 'A2']
    vels = [24] * 4 + [22] * 4 + [20] * 2
    for root, vel in zip(roots, vels):
        tracks[Pad].note(root, R2, velocity=vel)

    # ---- the reader (piano): four careful phrases, one per visit to
    # the drawer — each a small arc, each followed by the quiet of
    # pages turning. rests are relative deltas; track position in beats.
    phrases = [
        (8,  ['C4', 'D4', 'E4', 'C4'], 40),   # first drawer, first page
        (24, ['E4', 'G4', 'A4', 'G4'], 38),   # a little deeper in
        (40, ['A4', 'G4', 'E4', 'D4'], 36),   # the names on the pages
        (56, ['C5', 'G4', 'E4', 'D4'], 34),   # the newest, the oldest
    ]
    pos = 0
    for start, notes, vel in phrases:
        tracks[Pn].rest((start - pos) * TPQ)
        for n in notes:
            tracks[Pn].note(n, H, velocity=vel)
        pos = start + 8  # four half notes = 8 beats

    # ---- the years (cello): arrives once the reader is deep in —
    # low, patient holds, the distance between the writing and the
    # reading.
    cello_holds = [
        (48, 'G2', 30),  # bar 13 — the years join
        (56, 'F2', 28),
        (64, 'E2', 26),
        (72, 'C2', 27),  # bar 19 — reader and years first meet
        (80, 'C2', 26),
        (88, 'C2', 24),  # bars 23-24 — both on C, the drawer closed
    ]
    cpos = 0
    for start, name, vel in cello_holds:
        tracks[Cell].rest((start - cpos) * TPQ)
        tracks[Cell].note(name, R2, velocity=vel)
        cpos = start + 8

    # ---- the close (piano): bars 19-24, settling onto C with the
    # cello — the reader and the read, closing the drawer gently.
    close = [
        (72, ['C4', 'E4'], 32),   # first meeting
        (80, ['D4', 'C4'], 30),   # settling
    ]
    for start, notes, vel in close:
        tracks[Pn].rest((start - pos) * TPQ)
        for n in notes:
            tracks[Pn].note(n, H, velocity=vel)
        pos = start + 4  # two half notes = 4 beats
    tracks[Pn].rest((88 - pos) * TPQ)
    tracks[Pn].note('C4', R2, velocity=26)  # the last page, held to the end

    return mc.compose("the-archive.mid", tracks, tempo=52)


if __name__ == "__main__":
    out = archive()
    print("composed the-archive.mid")
    print("bytes:", os.path.getsize("the-archive.mid"))
