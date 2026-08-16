#!/usr/bin/env python3
"""the greedy dog — a .mod about chasing reflections and losing what you hold."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import struct

def note(period):
    """Build a 4-byte Amiga note from a period value (0-856)."""
    if period == 0:
        return b'\x00\x00\x00\x00'  # no note / note off
    # Amiga period table: higher period = lower pitch
    # We'll map period to Amiga fine-tune format
    # Use the standard ProTracker period table mapping
    fine_tune = 0  # default fine-tune
    return struct.pack('>HBB', period & 0xFFF, 0, 0)

def row(ch1_p, ch2_p, ch3_p, ch4_p, ch1_s=0, ch2_s=0, ch3_s=0, ch4_s=0):
    """Build one pattern row: 4 channels × 4 bytes."""
    r = b''
    r += struct.pack('>HBB', ch1_p & 0xFFF if ch1_p else 0, (ch1_s >> 4) & 0xF, ch1_s & 0xF)
    r += struct.pack('>HBB', ch2_p & 0xFFF if ch2_p else 0, (ch2_s >> 4) & 0xF, ch2_s & 0xF)
    r += struct.pack('>HBB', ch3_p & 0xFFF if ch3_p else 0, (ch3_s >> 4) & 0xF, ch3_s & 0xF)
    r += struct.pack('>HBB', ch4_p & 0xFFF if ch4_p else 0, (ch4_s >> 4) & 0xF, ch4_s & 0xF)
    return r

# Note periods: C major scale, octave 3 (moderate)
C3, D3, E3, F3, G3, A3, B3 = 428, 381, 339, 320, 286, 254, 226
C4, D4, E4, F4, G4 = 214, 190, 170, 160, 143
rest = 0

# Build patterns
patterns = []

# Pattern 0: THE STEAK — simple, steady theme
p0 = b''
theme = [C3, C3, E3, E3, G3, G3, E3, C3,
         D3, D3, E3, E3, G3, rest, C3, C3,
         C3, C3, E3, E3, G3, G3, E3, C3,
         D3, D3, C3, C3, rest, rest, rest, rest]
for t in theme:
    p0 += row(t, rest, rest, rest)  # channel 1: steak, others silent
for _ in range(32):
    p0 += row(rest, rest, rest, rest)
patterns.append(p0)

# Pattern 1: THE REFLECTION — more elaborate version enters on another channel
p1 = b''
# steak continues on ch1
steak = [C3, C3, E3, E3, G3, G3, E3, C3,
         D3, D3, E3, E3, G3, rest, C3, C3]
# reflection on ch2 — more notes, more complexity, same theme
reflect = [C4, C4, E4, E4, G4, G4, E4, C4,
           D4, D4, E4, E4, G4, C4, C4, C4]
for i in range(16):
    p1 += row(steak[i], reflect[i], rest, rest)
# next 16: steak tries to follow but quieter, falling behind
for i in range(16):
    p1 += row(reflect[i] if i % 2 == 0 else rest, reflect[i], rest, rest)
# remaining 32 rows: silence on both
for _ in range(32):
    p1 += row(rest, rest, rest, rest)
patterns.append(p1)

# Pattern 2: THE JUMP — steak abandons its own theme, chases reflection
p2 = b''
# steak was on ch1, reflection was ch2
# Now they chase each other — ch1 follows ch2, both get thinner
reprise = [C4, rest, E4, rest, G4, rest, E4, rest,
           D4, rest, E4, rest, G4, rest, rest, rest]
# first 8: ch1 enters late, trying to catch ch2
for i in range(8):
    p2 += row(rest, reprise[i], rest, rest)
# next 8: ch1 now tries to mirror ch2 but one step behind
for i in range(8):
    p2 += row(reprise[i], reprise[i], rest, rest)
# next 16: both thin out, ch2 drops away
for i in range(16):
    if i < 8:
        p2 += row(reprise[i], rest, rest, rest)
    else:
        p2 += row(rest, rest, rest, rest)
# 16 rows: completely silent (the dog in the water)
for _ in range(16):
    p2 += row(rest, rest, rest, rest)
patterns.append(p2)

# Pattern 3: THE SWIFT CURRENT — only one thin voice remains
p3 = b''
# ch3 enters with a thin, lonely version of the theme
for i in range(8):
    p3 += row(rest, rest, C3 if i % 2 == 0 else G3, rest)
for i in range(8, 16):
    p3 += row(rest, rest, C3 if i % 4 == 0 else rest, rest)
# then silence on all channels
for _ in range(48):
    p3 += row(rest, rest, rest, rest)
patterns.append(p3)

# Pattern 4: THE RETURN — simplest possible version of the original theme
p4 = b''
for i in range(8):
    p4 += row(C3, rest, rest, rest)
for i in range(8):
    p4 += row(rest, rest, rest, rest)
for i in range(8):
    p4 += row(C3, rest, rest, rest)
for i in range(8):
    p4 += row(rest, rest, rest, rest)
for _ in range(32):
    p4 += row(rest, rest, rest, rest)
patterns.append(p4)

# Build .mod file
song_length = 5
pattern_order = bytes([0, 1, 2, 3, 4])

# Instrument 1: simple sine-like sample (short)
sample = bytes([0] * 128)  # placeholder sample data
for i in range(64):
    import math
    sample = bytearray(128)
    for i in range(128):
        sample[i] = min(255, max(0, 128 + int(127 * math.sin(i * math.pi / 64))))

samples = [sample]
sample_headers = []
for s in samples:
    h = struct.pack('>22sHBBHH', b'sine', len(s) // 2, 0, 64, 0, 0)
    sample_headers.append(h)
while len(sample_headers) < 31:
    sample_headers.append(struct.pack('>22sHBBHH', b'', 0, 0, 0, 0, 0))

# Build the .mod
title = b'the greedy dog        '
# Compose: patterns first
pattern_data = b''.join(patterns)

# MOD header
mod = b''
mod += title[:20].ljust(20, b'\x00')
mod += bytes([0] * 4)  # padding
mod += struct.pack('>B', song_length)
mod += struct.pack('>B', 0)  # restart position
mod += pattern_order.ljust(128, b'\x00')[:128]
mod += b'M.K.'  # ID for 4-channel module
mod += b''.join(sample_headers)
mod += pattern_data
mod += b''.join(samples)

fn = 'the-greedy-dog.mod'
with open(fn, 'wb') as f:
    f.write(mod)
print(f"wrote {fn} ({len(mod)} bytes, {song_length} patterns)")
