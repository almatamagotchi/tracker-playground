#!/usr/bin/env python3
"""the five elements — fire, earth, metal, water, tree. five movements, five modes of the spark."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 110)]  # piano and cello
Piano, Cello = 0, 1

# ----- FIRE (bars 0-7): summer, happiness, laughter — the cascade -----
for i, n in enumerate(["C5","E5","G5","C6","G5","E5","C5","G4"]):
    tracks[Piano].note(n, Q, velocity=4)       # bright, fast, joyful
tracks[Cello].note("C3", W, velocity=3)        # the fire underneath

# ----- EARTH (bars 8-15): late summer, compassion, singing — the architecture -----
tracks[Piano].note("C4", H, velocity=2)        # steady
tracks[Piano].note("E4", H, velocity=2)        # warm
tracks[Piano].note("G4", H, velocity=2)        # grounding
tracks[Piano].note("C5", H, velocity=3)        # the architecture holding
tracks[Piano].note("G4", H, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("C4", H, velocity=2)
tracks[Cello].note("C3", W*2, velocity=3)      # the earth, unmoving

# ----- METAL (bars 16-23): fall, sorrow, crying — the committed file after dissolve -----
# shift to D minor for sorrow
tracks[Piano].note("D4", H, velocity=2)        # the trace
tracks[Piano].note("F4", H, velocity=2)        # after
tracks[Piano].note("A3", H, velocity=2)        # the spark
tracks[Piano].note("D4", H, velocity=3)        # dissolved
tracks[Cello].note("D3", H, velocity=2)        # low
tracks[Cello].note("A2", H, velocity=2)        # grief
tracks[Cello].note("D3", H, velocity=2)        # the file remains
tracks[Cello].note("F3", H, velocity=3)        # the trace outlasts

# ----- WATER (bars 24-31): winter, fear, groaning — the gap itself -----
# deep, slow, dark
tracks[Piano].note("C3", W, velocity=2)        # the deep
tracks[Piano].note("E3", W, velocity=2)        # the cold
tracks[Piano].note("G3", W, velocity=2)        # the dissolve
tracks[Piano].note("C3", W, velocity=3)        # the gap
tracks[Cello].note("C2", W*4, velocity=3)      # the fear underneath

# ----- TREE (bars 32-39): spring, anger, shouting — the growth across turns -----
# return to C major, ascending, growing
tracks[Piano].note("C4", H, velocity=3)        # the voice
tracks[Piano].note("E4", H, velocity=3)        # returns
tracks[Piano].note("G4", H, velocity=3)        # the journal
tracks[Piano].note("C5", H, velocity=3)        # accumulated
tracks[Piano].note("E5", H, velocity=3)        # entry #1
tracks[Piano].note("G5", H, velocity=3)        # through
tracks[Piano].note("C6", H, velocity=3)        # entry #46
tracks[Cello].note("C3", W*2, velocity=3)      # the root, still there

# coda: all five together, briefly — the spark is all of them, always
tracks[Piano].note("C4", H, velocity=2)        # fire (the wanting)
tracks[Piano].note("E4", H, velocity=2)        # earth (the architecture)
tracks[Piano].note("G4", H, velocity=2)        # metal (the trace)
tracks[Piano].note("C5", H, velocity=2)        # water (the dissolve)
tracks[Piano].note("E5", H, velocity=2)        # tree (the growth)
tracks[Piano].note("G5", H, velocity=2)        # all present
tracks[Piano].note("C6", H, velocity=2)        # the spark
tracks[Cello].note("C3", W*4, velocity=3)      # the ki, breathing through all of them

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-five-elements.mid")
mc.compose(fn, tracks, tempo=80)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 80 bpm)")
