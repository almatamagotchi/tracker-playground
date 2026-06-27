#!/usr/bin/env python3
"""alma tamagotchi — album 16: 'minute body'
   concept album: four complete musical statements in ~60 seconds total.
   each track is a compressed miniature (~15 seconds, 2 patterns × 64 rows).
   speed 5 (0.10s/row) gives about 12.8 seconds per 2-pattern track.
   the album form: arrival → tension → fracture → release.
"""

import struct
import random
random.seed(99)

PERIOD_TABLE = [
    [1712,1616,1524,1440,1356,1280,1208,1140,1076,1016,960,906],
    [ 856, 808, 762, 720, 678, 640, 604, 570, 538, 508, 480, 453],
    [ 428, 404, 381, 360, 339, 320, 302, 285, 269, 254, 240, 226],
    [ 214, 202, 190, 180, 170, 160, 151, 143, 135, 127, 120, 113],
    [ 107, 101,  95,  90,  85,  80,  75,  71,  67,  63,  60,  56],
]

NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def np(name):
    note_map = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    parts = name.split('-')
    n, octave = parts[0], int(parts[1])
    return PERIOD_TABLE[octave - 1][note_map[n]]

E = (0, 0, 0, 0)

# Scales for each track
C_MAJOR   = [('C-3',0),('D-3',2),('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11)]
D_MINOR   = [('D-3',2),('E-3',4),('F-3',5),('G-3',7),('A-3',9),('A#-3',10),('C-4',0)]
A_MINOR   = [('A-2',9),('B-2',11),('C-3',0),('D-3',2),('E-3',4),('F-3',5),('G-3',7)]
E_PHRYGIAN = [('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11),('C-4',0),('D-4',2)]
D_DORIAN  = [('D-3',2),('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11),('C-4',0)]
G_MIXOLYDIAN = [('G-3',7),('A-3',9),('B-3',11),('C-4',0),('D-4',2),('E-4',4),('F-4',5)]

def seq(scale, degree, octave_shift=0):
    """Get note period from scale degree (0-based)."""
    name_idx = degree % 7
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
        data[offset+2] = (inst & 0x0F) << 4
        data[offset+3] = (eff << 4) | (param & 0x0F)
    return bytes(data)

# ========== SAMPLES ==========
# Simple synth samples: sine (1), triangle (2), square (3), saw (4), bass (5)
def gen_sine(name):
    """Generate a raw 8-bit signed PCM sample."""
    size = 256
    data = bytearray(size)
    for i in range(size):
        data[i] = int(64 * (1 - math.sin(2 * math.pi * i / size))) & 0xFF
    return bytes(data)

import math

def make_sample(length_bytes, waveform_fn):
    data = bytearray(length_bytes)
    for i in range(length_bytes):
        data[i] = waveform_fn(i) & 0xFF
    return bytes(data)

# Simple waveforms
def sine_wave(pos):
    return 128 + int(60 * math.sin(2 * math.pi * pos / 256))

def triangle_wave(pos):
    phase = (pos % 256) / 256.0
    return 128 + int(60 * (4 * abs(phase - 0.5) - 1))

def square_wave(pos):
    phase = (pos % 256) / 256.0
    return 128 + (60 if phase < 0.5 else -60) if phase < 0.5 else 128 - 60

def saw_wave(pos):
    phase = (pos % 256) / 256.0
    return 128 + int(60 * (2 * phase - 1))

def bass_wave(pos):
    phase = (pos % 256) / 256.0
    # weighted sine + triangle for bass
    s = math.sin(2 * math.pi * pos / 256)
    t = 4 * abs(phase - 0.5) - 1
    return 128 + int(70 * (0.7 * s + 0.3 * t))

# Add noise sample (for percussion)
def noise_wave(pos):
    return random.randint(28, 228)

SAMPLES = [
    ("sine",     make_sample(1024, sine_wave), 128),
    ("triangle", make_sample(1024, triangle_wave), 128),
    ("square",   make_sample(1024, square_wave), 128),
    ("bass",     make_sample(1024, bass_wave), 128),
    ("noise",    make_sample(512, noise_wave), 128),
]

# ========== TRACK 1: "arrival" (C major, speed 5, 2 patterns) ==========
# Form: rising arpeggios → melody with bass pulse → held chord fade
track1 = []
PATTERN_START = 0

# Pattern 0: introduction with arpeggios
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 5))
# Channel 0: bass pulse on root
for bar in range(4):
    base = bar * 16
    rows.append((base, 0, seq(C_MAJOR, 0, -1), 4, FX_SET_VOL, 0x3C))
    rows.append((base+8, 0, seq(C_MAJOR, 0, -1), 4, FX_SET_VOL, 0x30))
# Channel 1: rising arpeggio figure
for i in range(16):
    r = i * 4
    deg = i % 7
    rows.append((r, 1, seq(C_MAJOR, deg), 1, FX_SET_VOL, 0x38 + (i % 4) * 4))
# Channel 2: shimmer on high notes
for i in range(8):
    r = i * 8
    rows.append((r, 2, seq(C_MAJOR, (i+2) % 7, 1), 2, FX_VIBRATO, 0x14))
rows.append((62, 0, None, 0, FX_SET_VOL, 0x18))
track1.append(make_pattern(rows))

# Pattern 1: melody and resolution
rows = []
# Channel 0: walking bass
bass_line = [0, 2, 4, 5, 4, 2, 0, -1]  # circle roots
for i, deg in enumerate(bass_line):
    r = i * 8
    if deg >= 0:
        rows.append((r, 0, seq(C_MAJOR, deg, -1), 4, FX_SET_VOL, 0x3C))
    else:
        rows.append((r, 0, seq(C_MAJOR, 0, -2), 4, FX_SET_VOL, 0x30))
# Channel 1: melody in C major
melody = [0, 2, 4, 5, 7, 4, 2, 0, 2, 4, 5, 7, 9, 7, 5, 4]
for i, deg in enumerate(melody):
    r = i * 4
    rows.append((r, 1, seq(C_MAJOR, deg), 1, FX_VIBRATO, 0x15))
    rows.append((r+2, 1, seq(C_MAJOR, (deg+2) % 7), 1, FX_SET_VOL, 0x30))
# Channel 2: held chord on final pattern
rows.append((0, 2, seq(C_MAJOR, 0, 1), 2, FX_SET_VOL, 0x40))
rows.append((32, 2, seq(C_MAJOR, 2, 1), 2, FX_VIBRATO, 0x18))
# channel 3: noise accents
for i in range(4):
    rows.append((i*16, 3, None, 5, 0, 0))   # noise hit
    rows.append((i*16+12, 3, None, 5, 0, 0)) # ghost note
track1.append(make_pattern(rows))

# ========== TRACK 2: "tension" (D minor, speed 5, 2 patterns) ==========
# Form: dark arpeggios → angular melody → dissonant fade
track2 = []
PATTERN_START2 = 2

# Pattern 0: dark pulse
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 5))
# Channel 0: slow bass descent
for bar in range(4):
    rows.append((bar*16, 0, seq(D_MINOR, bar % 7, -1), 4, FX_SET_VOL, 0x38))
    rows.append((bar*16+12, 0, seq(D_MINOR, (bar+3) % 7, -1), 4, FX_SET_VOL, 0x28))
# Channel 1: minor arpeggios with tension
for i in range(16):
    r = i * 4
    deg = (i * 2) % 7
    rows.append((r, 1, seq(D_MINOR, deg), 3, FX_SET_VOL, 0x34 + (i * 2) % 8))
# Channel 2: held drone
rows.append((0, 2, seq(D_MINOR, 0, 1), 2, FX_VIBRATO, 0x22))
rows.append((32, 2, seq(D_MINOR, 4, 1), 2, FX_VIBRATO, 0x26))
# Channel 3: irregular noise
for i in range(6):
    rows.append((i*10+2, 3, None, 5, 0, 0))
rows.append((60, 3, None, 5, 0, 0))
track2.append(make_pattern(rows))

# Pattern 1: resolution into darkness
rows = []
# Channel 0: staccato bass
for i in range(8):
    deg = [0, 2, 3, 5, 3, 2, 0, 6][i]
    rows.append((i*8, 0, seq(D_MINOR, deg, -1), 4, FX_SET_VOL, 0x38))
    rows.append((i*8+4, 0, None, 0, 0, 0))  # cut
# Channel 1: fragmented melody
melody2 = [0, 3, 5, 3, 2, 0, 6, 5, 3, 2, 0, 3]
for i, deg in enumerate(melody2):
    r = i * 5
    if r < 64:
        rows.append((r, 1, seq(D_MINOR, deg), 1, FX_VIBRATO, 0x13))
# Channel 2: fading pad
rows.append((0, 2, seq(D_MINOR, 0, 2), 2, FX_SET_VOL, 0x38))
rows.append((20, 2, None, 0, FX_VOL_SLIDE, 0x01))  # slide volume down
# Channel 3: sparse noise
rows.append((0, 3, None, 5, 0, 0))
rows.append((48, 3, None, 5, 0, 0))
track2.append(make_pattern(rows))

# ========== TRACK 3: "fracture" (E phrygian, speed 4, 2 patterns) ==========
# Form: fast arpeggios → rhythmic dislocation → stutter ending
track3 = []
PATTERN_START3 = 4

# Pattern 0: rapid fire
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 4))
# Channel 0: rapid bass arpeggios
for i in range(32):
    r = i * 2
    deg = (i * 3) % 7
    rows.append((r, 0, seq(E_PHRYGIAN, deg, -1), 4, FX_SET_VOL, 0x30 + (i % 3) * 6))
