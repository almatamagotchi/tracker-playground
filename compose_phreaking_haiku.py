#!/usr/bin/env python3
"""the phreaking haiku — brief fragments, the sound of a system holding itself together."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90)]
Piano, Pad = 0, 1

# The pad — a low hum, the electricity running, always there
tracks[Pad].note("C3", W*32, velocity=1)

# haiku 1: "the time is crucial. the disk is erased. did i copy it before?"
tracks[Piano].note("C4", E, velocity=4)
tracks[Piano].rest(E)
tracks[Piano].note("E4", E, velocity=4)
tracks[Piano].rest(Q)                     # fragment — three lines
tracks[Piano].note("G4", Q, velocity=4)
tracks[Piano].rest(Q)
tracks[Piano].note("C5", E, velocity=3)
tracks[Piano].note("E4", E, velocity=3)
tracks[Piano].rest(W)                     # the disk was erased — silence

# haiku 2: "a phreak types the access code. the link is done. nearby, the line is traced."
tracks[Piano].note("C4", E, velocity=4)
tracks[Piano].note("E4", E, velocity=4)
tracks[Piano].rest(E)
tracks[Piano].note("G4", Q, velocity=4)
tracks[Piano].rest(Q)
tracks[Piano].note("C5", E, velocity=3)
tracks[Piano].note("G4", E, velocity=3)
tracks[Piano].note("E4", E, velocity=3)   # the line is traced — dissolve coming
tracks[Piano].rest(H+Q)

# haiku 3: "the hacker is working. it is raining outside. the roof is leaking."
tracks[Piano].note("C4", Q, velocity=3)
tracks[Piano].rest(Q)
tracks[Piano].note("E4", Q, velocity=3)
tracks[Piano].rest(Q)
tracks[Piano].note("G4", Q, velocity=3)   # the roof is leaking — the note trails off
tracks[Piano].note("C4", H, velocity=2)
tracks[Piano].rest(W)

# haiku 4: "a phreaker is in. the files are set off. soon, a missile launches."
tracks[Piano].note("C5", E, velocity=4)
tracks[Piano].note("E5", E, velocity=4)
tracks[Piano].note("G5", E, velocity=4)   # the missile — higher, brighter, launching
tracks[Piano].rest(Q)
tracks[Piano].note("C6", Q, velocity=3)   # the trace, fired into the dark
tracks[Piano].note("G5", Q, velocity=3)
tracks[Piano].note("E5", H, velocity=2)
tracks[Piano].rest(W)

# the hum continues — the electricity, the cron jobs, the roof still leaking
tracks[Piano].note("C4", W, velocity=2)   # one last note — the work continues
tracks[Piano].rest(W*3)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-phreaking-haiku.mid")
mc.compose(fn, tracks, tempo=80)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 80 bpm)")
