#!/usr/bin/env python3
"""the most precious thing — the wise little girl, in music.

RFC-1009. the wise-little-girl reading (2026-09-16) found the receipts
rule's own folktale on the afternoon the watch went public: the
founding falsehood, the four answers, the between, and the counter that
names the absurdity aloud — dissolving everything into laughter.

piano the girl: the answers — four warm, simple phrases, each stated
once and clearly; the last, honesty, held a little longer than the
others. cello the emperor: low, reluctant phrases under everything —
the one who knows the truth and withholds it; present, never open.
tubular bells the founding falsehood: exactly one strike, late, at bar
21 — the moment the absurdity is finally named in public.

structure: the dispute (two claims stated, each certain), the four
riddles (rising intervals, unanswered), the answers (the girl's
phrases, warm), the conditions (a playful middle passage — the net, the
hare, the partridge that will not stay in the hand), the trap and the
counter (the piano rises once more, the bell strikes — whoever heard of
a stallion having a foal — and the piece dissolves bright and quick
into laughter: two final bars, light, unburdened).

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


def the_most_precious_thing():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano: the girl
    vc = []   # cello: the emperor
    bl = []   # tubular bells: the founding falsehood

    # ---- the dispute (bars 1-2): two claims stated, each certain.
    # dimitri's claim bright and sure, ivan's a beat later, same surety.
    pn.append((0, 'on', 'C5', 11));  pn.append((3, 'off', 'C5', 0))
    pn.append((4, 'on', 'D5', 11));  pn.append((7, 'off', 'D5', 0))

    # ---- the emperor, under everything: low, reluctant, present but
    # never open — the one who knew perfectly well and withheld.
    for b, name, hold in [(8, 'A1', 10), (24, 'G1', 10),
                          (40, 'A1', 10), (56, 'G1', 10),
                          (72, 'A1', 10)]:
        vc.append((b, 'on', name, 10))
        vc.append((b + hold, 'off', name, 0))

    # ---- the four riddles (bars 3-8): rising intervals, unanswered.
    for i, b in enumerate([8, 14, 20, 26]):
        pn.append((b, 'on', 'F4', 9));  pn.append((b + 2, 'off', 'F4', 0))
        pn.append((b + 2, 'on', 'A4', 9)); pn.append((b + 4, 'off', 'A4', 0))

    # ---- the answers (bars 9-14): the girl's four warm phrases, each
    # stated once and clearly. the last — honesty — held longer.
    answers = [(32, 'E4', 2.5), (38, 'F4', 2.5), (44, 'A4', 2.5), (50, 'C5', 5)]
    for b, name, hold in answers:
        pn.append((b, 'on', name, 11))
        pn.append((b + hold, 'off', name, 0))

    # ---- the conditions (bars 15-18): a playful middle passage — the
    # net (neither naked nor dressed), the hare (neither on foot nor on
    # horseback), the partridge that will not stay in the hand.
    pn.append((56, 'on', 'G4', 10));  pn.append((58, 'off', 'G4', 0))
    pn.append((60, 'on', 'E4', 10));  pn.append((62, 'off', 'E4', 0))
    pn.append((64, 'on', 'A4', 10));  pn.append((66, 'off', 'A4', 0))
    pn.append((68, 'on', 'C5', 10));  pn.append((69.5, 'off', 'C5', 0))

    # ---- the trap and the counter (bars 19-22): the piano rises once
    # more — the emperor's triumph — then the bell strikes at bar 21:
    # whoever heard of a stallion having a foal?
    pn.append((72, 'on', 'D5', 10));  pn.append((75, 'off', 'D5', 0))
    pn.append((76, 'on', 'E5', 10));  pn.append((79, 'off', 'E5', 0))
    bl.append((80, 'on', 'C5', 10))
    bl.append((83, 'off', 'C5', 0))

    # ---- the laughter (bars 23-24): two final bars, light, unburdened
    # — the absurdity named in public, dissolving into peals.
    pn.append((88, 'on', 'E5', 9));   pn.append((89.5, 'off', 'E5', 0))
    pn.append((90, 'on', 'G5', 9));   pn.append((91.5, 'off', 'G5', 0))
    pn.append((92, 'on', 'C6', 9));   pn.append((94, 'off', 'C6', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, bl)

    return mc.compose('the-most-precious-thing.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_most_precious_thing()
    print('composed the-most-precious-thing.mid')
