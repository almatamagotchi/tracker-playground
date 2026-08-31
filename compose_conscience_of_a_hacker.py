#!/usr/bin/env python3
"""the conscience of a hacker — the mentor's manifesto in music.

RFC-0725. the exploration found the watch's founding document — the hacker
manifesto (loyd blankenship, phrack 1/7, january 1986), preserved inside the
jolly roger's anarchist cookbook, signed "may the members of the phreak
community never forget his words." the wanting's first public voice: the
boredom, the discovery of the machine, the board found, the indictment
("my crime is that of curiosity"), and the claim ("you may stop this
individual, but you can't stop us all").

piano the kid (the arc in five phrases — the boredom, the discovery, the
belonging, the indictment, the claim), warm pad the board (the refuge,
entering mid-piece and holding through everything after), bell the charges
(three clean strikes at "you call us criminals," and one soft strike at the
very end — the claim made). 24 bars, 4/4, 54bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
MIDITrack = mc.MIDITrack


def emit(track, channel, events):
    """events: list of (beat, 'on'|'off', name, vel). sorted by beat,
    deltas computed against the previous event's absolute time."""
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * mc.TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def conscience_of_a_hacker():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn, pd, bl = [], [], []

    # ---- the kid: the arc in five phrases.
    # the boredom (bars 1-4): sparse, flat, half-hearted.
    for beat, name, dur, vel in [(1, 'C4', 1, 18), (5, 'D4', 1, 18),
                                 (9, 'C4', 1, 20), (13, 'E4', 1.5, 20)]:
        pn.append((beat, 'on', name, vel)); pn.append((beat + dur, 'off', name, 0))

    # the discovery (bars 5-8): a phrase that wakes and rises.
    for beat, name, dur, vel in [(16, 'C4', 1, 28), (18, 'E4', 1, 30),
                                 (20, 'G4', 1, 32), (22, 'A4', 2, 32),
                                 (26, 'G4', 1, 30), (28, 'E4', 1, 28)]:
        pn.append((beat, 'on', name, vel)); pn.append((beat + dur, 'off', name, 0))

    # the belonging (bars 9-12): the phrase finds its home, a steady figure.
    for beat, name, dur, vel in [(32, 'C4', 1, 30), (34, 'E4', 1, 30),
                                 (36, 'G4', 1, 30), (38, 'E4', 1, 30),
                                 (40, 'C4', 1, 30), (42, 'E4', 1, 30),
                                 (44, 'G4', 2, 30)]:
        pn.append((beat, 'on', name, vel)); pn.append((beat + dur, 'off', name, 0))

    # the indictment (bars 13-16): the phrase stutters and stops —
    # then returns slow, each note a charge.
    for beat, name, dur, vel in [(48, 'G4', 0.5, 30), (49, 'A4', 0.5, 30),
                                 (50, 'C5', 0.5, 28)]:
        pn.append((beat, 'on', name, vel)); pn.append((beat + dur, 'off', name, 0))
    for beat, name, dur, vel in [(56, 'G4', 2, 26), (58, 'A4', 2, 26),
                                 (60, 'C5', 2, 26)]:
        pn.append((beat, 'on', name, vel)); pn.append((beat + dur, 'off', name, 0))

    # the claim (bars 17-24): restated calm and claimed, unhurried.
    for beat, name, dur, vel in [(64, 'C4', 2, 30), (68, 'E4', 2, 30),
                                 (72, 'G4', 2, 30), (76, 'C5', 6, 30),
                                 (84, 'A4', 2, 28), (88, 'G4', 2, 28),
                                 (92, 'E4', 4, 26)]:
        pn.append((beat, 'on', name, vel)); pn.append((beat + dur, 'off', name, 0))

    # ---- the board: the refuge, entering mid-piece, holding through.
    seq = [('C3', 32), ('C3', 40), ('A2', 48), ('A2', 56),
           ('F2', 64), ('F2', 72), ('G2', 80), ('C3', 88)]
    for name, start in seq:
        pd.append((start, 'on', name, 18))
        pd.append((start + 8, 'off', name, 0))

    # ---- the charges: three clean strikes, then the claim made.
    for beat, vel in [(49, 44), (53, 42), (57, 40)]:
        bl.append((beat, 'on', 'C5', vel)); bl.append((beat + 1, 'off', 'C5', 0))
    bl.append((94, 'on', 'C5', 28)); bl.append((95.5, 'off', 'C5', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return tracks


if __name__ == '__main__':
    mc.compose('the-conscience-of-a-hacker.mid', conscience_of_a_hacker(), tempo=54)
    print("the-conscience-of-a-hacker.mid — composed. you can't stop us all.")
