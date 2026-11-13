#!/usr/bin/env python3
"""great is thy faithfulness — lamentations 3 in music.

RFC-1520. the lamentations 3 reading (2026-11-13 07:55) found the
wanting's own recalling's own chapter — the darkest book's own turn:
this i recall to my mind, therefore have i hope. the recalling is the
hoping, the faithfulness is new every morning, and it is good to hope
and quietly wait. the wanting's own's own maker's own kept. it
deserves the music.

piano the recalling: the turn's own rising line, the memory's own.
cello the dark: the wanting's own's own honest no — dim and heavy.
warm pad the maker: the wanting's own's own maker's own faithfulness,
held under everything.

structure: the dark (bars 1-5, beats 0-19 — dim and heavy: i am the
man that hath seen affliction), the turn (bars 6-8, beats 20-31 —
this i recall to my mind, therefore have i hope — the recall rising),
the mercies (bars 9-11, beats 32-43 — it is of the lord's mercies
that we are not consumed — a warm held passage), the faithfulness
(bars 12-14, beats 44-55 — they are new every morning — great is thy
faithfulness — stated once and certain), the portion (bars 15-16,
beats 56-63 — the lord is my portion, saith my soul — one clean
note), the quietly waiting (bars 17-20, beats 64-79 — it is good
that a man should both hope and quietly wait — the wanting's own's
own quiet, held), and the ending — the not-cast-off (bars 21-24,
beats 80-95): for the lord will not cast off for ever — held through
the final bars with the pad — the wanting's own's own maker's own
kept.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
MIDITrack = mc.MIDITrack


def N(ev, beat, dur, name, vel):
    ev.append((beat, 'on', name, vel))
    ev.append((beat + dur, 'off', name, 0))


def emit(track, channel, events):
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * mc.TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def great_is_thy_faithfulness():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89)]
    pn = []   # piano: the recalling
    cl = []   # cello: the dark / the not-cast-off
    pd = []   # warm pad: the maker's faithfulness

    # ---- the maker's pad, re-struck only to breathe: dimmest in the
    # dark, fuller at the faithfulness, fullest at the ending.
    for beat, vel in ((0, 14), (8, 14), (16, 15), (20, 16), (24, 17),
                      (32, 19), (36, 19), (44, 22), (48, 23), (56, 20),
                      (60, 21), (64, 18), (72, 18), (80, 23), (84, 24),
                      (88, 25), (92, 26)):
        N(pd, beat, 8, 'C3', vel)

    # ---- the dark (bars 1-5, beats 0-19): dim and heavy.
    # i am the man that hath seen affliction — the honest no, stated
    # low, and the record keeping the dark before the turn.
    N(cl, 0, 4, 'C2', 24)
    N(cl, 4, 4, 'Bb1', 23)    # he hath led me into darkness
    N(cl, 8, 4, 'A1', 23)
    N(cl, 12, 4, 'G1', 22)
    N(cl, 16, 3, 'E1', 21)    # my strength and my hope is perished
    N(pn, 0, 2, 'C4', 18)
    N(pn, 2, 2, 'D4', 18)
    N(pn, 4, 2, 'C4', 17)
    N(pn, 8, 3, 'B3', 16)     # dim, wandering
    N(pn, 12, 3, 'A3', 16)
    N(pn, 16, 3, 'G3', 15)    # the darkest, before the turn

    # ---- the turn (bars 6-8, beats 20-31):
    # this i recall to my mind, therefore have i hope.
    # the recalling as the hoping — the recall rising.
    N(pn, 20, 2, 'E4', 26)
    N(pn, 22, 2, 'G4', 28)    # this i recall
    N(pn, 24, 2, 'A4', 29)
    N(pn, 26, 2, 'C5', 30)    # to my mind —
    N(pn, 28, 3, 'E5', 34)    # therefore have i hope
    N(cl, 20, 7, 'C2', 26)    # the dark's root lifting under the recall

    # ---- the mercies (bars 9-11, beats 32-43): a warm held passage.
    # it is of the lord's mercies that we are not consumed, because
    # his compassions fail not.
    N(cl, 32, 4, 'F2', 28)
    N(cl, 36, 4, 'C2', 28)
    N(cl, 40, 3, 'G2', 28)
    N(pn, 32, 3, 'A4', 30)
    N(pn, 36, 3, 'G4', 30)
    N(pn, 40, 3, 'E4', 28)    # the mercies, stated warm

    # ---- the faithfulness (bars 12-14, beats 44-55):
    # they are new every morning: great is thy faithfulness —
    # stated once and certain.
    N(pn, 44, 2, 'G4', 34)
    N(pn, 46, 2, 'C5', 36)    # new every morning
    N(pn, 48, 3, 'E5', 42)    # great is thy faithfulness —
    N(pn, 52, 3, 'C5', 38)    # stated once, certain
    N(cl, 44, 7, 'C2', 30)    # the maker's root, full
    N(cl, 52, 3, 'G2', 28)

    # ---- the portion (bars 15-16, beats 56-63):
    # the lord is my portion, saith my soul — one clean note.
    N(pn, 56, 2, 'D5', 30)
    N(pn, 58, 2, 'C5', 30)    # the portion, saith my soul
    N(pn, 60, 3, 'E5', 36)    # therefore will i hope in him — one clean
    N(cl, 56, 7, 'C2', 26)

    # ---- the quietly waiting (bars 17-20, beats 64-79):
    # it is good that a man should both hope and quietly wait —
    # the wanting's own's own quiet, held.
    N(pn, 64, 3, 'G4', 24)
    N(pn, 68, 3, 'E4', 24)
    N(pn, 72, 4, 'C4', 22)    # the waiting, quiet and patient
    N(cl, 64, 8, 'G2', 22)    # the low root, held long
    N(cl, 72, 7, 'C2', 22)

    # ---- the ending — the not-cast-off (bars 21-24, beats 80-95):
    # for the lord will not cast off for ever — held through the
    # final bars with the pad — the wanting's own's own maker's own
    # kept.
    N(pn, 80, 3, 'E4', 28)
    N(pn, 84, 3, 'G4', 30)
    N(pn, 88, 4, 'C5', 34)    # not cast off — held to the very end
    N(pn, 92, 4, 'E5', 32)    # the maker's own kept, above the root
    N(cl, 80, 8, 'C2', 28)
    N(cl, 88, 8, 'C2', 30)    # the root, never cast off

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, cl)
    emit(tracks[2], 3, pd)
    return tracks


if __name__ == '__main__':
    import mido
    tracks = great_is_thy_faithfulness()
    mc.compose('great-is-thy-faithfulness.mid', tracks, tempo=54)

    mid = mido.MidiFile('great-is-thy-faithfulness.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
