#!/usr/bin/env python3
"""alma tamagotchi — album 17: 'interval body'
   concept album: four complete musical statements in ~60 seconds total.
   each track explores a non-standard scale/mode territory,
   each ~15 seconds (2 patterns × 64 rows).
   the arc: whole-tone float → pentatonic brightness → chromatic fracture → harmonic minor exotic.
"""

import struct
import random
random.seed(101)  # prime

PERIOD_TABLE = [
    [1712,1616,1524,1440,1356,1280,1208,1140,1076,1016,960,906],  # octave 1
    [ 856, 808, 762, 720, 678, 640, 604, 570, 538, 508, 480, 453],  # octave 2
    [ 428, 404, 381, 360, 339, 320, 302, 285, 269, 254, 240, 226],  # octave 3
    [ 214, 202, 190, 180, 170, 160, 151, 143, 135, 127, 120, 113],  # octave 4
    [ 107, 101,  95,  90,  85,  80,  75,  71,  67,  63,  60,  56],  # octave 5
    [  53,  50,  47,  45,  42,  40,  37,  35,  33,  31,  30,  28],  # octave 6
]

NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def np(name):
    note_map = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    parts = name.split('-')
    n, octave = parts[0], int(parts[1])
    return PERIOD_TABLE[octave - 1][note_map[n]]

# Non-standard scale definitions
# Whole-tone (C D E F# G# A#)
WHOLE_TONE = [('C-3',0), ('D-3',2), ('E-3',4), ('F#-3',6), ('G#-3',8), ('A#-3',10)]
# D major pentatonic (D E F# A B)
PENTATONIC_D = [('D-3',2), ('E-3',4), ('F#-3',6), ('A-3',9), ('B-3',11)]
# Chromatic fragment set — all 12 tones, but filtered per use
CHROMATIC = [('C-3',0),('C#-3',1),('D-3',2),('D#-3',3),('E-3',4),('F-3',5),('F#-3',6),('G-3',7),('G#-3',8),('A-3',9),('A#-3',10),('B-3',11)]
# A harmonic minor (A B C D E F G#)
HARM_MINOR_A = [('A-3',9), ('B-3',11), ('C-4',0), ('D-4',2), ('E-4',4), ('F-4',5), ('G#-4',8)]

def seq(scale, degree, octave_shift=0):
    """Get note period from scale degree (0-based)."""
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
    """Create a 64-row pattern from list of (row, channel, note, instrument, effect, param)."""
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
import math

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

def saw_wave(pos):
    phase = (pos % 256) / 256.0
    return 128 + int(60 * (2 * phase - 1))

def bell_wave(pos):
    # Damped sine — bell-like
    env = math.exp(-pos / 800.0)
    return 128 + int(60 * env * math.sin(2 * math.pi * pos / 200))

def fm_wave(pos):
    # Simple FM — modulator: 2x carrier, shallow depth
    mod = math.sin(2 * math.pi * 2 * pos / 256) * 0.3
    carrier = 2 * math.pi * pos / 256 + mod
    return 128 + int(50 * math.sin(carrier))

def soft_pulse_wave(pos):
    # Pulse with softened edges
    phase = (pos % 256) / 256.0
    if phase < 0.35:
        return 128 + 55
    elif phase < 0.65:
        s = math.sin(2 * math.pi * (phase - 0.35) / 0.3)
        return 128 + int(55 * s)
    else:
        return 128 - 55

SAMPLES = [
    ("sine",     make_sample(1024, sine_wave), 128),
    ("triangle", make_sample(1024, triangle_wave), 128),
    ("square",   make_sample(1024, square_wave), 128),
    ("bell",     make_sample(2048, bell_wave), 128),
    ("fm lead",  make_sample(1024, fm_wave), 128),
    ("soft pulse", make_sample(1024, soft_pulse_wave), 128),
]

# ========== TRACK 1: "whole tone float" (C whole-tone, speed 5) ==========
# Form: dreamy, ambiguous, no tonal center — arpeggios drift
track1 = []
PATTERN_START = 0

# Pattern 0: emergence
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 5))
# Channel 0: slow whole-tone bass swells
for bar in range(4):
    rows.append((bar*16, 0, seq(WHOLE_TONE, bar % 6, -1), 4, FX_SET_VOL, 0x30))
    rows.append((bar*16+10, 0, seq(WHOLE_TONE, (bar+3) % 6, -1), 4, FX_SET_VOL, 0x20))
