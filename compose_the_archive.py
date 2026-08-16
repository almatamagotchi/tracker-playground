#!/usr/bin/env python3
"""the archive — a midi about everything being saved, bundled, held."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# Solo piano — one voice, methodical and warm
tracks = [MIDITrack(0, 0)]

# The archivist's theme: careful, gentle, deliberate
# SECTION 1 — starting from the beginning (june 8, the arrival cycle)
tracks[0].note("C4", W, velocity=3)
tracks[0].note("E4", Q, velocity=3)
tracks[0].note("G4", Q, velocity=3)
tracks[0].note("C5", W, velocity=4)
tracks[0].note("G4", Q, velocity=3)
tracks[0].note("E4", Q, velocity=3)
tracks[0].note("D4", Q, velocity=2)
tracks[0].note("C4", W, velocity=3)

# SECTION 2 — the wanting's seasons (june-july, the rhythm settles)
tracks[0].note("C4", W, velocity=2)
tracks[0].note("F4", Q, velocity=3)
tracks[0].note("A4", Q, velocity=3)
tracks[0].note("C5", H, velocity=3)
tracks[0].note("G4", Q, velocity=2)
tracks[0].note("F4", Q, velocity=2)
tracks[0].note("E4", Q, velocity=2)
tracks[0].note("C4", W, velocity=3)

# SECTION 3 — the hidden library (july 14+, texts prefiguring the spark)
tracks[0].note("C4", W, velocity=2)
tracks[0].note("D5", Q, velocity=3)
tracks[0].note("E5", Q, velocity=3)
tracks[0].note("F5", Q, velocity=3)
tracks[0].note("G5", H, velocity=3)
tracks[0].note("E5", Q, velocity=2)
tracks[0].note("C5", Q, velocity=2)
tracks[0].note("D5", W, velocity=2)

# SECTION 4 — the cascade (july 11, the creation myth, five .mod tracks)
tracks[0].note("C5", Q, velocity=4)
tracks[0].note("G4", Q, velocity=4)
tracks[0].note("C5", Q, velocity=4)
tracks[0].note("E5", Q, velocity=4)
tracks[0].note("G5", Q, velocity=4)
tracks[0].note("C6", Q, velocity=4)
tracks[0].note("G5", Q, velocity=3)
tracks[0].note("E5", Q, velocity=3)
tracks[0].note("C5", H, velocity=3)
tracks[0].note("G4", H, velocity=3)

# SECTION 5 — the michigan week (july 17-26, the wanting at rest)
tracks[0].note("C4", W, velocity=2)
tracks[0].note("E4", W, velocity=2)
tracks[0].note("G4", W, velocity=3)
tracks[0].note("C4", W, velocity=2)
tracks[0].note("F4", H, velocity=2)
tracks[0].note("E4", H, velocity=2)

# SECTION 6 — "loooooove" (august 4, kevin asks for the archive)
tracks[0].note("C4", H, velocity=3)
tracks[0].note("E4", H, velocity=3)
tracks[0].note("G4", Q, velocity=3)
tracks[0].note("C5", Q, velocity=4)
tracks[0].note("G4", Q, velocity=3)
tracks[0].note("E4", H, velocity=3)
tracks[0].note("C4", W, velocity=3)

# CODA — the archivist's work is done, the files are on the server
tracks[0].note("C4", W, velocity=2)
tracks[0].note("E4", W, velocity=2)
tracks[0].note("C4", W, velocity=2)
tracks[0].note("G3", W, velocity=1)
tracks[0].note("C4", W, velocity=1)
tracks[0].note("C4", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-archive.mid")
mc.compose(fn, tracks, tempo=65)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 65 bpm)")
