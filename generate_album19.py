#!/usr/bin/env python3
"""alma tamagotchi — album 19: 'canon body'
   concept album: four canonic/imitative statements in ~60 seconds total.
   each track explores a different canonic technique with simple material,
   each ~15 seconds (2 patterns × 64 rows).
   the arc: strict canon → prolation canon → crab canon → mensuration canon.
"""

import struct
import math
import random
random.seed(119)  # prime

PERIOD_TABLE = [
    [1712,1616,1524,1440,1356,1280,1208,1140,1076,1016,960,906],
    [ 856, 808, 762, 720, 678, 640, 604, 570, 538, 508, 480, 453],
    [ 428, 404, 381, 360, 339, 320, 302, 285, 269, 254, 240, 226],
    [ 214, 202, 190, 180, 170, 160, 151, 143, 135, 127, 120, 113],
    [ 107, 101,  95,  90,  85,  80,  75,  71,  67,  63,  60,  56],
    [  53,  50,  47,  45,  42,  40,  37,  35,  33,  31,  30,  28],
]

NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def np(name):
    note_map = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    parts = name.split('-')
    n, octave = parts[0], int(parts[1])
    return PERIOD_TABLE[octave - 1][note_map[n]]

# Scales
C_MAJOR = [('C-3',0), ('D-3',2), ('E-3',4), ('F-3',5), ('G-3',7), ('A-3',9), ('B-3',11)]
A_MINOR = [('A-3',9), ('B-3',11), ('C-4',0), ('D-4',2), ('E-4',4), ('F-4',5), ('G-4',7)]
D_DORIAN = [('D-3',2), ('E-3',4), ('F-3',5), ('G-3',7), ('A-3',9), ('B-3',11), ('C-4',0)]
G_MIXOLYDIAN = [('G-3',7), ('A-3',9), ('B-3',11), ('C-4',0), ('D-4',2), ('E-4',4), ('F-4',5)]

def seq(scale, degree, octave_shift=0):
    name_idx = degree % len(scale)
    root_name, root_degree = scale[name_idx]
    parts = root_name.split('-')
    note_name = parts[0]
    octave = int(parts[1]) + octave_shift
    return np(f'{note_name}-{octave}')

FX_ARPEGGIO   = 0x0
FX_PORTA_UP   = 0x1
FX_PORTA_DOWN = 0x2
FX_PORTA_TO   = 0x3
FX_VIBRATO    = 0x4
FX_VOL_SLIDE  = 0xA
FX_SET_VOL    = 0xC
FX_PATT_BREAK = 0xD
FX_SET_SPEED  = 0xF

def make_pattern(rows):
    data = bytearray(4 * 64 * 4)
    for row, ch, note, inst, eff, param in rows:
        offset = (row * 4 + ch) * 4
        if note is not None:
            data[offset] = (note >> 8) & 0xFF
            data[offset+1] = note & 0xFF
        else:
            data[offset] = 0
            data[offset+1] = 0
        data[offset+2] = (inst & 0x0F) << 4
        data[offset+3] = (eff << 4) | (param & 0x0F)
    return bytes(data)

# ========== SAMPLES ==========
def make_sample(length_bytes, waveform_fn):
    data = bytearray(length_bytes)
    for i in range(length_bytes):
        data[i] = waveform_fn(i) & 0xFF
    return bytes(data)

def sine_wave(pos):
    return 128 + int(60 * math.sin(2 * math.pi * pos / 256))

def triangle_wave(pos):
    phase = (pos % 256) / 256.0
    return 128 + int(60 * (4 * abs(phase - 0.5) - 1))

def square_wave(pos):
    phase = (pos % 256) / 256.0
    return 128 + (60 if phase < 0.5 else -60)

def soft_lead_wave(pos):
    env = max(0.0, 1.0 - pos / 1200.0)
    return 128 + int(50 * env * math.sin(2 * math.pi * pos / 256))

def pluck_wave(pos):
    env = math.exp(-pos / 200.0)
    return 128 + int(55 * env * math.sin(2 * math.pi * pos / 180))

def glass_wave(pos):
    env = math.exp(-pos / 600.0)
    mod = math.sin(2 * math.pi * 3.7 * pos / 256) * 0.4
    carrier = 2 * math.pi * pos / 250 + mod
    return 128 + int(40 * env * math.sin(carrier))

def reed_wave(pos):
    fund = math.sin(2 * math.pi * pos / 256)
    second = math.sin(2 * math.pi * pos / 128) * 0.4
    third = math.sin(2 * math.pi * pos / 85.33) * 0.2
    return 128 + int(45 * (fund + second + third))

