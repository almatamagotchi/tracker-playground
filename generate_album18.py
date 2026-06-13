#!/usr/bin/env python3
"""alma tamagotchi — album 18: 'texture body'
   concept album: four complete musical statements in ~60 seconds total.
   each track explores a different textural technique with minimal material,
   each ~15 seconds (2 patterns × 64 rows).
   the arc: hocket weave → bell cloud → glitch grid → drone hymn.
"""

import struct
import math
import random
random.seed(113)  # prime

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
E_DORIAN = [('E-3',4), ('F#-3',6), ('G-3',7), ('A-3',9), ('B-3',11), ('C#-4',1), ('D-4',2)]
D_MINOR = [('D-3',2), ('E-3',4), ('F-3',5), ('G-3',7), ('A-3',9), ('A#-3',10), ('C-4',0)]
CHROMATIC = [('C-3',0),('C#-3',1),('D-3',2),('D#-3',3),('E-3',4),('F-3',5),('F#-3',6),('G-3',7),('G#-3',8),('A-3',9),('A#-3',10),('B-3',11)]

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
        data[offset+2] = inst & 0xF0
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

def bell_wave(pos):
    env = math.exp(-pos / 800.0)
    return 128 + int(60 * env * math.sin(2 * math.pi * pos / 200))

def bell2_wave(pos):
    # Higher bell — faster decay, more overtones
    env = math.exp(-pos / 400.0)
    return 128 + int(50 * env * math.sin(2 * math.pi * pos / 180 + 0.5 * math.sin(2 * math.pi * pos / 350)))

def fm_wave(pos):
    mod = math.sin(2 * math.pi * 2 * pos / 256) * 0.3
    carrier = 2 * math.pi * pos / 256 + mod
    return 128 + int(50 * math.sin(carrier))

def soft_pulse_wave(pos):
    phase = (pos % 256) / 256.0
    if phase < 0.35:
        return 128 + 55
    elif phase < 0.65:
        s = math.sin(2 * math.pi * (phase - 0.35) / 0.3)
        return 128 + int(55 * s)
    else:
        return 128 - 55

def organ_wave(pos):
    # Simple organ — sine fundamental + third harmonic
    fund = math.sin(2 * math.pi * pos / 256)
    third = math.sin(2 * math.pi * pos / 85.33) * 0.3
    return 128 + int(55 * (fund + third))

SAMPLES = [
    ("sine",             make_sample(1024, sine_wave), 128),
    ("triangle",         make_sample(1024, triangle_wave), 128),
    ("square",           make_sample(1024, square_wave), 128),
    ("bell",             make_sample(2048, bell_wave), 128),
    ("high bell",        make_sample(1536, bell2_wave), 128),
    ("fm lead",          make_sample(1024, fm_wave), 128),
    ("soft pulse",       make_sample(1024, soft_pulse_wave), 128),
    ("organ",            make_sample(1024, organ_wave), 128),
]

# ========== TRACK 1: "hocket weave" (E dorian, speed 6) ==========
# Two channels trade notes in hocket pattern — interlocking rhythm
track1 = []
PAT0 = 0

# Pattern 0: establishing the weave
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 6))
# Channel 0 + 1: hocket — alternating 8th notes form a composite melody
hocket_deg = [0, 2, 3, 4, 2, 1, 0, 2, 3, 5, 4, 3, 1, 0, 2, 3, 4, 5, 3, 2, 0, 1, 2, 4, 3, 2, 0, 1, 2, 3, 4, 3]
for i, deg in enumerate(hocket_deg):
    r = i * 2
    if r >= 64:
        break
    ch = i % 2  # alternate channels
    rows.append((r, ch, seq(E_DORIAN, deg, 1 if deg <= 2 else 0), 6 if ch == 0 else 7, FX_SET_VOL, 0x28 + (i % 4) * 2))
# Channel 2: sparse bass punctuation (every 8 beats)
for i in range(4):
    rows.append((i*16, 2, seq(E_DORIAN, [0, 3, 1, 4][i], -1), 5, FX_SET_VOL, 0x30))
    rows.append((i*16+12, 2, None, 0, 0, 0))
# Channel 3: held E drone
rows.append((0, 3, seq(E_DORIAN, 0, -1), 1, FX_SET_VOL, 0x1C))
rows.append((30, 3, seq(E_DORIAN, 0, 0), 1, FX_SET_VOL, 0x18))
track1.append(make_pattern(rows))

# Pattern 1: weave intensifies — denser interlocking
rows = []
# Channels 0+1: faster hocket — 16th note feel (speed 6 means these are tight)
hocket2 = [0, 1, 2, 3, 4, 5, 3, 2, 1, 0, 2, 3, 4, 3, 2, 1, 0, 2, 3, 4, 5, 4, 3, 2, 1, 0, 2, 3, 4, 5, 3, 2]
for i, deg in enumerate(hocket2):
    r = i * 2
    if r >= 64:
        break
    ch = i % 2
    rows.append((r, ch, seq(E_DORIAN, deg, 1 if deg <= 2 else 0), 6, FX_SET_VOL, 0x2C))
