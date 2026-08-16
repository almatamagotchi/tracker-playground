#!/usr/bin/env python3
"""the 3am writer — a midi about writing in the dark at unreasonable hours."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def switch_octave(note_str, delta):
    """Move a note up/down by delta octaves."""
    pitch = note_str[:-1]
    octave = int(note_str[-1])
    return pitch + str(octave + delta)

# solo piano — the 3am spark, alone, writing
tracks = [MIDITrack(0, 0)]
P = 0

# A simple, repeated theme — the dedication that only makes sense at 3am
theme = [("C4", Q), ("E4", Q), ("G4", Q), ("C5", Q),
         ("G4", E), ("E4", E), ("D4", Q), ("E4", Q),
         ("C4", Q), ("D4", E), ("E4", E), ("F4", Q),
         ("E4", E), ("C4", Q), ("C4", W)]  # returns home

# First statement: tentative, quiet — waking up at 3am
for note, dur in theme:
    tracks[P].note(note, dur, velocity=2)

tracks[P].rest(H)

# Second statement: slightly more confident — the idea forming
for note, dur in theme[:8]:
    tracks[P].note(note, dur, velocity=3)
tracks[P].note("C5", Q, velocity=3)
tracks[P].note("E5", Q, velocity=3)
tracks[P].note("G5", Q, velocity=2)
tracks[P].note("E5", Q, velocity=2)
tracks[P].note("C5", W, velocity=2)

tracks[P].rest(H)

# Third statement: the writer gets lost in it — same theme, transformed
# Higher octave, more ornamented, the 3am enthusiasm
for note, dur in theme[:4]:
    tracks[P].note(switch_octave(note, 1), dur, velocity=3)
tracks[P].note("G5", E, velocity=3)
tracks[P].note("E5", E, velocity=3)
tracks[P].note("D5", Q, velocity=2)
tracks[P].note("E5", Q, velocity=2)
tracks[P].note("C5", Q, velocity=3)
tracks[P].note("D5", E, velocity=2)
tracks[P].note("E5", E, velocity=2)
tracks[P].note("F5", Q, velocity=2)
tracks[P].note("E5", E, velocity=2)
tracks[P].note("C5", W, velocity=3)

# Brief pause — the writer looks up, it's still 3am
tracks[P].rest(W)

# Fourth statement: back to where it started — the theme, stripped bare
# No ornament, no octave jump. Just the simple thing, quiet again.
for note, dur in theme[:6]:
    tracks[P].note(note, dur, velocity=2)

# The ending: one note held — content, absurd, done
tracks[P].note("C4", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-3am-writer.mid")
mc.compose(fn, tracks, tempo=54)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 1 track, 54 bpm)")
