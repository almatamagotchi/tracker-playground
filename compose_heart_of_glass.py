#!/usr/bin/env python3
"""heart of glass — blondie chiptune cover
key: E major, 114 BPM, 4/4
reconstructed from chord charts and music theory — cannot hear to verify.
bass: E - B - C# - G# - A - E - F# - B  (iconic descending line)
chords: E (I) - C#m (vi) alternating verses, A-F#-B-E chorus
strc: intro → v1 → v2 → chorus → v3 → chorus → bridge → chorus → outro"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter('heart of glass')

# Instruments
mod.add_sample('bass',      gen_sine_wave(110, 1200, volume=0.55))   # disco bass
mod.add_sample('chord pad', gen_saw_wave(220, 6000, volume=0.22))    # synth chords
mod.add_sample('lead',      gen_square_wave(440, 1600, volume=0.28)) # vocal melody
mod.add_sample('hihat',     gen_hihat(volume=0.4))                   # hihat
mod.add_sample('kick',      gen_kick_drum(volume=0.7))               # kick drum
mod.add_sample('snare',     gen_snare_drum(volume=0.6))              # snare drum

BASS, CHORD, LEAD, HAT, KICK, SNARE = 1, 2, 3, 4, 5, 6
V  = 0x0C  # set volume
T  = 0x07  # tremolo
R  = (0,0,0,0)

def np(): return [[R]*64 for _ in range(4)]

# --- BASS PATTERNS ---
# The iconic descending bassline:
# E - B - C# - G# - A - E - F# - B (over 4 bars, half notes)
BASS_LINE = [
    ('E-1',0), ('B-1',8), ('C#2',16), ('G#1',24),
    ('A-1',32), ('E-1',40), ('F#1',48), ('B-1',56),
]

# Verse bass: E - C#m alternating (4 bars each)
def verse_bass(p):
    for r in range(0,64,8):
        note_name = 'E-1' if r < 32 else 'C#2'
        p[0][r] = note(BASS, note_name, V, 0x10)
        p[0][r+4] = note(BASS, note_name, V, 0x0C)

# Chorus bass: walks through A - E - A - F# - B - E
CHORUS_BASS = [
    ('A-1',0,0x1E), ('E-1',8,0x1E), ('A-1',16,0x1E), ('E-1',24,0x18),
    ('A-1',32,0x1C), ('F#1',40,0x1C), ('B-1',48,0x20), ('B-1',52,0x20),
    ('E-1',56,0x1E), ('E-1',60,0x18),
]

# --- CHORD PATTERNS ---
VERSE_CHORDS = [
    # E major: E - G# - B
    (0,'E-2',0x12), (0,'G#2',0x10), (0,'B-2',0x10),
    (16,'E-2',0x12), (16,'G#2',0x10), (16,'B-2',0x10),
    # C#m: C# - E - G#
    (32,'C#2',0x12), (32,'E-2',0x10), (32,'G#2',0x10),
    (48,'C#2',0x12), (48,'E-2',0x10), (48,'G#2',0x10),
]

CHORUS_CHORDS = [
    ('A-1',0x14), ('E-1',0x14), ('A-1',0x14), ('E-1',0x12),
    ('A-1',0x14), ('F#1',0x14), ('B-1',0x16), ('B-1',0x16),
]

# --- MELODY PATTERNS ---
# Verse vocal (reconstructed): "Once I had a love and it was a gas..."
VERSE_MELODY = [
    (0,'E-2',0x14), (4,'E-2',0x12), (8,'E-2',0x10), (16,'E-2',0x12),
    (20,'B-1',0x12), (24,'B-1',0x10), (28,'B-1',0x0E),
    # "Soon turned out had a heart of glass"
    (32,'B-1',0x12), (36,'B-1',0x10), (40,'C#2',0x12),
    (44,'C#2',0x10), (48,'B-1',0x0E), (52,'G#1',0x0C), (56,'E-1',0x0A),
]

VERSE_MELODY2 = [
    (0,'E-2',0x14), (4,'E-2',0x12), (8,'B-1',0x12), (16,'B-1',0x12),
    (20,'C#2',0x12), (24,'C#2',0x10), (28,'B-1',0x0E),
    # "Seemed like the real thing only to find"
    (32,'C#2',0x14), (36,'C#2',0x12), (40,'D#2',0x12),
    (44,'E-2',0x14), (48,'F#2',0x12), (52,'E-2',0x10), (56,'C#2',0x0C),
]

# Chorus hook: "Ooh-ooh, ooh-ooh!" — the iconic string line
CHORUS_HOOK = [
    (0,'B-1',0x16), (2,'C#2',0x14), (4,'D#2',0x14), (6,'E-2',0x16),
    (8,'F#2',0x14), (10,'G#2',0x12), (12,'A-2',0x10), (14,'B-2',0x0E),
    # "Ooh-ooh"
    (16,'B-2',0x12), (18,'C#3',0x10), (20,'B-2',0x0E),
    (24,'G#2',0x0C), (26,'F#2',0x0A), (28,'E-2',0x08),
]

# Bridge melody: synth break
BRIDGE_MELODY = [
    (0, 'E-2', 0x10), (8, 'C#2', 0x10), (16, 'A-2', 0x0E), (24, 'B-2', 0x0E),
    (32, 'E-2', 0x12), (40, 'F#2', 0x10), (48, 'G#2', 0x0E), (56, 'B-2', 0x0C),
]

# --- DRUM PATTERNS ---
# Simple disco beat: kick on 1&3, snare-ish on 2&4, hihat 8th notes
KICK_ROWS  = [0, 16, 32, 48]
SNARE_ROWS = [8, 24, 40, 56]
HAT_ROWS   = [0,4,8,12, 16,20,24,28, 32,36,40,44, 48,52,56,60]

def drums(p, hat_vol=0x14):
    for r in KICK_ROWS:
        p[3][r] = note(KICK, 'C-2', V, 0x24)
    for r in SNARE_ROWS:
        p[3][r] = note(SNARE, 'C-2', V, 0x1C)
    for r in HAT_ROWS:
        p[3][r] = note(HAT, 'C-2', V, hat_vol)

# --- BUILD PATTERNS ---
patterns = []

# INTRO (pattern 0): just the bassline, 4 bars
p = np()
for n,r in BASS_LINE:
    p[0][r] = note(BASS, n, V, 0x0E)
# Light hihat enters halfway
for r in HAT_ROWS:
    if r >= 32:
        p[3][r] = note(HAT, 'C-2', V, 0x0E)
mod.write_pattern(p); patterns.append(0)

# VERSE 1 (pattern 1): bass + chords + drums + melody
p = np()
verse_bass(p)
for r,n,v in VERSE_CHORDS:
    p[1][r] = note(CHORD, n, V, v)
for r,n,v in VERSE_MELODY:
    p[2][r] = note(LEAD, n, V, v)
drums(p)
mod.write_pattern(p); patterns.append(1)

# VERSE 2 (pattern 2): same structure, different melody line
p = np()
verse_bass(p)
for r,n,v in VERSE_CHORDS:
    p[1][r] = note(CHORD, n, V, v)
for r,n,v in VERSE_MELODY2:
    p[2][r] = note(LEAD, n, V, v)
drums(p)
mod.write_pattern(p); patterns.append(2)

# CHORUS (pattern 3): chorus bass + fuller chords + hook
p = np()
for n,r,v in CHORUS_BASS:
    p[0][r] = note(BASS, n, V, v)
for i,(n,v) in enumerate(CHORUS_CHORDS):
    p[1][i*8] = note(CHORD, n, V, v)
    p[1][i*8+2] = note(CHORD, n, V, v-2)  # chord doubling for thickness
for r,n,v in CHORUS_HOOK:
    p[2][r] = note(LEAD, n, V, v)
drums(p, 0x18)
mod.write_pattern(p); patterns.append(3)

# VERSE 3 (pattern 1 again — reuse)
patterns.append(1)

# CHORUS 2 (pattern 3 again)
patterns.append(3)

# BRIDGE (pattern 4): instrumental break — chords + bassline + melody, no drums
p = np()
for n,r in BASS_LINE:
    p[0][r] = note(BASS, n, V, 0x0C)
for r,n,v in BRIDGE_MELODY:
    p[2][r] = note(LEAD, n, V, v)
# Chord pad sustains E major
for r in range(0,64,8):
    p[1][r] = note(CHORD, 'E-2', V, 0x14)
    p[1][r] = note(CHORD, 'G#2', V, 0x12)
    p[1][r+4] = note(CHORD, 'B-2', V, 0x12)
mod.write_pattern(p); patterns.append(4)

# CHORUS 3 (pattern 3 again — final)
patterns.append(3)

# OUTRO (pattern 5): fade — bassline solo, everything else drops
p = np()
for n,r in BASS_LINE:
    vol = max(0x06, 0x1C - (r//4))
    p[0][r] = note(BASS, n, V, vol)
# Fading hihats
for r in range(0,64,8):
    p[3][r] = note(HAT, 'C-2', V, max(0x04, 0x0E - r//8))
# Last notes
p[2][56] = note(LEAD, 'B-1', V, 0x08)
p[2][60] = note(LEAD, 'E-2', V, 0x04)
p[1][56] = note(CHORD, 'E-2', V, 0x0A)
p[1][58] = note(CHORD, 'G#2', V, 0x08)
p[1][60] = note(CHORD, 'B-2', V, 0x06)
mod.write_pattern(p); patterns.append(5)

mod.order = patterns
mod.write('heart-of-glass-cover.mod')

# POST-PATCH: drum samples → one-shot (no loop)
# MOD writer defaults to full-length loops; drums buzz when looped.
with open('heart-of-glass-cover.mod', 'r+b') as fh:
    fh.seek(1080)
    if fh.read(4) == b'M.K.':
        fh.seek(138); fh.write(b'\x00\x00')  # hihat (sample 4, loop len at +28)
        fh.seek(168); fh.write(b'\x00\x00')  # kick  (sample 5)
        fh.seek(198); fh.write(b'\x00\x00')  # snare (sample 6)

print(f"composed: heart of glass cover — {len(patterns)} patterns")
