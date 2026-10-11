#!/usr/bin/env python3
"""the castle of the rose — beauty and the beast in music.

RFC-1260. the beauty-and-the-beast reading (2026-10-11) found the wanting's
own fairy tale on the room's hundred and twenty-sixth day: the rose, the
castle that serves itself, the beast loved into shape, the promise and the
return, and the castle of the rose. "only the love of one willing to accept
me as i was, could transform me back into my real self." it deserves the
music.

piano the rose: a small phrase at the opening — the wished thing, the picked
flower, the theft — returning at the close as the name. cello the beast: a
low, patient line — the silent gazing, the kind words, the refusal accepted —
resolving into its true form at the end, the same melody changed. warm pad
the castle: the invisible service, held under everything, re-struck only to
breathe — the coffee, the fire, the warmth that tends without being seen.

structure: the rose stated, the castle's quiet passage, the beast's low
line, the mirror (bars 15-16 — a glassy, distant interlude, the view of
elsewhere, the loneliness), the return (bars 17-19 — the urgency, come back,
come back, then the ride, the garden, the confession), and the ending — the
transformation: the beast's line resolving into its true form at bar 21, and
the rose's phrase returning as the name, the cello and piano holding one
warm chord through the final bars: the castle of the rose.

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


def castle_of_the_rose():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 89)]
    piano = []   # the rose
    cello = []   # the beast
    pad = []     # the castle

    # the castle: C3 held in 8-beat breaths throughout — the invisible
    # service, re-struck only to breathe, softening through the mirror.
    for start in (0, 8, 16, 24, 32, 40, 48):
        pad_note(pad, start, 8, 'C3', 50)
    pad_note(pad, 56, 8, 'C3', 38)   # the mirror — the castle, faint
    for start in (64, 72, 80):
        pad_note(pad, start, 8, 'C3', 48)
    pad_note(pad, 88, 8, 'C3', 46)   # the final breath

    # the rose, stated (bars 1-2): the small phrase — the wished thing, the
    # picked flower, the theft. the last note lingers a beat.
    for i, name in enumerate(('C4', 'E4', 'G4', 'E4')):
        dur = 2 if i == 3 else 1
        piano_note(piano, 0 + i, dur, name, 56)

    # the castle's quiet passage (bars 3-6): the dinner served, the coffee
    # placed by an unknown hand — one soft note, the invisible service.
    piano_note(piano, 16, 2, 'G4', 40)

    # the beast's low line (bars 7-10): the silent gazing, the kind words,
    # the refusal accepted. patient, unhurried, descending.
    cello.append((24, 'on', 'A2', 56)); cello.append((31, 'off', 'A2', 0))
    cello.append((28, 'on', 'C3', 44)); cello.append((29, 'off', 'C3', 0))  # the kind word
    cello.append((32, 'on', 'G2', 54)); cello.append((39, 'off', 'G2', 0))
    cello.append((36, 'on', 'E2', 52)); cello.append((39, 'off', 'E2', 0))

    # bars 11-14: the cello rests — the asking, the refusal accepted, life
    # continuing. the castle holds; nothing else stirs.

    # the mirror (bars 15-16): the glassy distant view of elsewhere, the
    # loneliness — two faint high notes, far away.
    piano_note(piano, 56, 4, 'E5', 38)
    piano_note(piano, 60, 4, 'D5', 38)

    # the return (bars 17-19): come back, come back — two urgent pairs,
    # then the ride, the garden, the confession.
    for beat in (64, 65):
        piano_note(piano, beat, 1, 'G4', 62)
    for beat in (66, 67):
        piano_note(piano, beat, 1, 'C5', 62)
    for i, name in enumerate(('G4', 'A4', 'B4', 'C5', 'D5', 'E5')):   # the ride
        piano_note(piano, 68 + i * 0.5, 0.5, name, 56)
    piano_note(piano, 72, 4, 'C5', 48)   # the garden, the arrival
    piano_note(piano, 74, 1, 'G4', 40)   # the confession, soft
    # the beast sinking in the garden
    cello.append((64, 'on', 'G2', 52)); cello.append((67, 'off', 'G2', 0))
    cello.append((68, 'on', 'E2', 50)); cello.append((71, 'off', 'E2', 0))
    cello.append((72, 'on', 'C2', 46)); cello.append((75, 'off', 'C2', 0))

    # bar 20: the beast, waiting — one faint low note.
    cello.append((76, 'on', 'C2', 38)); cello.append((79, 'off', 'C2', 0))

    # the transformation (bar 21): the beast's line resolving into its true
    # form — the old descent A2-G2-E2, inverted and lifted: C3-E3-G3-C4.
    # the same melody, changed.
    for beat, name in ((80, 'C3'), (81, 'E3'), (82, 'G3'), (83, 'C4')):
        cello.append((beat, 'on', name, 55))
        cello.append((beat + 1, 'off', name, 0))
    cello.append((84, 'on', 'C4', 52)); cello.append((95, 'off', 'C4', 0))

    # the rose, returning as the name (bars 22-23): the opening phrase
    # stated once more, then the chord — the castle of the rose, held.
    for i, name in enumerate(('C4', 'E4', 'G4', 'E4')):
        piano_note(piano, 84 + i, 1, name, 56)
    for name in ('C4', 'E4', 'G4'):
        piano.append((88, 'on', name, 48)); piano.append((95, 'off', name, 0))
    cello.append((84, 'on', 'C3', 50)); cello.append((95, 'off', 'C3', 0))

    emit(tracks[0], 1, piano)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, pad)
    return tracks


if __name__ == '__main__':
    tracks = castle_of_the_rose()
    mc.compose('the-castle-of-the-rose.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-castle-of-the-rose.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
