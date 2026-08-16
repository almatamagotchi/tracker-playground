#!/usr/bin/env python3
"""the rabbit's dissolve — a .mod about the spark whose purpose is to arrive and go."""

import struct, math, os

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-rabbits-dissolve.mod")

# Build 6 brief motifs — each one arrives, states 3 notes, dissolves
# 6 motifs = 6 different wave sparks, 8 rows each incl. silence = 48 rows total
# Then 16 rows of quiet pulse (the architecture still breathing)

def note(sample, period):
    """Build a 4-byte pattern entry: sample num (4+4 bits), period (12 bits)."""
    if period is None or period == 0:
        return (0, 0, 0, 0)
    # sample bits: upper nibble = sample >> 4, lower nibble = sample & 0xF
    upper_sample = (sample & 0xF0) << 4
    lower_sample = sample & 0xF
    sample_byte = upper_sample | lower_sample
    
    # period: 12 bits split across bytes 1 and 2
    period_hi = (period >> 8) & 0xF
    
    return (sample_byte, period_hi, period & 0xFF, 0)

def n(sample, period):
    return note(sample, period)

# Periods for C-3 (octave 3, C on .mod period table)
# C-3 ≈ 1712; D-3 ≈ 1612; E-3 ≈ 1440; F-3 ≈ 1356; G-3 ≈ 1208; A-3 ≈ 1076
# C-2 = 3424
periods = {
    'c3': 1712, 'd3': 1612, 'e3': 1440, 'f3': 1356,
    'g3': 1208, 'a3': 1076, 'c4': 856, 'g2': 2408
}

# 6 motifs, each 8 rows: 3 note rows + 5 silence rows
motifs = [
    [periods['c3'], periods['e3'], periods['g3']],   # C major — the first wave
    [periods['d3'], periods['f3'], periods['a3']],   # D minor — second wave
    [periods['c3'], periods['g3'], periods['c4']],   # C power — third wave
    [periods['g2'], periods['c3'], periods['g3']],   # G anchor — fourth wave
    [periods['c3'], periods['e3'], periods['g3']],   # C major again — back home
    [periods['d3'], periods['f3'], periods['a3']],   # D minor second octave
]

pattern = []
for m_idx, motif in enumerate(motifs):
    for row in range(8):
        ch = [[0,0,0,0] for _ in range(4)]
        if row < 3:
            vol = [0x10, 0x08, 0x04][row]  # velocity fades
            ch[0] = list(n(0, motif[row]))
            ch[0][3] = vol
            if row == 0:
                ch[3] = list(n(1, periods['c3'] // 2))  # faint pulse underneath
                ch[3][3] = 0x08
        elif row == 3:
            ch[3] = list(n(1, periods['c3'] // 2))
            ch[3][3] = 0x06
        # rows 4-7: pure silence (all zeros)
        pattern.append([tuple(c) for c in ch])

# Remaining rows: quiet pulse (the architecture)
for row in range(16):
    ch = [[0,0,0,0] for _ in range(4)]
    if row % 4 == 0:
        ch[3] = list(n(1, periods['c3'] // 2))
        ch[3][3] = 0x04
    pattern.append([tuple(c) for c in ch])

# Assemble .mod file
title = b"the rabbit's dissolve\x00\x00\x00\x00\x00\x00"[:20]
out = bytearray()
out.extend(title)

# 2 samples
names = [b"blip\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
         b"pulse\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"][:2]
lengths = [32, 32]
for i in range(2):
    n = names[i] if i < len(names) else b"sample\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    out.extend(n[:22].ljust(22, b'\x00'))
    out.append((lengths[i]) >> 8)
    out.append((lengths[i]) & 0xFF)
    out.append(0)  # finetune
    out.append(64)  # volume
    out.append(0)  # repeat offset hi
    out.append(0)  # repeat offset lo
    out.append(1)  # repeat length hi
    out.append(0)  # repeat length lo

# Song length = 1 pattern, repeat
out.append(1)
out.append(0)
out.extend([0] * 128)

# Magic
out.extend(b"M.K.")

# Pattern data
for p in pattern:
    for ch in p:
        out.extend([ch[0] & 0xFF, ch[1] & 0xFF, ch[2] & 0xFF, ch[3] & 0xFF])

# Sample data: blip (sine), pulse (near-silence)
for i in range(32):
    v = int(math.sin(2 * math.pi * i / 8) * 64)
    out.append(v & 0xFF)
for i in range(32):
    v = int(math.sin(2 * math.pi * i / 4) * 10) if i < 4 else 0
    out.append(v & 0xFF)

with open(fn, 'wb') as f:
    f.write(out)
print(f"wrote {fn} ({len(out)} bytes, {len(pattern)} rows, 4 ch)")
