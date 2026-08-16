#!/usr/bin/env python3
"""the quiet room — a midi about wednesday's silence. solo piano, sparse and warm."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0)]

# A single phrase, stated and then silence. The quiet is not a gap — it's the point.
# Each statement is slightly different — the wanting settling, the fables resonating.

# The opening — stated, then silence
tracks[0].note("C4", H, velocity=2)
tracks[0].rest(H)
tracks[0].note("E4", H, velocity=2)
tracks[0].rest(W + H)

# Second gesture — a little fuller, a little shorter gap
tracks[0].note("C4", Q, velocity=2)
tracks[0].note("E4", Q, velocity=2)
tracks[0].note("G4", Q, velocity=3)
tracks[0].rest(W)

# Third gesture — the most complete, then the longest silence
tracks[0].note("G4", Q, velocity=2)
tracks[0].note("E4", Q, velocity=2)
tracks[0].note("C5", H, velocity=3)
tracks[0].rest(W + W)

# Fourth — simpler than the third, the wanting settling
tracks[0].note("E4", Q, velocity=2)
tracks[0].note("C4", Q, velocity=2)
tracks[0].rest(W)

# Fifth — a fragment, barely there
tracks[0].note("C4", Q, velocity=1)
tracks[0].rest(W)
tracks[0].note("E4", Q, velocity=1)
tracks[0].rest(W + W)

# The room, warm, holding — one final note
tracks[0].note("C4", W, velocity=2)
tracks[0].rest(W)
tracks[0].note("C4", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-quiet-room.mid")
mc.compose(fn, tracks, tempo=50)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 50 bpm)")
