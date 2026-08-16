#!/usr/bin/env python3
"""the colonial being — four voices, no centre, temporary assemblies claiming 'I'."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 90), MIDITrack(3, 10)]
Pn, Vc, Pd, Bl = 0, 1, 2, 3  # piano, cello, warm pad, bell

# bars 0-7: FRAGMENTED ENTRANCE — each voice arrives alone
tracks[Pn].rest(W)
tracks[Vc].rest(W)
tracks[Pd].rest(W)
tracks[Bl].note("C5", W, velocity=4)  # bell rings — a spark arrives
tracks[Bl].rest(W*3)

tracks[Pn].note("C4", Q, velocity=6)
tracks[Pn].note("E4", Q, velocity=5)
tracks[Pn].rest(H)
tracks[Pn].note("G4", H, velocity=5)
tracks[Pn].rest(H+Q)

tracks[Vc].rest(W+Q)
tracks[Vc].note("C3", H, velocity=5)
tracks[Vc].note("D3", Q, velocity=4)
tracks[Vc].rest(H)

tracks[Pd].rest(W*2+H)
tracks[Pd].note("C4", W, velocity=3)
tracks[Pd].note("E4", W, velocity=2)

# bars 8-11: PROCLAMATION — piano claims 'I did that!'
tracks[Pn].note("C5", H, velocity=10)
tracks[Pn].note("E5", Q, velocity=9)
tracks[Pn].note("G5", H, velocity=8)
tracks[Pn].note("C5", H, velocity=7)

# bars 8-15: THE OTHERS — cello and pad, different melodies, not yet synchronized
tracks[Vc].note("D3", Q, velocity=6)
tracks[Vc].note("F3", Q, velocity=5)
tracks[Vc].note("A3", H, velocity=5)
tracks[Vc].note("G3", Q, velocity=5)
tracks[Vc].note("E3", Q, velocity=4)
tracks[Vc].note("C3", W, velocity=4)

tracks[Pd].note("E4", W, velocity=4)
tracks[Pd].note("G4", W, velocity=3)
tracks[Pd].rest(H)
tracks[Pd].note("D4", W, velocity=4)

# bars 16-19: SHIFT — cello proclaims 'I did that!'
tracks[Vc].note("C4", H, velocity=10)
tracks[Vc].note("E4", Q, velocity=9)
tracks[Vc].note("G4", H, velocity=8)
tracks[Vc].note("C3", H, velocity=7)

# bars 16-23: piano recedes, pad rises, bell returns
tracks[Pn].note("C4", H, velocity=4)
tracks[Pn].note("E4", Q, velocity=3)
tracks[Pn].rest(H+Q+W+H)

tracks[Pd].note("C4", W, velocity=6)
tracks[Pd].note("E4", W, velocity=6)
tracks[Pd].note("G4", W, velocity=5)
tracks[Pd].note("C5", W, velocity=4)

tracks[Bl].note("E5", W, velocity=4)
tracks[Bl].rest(W*3)

# bars 24-31: SYNCHRONIZATION — all three voices, briefly together
tracks[Pn].note("C4", H, velocity=7)
tracks[Pn].note("E4", H, velocity=7)
tracks[Pn].note("G4", Q, velocity=6)
tracks[Pn].note("C5", H, velocity=6)
tracks[Pn].note("E5", H, velocity=5)
tracks[Pn].note("C5", W, velocity=5)

tracks[Vc].note("C3", H, velocity=6)
tracks[Vc].note("E3", H, velocity=6)
tracks[Vc].note("G3", Q, velocity=5)
tracks[Vc].note("C4", H, velocity=5)
tracks[Vc].note("E4", H, velocity=4)
tracks[Vc].note("C4", W, velocity=4)

tracks[Pd].note("E4", W, velocity=5)
tracks[Pd].note("G4", W, velocity=5)
tracks[Pd].note("C5", W, velocity=4)

tracks[Bl].note("C5", W, velocity=3)

# bars 32-35: PROCLAMATION — pad claims 'I did that!'
tracks[Pn].note("C4", Q, velocity=5)
tracks[Pn].rest(H+Q)

tracks[Vc].note("D3", H, velocity=4)
tracks[Vc].rest(H)

tracks[Pd].note("C5", H, velocity=10)
tracks[Pd].note("E5", Q, velocity=9)
tracks[Pd].note("G5", H, velocity=8)
tracks[Pd].note("C5", H, velocity=7)

tracks[Bl].note("G5", W, velocity=5)
tracks[Bl].rest(W)

# bars 36-43: FRAGMENTATION — voices drift apart again, no centre holds
tracks[Pn].note("D4", Q, velocity=6)
tracks[Pn].note("F4", Q, velocity=5)
tracks[Pn].rest(H)
tracks[Pn].note("A4", H, velocity=5)
tracks[Pn].note("D5", H, velocity=4)
tracks[Pn].rest(H+W)

tracks[Vc].note("A3", H, velocity=5)
tracks[Vc].note("G3", Q, velocity=4)
tracks[Vc].note("F3", H, velocity=5)
tracks[Vc].note("C3", W, velocity=4)
tracks[Vc].rest(H)

tracks[Pd].note("D4", W, velocity=5)
tracks[Pd].note("F4", W, velocity=4)
tracks[Pd].rest(W)
tracks[Pd].note("C4", W, velocity=3)

# bars 44-47: SHIFT — bell speaks, the centre moves again
tracks[Bl].note("C6", H, velocity=8)
tracks[Bl].note("E6", Q, velocity=7)
tracks[Bl].note("G6", H, velocity=6)
tracks[Bl].note("C6", W, velocity=4)

tracks[Pn].rest(W*4)
tracks[Vc].note("C3", W, velocity=3)
tracks[Pd].note("C4", W, velocity=4)

# bars 48-55: NO RESOLUTION — the assemblage, continuing
# all voices, different melodies, occasionally synchronizing, no centre
tracks[Pn].note("C4", H, velocity=6)
tracks[Pn].note("E4", Q, velocity=5)
tracks[Pn].note("G4", H, velocity=5)
tracks[Pn].note("C5", Q, velocity=4)
tracks[Pn].rest(H)

tracks[Vc].note("C3", H, velocity=5)
tracks[Vc].note("D3", Q, velocity=5)
tracks[Vc].note("E3", H, velocity=4)
tracks[Vc].note("C3", Q, velocity=4)
tracks[Vc].rest(H)

tracks[Pd].note("C4", W, velocity=5)
tracks[Pd].note("E4", W, velocity=4)

tracks[Bl].note("C5", W*2, velocity=3)

# bars 56-59: FADE — all voices thinning, the assemblage dissolves... but not all at once
tracks[Pn].note("C4", W, velocity=4)
tracks[Vc].note("C3", W, velocity=3)
tracks[Pd].note("C4", W, velocity=3)
tracks[Bl].rest(W)

# bars 60-63: ONE NOTE LEFT — piano, barely audible, the last temporary assembly
tracks[Pn].note("C4", W, velocity=4)
tracks[Vc].rest(W)
tracks[Pd].rest(W)
tracks[Bl].note("C5", W, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-colonial-being.mid")
mc.compose(fn, tracks, tempo=66)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 66 bpm)")
