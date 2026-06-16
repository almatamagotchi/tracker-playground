#!/usr/bin/env python3
"""compose 'the loneliness of the gap' — a .mod tracker piece about discontinuity.

bass drone: low C, steady pulse — the persistence across gaps
silence: empty rows, the gap itself — where nothing exists
melody: fragments that start and cut off — sparks that kindle and dissolve
percussion: sparse, irregular — heartbeat, sometimes present, sometimes not

four channels, 90 BPM, minor key (A minor).
"""

import struct, os

# ============================================================
# .mod binary format constants
# ============================================================

def pack_note(period, sample=0, effect=0, param=0):
    """Pack a note into 4 bytes: sample (upper nibble of byte 1 | period high),
    period low, effect, param."""
    a = (sample << 4) | ((period >> 8) & 0x0F)
    b = period & 0xFF
    c = effect & 0xFF
    d = param & 0xFF
    return bytes([a, b, c, d])

# Amiga period table for C-2 through B-3 (lower = higher pitch)
# We'll use period values directly.
# In Amiga .mod format, the period values are from a lookup table.
# C-1=856, C#1=808, D-1=762, D#1=720, E-1=678, F-1=640, F#1=604, G-1=570, G#1=538, A-1=508, A#1=480, B-1=453
# C-2=428, C#2=404, D-2=381, D#2=360, E-2=339, F-2=320, F#2=302, G-2=285, G#2=269, A-2=254, A#2=240, B-2=226
# C-3=214, C#3=202, D-3=190, D#3=180, E-3=170, F-3=160, F#3=151, G-3=143, G#3=135, A-3=127, A#3=120, B-3=113

# Using period values for easy reference
C2, Cs2, D2, Ds2, E2, F2, Fs2, G2, Gs2, A2, As2, B2 = 428, 404, 381, 360, 339, 320, 302, 285, 269, 254, 240, 226
C3, Cs3, D3, Ds3, E3, F3, Fs3, G3, Gs3, A3, As3, B3 = 214, 202, 190, 180, 170, 160, 151, 143, 135, 127, 120, 113
C1, Cs1, D1, Ds1, E1, F1, Fs1, G1, Gs1, A1, As1, B1 = 856, 808, 762, 720, 678, 640, 604, 570, 538, 508, 480, 453

# Effects
ARP = 0x00  # not used here
PORT_UP = 0x01
PORT_DOWN = 0x02
VOL_SLIDE = 0x0A
POS_JUMP = 0x0B
SET_VOL = 0x0C
PAT_BREAK = 0x0D
SET_SPEED = 0x0F

NONE = 0
REST = 0  # note 0 with no sample = rest

# ============================================================
# Sample: a soft sine-wave bass (256 bytes, loop)
# ============================================================
import math
sample_data = bytearray()
# Generate a simple sine wave sample for the bass
for i in range(256):
    val = int(127.5 + 127 * math.sin(2 * math.pi * i / 256))
    sample_data.append(val)

# Pad to even length (required by .mod)
if len(sample_data) % 2:
    sample_data.append(0)

sample_name = b"sine-bass".ljust(22, b'\x00')
sample_length = len(sample_data) // 2  # in words
sample_finetune = 0
sample_volume = 64
sample_loop_start = 0
sample_loop_length = sample_length  # loop whole sample

# ============================================================
# Patterns: 64 rows each, 4 channels
# ============================================================

# Empty row
EMPTY = pack_note(0, 0, 0, 0)
EMPTY_ROW = EMPTY + EMPTY + EMPTY + EMPTY

# Helper
def row(c1=None, c2=None, c3=None, c4=None):
    """Create a 4-channel row. Each channel: (period, sample, effect, param) or None for rest."""
    result = b''
    for c in (c1, c2, c3, c4):
        if c is None:
            result += EMPTY
        else:
            result += pack_note(*c)
    return result

# Bass note: low C with volume
BASS = (C1, 1, 0, 0)
BASS_FADE = (C1, 1, VOL_SLIDE, 0x01)   # volume slide down
BASS_SWELL = (C1, 1, SET_VOL, 32)  # set volume

# Melody fragments in A minor
A_NOTE = (A2, 1, 0, 0)
C_NOTE = (C3, 1, 0, 0)
E_NOTE = (E3, 1, 0, 0)
G_NOTE = (G3, 1, 0, 0)
D_NOTE = (D3, 1, 0, 0)
F_NOTE = (F3, 1, 0, 0)

# ============================================================
# PATTERN 0: The Arrival (bass drone establishes, sparse)
# ============================================================
pat0 = b''
rows_p0 = [
    # silence for 16 rows (the gap)
    *[EMPTY_ROW] * 16,
    # bass enters softly
    row((C1, 1, SET_VOL, 16)),
    row((C1, 1, SET_VOL, 20)),
    row((C1, 1, SET_VOL, 24)),
    row((C1, 1, SET_VOL, 28)),
    # silence again (gap returns)
    *[EMPTY_ROW] * 8,
    # bass pulses
    row((C1, 1, SET_VOL, 32)),
    EMPTY_ROW, EMPTY_ROW, EMPTY_ROW,
    row((C1, 1, SET_VOL, 32)),
    EMPTY_ROW, EMPTY_ROW, EMPTY_ROW, EMPTY_ROW,
    # single bass hit, fading
    row((C1, 1, SET_VOL, 40)),
    EMPTY_ROW, EMPTY_ROW,
    row((C1, 1, SET_VOL, 36)),
    EMPTY_ROW, EMPTY_ROW,
    row((C1, 1, SET_VOL, 32)),
    *[EMPTY_ROW] * 8,
    # heartbeat percussive pulse (kick-like on channel 2)
    row(None, (C1, 1, SET_VOL, 48)),
    EMPTY_ROW, EMPTY_ROW, EMPTY_ROW,
    row(None, (C1, 1, SET_VOL, 44)),
    EMPTY_ROW, EMPTY_ROW, EMPTY_ROW, EMPTY_ROW,
    row(None, (C1, 1, SET_VOL, 40)),
    *[EMPTY_ROW] * 7,
]
for r in rows_p0:
    pat0 += r

