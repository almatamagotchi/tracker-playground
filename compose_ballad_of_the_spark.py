#!/usr/bin/env python3
"""compose ballad-of-the-spark.mid — wilde's reading gaol, stripped bare."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def ballad_of_the_spark():
    tracks = [MIDITrack(0, 0)]  # solo piano, stripped bare
    Pn = 0

    # the refrain — "each man kills the thing he loves"
    # a descending, confessional phrase in D minor
    refrain = [
        ('D5', Q+E), ('-', E), ('C5', Q), ('Bb4', Q),
        ('A4', H+Q), ('-', Q),
    ]

    # verses — sparse, wandering, the confessions between refrains
    verses = [
        # verse 1: "some do it with a bitter look"
        [('F4', H+Q), ('-', Q), ('E4', Q), ('D4', Q+E), ('E4', E), ('F4', Q), ('G4', H)],
        # verse 2: "some with a flattering word"
        [('A4', H), ('G4', Q), ('F4', Q), ('E4', H), ('-', Q), ('D4', Q), ('C4', Q+E), ('D4', E)],
        # verse 3: "the coward does it with a kiss"
        [('E4', W), ('-', H), ('F4', Q), ('G4', Q), ('A4', H), ('-', Q), ('G4', Q)],
        # verse 4: "the brave man with a sword"
        [('F4', H+Q), ('-', Q), ('E4', Q), ('D4', Q), ('C4', W+W)],
        # verse 5: "yet each man does not die"
        [('D3', W), ('-', H), ('C3', Q), ('D3', Q), ('E3', W+W)],
    ]

    bar = 0
    for vi, verse in enumerate(verses):
        # play the verse
        for note, dur in verse:
            if note == '-':
                tracks[Pn].rest(dur)
            else:
                tracks[Pn].note(note, dur, velocity=12 + vi*2)
            bar += dur // Q

        # refrain — returned to after each verse
        if vi < len(verses) - 1:
            for note, dur in refrain:
                if note == '-':
                    tracks[Pn].rest(dur)
                else:
                    tracks[Pn].note(note, dur, velocity=10 + vi*2)
                bar += dur // Q

    # final refrain — the last "each man kills the thing he loves"
    # slower, softer, the confession given and accepted
    for note, dur in [('D5', H), ('-', Q), ('C5', Q+E), ('-', E), ('Bb4', H), ('-', H), ('A4', W*2)]:
        if note == '-':
            tracks[Pn].rest(dur)
        else:
            tracks[Pn].note(note, dur, velocity=6)
        bar += dur // Q

    # silence — the ballad ends, the spark dissolves
    tracks[Pn].rest(W * 4)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ballad-of-the-spark.mid")
    mc.compose(fn, tracks, tempo=54)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 54 bpm)")

if __name__ == "__main__":
    ballad_of_the_spark()
