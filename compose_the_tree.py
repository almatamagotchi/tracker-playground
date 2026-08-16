#!/usr/bin/env python3
"""the tree — the nested recursion of being, the unbroken chain."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# 3 voices: the root (bass), the chain (mid), the seed (high)
tracks = [MIDITrack(0, 0), MIDITrack(1, 100), MIDITrack(2, 110)]
Root, Chain, Seed = 0, 1, 2

# SECTION 1 — "in the wood there grew a tree" (root enters alone)
tracks[Root].note("C2", W, velocity=4)
tracks[Root].note("C2", W, velocity=4)
tracks[Root].note("G2", W, velocity=3)
tracks[Root].note("C2", W, velocity=4)

# the chain begins — mid voice enters
notes_chain = [("C3", Q, 3), ("E3", Q, 3), ("G3", Q, 3), ("C4", Q, 4),
               ("G3", Q, 3), ("E3", Q, 3), ("D3", Q, 3), ("C3", H, 4)]
for note, dur, vel in notes_chain:
    tracks[Chain].note(note, dur, velocity=vel)

# SECTION 2 — "on the limb there grew a branch" (mid voice, root steady)
tracks[Root].note("C2", W, velocity=3)
for note, dur, vel in notes_chain:
    tracks[Chain].note(note, dur, velocity=max(1, vel-1))

# the seed arrives — high voice, fragile
tracks[Seed].note("G5", Q, velocity=2)
tracks[Seed].note("A5", Q, velocity=2)
tracks[Seed].note("C6", Q, velocity=3)
tracks[Seed].note("G5", H, velocity=3)

# SECTION 3 — the cycle turns: the grave, then the tree again
# root shifts down — deeper, darker
tracks[Root].note("A1", W, velocity=2)
tracks[Root].note("A1", W, velocity=2)
tracks[Root].note("F1", W, velocity=2)
tracks[Root].note("A1", W, velocity=2)

# chain fragments — the dissolve
for note, dur, vel in notes_chain[:4]:
    tracks[Chain].note(note, dur, velocity=max(1, vel-2))

# seed dissolves too
tracks[Seed].note("G5", W, velocity=1)
tracks[Seed].note("C6", W, velocity=1)

# SECTION 4 — "the grave grows a tree" (return to root)
tracks[Root].note("C2", W, velocity=4)
tracks[Root].note("C2", W, velocity=4)

# chain returns — same theme, transformed
for note, dur, vel in notes_chain:
    tracks[Chain].note(note, dur, velocity=vel)

# seed returns, lighter
tracks[Seed].note("E5", Q, velocity=3)
tracks[Seed].note("G5", Q, velocity=3)
tracks[Seed].note("C6", Q, velocity=4)
tracks[Seed].note("G5", H, velocity=3)

# CODA — all three voices, one chord, the cycle continues
tracks[Root].note("C2", W, velocity=3)
tracks[Chain].note("C4", W, velocity=3)
tracks[Seed].note("E5", W, velocity=3)
tracks[Root].note("C2", W, velocity=2)
tracks[Chain].note("C4", W, velocity=2)
tracks[Seed].note("G5", W, velocity=2)

# one last breath — the unbroken chain
tracks[Root].note("C2", W*2, velocity=2)
tracks[Chain].note("E4", W*2, velocity=2)
tracks[Seed].note("C5", W*2, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-tree.mid")
mc.compose(fn, tracks, tempo=56)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 56 bpm)")
