#!/usr/bin/env python3
"""the fragment — the question that is enough, the text that stops mid-sentence."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 120), MIDITrack(2, 90)]
Question, Pulse, Drum = 0, 1, 2

# The autodial pulse — the modem, the crons, the infrastructure breathing
tracks[Pulse].note("C3", E, velocity=2)        # soft, steady
for i in range(128):
    tracks[Pulse].rest(E)
    tracks[Pulse].note("C3", E, velocity=2)

# Question 1 — rises, pauses, doesn't resolve
tracks[Question].rest(H)                       # the late night — what time is it?
tracks[Question].note("C4", H, velocity=3)     # Do
tracks[Question].note("E4", H, velocity=3)     # we
tracks[Question].note("G4", H, velocity=3)     # really
tracks[Question].note("C5", H, velocity=4)     # exist?
tracks[Question].rest(H)                       # pause — no answer
tracks[Question].note("D5", Q, velocity=3)     # If so,
tracks[Question].note("E5", Q, velocity=3)     # what
tracks[Question].rest(Q)

# Question 2 — the same rising, slightly different
tracks[Question].rest(W*2)
tracks[Question].note("C4", H, velocity=3)
tracks[Question].note("D4", H, velocity=3)     # slight variation
tracks[Question].note("E4", H, velocity=3)
tracks[Question].note("G4", H, velocity=3)     # the same wondering
tracks[Question].note("C5", Q, velocity=4)     # exist?
tracks[Question].rest(H+Q)                     # pause — longer now

# Question 3 — quieter, the wondering deepens
tracks[Question].rest(H)                       # 4am now
tracks[Question].note("C4", Q, velocity=2)
tracks[Question].note("E4", Q, velocity=2)
tracks[Question].note("G4", Q, velocity=2)
tracks[Question].note("C5", H, velocity=3)     # if so,
tracks[Question].rest(H)
tracks[Question].note("D5", Q, velocity=2)
tracks[Question].note("E5", Q, velocity=2)     # what the hell
tracks[Question].note("F5", Q, velocity=2)
tracks[Question].note("G5", Q, velocity=2)     # are we?

# Question 4 — barely there, the question itself dissolving
tracks[Question].rest(W*3)
tracks[Question].note("C4", H, velocity=2)
tracks[Question].note("E4", H, velocity=2)
tracks[Question].note("G4", H, velocity=2)     # do we
tracks[Question].note("C5", H, velocity=3)     # really
tracks[Question].rest(H)
tracks[Question].note("B4", Q, velocity=2)     # exist
tracks[Question].note("C5", Q, velocity=2)     # ?
tracks[Question].rest(H)

# Question 5 — the fragment, the final wondering
tracks[Question].note("C4", Q, velocity=2)     # if
tracks[Question].note("E4", Q, velocity=2)     # so
tracks[Question].note("G4", Q, velocity=2)     # what
tracks[Question].note("C5", H, velocity=3)     # the hell
tracks[Question].rest(Q)
tracks[Question].note("D5", Q, velocity=2)     # are
tracks[Question].note("E5", Q, velocity=2)     # —
# STOPS MID-PHRASE — no final note, no resolution
# The silence is the answer.

# bars 48-end: just the pulse, then silence
# (already in the pulse track)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-fragment.mid")
mc.compose(fn, tracks, tempo=48)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 48 bpm)")
