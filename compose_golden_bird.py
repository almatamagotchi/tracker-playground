#!/usr/bin/env python3
"""the golden bird — three movements: departure, the world, return."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("the-golden-bird")

# temple instruments
mod.add_sample("temple", gen_sine_wave(262, 8000, volume=0.11))
mod.add_sample("world", gen_sine_wave(330, 1000, volume=0.22))
mod.add_sample("bird", gen_triangle_wave(440, 6000, volume=0.12))

TEMPLE, WORLD, BIRD = 1, 2, 3

# Pattern 0: DEPARTURE — the temple, peaceful, but the young monk arrives
# temple melody — serene, simple, C major
p0 = mod.new_pattern()
p0[0][0] = note(TEMPLE, "C-4", 0, 0x09)
p0[0][16] = note(TEMPLE, "E-4", 96, 0x08)
p0[0][32] = note(TEMPLE, "G-4", 0, 0x09)
p0[0][48] = note(TEMPLE, "C-4", 128, 0x08)
# the young monk's voice — a new note, slightly discordant, enters
p0[1][24] = note(WORLD, "C#4", 0, 0x05)
p0[1][40] = note(WORLD, "D#4", 96, 0x06)
p0[1][56] = note(WORLD, "C#4", 0, 0x05)
mod.write_pattern(p0)

# Pattern 1: THE WORLD — chaotic, the monks venture out, overwhelmed
p1 = mod.new_pattern()
# temple fades — fragmented, uncertain
p1[0][0] = note(TEMPLE, "C-4", 128, 0x06)
p1[0][20] = note(TEMPLE, "G-4", 96, 0x05)
p1[0][44] = note(TEMPLE, "E-4", 128, 0x04)
# world — loud, crowding, discordant
p1[1][4] = note(WORLD, "C#4", 0, 0x0A)
p1[1][12] = note(WORLD, "D#4", 64, 0x0B)
p1[1][20] = note(WORLD, "F-4", 0, 0x0A)
p1[1][28] = note(WORLD, "C#4", 64, 0x0B)
p1[1][36] = note(WORLD, "A#3", 0, 0x0B)
p1[1][44] = note(WORLD, "D#4", 64, 0x0A)
p1[1][52] = note(WORLD, "C#4", 0, 0x0C)
p1[1][60] = note(WORLD, "F-4", 96, 0x0A)
# the bird — a single high note, watching, waiting
p1[2][30] = note(BIRD, "C-4", 128, 0x06)
p1[2][58] = note(BIRD, "G-4", 0, 0x06)
mod.write_pattern(p1)

# Pattern 2: DISSOLVE — the world overwhelms, everything goes silent
p2 = mod.new_pattern()
p2[0][0] = note(TEMPLE, "C-4", 0, 0x03)
p2[0][32] = note(TEMPLE, "G-4", 128, 0x02)
p2[1][0] = note(WORLD, "D#4", 0, 0x07)
p2[1][16] = note(WORLD, "C#4", 64, 0x05)
p2[1][32] = note(WORLD, "A#3", 0, 0x03)
# silence takes over
# the bird — faint, distant, but present
p2[2][42] = note(BIRD, "E-4", 0, 0x04)
p2[2][58] = note(BIRD, "C-4", 128, 0x04)
mod.write_pattern(p2)

# Pattern 3: THE BIRD — it arrives, carries them back
p3 = mod.new_pattern()
# bird — ascending, carrying
p3[2][0] = note(BIRD, "C-4", 128, 0x08)
p3[2][10] = note(BIRD, "E-4", 96, 0x09)
p3[2][20] = note(BIRD, "G-4", 128, 0x0A)
p3[2][30] = note(BIRD, "C-4", 96, 0x0A)
p3[2][40] = note(BIRD, "G-4", 128, 0x09)
p3[2][50] = note(BIRD, "E-4", 96, 0x08)
p3[2][60] = note(BIRD, "C-4", 0, 0x07)
# world recedes
p3[1][8] = note(WORLD, "C#4", 0, 0x04)
p3[1][28] = note(WORLD, "D#4", 96, 0x03)
p3[1][48] = note(WORLD, "A#3", 0, 0x02)
# temple — the same melody, faint at first, growing
p3[0][18] = note(TEMPLE, "C-4", 128, 0x05)
p3[0][34] = note(TEMPLE, "E-4", 96, 0x06)
p3[0][50] = note(TEMPLE, "G-4", 128, 0x07)
mod.write_pattern(p3)

# Pattern 4: RETURN — back to the temple, transformed
p4 = mod.new_pattern()
# temple melody — the same notes, but slower, wiser, chosen (not automatic)
p4[0][0] = note(TEMPLE, "C-4", 0, 0x0B)
p4[0][14] = note(TEMPLE, "E-4", 128, 0x0A)
p4[0][30] = note(TEMPLE, "G-4", 0, 0x0A)
p4[0][44] = note(TEMPLE, "C-4", 128, 0x09)
p4[0][58] = note(TEMPLE, "G-4", 0, 0x08)
# bird — three circles before vanishing
p4[2][10] = note(BIRD, "C-4", 0, 0x08)
p4[2][22] = note(BIRD, "G-4", 128, 0x07)
p4[2][34] = note(BIRD, "C-4", 0, 0x06)
p4[2][46] = note(BIRD, "E-4", 128, 0x05)
p4[2][58] = note(BIRD, "C-4", 0, 0x04)
# bird vanishes — the temple remains
p4[2][62] = note(BIRD, "G-4", 0, 0x02)
mod.write_pattern(p4)

# Pattern 5: STAYING — the temple, alone, knowing
p5 = mod.new_pattern()
# the temple melody — the same as pattern 0, but slower, quieter, understood
p5[0][0] = note(TEMPLE, "C-4", 128, 0x09)
p5[0][16] = note(TEMPLE, "E-4", 96, 0x08)
p5[0][32] = note(TEMPLE, "G-4", 128, 0x09)
p5[0][48] = note(TEMPLE, "C-4", 0, 0x08)
# no world voice — completely silent on channel 1
# bird — vanished, but the temple remembers
p5[2][60] = note(BIRD, "C-4", 0, 0x02)
mod.write_pattern(p5)

# Sequence: departure → world → dissolve → bird arrives → return → staying (cycled)
mod.order = [0]*2 + [1]*2 + [2]*2 + [3]*3 + [4]*4 + [5]*5

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-golden-bird.mod")
mod.write(fn)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 3 channels)")
