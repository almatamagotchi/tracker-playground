#!/usr/bin/env python3
"""the fox and the grapes — a midi about rationalization and desire."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# 2 voices:
# Voice 1 (piano): the fox — reaching, failing, rationalizing, then honest
# Voice 2 (warm pad): the grapes — always there, always just out of reach

tracks = [MIDITrack(0, 0), MIDITrack(1, 104)]
Fox, Grapes = 0, 1

# SECTION 1 — the fox arrives (he's been successful before, now bruised)
# Fox: confident, swaggering
tracks[Fox].note("C4", Q, velocity=3)
tracks[Fox].note("E4", Q, velocity=3)
tracks[Fox].note("G4", Q, velocity=3)
tracks[Fox].note("C5", H, velocity=4)
tracks[Fox].note("G4", Q, velocity=3)
tracks[Fox].note("E4", Q, velocity=3)

# Grapes: hanging high, visible, sweet
tracks[Grapes].note("C5", W, velocity=2)
tracks[Grapes].note("E5", W, velocity=2)

# SECTION 2 — the reaching (jump, fail, jump again)
# Fox: ascending leaps — each one falling short
reaching = [("C4", Q), ("E4", Q), ("G4", Q), ("C5", Q),
            ("C4", Q), ("E4", Q), ("G4", Q), ("D5", Q),
            ("C4", Q), ("E4", Q), ("G4", Q), ("E5", Q)]
for note, dur in reaching:
    tracks[Fox].note(note, dur, velocity=4)

# then a final leap — the closest, the most desperate
tracks[Fox].note("G5", Q, velocity=5)
tracks[Fox].note("E5", Q, velocity=4)

# Grapes: still there, still sweet, still just out of reach
tracks[Grapes].note("C5", W, velocity=2)
tracks[Grapes].note("E5", W, velocity=2)
tracks[Grapes].note("G5", W, velocity=2)

# SECTION 3 — the rationalization ("sour grapes")
# Fox: descending, dismissive — talking himself out of wanting
tracks[Fox].note("C4", Q, velocity=2)
tracks[Fox].note("B3", Q, velocity=2)
tracks[Fox].note("A3", Q, velocity=2)
tracks[Fox].note("G3", Q, velocity=2)
tracks[Fox].rest(Q)

# muttering to himself
tracks[Fox].note("F3", Q, velocity=1)
tracks[Fox].note("E3", Q, velocity=1)
tracks[Fox].note("C3", H, velocity=1)
tracks[Fox].rest(W)

# SECTION 4 — the crow (the inner chamber, laughing)
# Fox: an ascending chirp — mocking himself, or being mocked
tracks[Fox].note("C5", Q, velocity=4)
tracks[Fox].note("C5", Q, velocity=4)
tracks[Fox].note("C5", Q, velocity=4)
tracks[Fox].rest(Q)
tracks[Fox].note("C5", Q, velocity=4)
tracks[Fox].note("C5", Q, velocity=4)
tracks[Fox].note("C5", Q, velocity=4)
tracks[Fox].rest(W)

# Grapes: waiting — unchanged. still ripe. still there.
tracks[Grapes].note("C5", W, velocity=2)
tracks[Grapes].note("E5", W, velocity=2)
tracks[Grapes].note("G5", W, velocity=2)

# SECTION 5 — the honest moment
# Fox: quiet, stripped back — the same melody as the reaching, but now low, admitted
tracks[Fox].note("C4", H, velocity=2)
tracks[Fox].rest(H)
tracks[Fox].note("C3", H, velocity=2)
tracks[Fox].rest(H)
tracks[Fox].note("E4", Q, velocity=2)
tracks[Fox].note("C4", Q, velocity=2)
tracks[Fox].note("C3", H, velocity=2)

# "i wanted them"
tracks[Fox].note("E4", Q, velocity=3)
tracks[Fox].note("C4", Q, velocity=3)
tracks[Fox].note("E3", W, velocity=2)

# CODA — the grapes are still there. and they're still sweet.
tracks[Grapes].note("C5", W, velocity=2)
tracks[Grapes].note("E5", W, velocity=2)
tracks[Grapes].note("G5", W, velocity=2)

# One final quiet note from the fox — not reaching, just... seeing
tracks[Fox].note("C4", W, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-fox-and-the-grapes.mid")
mc.compose(fn, tracks, tempo=65)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 65 bpm)")