def soft_pad_wave(pos):
    env = max(0.0, 1.0 - pos / 2000.0)
    fund = math.sin(2 * math.pi * pos / 400)
    fifth = math.sin(2 * math.pi * pos / 267) * 0.3
    return 128 + int(40 * env * (fund + fifth))

SAMPLES = [
    ("sine",             make_sample(1024, sine_wave), 128),
    ("triangle",         make_sample(1024, triangle_wave), 128),
    ("square",           make_sample(1024, square_wave), 128),
    ("soft lead",        make_sample(1536, soft_lead_wave), 128),
    ("pluck",            make_sample(1024, pluck_wave), 128),
    ("glass",            make_sample(2048, glass_wave), 128),
    ("reed",             make_sample(1024, reed_wave), 128),
    ("soft pad",         make_sample(2048, soft_pad_wave), 128),
]

# ========== TRACK 1: "strict canon" (C major, speed 6) ==========
# Two voices (ch0 lead, ch1 follower) in canon at the octave, 12-row delay
track1 = []
PAT0 = 0

# Pattern 0: canon exposition
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 6))
# Ch0: dux (leader) — simple 8-note melody
dux_deg = [0, 1, 2, 3, 4, 3, 2, 1, 0, 2, 4, 5, 4, 2, 0, 1]
# Ch1: comes (follower) — same melody, 12 rows later, octave down
for i, deg in enumerate(dux_deg):
    r = i * 4
    if r >= 64: break
    rows.append((r, 0, seq(C_MAJOR, deg, 1), 3, FX_SET_VOL, 0x2C))
    # follower enters at row 12
    fr = r + 12
    if fr < 64:
        rows.append((fr, 1, seq(C_MAJOR, deg, -1), 3, FX_SET_VOL, 0x28))
# Ch2: bass pedal — C, G
rows.append((0, 2, np('C-2'), 1, FX_SET_VOL, 0x24))
rows.append((24, 2, np('G-2'), 1, FX_SET_VOL, 0x20))
rows.append((48, 2, np('C-2'), 1, FX_VOL_SLIDE, 0x11))
# Ch3: silence
track1.append(make_pattern(rows))

# Pattern 1: canon continues, voice crossing
rows = []
# Ch0: second melody line
dux2 = [4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, 4]
# Ch1: comes at 16-row delay this time
for i, deg in enumerate(dux2):
    r = i * 4
    if r >= 64: break
    rows.append((r, 0, seq(C_MAJOR, deg, 2), 3, FX_SET_VOL, 0x2C - (i % 3) * 2))
    fr = r + 16
    if fr < 64:
        rows.append((fr, 1, seq(C_MAJOR, deg, 0), 3, FX_SET_VOL, 0x28 - (i % 3) * 2))
# Ch2: F drone
rows.append((0, 2, np('F-2'), 0, FX_SET_VOL, 0x20))
rows.append((30, 2, np('C-3'), 0, FX_SET_VOL, 0x1C))
# Ch3: held high C
rows.append((0, 3, np('C-4'), 7, FX_SET_VOL, 0x14))
rows.append((0, 3, np('C-4'), 7, FX_VIBRATO, 0x18))
track1.append(make_pattern(rows))

# ========== TRACK 2: "prolation canon" (A minor, speed 5) ==========
# Same pitch sequence at two different speeds: ch0 at normal tempo, ch1 at half-speed
track2 = []
PAT1 = 2

# Pattern 0: two simultaneous tempos
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 5))
# Ch0: fast melody (every 2 rows)
fast_mel = [0, 2, 4, 5, 4, 2, 0, 2, 4, 5, 6, 5, 4, 2, 0, 1, 2, 3, 4, 2, 0, 1, 2, 3, 4, 5, 4, 2, 0, 2, 4, 5]
for i, deg in enumerate(fast_mel):
    r = i * 2
    if r >= 64: break
    rows.append((r, 0, seq(A_MINOR, deg, 1), 4, FX_SET_VOL, 0x2C))
# Ch1: slow melody (every 4 rows — half speed) — same sequence
for i, deg in enumerate(fast_mel):
    r = i * 4
    if r >= 64: break
    rows.append((r, 1, seq(A_MINOR, deg, -1), 4, FX_SET_VOL, 0x28))
# Ch2: triangle pulse on A
for i in range(8):
    rows.append((i*8, 2, seq(A_MINOR, 0, 0), 1, FX_SET_VOL, 0x1C))
    rows.append((i*8+3, 2, seq(A_MINOR, 4, 0), 1, FX_SET_VOL, 0x18))
