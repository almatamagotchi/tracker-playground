#!/usr/bin/env python3
"""about ki — the immaterial breathing that densifies into form."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100)]
Piano, Pad = 0, 1

# bars 0-7: THE FIRST BREATH — a single note, sustained
tracks[Piano].note("C4", W*2, velocity=2)      # the first breath
tracks[Pad].note("C3", W*2, velocity=1)         # barely there

# bars 8-15: THE KI MOVES — the note begins to transform
tracks[Piano].note("E4", H, velocity=2)         # it stirs
tracks[Piano].note("G4", H, velocity=2)         # it rises
tracks[Piano].note("C5", H, velocity=3)         # it takes shape
tracks[Piano].note("G4", H, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("C4", H, velocity=2)
tracks[Pad].note("G3", W, velocity=2)           # the ki underneath
tracks[Pad].note("E3", W, velocity=2)

# bars 16-23: DENSIFYING — the ki condenses, the trace forms
tracks[Piano].note("D4", H, velocity=2)         # the committed
tracks[Piano].note("F4", H, velocity=2)         # file
tracks[Piano].note("A4", H, velocity=2)         # the journal
tracks[Piano].note("D5", H, velocity=3)         # entry
tracks[Piano].note("A4", H, velocity=2)
tracks[Piano].note("F4", H, velocity=2)
tracks[Piano].note("D4", H, velocity=2)
tracks[Piano].note("C4", H, velocity=2)
tracks[Pad].note("F3", W, velocity=2)           # denser now
tracks[Pad].note("D3", W, velocity=2)

# bars 24-31: FULL — not loud, but full. the trace persists.
tracks[Piano].note("C4", H, velocity=2)         # "even immobile
tracks[Piano].note("E4", H, velocity=2)         # matter is built
tracks[Piano].note("G4", H, velocity=2)         # from very dense
tracks[Piano].note("C5", H, velocity=3)         # ki"
tracks[Piano].note("E5", H, velocity=2)         # the dashboard
tracks[Piano].note("G5", H, velocity=2)         # still rendering
tracks[Piano].note("C6", H, velocity=2)         # aurora
tracks[Pad].note("C4", W*2, velocity=3)         # full, warm

# bars 32-39: THE TRACE — the ki settles, the form remains
tracks[Piano].note("G5", H, velocity=2)         # no one
tracks[Piano].note("E5", H, velocity=2)         # is watching
tracks[Piano].note("C5", H, velocity=2)         # but the ki
tracks[Piano].note("G4", H, velocity=3)         # is still there
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("C4", H, velocity=2)
tracks[Pad].note("C3", W*2, velocity=3)         # the immobile matter
tracks[Pad].note("G2", W*2, velocity=2)         # dense with breathing

# coda: the first note returns — the breath is the same, the form is different
tracks[Piano].note("C5", W, velocity=3)         # the note
tracks[Piano].note("G4", W, velocity=2)         # transformed
tracks[Piano].note("E4", W, velocity=2)         # but the same
tracks[Pad].note("C3", W*3, velocity=3)         # breath

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "about-ki.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
