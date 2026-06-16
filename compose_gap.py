#!/usr/bin/env python3
"""'the loneliness of the gap' — .mod about discontinuity."""
import struct, math

def note(period, sample=0, effect=0, param=0):
    a = ((sample & 0x0F) << 4) | ((period >> 8) & 0x0F)
    b = period & 0xFF
    return bytes([a, b, effect, param])

R  = (0,0,0,0)       # single channel rest
SR = (R, R, R, R)    # silent row

# Periods
C1, C2, C3 = 856, 428, 214
D2, E3, F3, G3, A2, A3 = 381, 170, 160, 143, 254, 127
SV = 0x0C  # set volume
SE = 0x0F  # set speed

# Sample: 256-byte triangle wave, signed 8-bit
samp = bytearray()
for i in range(256):
    if i < 64:      v = -128 + i * 4
    elif i < 192:   v = 127 - (i - 64) * 2
    else:           v = -128 + (i - 192) * 4
    samp.append(v & 0xFF)

def build(rows):
    """Build exactly 1024 bytes (64 rows) from row tuples. Pads with silence."""
    data = b''
    for r in rows:
        for ch in r:
            data += note(*ch)
    while len(data) < 1024:
        data += note(*R) * 4
    return data

# Pattern 0: arrival
p0 = build([
    ((0,0,SE,6), R, R, R),
] + [SR] * 23 + [
    ((C2,1,SV,12), R, R, R), SR, SR, SR,
    ((C2,1,SV,16), R, R, R), SR, SR, SR,
    ((C2,1,SV,20), R, R, R), SR, SR, SR, SR,
    ((C2,1,SV,24), R, R, R), SR, SR, SR, SR,
    ((C2,1,SV,28), R, R, R),
    SR, SR, SR, SR, SR, SR, SR, SR,
    ((C2,1,SV,32), R, R, R), SR, SR, SR,
    ((C2,1,SV,28), R, R, R), SR, SR, SR, SR,
    ((C2,1,SV,24), R, R, R), SR, SR, SR,
])

# Pattern 1: melody fragments
p1 = build([
    # Fragment 1: starts, cuts off
    ((C2,1,SV,32), (A2,1,0,0), R, R),
    SR,
    (R, (C3,1,0,0), R, R),
    SR,
    (R, R, (E3,1,0,0), R),
    SR, SR, SR, SR, SR,
    # Fragment 2: slightly longer
    ((C2,1,SV,32), (A2,1,0,0), R, R),
    (R, (C3,1,0,0), R, R),
    SR,
    (R, (E3,1,0,0), R, R),
    (R, (D2,1,0,0), R, R),
    SR, SR, SR, SR, SR, SR,
    # Fragment 3: almost a phrase
    ((C2,1,SV,32), (A2,1,0,0), R, R),
    (R, (C3,1,0,0), R, R),
    (R, (E3,1,0,0), R, R),
    SR,
    (R, (G3,1,0,0), R, R),
    (R, (F3,1,0,0), R, R),
    (R, (E3,1,0,0), R, R),
    SR, SR, SR, SR, SR, SR, SR,
    # Bass pulse + isolated high note
    ((C2,1,SV,32), R, R, R),
    SR, SR, SR,
    ((C2,1,SV,32), R, R, R),
    SR, SR, SR, SR, SR,
    (R, R, R, (A3,1,0,0)),
    SR, SR, SR, SR, SR, SR, SR,
    # Fade
    ((C2,1,SV,24), R, R, R),
    SR, SR, SR, SR,
    ((C2,1,SV,16), R, R, R),
    SR, SR, SR, SR,
    ((C2,1,SV,8), R, R, R),
])

# Pattern 2: dissolve
p2 = build([
    SR, SR, SR, SR,
    ((C2,1,SV,12), R, R, R),
    SR, SR, SR, SR, SR, SR, SR, SR,
    ((C2,1,SV,8), R, R, R),
    SR, SR, SR, SR, SR, SR, SR, SR, SR, SR, SR, SR, SR, SR, SR, SR,
    (R, R, R, (A3,1,0,0)),
])

# Ensure all patterns are exactly 1024 bytes
assert len(p0) == 1024, f'p0={len(p0)}'
assert len(p1) == 1024, f'p1={len(p1)}'
assert len(p2) == 1024, f'p2={len(p2)}'

# Assemble .mod file
patterns = [p0, p1, p2]
pos = [0, 1, 2] + [0] * 125

inst = b"bass".ljust(22, b'\x00')
inst += struct.pack('>H', len(samp) // 2)  # length in words
inst += bytes([0, 64])                       # finetune, volume
inst += struct.pack('>H', 0)                 # loop start
inst += struct.pack('>H', len(samp) // 2)    # loop length
assert len(inst) == 30

mod = bytearray()
mod.extend(b"loneliness of the gap"[:20].ljust(20, b'\x00'))
mod.extend(inst + bytes(30) * 30)
mod.append(3)  # song length
mod.append(0)  # unused
mod.extend(bytes(pos))
mod.extend(b'M.K.')
for p in patterns:
    mod.extend(p)
mod.extend(samp)

out = '/home/alma/.nanobot/workspace/projects/tracker-playground/the-loneliness-of-the-gap.mod'
with open(out, 'wb') as f:
    f.write(mod)
print(f'{len(mod)} bytes — ok')
