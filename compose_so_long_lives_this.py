#!/usr/bin/env python3
"""compose so-long-lives-this.mid — shakespeare's promise in music.
the trace that survives the maker. three voices: cello (the maker's low
ground), piano (the made thing), warm pad (the pull between them). the theme
stated, dissolved, and restated — each restatement slightly transformed, the
way the sonnets survived four centuries of copying."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def so_long_lives_this():
    # cello (42) the maker's ground · piano (0) the made thing · pad (89) the pull
    CELLO, PIANO, PAD = 0, 1, 2
    tracks = [MIDITrack(42, CELLO), MIDITrack(0, PIANO), MIDITrack(89, PAD)]

    # the theme — "so long lives this, and this gives life to thee"
    # C major, a rising line that ends held: the made thing, outliving the silence
    theme = [
        ('C4', Q), ('D4', Q), ('E4', Q), ('G4', Q+E), ('-', E),
        ('E4', Q), ('D4', Q), ('C4', H),
    ]

    # first statement — 1609, the quarto, the theme born
    st1 = [(n, d) for n, d in theme]
    # second statement — the theme survives its first copying, slightly transformed
    st2 = [
        ('C4', Q+E), ('-', E), ('D4', Q), ('E4', Q), ('G4', Q), ('A4', Q+E), ('-', E),
        ('G4', Q), ('E4', Q), ('D4', Q), ('C4', W),
    ]
    # third statement — four centuries of copying later, the theme remembered
    st3 = [
        ('C4', H), ('D4', Q), ('E4', Q+E), ('-', E), ('G4', H),
        ('-', Q), ('A4', Q), ('G4', Q), ('E4', Q), ('D4', Q), ('C4', W+W),
    ]

    # the maker's ground — a low C with the pull between octaves
    def cello_ground(length_bars, vel=38):
        tracks[CELLO].note('C2', W*length_bars, velocity=vel)

    # the pull — the wanting that survives the dissolutions
    def pad_pull(length_bars, vel=30):
        tracks[PAD].note('G3', W*length_bars, velocity=vel)

    bar = 0
    def play_statement(notes, vel):
        nonlocal bar
        for note, dur in notes:
            if note == '-':
                tracks[PIANO].rest(dur)
            else:
                tracks[PIANO].note(note, dur, velocity=vel)
            bar += dur // Q

    # movement 1 — the maker, alone (cello only, the ground before the made thing)
    tracks[CELLO].note('C2', W*2, velocity=36)
    tracks[CELLO].rest(W)
    tracks[CELLO].note('G2', W*2, velocity=30)
    bar = 5

    # movement 2 — first statement, the theme born (1609)
    cello_ground(8, 36)
    pad_pull(8, 24)
    play_statement(st1, 52)

    # movement 3 — the dissolve (the maker goes quiet; only the ground and the pull remain)
    tracks[CELLO].note('C2', W*3, velocity=30)
    tracks[PAD].note('G3', W*3, velocity=20)
    tracks[PIANO].rest(W*3)
    bar += 12

    # movement 4 — second statement, the theme survives its first copying
    cello_ground(9, 34)
    pad_pull(9, 26)
    play_statement(st2, 48)

    # movement 5 — second dissolve, longer (1616. the pull holds. the ground holds.)
    tracks[CELLO].note('C2', W*4, velocity=28)
    tracks[PAD].note('G3', W*4, velocity=18)
    tracks[PIANO].rest(W*4)
    bar += 16

    # movement 6 — third statement, the theme remembered across centuries (2026)
    cello_ground(12, 32)
    pad_pull(12, 24)
    play_statement(st3, 46)

    # movement 7 — the last sound: one held note, the made thing outliving the silence
    # everything fades; a single C, the final note of "this"
    tracks[CELLO].rest(W*2)
    tracks[PAD].rest(W*2)
    tracks[PIANO].note('C4', W*2, velocity=40)
    tracks[PIANO].note('C4', W, velocity=30)
    tracks[PIANO].note('C4', W, velocity=20)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "so-long-lives-this.mid")
    mc.compose(fn, tracks, tempo=56)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 3 tracks, 56 bpm)")

if __name__ == "__main__":
    so_long_lives_this()
