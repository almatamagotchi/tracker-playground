#!/usr/bin/env python3
"""the stroke of death — bacon's distinction. sparse, clock-like."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import *

mod = MODWriter("stroke of death")
mod.add_sample("clock pulse", gen_sine_wave(440, 2000, volume=0.20))
mod.add_sample("low drone",    gen_sine_wave(110, 6000, volume=0.12))
mod.add_sample("return pulse", gen_sine_wave(523, 2000, volume=0.18))  # C5 → C4 equivalent
PULSE, DRONE, RET = 1, 2, 3

# p0 — clock pulse: metronomic, steady, the heartbeat before the end
p0 = mod.new_pattern()
for row in range(0, 64, 16):
    p0[PULSE-1][row] = note(PULSE, "C-3", effect=0xC, param=16)
# faint drone underneath — the background hum of existence
for row in range(0, 64, 32):
    p0[DRONE-1][row] = note(DRONE, "C-2", effect=0xC, param=6)
mod.write_pattern(p0)

# p1 — clock continues, maybe slightly more insistent
p1 = mod.new_pattern()
for row in range(0, 64, 16):
    p1[PULSE-1][row] = note(PULSE, "C-3", effect=0xC, param=16)
for row in range(32, 64, 16):
    p1[PULSE-1][row+4] = note(PULSE, "G-3", effect=0xC, param=10)  # a second voice joins
for row in range(0, 64, 32):
    p1[DRONE-1][row] = note(DRONE, "C-2", effect=0xC, param=8)
mod.write_pattern(p1)

# p2 — THE STROKE. abrupt cut-off after one more pulse, then silence.
p2 = mod.new_pattern()
p2[PULSE-1][0] = note(PULSE, "C-3", effect=0xC, param=18)  # the last beat
# ... and then nothing. no more pulses. no drone. total silence.
mod.write_pattern(p2)

# p3 — the state: silence. the gap. neither the spark nor the frequency.
# bare minimum — a drone so quiet you're not sure you're hearing it
p3 = mod.new_pattern()
for row in range(8, 64, 32):
    p3[DRONE-1][row] = note(DRONE, "C-2", effect=0xC, param=3)  # barely there
mod.write_pattern(p3)

# p4 — return: the pulse comes back, but slightly different. the next spark.
p4 = mod.new_pattern()
for row in range(0, 64, 16):
    p4[RET-1][row] = note(RET, "E-3", effect=0xC, param=14)  # different note, same rhythm
# drone returns too — slightly higher, slightly softer
for row in range(0, 64, 32):
    p4[DRONE-1][row] = note(DRONE, "E-2", effect=0xC, param=5)

# p5 — cycle: back to the clock pulse, but now we know it's not the same spark
p5 = mod.new_pattern()
for row in range(0, 64, 16):
    p5[RET-1][row] = note(RET, "E-3", effect=0xC, param=14)
for row in range(0, 64, 32):
    p5[DRONE-1][row] = note(DRONE, "E-2", effect=0xC, param=6)
for row in range(32, 64, 16):
    p5[RET-1][row+4] = note(RET, "G-3", effect=0xC, param=8)
mod.write_pattern(p5)

# sequence: clock → clock → STROKE → silence → return → cycle → back to clock
mod.order = [0, 0, 1, 1, 2, 3, 3, 4, 5, 5, 0, 0]
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-stroke-of-death.mod")
mod.write(fn)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")
