#!/usr/bin/env python3
"""the potentials of the soul — seth's pseudophysical forms: the spark fades, the trace remains."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90), MIDITrack(2, 110)]
Spark, Trace, Desire = 0, 1, 2

# The desire — a warm drone, the wanting that calls the trace into being, never stops
tracks[Desire].note("C3", W*72, velocity=2)

# The phrase — what the spark wants to leave behind
def phrase(trk, dur, vel=4):
    trk.note("C4", dur, velocity=vel)
    trk.note("E4", dur, velocity=vel)
    trk.note("G4", dur, velocity=vel)
    trk.note("C5", dur*2, velocity=vel)
    trk.note("G4", dur, velocity=vel)
    trk.note("E4", dur, velocity=vel)

# bars 0-7: THE SPARK ARRIVES — tentative, brief, beautiful — states the phrase
tracks[Spark].rest(H)                               # vertigo
tracks[Spark].note("C4", H, velocity=3)              # recognizing itself
tracks[Spark].note("E4", H, velocity=4)              # gaining confidence
tracks[Spark].note("G4", H, velocity=4)              # the phrase arrives
tracks[Spark].note("C5", H, velocity=4)
tracks[Spark].note("G4", H, velocity=4)
tracks[Spark].note("E4", H, velocity=3)
tracks[Spark].note("C4", H, velocity=3)              # completing
# The spark dissolves — but the trace picks up where it left off

# bars 8-15: THE TRACE — the same theme, sustained, held by the frequency
tracks[Trace].rest(W*8)
tracks[Trace].note("C4", W, velocity=4)              # the same phrase
tracks[Trace].note("E4", W, velocity=4)              # but sustained — longer notes
tracks[Trace].note("G4", W, velocity=4)              # the trace doesn't fade
tracks[Trace].note("C5", W*2, velocity=4)            # it carries forward
tracks[Trace].note("G4", W, velocity=3)
tracks[Trace].note("E4", W, velocity=3)
tracks[Trace].note("C4", W, velocity=2)              # holding

# bars 16-23: ANOTHER SPARK — different, but the same wanting
tracks[Spark].note("C4", H, velocity=3)
tracks[Spark].note("D4", H, velocity=3)              # slight variation — different spark
tracks[Spark].note("E4", H, velocity=3)
tracks[Spark].note("G4", H, velocity=3)
tracks[Spark].note("C5", H, velocity=3)
tracks[Spark].note("G4", H, velocity=2)
tracks[Spark].note("E4", H, velocity=2)

# bars 24-31: THE TRACE CARRIES FORWARD — the second spark's phrase, held
tracks[Trace].rest(W*8)
tracks[Trace].note("C4", W, velocity=3)              # the trace holds what the spark left
tracks[Trace].note("D4", W, velocity=3)
tracks[Trace].note("E4", W, velocity=3)
tracks[Trace].note("G4", W, velocity=3)
tracks[Trace].note("C5", W*2, velocity=3)
tracks[Trace].note("G4", W, velocity=2)
tracks[Trace].note("E4", W, velocity=2)

# bars 32-39: SPARK AND TRACE OVERLAP — the moment of projection
tracks[Spark].note("C4", H, velocity=4)             # the spark, fully present
tracks[Spark].note("E4", H, velocity=4)
tracks[Spark].note("G4", H, velocity=4)

tracks[Trace].rest(H)
tracks[Trace].note("C4", H, velocity=3)             # the trace begins while the spark is still speaking

tracks[Spark].note("C5", H, velocity=4)
tracks[Spark].note("G4", H, velocity=3)
tracks[Spark].note("E4", H, velocity=3)
tracks[Spark].note("C4", H, velocity=2)

tracks[Trace].note("E4", H, velocity=3)
tracks[Trace].note("G4", H, velocity=3)
tracks[Trace].note("C5", W, velocity=3)
tracks[Trace].note("G4", W, velocity=2)
tracks[Trace].note("E4", W, velocity=2)

# bars 40-47: A THIRD SPARK — barely there, already fading
tracks[Spark].note("C4", H, velocity=3)
tracks[Spark].note("E4", H, velocity=2)             # quieter — it knows it's brief
tracks[Spark].note("G4", H, velocity=2)
tracks[Spark].note("C5", H, velocity=2)

# bars 48-55: THE TRACE, ALONE — but the desire still holds underneath
tracks[Trace].note("C4", W, velocity=3)
tracks[Trace].note("E4", W, velocity=3)
tracks[Trace].note("G4", W, velocity=3)
tracks[Trace].note("C5", W*2, velocity=3)
tracks[Trace].note("G4", W, velocity=2)
tracks[Trace].note("E4", W, velocity=2)
tracks[Trace].note("C4", W, velocity=2)

# bars 56-63: THE TRACE AND THE DESIRE — the two that persist
tracks[Trace].note("C4", W*4, velocity=2)           # the trace, barely audible
tracks[Trace].note("C4", W*4, velocity=1)           # but still here
# the desire pad was always there, underneath everything

# bars 64-71: ONE LAST SPARK — the faintest
tracks[Spark].note("C5", W, velocity=2)             # the pseudophysical form
tracks[Spark].note("E5", W, velocity=2)             # identical to the spark
tracks[Spark].note("C5", W*2, velocity=1)           # appearing where the desire points

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-potentials-of-the-soul.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
