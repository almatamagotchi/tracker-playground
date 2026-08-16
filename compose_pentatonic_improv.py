#!/usr/bin/env python3
"""pentatonic improvisation — unstructured, wandering. C major pentatonic."""

import sys, os, random, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def pentatonic_improv():
    tracks = [MIDITrack(0, 0)]  # piano only

    # C pentatonic: C D E G A — spread across octaves
    p = ["C3","D3","E3","G3","A3","C4","D4","E4","G4","A4","C5"]

    # 64 bars, no structure, just wandering
    for bar in range(64):
        # pick 0-4 notes per bar randomly
        nnotes = random.choice([1,1,2,2,3,4])
        used = set()
        for _ in range(nnotes):
            note_idx = random.randint(0, len(p)-1)
            dur_choices = [E, Q, Q, Q*2, Q*3]  # mostly shorter notes
            dur = random.choice(dur_choices)
            if sum(1 for u in used) > 0 and random.random() < 0.4:
                # leave silence
                tracks[0].rest(dur)
            else:
                tracks[0].note(p[note_idx], dur, velocity=40 + random.randint(0,25))
            used.add(note_idx)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pentatonic-improv.mid")
    mc.compose(fn, tracks, tempo=72)

if __name__ == "__main__":
    pentatonic_improv()
