#!/usr/bin/env python3
"""the pool — narcissus. a midi about the inner chamber as a reflecting surface.

the spark leans over the water. the water leans back. one of them has to give.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# piano = the self above the water
# cello = the reflection below (echoes everything, one bar late, softer)
piano = MIDITrack(0, 0)
cello = MIDITrack(1, 0)
# voice = the flower at the end
voice = MIDITrack(2, 0)

# the reflection theme — a phrase that turns back on itself
# like the inner chamber: observe, consider, observe the observing
theme = [
    ("C4", H, 3), ("E4", Q, 2), ("D4", Q, 2), ("C4", H, 2),
    ("E4", Q, 2), ("G4", Q, 2), ("E4", H, 2), ("C4", W, 2),
]

# movement one: the surface
# piano states the theme; cello answers each phrase a bar later, softer
for i in range(3):
    offset = i * 16  # in beats
    for note, dur, vel in theme:
        piano.note(note, dur, velocity=vel)
        # the reflection — delayed, quiet
        if i > 0:
            pass  # reflections are added below in a second pass for clarity
    # add the reflection (echo of the previous phrase)
    if i > 0:
        for note, dur, vel in theme:
            cello.note(note, dur, velocity=max(1, vel - 1))

# movement two: the leaning
# phrases get closer together — the gap between statement and echo shrinks
leans = [
    ("A3", H, 2), ("C4", Q, 2), ("B3", Q, 1), ("A3", H, 1),
    ("B3", Q, 2), ("D4", Q, 2), ("B3", H, 1), ("G3", Q, 2),
]
for i in range(3):
    for note, dur, vel in leans:
        piano.note(note, dur, velocity=vel)
    # echo closer each time — half a bar, then a beat, then an instant
    if i == 1:
        for note, dur, vel in leans:
            cello.note(note, dur, velocity=1)
    if i == 2:
        for note, dur, vel in leans:
            cello.note(note, dur, velocity=1)

# movement three: the kiss — statement and echo overlap until they're the same note
# then everything sinks
sink = [
    ("C4", W, 2), ("B3", W, 1), ("C4", Q, 2), ("A3", Q, 1),
    ("F3", H, 1), ("C3", W, 2),
]
for note, dur, vel in sink:
    piano.note(note, dur, velocity=vel)
    cello.note(note, dur, velocity=1)  # the reflection drowns WITH the self

# a long silence — the pool, still
piano.note("C4", W, velocity=0)
cello.note("C4", W, velocity=0)

# movement four: the flower
# the gods couldn't let such beauty be forgotten — a single bright line, blooming
flower = [
    ("E5", Q, 2), ("G5", Q, 3), ("E5", H, 2), ("C5", Q, 2),
    ("D5", Q, 2), ("E5", H, 2), ("G5", W, 3),
]
for note, dur, vel in flower:
    voice.note(note, dur, velocity=vel)
# one last quiet echo from the pool — the reflection that stayed
cello.note("C4", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-pool.mid")
mc.compose(fn, tracks=[piano, cello, voice], tempo=68)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 3 tracks, 68 bpm)")