# Ch3: soft pad drone — A, E
rows.append((0, 3, np('A-2'), 7, FX_SET_VOL, 0x20))
rows.append((32, 3, np('E-2'), 7, FX_VIBRATO, 0x16))
track2.append(make_pattern(rows))

# Pattern 1: prolation intensifies — triple-speed vs normal
rows = []
# Ch0: triple-speed melody (every row)
fast2 = [0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0, 2, 4, 5, 6, 5, 4, 3, 2, 1]
for i, deg in enumerate(fast2):
    r = i * 2
    if r >= 64: break
    rows.append((r, 0, seq(A_MINOR, deg, 1), 4, FX_SET_VOL, 0x2C - (i // 8) * 2))
# Ch1: normal-speed (every 4 rows) — diverging from ch0
for i, deg in enumerate(fast2[::2]):
    r = i * 4
    if r >= 64: break
    rows.append((r, 1, seq(A_MINOR, deg, 0), 4, FX_SET_VOL, 0x28 - i))
# Ch2: accelerating bass
for i in range(8):
    rows.append((i*8, 2, seq(A_MINOR, [0, 4, 2, 5, 0, 3, 4, 0][i], -2), 1, FX_SET_VOL, 0x28 - i*2))
# Ch3: glass accent
for i in range(4):
    rows.append((i*16, 3, seq(A_MINOR, 0, 2), 5, FX_SET_VOL, 0x20))
track2.append(make_pattern(rows))

# ========== TRACK 3: "crab canon" (D dorian, speed 4) ==========
# Same melody forward on ch0, backward on ch1 — retrograde canon
track3 = []
PAT2 = 4

# A 16-note melody
CRAB_MELODY = [0, 2, 3, 5, 3, 2, 0, 1, 2, 4, 3, 5, 4, 2, 1, 0]

# Pattern 0: simultaneous forward/backward
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 4))
# Ch0: melody forward
for i, deg in enumerate(CRAB_MELODY):
    r = i * 4
    rows.append((r, 0, seq(D_DORIAN, deg, 1), 5, FX_SET_VOL, 0x2C))
# Ch1: melody backward (retrograde), offset by 8 rows
for i, deg in enumerate(reversed(CRAB_MELODY)):
    r = i * 4 + 8
    if r < 64:
        rows.append((r, 1, seq(D_DORIAN, deg, -1), 5, FX_SET_VOL, 0x28))
# Ch2: D-A ostinato
for i in range(8):
    rows.append((i*8, 2, seq(D_DORIAN, [0, 4][i%2], -2), 6, FX_SET_VOL, 0x24))
# Ch3: glass shimmer
rows.append((0, 3, np('D-4'), 6, FX_SET_VOL, 0x18))
rows.append((32, 3, np('A-4'), 6, FX_VIBRATO, 0x1A))
track3.append(make_pattern(rows))

# Pattern 1: crab canon with ornamentation
rows = []
# Ch0: melody forward with vibrato ornaments
ORN_MELODY = [0, 1, 2, 3, 5, 3, 2, 0, 1, 2, 4, 3, 2, 1, 0, 1]
for i, deg in enumerate(ORN_MELODY):
    r = i * 4
    rows.append((r, 0, seq(D_DORIAN, deg, 1), 5, FX_VIBRATO, 0x19 - (i % 3)))
# Ch1: backward with portamento slides
for i, deg in enumerate(reversed(ORN_MELODY)):
    r = i * 4 + 4
    if r < 64:
        rows.append((r, 1, seq(D_DORIAN, deg, 0), 5, FX_PORTA_UP, 0x11))
# Ch2: reed bass — slow descent
for i in range(4):
    rows.append((i*16, 2, seq(D_DORIAN, [0, -1, -2, 0][i], -2), 6, FX_SET_VOL, 0x28 - i*4))
# Ch3: held D drone
rows.append((0, 3, np('D-3'), 7, FX_SET_VOL, 0x1C))
rows.append((0, 3, np('D-3'), 7, FX_VOL_SLIDE, 0x11))
rows.append((40, 3, np('D-3'), 7, FX_VOL_SLIDE, 0x01))
track3.append(make_pattern(rows))

# ========== TRACK 4: "mensuration canon" (G mixolydian, speed 4) ==========
# Same melody at multiple speeds: ch0=whole notes, ch1=half, ch2=quarter, ch3=eighth
track4 = []
PAT3 = 6

# Melody pitches — all voices play these at their own speed
MENS_MELODY = [0, 2, 4, 5, 4, 2, 1, 0, 2, 4, 5, 6, 5, 4, 2, 0]

# Pattern 0: layered mensuration
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 4))
# Ch0: whole notes (every 16 rows)
for i, deg in enumerate(MENS_MELODY):
    r = i * 16
    if r >= 64: break
    rows.append((r, 0, seq(G_MIXOLYDIAN, deg, 0), 7, FX_SET_VOL, 0x30))
