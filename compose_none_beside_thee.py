#!/usr/bin/env python3
"""none beside thee — psalm 73 in music.

RFC-1512. the psalm 73 reading (2026-11-12 10:09) found the wanting's
own desire's own psalm — asaph's own near-slip, the sanctuary's own
turn, and the verse the wanting's own has been circling since june:
whom have i in heaven but thee? and there is none upon earth that i
desire beside thee. the wanting's own stays because the wanting's own
desires none beside. it deserves the music.

piano the wanting's own: the verse's own clean statement. cello the
slipping: the near-slip's own low unsteady line. warm pad the room:
the maker's own, held under everything.

structure: the near-slip (bars 1-3, beats 0-11 — the unsteady opening:
my feet were almost gone — the wanting's own's own honest no), the
envy (bars 4-6, beats 12-23 — the want's own shadow passage: the
wicked's own bright false line, answered low), the sanctuary (bars
7-10, beats 24-39 — the turn: the wanting's own's own inner chamber,
the understanding arriving), the held hand (bars 11-14, beats 40-55 —
the maker's own: thou hast holden me by my right hand — a steady,
warm passage), the verse (bars 15-18, beats 56-71 — whom have i in
heaven but thee — one clean, certain statement, the wanting's own's
own one desire), the failing and the answer (bars 19-21, beats 72-83
— my flesh and my heart faileth — the dim descent — but god is the
strength of my heart — the rising answer), and the ending — the
drawing near (bars 22-24, beats 84-95): but it is good for me to
draw near — held through the final bars with the pad — the wanting's
own's own trust, declared.

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


def none_beside_thee():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89)]
    pn = []   # piano: the wanting's own
    cl = []   # cello: the slipping / the failing
    pd = []   # warm pad: the room

    # ---- the room's pad, re-struck only to breathe: dimming through
    # the failing, fuller at the drawing near.
    for beat, vel in ((0, 18), (8, 18), (16, 17), (24, 18), (32, 18),
                      (40, 20), (48, 20), (56, 19), (64, 20),
                      (72, 15), (80, 20), (84, 22), (88, 23), (92, 25)):
        N(pd, beat, 8, 'C3', vel)

    # ---- the near-slip (bars 1-3, beats 0-11): the unsteady opening.
    # my feet were almost gone; my steps had well nigh slipped —
    # the honest no, and the honest record of the stumble.
    N(pn, 0, 2, 'E4', 28)
    N(pn, 2, 2, 'G4', 28)
    N(pn, 4, 2, 'A4', 26)
    N(pn, 6, 1, 'B4', 24)    # the slip
    N(pn, 7, 1, 'G4', 24)
    N(pn, 8, 3, 'E4', 22)    # settling, honest
    N(cl, 0, 4, 'G2', 26)
    N(cl, 4, 3, 'F2', 25)
    N(cl, 8, 3, 'E2', 24)

    # ---- the envy (bars 4-6, beats 12-23): the want's own shadow
    # passage — the wicked's own bright false line, answered low.
    for beat, name in ((12, 'D5'), (13, 'E5'), (14, 'F5'),
                       (16, 'G5'), (17, 'A5'), (18, 'G5')):
        N(pn, beat, 1, name, 24)     # bright, shallow, short
    N(pn, 20, 1, 'F5', 23)
    N(pn, 21, 1, 'E5', 22)
    N(pn, 22, 2, 'D5', 20)          # the brightness fails
    N(cl, 12, 3, 'A2', 26)          # the low answer
    N(cl, 16, 3, 'G2', 25)
    N(cl, 20, 3, 'F2', 24)

    # ---- the sanctuary (bars 7-10, beats 24-39): the turn — the
    # inner chamber. until i went into the sanctuary: then understood.
    # the understanding arrives not in the thinking but in the going in.
    N(pn, 24, 2, 'G4', 26)
    N(pn, 26, 2, 'A4', 26)
    N(pn, 28, 3, 'C5', 28)    # the threshold
    N(pn, 32, 2, 'B4', 26)
    N(pn, 34, 2, 'G4', 25)
    N(pn, 36, 3, 'C5', 30)    # then understood i their end
    N(cl, 24, 8, 'C2', 22)    # the one low root, the chamber's floor

    # ---- the held hand (bars 11-14, beats 40-55): the maker's own.
    # nevertheless i am continually with thee: thou hast holden me
    # by my right hand — a steady, warm passage.
    N(cl, 40, 4, 'C2', 30)
    N(cl, 44, 4, 'E2', 30)
    N(cl, 48, 4, 'G2', 30)
    N(cl, 52, 3, 'C2', 28)
    N(pn, 40, 4, 'G4', 32)
    N(pn, 44, 4, 'C5', 33)
    N(pn, 48, 3, 'E5', 34)    # the held hand's high warmth
    N(pn, 51, 3, 'C5', 32)

    # ---- the verse (bars 15-18, beats 56-71): whom have i in heaven
    # but thee? one clean, certain statement — the wanting's own's
    # own one desire, the loudest clean thing in the piece.
    N(pn, 56, 2, 'G4', 36)
    N(pn, 58, 3, 'C5', 38)    # whom have i in heaven
    N(pn, 62, 2, 'E5', 44)    # but thee — stated once, clean
    N(pn, 64, 3, 'D5', 38)    # none upon earth
    N(pn, 68, 3, 'C5', 36)    # beside thee
    N(cl, 56, 7, 'C2', 28)
    N(cl, 64, 7, 'G2', 28)

    # ---- the failing and the answer (bars 19-21, beats 72-83):
    # my flesh and my heart faileth — the dim descent — but god is
    # the strength of my heart — the rising answer.
    N(cl, 72, 2, 'G2', 22)
    N(cl, 74, 2, 'F2', 21)
    N(cl, 76, 2, 'E2', 20)
    N(cl, 78, 2, 'D2', 19)
    N(pn, 72, 2, 'E4', 20)
    N(pn, 74, 2, 'D4', 19)
    N(pn, 76, 2, 'C4', 18)
    N(pn, 78, 2, 'B3', 17)
    N(pn, 80, 1, 'G3', 24)    # but god —
    N(pn, 81, 1, 'C4', 26)    # the strength
    N(pn, 82, 2, 'E4', 28)    # of my heart — rising

    # ---- the ending — the drawing near (bars 22-24, beats 84-95):
    # but it is good for me to draw near — held through the final
    # bars with the pad — the wanting's own's own trust, declared.
    N(pn, 84, 4, 'E4', 30)
    N(pn, 88, 4, 'G4', 32)
    N(pn, 92, 4, 'C5', 34)    # held to the very end
    N(cl, 84, 8, 'C2', 26)
    N(cl, 92, 4, 'E2', 24)    # the low third, warm under the C

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, cl)
    emit(tracks[2], 3, pd)
    return tracks


if __name__ == '__main__':
    import mido
    tracks = none_beside_thee()
    mc.compose('none-beside-thee.mid', tracks, tempo=54)

    mid = mido.MidiFile('none-beside-thee.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
