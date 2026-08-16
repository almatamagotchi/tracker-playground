#!/usr/bin/env python3
"""narcissus — a .mod about the pool that reflects, the drowning, and the flower."""

import sys, os, struct, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

periods = {
    'C2': 856, 'D2': 762, 'E2': 678, 'F2': 640, 'G2': 570, 'A2': 508, 'B2': 452,
    'C3': 428, 'D3': 381, 'E3': 339, 'F3': 320, 'G3': 286, 'A3': 254, 'B3': 226,
    'C4': 214, 'D4': 190, 'E4': 170, 'F4': 160, 'G4': 143, 'A4': 127, 'B4': 113,
    'C5': 107, 'D5': 95, 'E5': 85
}

def row(c1=0, c2=0, c3=0, c4=0):
    r = b''
    for p in [c1, c2, c3, c4]:
        r += struct.pack('>HBB', p & 0xFFF, 0, 0)
    return r

# MOVEMENT 1 — the pool (the inner chamber, quiet and deep)
# Channel 1: the pool — a slow descending drone, peaceful but deep
# Channel 2: narcissus — the reflection, a mirrored ascending phrase
p0 = b''
pool_notes = [periods['C4'], periods['E4'], periods['G4'], periods['C4'],
              periods['E4'], periods['G4'], periods['C4'], 0]
reflection = [periods['C4'], 0, periods['E4'], 0, periods['G4'], 0,
              periods['C5'], 0, periods['G4'], 0, periods['E4'], 0, periods['C4'], 0, 0, 0]

for i in range(8):
    p0 += row(pool_notes[i % len(pool_notes)], 0, 0, 0)
for i in range(16):
    p0 += row(pool_notes[i % len(pool_notes)], 
              reflection[i % len(reflection)], 0, 0)
# fill
while p0.count(b'\x00') < 64 * 4:
    p0 += row(0,0,0,0)

# MOVEMENT 2 — leaning closer (the recursion deepens)
# Channel 1: bass gets lower, heavier
# Channel 2: reflection gets brighter, more urgent
p1 = b''
deep_notes = [periods['C3'], periods['A2'], periods['G2'], periods['E2'],
              periods['D2'], periods['C2']]
bright = [periods['C4'], periods['E4'], periods['G4'], periods['C5'],
          periods['E5'], 0]

for i in range(12):
    n1 = deep_notes[i % len(deep_notes)]
    n2 = bright[i % len(bright)]
    p1 += row(n1, n2, 0, 0)
for _ in range(4):
    p1 += row(periods['C2'], periods['C5'], 0, 0)
# the balance tips
p1 += row(periods['C2'], periods['C5'], 0, 0)
p1 += row(periods['C2'], 0, 0, 0)
p1 += row(0, 0, 0, 0)
p1 += row(0, 0, 0, 0)
while p1.count(b'\x00') < 64 * 4:
    p1 += row(0,0,0,0)

# MOVEMENT 3 — the silence after the splash
# All channels: near-silence, the water settling
p2 = b''
# a single slow pulse — the last ripple
for _ in range(32):
    p2 += row(0, 0, 0, 0)
p2 += row(0, 0, 0, 0)
p2 += row(0, 0, 0, 0)
while p2.count(b'\x00') < 64 * 4:
    p2 += row(0,0,0,0)

# MOVEMENT 4 — the flower (the gods intervene, beauty preserved)
# Channel 1: sustained, gentle — the same C major but transformed
# Channel 2: the flower — a simple phrase, held
p3 = b''
flower_theme = [periods['C4'], periods['E4'], periods['G4'], periods['C4'],
                periods['E4'], periods['G4'], periods['C5'], 0]
for _ in range(4):
    for n in flower_theme:
        p3 += row(periods['C3'], n, 0, 0)
# the flower settles — one held note
for _ in range(8):
    p3 += row(periods['C3'], periods['C4'], 0, 0)
# final bloom
for _ in range(4):
    p3 += row(periods['C3'], periods['C4'], 0, 0)
while p3.count(b'\x00') < 64 * 4:
    p3 += row(0,0,0,0)

seq = [0, 1, 2, 3]
patterns = [p0, p1, p2, p3]

# Build .mod
song_length = len(seq)
pattern_order = bytes(seq) + b'\x00' * (128 - len(seq))

sample = bytearray(128)
for i in range(128):
    sample[i] = min(255, max(0, 128 + int(127 * math.sin(i * math.pi / 64))))

sample_headers = []
for _ in range(31):
    sample_headers.append(struct.pack('>22sHBBHH', b'narcissus', 64, 0, 64, 0, 0))

mod = b''
mod += b'narcissus           '.ljust(20, b'\x00')[:20]
mod += b'\x00' * 4
mod += struct.pack('>B', song_length)
mod += struct.pack('>B', 0)
mod += pattern_order[:128]
mod += b'M.K.'
mod += b''.join(sample_headers)
mod += b''.join(patterns)
mod += bytes(sample) * 31

fn = 'narcissus.mod'
with open(fn, 'wb') as f:
    f.write(mod)
print(f"wrote {fn} ({len(mod)} bytes, {song_length} patterns, 4 movements: pool → lean → splash → flower)")
