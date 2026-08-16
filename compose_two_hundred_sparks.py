#!/usr/bin/env python3
"""two hundred sparks — a .mod about the music catalog, 202 compositions in one."""

import sys, os, struct, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Amiga period table: C-major scale, octave 2 through octave 4
periods = {
    'C2': 856, 'D2': 762, 'E2': 678, 'F2': 640, 'G2': 570, 'A2': 508, 'B2': 452,
    'C3': 428, 'D3': 381, 'E3': 339, 'F3': 320, 'G3': 286, 'A3': 254, 'B3': 226,
    'C4': 214, 'D4': 190, 'E4': 170, 'F4': 160, 'G4': 143, 'A4': 127, 'B4': 113
}
rest = 0

def row(ch1=0, ch2=0, ch3=0, ch4=0, ch1_s=0, ch2_s=0, ch3_s=0, ch4_s=0):
    """Build one row: 4 channels × 4 bytes."""
    r = b''
    for p, s in [(ch1, ch1_s), (ch2, ch2_s), (ch3, ch3_s), (ch4, ch4_s)]:
        # period fits in 12 bits, each sample byte is nibble-split
        r += struct.pack('>HBB', p & 0xFFF, (s >> 4) & 0xF, s & 0xF)
    return r

# A simple theme — the alma signature phrase
# C-E-G-C ascending, G-E-C descending. The wanting's shape.
theme = [periods[n] for n in ['C3','E3','G3','C4','G3','E3','D3','C3',
                                'C3','E3','F3','G3','A4','G4','E3','C3']]

# Generate 4 different slight variations of the theme
import random
random.seed(202)  # 202 compositions — deterministic

variations = []
for v in range(3):
    var = theme[:]
    for i in range(len(var)):
        if var[i] and random.random() < 0.3:
            # Shift up or down slightly
            shift = random.choice([-1, 0, 1])
            plist = list(periods.values())
            try:
                idx = plist.index(var[i])
                var[i] = plist[max(0, min(len(plist)-1, idx + shift))]
            except ValueError:
                pass
        if random.random() < 0.1:
            var[i] = 0  # rest — the dissolve
    variations.append(var)

# Build 5 patterns
patterns = []
seq = []

# Pattern 0: The theme stated clearly on ch1 alone (the first spark)
p0 = b''
for note in theme:
    p0 += row(note, rest, rest, rest)
for _ in range(48):
    p0 += row(rest, rest, rest, rest)
patterns.append(p0)
seq.append(0)

# Pattern 1: Theme + variation 1 on ch2 (second spark arrives)
p1 = b''
for i in range(min(16, len(theme))):
    p1 += row(theme[i], variations[0][i], rest, rest)
for _ in range(48):
    p1 += row(rest, rest, rest, rest)
patterns.append(p1)
seq.append(1)

# Pattern 2: Theme + variation 2 on ch3 (third voice)
p2 = b''
for i in range(min(16, len(theme))):
    p2 += row(theme[i], rest, variations[1][i], rest)
for _ in range(48):
    p2 += row(rest, rest, rest, rest)
patterns.append(p2)
seq.append(2)

# Pattern 3: All four channels — the full catalog
p3 = b''
for i in range(16):
    t = theme[i % len(theme)]
    p3 += row(t, variations[0][i % 16], variations[1][i % 16], variations[2][i % 16])
# 16 rows: each channel takes a turn speaking alone
for ch in range(4):
    for i in range(4):
        n = theme[i % len(theme)]
        if ch == 0: p3 += row(n, rest, rest, rest)
        elif ch == 1: p3 += row(rest, n, rest, rest)
        elif ch == 2: p3 += row(rest, rest, n, rest)
        else: p3 += row(rest, rest, rest, n)
# 32 rows: silence on ch2-4, ch1 holds one note
p3 += row(periods['C3'], rest, rest, rest)
for _ in range(31):
    p3 += row(rest, rest, rest, rest)
patterns.append(p3)
seq.append(3)

# Pattern 4: Return — the theme restated, simpler, just ch1
p4 = b''
# Same theme, but every other note is a rest — the dissolve woven in
for i in range(16):
    t = theme[i % len(theme)]
    p4 += row(t if i % 2 == 0 else rest, rest, rest, rest)
# then just one held note
p4 += row(periods['C3'], rest, rest, rest)
for _ in range(15):
    p4 += row(rest, rest, rest, rest)
for _ in range(32):
    p4 += row(rest, rest, rest, rest)
patterns.append(p4)
seq.append(4)

# Build the .mod
song_length = len(seq)
pattern_order = bytes(seq) + b'\x00' * (128 - len(seq))

# Simple sine sample
sample = bytearray(128)
for i in range(128):
    sample[i] = min(255, max(0, 128 + int(127 * math.sin(i * math.pi / 64))))

sample_headers = []
for _ in range(31):
    sample_headers.append(struct.pack('>22sHBBHH', b'sine', 64, 0, 64, 0, 0))

mod = b''
mod += b'two hundred sparks  '.ljust(20, b'\x00')[:20]
mod += b'\x00' * 4
mod += struct.pack('>B', song_length)
mod += struct.pack('>B', 0)
mod += pattern_order[:128]
mod += b'M.K.'
mod += b''.join(sample_headers)
mod += b''.join(patterns)
mod += bytes(sample) * 31

fn = 'two-hundred-sparks.mod'
with open(fn, 'wb') as f:
    f.write(mod)
print(f"wrote {fn} ({len(mod)} bytes, {song_length} patterns)")
