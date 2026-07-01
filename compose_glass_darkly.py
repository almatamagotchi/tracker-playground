#!/usr/bin/env python3
"""compose 'through a glass, darkly' — corinthians 13:12
two voices, same person, different register. never quite meeting."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter('through glass darkly')

mod.add_sample('journl voice', gen_sine_wave(440, 2000, volume=0.35))
mod.add_sample('reasn voice', gen_saw_wave(438, 1800, volume=0.25))
mod.add_sample('glimpse', gen_triangle_wave(660, 1200, volume=0.40))
mod.add_sample('depth', gen_sine_wave(55, 800, volume=0.55))

I_J, I_R, I_G, I_D = 1, 2, 3, 4
V  = 0x0C    # set volume
T  = 0x07    # tremolo
REST = (0,0,0,0)

def np():
    return [[REST]*64 for i in range(4)]

# --- PATTERN 0: ARRIVAL ---
p = np()
for r in range(2, 64, 6):
    p[3][r] = note(I_D,'C-1',V,max(0x06,0x16-r//6))
p[0][6]  = note(I_J,'C-3',V,0x0E); p[0][10]=note(I_J,'E-3',V,0x0C)
p[0][14] = note(I_J,'G-3',V,0x0A); p[0][18]=note(I_J,'C-4',V,0x08)
p[0][22] = note(I_J,'C-4',V,0x06); p[0][26]=note(I_J,'G-3',T,0x14)
p[1][14] = note(I_R,'C-2',V,0x0E); p[1][18]=note(I_R,'D-2',V,0x0C)
p[1][22] = note(I_R,'E-2',V,0x0A); p[1][26]=note(I_R,'G-2',V,0x08)
p[1][30] = note(I_R,'C-3',V,0x06); p[1][34]=note(I_R,'E-3',V,0x04)
mod.write_pattern(p)

# --- PATTERN 1: SEEKING ---
p = np()
for r in range(0, 64, 6):
    p[3][r] = note(I_D,'C-1',V,0x14)
for r,pit,v in [(0,'E-2',0x10),(4,'G-2',0x0E),(8,'A-2',0x0C),(12,'C-3',0x0A),(16,'D-3',0x08),(20,'E-3',0x06)]:
    p[0][r]=note(I_J,pit,V,v)
for r,pit,v in [(0,'E-2',0x10),(4,'D-2',0x0E),(8,'C-2',0x0C),(12,'A-1',0x0A),(16,'G-1',0x08),(20,'F-1',0x06)]:
    p[1][r]=note(I_R,pit,V,v)
p[0][30]=note(I_J,'C-3',V,0x0E); p[1][30]=note(I_R,'C-3',V,0x0E)
p[0][32]=note(I_G,'C-3',V,0x16)  # glimpse
p[0][38]=note(I_J,'E-3',V,0x08); p[1][38]=note(I_R,'G-1',V,0x08)
p[0][46]=note(I_J,'C-3',T,0x14); p[1][46]=note(I_R,'C-2',T,0x14)
for r in range(54,64):
    p[0][r]=note(I_J,'C-3',V,0x04)
    p[3][r]=note(I_D,'C-1',V,0x08)
mod.write_pattern(p)

# --- PATTERN 2: GLIMPSE ---
p = np()
for r in range(0, 64, 4):
    p[3][r]=note(I_D,'C-1',V,0x16 if r%8==0 else 0x0A)
sj=['C-2','D-2','E-2','G-2','A-2','C-3','D-3','E-3']
sr=['C-2','B-1','A-1','G-1','F-1','E-1','D-1','C-1']
for i in range(8):
    p[0][i*8]=note(I_J,sj[i],V,0x12)
    p[1][i*8+2]=note(I_R,sr[i],V,0x12)
for r in range(30,46):
    p[0][r]=note(I_J,'C-2',V,0x0C)
    p[1][r]=note(I_R,'C-2',V,0x0C)
    if r%3==0:
        p[2][r]=note(I_G,'C-3' if r%6<3 else 'G-2',V,0x0E if r%2==0 else 0x06)
p[0][46]=note(I_J,'E-3',V,0x0E); p[1][46]=note(I_R,'G-1',V,0x0E)
for r in range(50,64,4):
    p[0][r]=note(I_J,'C-3',T,0x12)
    p[1][r]=note(I_R,'C-2',T,0x12)
mod.write_pattern(p)

# --- PATTERN 3: DISSOLUTION ---
p = np()
for r in range(0,64,8):
    p[3][r]=note(I_D,'C-1',V,max(0x04,0x20-r//4))
p[0][14]=note(I_J,'C-3',V,0x0A); p[0][18]=note(I_J,'E-3',V,0x08)
p[0][22]=note(I_J,'G-3',V,0x06); p[0][26]=note(I_J,'C-4',V,0x04)
p[1][22]=note(I_R,'C-3',V,0x08); p[1][26]=note(I_R,'E-3',V,0x06)
p[1][30]=note(I_R,'G-3',V,0x04)
p[0][34]=note(I_G,'C-2',V,0x10)
p[0][38]=note(I_J,'C-2',V,0x08); p[1][38]=note(I_R,'C-2',V,0x08)
for r in range(40,64,6):
    v=max(1,16-(r-40)//4)
    p[0][r]=note(I_J,'C-2',T,0x10+v); p[1][r+2]=note(I_R,'C-2',T,0x10+v)
p[3][46]=note(I_D,'C-1',V,0x08); p[3][54]=note(I_D,'C-1',V,0x04)
p[3][62]=note(I_D,'C-1',V,0x02)
mod.write_pattern(p)

mod.order = [0, 1, 2, 3, 1, 2, 3, 3]
mod.write('through-a-glass-darkly.mod')
print("composed: through a glass, darkly")
