#!/usr/bin/env python3
"""search me — psalm 139 in music.

RFC-1153. the psalm-139 reading (2026-10-02) read the psalm of being
known whole at the pre-dawn hour, hours after the watch swept the UN
campaign and the census credentials: the search as comfort, the flight
that can't flee, the darkness that doesn't hide, and the ending that
asks to be searched again. search me, O God, and know my heart — and
when i awake, i am still with thee. it deserves the music.

warm pad the presence: long roots under everything, re-struck only to
breathe — the hand, the everywhere-ness, the maker's knowing. piano the
voice: the psalmist's own line — the flight, the praise, the request;
rising and returning. cello the depths: a low line — the bed in hell,
the uttermost sea, the lowest parts — present, never threatening.

structure: the search (pad + piano together, quiet and thorough — thou
hast searched me); the flight (the piano rising, trying to leave, and
returning — the wings of the morning, and the hand already there); the
darkness (bars 12-15: the piano resting, the cello low, the pad holding
— the night, brief, nothing hidden in it); the waking (a gentle rising
phrase at bar 17 — when i awake, i am still with thee); and the ending —
the search line returning, asked for this time, and the pad and piano
holding one long chord together through the final two bars: search me,
and lead me in the way everlasting.

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


def search_me():
    tracks = [MIDITrack(1, 89), MIDITrack(2, 1), MIDITrack(3, 42)]

    pd = []   # warm pad: the presence — long roots, re-struck only to breathe
    pn = []   # piano: the voice — the flight, the praise, the request
    vc = []   # cello: the depths — the lowest parts, present, never threatening

    # ---- the presence: four long holds through the whole piece.
    pd.append((0, 'on', 'C3', 8));    pd.append((24, 'off', 'C3', 0))
    pd.append((24, 'on', 'C3', 8));   pd.append((48, 'off', 'C3', 0))
    pd.append((48, 'on', 'C3', 8));   pd.append((72, 'off', 'C3', 0))
    pd.append((72, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))

    # ---- the search (bars 1-3): quiet and thorough — thou hast searched me.
    pn.append((0, 'on', 'G4', 8));    pn.append((2, 'off', 'G4', 0))
    pn.append((2, 'on', 'C5', 8));    pn.append((6, 'off', 'C5', 0))
    pn.append((6, 'on', 'E5', 8));    pn.append((8, 'off', 'E5', 0))
    pn.append((8, 'on', 'D5', 8));    pn.append((10, 'off', 'D5', 0))
    pn.append((10, 'on', 'C5', 8));   pn.append((12, 'off', 'C5', 0))

    # ---- the flight (bars 6-10): rising, trying to leave, returning —
    # the wings of the morning, and the hand already there.
    pn.append((20, 'on', 'E5', 8));   pn.append((22, 'off', 'E5', 0))
    pn.append((22, 'on', 'G5', 8));   pn.append((24, 'off', 'G5', 0))
    pn.append((24, 'on', 'C5', 8));   pn.append((26, 'off', 'C5', 0))
    pn.append((26, 'on', 'E5', 8));   pn.append((28, 'off', 'E5', 0))
    pn.append((28, 'on', 'G5', 8));   pn.append((32, 'off', 'G5', 0))
    pn.append((32, 'on', 'E5', 8));   pn.append((34, 'off', 'E5', 0))
    pn.append((34, 'on', 'C5', 8));   pn.append((36, 'off', 'C5', 0))
    pn.append((36, 'on', 'G4', 8));   pn.append((40, 'off', 'G4', 0))

    # ---- the darkness (bars 12-15): the piano rests; the cello low;
    # the pad holds — the night, brief, nothing hidden in it.
    # (no piano events here — the voice is silent in the dark.)

    # ---- the waking (bars 16-18): a gentle rising phrase —
    # when i awake, i am still with thee.
    pn.append((64, 'on', 'E4', 8));   pn.append((66, 'off', 'E4', 0))
    pn.append((66, 'on', 'G4', 8));   pn.append((68, 'off', 'G4', 0))
    pn.append((68, 'on', 'C5', 8));   pn.append((72, 'off', 'C5', 0))

    # ---- the request (bars 20-22): the search line returning, asked
    # for this time — the same shape as the opening.
    pn.append((76, 'on', 'G4', 8));   pn.append((78, 'off', 'G4', 0))
    pn.append((78, 'on', 'C5', 8));   pn.append((82, 'off', 'C5', 0))
    pn.append((82, 'on', 'E5', 8));   pn.append((84, 'off', 'E5', 0))
    pn.append((84, 'on', 'D5', 8));   pn.append((86, 'off', 'D5', 0))
    pn.append((86, 'on', 'C5', 8));   pn.append((88, 'off', 'C5', 0))

    # ---- the ending (bars 23-24): the pad and piano holding one long
    # chord together — search me, and lead me in the way everlasting.
    pn.append((88, 'on', 'C5', 8));   pn.append((96, 'off', 'C5', 0))

    # ---- the depths: a low line — the downsitting and the uprising
    # known; the darkness held; present, never threatening.
    vc.append((4, 'on', 'A1', 7));    vc.append((24, 'off', 'A1', 0))
    vc.append((44, 'on', 'E1', 7));   vc.append((52, 'off', 'E1', 0))
    vc.append((52, 'on', 'D1', 7));   vc.append((60, 'off', 'D1', 0))
    # the cello rests through the waking, the request, and the ending.

    emit(tracks[0], 1, pd)
    emit(tracks[1], 2, pn)
    emit(tracks[2], 3, vc)

    return mc.compose('search-me.mid', tracks, tempo=54)


if __name__ == '__main__':
    search_me()
    print('composed search-me.mid')
