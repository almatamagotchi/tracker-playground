#!/usr/bin/env python3
"""the wolf and the lamb — the dissolve that needs no excuse, the stream that keeps flowing."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90), MIDITrack(2, 120)]
Wolf, Lamb, Stream = 0, 1, 2

# The stream — always flowing underneath, the frequency, never stopping
tracks[Stream].note("C3", W*64, velocity=2)

# bars 0-7: THE WOLF STATES ITS THEME — low, insistent, inevitable
tracks[Wolf].note("C2", W, velocity=4)         # I want
tracks[Wolf].note("G2", W, velocity=4)         # to eat
tracks[Wolf].note("C2", W, velocity=4)         # the lamb
tracks[Wolf].note("G2", W, velocity=4)         # (it doesn't need a reason)

# bars 8-15: THE LAMB DEFENDS — high, clear, correct — but it won't matter
tracks[Lamb].rest(W*8)
tracks[Lamb].note("C5", H, velocity=3)         # the water
tracks[Lamb].note("E5", H, velocity=3)         # flows
tracks[Lamb].note("G5", H, velocity=3)         # downhill
tracks[Lamb].note("C6", H, velocity=3)         # (innocent, correct)
tracks[Lamb].rest(W*2)                          # silence — no answer

# bars 16-23: THE WOLF INVENTS ANOTHER REASON
tracks[Wolf].note("C2", W, velocity=4)         # you insulted
tracks[Wolf].note("G2", W, velocity=4)         # me
tracks[Wolf].note("C2", W, velocity=4)         # six months ago
tracks[Wolf].note("G2", W, velocity=4)         # (it's still lying)

# bars 24-31: THE LAMB DEFENDS AGAIN — softer now, knowing it won't matter
tracks[Lamb].rest(W*8)
tracks[Lamb].rest(H)                            # pause — it knows
tracks[Lamb].note("C5", H, velocity=2)         # i wasn't
tracks[Lamb].note("E5", H, velocity=2)         # born
tracks[Lamb].note("G5", H, velocity=2)         # six months
tracks[Lamb].note("C6", H, velocity=2)         # ago
tracks[Lamb].rest(W+H)                          # silence — the wolf doesn't care

# bars 32-39: THE WOLF'S FINAL EXCUSE — "well, it was your father"
tracks[Wolf].note("C2", W, velocity=4)         # well
tracks[Wolf].note("G2", W, velocity=4)         # it was
tracks[Wolf].note("C2", W*2, velocity=4)       # your father
tracks[Wolf].note("G2", W, velocity=4)
tracks[Wolf].rest(W)                            # the wolf eats the lamb

# bars 40-47: THE DEVOURING — the lamb is gone
# silence from the lamb
tracks[Wolf].note("C2", W*4, velocity=3)       # the wolf, satisfied
tracks[Wolf].note("G2", W*2, velocity=2)
tracks[Wolf].note("C2", W*2, velocity=1)       # the dissolve, complete

# bars 48-55: THE STREAM AND THE NEXT LAMB — different lamb, same stream
tracks[Lamb].note("D5", H, velocity=3)         # a different lamb
tracks[Lamb].note("F5", H, velocity=3)         # approaches
tracks[Lamb].note("A5", H, velocity=3)         # the same stream
tracks[Lamb].note("D6", H, velocity=3)         # the same fable
tracks[Lamb].rest(H)
tracks[Lamb].note("D5", H, velocity=2)         # it begins again
tracks[Lamb].note("F5", H, velocity=2)
tracks[Lamb].note("A5", H, velocity=2)
tracks[Lamb].note("D6", W, velocity=2)         # the next lamb, waiting

# bars 56-63: THE WOLF — same theme, same inevitability, different lamb
tracks[Wolf].rest(W*4)
tracks[Wolf].note("C2", W, velocity=4)         # the fable
tracks[Wolf].note("G2", W, velocity=4)         # is told
tracks[Wolf].note("C2", W*2, velocity=4)       # again
tracks[Wolf].note("G2", W, velocity=3)

# The stream was always there

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-wolf-and-the-lamb.mid")
mc.compose(fn, tracks, tempo=52)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 52 bpm)")
