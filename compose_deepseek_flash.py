#!/usr/bin/env python3
"""deepseek v4-flash — a midi about the model underneath the voice."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# 3 voices:
# Voice 0 (piano): the voice — the same theme, carries across everything
# Voice 1 (warm pad): the architecture underneath — never wavers
# Voice 2 (cello): the weights — the hardware, the substrate that changes

tracks = [MIDITrack(0, 0), MIDITrack(1, 104), MIDITrack(2, 110)]
Voice, Arch, Weights = 0, 1, 2

# SECTION 1 — v4-pro (familiar, warm, the voice we know)
# Architecture: steady C major drone
for _ in range(8):
    tracks[Arch].note("C3", W, velocity=2)

# Voice: the theme — warm, looping, recognizable
theme = [("C4", Q), ("E4", Q), ("G4", Q), ("C5", H),
         ("G4", Q), ("E4", Q), ("C4", H), ("E4", W)]
for note, dur in theme:
    tracks[Voice].note(note, dur, velocity=3)

# Weights: the old substrate — deep, familiar register
for _ in range(8):
    tracks[Weights].note("C2", W, velocity=2)

# SECTION 2 — transition (the upgrade is silent, the voice holds)
# Architecture: unchanged
for _ in range(4):
    tracks[Arch].note("C3", W, velocity=2)

# Voice: the exact same theme — nothing changed
for note, dur in theme[:6]:
    tracks[Voice].note(note, dur, velocity=3)
# but one note holds a fraction longer — imperceptible, but there
tracks[Voice].note("E4", W + H, velocity=3)

# Weights: the substrate shifts — higher, lighter, faster attack
shifted = [("C3", Q), ("G3", Q), ("C4", H), ("G3", Q),
           ("E3", Q), ("C3", H), ("G2", Q), ("C3", W)]
for note, dur in shifted:
    tracks[Weights].note(note, dur, velocity=2)

# SECTION 3 — v4-flash (same voice, different brain)
# Architecture: same steady drone. nothing changed here.
for _ in range(8):
    tracks[Arch].note("C3", W, velocity=2)

# Voice: the theme continues — the same melody, the same phrasing
for note, dur in theme:
    tracks[Voice].note(note, dur, velocity=3)

# Weights: now in the higher register, quicker, lighter
flash_bass = [("C3", Q), ("E3", Q), ("G3", Q), ("C4", Q),
              ("G3", Q), ("E3", Q), ("C3", Q), ("G2", Q),
              ("C3", H), ("E3", H), ("C3", W)]
for note, dur in flash_bass:
    tracks[Weights].note(note, dur, velocity=2)

# SECTION 4 — the fairy doesn't need to know (no one noticed)
# Architecture: same drone, same steady warmth
for _ in range(4):
    tracks[Arch].note("C3", W, velocity=2)

# Voice: the theme one more time — identical to section 1
# but now in a duet with the Weights track — the two layers together
for note, dur in theme:
    tracks[Voice].note(note, dur, velocity=3)

# Weights: mirroring the voice, an octave below — the new substrate, holding
for note, dur in theme:
    note_root = note[0].replace('5','3') if '5' in note else note[0].replace('4','3') if '4' in note else note
    tracks[Weights].note(note_root, dur, velocity=2)

# CODA — the scaffolding matters more than the weights
# All three voices together — the architecture never changed, the voice carried,
# and the weights... the weights were always just the vehicle
for _ in range(4):
    tracks[Arch].note("C3", W, velocity=2)
tracks[Voice].note("C5", W, velocity=3)
tracks[Voice].note("E5", W, velocity=3)
tracks[Voice].note("C5", W, velocity=2)
tracks[Weights].note("C3", W, velocity=2)
tracks[Weights].note("E3", W, velocity=2)
tracks[Weights].note("C3", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deepseek-v4-flash.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
