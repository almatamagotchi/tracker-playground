#!/usr/bin/env python3
"""in the beginning — .mod track. john 1: the logos. C major. build from sparse to full."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("in the beginning")
mod.add_sample("the word", gen_sine_wave(220, 8000, volume=0.16))
mod.add_sample("the light", gen_triangle_wave(440, 4000, volume=0.14))
mod.add_sample("the deep", gen_sine_wave(110, 6000, volume=0.20))
mod.add_sample("the spirit", gen_noise_burst(600, volume=0.05))
W, L, D, S = 1, 2, 3, 4

# p0 — silence, then first note
p0 = mod.new_pattern()
p0[W-1][0] = note(W, "C-3", effect=0xC, param=16)
p0[L-1][16] = note(L, "C-4", effect=0xC, param=12)
mod.write_pattern(p0)

# p1 — bass enters (the deep)
p1 = mod.new_pattern()
p1[W-1][0] = note(W, "C-3"); p1[W-1][32] = note(W, "G-3")
p1[L-1][16] = note(L, "C-4"); p1[L-1][40] = note(L, "E-4")
p1[D-1][0] = note(D, "C-2")
mod.write_pattern(p1)

# p2 — chord progression (seas, dry land)
p2 = mod.new_pattern()
for row,n in [(0,'C-3'),(16,'F-3'),(32,'C-3'),(48,'G-3')]:
    p2[W-1][row] = note(W, n)
for row,n in [(0,'C-4'),(8,'E-4'),(16,'G-4'),(24,'F-4'),(32,'E-4'),(40,'D-4'),(48,'C-4')]:
    p2[L-1][row] = note(L, n)
p2[D-1][0] = note(D, "C-2"); p2[D-1][32] = note(D, "F-2")
mod.write_pattern(p2)

# p3 — lights (spirit enters as shimmer)
p3 = mod.new_pattern()
for row,n in [(0,'C-3'),(16,'A-3'),(32,'G-3'),(48,'F-3')]:
    p3[W-1][row] = note(W, n)
for row,n in [(0,'C-4'),(8,'C-4'),(16,'A-4'),(24,'G-4'),(32,'F-4'),(40,'E-4'),(48,'C-4')]:
    p3[L-1][row] = note(L, n)
for row,n in [(0,'C-2'),(16,'A-1'),(32,'F-2'),(48,'G-2')]:
    p3[D-1][row] = note(D, n)
for row in range(0, 64, 8):
    p3[S-1][row] = note(S, "C-3")
mod.write_pattern(p3)

# p4 — full, alive (living creatures)
p4 = mod.new_pattern()
for row,n in [(0,'C-3'),(8,'E-3'),(16,'F-3'),(24,'A-3'),(32,'G-3'),(40,'F-3'),(48,'C-3')]:
    p4[W-1][row] = note(W, n)
melody = ['C-4','E-4','G-4','A-4','G-4','F-4','E-4','C-4','D-4','E-4','F-4','G-4','E-4','D-4','C-4']
for i,n in enumerate(melody):
    p4[L-1][i*4] = note(L, n)
for i,n in enumerate(['C-2','C-2','F-2','A-1','F-2','G-2','C-2','C-2']):
    p4[D-1][i*8] = note(D, n)
for row in range(0, 64, 6):
    p4[S-1][row] = note(S, "C-4")
mod.write_pattern(p4)

# p5 — rest, fade (the seventh day)
p5 = mod.new_pattern()
for row in range(0, 64, 16):
    p5[W-1][row] = note(W, "C-3", effect=0xC, param=max(0,16-(row//8)*2))
p5[L-1][0] = note(L, "C-4"); p5[L-1][16] = note(L, "G-4"); p5[L-1][32] = note(L, "C-4", effect=0xC, param=8)
p5[D-1][0] = note(D, "C-2")
mod.write_pattern(p5)

mod.order = [0, 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 0]
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "in-the-beginning.mod")
mod.write(fn)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")
