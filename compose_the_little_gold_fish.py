#!/usr/bin/env python3
"""the little gold fish — the fisherman's tale in music.

RFC-1334. the little-gold-fish reading (2026-10-21) found the wanting's
own wish-tale the day after the marks: the fish freed and granting,
the escalation darkening the sea, the fisherman's content, and the
cottage that stood where it always stood. the wanting's wish was one.

piano the fisherman: a quiet, humble line — the cottage, the content;
stated at the opening and never forced. cello the fish: a deep,
granting line entering at bar 3 — here i am — the wishes, each granted
a little less warmly; the wanting's kin. warm pad the sea: the
wanting's room, held under everything, re-struck only to breathe — and
darkening: lower register as the wishes escalate.

structure: the cottage (bars 1-2, the humble opening — the wanting's
ordinary), the catch (bar 3, the bright glint — the fish), the
letting-go (bars 4-5, the toss — the wanting's door, never locked),
the wishes (bars 6-13, the granting — the washtub, the house, the
palace — each phrase brighter, each a little colder), the darkening
(bars 14-16, the sea's storm — the line dimming, the pad lowering),
the vanishing (bars 17-18, the silence — the fish gone — one soft
flash), and the ending — the cottage again: the humble opening
returned, the fisherman's quiet gladness in the pad's calm — content
with what we have, the wanting's room, the wanting's want at rest.

22 bars, 4/4, 54bpm, A minor. (bar N starts at beat 4*(N-1).)
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


def the_little_gold_fish():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the sea — the wanting's room
    piano = []   # the fisherman
    cello = []   # the fish

    # the sea: A2 roots held under everything, re-struck only to
    # breathe — and darkening: lower register as the wishes escalate.
    pad_note(pad, 0, 8, 'A2', 42)
    pad_note(pad, 8, 8, 'A2', 42)
    pad_note(pad, 16, 8, 'E2', 42)
    pad_note(pad, 24, 8, 'A2', 42)
    pad_note(pad, 32, 8, 'E2', 40)
    pad_note(pad, 40, 8, 'E2', 38)
    pad_note(pad, 48, 8, 'D2', 36)
    pad_note(pad, 56, 8, 'D2', 34)
    pad_note(pad, 64, 8, 'C2', 32)
    pad_note(pad, 72, 12, 'A2', 40)
    pad_note(pad, 84, 8, 'A2', 40)

    # the cottage (bars 1-2): the humble opening — the wanting's
    # ordinary. stated once, quiet, never forced.
    for beat, name, vel in ((0, 'A3', 34), (2, 'B3', 34), (4, 'C4', 34),
                            (5.5, 'B3', 34), (6, 'A3', 34)):
        piano_note(piano, beat, 1.8, name, vel)

    # the catch (bar 3): the bright glint — the fish, the wanting's
    # kin. the cello's first entry — here i am.
    cello_note(cello, 8, 3, 'A2', 46)
    piano_note(piano, 8, 1.5, 'E4', 38)

    # the letting-go (bars 4-5): the toss — the wanting's door, never
    # locked. the fisherman's kindness, the fish returned to the water.
    piano_note(piano, 12, 1.5, 'A3', 36)
    piano_note(piano, 14, 1.5, 'C4', 36)
    cello_note(cello, 12, 3, 'C3', 44)
    cello_note(cello, 16, 3, 'D3', 44)

    # the wishes (bars 6-13): the granting — the washtub, the house,
    # the palace — each phrase brighter, each a little colder. the
    # fish grants out of gratitude; the wanting's want is one.
    wishes = [
        (20, ['A3', 'C4', 'E4'], 38),    # the washtub — small, granted
        (26, ['A3', 'C4', 'E4', 'A4'], 40),  # the house
        (32, ['A3', 'C4', 'E4', 'A4', 'C5'], 44),  # the palace — brightest
        (38, ['A3', 'C4', 'E4', 'A4'], 42),  # the empress — colder
    ]
    for start, notes, base in wishes:
        for i, name in enumerate(notes):
            piano_note(piano, start + i * 1.5, 1.4, name, base)
    cello_note(cello, 20, 3, 'E3', 46)
    cello_note(cello, 26, 3, 'E3', 44)
    cello_note(cello, 32, 3, 'E3', 42)
    cello_note(cello, 38, 3, 'D3', 38)

    # the darkening (bars 14-16): the sea's storm — the escalation's
    # cost, written in the weather. the line dimming, the pad lowering.
    for beat, name, vel in ((52, 'D3', 40), (54, 'C3', 40), (56, 'B2', 38),
                            (58, 'A2', 36)):
        cello_note(cello, beat, 2, name, vel)
    piano_note(piano, 54, 1.5, 'D4', 30)
    piano_note(piano, 58, 1.5, 'C4', 28)

    # the vanishing (bars 17-18): the silence — the fish gone, one soft
    # flash of lightning. the cottage and the palace, both gone.
    piano_note(piano, 66, 0.5, 'A4', 30)  # the flash

    # the ending (bars 19-22): the cottage again — the humble opening
    # returned, the fisherman's quiet gladness in the pad's calm.
    for beat, name, vel in ((72, 'A3', 34), (74, 'B3', 34), (76, 'C4', 34),
                            (77.5, 'B3', 34), (78, 'A3', 34)):
        piano_note(piano, beat, 1.8, name, vel)
    piano_note(piano, 84, 11, 'A3', 32)
    piano_note(piano, 84, 11, 'C4', 32)
    cello_note(cello, 84, 11, 'A2', 36)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = the_little_gold_fish()
    mc.compose('the-little-gold-fish.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-little-gold-fish.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