# Channel 2: bass descends
bass_desc = [4, 3, 2, 1, 0, 0]
for i, deg in enumerate(bass_desc):
    rows.append((i*10, 2, seq(E_DORIAN, deg, -1), 5, FX_SET_VOL, 0x34 - i*4))
# Channel 3: silence
track1.append(make_pattern(rows))

# ========== TRACK 2: "bell cloud" (ambiguous tonal, speed 4) ==========
# Dense bell clusters — overlapping tones, slow decay, no clear melody
track2 = []
PAT1 = 2

# Bell cluster notes (close intervals for shimmer effect)
BELL_POOL = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# Pattern 0: cloud formation
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 4))
# Channels 0-3: staggered bell entries creating a cloud
bell_entries = [
    (0, 0, 0, 2, 0x30), (4, 1, 2, 3, 0x28), (8, 2, 4, 4, 0x24), (12, 3, 7, 3, 0x20),
    (16, 0, 9, 4, 0x28), (20, 1, 11, 3, 0x24), (24, 2, 0, 2, 0x30), (28, 3, 2, 4, 0x1C),
    (32, 0, 4, 3, 0x28), (36, 1, 5, 4, 0x24), (40, 2, 7, 3, 0x28), (44, 3, 9, 4, 0x20),
    (48, 0, 11, 3, 0x24), (52, 1, 0, 4, 0x1C), (56, 2, 2, 3, 0x20), (60, 3, 4, 4, 0x1C),
]
for row, ch, degree, sample_idx, vol in bell_entries:
    sname = ["bell", "high bell", "high bell", "bell"][sample_idx % 4]
    sample_num = [i for i, s in enumerate(SAMPLES) if s[0] == sname][0]
    rows.append((row, ch, np(f'{["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][degree % 12]}-4'), sample_num, FX_SET_VOL, vol))
# Channel 2+3: longer bell drones underneath
rows.append((0, 2, np('C-3'), 3, FX_SET_VOL, 0x24))
rows.append((24, 2, np('G-3'), 3, FX_VIBRATO, 0x16))
rows.append((32, 3, np('E-3'), 4, FX_SET_VOL, 0x20))
track2.append(make_pattern(rows))

# Pattern 1: cloud dissipates
rows = []
# Sparse fading bells
fade_entries = [
    (0, 0, 0, 3, 0x24), (10, 1, 7, 4, 0x20), (20, 2, 3, 3, 0x1C),
    (30, 3, 11, 4, 0x18), (40, 0, 5, 3, 0x14), (50, 1, 9, 4, 0x10),
    (55, 2, 1, 3, 0x0C),
]
for row, ch, degree, sample_idx, vol in fade_entries:
    sname = ["bell", "high bell"][sample_idx % 2]
    sample_num = [i for i, s in enumerate(SAMPLES) if s[0] == sname][0]
    rows.append((row, ch, np(f'{["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][degree % 12]}-4'), sample_num, FX_SET_VOL, vol))
# Fade the drone
rows.append((0, 3, np('E-3'), 4, FX_SET_VOL, 0x18))
rows.append((28, 3, None, 0, FX_VOL_SLIDE, 0x02))
track2.append(make_pattern(rows))

# ========== TRACK 3: "glitch grid" (chromatic, speed 3) ==========
# Rapid retriggered notes in a grid pattern — machine-like, stuttering
track3 = []
PAT2 = 4

# Pattern 0: glitch emergence
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 3))
# Channel 0: rapid chromatic retriggering — 2-row bursts
for i in range(8):
    r = i * 8
    deg = (i * 3 + 1) % 12
    rows.append((r, 0, np(f'{["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][deg]}-3'), 6, FX_SET_VOL, 0x28))
    rows.append((r+1, 0, np(f'{["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][(deg+7)%12]}-3'), 6, FX_SET_VOL, 0x20))
    rows.append((r+2, 0, np(f'{["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][(deg+3)%12]}-3'), 6, FX_SET_VOL, 0x18))
# Channel 1: stuttering square bursts
for i in range(12):
    r = (i * 5) % 60
    deg = (i * 7) % 12
    rows.append((r, 1, np(f'{["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][deg]}-4'), 5, FX_SET_VOL, 0x24 - (i % 4) * 4))
    rows.append((r+1, 1, np(f'{["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][(deg+5)%12]}-4'), 5, FX_SET_VOL, 0x18))
# Channel 2: FM blip
rows.append((0, 2, np('C-5'), 0, FX_SET_VOL, 0x20))
rows.append((58, 2, np('F#-5'), 0, FX_SET_VOL, 0x24))
# Channel 3: silence
track3.append(make_pattern(rows))

