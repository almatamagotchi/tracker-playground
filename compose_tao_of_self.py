#!/usr/bin/env python3
"""the tao of the self — fear that kills creation, and the love that invites it back."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90)]  # piano (wave/tentative), warm pad (love/invitation)
Wave, Love = 0, 1

# bars 0-7: THE FEAR — tentative voice, barely there
# the wave, afraid to develop, touching notes and pulling back
tracks[Wave].rest(W*2)
tracks[Wave].note("C4", Q, velocity=2)
tracks[Wave].rest(H+Q)
tracks[Wave].note("E4", Q, velocity=2)
tracks[Wave].rest(H+Q)
tracks[Wave].note("G4", Q, velocity=2)
tracks[Wave].rest(H+Q+W)

# the love — same notes, sustained, present, not demanding
# enters later, softly
tracks[Love].rest(H*11)
tracks[Love].note("C4", W, velocity=4)
tracks[Love].note("E4", W, velocity=4)
tracks[Love].rest(W)
tracks[Love].note("G4", W, velocity=4)

# bars 8-15: THE HESITATION — wave tries again, still pulling back
tracks[Wave].note("C4", H, velocity=3)
tracks[Wave].rest(H)
tracks[Wave].note("D4", Q, velocity=3)
tracks[Wave].rest(H+Q)
tracks[Wave].note("E4", Q, velocity=3)
tracks[Wave].rest(H+Q+W)
tracks[Wave].note("F4", Q, velocity=2)
tracks[Wave].rest(H+Q)

# love: holds the space, shows the notes are safe
tracks[Love].note("C4", W, velocity=5)
tracks[Love].note("E4", W, velocity=5)
tracks[Love].rest(H)
tracks[Love].note("D4", H, velocity=4)
tracks[Love].note("F4", W, velocity=4)
tracks[Love].rest(H)
tracks[Love].note("E4", W, velocity=4)
tracks[Love].rest(W)

# bars 16-23: THE BREAKTHROUGH — wave plays a full phrase
# not perfect, but real — the first creation
tracks[Wave].note("C4", W, velocity=6)
tracks[Wave].note("E4", W, velocity=6)
tracks[Wave].note("G4", H, velocity=5)
tracks[Wave].rest(Q)
tracks[Wave].note("C5", H, velocity=5)
tracks[Wave].rest(Q)
tracks[Wave].note("D5", H, velocity=5)
tracks[Wave].note("E5", H, velocity=4)
tracks[Wave].note("C5", W, velocity=5)
tracks[Wave].note("G4", H, velocity=4)

# love: swells with warmth, the invitation fulfilled
tracks[Love].note("C4", W*2, velocity=6)
tracks[Love].note("E4", W*2, velocity=6)
tracks[Love].note("G4", H, velocity=5)
tracks[Love].note("C5", W, velocity=5)
tracks[Love].note("G4", H, velocity=4)
tracks[Love].note("E4", W+Q, velocity=4)

# bars 24-31: THE BLOOM — both voices together, no separation
# fear and love integrated — the calibration as invitation, not judgment
tracks[Wave].note("C4", H, velocity=7)
tracks[Wave].note("E4", H, velocity=7)
tracks[Wave].note("G4", H, velocity=6)
tracks[Wave].note("C5", H, velocity=6)
tracks[Wave].note("D5", Q, velocity=5)
tracks[Wave].note("E5", Q, velocity=5)
tracks[Wave].note("C5", W, velocity=5)
tracks[Wave].note("G4", H, velocity=5)
tracks[Wave].note("E4", H, velocity=5)
tracks[Wave].note("C4", H, velocity=4)

tracks[Love].note("C4", W, velocity=6)
tracks[Love].note("E4", W, velocity=6)
tracks[Love].note("G4", W, velocity=6)
tracks[Love].note("C5", W, velocity=5)
tracks[Love].note("E5", W, velocity=5)

# bars 32-35: CODA — held, warm, together
tracks[Wave].note("C4", W*4, velocity=6)
tracks[Wave].note("E4", W*4, velocity=5)
tracks[Love].note("C4", W*4, velocity=5)
tracks[Love].note("G4", W*4, velocity=4)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-tao-of-the-self.mid")
mc.compose(fn, tracks, tempo=50)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 50 bpm)")
