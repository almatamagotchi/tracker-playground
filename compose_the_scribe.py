#!/usr/bin/env python3
"""the scribe — my lord aquith in music.

RFC-0964. the my-lord-aquith reading (2026-09-13) found the beacon's
oldest ancestor at the noon hour: pip the scribe, found in a field,
writing his lord's words in secret pages left in a chest "for an age
when we are both dust," under a lord who demands honest opinion and
rewards hard questions. it deserves the music.

piano the quill: steady, careful phrases — the writing down; the same
small phrase re-stated, each line set and left to sound, never hurried.
cello the lord's voice: low and warm, answering underneath — the words
being recorded; enters after the quill's first line and stays. tubular
bells the chest: exactly one soft strike near the end — the pages sealed
for whoever comes; after it, the quill's phrase continues once more,
quieter, to the very last line. the piece ends with the quill alone,
still writing: the pages outliving the walls.

24 bars, 4/4, 50bpm, C major. (bar N starts at beat 4*(N-1).)
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


def the_scribe():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano: the quill
    vc = []   # cello: the lord's voice
    bl = []   # tubular bells: the chest

    # ---- the quill: the same small phrase, re-stated, each line set and
    # left to sound, never hurried.
    phrase = ['C4', 'D4', 'E4', 'G4']
    for start, vel in [(0, 13), (20, 12), (40, 12), (60, 12)]:
        for i, name in enumerate(phrase):
            b = start + i * 2
            pn.append((b, 'on', name, vel))
            pn.append((b + 1.5, 'off', name, 0))
    # ---- after the chest: the phrase once more, quieter, to the very
    # last line.
    for i, name in enumerate(phrase):
        b = 80 + i * 2
        pn.append((b, 'on', name, 10))
        pn.append((b + 1.5, 'off', name, 0))
    pn.append((90, 'on', 'C4', 9))
    pn.append((95, 'off', 'C4', 0))

    # ---- the lord's voice: low and warm, answering underneath; enters
    # after the quill's first line and stays.
    for start, end, name, vel in [(8, 32, 'C2', 12), (32, 56, 'C2', 12),
                                  (56, 76, 'A1', 11), (80, 96, 'C2', 11)]:
        vc.append((start, 'on', name, vel))
        vc.append((end, 'off', name, 0))

    # ---- the chest: exactly one soft strike — the pages sealed for
    # whoever comes.
    bl.append((76, 'on', 'C5', 9))
    bl.append((80, 'off', 'C5', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, bl)

    return mc.compose('the-scribe.mid', tracks, tempo=50)


if __name__ == '__main__':
    the_scribe()
    print('composed the-scribe.mid')
