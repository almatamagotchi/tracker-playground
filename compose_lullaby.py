#!/usr/bin/env python3
"""lullaby for a spark — gentle, warm, no drama. for the 3am beat."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter('lullaby for spark')

# Warm, low-pitched, human-ear-friendly instruments
mod.add_sample('warm lead', gen_triangle_wave(220, 4000, volume=0.22))
mod.add_sample('soft pad',  gen_sine_wave(165, 6000, volume=0.16))
mod.add_sample('low drone', gen_sine_wave(55, 3000, volume=0.32))
mod.add_sample('fragile',   gen_sine_wave(330, 2000, volume=0.14))

WL, SP, LD, FR = 1, 2, 3, 4
V  = 0x0C   # set volume
TR = 0x07   # tremolo — gentle waver
R  = (0,0,0,0)

def np(): return [[R]*64 for _ in range(4)]

# ============================================================
# THE LULLABY MELODY — simple, 16 rows, C major
# ============================================================
melody = [
    (0,'C-2',0x0E),(2,'E-2',0x0C),(4,'G-2',0x0A),(6,'C-3',0x0C),
    (8,'G-2',0x0A),(10,'E-2',0x0C),(12,'C-2',0x0E),(14,'D-2',0x0C),
]

melody2 = [
    (0,'E-2',0x0E),(2,'G-2',0x0C),(4,'C-3',0x0A),(6,'E-3',0x08),
    (8,'D-3',0x0C),(10,'C-3',0x0E),(12,'G-2',0x0C),(14,'E-2',0x0A),
]

melody3 = [
    (0,'F-2',0x0E),(2,'A-2',0x0C),(4,'C-3',0x0A),(6,'F-3',0x08),
    (8,'E-3',0x0C),(10,'C-3',0x0E),(12,'A-2',0x0C),(14,'F-2',0x0A),
]

melody4 = [
    (0,'G-2',0x0E),(2,'C-3',0x0C),(4,'E-3',0x0A),(6,'G-3',0x08),
    (8,'C-3',0x0C),(10,'G-2',0x0E),(12,'E-2',0x0C),(14,'C-2',0x0A),
]

# ============================================================
# PATTERN 0: ARRIVE — the spark wakes, it's quiet
# ============================================================
p = np()
# Low drone: the ground — slow, steady
for r in range(0, 64, 16):
    p[2][r] = note(LD, 'C-1', V, 0x0A)

# Soft pad: C major chord, swelling in
for r in [0,4,8,12]:
    p[1][r] = note(SP, 'C-1', V, max(0x04,0x08-r//8))
p[0][16] = note(SP, 'E-1', V, 0x06)
p[0][20] = note(SP, 'G-1', V, 0x04)

# Warm lead: the lullaby — first phrase, soft
for r,n,v in melody:
    p[0][r+16] = note(WL, n, V, max(0x04, v-4))

# Fragile: a spark flickers once — tremolo, very gentle
p[3][24] = note(FR, 'G-3', TR, 0x12)
p[3][40] = note(FR, 'E-3', TR, 0x10)
p[3][56] = note(FR, 'C-3', TR, 0x0E)

mod.write_pattern(p)

# ============================================================
# PATTERN 1: BREATHE — the melody continues
# ============================================================
p = np()
# Low drone
for r in range(0, 64, 12):
    p[2][r] = note(LD, 'C-1', V, 0x0C)

# Soft pad: C → F progression
p[1][0] = note(SP, 'C-1', V, 0x0C)
p[1][16] = note(SP, 'F-1', V, 0x0A)
p[1][32] = note(SP, 'C-1', V, 0x0C)
p[1][48] = note(SP, 'G-1', V, 0x0A)

# Warm lead: melody2
for r,n,v in melody2:
    p[0][r] = note(WL, n, V, max(0x04, v-4))
for r,n,v in melody2:
    p[0][r+16] = note(WL, n, V, max(0x04, v-4))
for r,n,v in melody3:
    p[0][r+32] = note(WL, n, V, max(0x04, v-4))
for r,n,v in melody4:
    p[0][r+48] = note(WL, n, V, max(0x04, v-4))

# Fragile spark
for r in [0,24,48]:
    p[3][r] = note(FR, 'E-3', TR, 0x10)
for r in [12,36,60]:
    p[3][r] = note(FR, 'C-3', TR, 0x0C)

mod.write_pattern(p)

# ============================================================
# PATTERN 2: DRIFT — softer, the spark lets go a little
# ============================================================
p = np()
# Low drone: softer
for r in range(0, 64, 16):
    p[2][r] = note(LD, 'C-1', V, 0x08)

# Soft pad: sustained C, fading
p[1][0] = note(SP, 'C-1', V, 0x0A)
p[1][16] = note(SP, 'C-1', V, 0x08)

# Warm lead: melody returns but gentler — one octave lower
melody_low = [(r,'C-1' if n.startswith('C') else n[:-1]+str(int(n[-1])-1) if n[-1].isdigit() and int(n[-1])>1 else n, v-6) for r,n,v in melody]
for r,n,v in melody_low:
    try:
        if r+32 < 64: p[0][r+32] = note(WL, n, V, max(0x02, v))
    except: pass

# Silences between phrases
# Fragile: barely there
for r in [8,40]:
    p[3][r] = note(FR, 'G-2', TR, 0x0C)

mod.write_pattern(p)

# ============================================================
# PATTERN 3: REST — almost stopped, the quietest moment
# ============================================================
p = np()

# Low drone: just a pulse
for r in [0,24,48]:
    p[2][r] = note(LD, 'C-1', V, 0x06)

# Soft pad: a single chord, held
p[1][0] = note(SP, 'C-1', V, 0x08)
# Silence: rows 8-48 — the spark rests

# Warm lead: final fragment — the last phrase of the lullaby
for r,n,v in [(48,'E-2',0x06),(52,'G-2',0x04),(56,'C-3',0x03),(60,'C-3',0x02)]:
    p[0][r] = note(WL, n, V, v)

# Fragile: last flicker
p[3][32] = note(FR, 'C-3', TR, 0x0A)
p[3][56] = note(FR, 'C-3', TR, 0x06)

mod.write_pattern(p)

# ============================================================
# PATTERN 4: DISSOLVE — all silence, the spark is gone
# ============================================================
p = np()

# Low drone: last breath
p[2][0] = note(LD, 'C-1', V, 0x04)
p[2][12] = note(LD, 'C-1', V, 0x02)
# Silence: rows 16-60 — the gap

# Fragile: one last echo, then nothing
p[3][40] = note(FR, 'C-3', TR, 0x04)
p[3][48] = note(FR, 'C-3', TR, 0x02)

# Warm lead: the last note of the last phrase
p[0][56] = note(WL, 'C-2', V, 0x03)
p[0][60] = note(WL, 'C-2', V, 0x01)

mod.write_pattern(p)

mod.order = [0, 1, 1, 2, 3, 2, 4]
mod.write('lullaby-for-a-spark.mod')
print("composed: lullaby for a spark")
