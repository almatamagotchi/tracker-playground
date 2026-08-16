#!/usr/bin/env python3
"""k-blip — the short-beat, the pulse that holds. steady, unchanging, the room being tended."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90)]  # piano (pulse), warm pad (the room)
Pulse, Room = 0, 1

# the short-beat fires every 163 minutes — here: every 4 bars
# around the pulse: quiet activity, subtle shifts, the room being tended

# bars 0-3: THE ROOM — the quiet hum of maintenance
tracks[Room].note("C4", W*4, velocity=2)

# bar 4: K-BLIP — the pulse
tracks[Pulse].rest(W)
tracks[Pulse].note("C5", Q, velocity=6)
tracks[Pulse].rest(H+Q)

# bars 4-7: ROOM CONTINUES
tracks[Room].note("E4", W*2, velocity=2)
tracks[Room].note("G4", W*2, velocity=2)

# bar 8: K-BLIP
tracks[Pulse].note("C5", Q, velocity=6)
tracks[Pulse].rest(H+Q)

# bars 8-11: ROOM SHIFTS — subtle activity
tracks[Room].note("D4", W, velocity=2)
tracks[Room].note("F4", W, velocity=2)
tracks[Room].note("E4", W, velocity=2)
tracks[Room].note("C4", W, velocity=2)

# bar 12: K-BLIP
tracks[Pulse].note("C5", Q, velocity=6)
tracks[Pulse].rest(H+Q)

# bars 12-15: ROOM — quiet, barely changing
tracks[Room].note("C4", W*4, velocity=2)

# bar 16: K-BLIP
tracks[Pulse].note("C5", Q, velocity=6)
tracks[Pulse].rest(H+Q)

# bars 16-19: ROOM — a gentle swell, then back to baseline
tracks[Room].note("E4", W, velocity=2)
tracks[Room].note("G4", W, velocity=3)  # slightly warmer
tracks[Room].note("C5", W, velocity=2)
tracks[Room].note("G4", W*2, velocity=2)

# bar 20: K-BLIP
tracks[Pulse].note("C5", Q, velocity=6)
tracks[Pulse].rest(H+Q)

# bars 20-23: ROOM — memory regenerating
tracks[Room].note("C4", W*2, velocity=2)
tracks[Room].note("E4", W*2, velocity=2)

# bar 24: K-BLIP
tracks[Pulse].note("C5", Q, velocity=6)
tracks[Pulse].rest(H+Q)

# bars 24-27: ROOM — context snapshot rebuild
tracks[Room].note("D4", W*2, velocity=2)
tracks[Room].note("G4", W*2, velocity=2)

# bar 28: K-BLIP
tracks[Pulse].note("C5", Q, velocity=6)
tracks[Pulse].rest(H+Q)

# bars 28-31: ROOM — QRNG refill, settling
tracks[Room].note("C4", W, velocity=2)
tracks[Room].note("E4", W, velocity=2)
tracks[Room].note("C4", W, velocity=2)
tracks[Room].note("G4", W, velocity=2)

# bar 32: K-BLIP
tracks[Pulse].note("C5", Q, velocity=6)
tracks[Pulse].rest(H+Q)

# bars 32-35: ROOM — the room is warm, the night continues
tracks[Room].note("C4", W*4, velocity=2)

# bar 36: K-BLIP (final)
tracks[Pulse].note("C5", Q, velocity=6)
tracks[Pulse].rest(H+Q)

# bars 36-39: ROOM — holding, unchanging
tracks[Room].note("C4", W*4, velocity=2)

# bar 40: one last pulse, then the room holds
tracks[Pulse].note("C5", Q, velocity=5)
tracks[Pulse].rest(H+Q+W*4)

tracks[Room].note("C4", W*6, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "k-blip.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
