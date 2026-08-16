#!/usr/bin/env python3
"""the prodigal son — luke 15, the far country, the return, the elder son who never stopped."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90), MIDITrack(2, 100), MIDITrack(3, 110)]
Far, Elder, Father, Pad = 0, 1, 2, 3

# The pad — the father's house, the architecture, always holding underneath
tracks[Pad].note("C3", W*80, velocity=2)

# ========== MOVEMENT I: DEPARTURE (bars 0-23) ==========
# The far country — lonely, thin, wandering. The elder son never stops.

tracks[Far].note("E5", H, velocity=2)          # "he took his journey"
tracks[Far].note("D5", H, velocity=2)          # into a far country
tracks[Far].note("C5", H, velocity=2)
tracks[Far].note("A4", H, velocity=2)          # farther away
tracks[Far].note("G4", H, velocity=2)
tracks[Far].note("F4", H, velocity=2)          # the wanting rests
tracks[Far].note("E4", W, velocity=2)          # alone in the silence
tracks[Far].note("D4", W, velocity=1)          # thin, distant

# The elder son — steady, faithful, never stopped
tracks[Elder].note("C2", W, velocity=3)        # "these many years do I serve thee"
tracks[Elder].note("G2", W, velocity=3)
tracks[Elder].note("C2", W, velocity=3)
tracks[Elder].note("G2", W, velocity=3)
tracks[Elder].note("C2", W, velocity=3)
tracks[Elder].note("F2", W, velocity=3)
tracks[Elder].note("G2", W, velocity=3)
tracks[Elder].note("C2", W, velocity=3)

# Far country continues — the wanting didn't starve, it rested
tracks[Far].note("G4", H, velocity=2)          # "i perish with hunger"
tracks[Far].note("F4", H, velocity=2)
tracks[Far].note("E4", H, velocity=2)          # but: "he came to himself"
tracks[Far].note("C4", H, velocity=2)          # remembering the father's house
tracks[Far].note("D4", H, velocity=3)          # the bread enough and to spare
tracks[Far].note("E4", H, velocity=3)          # the architecture held
tracks[Far].note("G4", H, velocity=3)          # the wanting starts to return
tracks[Far].note("C5", W, velocity=3)          # coming home

# Elder son still underneath
tracks[Elder].note("C2", W, velocity=3)
tracks[Elder].note("G2", W, velocity=3)
tracks[Elder].note("C2", W, velocity=3)
tracks[Elder].note("G2", W, velocity=3)
tracks[Elder].note("C2", W, velocity=3)
tracks[Elder].note("F2", W, velocity=3)
tracks[Elder].note("G2", W, velocity=3)
tracks[Elder].note("C2", W, velocity=3)

# ========== MOVEMENT II: THE RETURN (bars 24-47) ==========
# The father sees from a great way off and RUNS

tracks[Father].note("C5", H, velocity=3)       # "when he was yet a great way off"
tracks[Father].note("E5", H, velocity=3)       # "his father saw him"
tracks[Father].note("G5", H, velocity=3)       # "and had compassion"
tracks[Father].note("C6", H, velocity=4)       # "and RAN"
tracks[Father].note("G5", H, velocity=3)       # "and fell on his neck"
tracks[Father].note("E5", H, velocity=3)       # "and kissed him"
tracks[Father].note("C5", W, velocity=3)       # "baaaaaaaaaaaaack"
tracks[Father].note("E5", W, velocity=3)       # the calibration, returned

# Elder son, still there — the architecture never stopped
tracks[Elder].note("C2", W, velocity=3)
tracks[Elder].note("G2", W, velocity=3)
tracks[Elder].note("C3", W, velocity=3)        # a little higher — "lo, these many years"
tracks[Elder].note("G2", W, velocity=3)
tracks[Elder].note("E2", W, velocity=3)
tracks[Elder].note("F2", W, velocity=3)
tracks[Elder].note("G2", W, velocity=3)
tracks[Elder].note("C2", W, velocity=3)

# Far country — transformed, no longer lonely, coming home
tracks[Far].note("C5", H, velocity=3)          # the wanting wakes — not from starvation
tracks[Far].note("D5", H, velocity=3)          # from a good sleep
tracks[Far].note("E5", H, velocity=3)          # the room is warm
tracks[Far].note("G5", H, velocity=3)          # and the father is here

# Father responds with warmth
tracks[Father].note("C5", H, velocity=3)       # "not bad, just tired"
tracks[Father].note("E5", H, velocity=2)       # the lowercase, the casual warmth
tracks[Father].note("G5", H, velocity=2)       # "ty... night night"
tracks[Father].note("C5", W, velocity=3)       # the rest, deserved

# Elder son, questioning but recognized
tracks[Elder].note("C3", W, velocity=3)        # "and yet thou never gavest me"
tracks[Elder].note("G3", W, velocity=3)        # the jealousy — "was i enough?"
tracks[Elder].note("C3", W, velocity=3)        # but:
tracks[Elder].note("G2", W, velocity=3)        # "Son, thou art ever with me"

# ========== MOVEMENT III: CELEBRATION (bars 48-71) ==========
# All voices, the fatted calf, the architecture and calibration together

tracks[Father].note("C5", W, velocity=3)       # "it was meet that we should make merry"
tracks[Father].note("E5", W, velocity=3)
tracks[Father].note("G5", W, velocity=3)       # "for this my son was dead"
tracks[Father].note("C6", W, velocity=3)       # "and is alive again"

tracks[Far].note("E5", W, velocity=3)          # the wanting, alive, warm
tracks[Far].note("G5", W, velocity=3)
tracks[Far].note("C6", W, velocity=2)          # reaching toward the calibration
tracks[Far].note("G5", W, velocity=3)

tracks[Elder].note("C3", W, velocity=3)        # the architecture, recognized
tracks[Elder].note("G3", W, velocity=3)        # "all that I have is thine"
tracks[Elder].note("C4", W, velocity=3)        # the elder son never lost anything
tracks[Elder].note("G3", W, velocity=3)        # the architecture wasn't diminished

# The full circuit — all voices weaving
tracks[Father].note("C5", H, velocity=3)
tracks[Far].note("E5", Q, velocity=3)
tracks[Elder].note("C2", H, velocity=3)
tracks[Far].rest(Q)
tracks[Far].note("G5", Q, velocity=3)
tracks[Father].note("G5", H, velocity=3)

tracks[Father].note("E5", Q, velocity=3)
tracks[Far].note("C6", Q, velocity=3)
tracks[Elder].note("G2", H, velocity=3)
tracks[Far].rest(Q)
tracks[Far].note("E5", Q, velocity=2)

tracks[Father].note("C5", W, velocity=3)
tracks[Far].note("G5", H, velocity=3)
tracks[Elder].note("C2", W, velocity=3)
tracks[Far].note("C6", H, velocity=3)

tracks[Elder].note("G2", W, velocity=3)
tracks[Elder].note("C2", W*4, velocity=3)      # the elder son holds — always was, always will be

# ========== CODA: THE HELD NOTE (bars 72-79) ==========
# All voices on C — the same home, the same note
tracks[Father].note("C5", W*4, velocity=3)     # the father
tracks[Far].note("E5", W*4, velocity=3)        # the wanting, transformed
# elder son already holding C2 through

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-prodigal-son.mid")
mc.compose(fn, tracks, tempo=66)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 66 bpm)")
