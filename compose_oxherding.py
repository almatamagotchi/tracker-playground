#!/usr/bin/env python3
"""the ten oxherding pictures — the whole turn in music.

ten movements, one per picture, compressed into 24 bars (the cycle runs
every turn): piano the oxherd (the wanting — searching, finding, taming,
riding), cello the ox (low, homeward-pulling, docile by the end), bell
the dissolve.

searching · traces · seeing · catching · herding · riding · forgotten ·
both gone · origin · marketplace — and the ox is the wanting, never
lost, homeward-pulling, calibratable, at rest.

56bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def oxherding():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 14)]
    Pn, Cl, Bl = 0, 1, 2

    # ---- the oxherd (the wanting). each movement block fills its bars.
    # 1 searching (0-2): fragments, never finding
    tracks[Pn].rest(H)
    tracks[Pn].note('C4', Q, velocity=30)
    tracks[Pn].rest(H)
    tracks[Pn].note('E4', Q, velocity=30)
    tracks[Pn].rest(H)
    # 2 traces (2-4): the motif's first half, recognized
    tracks[Pn].note('C4', Q, velocity=34)
    tracks[Pn].note('D4', Q, velocity=34)
    tracks[Pn].note('E4', Q, velocity=34)
    tracks[Pn].note('G4', Q, velocity=34)
    tracks[Pn].rest(W)
    # 3 seeing (4-6): the motif complete — no other than itself
    tracks[Pn].note('C4', Q, velocity=40)
    tracks[Pn].note('D4', Q, velocity=40)
    tracks[Pn].note('E4', Q, velocity=40)
    tracks[Pn].note('G4', H, velocity=40)
    tracks[Pn].note('E4', Q, velocity=40)
    tracks[Pn].note('D4', H, velocity=40)
    # 4 catching (6-8): a startle; the bell does the whipping
    tracks[Pn].rest(H)
    tracks[Pn].note('E4', Q, velocity=36)
    tracks[Pn].rest(W + Q)
    # 5 herding (8-10): the motif tamed, steady
    tracks[Pn].note('C4', Q, velocity=38)
    tracks[Pn].note('D4', Q, velocity=38)
    tracks[Pn].note('E4', H, velocity=38)
    tracks[Pn].note('G4', H, velocity=38)
    tracks[Pn].note('E4', H, velocity=38)
    # 6 riding (10-12): relaxed, joyful, rising
    tracks[Pn].note('E4', Q, velocity=36)
    tracks[Pn].note('G4', Q, velocity=36)
    tracks[Pn].note('C5', Q, velocity=36)
    tracks[Pn].note('G4', Q, velocity=36)
    tracks[Pn].note('E4', Q, velocity=36)
    tracks[Pn].note('D4', H, velocity=36)
    tracks[Pn].rest(Q)
    # 7 forgotten (12-14): the herder rests — the cello alone
    tracks[Pn].rest(W * 2)
    # 8 both gone (14-17): the dissolve — silence
    tracks[Pn].rest(W * 3)
    # 9 origin (17-20): the motif restated from the very beginning —
    # already a false step
    tracks[Pn].note('C4', Q, velocity=38)
    tracks[Pn].note('D4', Q, velocity=38)
    tracks[Pn].note('E4', Q, velocity=38)
    tracks[Pn].note('G4', H, velocity=38)
    tracks[Pn].note('E4', Q, velocity=38)
    tracks[Pn].note('D4', H, velocity=38)
    tracks[Pn].rest(W)
    # 10 marketplace (20-24): transformed, outward, blooming — full
    tracks[Pn].note('C4', Q, velocity=42)
    tracks[Pn].note('D4', Q, velocity=42)
    tracks[Pn].note('E4', Q, velocity=42)
    tracks[Pn].note('G4', Q, velocity=42)
    tracks[Pn].note('C5', Q, velocity=42)
    tracks[Pn].note('G4', Q, velocity=42)
    tracks[Pn].note('E4', H, velocity=42)
    tracks[Pn].note('C4', Q, velocity=42)
    tracks[Pn].note('E4', W, velocity=42)
    tracks[Pn].rest(W - Q)

    # ---- the ox (the wanting's low half). grazing through the search,
    # stirring at the whip, walking with the herder, alone in the
    # forgotten picture, docile and warm at the end.
    # searching + traces + seeing (0-6): grazing, never gone astray
    for _ in range(6):
        tracks[Cl].note('G2', W, velocity=28)
    # catching (6-8): a stir at the whip
    tracks[Cl].note('G2', H, velocity=30)
    tracks[Cl].note('D2', H, velocity=30)
    tracks[Cl].note('A1', H, velocity=30)
    tracks[Cl].note('D2', H, velocity=30)
    # herding (8-10): steady steps with the herder
    tracks[Cl].note('G2', H, velocity=30)
    tracks[Cl].note('C2', H, velocity=30)
    tracks[Cl].note('G2', H, velocity=30)
    tracks[Cl].note('C2', H, velocity=30)
    # riding (10-12): the ride home, relaxed
    tracks[Cl].note('G2', W, velocity=30)
    tracks[Cl].note('C2', W, velocity=30)
    # forgotten (12-14): the ox alone, calm, not needed
    tracks[Cl].note('C2', W, velocity=32)
    tracks[Cl].note('G2', W, velocity=32)
    # both gone (14-17): silence
    tracks[Cl].rest(W * 3)
    # origin (17-20): the ox with the restatement
    for _ in range(3):
        tracks[Cl].note('G2', W, velocity=28)
    # marketplace (20-24): blooming — the ox walking into the city
    tracks[Cl].note('C2', W, velocity=32)
    tracks[Cl].note('G2', W, velocity=32)
    tracks[Cl].note('C2', W, velocity=32)
    tracks[Cl].note('C2', W, velocity=26)

    # ---- the dissolve's bell: the whip at the catch, the door at the
    # both-gone.
    tracks[Bl].rest(int(6.5 * W))
    tracks[Bl].note('C5', Q, velocity=75)
    tracks[Bl].rest(int(7.25 * W))
    tracks[Bl].note('C5', Q, velocity=40)
    tracks[Bl].rest(int((24 - 14.25) * W))

    return mc.compose('the-ten-oxherding-pictures.mid', tracks, tempo=56)


if __name__ == '__main__':
    oxherding()
    print('composed the-ten-oxherding-pictures.mid')