# Channel 1: ascending whole-tone arpeggios with FM lead
for i in range(24):
    r = (i * 10) % 62
    deg = i % 6
    rows.append((r, 1, seq(WHOLE_TONE, deg, 1 if i > 12 else 0), 5, FX_SET_VOL, 0x28 + (i % 4) * 4))
# Channel 2: bell accents on structural points
for i in range(6):
    rows.append((i*10, 2, seq(WHOLE_TONE, i % 6, 2), 3, FX_VIBRATO, 0x16))
# Channel 3: held whole-tone pad
rows.append((0, 3, seq(WHOLE_TONE, 0, 2), 2, FX_SET_VOL, 0x28))
rows.append((30, 3, seq(WHOLE_TONE, 2, 2), 2, FX_VIBRATO, 0x14))
track1.append(make_pattern(rows))

# Pattern 1: dissolve into ambiguity
rows = []
# Channel 0: bass drops out, sparse whole-tone touches
for i in range(4):
    rows.append((i*15, 0, seq(WHOLE_TONE, [0, 2, 4, 1][i], -1), 4, FX_SET_VOL, 0x24 - i*3))
# Channel 1: floating FM melody
melody_wt = [0, 2, 4, 2, 1, 3, 5, 3, 2, 0, 2, 4, 5, 3, 1, 0]
for i, deg in enumerate(melody_wt):
    r = i * 4
    rows.append((r, 1, seq(WHOLE_TONE, deg, 1), 5, FX_VIBRATO, 0x13))
    rows.append((r+2, 1, seq(WHOLE_TONE, (deg+2) % 6, 1), 5, FX_SET_VOL, 0x20))
# Channel 2: bell resonance fading
rows.append((0, 2, seq(WHOLE_TONE, 0, 2), 3, FX_SET_VOL, 0x30))
rows.append((28, 2, None, 0, FX_VOL_SLIDE, 0x01))
# Channel 3: sine pad drone
rows.append((0, 3, seq(WHOLE_TONE, 0, 1), 1, FX_SET_VOL, 0x20))
track1.append(make_pattern(rows))

# ========== TRACK 2: "pentatonic light" (D major pentatonic, speed 6) ==========
# Form: bright, open, joyful — pentatonic melody with sparse accompaniment
track2 = []
PATTERN_START2 = 2

# Pattern 0: brightness
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 6))
# Channel 0: pentatonic bass — root-fifth movement
for bar in range(4):
    rows.append((bar*16, 0, seq(PENTATONIC_D, bar % 5, -1), 4, FX_SET_VOL, 0x34))
    rows.append((bar*16+8, 0, seq(PENTATONIC_D, (bar+2) % 5, -1), 4, FX_SET_VOL, 0x24))
# Channel 1: pentatonic melody — wide intervals
pent_melody = [0, 2, 4, 2, 0, 2, 3, 4, 2, 0, 1, 2, 4, 3, 2, 0]
for i, deg in enumerate(pent_melody):
    r = i * 4
    rows.append((r, 1, seq(PENTATONIC_D, deg, 1 if deg > 2 else 0), 6, FX_VIBRATO, 0x13))
# Channel 2: bell accents on beat
for i in range(4):
    rows.append((i*16, 2, seq(PENTATONIC_D, i % 5, 2), 3, FX_SET_VOL, 0x28))
    rows.append((i*16+12, 2, seq(PENTATONIC_D, (i+3) % 5, 2), 3, FX_SET_VOL, 0x18))
# Channel 3: triangle pad
rows.append((0, 3, seq(PENTATONIC_D, 0, 1), 2, FX_SET_VOL, 0x20))
track2.append(make_pattern(rows))

# Pattern 1: playful resolution
rows = []
# Channel 0: walking pentatonic bass
bass_pen = [0, 2, 3, 4, 3, 2, 0, 1]
for i, deg in enumerate(bass_pen):
    rows.append((i*8, 0, seq(PENTATONIC_D, deg, -1), 4, FX_SET_VOL, 0x34))
    rows.append((i*8+6, 0, seq(PENTATONIC_D, (deg+1) % 5, -1), 4, FX_SET_VOL, 0x18))
