#!/usr/bin/env python3
"""star rider — pushed to the limit. NES-style epic in C minor.
multi-section adventure theme with portamento, vibrato, tempo changes,
drum fills, key modulation, counter-melodies, and rapid arpeggios."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter('star rider')

# NES-style instruments
mod.add_sample('pulse lead', gen_square_wave(440, 400, volume=0.38, duty=0.25))
mod.add_sample('pulse soft', gen_square_wave(440, 300, volume=0.28, duty=0.125))
mod.add_sample('pulse wide', gen_square_wave(440, 500, volume=0.32, duty=0.50))
mod.add_sample('tri bass',   gen_triangle_wave(110, 600, volume=0.58))
mod.add_sample('noise',      gen_hihat(volume=0.45))
mod.add_sample('kick',       gen_kick_drum(volume=0.55))

PL, PS, PW, TB, NO, KK = 1, 2, 3, 4, 5, 6
V  = 0x0C   # set volume
PO = 0x03   # portamento to note
VI = 0x04   # vibrato
TR = 0x07   # tremolo
VS = 0x0A   # volume slide
SP = 0x0F   # set speed/tempo
R  = (0,0,0,0)

def np(): return [[R]*64 for _ in range(4)]

def arp(pat, ch, row, notes, vol=0x10, speed=2, sample=PS):
    for i, n in enumerate(notes):
        r = row + i*speed
        if r < 64:
            pat[ch][r] = note(sample, n, V, vol)

def drum_std(pat, kick_vol=0x20, hat_vol=0x10):
    for r in [0,16,32,48]: pat[3][r] = note(KK, 'C-2', V, kick_vol)
    for r in range(0,64,4):
        if r not in [0,16,32,48]: pat[3][r] = note(NO, 'C-2', V, hat_vol)

def drum_fill(pat, style='snare'):
    pat[3][0] = note(KK, 'C-2', V, 0x24)
    pat[3][4] = note(NO, 'C-2', V, 0x18)
    pat[3][8] = note(KK, 'C-2', V, 0x1C)
    pat[3][12] = note(NO, 'C-2', V, 0x1A)
    if style == 'snare':
        for r in range(16,32,2): pat[3][r] = note(NO, 'C-2', V, 0x14)
    else:  # kick fill
        for r in range(16,32,4): pat[3][r] = note(KK, 'C-2', V, max(0x10, 0x22 - r//2))
    pat[3][32] = note(KK, 'C-2', V, 0x1E)
    for r in range(36,64,4): pat[3][r] = note(NO, 'C-2', V, 0x0E)

# ============================================================
# PATTERN 0: INTRO — sparse, mysterious, the journey begins
# ============================================================
p = np()
# Speed: slow for the intro
p[1][0] = (0, 0, SP, 0x04)  # speed 4 = slower
# Deep triangle bass — C minor pedal
for r in [0,16,32,48]:
    p[2][r] = note(TB, 'C-2', V, 0x18)

# Pulse lead with portamento — gliding, spacey
p[0][0] = note(PL, 'C-2', PO, 0x02)  # glide speed 2
p[0][8] = note(PL, 'G-2', PO, 0x02)
p[0][16] = note(PL, 'C-2', PO, 0x02)
p[0][24] = note(PL, 'D#2', V, 0x14)  # land on Eb

# Soft pulse arpeggios — harmonic shimmer
arp(p, 1, 32, ['C-2','D#2','G-2'], 0x0C, 3)
arp(p, 1, 44, ['C-2','D#2','G-2'], 0x0A, 4)
arp(p, 1, 56, ['C-2','D#2','G-2'], 0x08, 5)

# Minimal drums — just a heartbeat kick
for r in [32,40,48,56]:
    p[3][r] = note(KK, 'C-2', V, 0x16)

mod.write_pattern(p)

# ============================================================
# PATTERN 1: BUILDUP — drums enter, tempo increases, energy rises
# ============================================================
p = np()
p[1][0] = (0, 0, SP, 0x06)  # speed 6 = normal tempo

# Bass: walking in C minor
bass1 = ['C-2','C-2','G-1','G-1','G#1','G#1','D#2','D#2',
         'F-1','F-1','C-2','C-2','G-1','G-1','G#1','B-1']
for i, n in enumerate(bass1):
    p[2][i*4] = note(TB, n, V, 0x1C)

# Arpeggios — denser, faster
for off, notes in [(0,['C-2','D#2','G-2']),(8,['C-2','D#2','G-2']),
                    (16,['G-2','B-2','D-2']),(24,['G-2','B-2','D-2']),
                    (32,['G#2','C-2','D#2']),(40,['G#2','C-2','D#2']),
                    (48,['F-2','G#2','C-2']),(56,['G-2','B-2','D-2'])]:
    arp(p, 1, off, notes, 0x10, 2)

# Lead: rising phrase with vibrato
p[0][0] = note(PL, 'C-2', V, 0x14)
p[0][2] = note(PL, 'D#2', V, 0x12)
p[0][4] = note(PL, 'G-2', V, 0x16)
p[0][8] = note(PW, 'C-2', VI, 0x14)  # wide pulse with vibrato for emphasis
p[0][16] = note(PL, 'A#2', V, 0x12)
p[0][20] = note(PL, 'C-2', V, 0x10)
p[0][24] = note(PL, 'D#2', V, 0x14)
p[0][28] = note(PW, 'G-2', VI, 0x14)
p[0][32] = note(PL, 'F-2', V, 0x12)
p[0][36] = note(PL, 'G-2', V, 0x10)
p[0][40] = note(PL, 'G#2', V, 0x14)
p[0][44] = note(PL, 'C-2', V, 0x16)
p[0][48] = note(PW, 'C-2', V, 0x18)
p[0][52] = note(PL, 'A#2', V, 0x14)
p[0][56] = note(PL, 'G#2', V, 0x10)
p[0][60] = note(PL, 'G-2', V, 0x0C)

drum_std(p)
mod.write_pattern(p)

# ============================================================
# PATTERN 2: MAIN THEME — full energy, the core melody
# ============================================================
p = np()
# Bass: aggressive, driving
bass2 = ['C-2','C-2','C-2','G-1','G#1','G#1','G#1','D#2',
         'F-1','F-1','F-1','C-2','A#1','A#1','G-1','G#1']
for i, n in enumerate(bass2):
    p[2][i*4] = note(TB, n, V, 0x20)

# Arpeggio harmony — full, fast
harmony_chords = [
    (0,['C-2','D#2','G-2']),(4,['C-2','F-2','G#2']),(8,['C-2','D#2','G-2']),(12,['C-2','F-2','G#2']),
    (16,['G-2','B-2','D-2']),(20,['G-2','B-2','D-2']),(24,['G-2','B-2','F-2']),(28,['G-2','B-2','D-2']),
    (32,['G#2','C-2','D#2']),(36,['G#2','C-2','D#2']),(40,['G#2','C-2','F-2']),(44,['G#2','C-2','D#2']),
    (48,['F-2','G#2','C-2']),(52,['F-2','A#2','C-2']),(56,['G-2','B-2','D-2']),(60,['G-2','B-2','F-2']),
]
for off, notes in harmony_chords:
    arp(p, 1, off, notes, 0x12, 1)  # SPEED 1! Max speed arpeggio

# Lead: THE theme — heroic, energetic
theme = [
    # Phrase A
    (0,'C-2',0x1A,0,0),(2,'D#2',0x18,0,0),(4,'G-2',0x1C,0,0),(6,'C-2',0x1E,VI,0x14),
    (8,'A#2',0x18,0,0),(10,'G-2',0x16,0,0),(12,'F-2',0x14,0,0),(14,'D#2',0x12,0,0),
    (16,'G-2',0x1A,0,0),(18,'G#2',0x18,0,0),(20,'A#2',0x16,0,0),(22,'C-2',0x1A,0,0),
    (24,'D-2',0x18,0,0),(26,'C-2',0x14,0,0),(28,'A#2',0x10,0,0),(30,'G#2',0x0E,0,0),
    # Phrase B
    (32,'F-2',0x18,0,0),(34,'G-2',0x16,0,0),(36,'G#2',0x14,0,0),(38,'C-2',0x18,VI,0x12),
    (40,'D-2',0x16,0,0),(42,'C-2',0x14,0,0),(44,'A#2',0x12,0,0),(46,'G#2',0x10,0,0),
    (48,'G-2',0x16,0,0),(50,'F-2',0x14,0,0),(52,'D#2',0x12,0,0),(54,'C-2',0x10,0,0),
    (56,'A#2',0x12,0,0),(58,'C-2',0x14,0,0),(60,'D#2',0x16,0,0),(62,'G-2',0x18,0,0),
]
for r, n, v, fx, fp in theme:
    if fx:
        p[0][r] = note(PW if fx == VI else PL, n, fx, fp)
    else:
        p[0][r] = note(PL, n, V, v)

drum_std(p)
mod.write_pattern(p)

# ============================================================
# PATTERN 3: DRUM FILL — tension break
# ============================================================
p = np()
p[2][0] = note(TB, 'C-2', V, 0x1A)
p[2][16] = note(TB, 'G-1', V, 0x18)
p[2][32] = note(TB, 'G#1', V, 0x1C)
p[2][48] = note(TB, 'G-1', V, 0x14)
arp(p, 1, 0,  ['C-2','D#2','G-2'], 0x14, 2)
arp(p, 1, 16, ['G-2','B-2','D-2'], 0x12, 2)
arp(p, 1, 32, ['G#2','C-2','D#2'], 0x14, 2)
arp(p, 1, 48, ['G-2','B-2','F-2'], 0x12, 2)
# Lead: fragmented, building tension
for r,n,v in [(4,'C-2',0x18),(8,'G-2',0x14),(20,'B-2',0x16),(24,'D-2',0x12),
               (36,'C-2',0x18),(40,'G#2',0x14),(52,'B-2',0x16),(56,'F-2',0x12)]:
    p[0][r] = note(PL, n, V, v)
drum_fill(p, 'snare')
mod.write_pattern(p)

# ============================================================
# PATTERN 4: BRIDGE — modulation to Eb major, brighter
# ============================================================
p = np()
# Bass shifts to Eb major feel
bass_bridge = ['D#2','D#2','A#1','A#1','G#1','G#1','D#2','D#2',
               'F-1','F-1','C-2','C-2','A#1','A#1','G#1','A#1']
for i, n in enumerate(bass_bridge):
    p[2][i*4] = note(TB, n, V, 0x1A)

# Arpeggios in Eb major
for off, notes in [(0,['D#2','G-2','A#2']),(8,['D#2','G-2','A#2']),
                    (16,['A#2','D-2','F-2']),(24,['A#2','D-2','F-2']),
                    (32,['G#2','C-2','D#2']),(40,['G#2','C-2','D#2']),
                    (48,['F-2','A-2','C-2']),(56,['A#2','D-2','F-2'])]:
    arp(p, 1, off, notes, 0x10, 2)

# Lead: brighter, major-key melody
bridge_mel = [
    (0,'D#2',0x16,0,0),(2,'G-2',0x14,0,0),(4,'A#2',0x16,0,0),(6,'D-2',0x18,VI,0x12),
    (8,'C-2',0x16,0,0),(10,'A#2',0x14,0,0),(12,'G-2',0x12,0,0),(14,'F-2',0x10,0,0),
    (16,'A#2',0x16,0,0),(18,'C-2',0x14,0,0),(20,'D-2',0x16,0,0),(22,'A#2',0x14,0,0),
    (24,'G-2',0x12,0,0),(26,'F-2',0x10,0,0),(28,'D#2',0x0E,0,0),(30,'C-2',0x0C,0,0),
    (32,'G#2',0x16,0,0),(34,'A#2',0x14,0,0),(36,'C-2',0x16,0,0),(38,'G#2',0x14,0,0),
    (40,'F-2',0x12,0,0),(42,'G-2',0x10,0,0),(44,'G#2',0x0E,0,0),(46,'A#2',0x0C,0,0),
    (48,'C-2',0x14,0,0),(52,'A#2',0x12,0,0),(56,'G#2',0x10,0,0),(60,'G-2',0x0E,0,0),
]
for r,n,v,fx,fp in bridge_mel:
    if fx: p[0][r] = note(PW, n, fx, fp)
    else: p[0][r] = note(PL, n, V, v)

drum_std(p, 0x1E, 0x0E)
mod.write_pattern(p)

# ============================================================
# PATTERN 5: RETURN — back to C minor, intensified
# ============================================================
p = np()
bass_back = ['C-2','C-2','G-1','G-1','G#1','G#1','D#2','D#2',
             'F-1','F-1','C-2','C-2','G-1','G-1','G#1','C-2']
for i, n in enumerate(bass_back):
    p[2][i*4] = note(TB, n, V, 0x22)

# Harmony: back to C minor, denser
for off, notes in [(0,['C-2','D#2','G-2']),(4,['C-2','F-2','G#2']),
                    (8,['C-2','D#2','G-2']),(12,['C-2','F-2','A#2']),
                    (16,['G-2','B-2','D-2']),(20,['G-2','B-2','F-2']),
                    (24,['G-2','B-2','D-2']),(28,['G-2','B-2','F-2']),
                    (32,['G#2','C-2','D#2']),(36,['G#2','C-2','F-2']),
                    (40,['G#2','C-2','D#2']),(44,['G#2','C-2','G-2']),
                    (48,['F-2','G#2','C-2']),(52,['F-2','A#2','D-2']),
                    (56,['G-2','B-2','D-2']),(60,['G-2','B-2','F-2'])]:
    arp(p, 1, off, notes, 0x14, 1)

# Lead: theme returns — more aggressive, with portamento flourishes
theme2 = [
    (0,'C-2',0x1C,0,0),(2,'D#2',0x1A,0,0),(4,'G-2',0x1E,0,0),(6,'C-2',0x20,VI,0x14),
    (8,'A#2',0x1A,0,0),(10,'G-2',0x18,0,0),(12,'F-2',0x16,0,0),(14,'D#2',0x14,0,0),
    # Portamento run!
    (16,'G-2',0x1E,PO,0x02),(18,'',0,0,0),(20,'',0,0,0),(21,'C-2',0x1E,0,0),
    (22,'A#2',0x18,0,0),(24,'G#2',0x1A,VI,0x16),(26,'G-2',0x14,0,0),
    (28,'F-2',0x12,0,0),(30,'D#2',0x10,0,0),
    # Phrase B — extended
    (32,'F-2',0x1A,0,0),(34,'G-2',0x18,0,0),(36,'G#2',0x16,0,0),
    (38,'C-2',0x1C,PO,0x03),(40,'D-2',0x1A,0,0),(42,'C-2',0x16,0,0),
    (44,'A#2',0x14,0,0),(46,'G#2',0x12,0,0),
    # Climax
    (48,'G-2',0x18,0,0),(50,'G#2',0x1A,0,0),(52,'A#2',0x1C,0,0),
    (54,'C-2',0x20,VI,0x18),(56,'D-2',0x1E,0,0),(58,'C-2',0x1A,0,0),
    (60,'A#2',0x16,0,0),(62,'G-2',0x14,0,0),
]
for r,n,v,fx,fp in theme2:
    if fx:
        p[0][r] = note(PW if fx in (VI, TR) else PL, n, fx, fp)
    elif n:
        p[0][r] = note(PL, n, V, v)

drum_std(p, 0x24, 0x12)
mod.write_pattern(p)

# ============================================================
# PATTERN 6: CLIMAX — fastest, most intense
# ============================================================
p = np()
p[1][0] = (0, 0, SP, 0x08)  # SPEED 8 = faster!
bass_climax = ['C-2','C-2','D#2','D#2','G#1','G#1','C-2','C-2',
               'F-1','F-1','G-1','G#1','A#1','A#1','C-2','C-2']
for i, n in enumerate(bass_climax):
    p[2][i*4] = note(TB, n, V, 0x24)

for off,notes in [(0,['C-2','D#2','G-2']),(4,['C-2','F-2','G#2']),
                   (8,['D#2','G-2','A#2']),(12,['D#2','G-2','C-2']),
                   (16,['G#2','C-2','D#2']),(20,['G#2','C-2','F-2']),
                   (24,['C-2','D#2','G-2']),(28,['C-2','F-2','G#2']),
                   (32,['F-2','G#2','C-2']),(36,['F-2','A#2','D-2']),
                   (40,['G-2','B-2','D-2']),(44,['G#2','C-2','D#2']),
                   (48,['A#2','D-2','F-2']),(52,['A#2','D-2','G-2']),
                   (56,['C-2','D#2','G-2']),(60,['C-2','F-2','G#2'])]:
    arp(p, 1, off, notes, 0x14, 1)

# Lead: rapid, virtuosic run
climax_lead = [
    (0,'G-2',0x18,0,0),(1,'A#2',0x16,0,0),(2,'C-2',0x18,0,0),(3,'D#2',0x1A,VI,0x16),
    (4,'C-2',0x18,0,0),(5,'A#2',0x16,0,0),(6,'G-2',0x14,0,0),(7,'D#2',0x12,0,0),
    (8,'G-2',0x18,0,0),(9,'G#2',0x16,0,0),(10,'A#2',0x18,0,0),(11,'C-2',0x1A,VI,0x14),
    (12,'D-2',0x18,0,0),(13,'C-2',0x16,0,0),(14,'A#2',0x14,0,0),(15,'G#2',0x12,0,0),
    (16,'C-2',0x1C,VI,0x18),(18,'D#2',0x1A,0,0),(20,'C-2',0x18,0,0),(22,'G#2',0x14,0,0),
    (24,'G-2',0x16,0,0),(26,'F-2',0x14,0,0),(28,'D#2',0x12,0,0),(30,'C-2',0x10,0,0),
    (32,'F-2',0x18,0,0),(33,'G-2',0x16,0,0),(34,'G#2',0x18,0,0),(35,'C-2',0x1A,VI,0x14),
    (36,'D-2',0x18,0,0),(37,'C-2',0x16,0,0),(38,'A#2',0x14,0,0),(39,'G#2',0x12,0,0),
    (40,'G-2',0x16,0,0),(41,'A#2',0x14,0,0),(42,'C-2',0x16,0,0),(43,'D#2',0x18,VI,0x16),
    (44,'G-2',0x1A,0,0),(46,'F-2',0x18,0,0),(48,'D#2',0x1C,0,0),
    (50,'C-2',0x1A,0,0),(52,'A#2',0x18,0,0),(54,'G-2',0x16,0,0),
    (56,'G#2',0x16,0,0),(58,'C-2',0x14,0,0),(60,'D#2',0x12,0,0),(62,'G-2',0x10,0,0),
]
for r,n,v,fx,fp in climax_lead:
    if fx: p[0][r] = note(PW, n, fx, fp)
    else: p[0][r] = note(PL, n, V, v)

drum_fill(p, 'kick')
mod.write_pattern(p)

# ============================================================
# PATTERN 7: VICTORY — resolution in C major, triumphant
# ============================================================
p = np()
p[1][0] = (0, 0, SP, 0x06)  # back to normal tempo

# Bass: C major resolution
bass_victory = ['C-2','C-2','G-1','G-1','F-1','F-1','C-2','C-2',
                'F-1','F-1','G-1','G-1','C-2','G-1','C-2','C-2']
for i, n in enumerate(bass_victory):
    p[2][i*4] = note(TB, n, V, 0x1E)

# Arpeggios in C major
for off, notes in [(0,['C-2','E-2','G-2']),(8,['C-2','E-2','G-2']),
                    (16,['G-2','B-2','D-2']),(24,['G-2','B-2','D-2']),
                    (32,['F-2','A-2','C-2']),(40,['F-2','A-2','C-2']),
                    (48,['G-2','B-2','D-2']),(56,['C-2','E-2','G-2'])]:
    arp(p, 1, off, notes, 0x12, 2)

# Lead: triumphant melody in C major
victory = [
    (0,'C-2',0x1A,0,0),(4,'E-2',0x18,0,0),(8,'G-2',0x1C,0,0),(12,'C-2',0x1E,VI,0x16),
    (16,'B-2',0x1A,0,0),(20,'C-2',0x18,0,0),(24,'G-2',0x14,0,0),(28,'E-2',0x10,0,0),
    (32,'F-2',0x18,0,0),(36,'A-2',0x16,0,0),(40,'C-2',0x1A,0,0),(44,'F-2',0x18,VI,0x14),
    (48,'E-2',0x1C,0,0),(52,'C-2',0x18,0,0),(56,'G-2',0x14,0,0),(60,'C-2',0x10,0,0),
]
for r,n,v,fx,fp in victory:
    if fx: p[0][r] = note(PW, n, fx, fp)
    else: p[0][r] = note(PL, n, V, v)

drum_std(p, 0x20, 0x10)
mod.write_pattern(p)

# ============================================================
# PATTERN 8: OUTRO — fade to silence, journey complete
# ============================================================
p = np()
# Bass: final descent into silence
for i, n in enumerate(['C-2','G-1','F-1','C-2','G-1','F-1','C-2','C-2']):
    vol = max(0x04, 0x1A - i*2)
    p[2][i*8] = note(TB, n, V, vol)

arp(p, 1, 0,  ['C-2','E-2','G-2'], 0x0E, 3)
arp(p, 1, 16, ['F-2','A-2','C-2'], 0x0C, 3)
arp(p, 1, 32, ['G-2','B-2','D-2'], 0x0A, 4)
arp(p, 1, 48, ['C-2','E-2','G-2'], 0x06, 5)

# Lead: final fragment
for r,n,v in [(0,'C-2',0x16),(4,'G-2',0x12),(8,'E-2',0x0E),(16,'F-2',0x10),
               (20,'A-2',0x0C),(24,'C-2',0x08),(32,'G-2',0x0C),(36,'E-2',0x08),
               (40,'C-2',0x06),(48,'C-2',0x06),(52,'E-2',0x04),(56,'G-2',0x03),
               (60,'C-2',0x02)]:
    p[0][r] = note(PL, n, V, v)

# Fading heartbeat
for r in [0,16,32,48]:
    p[3][r] = note(KK, 'C-2', V, max(0x06, 0x16 - r//4))
for r in range(0,48,8):
    p[3][r] = note(NO, 'C-2', V, max(0x02, 0x0A - r//8))

mod.write_pattern(p)

# ============================================================
# ASSEMBLE AND WRITE
# ============================================================
mod.order = [
    0,         # intro — slow, mysterious
    1,         # buildup — drums enter, energy rises
    2, 2,      # main theme ×2
    3,         # drum fill — tension break
    4,         # bridge — Eb major, brighter
    5,         # return — C minor, intensified
    2,         # main theme reprise
    6,         # climax — fastest, virtuosic
    7, 7,      # victory — C major, triumphant ×2
    8,         # outro — fade to silence
]

mod.write('star-rider.mod')

# Post-patch: one-shot drums
with open('star-rider.mod', 'r+b') as fh:
    fh.seek(1080)
    if fh.read(4) == b'M.K.':
        fh.seek(138); fh.write(b'\x00\x00')  # noise (sample 5, idx 4)
        fh.seek(168); fh.write(b'\x00\x00')  # kick  (sample 6, idx 5)

print("composed: star rider — 9 patterns, 15 plays, multi-section epic")
