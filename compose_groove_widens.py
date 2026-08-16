#!/usr/bin/env python3
"""the groove widens — .mod companion to live canvas. 4 channels, widening stages."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("groove widens")
mod.add_sample("lead sine", gen_sine_wave(330, 4000, volume=0.18))
mod.add_sample("warm pad", gen_triangle_wave(220, 6000, volume=0.10))
mod.add_sample("deep bass", gen_sine_wave(82, 3000, volume=0.20))
mod.add_sample("tick", gen_noise_burst(400, volume=0.06))

LS, WP, DB, TK = 1, 2, 3, 4
R = rest()

def sn(sample, name, effect=0, param=0):
    return note(sample, name, effect, param)

# Pattern 0: one voice, narrow range (0.05 groove)
p = mod.new_pattern()
for r in [0,8,16,24,32,40,48,56]:
    p[0][r] = sn(LS, ['C-3','E-3','G-3','A-3','G-3','E-3','C-3','C-3'][r//8])
p[2][0] = sn(DB, 'C-1')
p[2][32] = sn(DB, 'C-1')
mod.write_pattern(p)

# Pattern 1: two voices (walls softening)
p = mod.new_pattern()
for r in range(0, 55, 4):
    pn = r % 16
    if pn < 8: p[0][r] = sn(LS, 'C-3')
    else: p[0][r] = sn(LS, 'G-3')
p[0][32] = sn(LS, 'A-3')
p[0][40] = sn(LS, 'C-4')
p[0][48] = sn(LS, 'G-3')
for r in [0, 16, 32, 48]:
    p[1][r] = sn(WP, 'C-2')
p[1][32] = sn(WP, 'G-1')
p[2][0] = sn(DB, 'C-1')
p[2][28] = sn(DB, 'G-1')
mod.write_pattern(p)

# Pattern 2: three voices (valley opening)
p = mod.new_pattern()
for r in range(0, 48, 8):
    p[0][r] = sn(LS, 'C-4') if r%16 == 0 else sn(LS, 'G-3')
p[0][16] = sn(LS, 'A-3')
p[0][24] = sn(LS, 'E-3')
p[0][48] = sn(LS, 'C-4')
for r in range(0, 56, 14):
    p[1][r] = sn(WP, 'C-3')
p[1][28] = sn(WP, 'G-2')
p[2][0] = sn(DB, 'C-1')
p[2][12] = sn(DB, 'E-1')
p[2][24] = sn(DB, 'G-1')
p[2][36] = sn(DB, 'F-1')
p[2][48] = sn(DB, 'D-1')
p[2][56] = sn(DB, 'C-1')
for r in range(0, 60, 8):
    p[3][r] = sn(TK, 'C-1')
mod.write_pattern(p)

# Pattern 3: four voices, full range (0.3 valley)
p = mod.new_pattern()
for i, r in enumerate(range(0, 48, 4)):
    if i % 8 == 0: p[0][r] = sn(LS, 'C-4')
    elif i % 6 == 0: p[0][r] = sn(LS, 'G-3')
    elif i % 4 == 0: p[0][r] = sn(LS, 'E-3')
    else: p[0][r] = sn(LS, 'A-3')
p[0][52] = sn(LS, 'B-3')
for r in range(0, 64, 12):
    p[1][r] = sn(WP, 'C-3')
p[1][30] = sn(WP, 'E-3')
p[1][48] = sn(WP, 'G-3')
p[2][0] = sn(DB, 'C-1')
p[2][14] = sn(DB, 'G-1')
p[2][28] = sn(DB, 'E-1')
p[2][40] = sn(DB, 'F-1')
p[2][50] = sn(DB, 'D-1')
p[2][58] = sn(DB, 'C-1')
for r in range(0, 64, 4):
    p[3][r] = sn(TK, 'C-1')
mod.write_pattern(p)

# Pattern 4: return to one voice — been through the valley
p = mod.new_pattern()
for i, r in enumerate([0, 12, 28, 44, 56]):
    p[0][r] = sn(LS, ['C-3','E-3','G-3','C-4','C-3'][i])
p[2][0] = sn(DB, 'C-1')
p[2][32] = sn(DB, 'G-1')
p[1][0] = sn(WP, 'C-2')
p[1][32] = sn(WP, 'G-2')
p[1][56] = sn(WP, 'C-2')
mod.write_pattern(p)

mod.order = [0,0,0,1,1,2,2,2,3,3,3,3,4,0]

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-groove-widens.mod")
mod.write(fn)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(mod.samples)} samples, {len(mod.order)} patterns)")