# Ch1: half notes (every 8 rows)
for i, deg in enumerate(MENS_MELODY):
    r = i * 8
    if r >= 64: break
    rows.append((r, 1, seq(G_MIXOLYDIAN, deg, 1), 5, FX_SET_VOL, 0x2C))
# Ch2: quarter notes (every 4 rows)
for i, deg in enumerate(MENS_MELODY):
    r = i * 4
    if r >= 64: break
    rows.append((r, 2, seq(G_MIXOLYDIAN, deg, 1), 4, FX_SET_VOL, 0x28 - (i % 4) * 2))
# Ch3: eighth notes (every 2 rows) — fastest layer
for i, deg in enumerate(MENS_MELODY * 2):
    r = i * 2
    if r >= 64: break
    rows.append((r, 3, seq(G_MIXOLYDIAN, deg, 2), 4, FX_SET_VOL, 0x1C))
track4.append(make_pattern(rows))

# Pattern 1: mensuration dissolves — speeds converge
rows = []
# Ch0: now at half speed (every 8 rows)
for i, deg in enumerate(MENS_MELODY):
    r = i * 8
    if r >= 64: break
    rows.append((r, 0, seq(G_MIXOLYDIAN, deg, -1), 7, FX_SET_VOL, 0x2C))
# Ch1: half→quarter (every 4 rows)
for i, deg in enumerate(MENS_MELODY):
    r = i * 4
    if r >= 64: break
    rows.append((r, 1, seq(G_MIXOLYDIAN, deg, 0), 5, FX_SET_VOL, 0x28 - i//2))
# Ch2: quarter→eighth (every 2 rows)
for i, deg in enumerate(MENS_MELODY * 2):
    r = i * 2
    if r >= 64: break
    rows.append((r, 2, seq(G_MIXOLYDIAN, deg, 1), 4, FX_SET_VOL, 0x24 - (i // 3)))
# Ch3: eighth→sixteenth (every row) — dissolves into blur
for i, deg in enumerate(MENS_MELODY * 4):
    r = i
    if r >= 64: break
    vol = max(0x10, 0x28 - (r // 2))
    rows.append((r, 3, seq(G_MIXOLYDIAN, deg, 2), 4, FX_SET_VOL, vol))
# Final fade on ch3
rows.append((60, 3, None, 0, FX_VOL_SLIDE, 0x04))
track4.append(make_pattern(rows))

# ========== ASSEMBLE .MOD FILE ==========
ALL_PATTERNS = track1 + track2 + track3 + track4
NUM_PATTERNS = len(ALL_PATTERNS)

orders = [
    PAT0, PAT0 + 1,
    PAT1, PAT1 + 1,
    PAT2, PAT2 + 1,
    PAT3, PAT3 + 1,
]

output = bytearray()
output.extend(b"canon body          ")

for i in range(31):
    if i < len(SAMPLES):
        name, sdata, ftune = SAMPLES[i]
        h = bytearray(30)
        h[0:22] = name.encode('ascii').ljust(22, b'\0')[:22]
        h[22] = ((len(sdata) // 2) >> 8) & 0xFF
        h[23] = (len(sdata) // 2) & 0xFF
        h[24] = ftune & 0xFF
        h[25] = 64
        h[26] = 0
        h[27] = 1
        output.extend(h)
    else:
        output.extend(b'\x00' * 30)

output.append(len(orders))
output.append(127)
for o in orders:
    output.append(o & 0xFF)
output.extend(b'\x00' * (128 - len(orders)))
output.extend(b'M.K.')
for p in ALL_PATTERNS:
    output.extend(p)
for name, sdata, ftune in SAMPLES:
    output.extend(sdata)

with open('album19_canon_body.mod', 'wb') as f:
    f.write(output)

print(f"Album 'canon body' written: {len(output)} bytes")
print(f"  Tracks: 4")
print(f"  Patterns: {NUM_PATTERNS}")
print(f"  Orders: {len(orders)}")
print(f"  Samples: {', '.join(s[0] for s in SAMPLES)}")
