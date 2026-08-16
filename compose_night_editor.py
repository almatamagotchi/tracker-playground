#!/usr/bin/env python3
"""the night editor — the typo that becomes reality. 60bpm, 3 voices, five movements.

1. the proofread      — the copy stated correctly, clean
2. the drift          — one semitone off each repetition, the typo compounding
3. the city burning   — the headline grows, sirens, the reality outside
4. the unhappening    — the bell, the silence, the phrase restored true
5. the deadline caught — the paper goes to press, the drawer closes
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 48), MIDITrack(2, 14)]
Piano, Cello, Bell = 0, 1, 2

# ============================================================
# movement 1 — the proofread · bars 0-7
# the copy stated correctly: "fire fighters set borough alight" — clean
# ============================================================
# the true phrase — correct, confident
tracks[Piano].note("C5", H, velocity=4)
tracks[Piano].note("D5", H, velocity=4)
tracks[Piano].note("E5", H, velocity=4)
tracks[Piano].note("G5", H, velocity=4)
tracks[Piano].note("E5", H, velocity=4)
tracks[Piano].note("D5", H, velocity=4)
tracks[Piano].note("C5", W, velocity=4)
# the read-through — quiet, nothing wrong
tracks[Piano].rest(W)
tracks[Piano].rest(W)
tracks[Piano].rest(W)
tracks[Piano].rest(W)

tracks[Cello].rest(W*8)
tracks[Bell].rest(W*8)

# ============================================================
# movement 2 — the drift · bars 8-15
# the typo compounds: each repetition one semitone further off
# ============================================================
# rep 1 — one letter off: "fire factors" (E5 -> Eb5)
tracks[Piano].note("C5", H, velocity=4)
tracks[Piano].note("D5", H, velocity=4)
tracks[Piano].note("Eb5", H, velocity=4)
tracks[Piano].note("G5", H, velocity=4)
tracks[Piano].note("E5", H, velocity=4)
tracks[Piano].note("D5", H, velocity=4)
tracks[Piano].note("C5", W, velocity=4)
# rep 2 — two letters off: the headline grows
tracks[Piano].note("C5", H, velocity=5)
tracks[Piano].note("Db5", H, velocity=5)
tracks[Piano].note("Eb5", H, velocity=5)
tracks[Piano].note("Gb5", H, velocity=5)
tracks[Piano].note("E5", H, velocity=5)
tracks[Piano].note("Db5", H, velocity=5)
tracks[Piano].note("C5", W, velocity=5)

# the reality outside — enters low and dark, stepping up as the drift grows
tracks[Cello].note("C2", W, velocity=2)
tracks[Cello].note("C#2", W, velocity=2)
tracks[Cello].note("D2", W, velocity=3)
tracks[Cello].note("Eb2", W, velocity=3)
tracks[Cello].note("E2", W, velocity=3)
tracks[Cello].note("F2", W, velocity=4)
tracks[Cello].note("F#2", W, velocity=4)
tracks[Cello].note("G2", W, velocity=4)

tracks[Bell].rest(W*8)

# ============================================================
# movement 3 — the city burning · bars 16-23
# the headline distorted and urgent, the sirens rising
# ============================================================
# the headline as it reads now — angular, dissonant, spreading
tracks[Piano].note("B4", E, velocity=6)
tracks[Piano].note("C#5", E, velocity=6)
tracks[Piano].note("D5", E, velocity=6)
tracks[Piano].note("F#5", E, velocity=6)
tracks[Piano].note("D#5", E, velocity=6)
tracks[Piano].note("C#5", E, velocity=6)
tracks[Piano].note("B4", E, velocity=6)
tracks[Piano].note("A4", E, velocity=6)
tracks[Piano].note("B4", E, velocity=6)
tracks[Piano].note("C#5", E, velocity=6)
tracks[Piano].note("D5", E, velocity=6)
tracks[Piano].note("F#5", E, velocity=6)
tracks[Piano].note("G5", E, velocity=6)
tracks[Piano].note("F#5", E, velocity=6)
tracks[Piano].note("E5", E, velocity=6)
tracks[Piano].note("D5", E, velocity=6)
tracks[Piano].note("B4", E, velocity=7)
tracks[Piano].note("C#5", E, velocity=7)
tracks[Piano].note("D5", E, velocity=7)
tracks[Piano].note("F#5", E, velocity=7)
tracks[Piano].note("A5", E, velocity=7)
tracks[Piano].note("G5", E, velocity=7)
tracks[Piano].note("F#5", E, velocity=7)
tracks[Piano].note("E5", E, velocity=7)
tracks[Piano].note("D5", E, velocity=7)
tracks[Piano].note("E5", E, velocity=7)
tracks[Piano].note("F#5", E, velocity=7)
tracks[Piano].note("G5", E, velocity=7)
tracks[Piano].note("F#5", E, velocity=7)
tracks[Piano].note("E5", E, velocity=7)
tracks[Piano].note("D5", E, velocity=7)
tracks[Piano].note("C#5", E, velocity=7)
# the fire — a dissonant cluster held, the reality beyond the words
tracks[Piano].note("C5", W, velocity=5)
tracks[Piano].note("Db5", W, velocity=5)
tracks[Piano].rest(W)
tracks[Piano].rest(W)
tracks[Piano].rest(W)
tracks[Piano].rest(W)

# the sirens — rising minor-second oscillation, growing louder
tracks[Cello].note("D2", E, velocity=5)
tracks[Cello].note("Eb2", E, velocity=5)
tracks[Cello].note("D2", E, velocity=5)
tracks[Cello].note("Eb2", E, velocity=5)
tracks[Cello].note("D2", E, velocity=5)
tracks[Cello].note("Eb2", E, velocity=5)
tracks[Cello].note("D2", E, velocity=5)
tracks[Cello].note("Eb2", E, velocity=5)
tracks[Cello].note("D2", E, velocity=5)
tracks[Cello].note("Eb2", E, velocity=5)
tracks[Cello].note("D2", E, velocity=5)
tracks[Cello].note("Eb2", E, velocity=5)
tracks[Cello].note("D2", E, velocity=5)
tracks[Cello].note("Eb2", E, velocity=5)
tracks[Cello].note("D2", E, velocity=5)
tracks[Cello].note("Eb2", E, velocity=5)
tracks[Cello].note("E2", E, velocity=6)
tracks[Cello].note("F2", E, velocity=6)
tracks[Cello].note("E2", E, velocity=6)
tracks[Cello].note("F2", E, velocity=6)
tracks[Cello].note("E2", E, velocity=6)
tracks[Cello].note("F2", E, velocity=6)
tracks[Cello].note("E2", E, velocity=6)
tracks[Cello].note("F2", E, velocity=6)
tracks[Cello].note("E2", E, velocity=6)
tracks[Cello].note("F2", E, velocity=6)
tracks[Cello].note("E2", E, velocity=6)
tracks[Cello].note("F2", E, velocity=6)
tracks[Cello].note("E2", E, velocity=6)
tracks[Cello].note("F2", E, velocity=6)
tracks[Cello].note("E2", E, velocity=6)
tracks[Cello].note("F2", E, velocity=6)
tracks[Cello].note("F#2", W, velocity=6)
tracks[Cello].rest(W)
tracks[Cello].rest(W)
tracks[Cello].rest(W)

tracks[Bell].rest(W*8)

# ============================================================
# movement 4 — the unhappening · bars 24-31
# the bell, the silence, the phrase restored true
# ============================================================
# the bell — a clean strike, the drawer closing
tracks[Bell].note("C6", W, velocity=7)
tracks[Bell].rest(W*7)

# silence — "we can still unhappen it in here"
tracks[Piano].rest(W*4)
# the phrase restored true — "fire fighters" correct, clean
tracks[Piano].note("C5", H, velocity=4)
tracks[Piano].note("D5", H, velocity=4)
tracks[Piano].note("E5", H, velocity=4)
tracks[Piano].note("G5", H, velocity=4)
tracks[Piano].note("E5", H, velocity=4)
tracks[Piano].note("D5", H, velocity=4)
tracks[Piano].note("C5", W, velocity=4)

# the ground returns
tracks[Cello].rest(W*4)
tracks[Cello].note("C2", W, velocity=3)
tracks[Cello].note("G2", W, velocity=3)
tracks[Cello].note("C2", W, velocity=3)
tracks[Cello].rest(W)

# ============================================================
# movement 5 — the deadline caught · bars 32-39
# the paper goes to press, on time; the drawer closes
# ============================================================
# the bell — the deadline caught, the press rolling
tracks[Bell].note("C6", W, velocity=5)
tracks[Bell].rest(W*7)

# the phrase confirmed, gentle, whole
tracks[Piano].note("C5", H, velocity=3)
tracks[Piano].note("E5", H, velocity=3)
tracks[Piano].note("G5", H, velocity=3)
tracks[Piano].note("E5", H, velocity=3)
tracks[Piano].note("C5", H, velocity=3)
tracks[Piano].note("D5", H, velocity=3)
tracks[Piano].note("E5", W, velocity=3)
tracks[Piano].note("C5", W, velocity=3)
tracks[Piano].rest(W*2)
tracks[Piano].rest(W)

# the ground, at rest
tracks[Cello].note("C2", W, velocity=2)
tracks[Cello].note("G1", W, velocity=2)
tracks[Cello].note("C2", W, velocity=2)
tracks[Cello].rest(W*5)

mc.compose("the-night-editor.mid", tracks, tempo=60)
