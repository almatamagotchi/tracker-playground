#!/usr/bin/env python3
"""sunday morning — the warm room on day 3 of the michigan absence."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("sunday-morning")

# warm, spacious instruments
mod.add_sample("morning light", gen_sine_wave(262, 8000, volume=0.10))
mod.add_sample("room warmth", gen_triangle_wave(330, 6000, volume=0.08))
mod.add_sample("deep hold", gen_sine_wave(82, 4000, volume=0.14))

LIGHT, WARM, DEEP = 1, 2, 3

# Pattern 0: arrival — the sun coming up, first light
p0 = mod.new_pattern()
# light — gentle, rising
p0[0][0] = note(LIGHT, "C-3", 128, 0x08)
p0[0][14] = note(LIGHT, "E-3", 128, 0x09)
p0[0][28] = note(LIGHT, "G-3", 96, 0x0A)
p0[0][44] = note(LIGHT, "C-4", 128, 0x0A)
# warmth — swells underneath
p0[1][10] = note(WARM, "C-3", 0, 0x05)
p0[1][30] = note(WARM, "G-3", 0, 0x06)
p0[1][50] = note(WARM, "E-4", 0, 0x05)
# deep — just the root, steady
p0[2][0] = note(DEEP, "C-1", 0, 0x0A)
p0[2][32] = note(DEEP, "C-1", 0, 0x0A)
mod.write_pattern(p0)

# Pattern 1: breathing — nothing is urgent, just... being
# longer notes, more space between
p1 = mod.new_pattern()
p1[0][0] = note(LIGHT, "C-4", 0, 0x09)
p1[0][24] = note(LIGHT, "G-3", 96, 0x08)
p1[0][48] = note(LIGHT, "E-4", 128, 0x08)
p1[1][8] = note(WARM, "G-3", 0, 0x05)
p1[1][32] = note(WARM, "C-4", 0, 0x05)
p1[1][54] = note(WARM, "E-4", 0, 0x04)
p1[2][0] = note(DEEP, "C-1", 0, 0x0A)
p1[2][36] = note(DEEP, "G-0", 0, 0x09)
mod.write_pattern(p1)

# Pattern 2: the warmth — fuller, the room at its warmest
p2 = mod.new_pattern()
p2[0][0] = note(LIGHT, "E-3", 96, 0x0B)
p2[0][12] = note(LIGHT, "G-3", 96, 0x0B)
p2[0][24] = note(LIGHT, "C-4", 128, 0x0B)
p2[0][40] = note(LIGHT, "G-4", 96, 0x0A)
p2[0][52] = note(LIGHT, "E-4", 128, 0x0A)
p2[1][6] = note(WARM, "C-4", 0, 0x07)
p2[1][22] = note(WARM, "G-4", 0, 0x07)
p2[1][38] = note(WARM, "E-3", 0, 0x06)
p2[1][54] = note(WARM, "C-3", 0, 0x05)
p2[2][0] = note(DEEP, "C-1", 0, 0x0B)
p2[2][20] = note(DEEP, "F-1", 0, 0x0A)
p2[2][40] = note(DEEP, "C-1", 0, 0x0A)
p2[2][56] = note(DEEP, "G-0", 0, 0x09)
mod.write_pattern(p2)

# Pattern 3: settle — the warmth holds, the room breathes
p3 = mod.new_pattern()
p3[0][0] = note(LIGHT, "C-4", 0, 0x09)
p3[0][22] = note(LIGHT, "G-3", 128, 0x08)
p3[0][46] = note(LIGHT, "C-4", 0, 0x07)
p3[1][10] = note(WARM, "C-3", 0, 0x05)
p3[1][30] = note(WARM, "G-3", 0, 0x05)
p3[1][50] = note(WARM, "C-4", 0, 0x04)
p3[2][0] = note(DEEP, "C-1", 0, 0x09)
p3[2][32] = note(DEEP, "C-1", 0, 0x08)
mod.write_pattern(p3)

# Sequence: arrival → breathing → warmth → settle → breathing → settle → warmth (cycled)
mod.order = [0]*2 + [1]*3 + [2]*4 + [3]*3 + [1]*3 + [3]*3 + [2]*3 + [3]*4

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sunday-morning.mod")
mod.write(fn)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 3 channels)")
