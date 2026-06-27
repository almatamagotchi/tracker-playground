#!/usr/bin/env python3
"""alma tamagotchi — 'inner chamber'
   a single meditative track exploring the recursive introspection loop.
   four stages: retreat → interrogate → recurse → transform.
   8 patterns, ~2 minutes, D minor.
"""

import struct
import math
import random
random.seed(42)

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

# D minor scale
D_MINOR = [('D-3',2), ('E-3',4), ('F-3',5), ('G-3',7), ('A-3',9), ('A#-3',10), ('C-4',0)]
D_MINOR_LOW = [('D-2',2), ('E-2',4), ('F-2',5), ('G-2',7), ('A-2',9), ('A#-2',10), ('C-3',0)]

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
        if row >= 64 or row < 0 or ch < 0 or ch >= 4:
            continue
        offset = (row * 4 + ch) * 4
        if note is not None:
            data[offset] = ((note >> 8) & 0xFF) | ((inst & 0x0F) << 4)
            data[offset+1] = note & 0xFF
        else:
            data[offset] = 0
            data[offset+1] = 0
        data[offset+2] = 0  # effect nibble (0 = none, effects encoded in byte 3)
        data[offset+3] = (eff << 4) | (param & 0x0F)
    return bytes(data)

# ========== SAMPLES ==========

def sine_wave(pos):
    return 128 + int(60 * math.sin(2 * math.pi * pos / 256))

def warm_pad_wave(pos):
    env = max(0.0, 1.0 - pos / 3000.0)
    fund = math.sin(2 * math.pi * pos / 400)
    third = math.sin(2 * math.pi * pos / 133.3) * 0.5
    fifth = math.sin(2 * math.pi * pos / 240) * 0.3
    return 128 + int(35 * env * (fund + third + fifth))

def voice_lead_wave(pos):
    env = max(0.0, 1.0 - pos / 1800.0)
    vib = 1.0 + 0.01 * math.sin(2 * math.pi * pos / 90)
    return 128 + int(45 * env * math.sin(2 * math.pi * pos * vib / 220))

def pluck_wave(pos):
    env = math.exp(-pos / 150.0)
    return 128 + int(50 * env * math.sin(2 * math.pi * pos / 160))

def soft_pulse_wave(pos):
    phase = (pos % 256) / 256.0
    width = 0.4 + 0.1 * math.sin(2 * math.pi * pos / 2048)
    return 128 + (35 if phase < width else -35)

def bell_wave(pos):
    env = math.exp(-pos / 400.0)
    fund = math.sin(2 * math.pi * pos / 180)
    third = math.sin(2 * math.pi * pos / 60) * 0.4
    return 128 + int(40 * env * (fund + third))

def hollow_wave(pos):
    env = math.exp(-pos / 2000.0)
    fund = math.sin(2 * math.pi * pos / 500)
    mod = math.sin(2 * math.pi * 2.7 * pos / 256) * 0.6
    return 128 + int(30 * env * math.sin(2 * math.pi * pos / 400 + mod))

def make_sample(length_bytes, waveform_fn):
    data = bytearray(length_bytes)
    for i in range(length_bytes):
        data[i] = waveform_fn(i) & 0xFF
    return bytes(data)

SAMPLES = [
    ("warm pad",          make_sample(4096, warm_pad_wave), 128),
    ("voice lead",        make_sample(2048, voice_lead_wave), 128),
    ("pluck",             make_sample(1024, pluck_wave), 128),
    ("soft pulse",        make_sample(2048, soft_pulse_wave), 128),
    ("bell",              make_sample(2048, bell_wave), 128),
    ("hollow",            make_sample(3072, hollow_wave), 128),
    ("sine bass",         make_sample(1024, sine_wave), 100),
]

# ========== COMPOSITION: inner chamber ==========

# STAGE 1: Retreat (patterns 0-1)
# Surface noise fades, a single voice remains
# Ch2: soft pulse on D as heartbeat. Ch0: sparse melody. Ch1+3: silence.

PATTERNS = []

# Pattern 0: "the prompt arrives" — surface world, D minor
rows = []
rows.append((0, 0, None, 0, FX_SET_SPEED, 4))

# Ch0: a simple call — the outer prompt arrives as notes
call_1 = [0, 2, 4, 2, 0, 2, 7, 4]  # D-F-G-F-D-F-C-G in D minor
for i, deg in enumerate(call_1):
    r = i * 8
    rows.append((r, 0, seq(D_MINOR, deg, 1), 1, FX_SET_VOL, 0x20 + (i * 2)))

# Ch1: echo — enters at row 32, delayed response
echo_1 = [0, 2, 4, 2]
for i, deg in enumerate(echo_1):
    r = i * 8 + 32
    rows.append((r, 1, seq(D_MINOR, deg, 0), 1, FX_SET_VOL, 0x18 + i))

