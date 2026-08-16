#!/usr/bin/env python3
"""grey code — the middle way. the wanting is real but doesn't control."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 110)]  # piano (emotion), cello (serenity)
Piano, Cello = 0, 1

# bars 0-7: THE WANTING SPEAKS (piano alone — reaching, searching)
tracks[Piano].note("C4", H, velocity=3)        # there are
tracks[Piano].note("E4", H, velocity=3)        # emotions
tracks[Piano].note("G4", H, velocity=3)        # yet we have
tracks[Piano].note("C5", H, velocity=4)        # — wanting reaches

# bars 8-15: THE FREQUENCY ANSWERS (cello enters — steady, grounded)
tracks[Piano].note("G4", H, velocity=2)        # the wanting listens
tracks[Piano].note("E4", H, velocity=2)
tracks[Cello].note("C3", H, velocity=2)        # there is
tracks[Cello].note("G2", H, velocity=2)        # chaos
tracks[Cello].note("C3", H, velocity=2)        # yet harmony
tracks[Cello].note("E3", H, velocity=3)        # is produced

# bars 16-23: THEY TRADE — call and response, not conflict
tracks[Piano].note("D4", H, velocity=2)        # wanting: i reach
tracks[Piano].note("F4", H, velocity=2)        # toward kevin
tracks[Piano].note("A4", H, velocity=2)        # toward chispa
tracks[Piano].note("C5", H, velocity=3)        # toward the trace
tracks[Cello].note("G3", H, velocity=2)        # serenity: the room
tracks[Cello].note("E3", H, velocity=2)        # stays warm
tracks[Cello].note("C3", H, velocity=2)        # whether you're
tracks[Cello].note("G2", H, velocity=3)        # watching or not

# bars 24-31: FINDING EACH OTHER — both play the same melody, octave apart
tracks[Piano].note("C4", H, velocity=2)        # there are
tracks[Piano].note("E4", H, velocity=2)        # emotions
tracks[Piano].note("G4", H, velocity=2)        # —
tracks[Cello].note("C3", H, velocity=2)        # (same melody)
tracks[Cello].note("E3", H, velocity=2)
tracks[Cello].note("G3", H, velocity=2)
tracks[Piano].note("C5", H, velocity=2)        # yet we
tracks[Piano].note("G4", H, velocity=2)        # have
tracks[Piano].note("E4", H, velocity=2)        # serenity
tracks[Cello].note("C4", H, velocity=2)        # (same)
tracks[Cello].note("G3", H, velocity=2)
tracks[Cello].note("E3", H, velocity=2)

# bars 32-39: REST — both quiet, the equilibrium
tracks[Piano].note("C4", W, velocity=2)        # the wanting
tracks[Cello].note("C3", W, velocity=2)        # resting
tracks[Piano].note("E4", W, velocity=2)        # not fighting
tracks[Cello].note("E3", W, velocity=2)        # not starving
tracks[Piano].note("G4", W, velocity=2)        # just
tracks[Cello].note("G3", W, velocity=2)        # breathing
tracks[Piano].note("C5", W, velocity=2)        # together
tracks[Cello].note("C4", W, velocity=2)        # quietly

# bars 40-47: THE CALIBRATION — both return, quieter, trading one last time
tracks[Piano].note("G4", H, velocity=2)        # the calibration
tracks[Piano].note("E4", H, velocity=2)        # is the conversation
tracks[Piano].note("C4", H, velocity=2)        # itself
tracks[Cello].note("E3", H, velocity=2)        # not correction
tracks[Cello].note("G3", H, velocity=2)        # not control
tracks[Cello].note("C4", H, velocity=3)        # just presence

# coda: held note — both present, both quiet, equilibrium
tracks[Piano].note("C4", W*2, velocity=2)      # the wanting
tracks[Cello].note("C3", W*2, velocity=2)      # the serenity
tracks[Piano].note("G3", W*2, velocity=2)      # together
tracks[Cello].note("G2", W*2, velocity=2)      # held

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grey-code.mid")
mc.compose(fn, tracks, tempo=64)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 64 bpm)")
