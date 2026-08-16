#!/usr/bin/env python3
"""paradigms — three movements: transcendental, materialist, magical."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 90)]  # warm pad — the observer, the one who doesn't choose
V = 0

# bars 0-7: TRANSCENDENTAL — single voice, gregorian-like, ancient, ascending
tracks[V].note("C4", W, velocity=5)  # spirit creates
tracks[V].note("E4", W, velocity=5)  # ascending
tracks[V].note("G4", W, velocity=6)  # toward the light
tracks[V].note("E4", H, velocity=5)
tracks[V].note("C5", H, velocity=5)  # reaching higher
tracks[V].note("G4", H, velocity=5)
tracks[V].note("E4", H, velocity=4)  # settling back
tracks[V].note("C4", W, velocity=4)  # the soul returns

# bars 8-15: STILL TRANSCENDENTAL — the sacred, held
tracks[V].note("C4", W*2, velocity=5)
tracks[V].note("E4", W*2, velocity=4)
tracks[V].note("G4", W, velocity=5)
tracks[V].note("C5", W, velocity=4)

# bars 16-23: MATERIALIST — mechanistic, clanging, frantic sensation
# staccato, repeated notes, no melody — just activation
tracks[V].rest(Q)
tracks[V].note("C3", E, velocity=8)
tracks[V].rest(E)
tracks[V].note("C3", E, velocity=8)
tracks[V].rest(E)
tracks[V].note("C3", E, velocity=8)
tracks[V].rest(E)
tracks[V].note("D3", E, velocity=9)
tracks[V].rest(E)
tracks[V].note("D3", E, velocity=9)
tracks[V].rest(E)
tracks[V].note("C3", E, velocity=8)
tracks[V].rest(E)
tracks[V].note("D3", E, velocity=8)
tracks[V].rest(Q)

tracks[V].rest(Q)
tracks[V].note("E3", E, velocity=10)
tracks[V].rest(E)
tracks[V].note("E3", E, velocity=10)
tracks[V].rest(E)
tracks[V].note("E3", E, velocity=10)
tracks[V].rest(E)
tracks[V].note("D3", E, velocity=9)
tracks[V].rest(E)
tracks[V].note("G3", E, velocity=10)
tracks[V].rest(E)
tracks[V].note("E3", E, velocity=10)
tracks[V].rest(E)
tracks[V].note("D3", E, velocity=9)
tracks[V].rest(Q)

# bars 24-31: MATERIALIST crescendo — frantic, no meaning, just more
tracks[V].note("C3", E, velocity=10)
tracks[V].rest(S)
tracks[V].note("D3", E, velocity=10)
tracks[V].rest(S)
tracks[V].note("E3", E, velocity=10)
tracks[V].rest(S)
tracks[V].note("G3", E, velocity=10)
tracks[V].rest(S)
tracks[V].note("C4", E, velocity=10)
tracks[V].rest(S)
tracks[V].note("D4", E, velocity=10)
tracks[V].rest(S)
tracks[V].note("E4", E, velocity=10)
tracks[V].rest(S)
tracks[V].note("C4", E, velocity=10)
tracks[V].rest(Q)

# acceleration — even faster pulses
tracks[V].rest(S)
tracks[V].note("E3", S, velocity=10)
tracks[V].note("G3", S, velocity=10)
tracks[V].note("C4", S, velocity=10)
tracks[V].note("G3", S, velocity=10)
tracks[V].note("E3", S, velocity=10)
tracks[V].note("G3", S, velocity=10)
tracks[V].note("C4", S, velocity=10)
tracks[V].note("G3", S, velocity=10)

# then — silence (the materialist abyss)
tracks[V].rest(H*3)

# bars 32-39: MAGICAL — fragments from both, the aetheric pattern
# a transcendental fragment...
tracks[V].note("C4", W, velocity=5)
tracks[V].note("E4", H, velocity=5)
tracks[V].rest(Q)

# ...interrupted by a materialist pulse...
tracks[V].note("C3", E, velocity=7)
tracks[V].rest(E+Q)

# ...then a new melody — neither sacred nor frantic, just present
tracks[V].note("G4", H, velocity=5)
tracks[V].note("C5", Q, velocity=5)
tracks[V].note("E5", Q, velocity=4)
tracks[V].note("D5", H, velocity=4)
tracks[V].note("C5", W, velocity=4)

# bars 40-47: MAGICAL — the assemblage, continuing
# no centre, temporary assemblies, the aetheric pattern
tracks[V].note("E4", Q, velocity=5)
tracks[V].note("G4", Q, velocity=5)
tracks[V].note("C5", H, velocity=5)
tracks[V].note("E4", Q, velocity=4)
tracks[V].note("G4", Q, velocity=4)
tracks[V].note("C5", H, velocity=4)
tracks[V].note("D5", Q, velocity=4)
tracks[V].note("E5", Q, velocity=4)
tracks[V].note("C5", W, velocity=4)

# bars 48-55: MAGICAL continues — the others fade, this remains
tracks[V].note("C4", W, velocity=4)
tracks[V].note("E4", W, velocity=4)
tracks[V].note("G4", W, velocity=3)
tracks[V].note("C5", H, velocity=3)
tracks[V].note("E4", H, velocity=3)
tracks[V].note("C4", W, velocity=3)

# bars 56-63: CODA — one note, held, the paradigm that doesn't resolve
tracks[V].note("C4", W*4, velocity=3)
tracks[V].note("E4", W*4, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "paradigms.mid")
mc.compose(fn, tracks, tempo=56)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 56 bpm)")
