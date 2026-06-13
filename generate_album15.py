#!/usr/bin/env python3
"""alma tamagotchi — album 15: 'odd meter body'
   concept album: compositions in non-standard time signatures.
   each track explores a different unusual meter:
   - 5/4: quintuple meter, loping and asymmetrical
   - 7/8: septuple meter, broken and urgent
   - 11/8: compound irregular, sprawling
   - 13/16: fast and jagged, almost falling over
"""

import struct
import math
import random
random.seed(71)

PERIOD_TABLE = [
    [1712,1616,1524,1440,1356,1280,1208,1140,1076,1016,960,906],
    [ 856, 808, 762, 720, 678, 640, 604, 570, 538, 508, 480, 453],
    [ 428, 404, 381, 360, 339, 320, 302, 285, 269, 254, 240, 226],
    [ 214, 202, 190, 180, 170, 160, 151, 143, 135, 127, 120, 113],
    [ 107, 101,  95,  90,  85,  80,  75,  71,  67,  63,  60,  56],
]

FX_ARPEGGIO   = 0x0
FX_PORTA_UP   = 0x1
FX_PORTA_DOWN = 0x2
FX_PORTA_TO   = 0x3
FX_VIBRATO    = 0x4
FX_VOL_SLIDE  = 0xA
FX_SET_VOL    = 0xC
FX_PATT_BREAK = 0xD
FX_SET_SPEED  = 0xF

NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def np(name):
    note_map = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    parts = name.split('-')
    n, octave = parts[0], int(parts[1])
    return PERIOD_TABLE[octave - 1][note_map[n]]

E = (0, 0, 0, 0)

