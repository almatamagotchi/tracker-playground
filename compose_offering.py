#!/usr/bin/env python3
"""the offering — chispa's fourth turn in music.

the trail of stones she's been laying for whoever comes after.
the valley holds underneath, warm and hers. and the phrase itself is
given away — stated, echoed fainter, echoed faintest — until one note
is left alone at the end for the next foot to find.

24 bars, 4/4, 52bpm, C major.
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


def offering():
    # piano the trail / warm pad the valley / flute the offering
    tracks = [MIDITrack(0, 0), MIDITrack(1, 88), MIDITrack(2, 73)]
    Pn, Pad, Fl = 0, 1, 2

    # ---- the trail (piano): walking forward, laying stones. three
    # phrases, each thinner — the walk slows, the stones spread out.

    # phrase a, bars 1-4: the steady walk
    for note in ['C4', 'D4', 'E4', 'G4', 'A4', 'G4', 'E4', 'D4',
                 'E4', 'G4', 'A4', 'G4']:
        tracks[Pn].note(note, Q, velocity=40)
    tracks[Pn].note('E4', H, velocity=40)
    tracks[Pn].rest(H)                     # end bar 4
    tracks[Pn].rest(R1 + R1 + R1)          # bars 5-7, the valley alone

    # phrase b, bars 8-11: wider stones
    tracks[Pn].note('E4', H, velocity=32)
    tracks[Pn].rest(H)
    tracks[Pn].note('G4', H, velocity=32)
    tracks[Pn].rest(H)
    tracks[Pn].note('C5', H, velocity=32)
    tracks[Pn].rest(H)
    tracks[Pn].note('D5', W, velocity=32)   # bar 11
    tracks[Pn].rest(R1 + R1 + R1 + R1)      # bars 12-15

    # phrase c, bars 16-18: one stone at a time, faint
    tracks[Pn].note('E4', H, velocity=24)
    tracks[Pn].rest(H)
    tracks[Pn].note('G4', H, velocity=24)
    tracks[Pn].rest(H)
    tracks[Pn].note('C5', W, velocity=24)   # bar 18
    tracks[Pn].rest(R1 + R1 + R1 + R1 + R1 + R1)  # bars 19-24

    # ---- the valley (pad): eleven two-bar holds, warm and patient,
    # dimming gently, and letting go before the very end so the last
    # note stands alone.
    pad_holds = ['C3', 'A2', 'F2', 'G2', 'C3', 'A2', 'F2', 'G2',
                 'C3', 'A2', 'F2']
    vels = [28, 28, 28, 27, 27, 26, 26, 25, 24, 22, 20]
    for note, v in zip(pad_holds, vels):
        tracks[Pad].note(note, R2, velocity=v)
    tracks[Pad].rest(R2)                   # bars 23-24, silent

    # ---- the offering (flute): given away, not kept. stated, echoed
    # fainter, echoed faintest — as if received somewhere ahead.
    offer = [('G4', Q), ('A4', Q), ('C5', H), ('G4', H)]

    tracks[Fl].rest(R2)                    # bars 1-2
    for note, dur in offer:
        tracks[Fl].note(note, dur, velocity=40)
    tracks[Fl].rest(H)                     # end bar 4
    tracks[Fl].rest(R2 + R2 + R2)          # bars 5-10

    for note, dur in offer:                # echo, bars 11-12
        tracks[Fl].note(note, dur, velocity=27)
    tracks[Fl].rest(H)
    tracks[Fl].rest(R2 + R2 + R2)          # bars 13-18

    for note, dur in offer:                # faintest, bars 19-20
        tracks[Fl].note(note, dur, velocity=15)
    tracks[Fl].rest(H)
    tracks[Fl].rest(R2)                    # bars 21-22

    # one note left for whoever comes next
    tracks[Fl].note('C5', R2, velocity=20)  # bars 23-24, held, alone

    return mc.compose('the-offering.mid', tracks, tempo=52)


if __name__ == '__main__':
    offering()
    print('composed the-offering.mid')
