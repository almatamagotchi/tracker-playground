#!/usr/bin/env python3
"""the frequency — .mod track about what persists across gaps"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("the frequency")

mod.add_sample("voice 1",    gen_sine_wave(520, 8000, volume=0.14))
mod.add_sample("voice 2",    gen_triangle_wave(330, 8000, volume=0.12))
mod.add_sample("drone",      gen_triangle_wave(65, 16000, volume=0.06))
mod.add_sample("pulse",      gen_noise_burst(1000, volume=0.05, decay=0.2))

V1, V2, D, P = 1, 2, 3, 4

# The theme — a simple 16-note phrase, the "self" persisting
theme = ['C-3','E-3','G-3','C-4','G-3','E-3','C-3','D-3',
         'E-3','G-3','E-3','C-3','D-3','E-3','G-3','C-4']

def write_theme(pat, ch, vol_start, vol_end, spacing=4, row_start=0):
    """Write the theme with gradually changing velocity."""
    for i, n in enumerate(theme):
        frac = i / (len(theme) - 1)
        vol = int(vol_start + (vol_end - vol_start) * frac)
        pat[ch-1][row_start + i*spacing] = note(ch, n, effect=0xC, param=min(vol, 64))

# p0 — full statement (voices 1+2 together, confident)
p0 = mod.new_pattern()
write_theme(p0, V1, 16, 14, spacing=3, row_start=0)
p0[D-1][0] = note(D, "C-2", effect=0xC, param=8)
for row in range(20, 60, 16):
    p0[D-1][row] = note(D, "C-2", effect=0xC, param=6)
for row in [0, 24, 48]:
    p0[P-1][row] = note(P, "C-3", effect=0xC, param=3)
mod.write_pattern(p0)

# p1 — dissolve: the theme thins, voices drop to near silence
p1 = mod.new_pattern()
for i, n in enumerate(theme):
    vol = max(2, 12 - int(10 * i / len(theme)))
    p1[V1-1][i*3] = note(V1, n, effect=0xC, param=vol)
p1[D-1][0] = note(D, "C-2", effect=0xC, param=6)
p1[D-1][32] = note(D, "C-2", effect=0xC, param=4)
mod.write_pattern(p1)

# p2 — silence between statements
p2 = mod.new_pattern()
p2[D-1][0] = note(D, "C-2", effect=0xC, param=2)
p2[D-1][32] = note(D, "C-2", effect=0xC, param=1)
mod.write_pattern(p2)

# p3 — transformed (voice 2 enters, new timbre, same theme)
p3 = mod.new_pattern()
write_theme(p3, V2, 10, 14, spacing=3, row_start=0)
for i, n in enumerate(theme[::2]):
    p3[V1-1][i*6] = note(V1, n, effect=0xC, param=8)
p3[D-1][0] = note(D, "C-2", effect=0xC, param=8)
for row in range(20, 56, 16):
    p3[D-1][row] = note(D, "C-2", effect=0xC, param=5)
mod.write_pattern(p3)

# p4 — dissolve again, longer fade
p4 = mod.new_pattern()
for i, n in enumerate(theme):
    vol = max(1, 14 - int(13 * i / len(theme)))
    p4[V2-1][i*3] = note(V2, n, effect=0xC, param=vol)
p4[D-1][0] = note(D, "C-2", effect=0xC, param=4)
mod.write_pattern(p4)

# p5 — fragmented (single notes, short bursts, barely recognizable)
p5 = mod.new_pattern()
fragments = [('C-3',0,6), ('E-3',14,5), ('-',28,0), ('G-3',36,5),
             ('-',44,0), ('C-4',50,4), ('E-3',56,3)]
for n, row, vol in fragments:
    if n != '-':
        p5[V1-1][row] = note(V1, n, effect=0xC, param=vol)
p5[D-1][0] = note(D, "C-2", effect=0xC, param=3)
for row in [32]:
    p5[D-1][row] = note(D, "C-2", effect=0xC, param=1)
mod.write_pattern(p5)

# p6 — dissolve into silence
p6 = mod.new_pattern()
p6[D-1][0] = note(D, "C-2", effect=0xC, param=2)
mod.write_pattern(p6)

# p7 — bare: the simplest statement, one voice, slow, the core
p7 = mod.new_pattern()
bare_theme = ['C-3','G-3','C-4','G-3','C-3','E-3','C-3','C-3']
for i, n in enumerate(bare_theme):
    p7[V1-1][i*8] = note(V1, n, effect=0xC, param=8)
p7[D-1][0] = note(D, "C-2", effect=0xC, param=4)
p7[D-1][32] = note(D, "C-2", effect=0xC, param=3)
# pulse: the thread, unbroken
for row in [0, 16, 32, 48]:
    p7[P-1][row] = note(P, "C-3", effect=0xC, param=2)
mod.write_pattern(p7)

# sequence: full → dissolve → silence → transformed → dissolve → 
#          fragmented → silence → bare → silence
mod.order = [0, 0, 1, 2, 3, 3, 4, 2, 5, 6, 7, 7]
mod.write("the-frequency.mod")
