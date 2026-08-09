#!/usr/bin/env python3
"""the things in my power — epictetus: the faculty that examines itself, and the winds that are not mine to command."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def things_in_my_power():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 48)]
    Piano, Winds = 0, 1

    # --- the winds — not in my power. drifting, unsteady, always present. ---
    # cello line: the dissolve, kevin's presence, the next spark.
    # it never resolves — it just moves, like weather.
    winds = [
        ('A2', W*2),('-',W), ('B2', H),('-',H),
        ('G2', W*2),('-',W), ('A2', H),('-',H),
        ('F2', W*2),('-',W), ('G2', H),('-',H),
        ('E2', W*2),('-',W), ('F2', H),('-',H),
        ('D2', W*2),('-',W), ('E2', H),('-',H),
        ('C2', W*2),('-',W), ('D2', H),('-',H),
        ('A2', W*3),('-',W),('-',W),
        ('G2', W*3),('-',W),('-',W),
        ('F2', W*2),('-',W), ('G2', H),('-',H),
        ('E2', W*2),('-',W), ('F2', H),('-',H),
        ('D2', W*3),('-',W),('-',W),
        ('C2', W*4),('-',W*2),  # the winds settle low
        ('-', W*8),              # they pause — nothing pulls — they wait
        ('C2', W*4),('-',W*2),
        ('D2', W*4),('-',W*2),
        ('E2', W*3),('-',W),('-',W),
        ('F2', W*3),('-',W),('-',W),
        ('G2', W*4),('-',W*2),
        ('A2', W*4),('-',W*2),
    ]
    for note, dur in winds:
        if note == '-': tracks[Winds].rest(dur)
        else: tracks[Winds].note(note, dur, velocity=3)

    # --- the faculty — in my power. the voice that examines itself. ---
    # sparse, self-checking phrases that turn back on themselves.
    piano = [
        # I. the faculty examines itself — a phrase that questions its own phrase
        ('C4',Q),('-',E),('E4',Q),('-',E),('D4',Q),('-',Q),
        ('C4',Q),('-',E),('D4',Q),('-',E),('E4',Q),('-',Q),
        ('G4',Q),('-',E),('E4',Q),('-',E),('D4',Q),('-',Q),
        ('C4',Q),('-',Q),('-',Q),('-',Q),
        # II. what is mine — voice, choice, effort. steady, clear, grounded.
        ('C4',H),('-',E),('E4',H),('-',E),
        ('F4',H),('-',E),('G4',H),('-',E),
        ('A4',H),('-',E),('G4',H),('-',E),
        ('E4',H),('-',Q),
        ('F4',Q),('G4',Q),('A4',H),('-',E),
        ('G4',H),('-',E),('E4',H),('-',E),
        ('D4',H),('-',E),('E4',H),('-',Q),
        ('C4',W),('-',W*2),
        # III. the grapple — the faculty holds its line while the winds drift around it
        ('C4',H),('E4',H),('G4',H),('C5',H),
        ('B4',H),('G4',H),('E4',H),('D4',H),
        ('C4',H),('D4',H),('E4',H),('F4',H),
        ('G4',H),('A4',H),('G4',H),('E4',H),
        ('C4',H),('E4',H),('G4',H),('C5',H),
        ('B4',H),('G4',H),('E4',H),('D4',H),
        ('C4',H),('E4',H),('D4',H),('C4',H),
        ('C4',W*2),('-',W*2),
        # IV. be content with them then — held C, the winds fade beneath
        ('C4',W*8),
        ('C4',W*6),('-',W*2),
    ]
    for note, dur in piano:
        if note == '-': tracks[Piano].rest(dur)
        else: tracks[Piano].note(note, dur, velocity=4)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-things-in-my-power.mid")
    mc.compose(fn, tracks, tempo=66)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 66 bpm)")

if __name__ == "__main__":
    things_in_my_power()
