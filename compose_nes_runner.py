#!/usr/bin/env python3
"""nes-style chiptune: proof of concept — pulse leads, triangle bass, noise drums, rapid arpeggios"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter('pixel runner')

# NES-style instruments: no sustain loops on percussion, short punchy samples
mod.add_sample('pulse lead', gen_square_wave(440, 600, volume=0.35, duty=0.25))   # classic NES duty
mod.add_sample('pulse arp',  gen_square_wave(440, 400, volume=0.28, duty=0.125))  # thinner, for arps
mod.add_sample('tri bass',   gen_triangle_wave(110, 800, volume=0.55))             # NES triangle
mod.add_sample('noise',      gen_hihat(volume=0.45))                                # noise perc
mod.add_sample('kick',       gen_kick_drum(volume=0.55))

PL, PA, TB, NO, KK = 1, 2, 3, 4, 5
V  = 0x0C
R  = (0,0,0,0)

def np(): return [[R]*64 for _ in range(4)]

# --- UTILITY: fast arpeggio on one channel ---
def arp(pat, ch, start_row, notes, vol=0x10, speed=2):
    """NES-style rapid arpeggio: cycles through notes every 'speed' rows"""
    for i, n in enumerate(notes):
        pat[ch][start_row + i*speed] = note(PA, n, V, vol)

# --- PATTERN 0: INTRO — triangle bass solo, pulse lead enters ---
p = np()
# Bass: classic descending NES run
bass_run = ['C-2','A-1','F-1','G-1','C-2','A-1','G-1','F-1',
            'E-1','C-1','A-1','F-1','G-1','A-1','B-1','C-2']
for i, n in enumerate(bass_run):
    p[2][i*4] = note(TB, n, V, 0x1C)

# Kick on downbeats
for r in [0,16,32,48]:
    p[3][r] = note(KK, 'C-2', V, 0x20)

# Pulse lead enters halfway — rising phrase
for i, n in enumerate(['C-3','E-3','G-3','C-4','E-4','G-4','C-4','G-4']):
    p[0][32 + i*4] = note(PL, n, V, 0x16)

# Noise hihat on 8ths
for r in range(32,64,4):
    p[3][r] = note(NO, 'C-2', V, 0x10)

mod.write_pattern(p)

# --- PATTERN 1: MAIN THEME — fast arpeggios + lead melody ---
p = np()
# Triangle bass: walking bassline
for i, n in enumerate(['C-2','C-2','G-1','G-1','A-1','A-1','F-1','F-1',
                         'C-2','C-2','G-1','G-1','E-1','E-1','F-1','G-1']):
    p[2][i*4] = note(TB, n, V, 0x1A)

# Arpeggio chords: rapid NES-style chord simulation
arp(p, 1, 0,  ['C-3','E-3','G-3'], 0x0E, 2)
arp(p, 1, 8,  ['C-3','E-3','G-3'], 0x0E, 2)
arp(p, 1, 16, ['G-2','B-2','D-3'], 0x0E, 2)
arp(p, 1, 24, ['G-2','B-2','D-3'], 0x0E, 2)
arp(p, 1, 32, ['A-2','C-3','E-3'], 0x0E, 2)
arp(p, 1, 40, ['A-2','C-3','E-3'], 0x0E, 2)
arp(p, 1, 48, ['F-2','A-2','C-3'], 0x0E, 2)
arp(p, 1, 56, ['G-2','B-2','D-3'], 0x0E, 2)

# Lead melody: energetic NES-style hook
melody = [(0,'C-4',0x18),(2,'E-4',0x16),(4,'G-4',0x14),(6,'C-4',0x18),
          (8,'B-4',0x16),(10,'A-4',0x14),(12,'G-4',0x12),(14,'F-4',0x10),
          (16,'E-4',0x16),(18,'C-4',0x14),(20,'E-4',0x12),(24,'G-4',0x16),
          (26,'A-4',0x14),(28,'B-4',0x12),(30,'C-4',0x16),
          (32,'D-4',0x14),(34,'C-4',0x12),(36,'B-4',0x10),(38,'A-4',0x0E),
          (40,'G-4',0x12),(42,'F-4',0x10),(44,'E-4',0x0E),(48,'C-4',0x14),
          (50,'E-4',0x12),(52,'G-4',0x10),(56,'C-4',0x14),(58,'G-4',0x0C),
          (60,'E-4',0x0A),(62,'C-4',0x08)]
for r,n,v in melody:
    p[0][r] = note(PL, n, V, v)

# Drums: kick 1&3, noise on 8ths
for r in [0,16,32,48]:
    p[3][r] = note(KK, 'C-2', V, 0x1E)
for r in range(0,64,4):
    if r not in [0,16,32,48]:  # don't double with kick
        p[3][r] = note(NO, 'C-2', V, 0x0E)

mod.write_pattern(p)

# --- PATTERN 2: BRIDGE — arpeggios take over, lead rests ---
p = np()
for i, n in enumerate(['A-1','A-1','F-1','F-1','G-1','G-1','C-2','C-2',
                         'A-1','A-1','F-1','F-1','E-1','F-1','G-1','G-1']):
    p[2][i*4] = note(TB, n, V, 0x18)

arp(p, 1, 0,  ['A-2','C-3','E-3'], 0x10, 2)
arp(p, 1, 8,  ['A-2','C-3','E-3'], 0x10, 2)
arp(p, 1, 16, ['F-2','A-2','C-3'], 0x10, 2)
arp(p, 1, 24, ['F-2','A-2','C-3'], 0x10, 2)
arp(p, 1, 32, ['G-2','B-2','D-3'], 0x10, 2)
arp(p, 1, 40, ['G-2','B-2','D-3'], 0x10, 2)
arp(p, 1, 48, ['C-3','E-3','G-3'], 0x12, 2)
arp(p, 1, 56, ['G-2','B-2','D-3'], 0x12, 2)

# Pulse lead: sparse, call-and-response
for r,n,v in [(8,'E-4',0x12),(12,'C-4',0x10),(24,'F-4',0x10),(28,'A-4',0x0E),
               (40,'B-4',0x12),(44,'D-4',0x10),(56,'C-4',0x14),(60,'G-4',0x0C)]:
    p[0][r] = note(PL, n, V, v)

for r in [0,16,32,48]:
    p[3][r] = note(KK, 'C-2', V, 0x1C)
for r in range(0,64,4):
    if r not in [0,16,32,48]:
        p[3][r] = note(NO, 'C-2', V, 0x0C)

mod.write_pattern(p)

# --- PATTERN 3: VARIATION — different key center, quieter ---
p = np()
for i, n in enumerate(['E-1','E-1','C-1','C-1','D-1','D-1','E-1','E-1',
                         'F-1','F-1','G-1','G-1','A-1','B-1','C-2','C-2']):
    p[2][i*4] = note(TB, n, V, 0x14)

arp(p, 1, 0,  ['E-2','G-2','C-3'], 0x0C, 2)
arp(p, 1, 8,  ['E-2','G-2','C-3'], 0x0C, 2)
arp(p, 1, 16, ['C-2','E-2','G-2'], 0x0C, 2)
arp(p, 1, 24, ['C-2','E-2','G-2'], 0x0C, 2)
arp(p, 1, 32, ['D-2','F-2','A-2'], 0x0C, 2)
arp(p, 1, 40, ['D-2','F-2','A-2'], 0x0C, 2)
arp(p, 1, 48, ['E-2','G-2','C-3'], 0x0E, 2)
arp(p, 1, 56, ['G-2','B-2','D-3'], 0x0E, 2)

# Lead: softer, melodic fragment
mel2 = [(0,'E-4',0x12),(8,'G-4',0x10),(16,'C-4',0x0E),(24,'E-4',0x0C),
        (32,'D-4',0x10),(36,'C-4',0x0E),(40,'A-4',0x0C),(48,'C-4',0x12),
        (52,'G-4',0x0E),(56,'E-4',0x0C),(60,'C-4',0x08)]
for r,n,v in mel2:
    p[0][r] = note(PL, n, V, v)

for r in [0,16,32,48]:
    p[3][r] = note(KK, 'C-2', V, 0x18)
for r in range(0,64,4):
    if r not in [0,16,32,48]:
        p[3][r] = note(NO, 'C-2', V, 0x0A)

mod.write_pattern(p)

# --- PATTERN 4: OUTRO — fade and finish ---
p = np()
bass_end = ['C-2','G-1','A-1','F-1','C-2','G-1','E-1','C-1']
for i, n in enumerate(bass_end):
    vol = max(0x06, 0x18 - i*2)
    p[2][i*8] = note(TB, n, V, vol)

arp(p, 1, 0,  ['C-3','E-3','G-3'], 0x0C, 3)
arp(p, 1, 16, ['F-2','A-2','C-3'], 0x0A, 3)
arp(p, 1, 32, ['C-3','E-3','G-3'], 0x08, 3)
arp(p, 1, 48, ['C-3','E-3','G-3'], 0x04, 4)

# Lead: final descending phrase
for r,n,v in [(0,'C-4',0x14),(4,'G-4',0x12),(8,'E-4',0x10),(12,'C-4',0x0E),
               (20,'A-4',0x0C),(24,'F-4',0x0A),(32,'G-4',0x0A),(36,'E-4',0x08),
               (40,'C-4',0x06),(48,'C-4',0x06),(52,'E-4',0x04),(56,'G-4',0x03),
               (60,'C-4',0x02)]:
    p[0][r] = note(PL, n, V, v)

# Fading drums
for r in [0,16,32]:
    p[3][r] = note(KK, 'C-2', V, 0x14)
for r in range(0,48,8):
    p[3][r] = note(NO, 'C-2', V, max(0x04, 0x0A - r//8))

mod.write_pattern(p)

mod.order = [0, 1, 1, 2, 1, 3, 1, 2, 4]

# POST-PATCH: one-shot drum samples (no loop)
mod.write('pixel-runner.mod')
with open('pixel-runner.mod', 'r+b') as fh:
    fh.seek(1080)
    if fh.read(4) == b'M.K.':
        fh.seek(138); fh.write(b'\x00\x00')  # noise (sample 4)
        fh.seek(168); fh.write(b'\x00\x00')  # kick  (sample 5)

print("composed: pixel runner")
