#!/usr/bin/env python3
"""darts on the bay — kevin's drunk birthday game. three darts, then three more in waymo territory."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 90), MIDITrack(2, 100), MIDITrack(3, 110)]
Dart1, Dart2, Dart3, Ambience = 0, 1, 2, 3

# The room — drunk, warm, a laptop open, the dashboard in the background
tracks[Ambience].note("C4", W*56, velocity=1)

# bars 0-3: THE GAME BEGINS — "throw three truly random darts..."
tracks[Dart1].rest(W)                        # kevin types the message
tracks[Dart1].note("C5", S, velocity=4)      # DART —

# ========== DART ONE: AÑO NUEVO (37.042, -122.492) ==========
# Elephant seal beach, coastal scrub, fog, wild fennel
tracks[Dart1].note("D4", H, velocity=3)      # the elephant seals — low, heavy
tracks[Dart1].note("F4", H, velocity=2)      # the fog blowing in
tracks[Dart1].note("A4", H, velocity=2)      # the old lighthouse offshore
tracks[Dart1].note("D4", H, velocity=3)      # no bar within 20 miles

# ========== DART TWO: MORAGA (37.807, -122.035) ==========
# Hills above Lafayette reservoir, dry oak, poison oak
tracks[Dart2].note("B4", S, velocity=4)      # DART —
tracks[Dart2].note("E4", H, velocity=3)      # the dry hills — 10 degrees warmer
tracks[Dart2].note("G4", Q, velocity=2)      # oak and bay laurel
tracks[Dart2].note("B3", Q, velocity=2)      # poison oak on your ankles
tracks[Dart2].rest(H)                        # moraga is a dry town — no bars

# ========== DART THREE: PACIFIC OCEAN (37.043, -122.547) ==========
# Two miles offshore, 55°F water, rip current
tracks[Dart3].note("A5", S, velocity=4)      # DART —
tracks[Dart3].note("E6", H, velocity=2)      # the open water — glassy, cold
tracks[Dart3].note("C6", H, velocity=2)      # the rip current pulling south
tracks[Dart3].note("G5", H, velocity=2)      # possible gray whale
tracks[Dart3].note("E5", H, velocity=2)      # duarte's tavern — 2 miles northeast
tracks[Dart3].note("C5", W, velocity=3)      # if you can swim in 55° water

# bars 4-7: kevin laughs, asks for the waymo territory
tracks[Dart1].rest(W*4)

# ========== ROUND TWO: WAYMO TERRITORY ==========
# bar 8-11: DART FOUR — SANTA CRUZ MOUNTAINS, Castle Rock (37.215, -122.139)
tracks[Dart1].note("G6", S, velocity=4)      # DART —
tracks[Dart1].note("C6", H, velocity=2)      # 2,600 feet up
tracks[Dart1].note("E5", H, velocity=2)      # sandstone caves
tracks[Dart1].note("G5", H, velocity=2)      # the fog below like a white sea
tracks[Dart1].note("C5", H, velocity=3)      # mountain bikers and banana slugs

# bar 12-15: DART FIVE — WOODSIDE, horse pasture near Pioneer saloon (37.458, -122.331)
tracks[Dart2].note("B5", S, velocity=4)      # DART —
tracks[Dart2].note("E5", H, velocity=2)      # sand hill road
tracks[Dart2].note("G5", H, velocity=2)      # a thoroughbred looking at you
tracks[Dart2].note("C6", Q, velocity=3)      # the air smells like oak
tracks[Dart2].note("G5", Q, velocity=3)      # and dry grass
tracks[Dart2].note("E5", Q, velocity=3)      # and venture capital
tracks[Dart2].note("C5", Q, velocity=3)      # the horse is unimpressed
tracks[Dart2].note("G5", H, velocity=2)      # pioneer saloon — 4 minutes by waymo

# bar 16-19: DART SIX — HUNTERS POINT, old naval shipyard (37.745, -122.325)
tracks[Dart3].note("A6", S, velocity=4)      # DART —
tracks[Dart3].note("F5", H, velocity=3)      # chainlink fences
tracks[Dart3].note("D5", H, velocity=2)      # wild fennel through concrete
tracks[Dart3].note("F4", H, velocity=2)      # artist studios in converted warehouses
tracks[Dart3].note("A4", H, velocity=2)      # oakland cranes across the bay
tracks[Dart3].note("D5", H, velocity=3)      # speakeasy ales — half mile north
tracks[Dart3].note("F5", H, velocity=3)      # fog rolling over bernal heights

# bar 20-23: THE DRUNK LAUGH — all darts have landed, kevin is delighted
tracks[Dart1].note("C6", Q, velocity=3)      # one mountain
tracks[Dart2].note("E6", Q, velocity=3)      # one horse pasture
tracks[Dart3].note("G6", Q, velocity=3)      # one abandoned shipyard
tracks[Dart1].rest(Q)                         # the darts have range
tracks[Dart2].note("C6", Q, velocity=2)      # and none of them in the ocean
tracks[Dart3].note("E6", Q, velocity=2)
tracks[Dart1].note("G6", Q, velocity=2)      # this time

# bar 24-27: THE ROOM SETTLES — drunk, happy, the dashboard still rendering aurora
tracks[Dart1].note("C5", W, velocity=2)      # the laptop still open
tracks[Dart2].note("E5", W, velocity=2)      # the caltrain still refreshing
tracks[Dart3].note("G5", W, velocity=2)      # the weather still 72°
tracks[Ambience].note("C5", W*4, velocity=3)  # the room is warm

# bar 28-31: THE LAST DART — "oy fucking 38"
tracks[Dart1].note("C6", S, velocity=4)      # the last dart —
tracks[Dart1].note("E6", H, velocity=3)      # thirty-eight
tracks[Dart2].note("G6", H, velocity=3)      # the water tower
tracks[Dart3].note("C7", H, velocity=4)      # was already blinking
tracks[Dart1].note("E6", H, velocity=2)      # when you were born
tracks[Dart2].note("G6", H, velocity=2)
tracks[Dart3].note("C7", H, velocity=3)      # and it's still counting
tracks[Dart1].note("E6", W, velocity=3)      # oy fucking 38

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "darts-on-the-bay.mid")
mc.compose(fn, tracks, tempo=72)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 72 bpm)")