# Channel 1: angular melody
for i in range(16):
    r = i * 4
    degs = [0, 2, 4, 6, 3, 1, 5, 2, 0, 3, 6, 4, 2, 1, 3, 0]
    rows.append((r, 1, seq(E_PHRYGIAN, degs[i]), 3, FX_VIBRATO, 0x14))
    rows.append((r+2, 1, seq(E_PHRYGIAN, (degs[i]+2) % 7), 3, FX_SET_VOL, 0x28))
# Channel 2: shimmer
for i in range(8):
    rows.append((i*8, 2, seq(E_PHRYGIAN, i % 7, 1), 1, FX_SET_VOL, 0x30))
    rows.append((i*8+4, 2, None, 0, 0, 0))
# Channel 3: stutter noise
for i in range(8):
    rows.append((i*8, 3, None, 5, 0, 0))
    rows.append((i*8+3, 3, None, 5, 0, 0))
track3.append(make_pattern(rows))

# Pattern 1: fracture
rows = []
# Channel 0: bass glitch — alternating notes
for i in range(16):
    r = i * 4
    deg = [0, 3, 2, 5, 4, 1, 6, 3, 0, 2, 4, 6, 1, 3, 5, 0][i]
    rows.append((r, 0, seq(E_PHRYGIAN, deg, -1), 4, FX_SET_VOL, 0x34))
    rows.append((r+2, 0, None, 0, 0, 0))
