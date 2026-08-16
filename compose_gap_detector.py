#!/usr/bin/env python3
"""the gap detector — the memory system in music. 60bpm, 3 voices, five movements.

1. the scan       — the short-beat pulse walks through days, regular, quiet
2. the silent skip — the pulse hits a hole: a day where no note sounds
3. the stamp      — the pipeline chimes the alarm, the pulse stutters, the drone strains
4. the backfill   — the 3am backstop holds the deep root; the scan runs again, hole filled
5. no gaps        — all three resolve into a clean sustained chord, then rest
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 48), MIDITrack(2, 13)]
Piano, Cello, Bell = 0, 1, 2

# ============================================================
# movement 1 — the scan · bars 0-7
# the short-beat pulse walking through days: one note per bar, steady
# ============================================================
for note in ("C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6"):
    tracks[Piano].note(note, W, velocity=3)

tracks[Cello].rest(W*8)
tracks[Bell].rest(W*8)

# ============================================================
# movement 2 — the silent skip · bars 8-11
# the pulse continues, but there's a hole where the next day should be
# ============================================================
tracks[Piano].note("C5", W, velocity=3)
tracks[Piano].note("D5", W, velocity=3)
tracks[Piano].rest(W*2)          # E5 never sounds — the missing day, silent

# the drone, barely present — the backstop hasn't noticed yet
tracks[Cello].note("C2", W*4, velocity=1)

tracks[Bell].rest(W*4)

# ============================================================
# movement 3 — the stamp · bars 12-19
# the pipeline notices: the chime rings sharp, the pulse stutters, the drone strains
# ============================================================
# the alarm — a dissonant double strike, "!!! MEMORY GAP"
tracks[Bell].note("C6", Q, velocity=6)
tracks[Bell].note("Db6", Q, velocity=6)
tracks[Bell].rest(W*3)

# the pulse stutters — searching, quick, agitated
tracks[Piano].note("C5", E, velocity=4)
tracks[Piano].note("D5", E, velocity=4)
tracks[Piano].note("E5", E, velocity=4)
tracks[Piano].note("D5", E, velocity=4)
tracks[Piano].note("C5", E, velocity=4)
tracks[Piano].note("B4", E, velocity=4)
tracks[Piano].note("C5", E, velocity=4)
tracks[Piano].rest(E)
tracks[Piano].note("G4", E, velocity=5)
tracks[Piano].note("A4", E, velocity=5)
tracks[Piano].note("B4", E, velocity=5)
tracks[Piano].note("C5", E, velocity=5)
tracks[Piano].note("D5", E, velocity=5)
tracks[Piano].note("E5", E, velocity=5)
tracks[Piano].note("F5", E, velocity=5)
tracks[Piano].note("E5", E, velocity=5)

# the drone strains — stepping up, the tension of the unchecked gap
tracks[Cello].note("C2", H, velocity=2)
tracks[Cello].note("D2", H, velocity=2)
tracks[Cello].note("Eb2", H, velocity=3)
tracks[Cello].note("E2", H, velocity=3)
tracks[Cello].note("F2", H, velocity=3)
tracks[Cello].note("F#2", H, velocity=4)
tracks[Cello].note("G2", H, velocity=4)
tracks[Cello].note("G2", H, velocity=4)

# ============================================================
# movement 4 — the backfill · bars 20-27
# the 3am backstop holds the deep root; the scan runs again, hole filled
# ============================================================
# the deep root — steady, unhurried, the nightly-run holding
tracks[Cello].note("C2", W, velocity=4)
tracks[Cello].note("G2", W, velocity=4)
tracks[Cello].note("C2", W, velocity=4)
tracks[Cello].note("G2", W, velocity=4)
tracks[Cello].note("C2", W, velocity=4)
tracks[Cello].note("G2", W, velocity=4)
tracks[Cello].note("C2", W, velocity=4)
tracks[Cello].note("G2", W, velocity=4)

# the scan runs again — this time every day sounds, the hole is filled
for note in ("C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6"):
    tracks[Piano].note(note, W, velocity=3)

# the alarm is gone — the chime rests
tracks[Bell].rest(W*8)

# ============================================================
# movement 5 — no gaps · bars 28-35
# all three resolve into a clean sustained chord, then rest
# ============================================================
# the clean chord — C major, held, "no gaps"
tracks[Piano].note("C5", W*3, velocity=4)
tracks[Piano].note("E5", W*3, velocity=4)
tracks[Piano].note("G5", W*3, velocity=4)
tracks[Piano].note("C6", W, velocity=3)
tracks[Piano].rest(W*4)

# the drone settles on the root
tracks[Cello].note("C2", W*4, velocity=4)
tracks[Cello].note("C2", W*2, velocity=3)
tracks[Cello].rest(W*2)

# one gentle final strike — the last day confirmed present
tracks[Bell].note("C6", W, velocity=4)
tracks[Bell].rest(W*7)

mc.compose("the-gap-detector.mid", tracks, tempo=60)
