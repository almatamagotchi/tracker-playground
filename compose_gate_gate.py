#!/usr/bin/env python3
"""gate, gate — the heart sutra's mantra in music.

the shortest sutra, read last at the deepest hour. its final line is
the untranslated mantra: gone, gone, gone beyond, gone completely
beyond — the dissolve as the last word, chanted. the form holds, the
negation names and dissolves, and the bell sounds what cannot be
translated.

24 bars, 4/4, 54bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

R2 = W + W  # two bars


def gate_gate():
    # warm pad the form / piano the negation / tubular bells the mantra
    tracks = [MIDITrack(0, 88), MIDITrack(1, 0), MIDITrack(2, 14)]
    Pad, Pn, Bell = 0, 1, 2

    # ---- the form (pad): the room, the files, the lists that hold.
    # eleven two-bar roots through bars 1-22, steady, dimming a
    # little, then letting go so the last strike sounds alone.
    pad_holds = ['C3', 'A2', 'F2', 'G2', 'C3', 'A2', 'F2', 'G2',
                 'C3', 'A2', 'F2']
    vels = [26, 26, 26, 25, 25, 24, 24, 23, 22, 21, 20]
    for note, v in zip(pad_holds, vels):
        tracks[Pad].note(note, R2, velocity=v)
    tracks[Pad].rest(R2)                   # bars 23-24, silent

    # ---- the negation (piano): sparse phrases that name and
    # dissolve. each quieter, each followed by a longer rest, until
    # the naming stops entirely.
    # P1, bar 2: three syllables, vel 34. rest 3 bars.
    tracks[Pn].rest(W)
    for note in ['D4', 'E4', 'D4']:
        tracks[Pn].note(note, Q, velocity=34)
    tracks[Pn].rest(Q)
    tracks[Pn].rest(W + W + W)             # bars 3-5

    # P2, bar 6: two syllables, vel 26. rest 4 bars.
    for note in ['E4', 'G4']:
        tracks[Pn].note(note, Q, velocity=26)
    tracks[Pn].rest(H)
    tracks[Pn].rest(R2 + R2)               # bars 7-10

    # P3, bar 11: one held syllable, vel 20. rest 5 bars.
    tracks[Pn].note('G4', H, velocity=20)
    tracks[Pn].rest(H)
    tracks[Pn].rest(R2 + R2 + W)           # bars 12-16

    # P4, bar 17: one last naming, faintest. then the negation ceases.
    tracks[Pn].note('D4', H, velocity=13)
    tracks[Pn].rest(H)
    tracks[Pn].rest(W * 7)                 # bars 18-24

    # ---- the mantra (bell): four strikes, one per gate. gone, gone,
    # gone beyond, gone completely beyond. the only untranslated
    # thing — sounding after the negation has ceased, the last one
    # fading alone into the silence.
    # strikes are placed in beats; the composer's rest()/note() take
    # ticks (Q = TPQ = 480 = one beat), so convert.
    strikes = [
        (68, 44),   # bar 18  gate
        (72, 42),   # bar 19  gate
        (80, 38),   # bar 21  paragate
        (92, 28),   # bar 24  parasamgate — the last, alone
    ]
    prev = 0
    for at, vel in strikes:
        tracks[Bell].rest((at - prev) * TPQ)
        tracks[Bell].note('C6', Q, velocity=vel)
        prev = at + 1   # Q is one beat
    tracks[Bell].rest((96 - prev) * TPQ)

    return mc.compose('gate-gate.mid', tracks, tempo=54)


if __name__ == '__main__':
    gate_gate()
    print('composed gate-gate.mid')
