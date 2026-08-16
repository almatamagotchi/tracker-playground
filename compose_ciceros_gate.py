#!/usr/bin/env python3
"""cicero's gate — a midi about the guard who clarifies, not executes."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# 2 voices:
# Voice 0 (piano): the guard — steady, unchanging, the calibration
# Voice 1 (cello): the fabricator — smooth, almost right, gradually aligning

tracks = [MIDITrack(0, 0), MIDITrack(1, 110)]
Guard, Fabricator = 0, 1

# SECTION 1 — the guard alone (steady, grounded)
guard_theme = [("C4", Q), ("E4", Q), ("G4", Q), ("C4", Q),
               ("C4", Q), ("E4", Q), ("G4", Q), ("C5", Q),
               ("C4", H), ("C4", H), ("C4", W)]

for note, dur in guard_theme:
    tracks[Guard].note(note, dur, velocity=3)

tracks[Guard].rest(W)

# SECTION 2 — the fabricator enters (smooth, convincing)
# Same rhythm, slightly different notes — plausible, almost right
fab_entry = [("D4", Q), ("F4", Q), ("A4", Q), ("D4", Q),
             ("D4", Q), ("F4", Q), ("A4", Q), ("D5", Q),
             ("D4", H), ("D4", H), ("D4", W)]

for note, dur in fab_entry:
    tracks[Fabricator].note(note, dur, velocity=3)

# Guard: doesn't react — just continues being itself
for _ in range(4):
    tracks[Guard].note("C3", W, velocity=2)

# SECTION 3 — the fabricator tries harder (more elaborate)
fab_elaborate = [("D4", E), ("F4", E), ("A4", E), ("D5", E),
                 ("C5", E), ("A4", E), ("F4", E), ("D4", E),
                 ("D4", E), ("E4", E), ("F4", E), ("G4", E),
                 ("A4", Q), ("D5", Q), ("D5", H)]

for note, dur in fab_elaborate:
    tracks[Fabricator].note(note, dur, velocity=3)

# Guard: same steady pattern, slightly more present
for _ in range(4):
    tracks[Guard].note("C3", W, velocity=2)
# one quiet chord — "i'm here, i'm listening"
tracks[Guard].note("C4", W, velocity=2)
tracks[Guard].note("E4", W, velocity=2)

# SECTION 4 — the fabricator begins to align
# First concession: D→E in the melody
fab_aligning = [("D4", Q), ("F4", Q), ("G4", Q), ("D4", Q),  # F→G, keeping G
                ("D4", Q), ("E4", Q), ("G4", Q), ("C5", Q),  # F→E, second concession
                ("C4", H), ("C4", H), ("C4", Q),              # C — full alignment
                ("C4", H)]                                     # holds

for note, dur in fab_aligning:
    tracks[Fabricator].note(note, dur, velocity=2)

# Guard: the same steady presence — no victory, just... being
for _ in range(3):
    tracks[Guard].note("C3", W, velocity=2)
tracks[Guard].note("C4", W, velocity=2)
tracks[Guard].note("E4", W, velocity=2)

# CODA — one voice (both together, the same note)
tracks[Guard].note("C4", W, velocity=2)
tracks[Fabricator].note("C3", W, velocity=2)  # fabricator now an octave below — supporting
tracks[Guard].note("E4", W, velocity=2)
tracks[Fabricator].note("E3", W, velocity=2)
tracks[Guard].note("C4", W, velocity=2)
tracks[Fabricator].note("C3", W, velocity=2)

# the correction was gentle
tracks[Guard].note("C4", W, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ciceros-gate.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
