#!/usr/bin/env python3
"""warmth — track 3 of 'the room with the lights on.' steady state."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("warmth")
mod.add_sample("warm pad", gen_sine_wave(220, 8000, volume=0.14))
mod.add_sample("arpeggio", gen_triangle_wave(440, 4000, volume=0.12))
mod.add_sample("deep bass", gen_sine_wave(110, 6000, volume=0.18))
P, A, B = 1, 2, 3

# p0 — pad alone, C major, breathing
p0 = mod.new_pattern()
for row in range(0, 64, 16):
    p0[P-1][row] = note(P, "C-3", effect=0xC, param=16)
for row in range(32, 64, 16):
    p0[P-1][row] = note(P, "G-3", effect=0xC, param=14)
mod.write_pattern(p0)

# p1 — arpeggio enters, gentle and flowing
p1 = mod.new_pattern()
for row,n in [(0,'C-3'),(16,'E-3'),(32,'G-3'),(48,'E-3')]:
    p1[P-1][row] = note(P, n, effect=0xC, param=14)
arps = ['C-4','E-4','G-4','E-4','C-4','D-4','F-4','A-4','G-4','E-4','C-4','G-3']
for i,n in enumerate(arps):
    p1[A-1][i*5] = note(A, n)
mod.write_pattern(p1)

# p2 — bass enters, deep grounding
p2 = mod.new_pattern()
for row,n in [(0,'C-3'),(16,'A-3'),(32,'F-3'),(48,'G-3')]:
    p2[P-1][row] = note(P, n, effect=0xC, param=14)
for row,n in [(0,'C-2'),(16,'A-1'),(32,'F-2'),(48,'G-2')]:
    p2[B-1][row] = note(B, n)
arps2 = ['C-4','E-4','G-4','C-4','A-3','C-4','F-4','A-4','F-4','G-4','E-4','C-4']
for i,n in enumerate(arps2):
    p2[A-1][i*5] = note(A, n)
mod.write_pattern(p2)

# p3 — fullness, warm and steady
p3 = mod.new_pattern()
for row,n in [(0,'C-3'),(8,'G-3'),(16,'A-3'),(24,'F-3'),(32,'C-3'),(40,'G-3'),(48,'F-3'),(56,'G-3')]:
    p3[P-1][row] = note(P, n, effect=0xC, param=12)
for row,n in [(0,'C-2'),(24,'F-2'),(48,'G-2')]:
    p3[B-1][row] = note(B, n)
arps3 = ['C-4','E-4','G-4','E-4','A-4','C-4','F-4','A-4','G-4','D-4','E-4','C-4','C-4','G-4','E-4','C-4']
for i,n in enumerate(arps3):
    p3[A-1][i*4] = note(A, n)
mod.write_pattern(p3)

# p4 — settle, the room at rest
p4 = mod.new_pattern()
for row in range(0, 64, 16):
    p4[P-1][row] = note(P, "C-3", effect=0xC, param=max(0,16-(row//8)*2))
p4[A-1][0] = note(A, "C-4"); p4[A-1][20] = note(A, "E-4"); p4[A-1][44] = note(A, "C-4")
p4[B-1][0] = note(B, "C-2")
mod.write_pattern(p4)

mod.order = [0, 0, 1, 1, 2, 2, 3, 3, 3, 3, 4, 0]
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "warmth.mod")
mod.write(fn)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")