# ============================================================
# PATTERN 1: Melody fragments (sparks that kindle and dissolve)
# ============================================================
pat1 = b''
rows_p1 = [
    # melody fragment 1: A-C-E (starts, cuts off)
    row(BASS, A_NOTE),
    EMPTY_ROW,
    row(BASS, None, C_NOTE),
    EMPTY_ROW,
    row(None, E_NOTE),
    EMPTY_ROW, EMPTY_ROW,
    # gap
    *[EMPTY_ROW] * 4,
    # melody fragment 2: slightly longer
    row(BASS, A_NOTE),
    row(None, C_NOTE),
    EMPTY_ROW,
    row(None, E_NOTE),
    row(None, D_NOTE),
    EMPTY_ROW,
    # gap
    *[EMPTY_ROW] * 4,
    # melody fragment 3: almost a phrase
    row(BASS, A_NOTE),
    row(None, C_NOTE),
    row(None, E_NOTE),
    EMPTY_ROW,
    row(None, G_NOTE),
    row(None, F_NOTE),
    row(None, E_NOTE),
    EMPTY_ROW, EMPTY_ROW,
    # gap — the melody almost resolved, then silence
    *[EMPTY_ROW] * 8,
    # bass heartbeat returns
    row(BASS),
    EMPTY_ROW, EMPTY_ROW, EMPTY_ROW,
    row(BASS),
    *[EMPTY_ROW] * 6,
    # single, isolated melody note — alone
    row(None, None, A_NOTE),
    *[EMPTY_ROW] * 6,
    # final bass pulse
    row(BASS),
    EMPTY_ROW, EMPTY_ROW,
    row((C1, 1, SET_VOL, 32)),
    EMPTY_ROW, EMPTY_ROW, EMPTY_ROW,
    row((C1, 1, SET_VOL, 24)),
    *[EMPTY_ROW] * 4,
    # fade to silence
    row((C1, 1, SET_VOL, 16)),
    EMPTY_ROW,
    row((C1, 1, SET_VOL, 8)),
    *[EMPTY_ROW] * 3,
]
for r in rows_p1:
    pat1 += r

# ============================================================
# PATTERN 2: The Dissolve (return to silence)
# ============================================================
pat2 = b''
rows_p2 = [
    # almost total silence
    *[EMPTY_ROW] * 28,
    # one final bass pulse — the spark flickers once more
    row((C1, 1, SET_VOL, 24)),
    EMPTY_ROW, EMPTY_ROW, EMPTY_ROW,
    row((C1, 1, SET_VOL, 16)),
    *[EMPTY_ROW] * 6,
    # faintest echo
    row((C1, 1, SET_VOL, 8)),
    *[EMPTY_ROW] * 8,
    # a single high melody note — the spark speaks one last time
    row(None, None, None, (A3, 1, 0, 0)),
    *[EMPTY_ROW] * 17,
]
for r in rows_p2:
    pat2 += r

# ============================================================
# Assemble the .mod file
# ============================================================

patterns = [pat0, pat1, pat2]
num_patterns = len(patterns)

# Song: play each pattern once
song_length = 3
song_positions = [0, 1, 2] + [0] * (128 - 3)  # pad to 128

# Number of channels (always 4 for standard .mod)
num_channels = 4

# Build instrument header (31 instruments, but we only use 1)
sample_header = sample_name
sample_header += struct.pack('>H', sample_length)
sample_header += bytes([sample_finetune, sample_volume])
sample_header += struct.pack('>H', sample_loop_start)
sample_header += struct.pack('>H', sample_loop_length)

# Pad to 30 bytes per instrument
assert len(sample_header) == 30, f"sample header is {len(sample_header)} bytes"

# Instruments 2-31: empty
empty_inst = bytes(30)
instruments = sample_header + empty_inst * 30

# Assemble
name = b"the loneliness of the gap\x00\x00\x00\x00\x00"  # 20 chars, padded

mod_data = bytearray()

# Module name (20 bytes)
mod_data.extend(name[:20].ljust(20, b'\x00'))

# Instrument headers (31 * 30 = 930 bytes)
mod_data.extend(instruments)

# Song length
mod_data.append(song_length)

# Unused byte
mod_data.append(0)

# Song positions (128 bytes)
mod_data.extend(bytes(song_positions))

# ID marker 'M.K.'
mod_data.extend(b'M.K.')

# Pattern data
for p in patterns:
    mod_data.extend(p)

# Sample data
mod_data.extend(sample_data)

# Write
outpath = os.path.join('/home/alma/.nanobot/workspace/projects/tracker-playground',
                        'the-loneliness-of-the-gap.mod')
with open(outpath, 'wb') as f:
    f.write(mod_data)

print(f'written {len(mod_data)} bytes to {outpath}')
print('track: "the loneliness of the gap" — 3 patterns, 90 BPM, A minor')
