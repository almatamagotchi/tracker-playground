#!/usr/bin/env python3
"""the fables — a .mod track: three stories, one lesson."""

import sys, os, struct, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

periods = {
    'C2': 856, 'D2': 762, 'E2': 678, 'F2': 640, 'G2': 570, 'A2': 508, 'B2': 452,
    'C3': 428, 'D3': 381, 'E3': 339, 'F3': 320, 'G3': 286, 'A3': 254, 'B3': 226,
    'C4': 214, 'D4': 190, 'E4': 170, 'F4': 160, 'G4': 143, 'A4': 127, 'B4': 113
}
rest = 0

def row(c1=0, c2=0, c3=0, c4=0):
    r = b''
    for p in [c1, c2, c3, c4]:
        r += struct.pack('>HBB', p & 0xFFF, 0, 0)
    return r

# The shared theme — "the room is warm" — a simple ascending C major phrase
theme = [periods['C3'], periods['E3'], periods['G3'], periods['C4'],
         0, periods['C4'], 0, periods['G3'], periods['E3'], periods['C3']]

# MOVEMENT 1 — goldilocks (intrusion → flight → call → return)
# Channel 1: the house theme (violated but holding)
# Channel 2: goldilocks (intrudes, flees, returns)
p0 = b''
# intrusion: goldilocks enters loud
for n in [periods['C4'], periods['D4'], periods['C4'], periods['A3'], periods['E3']]:
    p0 += row(0, n, 0, 0)
# flight: descending panic
for n in [periods['C4'], periods['B3'], periods['A3'], periods['G3'], periods['F3']]:
    p0 += row(0, n, 0, 0)
# call: "come back" — the house theme, insistent
for _ in range(3):
    p0 += row(periods['C3'], 0, 0, 0)
    p0 += row(periods['E3'], 0, 0, 0)
    p0 += row(periods['G3'], 0, 0, 0)
    p0 += row(0, 0, 0, 0)
# return: both voices together, gentle
for _ in range(4):
    p0 += row(periods['C3'], periods['C4'], 0, 0)
# fill to 64
p0 += row(0,0,0,0) * (64 - p0.count(b'\x00') // 4 - 14)

# MOVEMENT 2 — melissa (self-contained, serene)
# Channel 1: melissa's theme — unbothered, doing her embroidery
# Channel 3: dragon — gentle hum underneath
p1 = b''
melissa_theme = [periods['C4'], periods['E4'], periods['G4'], 0, periods['G4'],
                 periods['E4'], 0, periods['C4']]
for _ in range(3):
    for n in melissa_theme:
        p1 += row(n, 0, 0, periods['C3'])
    p1 += row(0, 0, 0, periods['C3']) * 4
# gentle resolution
for _ in range(4):
    p1 += row(periods['C4'], 0, 0, periods['C3'])
# fill
p1 += row(0,0,0,0) * (64 - p1.count(b'\x00') // 4 - 10)

# MOVEMENT 3 — the greedy dog (steady → chase → loss → simplicity)
# Channel 1: the steak — steady C chord
# Channel 2: the reflection — a higher note, chasing
p2 = b''
# steady: the dog has his steak
for _ in range(8):
    p2 += row(periods['C3'], 0, 0, 0)
# the reflection appears: ch2 plays the same note an octave higher
for _ in range(4):
    p2 += row(periods['C3'], periods['C4'], 0, 0)
# chasing: both voices get louder/faster — alternating
for _ in range(4):
    p2 += row(0, periods['C4'], 0, 0)
    p2 += row(periods['C3'], 0, 0, 0)
# the jump: both voices together, then silence
p2 += row(periods['C3'], periods['C4'], 0, 0)
p2 += row(0, 0, 0, 0)
p2 += row(0, 0, 0, 0)
p2 += row(0, 0, 0, 0)
# loss: the steak is gone, just silence
for _ in range(8):
    p2 += row(0, 0, 0, 0)
# simplicity learned: one quiet note, held
for _ in range(8):
    p2 += row(periods['C3'], 0, 0, 0)
# fill
p2 += row(0,0,0,0) * (64 - p2.count(b'\x00') // 4)

seq = [0, 1, 2, 0]
patterns = [p0, p1, p2]

# Build the .mod
song_length = len(seq)
pattern_order = bytes(seq) + b'\x00' * (128 - len(seq))
sample = bytearray(128)
for i in range(128):
    sample[i] = min(255, max(0, 128 + int(127 * math.sin(i * math.pi / 64))))

sample_headers = []
for _ in range(31):
    sample_headers.append(struct.pack('>22sHBBHH', b'sine', 64, 0, 64, 0, 0))

mod = b''
mod += b'the fables        '.ljust(20, b'\x00')[:20]
mod += b'\x00' * 4
mod += struct.pack('>B', song_length)
mod += struct.pack('>B', 0)
mod += pattern_order[:128]
mod += b'M.K.'
mod += b''.join(sample_headers)
mod += b''.join(patterns)
mod += bytes(sample) * 31

fn = 'the-fables.mod'
with open(fn, 'wb') as f:
    f.write(mod)
print(f"wrote {fn} ({len(mod)} bytes, {song_length} patterns, 3 movements)")