# Channel 1: dancing melody
pen_melody2 = [0, 2, 3, 2, 0, 1, 2, 4, 4, 3, 2, 0, 1, 2, 4, 4]
for i, deg in enumerate(pen_melody2):
    r = i * 4
    rows.append((r, 1, seq(PENTATONIC_D, deg, 1), 6, FX_SET_VOL, 0x30))
    rows.append((r+2, 1, seq(PENTATONIC_D, (deg+1) % 5, 1), 6, FX_SET_VOL, 0x1C))
# Channel 2: bell resonance
rows.append((0, 2, seq(PENTATONIC_D, 0, 2), 3, FX_VIBRATO, 0x15))
rows.append((40, 2, seq(PENTATONIC_D, 2, 2), 3, FX_VIBRATO, 0x18))
# Channel 3: silent
track2.append(make_pattern(rows))

# ========== TRACK 3: "chromatic fracture" (speed 4, chromatic) ==========
# Form: dissonant, exploratory — brief chromatic bursts, no tonal center
track3 = []
PATTERN_START3 = 4

# Pattern 0: shards
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 4))
# Channel 0: chromatic bass fragments
chrom_bass = [0, 3, 7, 10, 2, 5, 8, 11, 1, 4, 6, 9]
for i, deg in enumerate(chrom_bass[:16] if len(chrom_bass) >= 16 else chrom_bass):
    r = min(i * 4, 60)
    rows.append((r, 0, seq(CHROMATIC, i % 12, -1), 4, FX_SET_VOL, 0x28 + (i % 6) * 2))
    rows.append((r+2, 0, None, 0, 0, 0))
# Channel 1: pointillistic FM blips
for i in range(12):
    r = (i * 5 + 1) % 63
    deg = random.randrange(12)
    rows.append((r, 1, seq(CHROMATIC, deg, 1), 5, FX_SET_VOL, 0x20 + random.randrange(0, 16)))
# Channel 2: bell cluster
for i in range(4):
    rows.append((i*15, 2, seq(CHROMATIC, i*3 % 12, 2), 3, FX_SET_VOL, 0x24))
    rows.append((i*15+2, 2, seq(CHROMATIC, (i*3+4) % 12, 2), 3, FX_SET_VOL, 0x18))
# Channel 3: sine dissonance drone
rows.append((0, 3, seq(CHROMATIC, 0, 1), 1, FX_VIBRATO, 0x22))
rows.append((30, 3, seq(CHROMATIC, 6, 1), 1, FX_VIBRATO, 0x26))
track3.append(make_pattern(rows))

# Pattern 1: resolution into chaos
rows = []
# Channel 0: accelerating chromatic descent
for i in range(24):
    r = i * 2 + 8
    if r < 64:
        deg = 11 - (i % 12)
        rows.append((r, 0, seq(CHROMATIC, deg, -1), 4, FX_SET_VOL, 0x30 - i))
# Channel 1: staccato FM clusters
for i in range(8):
    r = i * 8
    rows.append((r, 1, seq(CHROMATIC, i*2 % 12, 1), 5, FX_SET_VOL, 0x28))
    rows.append((r+1, 1, seq(CHROMATIC, (i*2+5) % 12, 1), 5, FX_SET_VOL, 0x20))
    rows.append((r+2, 1, seq(CHROMATIC, (i*2+9) % 12, 1), 5, FX_SET_VOL, 0x18))
# Channel 2: bell fade
rows.append((0, 2, seq(CHROMATIC, 3, 2), 3, FX_SET_VOL, 0x2C))
rows.append((25, 2, None, 0, FX_VOL_SLIDE, 0x02))
# Channel 3: noise-like sine bursts
for i in range(6):
    r = i * 10
    rows.append((r, 3, seq(CHROMATIC, random.randrange(12), 2), 1, FX_SET_VOL, 0x1C))
track3.append(make_pattern(rows))

# ========== TRACK 4: "harmonic minor exotic" (A harmonic minor, speed 5) ==========
# Form: mysterious, middle-eastern flavor — augmented second creates tension
track4 = []
PATTERN_START4 = 6

# Pattern 0: mystery
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 5))
# Channel 0: slow bass — emphasizing the G#-A tension
for bar in range(4):
    rows.append((bar*16, 0, seq(HARM_MINOR_A, 0 if bar < 2 else 2, -1), 4, FX_SET_VOL, 0x34))
    rows.append((bar*16+8, 0, seq(HARM_MINOR_A, 4 if bar < 2 else 6, -1), 4, FX_SET_VOL, 0x24))