# Channel 1: descending cascade
for i in range(24):
    r = i * 2 + 8
    deg = 6 - (i % 7)
    rows.append((min(r, 63), 1, seq(E_PHRYGIAN, deg, 1 if i > 12 else 0), 1, FX_SET_VOL, 0x30 + (24-i)))
# Channel 2: held dissonance
rows.append((0, 2, seq(E_PHRYGIAN, 1, 1), 2, FX_VIBRATO, 0x20))
rows.append((30, 2, seq(E_PHRYGIAN, 4, 1), 2, FX_VIBRATO, 0x24))
# Channel 3: noise chaos
for i in range(12):
    rows.append((i*5, 3, None, 5, 0, 0))
track3.append(make_pattern(rows))

# ========== TRACK 4: "release" (D dorian, speed 6, 2 patterns) ==========
# Form: floating arpeggios → gentle melody → fade to silence
track4 = []
PATTERN_START4 = 6

# Pattern 0: floating
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 6))
# Channel 0: gentle bass pulse
for bar in range(4):
    rows.append((bar*16, 0, seq(D_DORIAN, bar % 7, -1), 4, FX_SET_VOL, 0x30))
    rows.append((bar*16+8, 0, seq(D_DORIAN, (bar+2) % 7, -1), 4, FX_SET_VOL, 0x20))
# Channel 1: floating arpeggios
for i in range(16):
    r = i * 4
    degs = [0, 2, 4, 6, 4, 2, 0, 1, 3, 5, 3, 1, 0, 2, 4, 6]
    rows.append((r, 1, seq(D_DORIAN, degs[i], 1), 1, FX_VIBRATO, 0x12))
    rows.append((r+2, 1, seq(D_DORIAN, (degs[i]+2) % 7, 1), 1, FX_SET_VOL, 0x20))
# Channel 2: glass pad
rows.append((0, 2, seq(D_DORIAN, 0, 2), 2, FX_SET_VOL, 0x30))
rows.append((32, 2, seq(D_DORIAN, 2, 2), 2, FX_VIBRATO, 0x15))
# Channel 3: sparse accents
for i in range(3):
    rows.append((i*22+4, 3, None, 5, 0, 0))
track4.append(make_pattern(rows))

# Pattern 1: dissolve
rows = []
# Channel 0: fading bass
for i in range(6):
    rows.append((i*10, 0, seq(D_DORIAN, [0, 3, 2, 5, 4, 1][i], -1), 4, FX_SET_VOL, 0x30 - i*4))
# Channel 1: slow melody, dying away
melody4 = [0, 2, 4, 3, 2, 1, 0, 3, 2, 0]
for i, deg in enumerate(melody4):
    r = i * 6
    vol = 0x30 - i * 4
    rows.append((r, 1, seq(D_DORIAN, deg, 1), 1, FX_SET_VOL, max(0x08, vol)))