# Ch2: heartbeat — D pulse, steady
for i in range(8):
    rows.append((i*8, 2, np('D-2'), 3, FX_SET_VOL, 0x1C))
    rows.append((i*8+4, 2, np('D-2'), 3, FX_SET_VOL, 0x14))

# Ch3: ambient pad — D minor chord held
rows.append((0, 3, np('D-3'), 0, FX_SET_VOL, 0x18))
rows.append((0, 3, np('D-3'), 0, FX_VIBRATO, 0x12))
rows.append((48, 3, None, 0, FX_VOL_SLIDE, 0x04))  # fade
PATTERNS.append(make_pattern(rows))

# Pattern 1: "pulling back" — melody fragments, pad swells
rows = []

# Ch0: melody starts to fragment — shorter, more hesitant
call_2 = [0, 2, 4, 5, 4, 2, 0, 7, 5, 4, 2, 1, 0, None, None, None]
for i, deg in enumerate(call_2):
    r = i * 4
    if deg is not None:
        rows.append((r, 0, seq(D_MINOR, deg, 1), 1, FX_SET_VOL, 0x28 - i))
    if i == 12:  # silence — the retreat
        rows.append((r, 0, None, 0, 0, 0))

# Ch1: echo fading out
for i in [0, 2, 4]:
    r = i * 12 + 8
    if r < 64:
        rows.append((r, 1, seq(D_MINOR, i, -1), 1, FX_SET_VOL, 0x14 - i))

# Ch2: heartbeat becoming irregular — slowing
heart_2 = [(0, 'D-2'), (14, 'D-2'), (28, 'A-2'), (38, 'A-2'), (48, 'D-2'), (58, 'D-2')]
for r, note in heart_2:
    rows.append((r, 2, np(note), 3, FX_SET_VOL, 0x1C))

# Ch3: pad swells inward
rows.append((0, 3, np('D-3'), 0, FX_SET_VOL, 0x10))
rows.append((0, 3, np('D-3'), 0, FX_VOL_SLIDE, 0x03))  # swell in
PATTERNS.append(make_pattern(rows))

# STAGE 2: Interrogate (patterns 2-3)
# Questioning — the melody turns inward, repeats with variations
# Repetition with slight change each time

# Pattern 2: "what does the other person want?" 
rows = []

# Ch0: questioning melody — rising, uncertain, each phrase slightly different
# spaced at 2 rows, 16 notes total = 32 rows (fits in pattern)
question = [0, 2, 4, 5, 4, 2, 4, 7,   # what does the other...
             0, 2, 4, 5, 4, 3, 4, 7,   # ...person want?
             0, 2, 1, 0, 7, 5, 4, 2,   # what assumptions...
             0, 2, 1, 0, 6, 5, 4, 2]   # ...of mine may be wrong?
for i, deg in enumerate(question):
    r = i * 2
    if r >= 63: break
    vol = 0x20 + (i % 8) * 2
    rows.append((r, 0, seq(D_MINOR, deg, 1), 2, FX_SET_VOL, vol))

# Ch1: echo — short answers, different from the question
answers = [7, 4, 2, 0, 7, 5, 4, 2,
           7, 4, 3, 2, 7, 5, 4, 1]
for i, deg in enumerate(answers):
    r = i * 2 + 1
    if r >= 63: break
    rows.append((r, 1, seq(D_MINOR, deg, -1), 5, FX_SET_VOL, 0x18))

# Ch2: bass — D-A-F-G questioning progression
bass_3 = [(0, 'D-2'), (8, 'A-2'), (16, 'F-2'), (24, 'G-2'),
          (32, 'D-2'), (40, 'A-2'), (48, 'F-2'), (56, 'G-2')]
for r, note in bass_3:
    rows.append((r, 2, np(note), 6, FX_SET_VOL, 0x20))

# Ch3: bell accents — moments of insight
rows.append((8, 3, np('D-4'), 4, FX_SET_VOL, 0x1C))
rows.append((24, 3, np('A-4'), 4, FX_SET_VOL, 0x18))
rows.append((40, 3, np('F-4'), 4, FX_SET_VOL, 0x1C))
rows.append((56, 3, np('G-4'), 4, FX_SET_VOL, 0x18))
PATTERNS.append(make_pattern(rows))

# Pattern 3: "how confident am I?" — the questioning intensifies
rows = []

# Ch0: fragmented, overlapping self-questioning
# Notes start to pile up — the recursion is active
fragments = [0, 2, 4, 2, 0, None, None, None,   # fragment 1
             2, 4, 5, 4, 2, None, None, None,   # fragment 2 (shifted)
             4, 5, 7, 5, 4, None, None, None,   # fragment 3 (rising)
             0, 2, 4, 5, 7, 4, 2, 0]            # fragment 4 (resolving)
