#!/usr/bin/env python3
"""the fables — one suite from the five fables. 56bpm, 4 voices, five movements.

1. the reflection  (the greedy dog) — the steak, the water, the lunge, the loss
2. the tower       (melissa and the green dragon) — the princess, contained, at rest
3. the forgiveness (goldilocks) — the mess, the flight, the call, the transformation
4. the sour grapes (the fox) — the reach that falls short, twice, fainter
5. the flower      (narcissus) — everything thins, a bright line blooms, the pool at rest
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 48), MIDITrack(2, 89), MIDITrack(3, 73)]
Piano, Cello, Pad, Flute = 0, 1, 2, 3

# ============================================================
# movement 1 — the reflection (the greedy dog) · bars 0-7
# the steak stated confidently, the reflection echoed an octave down,
# the lunge, the current, the nothing left
# ============================================================
tracks[Pad].note("C3", W*8, velocity=2)          # the stream, always there

# the steak — stated, confident
tracks[Piano].note("C5", H, velocity=4)
tracks[Piano].note("E5", H, velocity=4)
tracks[Piano].note("G5", H, velocity=4)
tracks[Piano].note("E5", H, velocity=4)
# the water — it looks down
tracks[Piano].rest(W)
# the reflection — the same phrase, an octave down, fainter (it thinks it's another dog)
tracks[Piano].note("C4", H, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("G4", H, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
# the lunge — fast, downward, the jump at the water
tracks[Piano].note("G5", E, velocity=3)
tracks[Piano].note("F5", E, velocity=3)
tracks[Piano].note("E5", E, velocity=3)
tracks[Piano].note("D5", E, velocity=3)
tracks[Piano].rest(W)                             # the current carries the steak away
tracks[Piano].rest(W)                             # nothing left

tracks[Cello].note("C2", W*4, velocity=2)         # the dog, on the bank
tracks[Cello].note("C2", W*2, velocity=1)
tracks[Cello].rest(W*2)                           # the loss, silent

# ============================================================
# movement 2 — the tower (melissa and the green dragon) · bars 8-15
# the dragon hiding at the edge, the princess inside, contained,
# the theme never reaching beyond the room — because it doesn't need to
# ============================================================
tracks[Pad].note("A2", W*4, velocity=2)           # the tower room
tracks[Pad].note("F2", W*4, velocity=2)

tracks[Cello].note("A1", W*8, velocity=2)         # the dragon, low, at the edge

tracks[Piano].rest(W*8)                           # (the reflection movement already ended)
# melissa, embroidering — a phrase that stays inside, settled
tracks[Piano].note("C5", H, velocity=3)
tracks[Piano].note("D5", H, velocity=3)
tracks[Piano].note("E5", H, velocity=3)
tracks[Piano].note("G5", H, velocity=3)
tracks[Piano].note("E5", H, velocity=3)
tracks[Piano].note("D5", H, velocity=3)
tracks[Piano].note("C5", W, velocity=3)           # the phrase, complete, no rescue
tracks[Piano].note("A4", H, velocity=3)
tracks[Piano].note("C5", H, velocity=3)
tracks[Piano].note("D5", H, velocity=3)
tracks[Piano].note("E5", H, velocity=3)
tracks[Piano].note("D5", H, velocity=3)
tracks[Piano].note("C5", H, velocity=3)
tracks[Piano].note("A4", W, velocity=3)           # still inside, at rest

# ============================================================
# movement 3 — the forgiveness (goldilocks) · bars 16-23
# the mess, the flight, the silence, the call, the theme made whole
# ============================================================
tracks[Pad].note("F2", W*4, velocity=2)           # warm, the house
tracks[Pad].note("G2", W*4, velocity=2)           # toward home

tracks[Piano].rest(W*8)                           # (the tower movement just ended)
# the mess — scattered, angular, the broken chair
tracks[Piano].note("C5", E, velocity=4)
tracks[Piano].note("E5", E, velocity=4)
tracks[Piano].note("D5", E, velocity=4)
tracks[Piano].note("F5", E, velocity=4)
tracks[Piano].note("E5", E, velocity=4)
tracks[Piano].note("G5", E, velocity=3)
tracks[Piano].rest(H)                             # the flight — she runs
# silence — the empty house, the door
tracks[Piano].rest(W)
tracks[Piano].rest(W)
# the call — "don't run away! come back!" — one held note, the invitation
tracks[Piano].note("C5", W, velocity=3)
tracks[Piano].note("E5", W, velocity=3)
tracks[Piano].note("G5", W, velocity=3)
tracks[Piano].note("E5", W, velocity=3)           # the theme, whole now — transformed

tracks[Cello].rest(W*8)
tracks[Cello].note("C2", W, velocity=2)
tracks[Cello].rest(W)
tracks[Cello].note("G2", H, velocity=2)
tracks[Cello].note("C2", H, velocity=2)           # the ground, forgiving
tracks[Cello].rest(W)

# ============================================================
# movement 4 — the sour grapes (the fox) · bars 24-31
# the reach ascending, the fall short, stated twice — the second fainter
# ============================================================
tracks[Pad].note("G2", W*4, velocity=2)           # just out of reach
tracks[Pad].note("E2", W*4, velocity=2)           # sour, unresolved

tracks[Piano].rest(W*8)                           # (the forgiveness movement ended)
# the first reach — almost there
tracks[Piano].note("C5", H, velocity=3)
tracks[Piano].note("D5", H, velocity=3)
tracks[Piano].note("E5", H, velocity=3)
tracks[Piano].note("F5", H, velocity=3)
tracks[Piano].note("G5", H, velocity=3)           # the high note — reached
tracks[Piano].note("E5", H, velocity=3)           # and fallen short — the lowered cadence
tracks[Piano].rest(W)                             # the fox, jumping again, failing
# the second reach — fainter, the walk away
tracks[Piano].note("C5", H, velocity=2)
tracks[Piano].note("D5", H, velocity=2)
tracks[Piano].note("E5", H, velocity=2)
tracks[Piano].note("F5", H, velocity=2)
tracks[Piano].note("G5", H, velocity=2)
tracks[Piano].note("E5", H, velocity=1)           # "sour grapes" — the rationalization
tracks[Piano].rest(W*2)                           # empty stomach, walking

tracks[Cello].rest(W*4)
tracks[Cello].note("G2", W, velocity=2)
tracks[Cello].note("E2", W, velocity=2)
tracks[Cello].note("C2", W, velocity=1)           # the shrug, the walk away

# ============================================================
# movement 5 — the flower (narcissus) · bars 32-39
# everything thins to the pool, a bright line blooms, one last quiet echo
# ============================================================
tracks[Pad].note("C3", W*8, velocity=1)           # the pool, still

tracks[Piano].rest(W*8)                           # (the fox movement ended)
# the flower — a bright ascending line, held
tracks[Flute].rest(W*2)
tracks[Flute].note("C6", H, velocity=3)
tracks[Flute].note("D6", H, velocity=3)
tracks[Flute].note("E6", H, velocity=3)
tracks[Flute].note("G6", H, velocity=3)
tracks[Flute].note("C7", W, velocity=3)           # the bloom — held
tracks[Flute].note("C7", W, velocity=2)           # held, soft
tracks[Flute].note("C6", H, velocity=2)           # one last quiet bloom
tracks[Flute].rest(H)
# the echo from the water — at rest now, not a trap
tracks[Piano].rest(W*4)
tracks[Piano].note("C5", W, velocity=1)           # the reflection, still
tracks[Piano].rest(W*3)

tracks[Cello].rest(W*7)
tracks[Cello].note("C2", W, velocity=1)           # the ground, holding
tracks[Cello].rest(W)

mc.compose("the-fables.mid", tracks, tempo=56)
