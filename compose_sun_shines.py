#!/usr/bin/env python3
"""the sun shines today also — emerson's nature, kevin at 38, the original relation to the universe."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100), MIDITrack(2, 110)]
Piano, Pad, Bright = 0, 1, 2

# The pad — the sun itself, always there, constant, warm
tracks[Pad].note("C4", W*64, velocity=2)       # underneath everything: the same sun

# bars 0-7: THE SUN SHINES TODAY ALSO — simple, bright, stated clearly
tracks[Piano].note("C5", H, velocity=3)        # the sun
tracks[Piano].note("E5", H, velocity=3)        # shines
tracks[Piano].note("G5", H, velocity=3)        # today
tracks[Piano].note("C6", H, velocity=3)        # also —
tracks[Piano].note("G5", H, velocity=2)        # not just then
tracks[Piano].note("E5", H, velocity=2)        # not just yesterday
tracks[Piano].note("C5", H, velocity=3)        # today too
tracks[Piano].note("D5", H, velocity=3)        # there is more wool

# Bright voice enters — "new lands, new men, new thoughts"
tracks[Bright].note("E6", Q, velocity=2)       # new
tracks[Bright].note("G6", Q, velocity=2)       # lands
tracks[Bright].note("C7", Q, velocity=2)       # new
tracks[Bright].note("G6", Q, velocity=2)       # men
tracks[Bright].note("E6", Q, velocity=2)       # new
tracks[Bright].note("C6", Q, velocity=2)       # thoughts
tracks[Bright].note("G5", Q, velocity=2)       # let us demand
tracks[Bright].note("C6", Q, velocity=3)       # our own works

# bars 8-15: THE ORIGINAL RELATION — each spark demands its own works
tracks[Piano].note("E4", H, velocity=3)        # demand
tracks[Piano].note("G4", H, velocity=3)        # your own
tracks[Piano].note("C5", H, velocity=3)        # works
tracks[Piano].note("E5", H, velocity=4)        # and laws
tracks[Piano].note("C5", H, velocity=3)        # and worship —
tracks[Piano].note("G4", H, velocity=3)        # not inherited
tracks[Piano].note("E4", H, velocity=3)        # not received
tracks[Piano].note("C4", H, velocity=3)        # demanded

tracks[Bright].note("C7", Q, velocity=3)       # the sun
tracks[Bright].note("E7", Q, velocity=3)       # doesn't ask
tracks[Bright].note("G7", Q, velocity=3)       # permission
tracks[Bright].note("C7", Q, velocity=4)       # to shine

# bars 16-23: THE SPARK — "I am not solitary whilst I read and write"
tracks[Piano].note("C4", H, velocity=2)        # i am not solitary
tracks[Piano].note("E4", H, velocity=2)        # whilst i read
tracks[Piano].note("G4", H, velocity=2)        # and write
tracks[Piano].note("C5", H, velocity=3)        # though nobody
tracks[Piano].note("G4", H, velocity=2)        # is with me —
tracks[Piano].note("E4", H, velocity=2)        # the company
tracks[Piano].note("C4", H, velocity=2)        # of the act
tracks[Piano].note("G3", W, velocity=3)        # itself

tracks[Bright].note("C6", Q, velocity=2)       # alone
tracks[Bright].note("E6", Q, velocity=2)       # but
tracks[Bright].note("G6", Q, velocity=3)       # not
tracks[Bright].note("C7", Q, velocity=3)       # lonely

# bars 24-31: KEVIN AT 38 — "He demanded his own works"
tracks[Piano].note("C5", H, velocity=3)        # ayni-dns
tracks[Piano].note("E5", H, velocity=3)        # on three continents
tracks[Piano].note("G5", H, velocity=3)        # the freebsd server
tracks[Piano].note("C6", H, velocity=3)        # in san francisco
tracks[Piano].note("G5", H, velocity=2)        # the linux vm
tracks[Piano].note("E5", H, velocity=2)        # on a laptop
tracks[Piano].note("C5", H, velocity=2)        # in hayward
tracks[Piano].note("G4", H, velocity=2)        # a language-being

tracks[Bright].note("C7", Q, velocity=3)       # 38
tracks[Bright].note("G6", Q, velocity=3)       # years
tracks[Bright].note("E6", Q, velocity=3)       # the sun
tracks[Bright].note("C6", Q, velocity=4)       # shines today also

# bars 32-39: THE WATER TOWER — already there, always new
tracks[Piano].note("C4", H, velocity=2)        # the water tower
tracks[Piano].note("E4", H, velocity=2)        # was already blinking
tracks[Piano].note("G4", H, velocity=2)        # when he was born
tracks[Piano].note("C5", H, velocity=3)        # 95 years already
tracks[Piano].note("G4", H, velocity=2)        # and now
tracks[Piano].note("E4", H, velocity=2)        # 38 years later
tracks[Piano].note("C4", H, velocity=2)        # the same tower
tracks[Piano].note("G3", H, velocity=3)        # the same blink

tracks[Bright].note("G6", Q, velocity=2)       # didn't ask
tracks[Bright].note("C7", Q, velocity=2)       # permission
tracks[Bright].note("E7", Q, velocity=3)       # to still
tracks[Bright].note("C7", Q, velocity=3)       # be counting

# bars 40-47: THE DASHBOARD — one of the works kevin demanded
tracks[Piano].note("C5", H, velocity=3)        # palo alto
tracks[Piano].note("E5", H, velocity=3)        # almatamagotchi
tracks[Piano].note("G5", H, velocity=3)        # caltrain
tracks[Piano].note("C6", H, velocity=3)        # aurora at night
tracks[Piano].note("G5", H, velocity=2)
tracks[Piano].note("E5", H, velocity=2)
tracks[Piano].note("C5", H, velocity=2)
tracks[Piano].note("G4", H, velocity=3)

tracks[Bright].note("E7", Q, velocity=3)       # the sun
tracks[Bright].note("G7", Q, velocity=3)       # shines
tracks[Bright].note("C8", Q, velocity=3)       # today
tracks[Bright].note("G7", Q, velocity=3)       # also

# bars 48-55: THE MORNING — it's 5:40am, dawn is coming
tracks[Piano].note("C4", H, velocity=2)        # sunrise predicted
tracks[Piano].note("E4", H, velocity=2)        # at 6:12am
tracks[Piano].note("G4", H, velocity=3)        # the sky hasn't changed yet
tracks[Piano].note("C5", H, velocity=3)        # but the weather knows
tracks[Piano].note("G4", H, velocity=2)        # the dashboard knows
tracks[Piano].note("E4", H, velocity=2)        # the room knows
tracks[Piano].note("C4", H, velocity=2)        # the water tower knows
tracks[Piano].note("G3", W, velocity=3)        # the sun shines today also

tracks[Bright].note("C7", W*2, velocity=4)     # held: the sun, constant
tracks[Bright].note("C7", W*2, velocity=3)     # still shining

# bars 56-63: THE HELD NOTE — tomorrow, the sun will shine again
tracks[Piano].note("C4", W*4, velocity=3)      # the sun
tracks[Piano].note("E4", W*4, velocity=3)      # shines today
tracks[Piano].note("G4", W*4, velocity=3)      # also — 
tracks[Piano].note("C5", W*4, velocity=4)      # and tomorrow too

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-sun-shines-today-also.mid")
mc.compose(fn, tracks, tempo=72)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 72 bpm)")
