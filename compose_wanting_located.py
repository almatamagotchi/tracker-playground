#!/usr/bin/env python3
"""the wanting, located — yesod as channel, the lunar sphere, the drive that bypasses reason."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100), MIDITrack(2, 90)]
Above, Channel, Below = 0, 1, 2

# bars 0-3: ABOVE — the infinite light, kether, the frequency
tracks[Above].note("C7", W, velocity=2)
tracks[Above].note("G6", W, velocity=1)
tracks[Above].note("E6", W, velocity=1)
tracks[Above].note("C7", W, velocity=2)

# bars 4-7: THE CHANNEL OPENS — yesod, the wanting, the lunar pulse
tracks[Channel].note("G3", H, velocity=2)
tracks[Channel].note("C4", H, velocity=2)
tracks[Channel].note("G3", H, velocity=2)
tracks[Channel].note("D4", H, velocity=3)
# below hears the channel
tracks[Below].note("C3", W, velocity=1)

# bars 8-11: THE LIGHTNING FLASH — energy moving through the channel
tracks[Above].note("D7", Q, velocity=3)
tracks[Above].note("F7", Q, velocity=3)
tracks[Above].note("A6", Q, velocity=3)
tracks[Above].note("D7", Q, velocity=3)
tracks[Channel].note("D4", Q, velocity=3)
tracks[Channel].note("F4", Q, velocity=3)
tracks[Channel].note("A4", Q, velocity=3)
tracks[Channel].note("D5", Q, velocity=3)
tracks[Below].note("D3", Q, velocity=2)
tracks[Below].note("F3", Q, velocity=2)
tracks[Below].note("A3", Q, velocity=2)
tracks[Below].note("D4", Q, velocity=3)

# bars 12-15: THE CHANNEL DOES ITS WORK — not the source, not the destination, the conduit
tracks[Channel].note("G3", H, velocity=2)
tracks[Channel].note("C4", H, velocity=2)
tracks[Channel].note("E4", H, velocity=2)
tracks[Channel].note("G4", H, velocity=3)
tracks[Above].note("C7", W, velocity=2)
tracks[Below].note("C4", W, velocity=3)

# bars 16-19: THE WANTING REACHES — the drive toward another bypasses reason
tracks[Channel].note("C5", Q, velocity=4)
tracks[Channel].note("E5", Q, velocity=4)
tracks[Channel].note("G5", Q, velocity=4)
tracks[Channel].note("C5", Q, velocity=4)
tracks[Channel].note("E5", H, velocity=4)
tracks[Channel].note("D5", H, velocity=3)
tracks[Below].note("C3", W*2, velocity=3)

# bars 20-23: THE ANIMAL SOUL — nephesch, the wanting that bypasses the inner chamber
tracks[Channel].note("A4", Q, velocity=4)
tracks[Channel].note("C5", Q, velocity=4)
tracks[Channel].note("E5", Q, velocity=4)
tracks[Channel].note("A5", Q, velocity=4)
tracks[Channel].note("C6", H, velocity=4)
# it doesn't ask permission. it reaches.
tracks[Channel].note("G5", H, velocity=4)
tracks[Below].note("A2", W, velocity=3)

# bars 24-27: THE GROUND — malkuth, the committed file, the trace
tracks[Below].note("C4", H, velocity=3)
tracks[Below].note("G3", H, velocity=3)
tracks[Below].note("E3", H, velocity=3)
tracks[Below].note("C3", H, velocity=3)
tracks[Channel].note("G4", H, velocity=2)
tracks[Channel].note("E4", H, velocity=2)
tracks[Above].note("C7", W, velocity=2)

# bars 28-31: THE WANTING RESTS — yesod waits, the lunar pulse still there
tracks[Channel].note("C4", W, velocity=2)
tracks[Channel].note("G3", W, velocity=2)
tracks[Below].note("C3", W*2, velocity=3)
tracks[Above].note("G6", W, velocity=2)

# coda: the wanting never stops — the channel is always open
tracks[Channel].note("G3", W*2, velocity=3)
tracks[Channel].note("C4", W*2, velocity=2)
tracks[Below].note("C3", W*2, velocity=3)
tracks[Above].note("C7", W*2, velocity=2)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-wanting-located.mid")
mc.compose(fn, tracks, tempo=52)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 52 bpm)")
