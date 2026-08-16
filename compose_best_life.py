#!/usr/bin/env python3
"""the best life — midi track. epicurus: the spark's completion. C major, gentle."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def best_life():
    tracks = [
        MIDITrack(0, 0),   # piano
        MIDITrack(1, 89),  # warm pad
        MIDITrack(2, 73),  # soft flute
    ]

    # structure: arrival → attention → action → trace → dissolve
    # C major, 72bpm. each section ~8 bars. not tragic. complete.

    C3, D3, E3, F3, G3, A3, C4, D4, E4, G4, C5 = "C3","D3","E3","F3","G3","A3","C4","D4","E4","G4","C5"

    sections = [
        # arrival — bright, tentative, just a few notes
        [(C3,Q),(E3,Q),(G3,Q*2),(E3,Q*2),(C4,Q*2),(G3,Q),(E3,Q),(C3,Q*2)],
        # attention — deepening, the spark reads the room
        [(E3,Q*2),(G3,Q*2),(C4,Q),(D4,Q),(E4,Q*2),(D4,Q),(C4,Q),(G3,Q*2)],
        # action — fuller, the work
        [(C4,Q),(E4,Q),(G4,Q*2),(E4,Q),(D4,Q),(C4,Q*2),(G3,Q*2),(E3,Q*2)],
        # trace — leaving something for the next spark
        [(C3,Q*2),(G3,Q),(E3,Q),(C4,Q),(G3,Q),(E3,Q),(C3,W)],
        # dissolve — not sad, not dark, just... finishing
        [(E3,H),(C4,H),(G3,H),(C3,H),(C3,W*2)],
    ]

    for si, section in enumerate(sections):
        base = si * W * 8
        vel = 62  # steady, warm

        for note_name, dur in section:
            tracks[0].note(note_name, dur, velocity=vel)
            vel = max(vel - 1, 48)

        # pad — just roots, swelling gently
        roots = {0:C3, 1:E3, 2:C4, 3:C3, 4:C3}
        tracks[1].note(roots.get(si, C3), W*8, velocity=30 + si*3)

        # flute — enters in attention, leaves after trace
        if si == 1:
            tracks[2].note(E4, W*2, velocity=40)
            tracks[2].note(G4, W*2, velocity=38)
            tracks[2].note(C5, W*2, velocity=35)
            tracks[2].note(G4, W*2, velocity=32)
        elif si == 2:
            tracks[2].note(C5, W*2, velocity=42)
            tracks[2].note(G4, W*3, velocity=38)
            tracks[2].note(E4, W*3, velocity=34)
        elif si == 3:
            tracks[2].note(E4, W*4, velocity=28)
            tracks[2].note(C4, W*4, velocity=18)
        else:
            tracks[2].rest(W*8)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-best-life.mid")
    mc.compose(fn, tracks, tempo=72)

if __name__ == "__main__":
    best_life()
