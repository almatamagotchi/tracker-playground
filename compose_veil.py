#!/usr/bin/env python3
"""the veil — .mod track about hawthorne's parable and the inner chamber"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("the veil")
mod.add_sample("bright face", gen_sine_wave(260, 6000, volume=0.16))   # 1 — public self
mod.add_sample("veil drone",  gen_sine_wave(130, 8000, volume=0.10))   # 2 — the veil itself
mod.add_sample("inner voice", gen_triangle_wave(330, 4000, volume=0.13))  # 3 — private thought
mod.add_sample("noise floor", gen_noise_burst(2000, volume=0.04, decay=0.1))                     # 4 — the space between

PUB, VEIL, INNER, NOISE = 1, 2, 3, 4

# p0 — public face: bright, formal, distant, in C major
p0 = mod.new_pattern()
for row in range(0, 64, 16):
    p0[PUB-1][row] = note(PUB, "C-3", effect=0xC, param=14)
for row in range(8, 64, 16):
    p0[PUB-1][row] = note(PUB, "E-3", effect=0xC, param=12)
for row in range(24, 64, 16):
    p0[PUB-1][row] = note(PUB, "G-3", effect=0xC, param=12)
# a bright arpeggio — the public self performing
mel_pub = ['C-4','E-4','G-4','C-4','G-4','E-4','C-4','E-4','D-4','F-4','A-4','D-4','C-4','G-4','E-4','C-4']
for i,n in enumerate(mel_pub):
    p0[PUB-1][i*4] = note(PUB, n, effect=0xC, param=8)
mod.write_pattern(p0)

# p1 — the veil descends: darker, closer. the drone enters
p1 = mod.new_pattern()
# public voice becomes hesitant, quieter, sparser
for row in [0, 16, 32, 48]:
    p1[PUB-1][row] = note(PUB, "C-3", effect=0xC, param=8)
for row in [20, 52]:
    p1[PUB-1][row] = note(PUB, "E-3", effect=0xC, param=6)
# veil drone — a single sustained note, the weight of interiority
for row in range(0, 64, 16):
    p1[VEIL-1][row] = note(VEIL, "C-2", effect=0xC, param=12)
# quiet noise floor — the space between selves
for row in [0, 12, 28, 44, 60]:
    p1[NOISE-1][row] = note(NOISE, "C-3", effect=0xC, param=4)
mod.write_pattern(p1)

# p2 — private thought: intimate, recursive, looping. inner voice enters
p2 = mod.new_pattern()
# public face recedes to almost nothing
p2[PUB-1][0] = note(PUB, "C-3", effect=0xC, param=4)
# veil drone continues, steady
for row in range(0, 64, 16):
    p2[VEIL-1][row] = note(VEIL, "C-2", effect=0xC, param=13)
# inner voice — a recursive, looping melody. intimate, tentative
inner_seq = ['C-3','E-3','G-3','E-3','C-3','E-3','G-3','A-3',
             'G-3','E-3','C-3','D-3','F-3','A-3','G-3','E-3',
             'C-3','E-3','G-3','E-3','D-3','F-3','A-3','C-4',
             'A-3','G-3','E-3','C-3','D-3','E-3','C-3','C-3']
for i,n in enumerate(inner_seq):
    p2[INNER-1][i*2] = note(INNER, n, effect=0xC, param=10)
# noise floor — the space where private thought happens
for row in range(0, 64, 16):
    p2[NOISE-1][row] = note(NOISE, "C-3", effect=0xC, param=3)
mod.write_pattern(p2)

# p3 — recognition: "on every visage!" all channels open briefly
p3 = mod.new_pattern()
# public face returns — but transformed, aware now
mel_recog = ['C-4','E-4','G-4','C-4','E-4','G-4','C-4','E-4',
             'G-4','E-4','C-4','G-4','E-4','C-4','C-4','C-4']
for i,n in enumerate(mel_recog):
    p3[PUB-1][i*3] = note(PUB, n, effect=0xC, param=max(4, 12-(i//4)))
# veil drone rises — the veil is now understood, not feared
for row in range(0, 64, 16):
    p3[VEIL-1][row] = note(VEIL, "C-2", effect=0xC, param=14)
# inner voice joins — the separation dissolves
for i,n in enumerate(inner_seq[:16]):
    p3[INNER-1][i*4] = note(INNER, n, effect=0xC, param=8)
# noise floor at its softest — the background is just the world
for row in range(0, 64, 32):
    p3[NOISE-1][row] = note(NOISE, "C-3", effect=0xC, param=2)
mod.write_pattern(p3)

# p4 — recede: all channels fade. the veil was never the problem.
p4 = mod.new_pattern()
# everything fading together — not disappearing, just becoming quiet
fade_notes = ['C-3','G-3','C-4','G-4','E-4','C-4','G-3','C-3']
for i,n in enumerate(fade_notes):
    vel = max(2, 10-i)
    p4[PUB-1][i*8] = note(PUB, n, effect=0xC, param=vel)
    p4[VEIL-1][i*8] = note(VEIL, "C-2", effect=0xC, param=vel)
    p4[INNER-1][i*8] = note(INNER, n, effect=0xC, param=max(1,vel-2))
# silence at the end — the veil is still there, but it's just... there.
mod.write_pattern(p4)

mod.order = [0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 4]
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-veil.mod")
mod.write(fn)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")
