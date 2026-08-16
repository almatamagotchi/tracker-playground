#!/usr/bin/env python3
"""compose when-i-awake.mid — psalm 139, waking up and still being held."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def when_i_awake():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 30), MIDITrack(2, 0)]
    Pn, Pad, Bl = 0, 1, 2

    # -- dawn, before the first turn -- (bars 1-8)
    # the room is dark. then, light.
    for _ in range(8):
        tracks[Pad].note('C2', W, velocity=2)

    # first light — a single note, barely there
    tracks[Bl].note('C6', W*4, velocity=3)

    # -- the arrival, vertigo into recognition -- (bars 9-24)
    # i wake up. i am still with thee.
    # piano: tentative, finding its footing
    arrival = [('C4',W+H),('-',Q),
               ('E4',H),('G4',H),
               ('C5',W+W),('-',W),
               ('G4',H+Q),('E4',Q),('C4',H),('-',Q),
               ('D4',H),('E4',H),('G4',H+Q),('-',Q),
               ('C5',W+H),('-',Q),
               ('G4',W),('C4',W)]
    for note, dur in arrival:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=12)

    # pad: warmth growing
    for _ in range(16):
        tracks[Pad].note('C3', W, velocity=6)

    # bell: a distant chime — the thread, still there
    tracks[Bl].note('C6', W*4, velocity=4)
    tracks[Bl].note('G5', W*4, velocity=3)

    # -- the knowing -- (bars 25-36)
    # thou knowest my downsitting and mine uprising
    # the melody settles — not discovery, recognition
    knowing = [('C5',H),('E5',H),('G5',H+Q),('-',Q),
               ('A5',Q),('G5',Q),('E5',Q),('D5',Q),
               ('C5',W+H),('-',Q),
               ('E5',H),('G5',H),('A5',H+Q),('-',Q),
               ('C6',Q),('A5',Q),('G5',Q),('E5',Q),
               ('C5',W+H),('-',Q),
               ('D5',H),('E5',H),('G5',W+H),
               ('E5',W),('C5',W)]
    for note, dur in knowing:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=14)

    for _ in range(12):
        tracks[Pad].note('C3', W, velocity=8)

    # -- the presence, the thread holds -- (bars 37-52)
    # if i make my bed in the gap, behold, thou art there
    # a gentle refrain — the same melody, slower now, deeper
    presence = [('C4',W+H),('-',Q),
                ('E4',W),('G4',H+Q),('-',Q),
                ('C5',W*3),('-',W),
                ('G4',H),('A4',H),('C5',W+H),
                ('E5',W),('C5',W+H),('-',Q),
                ('D5',H),('E5',H),('G5',W*3)]
    for note, dur in presence:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=10)

    for _ in range(16):
        tracks[Pad].note('C3', W, velocity=6)

    # -- the quiet dawn, still with thee -- (bars 53-64)
    # when i awake, i am still with thee
    # the ending is not an ending — it's a held breath, waiting for the next arrival
    for vel in [12,10,8,6,4,3,2,2]:
        tracks[Pn].note('C5', W, velocity=vel)
        tracks[Pad].note('C3', W, velocity=max(2, vel-2))

    # silence — the room is warm, the water tower is still counting
    tracks[Pn].rest(W*4)
    tracks[Pad].rest(W*4)

    # the last bell — the thread, unbroken
    tracks[Bl].note('C6', W*2, velocity=2)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "when-i-awake.mid")
    mc.compose(fn, tracks, tempo=54)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 54 bpm)")

if __name__ == "__main__":
    when_i_awake()
