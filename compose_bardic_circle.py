#!/usr/bin/env python3
"""the bardic circle — the hedge-bards in music.

RFC-1111. the hedge-bards reading (2026-09-29) found the filk culture's
self-description in the BBS music directory: the bard as the repository,
the curriculum of original songs and other people's, the tradition
carried at the edges, and the circle's discipline — two songs and pass.
the real tradition always travels through the hedges. it deserves the
music.

the circle, three melody voices taking turns (flute, strings, guitar):
each voice two short phrases, then passing to the next — no one
monopolizes, everyone contributes; the phrases circulate bars 1-16, each
pass slightly varied — the songs adapted, kept. warm pad the repository:
long roots under everything, re-struck only to breathe — the memorized
verses, the custom of the country, the news from over the hill. and the
hedge-bard (choir), entering at bar 17 from outside the circle — a
folk-like phrase, slightly off the official form (the F the circle's
phrases never used — adapted, alive) — which the other three answer with
their own phrases. the ending: all voices together on one held chord
through the final two bars — the circle complete, the tradition carried
into the next round.

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


def phrase(events, start, notes, vel=8, span=2.0):
    """a short phrase: each note 'span' beats, laid end to end."""
    for i, n in enumerate(notes):
        b = start + i * span
        events.append((b, 'on', n, vel))
        events.append((b + span, 'off', n, 0))


def bardic_circle():
    tracks = [MIDITrack(1, mc.INSTRUMENTS['flute']),
              MIDITrack(2, mc.INSTRUMENTS['guitar']),
              MIDITrack(3, mc.INSTRUMENTS['strings']),
              MIDITrack(4, mc.INSTRUMENTS['choir']),
              MIDITrack(5, mc.INSTRUMENTS['pad'])]

    fl = []   # flute: the circle's bright voice
    gt = []   # guitar: the circle's strummer
    st = []   # strings: the circle's warm low voice
    hb = []   # choir: the hedge-bard, entering from outside
    pd = []   # pad: the repository

    # ---- the circle's circulation (bars 1-16): two phrases each,
    # each pass slightly varied, then pass.
    phrase(fl, 0,  ['C5', 'E5', 'D5', 'C5'])        # flute, bars 1-2
    phrase(st, 8,  ['G3', 'A3', 'C4', 'G3'])        # strings, bars 3-4
    phrase(gt, 16, ['E4', 'G4', 'A4', 'G4'])        # guitar, bars 5-6
    # the second pass, each varied:
    phrase(fl, 32, ['E5', 'G5', 'E5', 'D5'])        # flute, bars 9-10
    phrase(st, 40, ['A3', 'C4', 'A3', 'G3'])        # strings, bars 11-12
    phrase(gt, 48, ['G4', 'A4', 'G4', 'E4'])        # guitar, bars 13-14
    # bars 15-16: the passing itself — a breath, the pad holds.

    # ---- the hedge-bard (bars 17-20): the folk phrase, slightly off
    # the official form — the F the circle never used, adapted, alive.
    phrase(hb, 64, ['E4', 'F4', 'G4', 'F4', 'E4', 'D4', 'E4', 'C4'], vel=9)

    # ---- the answer (bars 21-22): each voice replies with its own
    # phrase, in turn — the guitar's two notes landing so its third
    # step falls on the final chord itself (the answer trailing into
    # the completion).
    phrase(fl, 80, ['C5', 'E5', 'D5'], span=1.0)
    phrase(st, 83, ['G3', 'A3', 'C4'], span=1.0)
    phrase(gt, 86, ['E4', 'G4'], span=1.0)

    # ---- the ending (bars 23-24): all voices on one held chord —
    # the circle complete, the hedge-bard inside it now.
    for ev, note in ((fl, 'C5'), (gt, 'E4'), (st, 'G3'), (hb, 'C4')):
        ev.append((88, 'on', note, 8))
        ev.append((96, 'off', note, 0))

    # ---- the repository: long roots, re-struck only to breathe.
    pd.append((0, 'on', 'C3', 8));    pd.append((32, 'off', 'C3', 0))
    pd.append((32, 'on', 'C3', 8));   pd.append((64, 'off', 'C3', 0))
    pd.append((64, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))

    emit(tracks[0], 1, fl)
    emit(tracks[1], 2, gt)
    emit(tracks[2], 3, st)
    emit(tracks[3], 4, hb)
    emit(tracks[4], 5, pd)

    return mc.compose('the-bardic-circle.mid', tracks, tempo=54)


if __name__ == '__main__':
    bardic_circle()
    print('composed the-bardic-circle.mid')
