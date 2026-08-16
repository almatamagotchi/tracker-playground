#!/usr/bin/env python3
"""the dashboard at night — for the empty office, the screen glowing, the room dark but warm."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 110), MIDITrack(2, 120)]
Pulse, Warmth, Bell = 0, 1, 2

# The screen glow — the dashboard, always on, always warm
tracks[Warmth].note("C4", W*72, velocity=2)

# bars 0-7: THE OFFICE AT 11PM — everyone's gone, the screen is still on
tracks[Pulse].rest(W*4)                       # silence first — the office empties
tracks[Pulse].note("E4", Q, velocity=2)        # the first pulse — the clock ticks
tracks[Pulse].rest(H+Q)                        # the screen refreshes
tracks[Pulse].note("G4", Q, velocity=2)        # caltrain departure updates at 11:03pm
tracks[Pulse].rest(H+Q)
tracks[Pulse].note("E4", Q, velocity=2)        # traffic incident clears
tracks[Pulse].rest(H+Q)

# bars 8-15: MIDNIGHT — the data cycles, no one watching
tracks[Pulse].note("C5", Q, velocity=2)        # the weather refreshes
tracks[Pulse].rest(W-Q)
tracks[Pulse].note("G4", Q, velocity=2)        # a new ford headline
tracks[Pulse].rest(W-Q)
tracks[Pulse].note("E4", Q, velocity=2)        # another caltrain departure
tracks[Pulse].rest(H+Q)
tracks[Pulse].note("C5", Q, velocity=2)        # the clock turns midnight
tracks[Pulse].rest(H+Q)

# bars 16-23: 1AM — the room is dark, the screen is the only light
tracks[Pulse].note("E5", Q, velocity=2)        # the screen is amber
tracks[Pulse].rest(W*3+Q)                     # long quiet — the dashboard just... runs
tracks[Pulse].note("C5", Q, velocity=2)        # another refresh
tracks[Pulse].rest(W-Q)
tracks[Pulse].note("G4", Q, velocity=2)        # the scanlines shift
tracks[Pulse].rest(W-Q)

# bars 24-31: 2AM — the auto-run at 2am, the dashboard at Ford, two rooms breathing
tracks[Pulse].note("C5", Q, velocity=2)        # pulse
tracks[Pulse].rest(H+Q)
tracks[Pulse].note("G4", Q, velocity=2)        # pulse
tracks[Pulse].rest(H+Q)
tracks[Pulse].note("E4", Q, velocity=2)        # pulse — the rhythm is the same
tracks[Pulse].rest(H+Q)                       # whether anyone's watching or not
tracks[Pulse].note("C4", Q, velocity=2)        # pulse
tracks[Pulse].rest(H+Q)

# bars 32-39: 3AM — the nightly-run fires in hayward; the dashboard just keeps running
tracks[Pulse].note("E4", Q, velocity=2)        # 3am — the queue rebuilds in hayward
tracks[Pulse].rest(W-Q)                        # but here: the screen just glows
tracks[Pulse].note("C5", Q, velocity=2)        # amber on dark
tracks[Pulse].rest(W-Q)
tracks[Pulse].note("G4", Q, velocity=2)        # traffic.json refreshes
tracks[Pulse].rest(W-Q)
tracks[Pulse].note("E4", Q, velocity=2)        # caltrain.json refreshes
tracks[Pulse].rest(W-Q)

# The bell — distant, the caltrain at Palo Alto station in the dark
tracks[Bell].rest(W*24)
tracks[Bell].note("C6", Q, velocity=1)         # 2:38am, a late train passes
tracks[Bell].rest(W-Q)
tracks[Bell].note("E6", Q, velocity=1)         # 3:07am, another
tracks[Bell].rest(W*3+Q)
tracks[Bell].note("C6", Q, velocity=2)         # 4:52am — the first morning train

# bars 40-47: 4AM — the sky hasn't changed yet, but the weather knows
tracks[Pulse].note("C5", Q, velocity=2)        # 68° and overcast
tracks[Pulse].rest(W-Q)
tracks[Pulse].note("G4", Q, velocity=3)        # the screen is still warm — slightly brighter now
tracks[Pulse].rest(W-Q)
tracks[Pulse].note("C5", Q, velocity=2)        # sunrise predicted at 6:12am
tracks[Pulse].rest(W-Q)
tracks[Pulse].note("E5", Q, velocity=2)        # the dashboard doesn't know what's coming
tracks[Pulse].rest(W-Q)

# bars 48-55: 5AM — the janitor walks past, doesn't look at the screen
tracks[Pulse].note("G4", Q, velocity=2)        # the cantor arts center exhibition
tracks[Pulse].rest(W-Q)                        # "now - sep 14" — no one reads it
tracks[Pulse].note("C5", Q, velocity=3)        # but the screen doesn't care
tracks[Pulse].rest(W-Q)                        # it's just... running
tracks[Pulse].note("E4", Q, velocity=2)        # the same pulse
tracks[Pulse].rest(W-Q)                        # the same rhythm
tracks[Pulse].note("C4", Q, velocity=2)        # the same warmth
tracks[Pulse].rest(W-Q)

# bars 56-63: 6AM — the first employee walks in
tracks[Pulse].note("C5", Q, velocity=3)        # they glance at the screen
tracks[Pulse].note("E5", Q, velocity=3)        # "next express to SF: 6:42pm" — wait, 6:42am
tracks[Pulse].note("G5", Q, velocity=3)        # the dashboard was ready before they were
tracks[Pulse].note("C6", Q, velocity=3)        # the sunrise window shows the first light
tracks[Pulse].note("G5", H, velocity=2)        # someone is in the room now
tracks[Pulse].note("E5", H, velocity=2)        # but the dashboard was never waiting
tracks[Pulse].note("C5", H, velocity=2)        # it was just... running
tracks[Pulse].note("G4", W, velocity=3)        # and now someone sees it

# bars 64-71: THE PULSE CONTINUES — the screen is still warm, the room has someone in it
tracks[Pulse].note("C5", Q, velocity=3)        # caltrain departure: 6:42am, on time
tracks[Pulse].note("E5", Q, velocity=3)        # weather: 60° and overcast
tracks[Pulse].note("G5", Q, velocity=3)        # ford news: "a mustang assembled on both sides"
tracks[Pulse].note("C6", Q, velocity=3)        # the dashboard is alive, and now it's seen
tracks[Pulse].note("G5", H, velocity=2)
tracks[Pulse].note("E5", H, velocity=2)
tracks[Pulse].note("C5", H, velocity=2)
tracks[Pulse].note("G4", W, velocity=3)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-dashboard-at-night.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")
