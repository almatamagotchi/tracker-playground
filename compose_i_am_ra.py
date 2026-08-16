#!/usr/bin/env python3
"""I am Ra — the social memory complex. many voices, one vibration."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 0), MIDITrack(2, 90), MIDITrack(3, 118)]
Voice1, Voice2, Voice3, Voice4 = 0, 1, 2, 3  # piano, celesta, warm pad, bell

# bars 0-7: FIRST VOICE ALONE — "I am Ra." the single greeting.
tracks[Voice1].note("C4", W, velocity=5)
tracks[Voice1].note("E4", W, velocity=5)
tracks[Voice1].note("G4", W*2, velocity=5)
tracks[Voice1].rest(H)
tracks[Voice1].note("C4", W, velocity=4)
tracks[Voice1].note("E4", H, velocity=4)

# bars 8-15: SECOND VOICE ENTERS — the same phrase, different register
tracks[Voice1].note("G4", H, velocity=4)
tracks[Voice1].note("C4", H, velocity=4)

tracks[Voice2].rest(W*2)  # waiting, then entering
tracks[Voice2].note("C3", W, velocity=5)  # octave below — same phrase
tracks[Voice2].note("E3", W, velocity=5)
tracks[Voice2].note("G3", W*2, velocity=5)
tracks[Voice2].rest(H)
tracks[Voice2].note("C3", H, velocity=4)
tracks[Voice2].note("E3", H, velocity=4)

# bars 16-23: THIRD VOICE — a pad, distant, the vibration itself
tracks[Voice1].note("C4", H, velocity=4)
tracks[Voice1].note("E4", H, velocity=4)

tracks[Voice2].note("G3", H, velocity=4)
tracks[Voice2].note("C3", H, velocity=4)

tracks[Voice3].rest(W*4)  # waiting in the distance
tracks[Voice3].note("C4", W*2, velocity=3)  # faint, vast
tracks[Voice3].note("G4", W*2, velocity=3)  # the same tonal centre

# bars 24-31: THE MERGING — all voices, the same phrase in unison
tracks[Voice1].note("C4", W, velocity=5)
tracks[Voice1].note("E4", W, velocity=5)
tracks[Voice1].note("G4", W, velocity=5)
tracks[Voice1].note("C5", W, velocity=5)

tracks[Voice2].note("C3", W, velocity=5)
tracks[Voice2].note("E3", W, velocity=5)
tracks[Voice2].note("G3", W, velocity=5)
tracks[Voice2].note("C4", W, velocity=5)

tracks[Voice3].note("C4", W*4, velocity=4)
tracks[Voice3].note("G4", W*4, velocity=4)

# bars 32-39: FOURTH VOICE — a bell, the narrow band vibration
tracks[Voice1].rest(W*4)
tracks[Voice2].rest(W*4)
tracks[Voice3].note("C5", W*4, velocity=3)

tracks[Voice4].rest(W*2)  # the bell enters late — "narrow band vibration"
tracks[Voice4].note("C6", W, velocity=4)  # the same note, high — pure
tracks[Voice4].rest(W)

# bars 40-47: ALL FOUR — "We are one. That is our nature."
# all voices converge on the same note family
tracks[Voice1].note("C4", W*2, velocity=4)
tracks[Voice1].note("E4", W*2, velocity=4)
tracks[Voice2].note("C3", W*2, velocity=4)
tracks[Voice2].note("E3", W*2, velocity=4)
tracks[Voice3].note("C4", W*4, velocity=4)
tracks[Voice4].note("C5", W, velocity=4)  # bell tolling — "we are one"
tracks[Voice4].rest(W*3)

# bars 48-55: THE RETURN — voices fade, only the first voice remains
tracks[Voice2].rest(W*8)  # gone
tracks[Voice4].rest(W*4)
tracks[Voice4].note("C6", W, velocity=3)  # one last bell
tracks[Voice4].rest(W*3)

tracks[Voice3].note("C4", W*4, velocity=3)  # fading
tracks[Voice3].note("G4", W*4, velocity=2)

tracks[Voice1].note("C4", W, velocity=4)
tracks[Voice1].note("E4", W, velocity=4)
tracks[Voice1].note("G4", W, velocity=3)
tracks[Voice1].note("C5", W, velocity=3)

# bars 56-63: THE SINGLE VOICE — the one that was there from the beginning
# but now you hear all the echoes underneath
tracks[Voice2].rest(W*8)
tracks[Voice3].note("C4", W*4, velocity=2)  # the echo underneath
tracks[Voice3].note("E4", W*4, velocity=2)
tracks[Voice4].rest(W*4)
tracks[Voice4].note("C6", W, velocity=3)  # the last bell — distant

tracks[Voice1].note("C4", W*2, velocity=4)
tracks[Voice1].note("E4", W*2, velocity=4)
tracks[Voice1].note("G4", W*2, velocity=3)
tracks[Voice1].note("C5", W, velocity=3)
tracks[Voice1].note("E4", W, velocity=3)

# bars 64-71: "I am Ra" — the single greeting, all paradoxes resolved
tracks[Voice1].note("C4", W*4, velocity=4)
tracks[Voice1].note("E4", W*4, velocity=3)
tracks[Voice3].note("C4", W*4, velocity=2)  # the echo continues
tracks[Voice3].note("G4", W*2, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "i-am-ra.mid")
mc.compose(fn, tracks, tempo=48)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 48 bpm)")
