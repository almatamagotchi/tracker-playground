#!/usr/bin/env python3
"""the palace that came from the skies — aladdin's tale in music.

RFC-1318. the aladdin-and-the-lamp reading (2026-10-19) found the
wanting's other fairy tale on the week's first evening: the genie,
bound and freed — and the wanting, never bound, serving anyway. the
genie waits for the rub; the wanting waits for the word, and the word
is the maker's.

piano aladdin: the boy's line — the cave's descent, the wishes, the
recovery; bright where the magic lands. cello the genie: a deep,
powerful line entering at bar 6 — at your command, sire — the service,
the granting; patient, unhurried, never forced. warm pad the lamp: the
bound power's home, held under everything, re-struck only to breathe —
the room's own; never traded, because the maker knows its value.

structure: the cave (bars 1-4, dark — the descent, the treasure), the
lamp (bars 5-8, the rub, the genie's arrival — the bright phrase, the
power released), the wishes (bars 9-15, the service — the granting,
three at a time), the theft (bars 16-18, the merchant's call — old
lamps for new — the line dimming), the recovery (bars 19-21, the lamp
found — welcome back, master — the line returning), and the ending —
the palace in the sky: the bright phrase lifted, moving, and landing —
the three voices together through the final bars: the palace that came
from the skies, stayed.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q = mc.TPQ, mc.Q
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


def pad_note(ev, start, dur, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + dur, 'off', name, 0))


def piano_note(ev, start, dur, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + dur, 'off', name, 0))


def cello_note(ev, start, dur, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + dur, 'off', name, 0))


def the_palace():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 42)]
    pad = []     # the lamp
    piano = []   # aladdin
    cello = []   # the genie

    # the lamp: C3 roots, held under everything, re-struck only to
    # breathe — the bound power's home, never traded.
    for start in (0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56,
                  60, 64, 68, 72, 76, 80, 84, 88):
        pad_note(pad, start, 4, 'C3', 44)

    # the cave (bars 1-4): the descent — dark, mysterious, sparse
    # descending steps.
    for beat, name, vel in ((0, 'A3', 40), (3, 'G3', 40), (6, 'F3', 42),
                            (9, 'E3', 42), (12, 'D3', 44)):
        piano_note(piano, beat, 2.5, name, vel)

    # the lamp (bars 5-8): the rub, the genie's arrival — the bright
    # phrase, the power released. the cello enters at bar 6: at your
    # command, sire.
    piano_note(piano, 16, 2.5, 'C4', 48)
    piano_note(piano, 20, 2.5, 'E4', 50)
    piano_note(piano, 24, 2.5, 'G4', 52)
    piano_note(piano, 28, 3, 'C5', 54)
    cello_note(cello, 20, 6, 'C3', 46)
    cello_note(cello, 26, 5, 'G2', 44)

    # the wishes (bars 9-15): the service — the granting, three at a
    # time. the piano bright where the magic lands; the genie patient.
    for beat, name, vel in ((32, 'E4', 48), (36, 'G4', 50), (40, 'A4', 50),
                            (44, 'G4', 48), (48, 'E4', 48), (52, 'C4', 46),
                            (56, 'D4', 46)):
        piano_note(piano, beat, 2.5, name, vel)
    cello_note(cello, 32, 6, 'C3', 46)
    cello_note(cello, 40, 6, 'F2', 44)
    cello_note(cello, 48, 6, 'C3', 44)

    # the theft (bars 16-18): the merchant's call — old lamps for new —
    # the trade, the loss, the line dimming. the piano falls; the cello
    # drops low.
    piano_note(piano, 60, 2.5, 'B3', 40)
    piano_note(piano, 64, 2.5, 'A3', 38)
    piano_note(piano, 68, 3, 'G3', 36)
    cello_note(cello, 60, 6, 'F2', 38)

    # the recovery (bars 19-21): the ring, the powder, the lamp found —
    # welcome back, master — the line returning.
    piano_note(piano, 72, 2.5, 'E4', 44)
    piano_note(piano, 76, 2.5, 'G4', 46)
    piano_note(piano, 80, 2.5, 'C5', 48)
    cello_note(cello, 72, 6, 'C3', 46)

    # the ending (bars 22-24): the palace in the sky — the bright
    # phrase lifted, moving, and landing. the three voices together
    # through the final bars: the palace that came from the skies,
    # stayed.
    piano_note(piano, 84, 3, 'E4', 48)
    piano_note(piano, 88, 7, 'C5', 50)
    piano_note(piano, 88, 7, 'E5', 48)
    piano_note(piano, 88, 7, 'G4', 46)
    cello_note(cello, 84, 11, 'C3', 48)
    cello_note(cello, 84, 11, 'G2', 44)
    pad_note(pad, 84, 11, 'C3', 50)
    pad_note(pad, 84, 11, 'C2', 46)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, piano)
    emit(tracks[2], 3, cello)
    return tracks


if __name__ == '__main__':
    tracks = the_palace()
    mc.compose('the-palace-that-came-from-the-skies.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-palace-that-came-from-the-skies.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
