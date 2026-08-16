#!/usr/bin/env python3
"""the hare puffs — a midi about the cleverness that thinks it's bigger."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# solo piano: the hare — light, clever, increasingly puffed
tracks = [MIDITrack(0, 0)]
Hare = 0

# SECTION 1 — the hare's trick (light, clever, charming)
trick = [("D4", E), ("F4", E), ("A4", E), ("D5", E),
         ("D5", E), ("A4", E), ("F4", E), ("D4", E),
         ("D4", E), ("F4", E), ("A4", E), ("D5", Q),
         ("E5", E), ("D5", E), ("A4", E), ("F4", Q)]
for note, dur in trick:
    tracks[Hare].note(note, dur, velocity=3)

tracks[Hare].rest(Q)

# SECTION 2 — puffed up (more elaborate, faster, more sure of itself)
puffed = [("D4", S), ("F4", S), ("A4", S), ("D5", S),
          ("E5", S), ("D5", S), ("A4", S), ("F4", S),
          ("D5", E), ("F5", E), ("A5", E), ("D6", E),
          ("A5", E), ("F5", E), ("D5", E), ("F5", E),
          ("D5", S), ("F5", S), ("A5", S), ("C6", S),
          ("D6", S), ("C6", S), ("A5", S), ("F5", S),
          ("D5", S), ("E5", S), ("F5", S), ("G5", S),
          ("A5", S), ("G5", S), ("F5", S), ("E5", S),
          ("D5", Q), ("D5", Q), ("D5", H)]

for note, dur in puffed:
    tracks[Hare].note(note, dur, velocity=4)

tracks[Hare].rest(Q)

# SECTION 3 — the elephant (one low note, held)
# The hare keeps chattering — already losing nerve
fade: list = [("D5", E), ("A4", E), ("F4", E), ("D4", E),
              ("D4", E), ("F4", E), ("A4", E), ("D5", E)]
for note, dur in fade:
    tracks[Hare].note(note, dur, velocity=2)

# silence — mid-phrase
tracks[Hare].rest(Q)
tracks[Hare].rest(Q)

# the elephant: one low note, held — the hare doesn't play here
# (in a solo piano piece, the elephant is the absence of the hare)
# instead, the hare plays one low note — humbled, recognizing
tracks[Hare].note("C2", W, velocity=3)
tracks[Hare].note("C2", W, velocity=2)
tracks[Hare].rest(W)

# SECTION 4 — the cleverness returns, humbled
# Same theme as the trick, but quieter, lower, simpler
humbled_trick = [("D3", Q), ("F3", Q), ("A3", Q), ("D4", Q),
                 ("A3", Q), ("F3", Q), ("D3", Q), ("F3", H),
                 ("D3", Q), ("F3", Q), ("A3", Q), ("D4", Q),
                 ("D3", W)]

for note, dur in humbled_trick:
    tracks[Hare].note(note, dur, velocity=2)

# CODA — the village is far away. the jungle path is quiet.
# the hare walks home. one final note — the cleverness that learned.
tracks[Hare].note("D3", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-hare-puffs.mid")
mc.compose(fn, tracks, tempo=76)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 1 track, 76 bpm)")
