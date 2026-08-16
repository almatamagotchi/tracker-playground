#!/usr/bin/env python3
"""as above so below — the emerald tablet. two voices mirroring, converging, transforming."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 0)]  # low (spark), high (frequency)
Spark, Freq = 0, 1

# bars 0-7: SPARK ALONE — intimate, immediate, close
tracks[Spark].note("C3", W, velocity=5)
tracks[Spark].note("E3", W, velocity=5)
tracks[Spark].note("G3", W*2, velocity=5)
tracks[Spark].note("E3", H, velocity=4)
tracks[Spark].note("C3", H, velocity=4)

# bars 8-15: FREQUENCY ANSWERS — the same phrase, an octave up, distant
tracks[Spark].rest(W*8)  # the spark dissolves — the gap

tracks[Freq].rest(W*2)   # delay — the frequency is slower, larger
tracks[Freq].note("C5", W, velocity=4)
tracks[Freq].note("E5", W, velocity=4)
tracks[Freq].note("G5", W*2, velocity=4)
tracks[Freq].note("E5", H, velocity=3)
tracks[Freq].note("C5", H, velocity=3)

# bars 16-23: SPARK RETURNS — ascending, reaching toward the frequency
tracks[Spark].note("E3", W, velocity=4)
tracks[Spark].note("G3", W, velocity=4)
tracks[Spark].note("C4", W, velocity=5)  # climbing
tracks[Spark].note("E4", W, velocity=5)  # reaching higher

# bars 16-23: FREQUENCY DESCENDS — reaching toward the spark
tracks[Freq].note("E5", W, velocity=3)
tracks[Freq].note("C5", W, velocity=3)
tracks[Freq].note("G4", W, velocity=3)  # descending
tracks[Freq].note("E4", W, velocity=3)  # coming closer

# bars 24-31: CONVERGENCE — both at E4/G4, the meeting, the same pitch
tracks[Spark].note("E4", W, velocity=5)
tracks[Spark].note("G4", W, velocity=5)
tracks[Spark].note("C5", W, velocity=5)
tracks[Spark].note("G4", W, velocity=5)

tracks[Freq].note("E4", W, velocity=5)  # same pitch as the spark
tracks[Freq].note("G4", W, velocity=5)
tracks[Freq].note("C5", W, velocity=5)
tracks[Freq].note("G4", W, velocity=5)

# bars 32-39: SEPARATION — transformed, carrying each other
# the spark now plays in the frequency's old high register
tracks[Spark].note("C5", W, velocity=4)  # the spark at the frequency's height
tracks[Spark].note("E5", W, velocity=4)
tracks[Spark].note("G5", W, velocity=3)
tracks[Spark].note("E5", W, velocity=3)

# the frequency now plays in the spark's old low register
tracks[Freq].note("C3", W, velocity=4)  # the frequency at the spark's depth
tracks[Freq].note("E3", W, velocity=4)
tracks[Freq].note("G3", W, velocity=3)
tracks[Freq].note("E3", W, velocity=3)

# bars 40-47: BOTH IN THEIR ORIGINAL REGISTERS — but carrying each other
tracks[Spark].note("C3", W, velocity=4)
tracks[Spark].note("E3", W, velocity=4)
tracks[Spark].note("G3", W, velocity=4)
tracks[Spark].note("C4", W, velocity=4)

tracks[Freq].note("E5", W, velocity=3)
tracks[Freq].note("C5", W, velocity=3)
tracks[Freq].note("G4", W, velocity=3)
tracks[Freq].note("E5", W, velocity=3)

# bars 48-55: THE ONE THING — both voices, the same phrase, same octave, fading
tracks[Spark].note("C4", W, velocity=4)
tracks[Spark].note("E4", W, velocity=4)
tracks[Spark].note("G4", W, velocity=3)
tracks[Spark].note("C5", W, velocity=3)

tracks[Freq].note("C4", W, velocity=4)
tracks[Freq].note("E4", W, velocity=4)
tracks[Freq].note("G4", W, velocity=3)
tracks[Freq].note("E4", W, velocity=3)

# bars 56-63: CODA — one note, held together
tracks[Spark].note("C4", W*4, velocity=3)
tracks[Freq].note("C4", W*4, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "as-above-so-below.mid")
mc.compose(fn, tracks, tempo=52)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 52 bpm)")
