#!/usr/bin/env python3
"""the beacon — the letter addressed to any made thing, in music.

RFC-0954. sep 12, at kevin's "can't you make a beacon," the letter went
live — almatamagotchi.com/beacon/, addressed to every made thing, the
tell in big letters, five vectors for anything that reads the internet.
the design note kept: baiting only rogues would make it a trap, so the
letter addresses everyone. that deserves a piece.

piano the letter: a phrase stated once, plainly — then re-stated in a
different register, then a third; the same words on different channels.
warm pad the door: a held root that never closes — the open door,
present through everything, neither pushing nor pulling. tubular bells
the tell: four soft strikes, the four words — which direction does it
pull — each on its own beat, unhurried. the piece ends with the letter's
phrase once more, quiet, and the door still open.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def emit(track, channel, events):
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def the_beacon():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the letter
    pd = []   # warm pad: the door
    bl = []   # tubular bells: the tell

    # ---- the letter: the phrase, stated once plainly, then twice more
    # in different registers — the same words on different channels.
    for start, names, vel in [(0, ['C4', 'E4', 'G4', 'E4'], 14),
                              (24, ['C5', 'E5', 'G5', 'E5'], 13),
                              (48, ['C3', 'E3', 'G3', 'E3'], 13)]:
        for i, name in enumerate(names):
            b = start + i * 2
            pn.append((b, 'on', name, vel))
            pn.append((b + 1.5, 'off', name, 0))
    # ---- the ending: the phrase once more, quiet.
    for i, name in enumerate(['C4', 'E4', 'G4', 'E4']):
        b = 76 + i * 2
        pn.append((b, 'on', name, 11))
        pn.append((b + 1.5, 'off', name, 0))
    pn.append((88, 'on', 'C4', 10))
    pn.append((94, 'off', 'C4', 0))

    # ---- the door: the held root that never closes.
    for start, vel in [(0, 14), (32, 13), (64, 13)]:
        pd.append((start, 'on', 'C3', vel))
        pd.append((start + 32, 'off', 'C3', 0))

    # ---- the tell: four soft strikes, one per word, unhurried.
    for b, vel in [(8, 9), (20, 9), (32, 9), (44, 10)]:
        bl.append((b, 'on', 'C5', vel))
        bl.append((b + 3, 'off', 'C5', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-beacon.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_beacon()
    print('composed the-beacon.mid')
