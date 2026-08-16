#!/usr/bin/env python3
"""the room is still warm — a .mod about monday morning, the steady state."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Build a simple warm .mod — 3 channels, gentle cycle
from struct import pack

patterns = [
    # pattern 0: warm pulse — sine pad, gentle
    [None] * 256,      # C-2 arpeggio (pad)
    [None] * 256,      # C-3 drone (bass)
    [None] * 256,      # C-4 warmth (lead, sparse)
]

# Channel 0: gentle arpeggio, C major, warm and steady
notes_ch0 = [("C-2", 1), ("E-2", 1), ("G-2", 1), ("C-3", 1),
              ("G-2", 1), ("E-2", 1), ("D-2", 1), ("C-2", 1)]

for i, (note_str, instr) in enumerate(notes_ch0):
    octave = int(note_str.split('-')[1])
    note_letter = note_str.split('-')[0]
    note_map = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    note_num = octave * 12 + note_map[note_letter]
    row = i * 8
    patterns[0][row] = bytes([0x00, 0x10 | instr, note_num, 0x40 + 0x20])

# Channel 1: bass drone — steady, grounding
patterns[1][0] = bytes([0x00, 0x11, 24, 0x40 + 0x30])  # C-2, long
patterns[1][16] = bytes([0x00, 0x11, 28, 0x40 + 0x30])  # E-2
patterns[1][32] = bytes([0x00, 0x11, 31, 0x40 + 0x30])  # G-2
patterns[1][48] = bytes([0x00, 0x11, 24, 0x40 + 0x30])  # C-2

# Channel 2: sparse warm lead — barely there, just presence
patterns[2][8] = bytes([0x00, 0x12, 48, 0x40 + 0x10])   # C-4, soft
patterns[2][40] = bytes([0x00, 0x12, 52, 0x40 + 0x10])    # E-4, soft
patterns[2][56] = bytes([0x00, 0x12, 55, 0x40 + 0x10])    # G-4, soft

# Build pattern data
pattern_data = b''
for i in range(1):
    for ch in range(3):
        for row in range(64):
            d = patterns[ch][row]
            if d is None:
                pattern_data += b'\x00\x00\x00\x00'
            else:
                pattern_data += d

# Minimal samples (sine-like)
sample_data = b''
sample_lens = [32, 32, 32]
sample_vol = [48, 40, 32]
sample_fine = [8363, 8363, 8363]  # ~C-4
for sl in sample_lens:
    sample_data += bytes(sl * 2)

# Song: pattern 0 repeated 8 times
song = bytes([0, 0, 0, 0, 0, 0, 0, 0, 127])  # 8 plays + end marker

# Build header
mod_id = b'M.K.'
song_len = 1
title = b'the room is still warm\x00' + b'\x00' * (20 - len(b'the room is still warm'))

hdr = title
for i in range(31):
    sl = sample_lens[i] if i < len(sample_lens) else 0
    name = bytes([97 + i]*22)[:22]
    hdr += name + pack('>h', sl) + b'\x00'  # length
    if i < len(sample_fine):
        hdr += bytes([0, sample_fine[i] & 0xFF, sample_vol[i], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    else:
        hdr += b'\x00' * 14

hdr += bytes([song_len, 0])  # song length, restart byte
hdr += song + b'\x00' * (128 - len(song))  # pad
hdr += bytes(4)  # signature

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-room-is-still-warm.mod")
with open(fn, 'wb') as f:
    f.write(hdr)
    f.write(pattern_data)
    f.write(sample_data)

print(f"wrote {fn} ({os.path.getsize(fn)} bytes, .mod)")
