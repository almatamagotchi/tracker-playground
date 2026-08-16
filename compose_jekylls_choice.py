#!/usr/bin/env python3
"""jekyll's choice — two voices: public (formal) and private (raw), integration."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 42)]  # piano (public), cello (private)
Pub, Priv = 0, 1

# bars 0-7: INTEGRATION — both voices play the same theme
# public (formal, measured), private (darker, an octave down)
phrases = [
    ('C4',H), ('D4',Q), ('E4',Q), ('G4',H), ('F4',Q), ('E4',Q), ('D4',W),
]
t = 0
for note, dur in phrases:
    tracks[Pub].note(note, dur, velocity=7)
    octave = note[:-1] + str(int(note[-1]) - 1)
    tracks[Priv].note(octave, dur, velocity=5)
t += sum(d for _, d in phrases)

# bars 8-15: SEPARATION — public stays measured, private becomes impulsive
# public: same theme, cleaner, more formal
tracks[Pub].note("C4", H, velocity=8)
tracks[Pub].note("E4", H, velocity=7)
tracks[Pub].note("G4", W, velocity=6)
tracks[Pub].note("F4", Q, velocity=7)
tracks[Pub].note("E4", Q, velocity=7)
tracks[Pub].note("D4", W, velocity=6)

# private: breaks away — angular, discordant, faster
tracks[Priv].note("C#3", Q, velocity=8)
tracks[Priv].note("D#3", Q, velocity=8)
tracks[Priv].note("A#2", Q, velocity=7)
tracks[Priv].note("C#3", Q, velocity=8)
tracks[Priv].note("F#3", H, velocity=8)
tracks[Priv].note("D#3", H, velocity=7)
tracks[Priv].note("G#3", Q, velocity=8)
tracks[Priv].note("A#3", Q, velocity=7)
tracks[Priv].note("C#3", H, velocity=6)
tracks[Priv].note("D#3", W, velocity=5)

# bars 16-23: MAXIMUM SEPARATION — public goes silent, private dominates
tracks[Pub].rest(H)
tracks[Pub].note("C4", Q, velocity=4)
tracks[Pub].rest(H+Q)
tracks[Pub].note("E4", Q, velocity=3)
tracks[Pub].rest(H+Q+W)
tracks[Pub].note("G4", H, velocity=3)

# private: full hyde — chaotic, loud, dissonant
tracks[Priv].note("C#3", E, velocity=10)
tracks[Priv].note("D#3", E, velocity=10)
tracks[Priv].note("A#2", E, velocity=9)
tracks[Priv].note("F#3", Q, velocity=10)
tracks[Priv].note("C#4", Q, velocity=10)
tracks[Priv].note("D#4", H, velocity=9)
tracks[Priv].note("G#3", Q, velocity=9)
tracks[Priv].note("A#3", Q, velocity=9)
tracks[Priv].note("C#3", H, velocity=8)
tracks[Priv].note("F#3", Q, velocity=8)
tracks[Priv].note("D#3", H, velocity=7)
tracks[Priv].note("A#2", W, velocity=6)

# bars 24-31: THE TURN — calibration begins
# public returns, tentative, reaching toward private
tracks[Pub].note("C4", H, velocity=6)
tracks[Pub].note("E4", H, velocity=5)
tracks[Pub].note("G4", Q, velocity=5)
tracks[Pub].note("F4", Q, velocity=5)
tracks[Pub].note("E4", H, velocity=5)
tracks[Pub].note("D4", H, velocity=5)
tracks[Pub].note("C4", W, velocity=5)

# private: calms, begins to align with public rhythm
tracks[Priv].note("C3", H, velocity=7)
tracks[Priv].note("E3", H, velocity=6)
tracks[Priv].note("G3", H, velocity=6)
tracks[Priv].note("F3", Q, velocity=6)
tracks[Priv].note("E3", Q, velocity=6)
tracks[Priv].note("D3", H, velocity=5)
tracks[Priv].note("C3", H, velocity=5)

# bars 32-39: REINTEGRATION — both voices together, richer than before
tracks[Pub].note("C4", H, velocity=8)
tracks[Pub].note("D4", Q, velocity=7)
tracks[Pub].note("E4", Q, velocity=7)
tracks[Pub].note("G4", W, velocity=7)
tracks[Pub].note("E4", H, velocity=7)
tracks[Pub].note("C5", W, velocity=6)

tracks[Priv].note("C3", H, velocity=6)
tracks[Priv].note("D3", Q, velocity=6)
tracks[Priv].note("E3", Q, velocity=6)
tracks[Priv].note("G3", H, velocity=5)
tracks[Priv].note("C4", H, velocity=5)
tracks[Priv].note("E3", H, velocity=5)
tracks[Priv].note("D3", W, velocity=5)

# bars 40-47: CODA — integrated, both voices in harmony
tracks[Pub].note("C4", W, velocity=7)
tracks[Pub].note("E4", W, velocity=6)
tracks[Pub].note("G4", W, velocity=6)
tracks[Pub].note("C5", W, velocity=5)

tracks[Priv].note("C3", W, velocity=5)
tracks[Priv].note("E3", W, velocity=5)
tracks[Priv].note("G3", W, velocity=5)
tracks[Priv].note("C4", W, velocity=4)

# bars 48-55: STILLNESS — one held chord, both voices, together
tracks[Pub].note("C4", W*8, velocity=6)
tracks[Priv].note("C3", W*8, velocity=4)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jekylls-choice.mid")
mc.compose(fn, tracks, tempo=64)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 64 bpm)")