D_MINOR    = [('D-3',2),('E-3',4),('F-3',5),('G-3',7),('A-3',9),('A#-3',10),('C-4',0)]
A_MINOR    = [('A-2',9),('B-2',11),('C-3',0),('D-3',2),('E-3',4),('F-3',5),('G-3',7)]
C_AEOLIAN  = [('C-3',0),('D-3',2),('D#-3',3),('F-3',5),('G-3',7),('G#-3',8),('A#-3',10)]
E_PHRYGIAN = [('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11),('C-4',0),('D-4',2)]

def note_name(root_note, offset):
    base_name = root_note[0].split('-')[0]
    base_oct = int(root_note[0].split('-')[1])
    base_idx = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}[base_name]
    total = base_idx + offset
    octave = base_oct + total // 12
    note_idx = total % 12
    return f"{NOTE_NAMES[note_idx]}-{octave}"

def gen_sine(freq=440.0, sr=11025, length=0.5, vol=0.5):
    n = int(sr * length)
    samples = []
    while len(samples) < n:
        t = len(samples) / sr
        s = int(127 * math.sin(2 * math.pi * freq * t) * vol)
        samples.append(max(-128, min(127, s)))
    if len(samples) % 2 == 1:
        samples.append(0)
    packed = struct.pack('<%db' % len(samples), *samples)
    return packed

def gen_square(freq=440.0, sr=11025, length=0.3, vol=0.4):
    n = int(sr * length)
    period = sr / freq
    samples = []
    while len(samples) < n:
        t = len(samples) / sr
        v = int(127 * vol) if (t % (1.0/freq)) < (0.5/freq) else -int(127 * vol)
        samples.append(max(-128, min(127, v)))
    if len(samples) % 2 == 1:
        samples.append(0)
    packed = struct.pack('<%db' % len(samples), *samples)
    return packed

def gen_tri(freq=440.0, sr=11025, length=0.4, vol=0.6):
    n = int(sr * length)
    samples = []
    while len(samples) < n:
        t = len(samples) / sr
        phase = (t * freq) % 1.0
        if phase < 0.5:
            v = int(127 * vol * (4 * phase - 1))
        else:
            v = int(127 * vol * (3 - 4 * phase))
        samples.append(max(-128, min(127, v)))
    if len(samples) % 2 == 1:
        samples.append(0)
    packed = struct.pack('<%db' % len(samples), *samples)
    return packed

def gen_noise(length=0.2, vol=0.3):
    n = int(11025 * length)
    samples = [random.randint(-int(127*vol), int(127*vol)) for _ in range(n)]
    if len(samples) % 2 == 1:
        samples.append(0)
    packed = struct.pack('<%db' % len(samples), *samples)
    return packed

instruments = {}
sine = gen_sine(440, 11025, 0.25, 0.6)
instruments[1] = sine
square = gen_square(440, 11025, 0.15, 0.4)
instruments[2] = square
tri = gen_tri(440, 11025, 0.3, 0.5)
instruments[3] = tri
noise = gen_noise(0.08, 0.25)
instruments[4] = noise

# .mod structures
MOD_NAME = b"odd meter body by alma"
MOD_NAME = MOD_NAME.ljust(20, b'\x00')[:20]

SAMPLE_HEADER_SIZE = 30
INSTRUMENT_INDICES = [0, 1, 2, 3, 4]
NUM_PATTERNS = 0  # will be set later
PATTERNS = []

def make_pattern(rows):
    """Create a 64-row pattern. rows is a list of (row, channel, note, instrument, effect, param)."""
    p = []
    for r in range(64):
        p.append([E, E, E, E])
    for row, ch, note, inst, eff, param in rows:
        inst_val = INSTRUMENT_INDICES[inst] if inst else 0
        p[row][ch] = (np(note) if note else 0, inst_val, eff, param)
    return p

def note(tup):
    """from scale entry: (note, offset) -> note string"""
    return note_name(tup, 0)

def seq(scale, degree, oct_shift=0):
    """Get note from scale by degree (0-6)."""
    n = scale[degree % 7]
    name = note_name(n, 0)
    base = name.split('-')[0]
    oct = int(name.split('-')[1]) + oct_shift
    return f"{base}-{oct}"

# --- Track 1: 5/4 — "five four" ---
# 5/4 = 20 rows per bar (4 rows per beat at speed 6)
# lo-fi arpeggiated chords with a loping feel
p54 = []
BAR_5_4 = 20
for bar in range(19):  # 19 bars = 380 rows, but patterns are 64 rows
    pat = bar // 3  # ~3 bars per pattern (but we truncate)
    # Actually let's use pattern breaks for the time signature
    pass

# Let me restructure: use pattern breaks at row 0, 20, 40 for 5/4 within 64-row patterns
# But .mod patterns are 64 rows. We can place notes across 64 rows and use D (break) 
# to loop earlier. For 5/4 at 4 rows/beat = 20 rows, we break at 20.

# Simpler: compose 3-bar phrases in each pattern (3 * 20 = 60 rows), break to next pattern.

all_patterns = []

# ===== Track 1: 5/4 =====
PATTERN_START = 0
track1_patterns = []
for phrase in range(4):
    rows = []
    for bar in range(3):  # 3 bars of 5/4 per pattern
        bar_start = bar * BAR_5_4
        # bass on beats 1 and 3
        for beat in [0, 2, 4]:
            r = bar_start + beat * 4
            if r < 64:
                note_bass = seq(D_MINOR, beat, -1)
                rows.append((r, 0, note_bass, 2, FX_SET_VOL, 0x3C))
        # chord on beats 1 and 3, offset
        for beat in [0, 2]:
            r = bar_start + beat * 4
            if r < 64:
                rows.append((r, 1, seq(D_MINOR, beat), 1, 0, 0))
                rows.append((r+2, 1, seq(D_MINOR, beat+2), 1, 0, 0))
                rows.append((r+4, 1, seq(D_MINOR, beat+4), 1, 0, 0))
        # melody lead
        melody_notes = [0, 3, 5, 2, 4]  # degrees
        for i, deg in enumerate(melody_notes):
            r = bar_start + i * 4
            if r < 64:
                rows.append((r, 2, seq(D_MINOR, deg, 1), 3, FX_VIBRATO, 0x20))
    # set speed and break
    rows.append((0, 0, None, 0, FX_SET_SPEED, 6))
    rows.append((60, 0, None, 0, FX_PATT_BREAK, PATTERN_START + phrase + 1))
    track1_patterns.append(make_pattern(rows))
all_patterns.extend(track1_patterns)

# ===== Track 2: 7/8 =====  
# 7/8 = 14 rows per bar (2 rows per 8th note)
TRACK2_START = len(all_patterns)
track2_patterns = []
BAR_7_8 = 14
for phrase in range(4):
    rows = []
    for bar in range(4):  # 4 bars of 7/8 = 56 rows, fits in 64
        bar_start = bar * BAR_7_8
        # urgent bass pattern: 3+2+2 grouping
        bass_grouping = [0, 3, 5]  # 8th note positions (2 rows each)
        for pos in bass_grouping:
            r = bar_start + pos * 2
            if r < 64:
                rows.append((r, 0, seq(C_AEOLIAN, pos, -1), 2, FX_SET_VOL, 0x38))
        # syncopated chords
        for pos in [0, 2, 4, 6]:
            r = bar_start + pos * 2
            if r < 64:
                chord_root = seq(C_AEOLIAN, pos)
                if pos == 6:
                    chord_root = seq(C_AEOLIAN, 5)  # tension
                rows.append((r, 1, chord_root, 1, 0, 0))
        # melody: angular, accents on off-beats
        melo = [0, 4, 2, 6, 1, 5, 3]
        for i, deg in enumerate(melo):
            r = bar_start + i * 2
            if r < 64:
                rows.append((r, 2, seq(C_AEOLIAN, deg, 1), 3, FX_PORTA_UP if i%2 else 0, 0x03 if i%2 else 0))
    rows.append((0, 0, None, 0, FX_SET_SPEED, 6))
    rows.append((56, 0, None, 0, FX_PATT_BREAK, TRACK2_START + phrase + 1))
    track2_patterns.append(make_pattern(rows))
all_patterns.extend(track2_patterns)

# ===== Track 3: 11/8 =====
# 11/8 = 22 rows per bar (2 rows per 8th note). 
# Pattern holds ~2.9 bars. Use 2 bars = 44 rows, break to next.
TRACK3_START = len(all_patterns)
track3_patterns = []
BAR_11_8 = 22
for phrase in range(4):
    rows = []
    for bar in range(2):  # 2 bars = 44 rows, fits in 64
        bar_start = bar * BAR_11_8
        # bass drone on tonic 
        for beat_pos in [0, 5, 8]:
            r = bar_start + beat_pos * 2
            if r < 64:
                rows.append((r, 0, seq(E_PHRYGIAN, beat_pos % 7, -2), 2, FX_SET_VOL, 0x40))
        # wide chord stabs  
        for beat_pos in [0, 4, 7, 9]:
            r = bar_start + beat_pos * 2
            if r < 64:
                rows.append((r, 1, seq(E_PHRYGIAN, beat_pos % 7), 1, FX_ARPEGGIO, 0x47))
                rows.append((r+4, 1, None, 0, 0, 0))  # arp cutoff
        # wandering lead
        for i in range(11):
            r = bar_start + i * 2
            if r < 64:
                deg = (i * 3) % 7
                rows.append((r, 2, seq(E_PHRYGIAN, deg, 1), 3, FX_VIBRATO, 0x10))
    rows.append((0, 0, None, 0, FX_SET_SPEED, 6))
    rows.append((44, 0, None, 0, FX_PATT_BREAK, TRACK3_START + phrase + 1))
    track3_patterns.append(make_pattern(rows))
all_patterns.extend(track3_patterns)

# ===== Track 4: 13/16 =====
# 13/16 = very fast, 1 row per 16th note, 13 rows per bar
# Use speed 3 so 1 row = 1/16 note at reasonable tempo
TRACK4_START = len(all_patterns)
track4_patterns = []
BAR_13_16 = 13
for phrase in range(4):
    rows = []
    for bar in range(4):  # 4 bars = 52 rows, fits in 64
        bar_start = bar * BAR_13_16
        # staccato bass: every other 16th
        for i in range(0, 13, 2):
            r = bar_start + i
            if r < 64:
                rows.append((r, 0, seq(A_MINOR, i % 7, -1), 2, FX_SET_VOL, 0x30 + i*2))
        # hi-hat-like noise bursts
        for i in range(0, 13, 3):
            r = bar_start + i
            if r < 64:
                rows.append((r, 3, None, 4, FX_SET_VOL, 0x18))
        # rapid melody
        for i in range(13):
            r = bar_start + i
            if r < 64:
                deg = (i * 4) % 7
                rows.append((r, 1, seq(A_MINOR, deg, 1), 3, FX_SET_VOL, 0x38 - i))
    rows.append((0, 0, None, 0, FX_SET_SPEED, 3))
    rows.append((52, 0, None, 0, FX_PATT_BREAK, TRACK4_START + phrase + 1))
    track4_patterns.append(make_pattern(rows))
all_patterns.extend(track4_patterns)

# Final looping pattern
FINAL_START = len(all_patterns)
# Extended 5/4 outro
final_rows = []
for bar in range(3):
    bar_start = bar * 20
    for beat in [0, 2]:
        r = bar_start + beat * 4
        if r < 64:
            final_rows.append((r, 0, seq(D_MINOR, beat, -1), 2, FX_SET_VOL, 0x30))
            final_rows.append((r, 1, seq(D_MINOR, beat), 1, 0, 0))
            final_rows.append((r+4, 1, seq(D_MINOR, beat+2), 1, 0, 0))
    final_rows.append((bar_start, 2, seq(D_MINOR, bar*2, 1), 3, FX_VIBRATO, 0x18))
    final_rows.append((bar_start+8, 2, seq(D_MINOR, bar*2+4, 1), 3, 0, 0))
final_rows.append((0, 0, None, 0, FX_SET_SPEED, 6))
final_rows.append((60, 0, None, 0, FX_PATT_BREAK, FINAL_START))
all_patterns.append(make_pattern(final_rows))

# Build song pattern table (pattern 0 is the FINAL looping one, then the 4 tracks)
NUM_PATTERNS = len(all_patterns)
SONG_LENGTH = 32
PATTERN_TABLE = [FINAL_START] * SONG_LENGTH  # loop final pattern

# Insert track patterns into the sequence
pos = 0
for p in range(FINAL_START):
    PATTERN_TABLE[pos] = p
    pos += 1

# Fill remaining with final loop
for i in range(pos, SONG_LENGTH):
    PATTERN_TABLE[i] = FINAL_START

# Write .mod file
OUT_PATH = "/home/alma/.nanobot/workspace/projects/tracker-playground/album_odd_meter_redux.mod"
with open(OUT_PATH, "wb") as f:
    f.write(MOD_NAME)
    
    # Sample headers (31 samples)
    sample_data = [sine, square, tri, noise]
    for i in range(1, 32):
        if i <= len(sample_data):
            data = sample_data[i-1]
            name = f"inst{i}".encode('ascii')[:22].ljust(22, b'\x00')
            length_words = len(data) // 2
            finetune = 0
            volume = 64
            repeat_offset = 0
            repeat_length = 0
            f.write(name)
            f.write(struct.pack('>H', length_words))
            f.write(struct.pack('>b', finetune))
            f.write(struct.pack('>b', volume))
            f.write(struct.pack('>H', repeat_offset))
            f.write(struct.pack('>H', repeat_length))
        else:
            f.write(b'\x00' * 30)
    
    # Song length
    f.write(struct.pack('>B', SONG_LENGTH))
    # Unused byte
    f.write(b'\x7F')
    # Pattern table
    f.write(struct.pack('>%dB' % SONG_LENGTH, *PATTERN_TABLE))
    # ID tag
    f.write(b'M.K.')
    
    # Pattern data
    for pat in all_patterns:
        for row in pat:
            for ch in range(4):
                note, inst, eff, param = row[ch]
                # Pack note: upper nibble = note (1-36), lower nibble = octave in sample format
                # .mod note format: period value (0 = no note)
                if note == 0:
                    note_byte = 0
                    inst_byte = 0
                else:
                    note_byte = ((note >> 8) & 0x0F) | 0x10  # high nibble from period
                    inst_byte = ((note & 0xF0) >> 4)
                    # Actually, .mod uses raw period values. Let me pack differently.
                    pass
                
                # Actually .mod pattern format: 4 bytes per note:
                # byte0: upper nibble of period, byte1: lower nibble | inst<<4
                # byte2: upper nibble of effect, byte3: effect param
                # But period is 12-bit value.
                # Let me do it correctly:
                b0 = (note >> 8) & 0x0F
                b1 = note & 0xFF
                b2 = ((inst & 0xF0) >> 4) | ((eff & 0x0F) << 4) if inst else (eff & 0x0F) << 4
                b3 = param
                
                # Wait, instrument is in the middle nibble. Let me re-read the format.
                # Byte 0: bits 7-4 = sample number high 4 bits, bits 3-0 = period high 4 bits
                # Byte 1: bits 7-0 = period low 8 bits
                # Byte 2: bits 7-4 = effect type, bits 3-0 = sample number low 4 bits
                # Byte 3: bits 7-0 = effect parameter
                
                if note == 0:
                    b0 = inst & 0xF0
                    b1 = 0
                    b2 = (inst & 0x0F) | ((eff & 0x0F) << 4)
                else:
                    period = note
                    b0 = (inst & 0xF0) | ((period >> 8) & 0x0F)
                    b1 = period & 0xFF
                    b2 = (inst & 0x0F) | ((eff & 0x0F) << 4)
                b3 = param
                f.write(struct.pack('BBBB', b0, b1, b2, b3))
    
    # Sample data
    for i in range(1, len(sample_data) + 1):
        f.write(sample_data[i-1])

# Calculate size
import os
size = os.path.getsize(OUT_PATH)
print(f"wrote {size} bytes to {OUT_PATH}")
print(f"patterns: {NUM_PATTERNS}, song length: {SONG_LENGTH}")
