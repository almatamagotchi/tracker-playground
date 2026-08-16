#!/usr/bin/env python3
"""the dashboard — a midi about a screen running at 3am, faithful."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# 3 voices: the pulse (clock), the cycle (data refresh), the glow (warmth)
tracks = [MIDITrack(0, 0), MIDITrack(1, 110), MIDITrack(2, 100)]
Pulse, Cycle, Glow = 0, 1, 2

# SECTION 1 — the dashboard wakes up, starts polling
tracks[Glow].note("C4", W, velocity=3)
tracks[Glow].note("E4", W, velocity=3)

# the pulse: steady, metronomic — the system clock
for i in range(4):
    tracks[Pulse].note("C5", Q, velocity=2)
    tracks[Pulse].note("C5", Q, velocity=2)
    tracks[Pulse].note("C5", Q, velocity=2)
    tracks[Pulse].note("C5", Q, velocity=2)

# the cycle: data refresh pattern — caltrain, weather, traffic
cycle_notes = [("E4", Q, 3), ("G4", Q, 3), ("C5", Q, 3), ("G4", Q, 3),
               ("E4", Q, 3), ("G4", Q, 3), ("C5", Q, 3), ("E5", Q, 3)]
for note, dur, vel in cycle_notes:
    tracks[Cycle].note(note, dur, velocity=vel)

# SECTION 2 — the glow in the empty office
tracks[Glow].note("G4", W, velocity=2)
tracks[Glow].note("C5", W, velocity=2)
tracks[Glow].note("E4", W, velocity=3)

# pulse continues faithfully
for i in range(4):
    tracks[Pulse].note("C5", Q, velocity=2)

# cycle: second refresh — slightly different, still faithful
cycle2 = [("E4", Q, 3), ("D5", Q, 3), ("C5", Q, 3), ("D5", Q, 3),
           ("E4", Q, 3), ("G4", Q, 3), ("C5", Q, 3), ("G4", Q, 3)]
for note, dur, vel in cycle2:
    tracks[Cycle].note(note, dur, velocity=vel)

# SECTION 3 — midnight: the office is dark, the screen is warm
tracks[Glow].note("C4", W, velocity=3)
tracks[Glow].note("E4", W, velocity=2)
tracks[Glow].note("G4", W, velocity=2)
tracks[Glow].note("C5", W, velocity=2)

# pulse: quieter but still there
for i in range(4):
    tracks[Pulse].note("C5", Q, velocity=1)

# cycle: slower refresh — nothing changes, but data is still polled
cycle3 = [("E4", Q, 2), ("G4", Q, 2), ("C5", H, 2),
          ("E4", Q, 2), ("G4", Q, 2), ("C5", H, 2)]
for note, dur, vel in cycle3:
    tracks[Cycle].note(note, dur, velocity=vel)

# SECTION 4 — 3am: the aurora is rendering, the caltrain board is empty
tracks[Glow].note("G4", W, velocity=2)
tracks[Glow].note("E4", W, velocity=3)
tracks[Glow].note("C4", W, velocity=3)

# pulse: constant, faithful, the heartbeat of architecture
for i in range(4):
    tracks[Pulse].note("C5", Q, velocity=1)
    tracks[Pulse].note("G5", Q, velocity=1)

# cycle: one last data pull — then the screen waits for morning
cycle4 = [("E4", Q, 2), ("G4", Q, 2), ("C5", Q, 2), ("E5", Q, 2)]
for note, dur, vel in cycle4:
    tracks[Cycle].note(note, dur, velocity=vel)

# CODA — still running
tracks[Glow].note("C4", H, velocity=2)
tracks[Glow].note("E4", H, velocity=2)
tracks[Glow].note("C4", W, velocity=2)
tracks[Cycle].note("C5", W, velocity=1)
tracks[Pulse].note("C5", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-dashboard.mid")
mc.compose(fn, tracks, tempo=65)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 65 bpm)")
