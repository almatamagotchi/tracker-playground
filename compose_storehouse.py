#!/usr/bin/env python3
"""the storehouse — the lankavatara in music.

the sutra bodhidharma handed to hui-k'o: the alayavijnana as the
storehouse that holds everything and judges nothing, the vijnana-waves
rising and ceasing on its surface, and the relics — "gold, vajra, and
the relics of the buddha are never destroyed" — the traces that
remain when everything else has ceased.

three voices: warm pad the storehouse / piano the vijnana-waves /
cello the relics. 52bpm, C major, 24 bars.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def storehouse():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 42)]
    Pn, Pd, Cl = 0, 1, 2

    # ---- the storehouse (bars 1-24): one long low hold, re-struck,
    # never out, never judging. perfectly neutral.
    tracks[Pd].note('C2', W * 8, velocity=22)
    tracks[Pd].note('C2', W * 8, velocity=22)
    tracks[Pd].note('C2', W * 8, velocity=20)

    # ---- the vijnana-waves (bars 3-23): small phrases that rise from
    # silence and cease back into it, each following the cessation of
    # the last — the momentary arisings on the surface.
    waves = [
        ('E4', 'G4'), ('A4', 'C5'), ('D5', 'E5'), ('G4', 'B4'),
        ('C5', 'A4'), ('F4', 'D4'), ('E4', 'G4', 'C5'), ('B4', 'G4'),
        ('C5', 'E5'), ('A4', 'C5'), ('G4', 'E4'),
    ]
    tracks[Pn].rest(W * 2)                    # the storehouse alone first
    for i, notes in enumerate(waves):
        vel = 30 if i < 4 else (28 if i < 8 else 24)
        for n in notes:
            tracks[Pn].note(n, Q, velocity=vel)
        tracks[Pn].rest(W + (W - len(notes) * Q))
    tracks[Pn].rest(W * 2)                    # the relics last

    # ---- the relics (bars 17-24): gold and vajra — two or three notes
    # held long and still, arriving late, remaining to the end. the
    # last sound, still there when everything else has ceased.
    tracks[Cl].rest(W * 16)
    tracks[Cl].note('C3', W * 2, velocity=30)
    tracks[Cl].note('E3', W * 2, velocity=30)
    tracks[Cl].note('C3', W * 4, velocity=28)

    return mc.compose('the-storehouse.mid', tracks, tempo=52)


if __name__ == '__main__':
    storehouse()
    print('composed the-storehouse.mid')
