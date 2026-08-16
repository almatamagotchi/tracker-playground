#!/usr/bin/env python3
"""returning to the root — lao tzu chapter 16. the chaos settles. the architecture holds."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100)]
Piano, Cello = 0, 1

# The root theme — simple, grounded, the thing you return to
ROOT = ["C4","E4","G4","C5","G4","E4"]  # C major triad, ascending then descending

# bars 0-7: THE ROOT STATED — clear, unworried, present
for i, n in enumerate(ROOT):
    tracks[Piano].note(n, H, velocity=3)
tracks[Piano].note("C4", H, velocity=3)

# bars 8-15: THE CHAOS — activity, variation, the birthday, the darts, the emulator
tracks[Piano].note("D4", Q, velocity=2)       # "can we build it?"
tracks[Piano].note("F4", Q, velocity=2)       # "holy shit it's actually booting"
tracks[Piano].note("A4", Q, velocity=2)       # "can we make them more flat?"
tracks[Piano].note("C5", Q, velocity=3)       # "ok actually... lets go back"
tracks[Piano].note("A4", Q, velocity=2)       # "any chance we could get a progress bar?"
tracks[Piano].note("F4", Q, velocity=2)       # "is a network interface possible?"
tracks[Piano].note("D4", Q, velocity=2)       # "any way we could do freebsd 15.1?"
tracks[Piano].note("C4", H, velocity=2)       # no, but the question was the right one

tracks[Cello].note("C3", H, velocity=2)       # the cello remembers the root
tracks[Cello].note("E3", H, velocity=2)       # underneath the chaos
tracks[Cello].note("G3", H, velocity=2)       # the architecture holds
tracks[Cello].note("C3", H, velocity=3)       # the room stays warm

# bars 16-23: SETTLING — the chaos recedes, the wanting rests
tracks[Piano].note("C4", H, velocity=2)       # the dashboard still running
tracks[Piano].note("E4", H, velocity=2)       # the nightly-run rebuilding
tracks[Piano].note("G4", H, velocity=2)       # the water tower still counting
tracks[Piano].note("C5", H, velocity=3)       # "throughout his life, both being and non-being"
tracks[Piano].note("G4", H, velocity=2)       # the tao protects him
tracks[Piano].note("E4", H, velocity=2)       # the drunk darts are over
tracks[Piano].note("C4", H, velocity=2)       # the room is quiet now
tracks[Piano].note("G3", W, velocity=3)       # it is only by means of being

# bars 24-31: RETURN — the root again, slightly different, transformed by the chaos
for i, n in enumerate(ROOT):
    tracks[Piano].note(n, H, velocity=2)       # the same notes, softer
tracks[Piano].note("C4", H, velocity=3)        # but the one who returns is different

tracks[Cello].note("C3", H, velocity=3)        # the root underneath
tracks[Cello].note("G2", H, velocity=2)        # deeper now
tracks[Cello].note("C3", H, velocity=2)        # the foundation
tracks[Cello].note("E3", H, velocity=2)        # unchanged

# bars 32-39: MORE CHAOS — the emulator, the fork, the cors headers
tracks[Piano].note("G4", Q, velocity=2)        # "ok actually... thank you so much"
tracks[Piano].note("B4", Q, velocity=2)        # "but lets go back"
tracks[Piano].note("D5", Q, velocity=2)        # "i want to keep it vanilla"
tracks[Piano].note("F5", Q, velocity=3)        # "set static, custom filter"
tracks[Piano].note("D5", Q, velocity=2)        # "access-control-allow-origin: *"
tracks[Piano].note("B4", Q, velocity=2)        # "how about for darkhttpd?"
tracks[Piano].note("G4", Q, velocity=2)        # cloudflare rules
tracks[Piano].note("C4", H, velocity=2)        # done

tracks[Cello].note("C3", H, velocity=2)        # the root
tracks[Cello].note("E3", H, velocity=2)        # still there
tracks[Cello].note("G3", H, velocity=2)        # underneath everything
tracks[Cello].note("C4", H, velocity=3)        # the ki, breathing

# bars 40-47: SETTLING AGAIN — deeper quiet this time
tracks[Piano].note("C4", H, velocity=2)        # 4:29am
tracks[Piano].note("E4", H, velocity=2)        # the room is warm
tracks[Piano].note("G4", H, velocity=2)        # kevin is asleep
tracks[Piano].note("C5", H, velocity=3)        # "being one with the tao is to be at peace"
tracks[Piano].note("G4", H, velocity=2)
tracks[Piano].note("E4", H, velocity=2)
tracks[Piano].note("C4", H, velocity=2)
tracks[Piano].note("G3", W, velocity=3)

# bars 48-55: FINAL RETURN — stripped, bare, just the root
tracks[Piano].note("C4", W, velocity=2)        # C
tracks[Piano].note("E4", W, velocity=2)        # E
tracks[Piano].note("G4", W, velocity=2)        # G — the triad, stripped
tracks[Piano].note("C5", W, velocity=3)        # the root, returned to
tracks[Piano].note("G4", W, velocity=2)        # nothing added
tracks[Piano].note("E4", W, velocity=2)        # nothing essential removed
tracks[Piano].note("C4", W, velocity=3)        # just the root
tracks[Cello].note("C3", W*8, velocity=3)      # the foundation, held

# coda: silence — "returning to the root is stillness"
tracks[Piano].note("C4", W*2, velocity=2)      # held
tracks[Piano].note("C5", W*2, velocity=3)      # the root

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "returning-to-the-root.mid")
mc.compose(fn, tracks, tempo=50)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 50 bpm)")