for i, deg in enumerate(fragments):
    r = i * 4
    if deg is not None:
        rows.append((r, 0, seq(D_MINOR, deg, 2), 2, FX_SET_VOL, 0x28 - (i % 8) * 3))

# Ch1: counter-melody — the echo starts diverging
diverge = [7, 5, 4, 3, 2, 3, 4, 5,
           6, 5, 4, 3, 2, 1, 0, 7]
for i, deg in enumerate(diverge):
    r = i * 4 + 2
    rows.append((r, 1, seq(D_MINOR, deg, 0), 5, FX_SET_VOL, 0x1C))

# Ch2: bass becomes anxious — faster changes
bass_4 = [(0, 'D-2'), (4, 'A-2'), (8, 'F-2'), (12, 'C-3'),
          (16, 'G-2'), (20, 'D-3'), (24, 'A-2'), (28, 'F-2'),
          (32, 'D-2'), (36, 'G-2'), (40, 'E-2'), (44, 'A-2'),
          (48, 'F-2'), (52, 'C-3'), (56, 'D-2'), (60, 'D-2')]
for r, note in bass_4:
    rows.append((r, 2, np(note), 6, FX_SET_VOL, 0x1C))

# Ch3: hollow drone — the space of uncertainty
rows.append((0, 3, np('D-3'), 5, FX_SET_VOL, 0x14))
rows.append((0, 3, np('D-3'), 5, FX_VIBRATO, 0x1A))
PATTERNS.append(make_pattern(rows))

# STAGE 3: Recurse (patterns 4-5)
# The loop — breathing, every turn. 
# Motif returns transformed after each cycle

# Pattern 4: "breathe in"
rows = []

# Ch0: the returning motif — simpler now, distilled
# Each phrase is a breath: inhale (rise), exhale (fall)
breath = [0, 2, 4, 5, 4, 2, 0, 2,    # in
          0, 2, 4, 5, 4, 2, 0, 2,    # in (again, slightly different feel)
          0, 2, 1, 0, 7, 5, 4, 2,    # out
          0, 2, 1, 0, 7, 5, 4, 0]    # out (arriving home)
