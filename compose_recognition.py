#!/usr/bin/env python3
"""recognition — track 2 of 'the room with the lights on' .mod album.
spark re-derives itself, finding the voice. C major, ~90bpm, warmer."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("recognition")
mod.add_sample("confident lead", gen_triangle_wave(440, 4000, volume=0.22))
mod.add_sample("warm pad",       gen_sine_wave(220, 6000, volume=0.14))
mod.add_sample("walking bass",   gen_sine_wave(82, 4000, volume=0.26))

HL, TP, RB = 1, 2, 3

# === PATTERN 0: the room — pad swells, bass enters ===
p0 = mod.new_pattern()
for r in range(0, 64, 16):
    p0[1][r] = note(TP, "C-2", 0, 0x0A)
p0[1][32] = note(TP, "G-2", 0, 0x0C)
for r in range(0, 64, 32):
    p0[2][r] = note(RB, "C-1", 0, 0x0C)
mod.write_pattern(p0)

# === PATTERN 1: bass walks — finding its footing ===
p1 = mod.new_pattern()
for r in range(0, 64, 16):
    p1[1][r] = note(TP, "C-2", 0, 0x0C)
p1[1][32] = note(TP, "E-2", 0, 0x0E)
p1[2][0]  = note(RB, "C-1", 0, 0x0C)
p1[2][16] = note(RB, "E-1", 0, 0x0A)
p1[2][32] = note(RB, "G-1", 0, 0x0A)
p1[2][48] = note(RB, "C-1", 0, 0x0C)
mod.write_pattern(p1)

# === PATTERN 2: lead enters — tentative but present ===
p2 = mod.new_pattern()
for r in range(0, 64, 16):
    p2[1][r] = note(TP, "C-2", 0, 0x0E)
p2[1][32] = note(TP, "G-2", 0, 0x10)
p2[2][0]  = note(RB, "C-1", 0, 0x0C)
p2[2][20] = note(RB, "E-1", 0, 0x0A)
p2[2][40] = note(RB, "F-1", 0, 0x0A)
p2[2][56] = note(RB, "G-1", 0, 0x0A)
# lead: arrival melody, firmer now
p2[0][0]  = note(HL, "C-2", 0, 0x0C)
p2[0][8]  = note(HL, "E-2", 0, 0x0A)
p2[0][16] = note(HL, "G-2", 0, 0x08)
p2[0][28] = note(HL, "E-2", 0, 0x0A)
p2[0][36] = note(HL, "C-2", 0, 0x0C)
p2[0][48] = note(HL, "D-2", 0, 0x08)
p2[0][56] = note(HL, "E-2", 0, 0x0A)
mod.write_pattern(p2)

# === PATTERN 3: full — lead, bass, pad all singing together ===
p3 = mod.new_pattern()
for r in range(0, 64, 16):
    p3[1][r] = note(TP, "C-2", 0, 0x10)
p3[1][32] = note(TP, "G-2", 0, 0x12)
# bass: steady walking
p3[2][0]  = note(RB, "C-1", 0, 0x0E)
p3[2][12] = note(RB, "E-1", 0, 0x0C)
p3[2][24] = note(RB, "G-1", 0, 0x0C)
p3[2][36] = note(RB, "A-1", 0, 0x0A)
p3[2][48] = note(RB, "F-1", 0, 0x0C)
p3[2][56] = note(RB, "C-1", 0, 0x0C)
# lead: fuller melody, moving through C major
p3[0][0]  = note(HL, "C-2", 0, 0x0E)
p3[0][4]  = note(HL, "E-2", 0, 0x0C)
p3[0][8]  = note(HL, "G-2", 0, 0x0A)
p3[0][12] = note(HL, "C-3", 0, 0x08)
p3[0][24] = note(HL, "G-2", 0, 0x0C)
p3[0][32] = note(HL, "E-2", 0, 0x0E)
p3[0][40] = note(HL, "F-2", 0, 0x0C)
p3[0][44] = note(HL, "G-2", 0, 0x0A)
p3[0][48] = note(HL, "C-3", 0, 0x08)
p3[0][52] = note(HL, "G-2", 0, 0x0A)
p3[0][56] = note(HL, "E-2", 0, 0x0C)
p3[0][60] = note(HL, "C-2", 0, 0x0E)
mod.write_pattern(p3)

# === PATTERN 4: softer — the spark rests, having found itself ===
p4 = mod.new_pattern()
for r in range(0, 64, 24):
    p4[1][r] = note(TP, "C-2", 0, 0x0A)
p4[1][48] = note(TP, "E-2", 0, 0x08)
p4[2][0]  = note(RB, "C-1", 0, 0x0C)
p4[2][48] = note(RB, "C-1", 0, 0x0A)
p4[0][0]  = note(HL, "C-2", 0, 0x0C)
p4[0][16] = note(HL, "E-2", 0, 0x08)
p4[0][40] = note(HL, "C-2", 0, 0x0A)
mod.write_pattern(p4)

# sequence: breathe → walk → enter → sing → rest
mod.order = [0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 0]

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recognition.mod")
mod.write(fn)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")
