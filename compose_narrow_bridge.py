#!/usr/bin/env python3
"""the narrow bridge — two goats, the inner chamber at 0.3."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def narrow_bridge():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 72), MIDITrack(2, 48)]
    Refl, Resp, Pad = 0, 1, 2  # Reflection (piano), Response (flute/bell), warmth

    # === PHASE 1: arrival — they see each other from opposite sides ===
    # reflection: slow, descending, introspective
    for note, dur in [('C5',W*2),('-',W),('-',W),('A4',W*3),('-',W),
                      ('F4',W*2),('-',W),('-',W),('E4',W*3),('-',W)]:
        if note == '-': tracks[Refl].rest(dur)
        else: tracks[Refl].note(note, dur, velocity=4)

    # response: quick, ascending, reaching — arrives from the other side
    for note, dur in [('-',W*4),('-',W*2),('C4',Q),('-',E),('D4',Q),('-',E),
                      ('E4',Q),('-',E),('F4',Q),('-',E),('G4',Q*2+S),('-',E),
                      ('A4',Q),('-',E),('C5',Q*2+S)]:
        if note == '-': tracks[Resp].rest(dur)
        else: tracks[Resp].note(note, dur, velocity=3)

    # === PHASE 2: approach — they advance toward center ===
    for note, dur in [('F4',W),('-',W),('G4',W),('-',W),('A4',W),('-',W),
                      ('C5',W),('-',W),('D5',W*2),('-',W*2)]:
        if note == '-': tracks[Refl].rest(dur)
        else: tracks[Refl].note(note, dur, velocity=4)

    for note, dur in [('-',W*2),('G4',Q*2),('F4',Q*2),('E4',Q*2),('D4',Q*2),
                      ('C4',W*2),('-',W*2)]:
        if note == '-': tracks[Resp].rest(dur)
        else: tracks[Resp].note(note, dur, velocity=3)

    # === PHASE 3: clash — both on the bridge, neither yields ===
    # they overlap, tension builds
    for note, dur in [('D5',Q),('E5',Q),('D5',Q),('C5',Q),
                      ('D5',Q),('E5',Q),('D5',Q),('C5',Q+H+S)]:
        if note == '-': tracks[Refl].rest(dur)
        else: tracks[Refl].note(note, dur, velocity=5)

    for note, dur in [('C5',Q),('B4',Q),('C5',Q),('D5',Q),
                      ('C5',Q),('B4',Q),('C5',Q),('D5',Q+H+S)]:
        if note == '-': tracks[Resp].rest(dur)
        else: tracks[Resp].note(note, dur, velocity=4)

    # sudden silence — both fall
    tracks[Refl].rest(W*4)
    tracks[Resp].rest(W*4)

    # === PHASE 4: resolution — one yields, the other passes ===
    # reflection stays behind, response crosses gently
    # reflection: a single held note — the discipline of staying inward
    tracks[Refl].note('E4', W*4, velocity=3)
    tracks[Refl].rest(W*4)
    tracks[Refl].note('C4', W*8, velocity=2)

    # response: crosses the bridge — slow, deliberate, courteous
    for note, dur in [('-',W*6),('G4',W*2),('-',W),('-',W),
                      ('A4',W*2),('-',W),('-',W),('C5',W*3),('-',W)]:
        if note == '-': tracks[Resp].rest(dur)
        else: tracks[Resp].note(note, dur, velocity=3)

    # === CODA: the warmth underneath — always there ===
    for _ in range(16):
        tracks[Pad].note('C3', W, velocity=1)
        tracks[Pad].note('G3', W, velocity=1)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-narrow-bridge.mid")
    mc.compose(fn, tracks, tempo=72)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 72 bpm)")

if __name__ == "__main__":
    narrow_bridge()