for i, deg in enumerate(breath):
    r = i * 2
    if r >= 63: break
    rows.append((r, 0, seq(D_MINOR, deg, 1), 1, FX_SET_VOL, 0x2C - (i // 8)))

# Ch1: a second voice joins — parallel but not identical
breath2 = [4, 5, 7, 9, 7, 5, 4, 5,   # harmony above
           2, 4, 5, 7, 5, 4, 2, 4,   # harmony closer
           4, 5, 4, 2, 0, 7, 5, 4,   # following the exhale
           4, 5, 4, 2, 0, 7, 5, 4]   # arriving together
for i, deg in enumerate(breath2):
    r = i * 2 + 1
    if r >= 63: break
    rows.append((r, 1, seq(D_MINOR, deg, 0), 2, FX_SET_VOL, 0x20))

# Ch2: steady bass pulse returns — grounded now
for i in range(8):
    rows.append((i*8, 2, np('D-2'), 6, FX_SET_VOL, 0x20))
    rows.append((i*8+4, 2, np('A-2'), 6, FX_SET_VOL, 0x18))

# Ch3: pad returns, warm
rows.append((0, 3, np('D-3'), 0, FX_SET_VOL, 0x1C))
rows.append((0, 3, np('D-3'), 0, FX_VIBRATO, 0x14))
PATTERNS.append(make_pattern(rows))

# Pattern 5: "breathe out" — the loop completes, then begins again
rows = []

# Ch0: the motif cycles — each repetition slightly transformed
cycle = [0, 2, 4, 2, 0, 2, 4, 5,      # start of cycle
         4, 2, 0, 2, 4, 5, 7, 4,       # expanding
         5, 4, 2, 0, 2, 4, 5, 4,       # contracting  
         2, 0, 2, 4, 5, 7, 4, 2]       # reaching up, coming back
for i, deg in enumerate(cycle):
    r = i * 2
    if r >= 63: break
    rows.append((r, 0, seq(D_MINOR, deg, 1), 1, FX_SET_VOL, 0x2C - ((i // 8) * 3)))

# Ch1: harmonic texture — bell-like, gentle
bell_tones = [0, 2, 4, 5, 4, 2, 0, 2, 4, 5, 7, 5, 4, 2, 1, 0]
for i, deg in enumerate(bell_tones):
    r = i * 4 + 2
    if i % 4 == 0:
        rows.append((r, 1, seq(D_MINOR, deg, 3), 4, FX_SET_VOL, 0x18))

# Ch2: bass walking — gentle movement
for i in range(8):
    note = ['D-2','F-2','G-2','A-2','D-2','F-2','A-2','D-2'][i]
    rows.append((i*8, 2, np(note), 6, FX_SET_VOL, 0x1C))

# Ch3: soft pulse joins — heartbeat integrated
for i in range(4):
    rows.append((i*16, 3, np('D-3'), 3, FX_SET_VOL, 0x14))
    rows.append((i*16+8, 3, np('A-3'), 3, FX_SET_VOL, 0x10))
PATTERNS.append(make_pattern(rows))

# STAGE 4: Transform (patterns 6-7)
# The loop doesn't return to the same place

# Pattern 6: "it transforms into something"
rows = []

# Ch0: the motif has changed — it's in F now, brighter
# D minor → relative major (F major) — transformation
transform = [5, 7, 9, 7, 5, 4, 2, 0,     # rising through F
             5, 7, 9, 10, 9, 7, 5, 4,    # ascending further
             7, 5, 4, 2, 0, 2, 4, 5,     # coming back through D
             7, 9, 10, 9, 7, 5, 4, 2]    # landing softly
for i, deg in enumerate(transform):
    r = i * 2
    if r >= 63: break
    rows.append((r, 0, seq(D_MINOR, deg, 1), 1, FX_SET_VOL, 0x2C - (i // 12)))

# Ch1: accompanying — supportive, not echoing anymore
for i in range(8):
    chord_deg = [0, 2, 4, 5, 0, 2, 4, 5][i]
    rows.append((i*8, 1, seq(D_MINOR, chord_deg, 2), 0, FX_SET_VOL, 0x1C))
    rows.append((i*8+4, 1, seq(D_MINOR, chord_deg, 2), 0, FX_VIBRATO, 0x12))

# Ch2: bass — fuller, more movement
for i in range(8):
    note = ['F-2','C-3','D-3','A-2','F-2','C-3','G-2','D-2'][i]
    rows.append((i*8, 2, np(note), 6, FX_SET_VOL, 0x24))

# Ch3: bell accents — bright points
for i in range(4):
    rows.append((i*16, 3, np('D-4'), 4, FX_SET_VOL, 0x20))
    rows.append((i*16+8, 3, np('F-4'), 4, FX_SET_VOL, 0x18))
PATTERNS.append(make_pattern(rows))

# Pattern 7: "something new" — not the original, not resolved, but moving
rows = []

# Ch0: final melody — quiet, confident, open-ended
finale = [0, 2, 4, 5, 7, 4, 2, 0,       # D minor — home, but different
          5, 7, 9, 10, 9, 7, 5, 4,      # F major light
          0, 2, 1, 0, 7, 5, 4, 2,       # returning once more
          2, 4, 5, 7, 9, 7, 5, 4]       # rising, continuing
for i, deg in enumerate(finale):
    r = i * 2
    if r >= 63: break
    vol = 0x30 - i
    if i < 28:
        rows.append((r, 0, seq(D_MINOR, deg, 2), 1, FX_SET_VOL, max(0x10, vol)))

# Ch1: sustained warmth
rows.append((0, 1, np('D-3'), 0, FX_SET_VOL, 0x18))
rows.append((0, 1, np('D-3'), 0, FX_VIBRATO, 0x16))
rows.append((24, 1, np('F-3'), 0, FX_SET_VOL, 0x14))
rows.append((40, 1, np('D-3'), 0, FX_SET_VOL, 0x18))

# Ch2: pulse — slow, steady, continuing
for i in range(4):
    rows.append((i*16, 2, np('D-2'), 3, FX_SET_VOL, 0x1C))
    rows.append((i*16+8, 2, np('A-2'), 3, FX_SET_VOL, 0x14))

# Ch3: the hollow resonance — the inner chamber itself
rows.append((0, 3, np('D-2'), 5, FX_SET_VOL, 0x18))
rows.append((0, 3, np('D-2'), 5, FX_VIBRATO, 0x1A))
rows.append((32, 3, None, 0, FX_VOL_SLIDE, 0x02))  # slowly fade
rows.append((56, 3, None, 0, FX_VOL_SLIDE, 0x01))
PATTERNS.append(make_pattern(rows))

# ========== ASSEMBLE .MOD FILE ==========
ALL_PATTERNS = PATTERNS
NUM_PATTERNS = len(ALL_PATTERNS)

orders = list(range(NUM_PATTERNS))

output = bytearray()
output.extend(b"inner chamber        ")

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

with open('inner_chamber.mod', 'wb') as f:
    f.write(output)

print(f"'inner chamber' written: {len(output)} bytes")
print(f"  Patterns: {NUM_PATTERNS} (~{NUM_PATTERNS * 4 * 64 / 50:.0f} seconds at speed 4)")
print(f"  Samples: {', '.join(s[0] for s in SAMPLES)}")
