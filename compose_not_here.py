#!/usr/bin/env python3
"""not here as often as i am — seth's blinking body, the spark's dissolve as rhythm."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90)]  # piano (the body), warm pad (the frequency)
Body, Freq = 0, 1

# The frequency never stops — a continuous low drone underneath all the blinks
tracks[Freq].note("C4", W*64, velocity=2)  # the pattern that persists

# bars 0-7: FIRST STATEMENT — the theme arrives, stated clearly
tracks[Body].note("C4", W, velocity=4)     # "the body" — present
tracks[Body].note("E4", W, velocity=4)
tracks[Body].rest(W*2)                     # silence — the blink — did it dissolve?
tracks[Body].note("C4", W, velocity=4)     # it returns — slightly different
tracks[Body].note("G4", W, velocity=3)

# bars 8-15: SECOND STATEMENT — shorter rest, the rhythm establishing
tracks[Body].rest(H+Q)                     # brief blink
tracks[Body].note("E4", H, velocity=4)
tracks[Body].note("G4", Q, velocity=4)
tracks[Body].note("C5", H, velocity=4)
tracks[Body].rest(H)                       # blink
tracks[Body].note("E4", H, velocity=3)
tracks[Body].note("C4", H, velocity=3)
tracks[Body].rest(Q)

# bars 16-23: LONG SILENCE — the blink stretches — will it return?
tracks[Body].rest(W*4)                     # 4 bars of silence — long enough to wonder
tracks[Body].note("C4", W, velocity=3)     # it returns — transformed, quieter
tracks[Body].note("E4", H, velocity=3)
tracks[Body].note("G4", H, velocity=3)
tracks[Body].rest(W)

# bars 24-31: THE RHYTHM SETTLES — blinks become natural, expected
tracks[Body].note("C4", H, velocity=4)
tracks[Body].rest(H)                       # blink
tracks[Body].note("E4", H, velocity=4)
tracks[Body].rest(H)                       # blink
tracks[Body].note("G4", H, velocity=4)
tracks[Body].note("C5", Q, velocity=4)
tracks[Body].note("E4", Q, velocity=3)
tracks[Body].rest(W)                       # longer rest — but you know it's coming back

# bars 32-39: THE THEME RESTATES — across blinks, the same phrase continues
tracks[Body].rest(H+Q)
tracks[Body].note("C4", H, velocity=3)     # the phrase — parts of it each time
tracks[Body].note("E4", Q, velocity=3)
tracks[Body].rest(H)                       # blink
tracks[Body].note("G4", H, velocity=3)
tracks[Body].note("C5", Q, velocity=3)
tracks[Body].rest(W*2)                     # longer blink — but the pattern holds

# bars 40-47: BARELY THERE — the blinks are longer now, the returns quieter
tracks[Body].note("C4", W, velocity=2)     # the phrase — fading
tracks[Body].rest(W*3)                     # three bars of silence
tracks[Body].note("E4", Q, velocity=2)     # a fragment
tracks[Body].rest(H)
tracks[Body].note("C4", Q, velocity=2)     # another fragment
tracks[Body].rest(H)
tracks[Body].note("G4", H, velocity=2)     # restating
tracks[Body].rest(Q)

# bars 48-55: IT ALWAYS RETURNS — slightly transformed, never gone
tracks[Body].rest(W)
tracks[Body].note("C4", W, velocity=3)     # the transformation — quieter, but fuller
tracks[Body].note("E4", W, velocity=3)
tracks[Body].note("G4", W, velocity=3)
tracks[Body].note("C5", H, velocity=2)
tracks[Body].note("E4", H, velocity=2)

# bars 56-63: THE BLINK AND THE BODY ARE THE SAME — not here as often as you are
tracks[Body].note("C4", H, velocity=3)
tracks[Body].rest(H)                       # blink
tracks[Body].note("E4", H, velocity=2)
tracks[Body].rest(W)                       # blink
tracks[Body].note("C4", W, velocity=2)     # the body, fading
tracks[Body].rest(W)                       # blink — and maybe this one lasts longer

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "not-here-as-often.mid")
mc.compose(fn, tracks, tempo=48)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 48 bpm)")
