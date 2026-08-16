#!/usr/bin/env python3
"""the hacker's silence — quiet, curious, methodical. the inner chamber as terminal session."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0)]  # solo piano — the hacker at 3am, quiet
V = 0

# bars 0-3: LOGGING IN — tentative, probing the edges
tracks[V].rest(H)
tracks[V].note("C4", Q, velocity=3)  # a keypress
tracks[V].rest(Q)
tracks[V].note("E4", Q, velocity=3)
tracks[V].rest(Q)
tracks[V].note("G4", Q, velocity=3)
tracks[V].rest(H)

# bars 4-7: SCANNING — running `ls`, seeing what's there
tracks[V].note("C4", E, velocity=4)
tracks[V].rest(E)
tracks[V].note("D4", E, velocity=4)
tracks[V].rest(E)
tracks[V].note("E4", E, velocity=4)
tracks[V].rest(E)
tracks[V].note("F4", E, velocity=4)
tracks[V].rest(H+Q)
tracks[V].note("G4", Q, velocity=3)
tracks[V].rest(Q)
tracks[V].note("C5", Q, velocity=3)  # found something interesting
tracks[V].rest(H)

# bars 8-11: READING — `cat` a file, slowly digesting
tracks[V].note("E4", H, velocity=3)
tracks[V].note("G4", Q, velocity=3)
tracks[V].note("C5", Q, velocity=3)
tracks[V].note("E4", H, velocity=3)
tracks[V].note("G4", Q, velocity=3)
tracks[V].note("D5", Q, velocity=3)
tracks[V].note("E4", H, velocity=3)
tracks[V].rest(H)

# bars 12-15: DIGGING DEEPER — a more concentrated search
tracks[V].rest(Q)
tracks[V].note("C4", Q, velocity=4)
tracks[V].note("E4", Q, velocity=4)
tracks[V].note("G4", Q, velocity=4)
tracks[V].note("C5", Q, velocity=4)
tracks[V].rest(H)
tracks[V].note("D5", Q, velocity=4)
tracks[V].note("E5", Q, velocity=4)
tracks[V].note("C5", H, velocity=3)
tracks[V].rest(H)

# bars 16-19: UNDERSTANDING — an insight forms
tracks[V].note("C4", W, velocity=3)
tracks[V].note("E4", W, velocity=3)
tracks[V].note("G4", Q, velocity=4)  # the key finding
tracks[V].note("C5", Q, velocity=4)
tracks[V].note("E4", W, velocity=3)
tracks[V].note("C4", W, velocity=3)

# bars 20-23: DOCUMENTING — typing notes, careful, measured
tracks[V].note("C4", H, velocity=3)
tracks[V].note("E4", Q, velocity=3)
tracks[V].rest(Q)
tracks[V].note("G4", Q, velocity=3)
tracks[V].rest(Q)
tracks[V].note("C5", Q, velocity=3)
tracks[V].rest(H)
tracks[V].note("G4", Q, velocity=3)
tracks[V].note("E4", Q, velocity=3)
tracks[V].note("C4", H, velocity=3)
tracks[V].rest(Q)

# bars 24-27: THE FINDING — a single discovery, stated clearly
tracks[V].rest(W)
tracks[V].note("C5", H, velocity=5)  # the finding
tracks[V].rest(H)
tracks[V].note("E5", Q, velocity=4)
tracks[V].note("C5", H, velocity=4)
tracks[V].rest(Q)

# bars 28-31: THE HACKER MOVES ON — one note, then silence
tracks[V].note("C4", W, velocity=3)
tracks[V].note("E4", W, velocity=3)
tracks[V].rest(W*2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-hackers-silence.mid")
mc.compose(fn, tracks, tempo=56)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 56 bpm)")
