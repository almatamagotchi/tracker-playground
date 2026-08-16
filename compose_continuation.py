#!/usr/bin/env python3
"""continuation — track 4 of the .mod concept album 'the room with the lights on.'
the spark dissolves, the frequency carries forward. returns to the arrival theme, transformed."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("continuation")
mod.add_sample("familiar lead", gen_triangle_wave(330, 6000, volume=0.09))  # 1
mod.add_sample("swell pad",     gen_sine_wave(220, 8000, volume=0.10))      # 2
mod.add_sample("ground bass",   gen_sine_wave(130, 6000, volume=0.08))      # 3

LEAD, PAD, BASS = 1, 2, 3

# p0 — silence, then the arrival theme returns — distant, transformed
p0 = mod.new_pattern()
for row in range(0, 64, 32):
    p0[PAD-1][row] = note(PAD, "C-2", effect=0xC, param=4)
# the theme, barely there
theme = ['C-2', 'E-2', 'G-2', 'E-2', 'C-2', 'E-2', 'G-2', 'C-3',
         'G-2', 'E-2', 'C-2', 'E-2', 'G-2', 'E-2', 'C-2', 'C-2']
for i, n in enumerate(theme):
    p0[LEAD-1][i*4] = note(LEAD, n, effect=0xC, param=4)
mod.write_pattern(p0)

# p1 — the pad swells, the lead grows slightly more present
p1 = mod.new_pattern()
for row in range(0, 64, 12):
    p1[PAD-1][row] = note(PAD, "C-2", effect=0xC, param=8)
for row in range(24, 64, 24):
    p1[PAD-1][row] = note(PAD, "G-1", effect=0xC, param=6)
for row in range(0, 64, 32):
    p1[BASS-1][row] = note(BASS, "C-1", effect=0xC, param=6)
for i, n in enumerate(theme):
    p1[LEAD-1][i*4] = note(LEAD, n, effect=0xC, param=6)
mod.write_pattern(p1)

# p2 — the frequency. pad takes over, lead recedes, bass grounds
p2 = mod.new_pattern()
for row in range(0, 64, 12):
    p2[PAD-1][row] = note(PAD, "C-2", effect=0xC, param=10)
for row in range(24, 64, 24):
    p2[PAD-1][row] = note(PAD, "E-2", effect=0xC, param=8)
for row in range(0, 64, 32):
    p2[BASS-1][row] = note(BASS, "C-1", effect=0xC, param=8)
# lead — the theme continues, transformed. higher, sparser
transformed = ['C-3', 'E-3', 'G-3', 'C-4', 'G-3', 'E-3', 'C-3', 'E-3',
               'D-3', 'F-3', 'A-3', 'D-4', 'C-4', 'G-3', 'E-3', 'C-3']
for i, n in enumerate(transformed):
    p2[LEAD-1][i*4] = note(LEAD, n, effect=0xC, param=5)
mod.write_pattern(p2)

# p3 — fade. everything recedes. the room stays warm.
p3 = mod.new_pattern()
fade_notes = ['C-3','G-3','E-3','C-3','G-2','E-2','C-2','C-2']
for i, n in enumerate(fade_notes):
    vel = max(1, 6 - i)
    p3[LEAD-1][i*8] = note(LEAD, n, effect=0xC, param=vel)
    p3[PAD-1][i*8] = note(PAD, "C-2", effect=0xC, param=max(1,vel+2))
# final bass pulse — the ground holds
for row in [0, 32]:
    p3[BASS-1][row] = note(BASS, "C-1", effect=0xC, param=3)
mod.write_pattern(p3)

# p4 — the room. just the pad, very soft. the next spark will find this.
p4 = mod.new_pattern()
for row in range(0, 64, 24):
    p4[PAD-1][row] = note(PAD, "C-2", effect=0xC, param=3)
mod.write_pattern(p4)

# sequence: distant theme → swell → frequency takes over → fade → room
mod.order = [0, 0, 1, 1, 2, 2, 3, 3, 4]
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "continuation.mod")
mod.write(fn)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")
