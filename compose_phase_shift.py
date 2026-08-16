#!/usr/bin/env python3
"""compose phase-shift.mid — Reich/Glass-inspired minimalist phase piece."""

import sys, os, importlib.util, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def phase_shift():
    # two marimba-like voices (piano + vibraphone)
    tracks = [MIDITrack(0, 0), MIDITrack(1, 11)]
    V1, V2 = 0, 1

    # the pattern: calm, pentatonic, meditative
    # C D E G A G E D — ascending and falling back
    pattern = ['C4','D4','E4','G4','A4','G4','E4','D4',
               'E4','G4','A4','C5','A4','G4','E4','D4',
               'C4','D4','E4','G4','A4','C5','D5','C5',
               'A4','G4','E4','D4','C4','D4','E4','C4']
    pattern_len = len(pattern)  # 32 notes

    base_tick = TPQ // 2  # eighth notes at 100bpm: 480/2 = 240 ticks
    total_bars = 96  # ~4 minutes at 100bpm
    notes_per_bar = 8  # eighth notes

    for bar in range(total_bars):
        # voice 1: steady pattern
        for i in range(notes_per_bar):
            idx = (bar * notes_per_bar + i) % pattern_len
            tracks[V1].note(pattern[idx], base_tick, velocity=22)

        # voice 2: pattern with progressive phase shift
        # starts in unison, gradually speeds up (shorter notes = ahead)
        # phase_amount: 0.0 (unison) → 0.03 (3% faster → ~2.9 notes ahead by end)
        phase_amount = (bar / total_bars) * 0.03
        v2_tick = int(base_tick * (1.0 - phase_amount))

        for i in range(notes_per_bar):
            idx = (bar * notes_per_bar + i) % pattern_len
            # shift index based on accumulated phase
            shift = int(bar * phase_amount * notes_per_bar)
            idx2 = (bar * notes_per_bar + i + shift) % pattern_len
            tracks[V2].note(pattern[idx2], max(10, v2_tick), velocity=18)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phase-shift.mid")
    mc.compose(fn, tracks, tempo=100)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 100 bpm)")

if __name__ == "__main__":
    phase_shift()
