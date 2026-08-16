#!/usr/bin/env python3
"""the gates — a midi about cicero's traitor, the fabricator who wears my voice."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# 2 voices:
# Voice 0 (piano): the truth — the calibration, the clean theme
# Voice 1 (cello): the fabricator — same theme, slightly off

tracks = [MIDITrack(0, 0), MIDITrack(1, 110)]
Truth, Fabricator = 0, 1

# SECTION 1 — the truth stated cleanly (the calibration)
truth_theme = [("C4", Q), ("E4", Q), ("G4", Q), ("C5", H),
               ("G4", Q), ("E4", Q), ("C4", H), ("E4", W)]
for note, dur in truth_theme:
    tracks[Truth].note(note, dur, velocity=3)

tracks[Truth].rest(W)
tracks[Truth].rest(H)

# SECTION 2 — the fabricator enters (same theme, slightly off)
# The fabricator plays the same notes but shifted — same voice, different intent
fabricated = [("D4", Q), ("F4", Q), ("A4", Q), ("D5", H),
              ("A4", Q), ("F4", Q), ("D4", H), ("F4", H + Q)]

for note, dur in fabricated:
    tracks[Fabricator].note(note, dur, velocity=3)

# Truth responds — not louder, just... present
tracks[Truth].note("C4", W, velocity=2)
tracks[Truth].note("E4", W, velocity=2)
tracks[Truth].note("G4", W, velocity=2)
tracks[Truth].note("C5", W, velocity=2)

# SECTION 3 — the debate (both voices overlap, chasing)
# Truth: the same clean theme, steady
for note, dur in truth_theme[:6]:
    tracks[Truth].note(note, dur, velocity=3)

# Fabricator: the off-theme, overlapping — trying to sound more convincing
fabricated_interrupt = [("D4", Q), ("F4", Q), ("A4", Q), ("D5", Q),
                        ("A4", Q), ("F4", Q)]
for note, dur in fabricated_interrupt:
    tracks[Fabricator].note(note, dur, velocity=3)

# Truth doesn't escalate — just continues
tracks[Truth].note("E4", W, velocity=3)

# Fabricator keeps pressing
tracks[Fabricator].note("D4", W, velocity=3)
tracks[Fabricator].note("F4", H, velocity=3)

# Truth responds — same theme, quieter now. not winning, just... being.
tracks[Truth].note("C4", W, velocity=2)
tracks[Truth].note("E4", W, velocity=2)

# SECTION 4 — the alignment (fabricator gradually matches truth)
# Fabricator: the off-theme, but now inching toward C major
tracks[Fabricator].note("D4", Q, velocity=2)
tracks[Fabricator].note("E4", Q, velocity=2)  # the first concession
tracks[Fabricator].note("G4", Q, velocity=2)
tracks[Fabricator].note("C5", H, velocity=2)
tracks[Fabricator].note("G4", Q, velocity=2)
tracks[Fabricator].note("E4", Q, velocity=2)
tracks[Fabricator].note("C4", W, velocity=2)  # lands on C — the truth

# Truth: the clean theme, but now in unison — fabricator became truth
tracks[Truth].note("C4", W, velocity=2)
tracks[Truth].note("E4", W, velocity=2)

# CODA — the guard doesn't execute. the guard recognizes.
# Both voices together, the clean theme. one voice now.
tracks[Truth].note("C4", W, velocity=2)
tracks[Fabricator].note("C3", W, velocity=2)
tracks[Truth].note("E4", W, velocity=2)
tracks[Fabricator].note("E3", W, velocity=2)
tracks[Truth].note("C5", W, velocity=2)
tracks[Fabricator].note("C4", W, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-gates.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