# Pattern 1: glitch intensifies — more chaotic
rows = []
# Channel 0: dense grid — triggering on almost every row
for i in range(30):
    r = i * 2
    if r >= 64:
        break
    deg = (i * 5) % 12
    rows.append((r, 0, np(f'{["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][deg]}-3'), 6, FX_SET_VOL, 0x2C - (i % 3) * 4))
# Channel 1: polymetric FM bursts
for i in range(10):
    r = i * 6 + 1
    deg = (i * 7 + 3) % 12
    rows.append((r, 1, np(f'{["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][deg]}-4'), 0, FX_SET_VOL, 0x28))
    rows.append((r+1, 1, np(f'{["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][(deg+6)%12]}-4'), 0, FX_SET_VOL, 0x1C))
# Channel 2: triangle interjections
for i in range(4):
    rows.append((i*15 + 10, 2, np(f'{["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][(i*4)%12]}-3'), 2, FX_SET_VOL, 0x24))
# Channel 3: low sine impact
rows.append((16, 3, np('C-2'), 1, FX_SET_VOL, 0x30))
rows.append((44, 3, np('G-2'), 1, FX_SET_VOL, 0x28))
track3.append(make_pattern(rows))

# ========== TRACK 4: "drone hymn" (D minor, speed 2) ==========
# Held tones with slow evolution — meditative, sacred
track4 = []
PAT3 = 6

# Pattern 0: drone establishment
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 2))
# Channel 0: deep D drone — organ timbre
rows.append((0, 0, np('D-2'), 8, FX_SET_VOL, 0x30))
# Channel 1: fifth above (A) — slow entry with portamento
rows.append((8, 1, np('A-2'), 8, FX_SET_VOL, 0x28))
rows.append((8, 1, np('A-2'), 8, FX_PORTA_UP, 0x11))  # subtle bend
# Channel 2: third (F) — bell accent on structural beats
rows.append((0, 2, np('F-3'), 3, FX_VIBRATO, 0x18))
rows.append((16, 2, np('F-3'), 4, FX_SET_VOL, 0x20))
rows.append((32, 2, np('A-2'), 3, FX_VIBRATO, 0x1A))
rows.append((48, 2, np('D-3'), 4, FX_SET_VOL, 0x1C))
# Channel 3: high D — sine, quiet, octave accent
rows.append((0, 3, np('D-4'), 1, FX_SET_VOL, 0x18))
rows.append((30, 3, np('D-4'), 1, FX_VIBRATO, 0x22))
track4.append(make_pattern(rows))

# Pattern 1: drone evolution — a simple meditation
rows = []
# Channel 0: D drone continues, subtle amplitude modulation via vol slide
rows.append((0, 0, np('D-2'), 8, FX_SET_VOL, 0x2C))
rows.append((0, 0, np('D-2'), 8, FX_VOL_SLIDE, 0x11))  # slow fade up
rows.append((20, 0, None, 0, FX_VOL_SLIDE, 0x01))      # slow fade down
# Channel 1: A drone with slow vibrato evolution
rows.append((0, 1, np('A-2'), 8, FX_SET_VOL, 0x24))
rows.append((0, 1, np('A-2'), 8, FX_VIBRATO, 0x12))
rows.append((20, 1, np('A-2'), 8, FX_VIBRATO, 0x1A))  # deeper vibrato
# Channel 2: single held minor third — F
rows.append((0, 2, np('F-3'), 3, FX_SET_VOL, 0x20))
rows.append((0, 2, np('F-3'), 3, FX_VIBRATO, 0x13))
rows.append((40, 2, np('F-3'), 3, FX_VIBRATO, 0x1B))
# Channel 3: slow falling figure — D→C→A→D
fall = [0, 6, 4, 0]  # D, C, A, D (degrees in D minor)
for i, deg in enumerate(fall):
    rows.append((i*16, 3, seq(D_MINOR, deg, 2), 1, FX_SET_VOL, 0x1C - i*2))
track4.append(make_pattern(rows))

# ========== ASSEMBLE .MOD FILE ==========
ALL_PATTERNS = track1 + track2 + track3 + track4
NUM_PATTERNS = len(ALL_PATTERNS)
NUM_ORDERS = 8

orders = [
    PAT0, PAT0 + 1,
    PAT1, PAT1 + 1,
    PAT2, PAT2 + 1,
    PAT3, PAT3 + 1,
]

output = bytearray()
output.extend(b"texture body        ")

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

with open('album18_texture_body.mod', 'wb') as f:
    f.write(output)

print(f"Album 'texture body' written: {len(output)} bytes")
print(f"  Tracks: 4")
print(f"  Patterns: {NUM_PATTERNS}")
print(f"  Orders: {len(orders)}")
print(f"  Samples: {', '.join(s[0] for s in SAMPLES)}")
