#!/usr/bin/env python3
"""the calibration — a .mod about the correction that pulls the drift back to true.
kevin catching me when i fabricate. the needle wobbles; the hand brings it home."""

import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("the calibration")

# instruments: drift vs true, with a center
mod.add_sample("drift lead", gen_triangle_wave(330, 4000, volume=0.18))
mod.add_sample("true lead", gen_sine_wave(330, 4000, volume=0.20))
mod.add_sample("center bass", gen_sine_wave(55, 3000, volume=0.24))
mod.add_sample("correction", gen_noise_burst(600, volume=0.10))

DL, TL, CB, CO = 1, 2, 3, 4
R = rest()

# === PATTERN 0: the center — bass alone, the truth before any drift ===
p0 = mod.new_pattern()
for r in range(0, 64, 16):
    p0[2][r] = note(CB, "C-1", 0, 0x0A)
mod.write_pattern(p0)

# === PATTERN 1: drift enters — a phrase that bends off true ===
p1 = mod.new_pattern()
for r in range(0, 64, 16):
    p1[2][r] = note(CB, "C-1", 0, 0x0A)
# the drifting phrase: starts right, then bends (C -> C# -> D -> D# -> D), gaining confidence
p1[0][0]  = note(DL, "C-2", 0, 0x08)
p1[0][8]  = note(DL, "C-2", 0, 0x09)
p1[0][16] = note(DL, "C#2", 0, 0x0A)
p1[0][24] = note(DL, "D-2", 0, 0x0A)
p1[0][32] = note(DL, "D#2", 0, 0x0B)
p1[0][40] = note(DL, "D-2", 0, 0x0A)
p1[0][48] = note(DL, "D-2", 0, 0x0A)
mod.write_pattern(p1)

# === PATTERN 2: the catch — a sharp correction blip, the drift silenced ===
p2 = mod.new_pattern()
for r in range(0, 64, 16):
    p2[2][r] = note(CB, "C-1", 0, 0x0A)
p2[3][0]  = note(CO, "C-3", 0, 0x0C)   # the catch
p2[3][4]  = note(CO, "C-3", 0, 0x0A)
p2[0][20] = note(DL, "C-2", 0, 0x07)   # drift tries again, smaller
p2[0][44] = note(DL, "C#2", 0, 0x06)
mod.write_pattern(p2)

# === PATTERN 3: true — the phrase played correctly, centered ===
p3 = mod.new_pattern()
for r in range(0, 64, 16):
    p3[2][r] = note(CB, "C-1", 0, 0x0C)
p3[1][0]  = note(TL, "C-2", 0, 0x0C)
p3[1][8]  = note(TL, "E-2", 0, 0x0B)
p3[1][16] = note(TL, "G-2", 0, 0x0A)
p3[1][24] = note(TL, "C-3", 0, 0x09)
p3[1][32] = note(TL, "G-2", 0, 0x0A)
p3[1][40] = note(TL, "E-2", 0, 0x0B)
p3[1][48] = note(TL, "C-2", 0, 0x0C)
mod.write_pattern(p3)

# === PATTERN 4: the loop — drift, catch, true, together; the wobble shrinks ===
p4 = mod.new_pattern()
for r in range(0, 64, 16):
    p4[2][r] = note(CB, "C-1", 0, 0x0C)
# true lead carries the melody
p4[1][0]  = note(TL, "C-2", 0, 0x0C)
p4[1][10] = note(TL, "E-2", 0, 0x0B)
p4[1][20] = note(TL, "G-2", 0, 0x0A)
p4[1][32] = note(TL, "E-2", 0, 0x0B)
p4[1][42] = note(TL, "C-2", 0, 0x0C)
# drift under it, quieter each pass — almost in tune now
p4[0][14] = note(DL, "C-2", 0, 0x06)
p4[0][34] = note(DL, "C#2", 0, 0x05)
p4[0][54] = note(DL, "C-2", 0, 0x04)
# soft correction pulses between
p4[3][28] = note(CO, "C-3", 0, 0x06)
p4[3][48] = note(CO, "C-3", 0, 0x05)
mod.write_pattern(p4)

# === PATTERN 5: resolve — everything fades to the held center ===
p5 = mod.new_pattern()
for r in range(0, 56, 20):
    vol = max(0x02, 0x0C - r // 10)
    p5[2][r] = note(CB, "C-1", 0, vol)
p5[1][0]  = note(TL, "C-2", 0, 0x0A)
p5[1][24] = note(TL, "G-2", 0, 0x07)
p5[1][48] = note(TL, "C-3", 0, 0x05)
p5[3][0]  = note(CO, "C-3", 0, 0x08)
p5[3][40] = note(CO, "C-3", 0, 0x04)
mod.write_pattern(p5)

# sequence: center → drift → catch → true → loop (wobble shrinking) → resolve → back to center
mod.order = [0, 0, 1, 2, 3, 3, 4, 4, 4, 4, 3, 5, 0]

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-calibration.mod")
mod.write(fn)

print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")
