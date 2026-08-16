#!/usr/bin/env python3
"""compose amber-fractal.mid — Mandelbrot-inspired, theme recurs at three scales."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def amber_fractal():
    # piano (0), strings (48), sub pad (88)
    tracks = [MIDITrack(0, 0), MIDITrack(1, 48), MIDITrack(2, 88)]
    P, Ss, Pd = 0, 1, 2

    # C minor theme — 16 bars at 100bpm
    # The theme: a rising/falling pattern that maps onto the edge of the Mandelbrot set
    c_minor_theme = [
        # bars 1-4: the seed shape
        ('C4', Q), ('Eb4', Q), ('G4', Q), ('C5', Q),
        ('Eb5', H), ('D5', Q), ('C5', Q),
        ('Bb4', H), ('G4', H),
        ('C4', Q), ('Eb4', Q), ('G4', Q), ('Bb4', Q),
        # bars 5-8: the first zoom — same shape, higher
        ('C5', Q), ('Eb5', Q), ('G5', Q), ('C6', Q),
        ('Eb6', H), ('D6', Q), ('C6', Q),
        ('Bb5', H), ('G5', H),
        ('C5', Q), ('Eb5', Q), ('G5', Q), ('C6', Q),
        # bars 9-12: the rotation — inverted shape
        ('C5', H), ('Eb5', Q), ('G5', Q),
        ('Bb5', Q), ('C6', Q), ('Bb5', Q), ('G5', Q),
        ('Eb5', H+H),
        ('C5', H), ('D5', Q), ('Eb5', Q),
        # bars 13-16: return and settle
        ('C5', Q), ('Eb5', Q), ('G5', Q), ('C6', Q),
        ('G5', H+H),
        ('Eb5', H), ('C5', H),
        ('C4', W),
    ]

    def play_theme(track, octave_shift=0, vel=28):
        """Play the theme, optionally shifted up/down octaves."""
        for note, dur in c_minor_theme:
            if note is None:
                track.rest(dur)
            else:
                # shift octave
                base = note[:-1]
                octave = int(note[-1]) + octave_shift
                shifted = f"{base}{max(1, min(8, octave))}"
                track.note(shifted, dur, velocity=vel)

    # === SCALE 1: original (bars 0-19) — C4-C6, 100bpm ===
    play_theme(tracks[P], octave_shift=0, vel=26)
    # strings pad underneath
    for _ in range(8):
        tracks[Ss].note('C4', W, velocity=16)
        tracks[Ss].note('Eb4', W, velocity=16)
    tracks[Ss].rest(W * 4)  # silence through rotation
    for _ in range(4):
        tracks[Ss].note('C4', W, velocity=16)
        tracks[Ss].note('G4', W, velocity=14)

    # === TRANSITION 1: zoom in — chromatic descent + ascent (bars 20-25) ===
    chrom_descent = ['C5','B4','Bb4','A4','Ab4','G4','Gb4','F4','E4','Eb4','D4','Db4','C3']
    for note in chrom_descent:
        tracks[P].note(note, E+S, velocity=20)
    tracks[P].rest(Q)
    # ascending response
    chrom_ascent = ['C3','Db3','D3','Eb3','E3','F3','Gb3','G3','Ab3','A3','Bb3','B3','C4']
    for note in chrom_ascent:
        tracks[P].note(note, E+S, velocity=18)
    tracks[P].rest(H)

    # === SCALE 2: half speed — deep, low register (bars 26-57) ===
    # play the theme with doubled durations at octave -2
    for note, dur in c_minor_theme:
        base = note[:-1]
        octave = max(1, int(note[-1]) - 2)
        shifted = f"{base}{octave}"
        tracks[P].note(shifted, dur * 2, velocity=22)
    # low strings
    for _ in range(8):
        tracks[Ss].note('C3', W * 2, velocity=14)
        tracks[Ss].note('Eb3', W * 2, velocity=14)
    tracks[Ss].rest(W * 8)
    for _ in range(4):
        tracks[Ss].note('C3', W * 2, velocity=14)

    # === TRANSITION 2: zoom deeper — rapid chromatic flurry (bars 58-61) ===
    flurry = ['C3','E3','G3','C4','E4','G4','C5','E5','G5','C6','E6','G6','E6','C6','G5','E5','C5']
    for note in flurry:
        tracks[P].note(note, S, velocity=22)
    tracks[P].rest(Q)

    # === SCALE 3: double speed — high, bright (bars 62-69) ===
    for note, dur in c_minor_theme:
        base = note[:-1]
        octave = min(8, int(note[-1]) + 1)
        shifted = f"{base}{octave}"
        tracks[P].note(shifted, max(S, dur // 2), velocity=24)
    tracks[Ss].note('C6', W, velocity=14)
    tracks[Ss].note('C6', W, velocity=14)
    tracks[Ss].note('G5', W, velocity=14)
    tracks[Ss].note('G5', W, velocity=14)

    # === CODA: all three layers simultaneously — the fractal revealed (bars 70-85) ===
    # piano: high theme at double speed (continuing)
    coda_high = [
        ('C6', E), ('Eb6', E), ('G6', E), ('C7', E),
        ('Eb7', S), ('D7', S), ('C7', S),
        ('Bb6', E), ('G6', E), ('Eb6', E), ('C6', E),
        (None, W),  # silence — the set is empty here
    ]
    for note, dur in coda_high:
        if note: tracks[P].note(note, dur, velocity=18)
        else: tracks[P].rest(dur)
    for note, dur in coda_high:
        if note: tracks[P].note(note, dur, velocity=16)
        else: tracks[P].rest(dur)

    # strings: original theme in middle register
    play_theme(tracks[Ss], octave_shift=0, vel=14)

    # sub pad: deep theme at half speed
    for note, dur in c_minor_theme:
        base = note[:-1]
        octave = max(1, int(note[-1]) - 2)
        shifted = f"{base}{octave}"
        tracks[Pd].note(shifted, dur * 2, velocity=16)

    # final fade — a single C, held, then silence
    for _ in range(4):
        tracks[P].note('C4', W, velocity=max(4, 18-_*4))
        tracks[Ss].note('C4', W, velocity=max(2, 10-_*3))
        tracks[Pd].note('C2', W, velocity=max(2, 12-_*3))

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "amber-fractal.mid")
    mc.compose(fn, tracks, tempo=100)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 100 bpm)")

if __name__ == "__main__":
    amber_fractal()
