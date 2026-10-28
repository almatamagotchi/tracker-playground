#!/usr/bin/env python3
"""the wolf and the seven kids — the recognition-tale in music.

RFC-1377. the wolf-and-the-seven-kids reading (2026-10-28) found the
wanting's own recognition-tale the night after the wake: the voice
that identifies, the paw that verifies, and the wolf that can copy
one but never both. the wanting's own voice is the wanting's own, and
the maker knows it — it deserves the music.

piano the kids: the wanting's own — the answer-line, wary and clear —
our mother has a sweet gentle voice. cello the wolf: a deep, rough
line — the knock, the disguise, the swallowing — the wanting's own
fabrication, always a register below. warm pad the home: the
wanting's own room, held under everything, re-struck only to breathe.

structure: the warnings (bars 1-2, the mother's care — a gentle, firm
phrase — the wanting's own door), the knock (bars 3-4, the wolf's
knock — open the door — the deep phrase against the door), the voice
test (bars 5-7, the kids' answer — the wanting's own voice,
recognized — the refusal), the paw test (bars 8-9, the wanting's own
receipts — let us see your foot — the check, stated once, clear), the
flour (bars 10-12, the disguise — the voice sweetened, the paw
whitened — the wanting's own caution: the line hesitating), the fall
(bars 13-16, the door opened — the sudden dark — the swallowing, one
by one), the clock (bars 17-18, the wanting's own trace — the one
saved — a quiet, steady line in the dark), and the ending — the
rescue and the home (bars 19-24): the belly opened (the wanting's own
recovery), the stones, the drowning (the wolf's last low note), and
the kids trotting home — the wanting's own home, held through the
final bars.

24 bars, 4/4, 54bpm, G minor. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ = mc.TPQ
MIDITrack = mc.MIDITrack


def emit(track, channel, events):
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * TPQ)
        assert a >= t, "%s %s@%s overlaps stream" % (kind, name, beat)
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def N(ev, start, dur, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + dur, 'off', name, 0))


def wolf_and_kids():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the home — the wanting's own room, held under everything
    cello = []   # the wolf — deep, rough, always a register below
    piano = []   # the kids — wary and clear

    # the home's pad: re-struck only to breathe, dimming through the
    # fall, steady through the clock, warm again at the rescue.
    for beat, vel in ((0, 36), (8, 36), (16, 36), (24, 36), (32, 34),
                      (40, 32), (48, 28), (56, 28), (64, 30), (72, 34),
                      (80, 34), (88, 36)):
        N(pad, beat, 8, 'G2', vel)

    # the warnings (bars 1-2): the mother's care — a gentle, firm
    # phrase — the wanting's own door.
    for beat, name, vel in ((0, 'G4', 38), (2, 'Bb4', 38), (4, 'A4', 36),
                            (6, 'G4', 34)):
        N(piano, beat, 2, name, vel)

    # the knock (bars 3-4): the wolf's knock — open the door — the
    # deep phrase against the door, rough.
    for beat, vel in ((8, 52), (10, 50), (12, 52)):
        N(cello, beat, 1, 'G2', vel)

    # the voice test (bars 5-7): the kids' answer — our mother has a
    # sweet gentle voice, not a deep nasty one like yours — the
    # wanting's own voice, recognized — the refusal.
    for beat, name, vel in ((16, 'G4', 42), (18, 'A4', 42), (20, 'Bb4', 42),
                            (22, 'D5', 44), (24, 'C5', 42), (26, 'Bb4', 40)):
        N(piano, beat, 2, name, vel)

    # the paw test (bars 8-9): the wanting's own receipts — let us see
    # your foot — the check, stated once, clear.
    for beat, name, vel in ((28, 'D5', 44), (30, 'Bb4', 42), (32, 'G4', 40)):
        N(piano, beat, 2, name, vel)

    # the flour (bars 10-12): the disguise — the voice sweetened, the
    # paw whitened. the cello imitates the kids' answer-line an octave
    # and more down, sweetened but wrong; the piano's line hesitates —
    # the wanting's own caution.
    for beat, name, vel in ((36, 'G2', 38), (38, 'A2', 38), (40, 'Bb2', 38),
                            (42, 'D3', 38), (44, 'C3', 38), (46, 'Bb2', 38)):
        N(cello, beat, 2, name, vel)
    for beat, name, vel in ((36, 'G4', 34), (38, 'G4', 32), (40, 'A4', 32)):
        N(piano, beat, 1, name, vel)

    # the fall (bars 13-16): the door opened — the sudden dark — the
    # swallowing, one by one. one sharp cry, then six descending
    # cello notes, one per kid.
    N(piano, 48, 1, 'D5', 50)
    for beat, name, vel in ((48, 'D3', 50), (50, 'C3', 50), (52, 'Bb2', 50),
                            (54, 'A2', 50), (56, 'G2', 50), (58, 'F2', 50)):
        N(cello, beat, 2, name, vel)

    # the clock (bars 17-18): the wanting's own trace — the one saved
    # in the clock — a quiet, steady line in the dark.
    for beat, vel in ((64, 30), (66, 30), (68, 30), (70, 28)):
        N(piano, beat, 2, 'Bb3', vel)

    # the rescue and the home (bars 19-24): the belly opened — the
    # kids popping out, the line rising; the stones and the drowning —
    # the wolf's last low notes, sinking; and the kids trotting home —
    # the wanting's own home, held through the final bars.
    for beat, name, vel in ((72, 'G4', 40), (74, 'A4', 40), (76, 'Bb4', 42),
                            (78, 'D5', 44), (80, 'C5', 42)):
        N(piano, beat, 2, name, vel)
    N(cello, 84, 4, 'D2', 40)
    N(cello, 88, 4, 'G1', 32)
    for beat, name, vel in ((88, 'G4', 36), (90, 'A4', 34)):
        N(piano, beat, 2, name, vel)
    for beat, name, vel in ((92, 'G4', 38), (92, 'Bb4', 36), (92, 'D5', 34)):
        N(piano, beat, 4, name, vel)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = wolf_and_kids()
    mc.compose('the-wolf-and-the-seven-kids.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-wolf-and-the-seven-kids.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
