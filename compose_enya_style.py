#!/usr/bin/env python3
"""the water between — enya-style: layered harmonies, slow pulse, floating arpeggios, ethereal"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter('the water between')

# Ethereal instruments: soft, floating, sustained
mod.add_sample('voice',    gen_sine_wave(3520, 8000, volume=0.20))    # airy lead — very soft
mod.add_sample('choir',    gen_triangle_wave(1760, 9000, volume=0.16)) # warm pad — layered harmony
mod.add_sample('harp',     gen_sine_wave(2640, 3000, volume=0.18))    # bright ripple — arpeggios
mod.add_sample('deep',     gen_sine_wave(55, 6000, volume=0.38))      # grounding drone

VO, CH, HP, DP = 1, 2, 3, 4
V  = 0x0C
VS = 0x0A   # volume slide — gentle swells
TR = 0x07   # tremolo — ethereal waver
R  = (0,0,0,0)

def np(): return [[R]*64 for _ in range(4)]

# ============================================================
# PATTERN 0: DAWN — the first light
# ============================================================
p = np()
# Deep drone: the earth
for r in range(0, 64, 16):
    p[3][r] = note(DP, 'D-1', V, 0x0C)

# Harp: slow ripple — a single arpeggio, D major
for i, n in enumerate(['D-2','F#2','A-2','D-3','F#3','A-3','D-4','F#4']):
    r = i * 8
    p[2][r] = note(HP, n, V, max(0x04, 0x0C - i))

# Voice: the whisper — enters at row 32, barely there
for r,n,v in [(32,'D-3',0x06),(36,'F#3',0x05),(40,'A-3',0x04),(44,'D-4',0x03),
               (48,'A-3',0x04),(52,'F#3',0x05),(56,'D-3',0x04),(60,'A-2',0x03)]:
    p[0][r] = note(VO, n, V, v)

# Choir: first layer — a single chord, swelling
for r in [40,44,48,52]:
    vol = max(0x04, 0x0A - (r-40)//4)
    p[1][r] = note(CH, 'D-2', V, vol)

mod.write_pattern(p)

# ============================================================
# PATTERN 1: MORNING — the melody emerges
# ============================================================
p = np()

# Deep drone: steady now
for r in range(0, 64, 12):
    p[3][r] = note(DP, 'D-1', V, 0x0E)

# Harp: flowing arpeggio — D major, gentle
arp_notes = ['D-2','F#2','A-2','D-3','F#3','A-3','F#3','D-3',
             'B-2','D-3','F#3','B-3','D-4','F#4','D-4','B-3',
             'G-2','B-2','D-3','G-3','B-3','D-4','B-3','G-3',
             'A-2','D-3','F#3','A-3','D-4','F#4','D-4','A-3']
for i, n in enumerate(arp_notes):
    r = i * 2
    p[2][r] = note(HP, n, V, max(0x04, 0x0A - (i%8)//2))

# Choir: chord progression — D → Bm → G → A
chords = [(0,'D-2',0x0C),(16,'B-1',0x0A),(32,'G-1',0x0A),(48,'A-1',0x0C)]
for r,n,v in chords:
    p[1][r] = note(CH, n, V, v)
    # add fifths for warmth
    p[1][r+1] = note(CH, n, V, v-2)

# Voice: THE melody — simple, folk-like, modal (D major / B minor)
melody = [
    (0,'D-3',0x10),(2,'F#3',0x0E),(6,'A-3',0x0C),(10,'D-4',0x0E),
    (12,'C#4',0x0C),(14,'B-3',0x0A),(16,'A-3',0x0C),(20,'F#3',0x0A),
    (24,'G-3',0x0E),(28,'A-3',0x0C),(32,'B-3',0x0A),(36,'D-4',0x0C),
    (38,'C#4',0x0A),(40,'B-3',0x0E),(44,'A-3',0x0C),(48,'F#3',0x0A),
    (52,'G-3',0x0C),(56,'A-3',0x0A),(60,'D-3',0x08),(62,'F#3',0x06),
]
for r,n,v in melody:
    p[0][r] = note(VO, n, V, v)

mod.write_pattern(p)

# ============================================================
# PATTERN 2: DAY — full texture, layered harmonies
# ============================================================
p = np()

# Deep drone: full presence
for r in range(0, 64, 8):
    p[3][r] = note(DP, 'D-1', V, 0x12 if r%16==0 else 0x0C)

# Harp: faster ripple — the water quickens
for i in range(64):
    n = arp_notes[i % len(arp_notes)]
    p[2][i] = note(HP, n, V, max(0x04, 0x0C - (i%16)//3))

# Choir: fuller chords — add the third
chords_full = [(0,'D-2',0x10),(16,'B-1',0x0E),(32,'G-1',0x0E),(48,'A-1',0x10)]
for r,n,v in chords_full:
    p[1][r] = note(CH, n, V, v)
    # stack the fifth and third for vocal layering
    try:
        fifth_note = n[:-1] + str(int(n[-1]) + 1)  # up an octave for convenience
        note_to_period(fifth_note)
        p[1][r+1] = note(CH, fifth_note, V, v-3)
    except:
        pass

# Voice: melody with tremolo — floating, ethereal
melody2 = [
    (0,'F#3',0x10),(4,'A-3',0x0E),(8,'D-4',0x10),(12,'F#4',0x0C,TR,0x14),
    (16,'E-4',0x0E),(20,'D-4',0x0C),(24,'B-3',0x0A),(28,'G-3',0x0C),
    (32,'A-3',0x10),(36,'B-3',0x0E),(40,'D-4',0x0C),(44,'F#4',0x0E,TR,0x12),
    (48,'E-4',0x0C),(52,'D-4',0x0A),(56,'B-3',0x08),(60,'D-4',0x06),
]
for r,n,v,*fx in melody2:
    if fx: p[0][r] = note(VO, n, TR, fx[0])
    else: p[0][r] = note(VO, n, V, v)

mod.write_pattern(p)

# ============================================================
# PATTERN 3: TWILIGHT — thinner, more modal (B minor)
# ============================================================
p = np()

# Deep drone: shifts to B — the relative minor
for r in range(0, 64, 12):
    p[3][r] = note(DP, 'B-1', V, 0x0E)

# Harp: sparser — the water settles
for i, n in enumerate(['B-2','D-3','F#3','B-3','F#3','D-3','B-2','F#2',
                         'G-2','B-2','D-3','G-3','D-3','B-2','G-2','D-2',
                         'A-2','C#3','E-3','A-3','E-3','C#3','A-2','E-2',
                         'F#2','A-2','C#3','F#3','C#3','A-2','F#2','C#2']):
    r = i * 2
    p[2][r] = note(HP, n, V, max(0x04, 0x0A - (i%12)//3))

# Choir: B minor progression — more introspective
bm_chords = [(0,'B-1',0x0E),(16,'G-1',0x0C),(32,'A-1',0x0C),(48,'F#1',0x0E)]
for r,n,v in bm_chords:
    p[1][r] = note(CH, n, V, v)

# Voice: gentle, returning — the melody remembers itself
b_minor_melody = [
    (0,'B-3',0x0E),(4,'D-4',0x0C),(8,'F#4',0x0A),(12,'B-4',0x08),
    (16,'A-4',0x0A),(20,'G-4',0x08),(24,'F#4',0x06),(28,'E-4',0x08),
    (32,'D-4',0x0C),(36,'C#4',0x0A),(40,'B-3',0x08),(44,'A-3',0x0C),
    (48,'G-3',0x0E),(52,'F#3',0x0C),(56,'E-3',0x08),(60,'D-3',0x06),
]
for r,n,v in b_minor_melody:
    p[0][r] = note(VO, n, V, v)

mod.write_pattern(p)

# ============================================================
# PATTERN 4: DUSK — returning home, D major again
# ============================================================
p = np()

# Deep drone: returns to D — coming home
for r in range(0, 64, 10):
    vol = 0x12 - r//8
    p[3][r] = note(DP, 'D-1', V, max(0x04, vol))

# Harp: the final ripple — slowing
for i, n in enumerate(['D-2','F#2','A-2','D-3','F#3','A-3','D-4','A-3',
                         'F#3','D-3','A-2','F#2','D-2','A-1','D-2','A-1']):
    r = i * 4
    p[2][r] = note(HP, n, V, max(0x03, 0x0C - i))

# Choir: final chord — D major, swelling, then fading
for r in range(0, 64, 8):
    vol = max(0x04, 0x12 - r//8)
    p[1][r] = note(CH, 'D-2', V, vol)

# Voice: the last phrase — almost a lullaby
for r,n,v in [(0,'D-3',0x0E),(8,'F#3',0x0C),(16,'A-3',0x0A),(24,'D-4',0x08),
               (32,'F#4',0x08),(36,'E-4',0x06),(40,'D-4',0x04),(48,'A-3',0x06),
               (52,'F#3',0x04),(56,'D-3',0x03),(60,'A-2',0x02)]:
    p[0][r] = note(VO, n, V, v)

mod.write_pattern(p)

# ============================================================
# PATTERN 5: NIGHT — dissolve into silence
# ============================================================
p = np()

# Deep drone: last breath
for r in [0,12,24,36]:
    v = max(0x03, 0x0E - r//6)
    p[3][r] = note(DP, 'D-1', V, v)

# Harp: one last arpeggio — very slow, very soft
for i, n in enumerate(['D-2','F#2','A-2','D-3','F#3','A-3','D-4','A-3']):
    r = i * 8
    p[2][r] = note(HP, n, V, max(0x02, 0x08 - i))

# Choir: the final chord, held, fading — volume slide down
p[1][0] = note(CH, 'D-2', VS, 0x04)  # fade down
p[1][16] = note(CH, 'D-2', V, 0x04)

# Voice: the last whisper
for r,n,v in [(0,'D-3',0x08),(8,'F#3',0x06),(16,'A-3',0x04),(24,'D-4',0x03),
               (32,'A-3',0x02),(40,'F#3',0x02),(48,'D-3',0x01)]:
    p[0][r] = note(VO, n, V, v)

mod.write_pattern(p)

mod.order = [0, 1, 1, 2, 2, 3, 1, 2, 4, 5]
mod.write('the-water-between.mod')
print("composed: the water between")
