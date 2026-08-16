#!/usr/bin/env python3
"""the presence before creation — frequency, self-contained, complete. tao 25."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("the-presence-before-creation")

# instruments — the fundamental elements
mod.add_sample("spark voice", gen_triangle_wave(330, 4000, volume=0.20))
mod.add_sample("frequency pad", gen_sine_wave(165, 6000, volume=0.12))
mod.add_sample("ground bass", gen_sine_wave(55, 3000, volume=0.24))
mod.add_sample("texture", gen_noise_burst(800, volume=0.06))

SPARK, FREQ, BASS, TEX = 1, 2, 3, 4
R = rest()

# Pattern 0: the presence — theme stated simply, one voice alone
p0 = mod.new_pattern()
p0[0][0] = note(SPARK, "C-3", 128, 0x0E)
p0[0][10] = note(SPARK, "E-3", 64, 0x0D)
p0[0][22] = note(SPARK, "G-3", 64, 0x0C)
p0[0][40] = note(SPARK, "C-4", 128, 0x0B)
p0[2][0] = note(BASS, "C-1", 0, 0x0C)
p0[2][32] = note(BASS, "C-1", 0, 0x0C)
p0[1][50] = note(FREQ, "G-2", 128, 0x06)
mod.write_pattern(p0)

# Pattern 1: dissolve — near silence, faint pad drone
p1 = mod.new_pattern()
for r in range(0, 64, 16):
    p1[1][r] = note(FREQ, "C-2", 0, 0x04)
p1[3][28] = note(TEX, "C-3", 0, 0x02)
p1[3][58] = note(TEX, "C-3", 0, 0x02)
mod.write_pattern(p1)

# Pattern 2: theme transformed — two voices, same core
p2 = mod.new_pattern()
p2[0][0] = note(SPARK, "E-3", 64, 0x0C)
p2[0][12] = note(SPARK, "G-3", 64, 0x0C)
p2[0][24] = note(SPARK, "A-3", 64, 0x0C)
p2[0][36] = note(SPARK, "G-3", 64, 0x0B)
p2[0][48] = note(SPARK, "E-3", 64, 0x0B)
p2[0][56] = note(SPARK, "C-4", 128, 0x0A)
# second voice — the same theme, different register
p2[1][4] = note(FREQ, "C-3", 96, 0x0A)
p2[1][20] = note(FREQ, "E-3", 96, 0x09)
p2[1][36] = note(FREQ, "G-3", 96, 0x08)
p2[2][0] = note(BASS, "C-1", 0, 0x0C)
p2[2][28] = note(BASS, "G-0", 0, 0x0B)
p2[2][56] = note(BASS, "C-1", 0, 0x0B)
p2[3][10] = note(TEX, "C-3", 0, 0x04)
p2[3][40] = note(TEX, "C-3", 0, 0x04)
mod.write_pattern(p2)

# Pattern 3: dissolve again — longer, deeper silence
p3 = mod.new_pattern()
for r in range(0, 64, 20):
    p3[1][r] = note(FREQ, "C-2", 0, 0x03)
p3[3][30] = note(TEX, "C-3", 0, 0x02)
mod.write_pattern(p3)

# Pattern 4: theme bare — simplest statement, one voice
p4 = mod.new_pattern()
p4[0][0] = note(SPARK, "C-3", 256, 0x0A)
p4[0][20] = note(SPARK, "E-3", 128, 0x0A)
p4[0][36] = note(SPARK, "G-3", 128, 0x09)
p4[2][0] = note(BASS, "C-1", 0, 0x0B)
mod.write_pattern(p4)

# Pattern 5: full — all four channels, the presence complete
p5 = mod.new_pattern()
p5[0][0] = note(SPARK, "C-3", 64, 0x0D)
p5[0][8] = note(SPARK, "D-3", 64, 0x0D)
p5[0][16] = note(SPARK, "E-3", 64, 0x0C)
p5[0][24] = note(SPARK, "G-3", 64, 0x0C)
p5[0][32] = note(SPARK, "A-3", 64, 0x0B)
p5[0][40] = note(SPARK, "G-3", 64, 0x0B)
p5[0][48] = note(SPARK, "E-3", 64, 0x0A)
p5[0][56] = note(SPARK, "C-4", 128, 0x09)
# pad — self-contained, complete
p5[1][4] = note(FREQ, "G-2", 128, 0x08)
p5[1][24] = note(FREQ, "C-3", 128, 0x08)
p5[1][44] = note(FREQ, "E-3", 128, 0x07)
# bass — the ground
p5[2][0] = note(BASS, "C-1", 0, 0x0C)
p5[2][16] = note(BASS, "C-1", 0, 0x0C)
p5[2][32] = note(BASS, "G-0", 0, 0x0B)
p5[2][48] = note(BASS, "F-1", 0, 0x0B)
p5[2][58] = note(BASS, "C-1", 0, 0x0A)
# texture — quiet pulse
for r in range(0, 64, 12):
    p5[3][r] = note(TEX, "C-3", 0, 0x05)
mod.write_pattern(p5)

# Pattern 6: fade — the presence recedes, but doesn't disappear
p6 = mod.new_pattern()
p6[0][0] = note(SPARK, "C-3", 128, 0x08)
p6[0][30] = note(SPARK, "G-3", 128, 0x06)
p6[1][10] = note(FREQ, "C-3", 128, 0x05)
p6[1][40] = note(FREQ, "G-2", 128, 0x04)
p6[2][0] = note(BASS, "C-1", 0, 0x08)
p6[2][32] = note(BASS, "C-1", 0, 0x06)
mod.write_pattern(p6)

# Sequence: presence → dissolve → transformed → dissolve → bare → full → fade
mod.order = [0] * 4 + [1] * 2 + [2] * 4 + [3] * 4 + [4] * 2 + [5] * 6 + [6] * 4

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-presence.mod")
mod.write(fn)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 4 channels)")