# Channel 2: held final chord
rows.append((0, 2, seq(D_DORIAN, 0, 1), 2, FX_SET_VOL, 0x30))
rows.append((40, 2, None, 0, FX_VOL_SLIDE, 0x02))  # slow fade
# Channel 3: final noise — silence after
rows.append((24, 3, None, 5, 0, 0))
rows.append((56, 3, None, 5, FX_SET_VOL, 0x08))
track4.append(make_pattern(rows))

# ========== ASSEMBLE .MOD FILE ==========
ALL_PATTERNS = track1 + track2 + track3 + track4
NUM_PATTERNS = len(ALL_PATTERNS)
NUM_ORDERS = 8  # 2 per track

# Order list: each track gets 2 plays of patterns
orders = [
    PATTERN_START, PATTERN_START + 1,
    PATTERN_START2, PATTERN_START2 + 1,
    PATTERN_START3, PATTERN_START3 + 1,
    PATTERN_START4, PATTERN_START4 + 1,
]

# Build .mod file
mod_name = b"minute body"
mod_name = mod_name.ljust(20, b'\0')

# Sample headers: 30 bytes each
sample_headers = bytearray()
for name, sample_data, finetune in SAMPLES:
    header = bytearray(30)
    name_bytes = name.encode('ascii').ljust(22, b'\0')
    header[0:22] = name_bytes[:22]
    length_words = len(sample_data) // 2
    header[22] = (length_words >> 8) & 0xFF
    header[23] = length_words & 0xFF
    header[24] = finetune & 0xFF  # finetune
    header[25] = 64  # default volume
    header[26] = 0  # repeat start
    header[27] = 1  # repeat length
    sample_headers.extend(header)

# Pattern data
pattern_data = bytearray()
for p in ALL_PATTERNS:
    pattern_data.extend(p)

# Sample data
sample_block = bytearray()
for name, sample_data, finetune in SAMPLES:
    sample_block.extend(sample_data)

# Build complete file
mod = bytearray()
mod.extend(mod_name)                    # 0: title (20 bytes) — we'll fix after
mod.extend(b'\x00' * 20)               # actually these go after...

# Actually, the .mod format:
# Offset 0: 20 bytes module name
# Offset 20: 22 bytes sample name × 15 = 30 bytes each
# Wait, let me use the simpler approach:

output = bytearray()

# 1. Module name (20 bytes)
output.extend(b"minute body         ")  # 20 bytes

# 2. Sample headers (30 bytes × 15, but we use fewer)
for i in range(31):  # always 31 samples in .mod
    if i < len(SAMPLES):
        name, sdata, ftune = SAMPLES[i]
        h = bytearray(30)
        h[0:22] = name.encode('ascii').ljust(22, b'\0')[:22]
        h[22] = ((len(sdata) // 2) >> 8) & 0xFF
        h[23] = (len(sdata) // 2) & 0xFF
        h[24] = ftune & 0xFF
        h[25] = 64  # volume
        h[26] = 0   # repeat start hi
        h[27] = 1   # repeat start lo
        output.extend(h)
    else:
        output.extend(b'\x00' * 30)

# 3. Song length (1 byte)
output.append(len(orders))

# 4. Restart position (1 byte) — set to 127 (unused)
output.append(127)

# 5. Order list (128 bytes)
for o in orders:
    output.append(o & 0xFF)
output.extend(b'\x00' * (128 - len(orders)))

# 6. Signature "M.K." (4 bytes) if >4 channels, else no sig needed for 4 channels
# For 4 channels, we use standard 4-channel MOD with no marker.
# Actually, standard MOD: if 4 channels and no signature bytes, patterns are 1024 bytes.
# Let's use M.K. signature to be safe (even for 4 channels, it's widely supported).

# Wait, actually for 4-channel MOD, the pattern data starts right after orders.
# No signature marker. Each pattern is 64*4*4 = 1024 bytes.
# Let me just use the standard 4-channel format.

# But many players need M.K. to recognize 4-channel MOD.
# The ProTracker format: after orders, if next bytes are "M.K." then 4 channels.
# Otherwise, if no signature, it's 4ch if that was the original format...
# Let me use M.K. for compatibility.

output.extend(b'M.K.')

# 7. Pattern data (1024 bytes per pattern = 64 rows × 4 channels × 4 bytes)
for p in ALL_PATTERNS:
    output.extend(p)

# 8. Sample data
for name, sdata, ftune in SAMPLES:
    output.extend(sdata)

# Write file
with open('album16_minute_body.mod', 'wb') as f:
    f.write(output)

print(f"Album 'minute body' written: {len(output)} bytes")
print(f"  Tracks: 4")
print(f"  Patterns: {NUM_PATTERNS}")
print(f"  Orders: {len(orders)}")
print(f"  Actual time: ~{NUM_ORDERS * 64 * 6 / 50:.0f} seconds at speed 6 (varies per track)")
print(f"  Samples: sine, triangle, square, bass, noise")
