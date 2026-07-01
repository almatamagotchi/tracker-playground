#!/usr/bin/env python3
"""canon in d minor — baroque-style counterpoint for 4 voices.
each voice enters 12 rows after the last. no drums. just polyphony."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter('canon in d minor')

# Baroque-style instruments: bright, precise, minimal sustain
mod.add_sample('voice 1', gen_square_wave(880, 300, volume=0.30, duty=0.25))   # soprano — bright pulse
mod.add_sample('voice 2', gen_square_wave(660, 300, volume=0.26, duty=0.25))   # alto — slightly softer
mod.add_sample('voice 3', gen_triangle_wave(220, 500, volume=0.42))             # tenor — warm triangle
mod.add_sample('continuo',gen_sine_wave(110, 2000, volume=0.22))                # bass — sustained organ

V1, V2, V3, CO = 1, 2, 3, 4
V  = 0x0C   # set volume
R  = (0,0,0,0)

def np(): return [[R]*64 for _ in range(4)]

# ============================================================
# THE CANON MELODY — 32 rows, in D minor
# Each voice plays this melody, offset by 12 rows
# ============================================================
# baroque flavor: stepwise with occasional leaps, ornamented
melody = [
    # Phrase A: ascending
    (0,'D-2',0x16),(1,'E-2',0x14),(2,'F-2',0x14),(3,'G-2',0x16),
    (4,'A-2',0x18),(5,'A-2',0x16),(6,'G-2',0x12),(7,'F-2',0x10),
    # Phrase B: turning point
    (8,'E-2',0x14),(9,'D-2',0x12),(10,'C#2',0x10),(11,'D-2',0x12),
    (12,'A-1',0x16),(13,'A-1',0x14),(14,'B-1',0x12),(15,'C#2',0x10),
    # Phrase C: descent with ornament
    (16,'D-2',0x14),(17,'E-2',0x12),(18,'F-2',0x12),(19,'E-2',0x10),
    (20,'D-2',0x14),(21,'C#2',0x12),(22,'D-2',0x10),(23,'A-1',0x0E),
    # Phrase D: cadence
    (24,'B-1',0x12),(25,'C#2',0x10),(26,'D-2',0x12),(27,'F-2',0x10),
    (28,'E-2',0x10),(29,'D-2',0x0E),(30,'C#2',0x0C),(31,'D-2',0x08),
]

# ============================================================
# PATTERN 0: EXPOSITION — voices enter one by one
# ============================================================
p = np()

# Continuo: D minor pedal — the ground beneath everything
for r in range(0, 64, 12):
    p[3][r] = note(CO, 'D-1', V, 0x0E)

# Voice 1 (soprano): enters at row 0, plays at pitch
for r,n,v in melody:
    if r < 64:
        p[0][r] = note(V1, n, V, v)

# Voice 2 (alto): enters at row 12, same melody
for r,n,v in melody:
    rr = r + 12
    if rr < 64:
        # slightly softer — second voice
        p[1][rr] = note(V2, n, V, max(0x04, v-4))

# Voice 3 (tenor): enters at row 24, same melody down an octave
for r,n,v in melody:
    rr = r + 24
    if rr < 64:
        # transpose down — change octave numbers
        n_lower = n[:-1] + str(int(n[-1]) - 1) if n[-1].isdigit() else n
        try:
            note_to_period(n_lower)
            p[2][rr] = note(V3, n_lower, V, max(0x04, v-4))
        except:
            pass  # skip if out of range

mod.write_pattern(p)

# ============================================================
# PATTERN 1: FULL TEXTURE — all voices fully engaged
# ============================================================
p = np()

# Continuo: walking bass in D minor
bass_line = ['D-1','A-1','F-1','C-1','G-1','D-1','A-1','D-1',
             'B-1','F-1','C#2','A-1','D-1','A-1','D-1','D-1']
for i, n in enumerate(bass_line):
    r = i * 4
    p[3][r] = note(CO, n, V, 0x10 if i%2==0 else 0x0C)

# All three voices play the canon simultaneously
for r,n,v in melody:
    if r < 64: p[0][r] = note(V1, n, V, v)
for r,n,v in melody:
    rr = r + 12
    if rr < 64: p[1][rr] = note(V2, n, V, max(0x04, v-4))
for r,n,v in melody:
    rr = r + 24
    if rr < 64:
        n_lower = n[:-1] + str(int(n[-1]) - 1)
        try:
            note_to_period(n_lower)
            p[2][rr] = note(V3, n_lower, V, max(0x04, v-4))
        except:
            pass

mod.write_pattern(p)

# ============================================================
# PATTERN 2: VARIATION — voices invert, exchange roles  
# ============================================================
p = np()

# Continuo moves more
bass2 = ['D-1','D-1','C#2','C#2','F-1','F-1','G-1','G-1',
         'A-1','A-1','D-1','D-1','A-1','C#2','D-1','D-1']
for i, n in enumerate(bass2):
    r = i * 4
    p[3][r] = note(CO, n, V, 0x12 if i%4==0 else 0x0C)

# Voice 1: melody with ornamentation (added passing tones)
ornamented = melody[:]
# Add a few trill-like ornaments — rapid neighbor notes
extras = [(5,'A#2',0x0E),(13,'G#1',0x0C),(21,'C-2',0x0E),(29,'C#2',0x0C)]
for r,n,v in extras:
    if r < 64: p[0][r] = note(V2, n, V, v)
for r,n,v in ornamented:
    if r < 64: p[0][r] = note(V1, n, V, max(0x06, v-2))

# Voice 2: canon in inversion (descending when the melody ascends)
inverted = [
    (0,'D-2',0x14),(1,'C#2',0x12),(2,'C-2',0x12),(3,'B-1',0x14),
    (4,'A-1',0x16),(5,'A-1',0x14),(6,'B-1',0x12),(7,'C-2',0x10),
    (8,'D-2',0x14),(9,'E-2',0x12),(10,'F-2',0x10),(11,'E-2',0x12),
    (12,'D-2',0x16),(13,'D-2',0x14),(14,'C-2',0x12),(15,'B-1',0x10),
    (16,'A-1',0x14),(17,'G-1',0x12),(18,'F-1',0x12),(19,'G-1',0x10),
    (20,'A-1',0x14),(21,'B-1',0x12),(22,'A-1',0x10),(23,'D-2',0x0E),
    (24,'C-2',0x12),(25,'B-1',0x10),(26,'A-1',0x12),(27,'F-1',0x10),
    (28,'G-1',0x10),(29,'A-1',0x0E),(30,'B-1',0x0C),(31,'C#2',0x08),
]
for r,n,v in inverted:
    rr = r + 16
    if rr < 64: p[1][rr] = note(V2, n, V, v)

# Voice 3: sustained harmony notes
harmony = [(0,'D-2',0x10),(16,'F-2',0x0E),(32,'A-2',0x0C),(48,'D-2',0x0A),
           (8,'C-2',0x0E),(24,'E-2',0x0C),(40,'G-2',0x0A),(56,'C#2',0x08)]
for r,n,v in harmony:
    if r < 64: p[2][r] = note(V3, n, V, v)

mod.write_pattern(p)

# ============================================================
# PATTERN 3: STRETTO — voices enter closer together (every 8 rows)
# ============================================================
p = np()

# Continuo: pedal D with ornaments
for r in range(0, 64, 8):
    p[3][r] = note(CO, 'D-1', V, 0x12 if r%16==0 else 0x0A)
p[3][32] = note(CO, 'A-1', V, 0x10)
p[3][48] = note(CO, 'D-1', V, 0x0E)

# Stretto: voices enter every 8 rows instead of 12
for r,n,v in melody:
    if r < 64: p[0][r] = note(V1, n, V, v)
for r,n,v in melody:
    rr = r + 8
    if rr < 64: p[1][rr] = note(V2, n, V, max(0x04, v-4))
for r,n,v in melody:
    rr = r + 24  # bass still at +24 for fuller texture
    if rr < 64:
        n_lower = n[:-1] + str(int(n[-1]) - 1)
        try:
            note_to_period(n_lower)
            p[2][rr] = note(V3, n_lower, V, max(0x04, v-4))
        except:
            pass

mod.write_pattern(p)

# ============================================================
# PATTERN 4: CADENCE — resolution, the voices converge and rest
# ============================================================
p = np()

# Continuo: final cadence — D minor perfect cadence
cadence_bass = [(0,'A-1',0x14),(4,'A-1',0x12),(8,'A-1',0x10),
                (12,'A-1',0x0E),(16,'D-1',0x14),(20,'D-1',0x12),
                (24,'D-1',0x10),(28,'D-1',0x0E),
                (32,'G-1',0x12),(36,'G-1',0x0E),
                (40,'A-1',0x10),(44,'A-1',0x0C),
                (48,'D-1',0x14),(52,'D-1',0x0E),
                (56,'D-1',0x0A),(60,'D-1',0x06)]
for r,n,v in cadence_bass:
    p[3][r] = note(CO, n, V, v)

# Voice 1: closing phrase, descending
for r,n,v in [(0,'A-2',0x14),(2,'G-2',0x12),(4,'F-2',0x10),(6,'E-2',0x0E),
               (8,'D-2',0x12),(10,'C#2',0x10),(12,'D-2',0x0E),(14,'A-1',0x0C),
               (16,'D-2',0x16),(20,'F-2',0x14),(24,'A-2',0x12),(28,'D-3',0x10),
               (32,'C-3',0x14),(36,'A#2',0x12),(40,'A-2',0x10),(44,'G-2',0x0E),
               (48,'F-2',0x12),(52,'E-2',0x0E),(56,'D-2',0x0A),(60,'D-2',0x06)]:
    p[0][r] = note(V1, n, V, v)

# Voice 2: echoes the closing phrase
for r,n,v in [(4,'F-2',0x10),(8,'E-2',0x0E),(12,'D-2',0x0C),(16,'A-1',0x0A),
               (20,'D-2',0x12),(24,'F-2',0x10),(28,'A-2',0x0E),(32,'D-3',0x0C),
               (36,'C-3',0x10),(44,'A-2',0x0C),(52,'F-2',0x0A),(60,'D-2',0x04)]:
    p[1][r] = note(V2, n, V, v)

# Voice 3: final harmony
for r,n,v in [(0,'D-2',0x0C),(16,'D-2',0x0E),(32,'C#2',0x0C),(48,'D-2',0x0A),(56,'D-2',0x04)]:
    p[2][r] = note(V3, n, V, v)

mod.write_pattern(p)

# ============================================================
# PATTERN 5: CODA — all voices fade, final chord
# ============================================================
p = np()

# Continuo: final D, fading
for r in [0,8,16,24,32,40]:
    vol = max(0x04, 0x14 - r//4)
    p[3][r] = note(CO, 'D-1', V, vol)

# Voice 1: the melody's last echo — very soft
for r,n,v in [(0,'D-2',0x0C),(4,'F-2',0x0A),(8,'A-2',0x08),(16,'D-3',0x06),
               (24,'D-2',0x04),(32,'F-2',0x03),(40,'A-2',0x02)]:
    p[0][r] = note(V1, n, V, v)

# Voice 2: final harmony, almost inaudible
for r,n,v in [(4,'A-2',0x08),(12,'F-2',0x06),(20,'D-2',0x04),(28,'A-1',0x02)]:
    p[1][r] = note(V2, n, V, v)

# Voice 3: the last note — the tonic
p[2][0] = note(V3, 'D-1', V, 0x0C)
p[2][8] = note(V3, 'D-1', V, 0x08)
p[2][16] = note(V3, 'D-1', V, 0x06)
p[2][24] = note(V3, 'D-1', V, 0x04)
p[2][32] = note(V3, 'D-1', V, 0x02)
p[2][40] = note(V3, 'D-1', V, 0x01)  # dissolve

mod.write_pattern(p)

mod.order = [0, 0, 1, 1, 2, 1, 3, 2, 1, 4, 5, 5]
mod.write('canon-in-d-minor.mod')
print("composed: canon in d minor")