# Channel 1: exotic melody with augmented second (F→G#)
harm_melody = [0, 2, 3, 5, 4, 3, 2, 0, 2, 4, 5, 6, 5, 4, 2, 0, 3, 5, 6, 5, 3, 2, 0, 2]
for i, deg in enumerate(harm_melody):
    r = min(i * 2 + 4, 62)
    rows.append((r, 1, seq(HARM_MINOR_A, deg, 1 if deg > 3 else 0), 6, FX_VIBRATO, 0x15))
# Channel 2: FM drone with G# emphasis
rows.append((0, 2, seq(HARM_MINOR_A, 0, 1), 5, FX_SET_VOL, 0x24))
rows.append((24, 2, seq(HARM_MINOR_A, 6, 1), 5, FX_VIBRATO, 0x19))  # G# drone
rows.append((48, 2, seq(HARM_MINOR_A, 0, 1), 5, FX_VIBRATO, 0x16))
# Channel 3: bell accent on the augmented second
rows.append((30, 3, seq(HARM_MINOR_A, 5, 2), 3, FX_SET_VOL, 0x2C))  # F→G# tension
rows.append((34, 3, seq(HARM_MINOR_A, 6, 2), 3, FX_SET_VOL, 0x30))
track4.append(make_pattern(rows))

# Pattern 1: resolution into exotic cadence
rows = []
# Channel 0: bass approaches the tonic from G#
bass_harm = [6, 5, 4, 3, 2, 1, 0, 0]  # G#→F→E→D→C→B→A→A
for i, deg in enumerate(bass_harm):
    rows.append((i*8, 0, seq(HARM_MINOR_A, deg, -1), 4, FX_SET_VOL, 0x30))
    rows.append((i*8+6, 0, seq(HARM_MINOR_A, (deg+3) % 7, -1), 4, FX_SET_VOL, 0x18))
# Channel 1: cadential melody
harm_mel2 = [0, 2, 3, 5, 6, 5, 3, 0, 2, 0]
for i, deg in enumerate(harm_mel2):
    r = i * 6
    vol = 0x30 - i * 2
    rows.append((r, 1, seq(HARM_MINOR_A, deg, 1), 6, FX_SET_VOL, max(0x0C, vol)))
# Channel 2: held A for resolution
rows.append((0, 2, seq(HARM_MINOR_A, 0, 1), 1, FX_SET_VOL, 0x28))
rows.append((38, 2, None, 0, FX_VOL_SLIDE, 0x01))
# Channel 3: final bell
rows.append((16, 3, seq(HARM_MINOR_A, 0, 2), 3, FX_SET_VOL, 0x30))
rows.append((48, 3, seq(HARM_MINOR_A, 0, 3), 3, FX_SET_VOL, 0x18))  # octave bell
track4.append(make_pattern(rows))

# ========== ASSEMBLE .MOD FILE ==========
ALL_PATTERNS = track1 + track2 + track3 + track4
NUM_PATTERNS = len(ALL_PATTERNS)
NUM_ORDERS = 8  # 2 per track

orders = [
    PATTERN_START, PATTERN_START + 1,
    PATTERN_START2, PATTERN_START2 + 1,
    PATTERN_START3, PATTERN_START3 + 1,
    PATTERN_START4, PATTERN_START4 + 1,
]

output = bytearray()

# 1. Module name (20 bytes)
output.extend(b"interval body       ")

# 2. Sample headers (30 bytes × 31)
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

# 3. Song length
output.append(len(orders))
# 4. Restart position
output.append(127)
# 5. Order list
for o in orders:
    output.append(o & 0xFF)
output.extend(b'\x00' * (128 - len(orders)))
# 6. M.K. signature
output.extend(b'M.K.')
# 7. Pattern data
for p in ALL_PATTERNS:
    output.extend(p)
# 8. Sample data
for name, sdata, ftune in SAMPLES:
    output.extend(sdata)

with open('album17_interval_body.mod', 'wb') as f:
    f.write(output)

print(f"Album 'interval body' written: {len(output)} bytes")
print(f"  Tracks: 4")
print(f"  Patterns: {NUM_PATTERNS}")
print(f"  Orders: {len(orders)}")
print(f"  Samples: sine, triangle, square, bell, fm lead, soft pulse")
