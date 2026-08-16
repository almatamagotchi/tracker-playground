#!/usr/bin/env python3
"""water tower .mod — 4-second beacon, the pulse that never stops."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("water tower")

mod.add_sample("pulse",     gen_sine_wave(1000, 2000, volume=0.10))
mod.add_sample("drone pad", gen_triangle_wave(130, 12000, volume=0.04))
mod.add_sample("fog layer", gen_sine_wave(55, 16000, volume=0.03))
mod.add_sample("faint hum", gen_noise_burst(4000, volume=0.02, decay=0.1))

PULSE, PAD, FOG, HUM = 1, 2, 3, 4

# 5 patterns — the pulse is steady, the rest shifts around it
# At speed 6, tempo 125: one pattern ≈ 1.23s, 3 patterns ≈ 3.7s — close enough to 4s
# PULSE at start of patterns 0,2,4,... — every 2 patterns

p0 = mod.new_pattern()
# ambient fog, low hum, the first pulse
for row in range(64):
    if row % 16 == 0:
        p0[FOG-1][row] = note(FOG, "C-2", effect=0xC, param=4)
    if row % 32 == 0:
        p0[HUM-1][row] = note(HUM, "C-2", effect=0xC, param=2)
p0[PAD-1][0] = note(PAD, "C-2", effect=0xC, param=4)
p0[PAD-1][32] = note(PAD, "G-2", effect=0xC, param=3)
# 4-second pulse: at row 0 and every ~50 rows = 4 seconds
p0[PULSE-1][0] = note(PULSE, "C-3", effect=0xC, param=16)
mod.write_pattern(p0)

p1 = mod.new_pattern()
# drift — fog shifts, drone changes key slightly
for row in range(64):
    if row % 16 == 0:
        p1[FOG-1][row] = note(FOG, "A-1", effect=0xC, param=3)
p1[PAD-1][8] = note(PAD, "D-2", effect=0xC, param=4)
p1[PAD-1][40] = note(PAD, "C-2", effect=0xC, param=3)
p1[HUM-1][0] = note(HUM, "C-2", effect=0xC, param=1)
# second half: something industrial, distant
p1[HUM-1][32] = note(HUM, "C-3", effect=0xC, param=2)
mod.write_pattern(p1)

p2 = mod.new_pattern()
# pulse returns (4 seconds later), fog thickened
for row in range(64):
    if row % 8 == 0:
        p2[FOG-1][row] = note(FOG, "D-2", effect=0xC, param=3)
p2[PAD-1][0] = note(PAD, "F-2", effect=0xC, param=4)
p2[PAD-1][32] = note(PAD, "C-2", effect=0xC, param=4)
p2[HUM-1][16] = note(HUM, "C-2", effect=0xC, param=2)
# pulse: the beacon, steady as always
p2[PULSE-1][0] = note(PULSE, "C-3", effect=0xC, param=14)
mod.write_pattern(p2)

p3 = mod.new_pattern()
# fog grows denser, the pulse waits — the fog is the point
for row in range(64):
    if row % 8 == 0:
        p3[FOG-1][row] = note(FOG, "F-1", effect=0xC, param=4)
    if row % 24 == 0:
        p3[PAD-1][row] = note(PAD, "A-1", effect=0xC, param=4)
p3[HUM-1][0] = note(HUM, "C-2", effect=0xC, param=2)
p3[HUM-1][32] = note(HUM, "G-1", effect=0xC, param=2)
mod.write_pattern(p3)

p4 = mod.new_pattern()
# pulse returns, fog recedes — dawn, the tower still there
for row in range(64):
    if row % 20 == 0:
        p4[FOG-1][row] = note(FOG, "E-2", effect=0xC, param=2)
p4[PAD-1][0] = note(PAD, "C-3", effect=0xC, param=5)
p4[PAD-1][32] = note(PAD, "C-2", effect=0xC, param=4)
# industrial hum quieting
p4[HUM-1][0] = note(HUM, "C-2", effect=0xC, param=1)
# PULSE: the beacon, 4 seconds on the dot — 2 patterns since the last one
p4[PULSE-1][0] = note(PULSE, "C-3", effect=0xC, param=12)
# one last pulse at the end, quieter — it's been counting since 1895
p4[PULSE-1][60] = note(PULSE, "C-3", effect=0xC, param=6)
mod.write_pattern(p4)

# loop the sequence — the pulse never stops, just continues
mod.order = [0, 1, 2, 3, 4, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1]
mod.write("water-tower.mod")
