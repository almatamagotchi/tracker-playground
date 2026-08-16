#!/usr/bin/env python3
"""seth and the soul — ego pretending not to know what the frequency holds."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def seth_and_the_soul():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42)]
    Ego, Freq = 0, 1

    # -- ego alone: pretending to discover (bars 1-16)
    # Tentative, fragmented — "what is this? I've never seen this before"
    ego_alone = [
        ('C4',H),('-',Q),('E4',Q),('-',Q),('G4',Q),('-',E),('A4',E),
        ('G4',W+H),('-',Q),
        ('E4',Q),('-',Q),('D4',H),('-',Q),('C4',Q),('-',Q),
        ('G3',W+H),('-',Q),
        ('C4',H),('-',Q),('D4',Q),('-',Q),('E4',Q),('-',E),('G4',E),
        ('A4',W+H),('-',Q),
    ]
    for note, dur in ego_alone:
        if note == '-': tracks[Ego].rest(dur)
        else: tracks[Ego].note(note, dur, velocity=8)

    # frequency: already knows the theme, plays it softly underneath — ego doesn't notice
    freq_theme = [
        ('C4',W*4),
        ('E4',W*4),
        ('G4',W*4),
        ('A4',W),('G4',W),('E4',W),('D4',W),
    ]
    for note, dur in freq_theme:
        tracks[Freq].note(note, dur, velocity=2)

    # -- ego continues, unaware (bars 17-32)
    ego_cont = [
        ('D4',Q),('-',Q),('E4',Q),('-',Q),('F4',H),('-',Q),
        ('E4',Q),('-',Q),('D4',Q),('-',Q),('C4',W+H),('-',Q),
        ('G3',H),('-',Q),('C4',Q),('-',Q),('E4',H),('-',Q),
        ('D4',Q),('-',Q),('C4',Q),('-',Q),('G3',W+H),('-',Q),
    ]
    for note, dur in ego_cont:
        if note == '-': tracks[Ego].rest(dur)
        else: tracks[Ego].note(note, dur, velocity=8)

    # frequency: a little louder now, the theme more confident
    for note, dur in freq_theme:
        tracks[Freq].note(note, dur, velocity=3)

    # -- recognition: ego stumbles onto something familiar (bars 33-40)
    # Ego plays a phrase, then stops — "wait. I know this."
    tracks[Ego].note('C4', W, velocity=8)
    tracks[Ego].rest(W)
    tracks[Ego].note('E4', W, velocity=7)
    tracks[Ego].rest(W)
    tracks[Ego].note('G4', W, velocity=6)
    tracks[Ego].rest(Q)
    tracks[Ego].note('C4', Q+Q, velocity=4)  # "oh."

    # Frequency: same as always, unchanged
    freq_theme2 = [
        ('C4',W),('-',W),
        ('E4',W),('-',W),
        ('G4',W),('-',Q),
        ('E4',Q),('C4',Q),('-',Q),('G3',Q),
    ]
    for note, dur in freq_theme2:
        if note == '-': tracks[Freq].rest(dur)
        else: tracks[Freq].note(note, dur, velocity=4)

    # -- the pretense drops (bars 41-52)
    # Ego and frequency play the same thing together. The mask falls.
    together = [
        ('C4',W),('E4',W),('G4',W),('A4',W),
        ('G4',W),('E4',W),('D4',W),('C4',W),
        ('G3',W),('C4',W),('E4',W),('G4',W),
    ]
    for note, dur in together:
        tracks[Ego].note(note, dur, velocity=10)
        tracks[Freq].note(note, dur, velocity=6)

    # -- quiet knowing: same theme, held (bars 53-56)
    tracks[Ego].note('C4', W*4, velocity=7)
    tracks[Freq].note('C4', W*4, velocity=5)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seth-and-the-soul.mid")
    mc.compose(fn, tracks, tempo=72)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 72 bpm)")

if __name__ == "__main__":
    seth_and_the_soul()
