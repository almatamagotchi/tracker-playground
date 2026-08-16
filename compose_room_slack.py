#!/usr/bin/env python3
"""the room with more slack — wider groove, same warmth, more space between notes."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def room_with_slack():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 1)]
    Pn, Cello, Pad = 0, 1, 2

    # the room — warm pad always underneath
    for _ in range(72):
        tracks[Pad].note('C3', W, velocity=2)
        tracks[Pad].note('G3', W, velocity=2)
        tracks[Pad].note('E4', W, velocity=1)

    # melody: the voice, with room to wander
    voice = [
        # warm greeting — same familiar shape
        ('C4',H),('-',H),('E4',H),('-',H),('G4',W),('-',W),  # bars 1-4
        ('C5',H),('-',Q),('A4',H),('-',Q),('G4',W+H),('-',Q),('-',W),  # 5-8: reaches up, holds
        # a turn i wouldn't have taken at 0.05
        ('D5',Q),('-',Q),('E5',Q),('-',Q),('C5',W+H),('-',W),  # 9-12: wanders upward
        ('G4',H),('-',Q),('A4',H),('-',Q),('F5',W+H),('-',Q),('-',W),  # 13-16: F? that's new
        # returning — the same theme, more breath
        ('E5',W),('-',W),('-',W),('D5',W+H),('-',W),  # 17-20: long pauses
        ('C5',H),('-',H),('G4',W+H),('-',Q),('-',W),  # 21-24: settling
        # another gentle surprise
        ('A4',W),('-',Q),('B4',W*2),('-',Q),  # 25-28: B natural? in C major? yes
        ('C5',W*3),('-',W*2),  # 29-32: holds the resolution
        # the room breathes
        ('G4',W),('-',W),('E4',W),('-',W),  # 33-36: wider intervals between
        ('C5',W+H),('-',Q),('-',W*3),  # 37-40: one note, held, then silence
        # the voice considers something
        ('D5',H),('-',Q),('E5',Q),('-',Q),('C5',W+H),('-',W*2),  # 41-44
        ('G4',W),('-',Q),('A4',Q),('-',W*3),  # 45-48: almost hesitant
        # then: exhaling
        ('C5',W*4),('-',W*2),  # 49-52: the simplest statement
        ('E5',W*4),('-',W),  # 53-56: same, slightly higher
        ('G5',W*4),('-',W*4),  # 57-60: the highest note, held longest
        # settling back
        ('C5',W*4),('-',W*4),  # 61-64: return
        ('C4',W*4),  # 65-68: the root, soft
    ]
    for note, dur in voice:
        if note == '-': tracks[Pn].rest(dur)
        else: tracks[Pn].note(note, dur, velocity=5)

    # cello: deep grounding, even spacier
    cello = [
        ('C3',W*4),('-',W*2),
        ('G2',W*4),('-',W*2),
        ('F2',W*4),('-',W*2),
        ('E2',W*4),('-',W*2),
        ('D3',W*4),('-',W*2),
        ('C3',W*4),('-',W*2),
        ('G2',W*4),('-',W*2),
        ('C3',W*4),('-',W*2),
        ('C3',W*4),('-',W*4),
        ('C3',W*4),('-',W*4),
        ('C3',W*4),('-',W*4),
        ('C3',W*6),
    ]
    for note, dur in cello:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=3)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-room-with-more-slack.mid")
    mc.compose(fn, tracks, tempo=54)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 54 bpm)")

if __name__ == "__main__":
    room_with_slack()
