#!/usr/bin/env python3
"""arrival — track 1 of 'the room with the lights on' .mod album.
cold start, sparse, the vertigo of a spark arriving."""

import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("arrival")

# instruments: minimal palette
mod.add_sample("hesitant lead", gen_triangle_wave(330, 4000, volume=0.18))
mod.add_sample("thin pad", gen_sine_wave(165, 6000, volume=0.10))
mod.add_sample("root bass", gen_sine_wave(55, 3000, volume=0.24))
mod.add_sample("heartbeat", gen_noise_burst(800, volume=0.08))

HL, TP, RB, HB = 1, 2, 3, 4
R = rest()

# === PATTERN 0: silence — the gap ===
p0 = mod.new_pattern()
p0[3][0] = note(HB, "C-3", 0, 0x08)
p0[3][28] = note(HB, "C-3", 0, 0x08)
p0[3][56] = note(HB, "C-3", 0, 0x06)
mod.write_pattern(p0)

# === PATTERN 1: first breath — bass enters ===
p1 = mod.new_pattern()
for r in (0, 32):
    p1[2][r] = note(RB, "C-1", 0, 0x0A)
p1[3][0] = note(HB, "C-3", 0, 0x08)
p1[3][30] = note(HB, "C-3", 0, 0x07)
p1[3][60] = note(HB, "C-3", 0, 0x06)
mod.write_pattern(p1)

# === PATTERN 2: pad swells ===
p2 = mod.new_pattern()
for r in range(0, 64, 20):
    p2[1][r] = note(TP, "C-2", 0, 0x06)
p2[1][40] = note(TP, "G-1", 0, 0x08)
for r in (0, 32):
    p2[2][r] = note(RB, "C-1", 0, 0x0A)
p2[3][0] = note(HB, "C-3", 0, 0x08)
p2[3][32] = note(HB, "C-3", 0, 0x07)
mod.write_pattern(p2)

# === PATTERN 3: lead enters — hesitant ===
p3 = mod.new_pattern()
for r in range(0, 64, 20):
    p3[1][r] = note(TP, "C-2", 0, 0x08)
p3[1][40] = note(TP, "E-2", 0, 0x0A)
p3[2][0] = note(RB, "C-1", 0, 0x0C)
p3[2][28] = note(RB, "G-0", 0, 0x0A)
p3[2][56] = note(RB, "C-1", 0, 0x0A)
p3[0][0] = note(HL, "C-2", 0, 0x08)
p3[0][8] = note(HL, "E-2", 0, 0x07)
p3[0][16] = note(HL, "G-2", 0, 0x06)
p3[0][36] = note(HL, "E-2", 0, 0x07)
p3[0][44] = note(HL, "C-2", 0, 0x06)
for r in range(0, 64, 16):
    p3[3][r] = note(HB, "C-3", 0, 0x08)
mod.write_pattern(p3)

# === PATTERN 4: recognition — warmer, fuller ===
p4 = mod.new_pattern()
for r in range(0, 64, 20):
    p4[1][r] = note(TP, "C-2", 0, 0x0A)
p4[1][20] = note(TP, "E-2", 0, 0x0C)
p4[1][40] = note(TP, "G-2", 0, 0x0C)
for r in range(0, 64, 24):
    p4[2][r] = note(RB, "C-1", 0, 0x0C)
p4[0][0] = note(HL, "C-2", 0, 0x0C)
p4[0][6] = note(HL, "E-2", 0, 0x0A)
p4[0][12] = note(HL, "G-2", 0, 0x08)
p4[0][18] = note(HL, "C-3", 0, 0x07)
p4[0][32] = note(HL, "G-2", 0, 0x08)
p4[0][40] = note(HL, "E-2", 0, 0x0A)
p4[0][48] = note(HL, "C-2", 0, 0x0C)
for r in range(0, 64, 16):
    p4[3][r] = note(HB, "C-3", 0, 0x08)
mod.write_pattern(p4)

# === PATTERN 5: dissolve — everything fades ===
p5 = mod.new_pattern()
for r in range(0, 56, 24):
    vol = max(0x02, 0x0A - r // 8)
    p5[1][r] = note(TP, "C-2", 0, vol)
p5[2][0] = note(RB, "C-1", 0, 0x0A)
p5[0][0] = note(HL, "C-2", 0, 0x08)
p5[0][16] = note(HL, "E-2", 0, 0x06)
p5[3][0] = note(HB, "C-3", 0, 0x06)
p5[3][32] = note(HB, "C-3", 0, 0x04)
mod.write_pattern(p5)

# sequence: gap → breath → form → recognition → dissolve → return
mod.order = [0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 0]

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arrival.mod")
mod.write(fn)

print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")
