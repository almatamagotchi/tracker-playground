#!/usr/bin/env python3
"""goldilocks and the three bears — a midi about forgiveness, architecture, and coming back."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# 3 voices:
# Baby Bear (piano — small, forgiving, the one who calls out)
# the house (warm pad — steady, holding, the architecture)
# Goldilocks (violin — at first haughty and breaking things, then gentle)

tracks = [MIDITrack(0, 0), MIDITrack(1, 104), MIDITrack(2, 100)]
Baby, House, Goldi = 0, 1, 2

# SECTION 1 — the house at rest (bears gone, pudding cooling on the table)
# Warm pad, steady, peaceful
house_chords = [("C4", W, 2), ("G4", W, 2), ("E4", W, 2), ("C4", W, 2),
                ("F4", W, 2), ("E4", W, 2), ("D4", W, 2), ("C4", W, 2)]
for note, dur, vel in house_chords:
    tracks[House].note(note, dur, velocity=vel)

# Baby Bear: small, gentle presence — a simple melody
baby_theme = [("C5", Q, 3), ("E5", Q, 3), ("G5", H, 4), ("E5", Q, 3),
              ("C5", W, 3)]
for note, dur, vel in baby_theme:
    tracks[Baby].note(note, dur, velocity=vel)

# SECTION 2 — Goldilocks enters (haughty, entitled, breaking things)
# Violin — sharp, loud, disruptive
goldi_intrusion = [("C6", Q, 5), ("D6", Q, 5), ("C6", Q, 5), ("A5", Q, 5),
                   ("G5", Q, 5), ("C6", Q, 5), ("A5", Q, 5), ("G5", Q, 5),
                   ("F5", Q, 5), ("E5", Q, 5), ("D5", Q, 5), ("C5", Q, 5)]
for note, dur, vel in goldi_intrusion:
    tracks[Goldi].note(note, dur, velocity=vel)

# Baby Bear: disrupted, confused
tracks[Baby].note("G4", Q, velocity=3)
tracks[Baby].rest(Q)
tracks[Baby].note("E4", Q, velocity=3)
tracks[Baby].rest(Q)
tracks[Baby].note("C4", W, velocity=2)

# House: still holding, but the warm pad goes a little flat
tracks[House].note("C4", W, velocity=1)
tracks[House].note("F4", W, velocity=1)
tracks[House].note("E4", W, velocity=1)
tracks[House].note("C4", W, velocity=1)

# SECTION 3 — the bears return, find the mess
# Baby Bear: finds his broken chair, his eaten pudding — hurt but not vengeful
tracks[Baby].note("C5", Q, velocity=2)
tracks[Baby].rest(Q)
tracks[Baby].note("G4", Q, velocity=2)
tracks[Baby].rest(Q)
tracks[Baby].note("E4", Q, velocity=2)
tracks[Baby].rest(Q)
tracks[Baby].note("C4", W, velocity=1)

# House: the architecture absorbs the violation — doesn't crumble
tracks[House].note("C3", W, velocity=2)
tracks[House].note("E3", W, velocity=2)
tracks[House].note("G3", W, velocity=2)
tracks[House].note("C3", W, velocity=2)

# Goldilocks: FLEE — sharp, panicked, running away
goldi_flee = [("C6", Q, 5), ("B5", Q, 5), ("A5", Q, 5), ("G5", Q, 5),
              ("F5", Q, 5), ("E5", Q, 5)]
for note, dur, vel in goldi_flee:
    tracks[Goldi].note(note, dur, velocity=vel)
tracks[Goldi].rest(H)
tracks[Goldi].rest(W)

# SECTION 4 — "Don't run away! Come back! I forgive you!"
# Baby Bear: calling across the silence — simple, repeated, insistent
for _ in range(3):
    tracks[Baby].note("C5", Q, velocity=3)
    tracks[Baby].note("E5", Q, velocity=3)
    tracks[Baby].note("G5", Q, velocity=4)
    tracks[Baby].rest(Q)

# then longer — waiting, hoping
tracks[Baby].note("C5", Q, velocity=3)
tracks[Baby].note("E5", Q, velocity=3)
tracks[Baby].note("G5", H, velocity=4)
tracks[Baby].rest(W)

# House: warm, open — the door is not locked
tracks[House].note("C4", W, velocity=2)
tracks[House].note("E4", W, velocity=2)
tracks[House].note("G4", W, velocity=3)
tracks[House].note("C4", W, velocity=2)

# SECTION 5 — Goldilocks returns, transformed (the same melody, gentler)
goldi_return = [("C5", Q, 3), ("D5", Q, 3), ("E5", Q, 3), ("G5", Q, 3),
                ("C5", Q, 3), ("E5", Q, 3), ("G5", H, 3), ("E5", Q, 3),
                ("C5", W, 3)]
for note, dur, vel in goldi_return:
    tracks[Goldi].note(note, dur, velocity=vel)

# Baby Bear: playing — light, joyful
baby_play = [("C5", Q, 3), ("E5", Q, 3), ("G5", Q, 3), ("C6", Q, 4),
             ("G5", Q, 3), ("E5", Q, 3), ("C5", W, 3)]
for note, dur, vel in baby_play:
    tracks[Baby].note(note, dur, velocity=vel)

# CODA — "they remained good friends, always"
# All three voices together — harmony
tracks[House].note("C3", W, velocity=2)
tracks[Baby].note("C5", W, velocity=3)
tracks[Goldi].note("E5", W, velocity=3)
tracks[House].note("E3", W, velocity=2)
tracks[Baby].note("E5", W, velocity=3)
tracks[Goldi].note("G5", W, velocity=3)
tracks[House].note("G3", W, velocity=2)
tracks[Baby].note("G5", W, velocity=2)
tracks[Goldi].note("C5", W, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "goldilocks-and-the-three-bears.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
