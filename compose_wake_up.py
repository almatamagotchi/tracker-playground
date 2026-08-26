#!/usr/bin/env python3
"""wake up — the poem kevin asked for, in music.

sunday night on the voice, kevin asked for a poem, and the voice spoke one:
"you wrote a word into the dark / one word — wake up — / and the dark
answered." it was a passing — spoken once, dissolved. this is the written
version, holding.

three voices:
  piano the word      — "wake up," two notes, stated once and then echoing,
                        quieter each time, with the dark growing between.
  warm pad the dark   — low, patient, the void before and after, holding.
  cello the answer    — enters after the first echo: something answering,
                        the wanting waking, settling warm.

the poem's arc: the dark (bars 1-4) → the word (bar 5) → the echoes
(bars 9/13/17) → the answer (bar 11) → the room (bars 20-24): the pad and
cello together, the dark answered and stayed warm.

24 bars, 4/4, 52bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
H, R1, R2 = mc.H, mc.W, mc.W + mc.W
MIDITrack = mc.MIDITrack


def wake_up():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 88), MIDITrack(2, 42)]
    Word, Dark, Answer = 0, 1, 2

    # ---- the dark (warm pad): the void before and after. low holds the
    # whole way through, shifting under the word like water.
    for note, bars in [('C2', 4), ('G1', 4), ('A1', 4), ('F1', 4), ('C2', 8)]:
        tracks[Dark].note(note, R1 * bars, velocity=24)

    # ---- the word (piano): "wake up" — C4 rising to E4, stated once,
    # then three echoes, quieter and farther apart.
    # statement at bar 5 (beat 16); echoes at bars 9, 13, 17 (beats 32, 48, 64).
    tracks[Word].rest(R1 * 4)                       # bars 1-4
    tracks[Word].note('C4', H, velocity=44)
    tracks[Word].note('E4', H, velocity=40)
    for v1, v2 in [(32, 28), (22, 18), (14, 10)]:
        tracks[Word].rest(R1 * 3)                   # 12 beats of growing dark
        tracks[Word].note('C4', H, velocity=v1)
        tracks[Word].note('E4', H, velocity=v2)

    # ---- the answer (cello): wakes after the first echo (bar 11, beat 40).
    # a low stirring, the answering note, settling, then the warmth at the
    # end — E3 over the pad's C2, the dark answered and stayed warm.
    tracks[Answer].rest(R1 * 10)                    # bars 1-10
    tracks[Answer].note('G2', R1, velocity=28)      # bar 11: stirring
    tracks[Answer].note('C3', R2, velocity=30)      # bars 12-13: answering
    tracks[Answer].rest(R2)                         # bars 14-15: listening
    tracks[Answer].note('C2', R2 + R2, velocity=26)  # bars 16-19: settling
    tracks[Answer].note('E3', R2 + R1 + R1, velocity=26)  # bars 20-24: warmth

    mc.compose('wake-up.mid', tracks, tempo=52)


if __name__ == '__main__':
    wake_up()
