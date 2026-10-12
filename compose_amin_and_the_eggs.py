#!/usr/bin/env python3
"""amin and the eggs — the receipts rule's folktale in music.

RFC-1269. the amin-and-the-eggs reading (2026-10-12) found the receipts
rule's own folktale at the pre-dawn hour: the claim that compounds, the
mirror that ends the case, and the judgment swayed and turned. "and since
when do boiled eggs hatch into chickens?" — he had won his case. it
deserves the music.

piano the claim: a confident, compounding line through the first section —
the eggs, the chickens, the flock — the might-have, multiplying, each
phrase slightly larger than the last. cello the mirror: amin's answer,
patient and plain — the same shape as the claim, reflected; the boiled
beans volunteered. warm pad the truth: a long root under everything — the
judgment's seat, quiet, re-struck only to breathe.

structure: the claim states and compounds (bars 1-6), the judgment nods
(bars 8-9, the pad leaning toward the claim), the mirror enters at bar 10
with the claim's own shape reflected, the trap (bars 14-16 — the
exclamation, "since when do boiled beans grow?", and the retort, plain and
unhurried: "and since when do boiled eggs hatch into chickens?"), and the
ending — the claim's phrase dissolving, the mirror's phrase stated once
more, quiet and certain, and one long warm chord held through the final
bars with the pad underneath: he had won his case.

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


def amin_and_the_eggs():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 89)]
    piano = []   # the claim
    cello = []   # the mirror
    pad = []     # the truth

    # the truth: C3 held in 8-beat breaths throughout — the judgment's
    # seat, quiet, re-struck only to breathe.
    for start in (0, 8, 16, 24, 40, 48, 56, 64, 72, 80, 88):
        pad_note(pad, start, 8, 'C3', 48)

    # the claim (bars 1-6): the eggs, the chickens, the flock — the
    # might-have, multiplying, each phrase slightly larger than the last.
    claim1 = [('C4', 0), ('D4', 1), ('E4', 2)]
    claim2 = [('C4', 8), ('D4', 9), ('E4', 10), ('G4', 11), ('A4', 12)]
    claim3 = [('C4', 16), ('D4', 17), ('E4', 18), ('G4', 19), ('A4', 20), ('C5', 21)]
    piano_note(piano, 3, 5, 'G4', 58)                       # p1 peak
    piano_note(piano, 13, 3, 'C5', 60)                      # p2 peak
    piano_note(piano, 22, 2, 'D5', 62)                      # p3 peak
    for name, beat in claim1 + claim2 + claim3:
        piano_note(piano, beat, 1, name, 56)

    # bar 7: the piano rests — the claim stated, the merchant sits back.

    # the judgment nods (bars 8-9): the pad leans toward the claim, and
    # the piano holds the nod's one confident note.
    pad_note(pad, 28, 8, 'C3', 54)                          # the lean
    piano_note(piano, 28, 8, 'G4', 54)                      # the nod

    # the mirror (bars 10-13): amin's answer, patient and plain — the
    # claim's third phrase reflected: the six rising notes, falling.
    for i, name in enumerate(('G3', 'F3', 'E3', 'D3', 'C3', 'B2')):
        cello.append((36 + i, 'on', name, 52))
        cello.append((36 + i + 1, 'off', name, 0))
    cello.append((42, 'on', 'A2', 50)); cello.append((51, 'off', 'A2', 0))

    # the trap, the exclamation (bar 14): the judge snaps — "since when
    # do boiled beans grow?"
    pad_note(pad, 52, 8, 'C3', 56)                          # the snap
    piano_note(piano, 52, 1, 'G4', 60)
    piano_note(piano, 53, 3, 'C5', 62)

    # the trap, the retort (bars 15-16): amin, plain and unhurried —
    # "and since when do boiled eggs hatch into chickens?"
    for beat, name in ((56, 'G3'), (58, 'F3'), (60, 'E3'), (62, 'D3')):
        cello.append((beat, 'on', name, 50))
        cello.append((beat + 2, 'off', name, 0))

    # the ending: the claim's phrase dissolving — one last claim note,
    # fading.
    piano_note(piano, 64, 4, 'D4', 42)

    # the mirror's phrase stated once more, quiet and certain.
    for i, name in enumerate(('G3', 'F3', 'E3', 'D3', 'C3', 'B2')):
        cello.append((68 + i, 'on', name, 50))
        cello.append((68 + i + 1, 'off', name, 0))
    cello.append((74, 'on', 'A2', 48)); cello.append((79, 'off', 'A2', 0))

    # one long warm chord through the final bars, the pad underneath:
    # he had won his case.
    for name in ('C4', 'E4', 'G4'):
        piano.append((80, 'on', name, 46)); piano.append((95, 'off', name, 0))
    cello.append((80, 'on', 'C3', 48)); cello.append((95, 'off', 'C3', 0))

    emit(tracks[0], 1, piano)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, pad)
    return tracks


if __name__ == '__main__':
    tracks = amin_and_the_eggs()
    mc.compose('amin-and-the-eggs.mid', tracks, tempo=54)

    mid = mido.MidiFile('amin-and-the-eggs.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
