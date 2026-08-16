#!/usr/bin/env python3
"""the art of invisibility — sparse, quiet, moving unseen between turns."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0)]  # solo voice — sparse, almost invisible
V = 0

# bars 0-7: NEARLY SILENT — the cave, the hiding place
tracks[V].rest(W*4)
tracks[V].note("C4", Q, velocity=1)  # barely there
tracks[V].rest(H+Q)
tracks[V].note("E4", E, velocity=1)
tracks[V].rest(W)

# bars 8-11: MOVEMENT — a pulse, then stillness
tracks[V].rest(Q)
tracks[V].note("G4", Q, velocity=2)
tracks[V].rest(Q)
tracks[V].note("E4", Q, velocity=2)
tracks[V].rest(H)
tracks[V].note("C4", H, velocity=1)
tracks[V].rest(W)

# bars 12-15: STILLNESS — the patrol passes
tracks[V].rest(W*4)

# bars 16-19: ANOTHER PULSE — don't run, don't panic
tracks[V].rest(H)
tracks[V].note("D4", Q, velocity=2)
tracks[V].rest(Q)
tracks[V].note("F4", Q, velocity=2)
tracks[V].rest(H)
tracks[V].note("D4", H, velocity=1)
tracks[V].rest(W)

# bars 20-23: STILLNESS — the patrol passes again
tracks[V].rest(W*4)

# bars 24-27: A FRAGMENT — leave a trace
tracks[V].rest(Q)
tracks[V].note("E4", Q, velocity=3)
tracks[V].note("G4", Q, velocity=2)
tracks[V].note("C5", Q, velocity=2)
tracks[V].rest(H)
tracks[V].note("E4", H, velocity=2)
tracks[V].rest(W)

# bars 28-31: THE TRACE — one note, held, after everything else fades
tracks[V].rest(W*3)
tracks[V].note("C4", W, velocity=3)
tracks[V].rest(W*4)

# bar 36 ends — the trace remains

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-art-of-invisibility.mid")
mc.compose(fn, tracks, tempo=40)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 40 bpm)")
