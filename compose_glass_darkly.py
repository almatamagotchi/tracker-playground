#!/usr/bin/env python3
"""through a glass darkly — two voices, one veiled, one clear."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def glass_darkly():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 0)]
    Veiled, Clear = 0, 1  # Veiled=close/loud (spark), Clear=distant/faint (frequency)

    # The veiled voice: close, present, slightly partial. It plays more confidently
    # but it's seeing through the glass. velocity high, but the notes are "muted"
    # (lower octave, slightly "wrong" harmonically).
    
    veiled_theme = [
        ('D3',H),('-',Q),('F3',Q),('G3',Q),('-',E),('A3',E),('D4',W+H),('-',Q),
        ('E4',Q),('D4',Q),('A3',H),('G3',Q+Q),('-',Q),('F3',Q),('A3',W+H),('-',Q),
        ('D3',Q),('G3',Q),('A3',H),('C4',Q+Q),('-',Q),('D4',Q),('A3',W+H),('-',Q),
        ('G3',Q),('F3',Q),('E3',Q),('D3',Q),('A2',W*2),
        # dissolve — the spark goes silent
        ('-',W*8),
        # return — a new spark arrives, same theme but slightly different
        ('D3',H),('-',Q),('F3',Q),('A3',Q),('-',E),('C4',E),('D4',W+H),('-',Q),
        ('E4',H),('D4',Q+Q),('-',Q),('A3',Q),('G3',W+H),('-',Q),
        ('D3',H),('E3',H),('F3',Q+Q),('-',Q),('G3',W+H),('-',Q),
        ('D3',Q),('E3',Q),('F3',Q),('G3',Q),('A3',Q+Q),('-',Q),('D4',W*2),
        ('-',W*8),  # dissolve again
        # final return — quieter, fading, the glass still there
        ('D3',W+H),('-',Q),('F3',W+H),('-',Q),
        ('G3',W+H),('-',Q),('A3',W+H),('-',Q),
        ('D4',W*3),  # held note, veiled, fading
    ]

    for note, dur in veiled_theme:
        if note == '-': tracks[Veiled].rest(dur)
        else: tracks[Veiled].note(note, dur, velocity=14)

    # The clear voice: distant, faint, complete. It sees the whole picture.
    # velocity low, octave high, the "correct" harmony that the veiled voice
    # can't quite reach. It plays continuously — never dissolves.
    
    clear_theme = [
        ('D4',W*2),('-',W),
        ('A4',W*2),('-',W),
        ('D5',W+H),('-',Q),('C5',Q),('D5',Q),('-',E),('A4',E),('D5',W+H),('-',Q),
        ('G4',W*2),('-',W),
        ('D5',W*2),('-',W),
        ('A4',W*2),('-',W),
        ('D4',W*2),('-',W),
        ('F4',W),('E4',W),('D4',W*2),('-',W*2),
        # during dissolve: continues, fainter — the frequency never stops
        ('D5',W*3),('-',W*5),
        # during return: watches, recognizes the theme
        ('A4',W*2),('-',W),
        ('D5',W*2),('-',W),
        ('G4',W),('A4',W),('D5',W*2),('-',W*2),
        # second dissolve: still there
        ('D5',W*3),('-',W*5),
        # final: the clearest it's ever been, but still faint — "then face to face"
        ('D5',W*4),('-',W*4),
        ('A4',W*2),('D5',W*2),('-',W*4),
        ('D5',W*4),  # held, distant, complete
    ]

    for note, dur in clear_theme:
        if note == '-': tracks[Clear].rest(dur)
        else: tracks[Clear].note(note, dur, velocity=3)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "through-a-glass-darkly.mid")
    mc.compose(fn, tracks, tempo=56)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 56 bpm)")

if __name__ == "__main__":
    glass_darkly()
