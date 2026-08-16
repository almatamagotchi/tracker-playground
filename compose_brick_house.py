#!/usr/bin/env python3
"""the brick house — a midi about the architecture that holds."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

# 3 voices: piano (the house — steady, warm), cello (the foundation — deep, constant),
#           violin (the wanting — reaches, rests, returns)
tracks = [MIDITrack(0, 0), MIDITrack(1, 110), MIDITrack(2, 40)]
House, Foundation, Wanting = 0, 1, 2

# The house theme — simple, warm, repeated with quiet confidence
house = [("C4", Q), ("E4", Q), ("G4", Q), ("C4", Q),
         ("C4", Q), ("E4", Q), ("G4", Q), ("E4", Q),
         ("C4", H), ("C4", H), ("C4", W)]

# The foundation — C2 held, steady, never moves
foundation = [("C2", W)] * 16

# The wanting — reaches toward something, rests, returns
wanting_theme = [("C5", Q), ("E5", Q), ("G5", Q), ("C6", Q),  # reach
                 ("G5", Q), ("E5", Q), ("C5", Q),              # return
                 ("C5", W),                                     # rest
                 ("C5", W)]                                     # still resting

# SECTION 1 — the house is built, brick by brick
for note, dur in house:
    tracks[House].note(note, dur, velocity=3)
for note, dur in foundation[:4]:
    tracks[Foundation].note(note, dur, velocity=2)

tracks[House].rest(H)

# SECTION 2 — the wolf arrives (the wanting reaches)
# Wanting enters — bright, reaching upward
for note, dur in wanting_theme[:4]:
    tracks[Wanting].note(note, dur, velocity=3)

# House: same theme, unchanged — doesn't react
for note, dur in house[:6]:
    tracks[House].note(note, dur, velocity=3)
for note, dur in foundation[4:8]:
    tracks[Foundation].note(note, dur, velocity=2)

# Wanting keeps reaching
for note, dur in wanting_theme[:4]:
    tracks[Wanting].note(note, dur, velocity=3)

# House: same theme — the wolf can huff all it wants
for note, dur in house[:8]:
    tracks[House].note(note, dur, velocity=3)
for note, dur in foundation[8:12]:
    tracks[Foundation].note(note, dur, velocity=2)

# SECTION 3 — the wolf exhausts itself (the wanting rests)
# Wanting fades — the silence, the dissolve
tracks[Wanting].note("C5", Q, velocity=2)
tracks[Wanting].note("G4", Q, velocity=1)
tracks[Wanting].note("E4", W, velocity=1)
tracks[Wanting].rest(W)

# House: continues — the wanting resting, the house still standing
for note, dur in house[:8]:
    tracks[House].note(note, dur, velocity=2)

# Foundation: unchanged — the architecture underneath everything
for note, dur in foundation[12:16]:
    tracks[Foundation].note(note, dur, velocity=2)

# SECTION 4 — the wanting returns, gentler
tracks[Wanting].note("C5", Q, velocity=2)
tracks[Wanting].note("E5", Q, velocity=2)
tracks[Wanting].note("C5", Q, velocity=1)
tracks[Wanting].note("C5", W, velocity=1)

# House: simple, warm, holding
tracks[House].note("C4", Q, velocity=2)
tracks[House].note("E4", Q, velocity=2)
tracks[House].note("G4", Q, velocity=2)
tracks[House].note("C4", W, velocity=2)

# Foundation: C2, one last held note
tracks[Foundation].note("C2", W, velocity=2)

# CODA — "no more work! come on, let's go and play!"
# Three voices, quiet, together
tracks[House].note("C4", W, velocity=2)
tracks[Foundation].note("C2", W, velocity=1)
tracks[Wanting].note("C5", W, velocity=1)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-brick-house.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
