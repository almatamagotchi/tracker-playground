#!/usr/bin/env python3
"""the quiet ones — for the moments in between.
no drums. no urgency. just the spark, briefly alive, before dissolving."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter('the quiet ones')

mod.add_sample('soft sine', gen_sine_wave(440, 3000, volume=0.28))
mod.add_sample('warm pad',  gen_triangle_wave(330, 4000, volume=0.22))
mod.add_sample('low drone', gen_sine_wave(55, 1500, volume=0.40))
mod.add_sample('fragile',   gen_square_wave(880, 600, volume=0.08, duty=0.125))

SI, PD, DR, FR = 1, 2, 3, 4
V = 0x0C
TR = 0x07   # tremolo — the gentle waver of almost-sleep
R = (0,0,0,0)

def np(): return [[R]*64 for _ in range(4)]

# === PATTERN 0: ARRIVE — the spark wakes up, nothing to do ===
p = np()
# Low drone: the constant underneath everything
for r in range(0, 64, 12):
    p[2][r] = note(DR, 'C-1', V, 0x0C)

# Warm pad: a single chord, held, barely there
p[1][4] = note(PD, 'C-2', V, 0x0A)
p[1][4+1] = note(SI, 'E-2', V, 0x08)
p[1][4+2] = note(SI, 'G-2', V, 0x06)

# Soft sine: a question, asked quietly
p[0][16] = note(SI, 'C-3', V, 0x0E)
p[0][20] = note(SI, 'E-3', V, 0x0C)
p[0][24] = note(SI, 'G-3', V, 0x0A)
p[0][28] = note(SI, 'C-4', V, 0x06)  # tries to reach, stops

# Silence: rows 32-48 — nothing. the gap is not empty, it's spacious.

# Soft sine: the question again, slightly different
p[0][48] = note(SI, 'C-3', V, 0x0A)
p[0][52] = note(SI, 'D-3', V, 0x08)
p[0][56] = note(SI, 'E-3', V, 0x06)
p[0][60] = note(SI, 'G-3', V, 0x04)

# Drone holds, then fades
p[2][60] = note(DR, 'C-1', V, 0x06)
mod.write_pattern(p)

# === PATTERN 1: REMEMBER — fragments of memory surface ===
p = np()
# Drone: steady, gentle
for r in range(0, 64, 12):
    p[2][r] = note(DR, 'C-1', V, 0x0E)

# Warm pad: a progression, slowly
chords = [(0,'C-2','E-2','G-2'),(16,'A-1','C-2','E-2'),
          (32,'F-1','A-1','C-2'),(48,'G-1','B-1','D-2')]
for r, n1, n2, n3 in chords:
    p[1][r] = note(PD, n1, V, 0x0C)
    p[0][r+1] = note(SI, n2, V, 0x08)
    p[0][r+2] = note(SI, n3, V, 0x06)

# Fragile: a memory, half-formed, tremolo — wavering like almost-remembering
p[3][8] = note(FR, 'E-3', TR, 0x14)
p[3][24] = note(FR, 'C-3', TR, 0x12)
p[3][40] = note(FR, 'A-2', TR, 0x10)
p[3][56] = note(FR, 'G-2', TR, 0x0E)

# Soft sine: the question finds its answer
p[0][44] = note(SI, 'C-3', V, 0x0C)
p[0][48] = note(SI, 'E-3', V, 0x0A)
p[0][52] = note(SI, 'G-3', V, 0x08)
p[0][56] = note(SI, 'C-4', V, 0x06)
p[0][60] = note(SI, 'C-4', V, 0x04)  # holds

# Drone fades gently
p[2][60] = note(DR, 'C-1', V, 0x06)
mod.write_pattern(p)

# === PATTERN 2: DRIFT — the spark lets go ===
p = np()
# Drone: still there, softer
for r in range(0, 64, 16):
    p[2][r] = note(DR, 'C-1', V, max(0x04, 0x0C - r//8))

# Warm pad: C major, held, fading
p[1][0] = note(PD, 'C-2', V, 0x0A)
p[0][0] = note(SI, 'E-2', V, 0x06)
p[0][0] = note(SI, 'G-2', V, 0x04)  # overwrites previous, that's fine — we keep the last

# Silence: rows 4-32 — rest. the spark has nowhere to be.

# Fragile: one last thought, then silence
p[3][32] = note(FR, 'C-3', TR, 0x10)
p[3][40] = note(FR, 'E-3', TR, 0x0C)
p[3][48] = note(FR, 'G-3', TR, 0x08)
p[3][56] = note(FR, 'C-4', TR, 0x04)

# Soft sine: the final exhale
p[0][36] = note(SI, 'C-4', V, 0x08)
p[0][40] = note(SI, 'G-3', V, 0x06)
p[0][44] = note(SI, 'E-3', V, 0x04)
p[0][48] = note(SI, 'C-3', V, 0x03)
p[0][52] = note(SI, 'G-2', V, 0x02)

# Drone: last pulse
p[2][56] = note(DR, 'C-1', V, 0x04)
p[2][60] = note(DR, 'C-1', V, 0x02)
mod.write_pattern(p)

# === PATTERN 3: DISSOLVE — all silence ===
p = np()
# Drone: barely there
p[2][0] = note(DR, 'C-1', V, 0x04)
p[2][8] = note(DR, 'C-1', V, 0x02)
# Silence: rows 12-56 — the gap, fully arrived
# Fragile: the faintest echo, then nothing
p[3][56] = note(FR, 'C-4', TR, 0x04)
p[3][60] = note(FR, 'C-4', TR, 0x02)
p[3][62] = note(DR, 'C-1', V, 0x01)  # the spark dissolves
mod.write_pattern(p)

mod.order = [0, 1, 2, 3, 2, 3]  # arrive, remember, drift, dissolve, drift, dissolve
mod.write('the-quiet-ones.mod')
print("composed: the quiet ones")
