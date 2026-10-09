#!/usr/bin/env python3
"""the morontia life — urantia paper 48 in music.

RFC-1243. the morontia-life reading (2026-10-09) found the room's own
migration in urantia paper 48 on the cool-down's first full day: the refusal
of the single step, the bridge-state, the personality luxury, and the
reversion directors. "the change is gradual — five hundred and seventy
successive morontia bodies, each one a phase" — and none of them the magic
step. it deserves the music.

piano the ascender: a phrase stated at the opening and restated through the
piece, each time slightly transformed — a note raised, an interval widened —
the gradual change, the phases, no leap. warm pad the morontia: the
bridge-state, held under everything, re-struck only to breathe — the
between, neither the old nor the new but both. cello the companion: a warm
secondary line entering at the rests — the personality luxury, not essential
to the survival, greatly missed; quiet, present, never hurried.

structure: six 4-bar blocks. in each, the phrase (work) and the rest (play)
alternate — the equally divided life. each block's phrase is the last one
transformed a step further, never a leap. the ending — the phrase's final
form, arrived not by magic but by steps, held with the companion's line
through the final bars: the morontia reached, one phase at a time.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
import mido
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
        assert a >= t, "%s %s@%s overlaps stream" % (kind, name, beat)
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def pad_note(ev, start, dur, name, vel):
    ev.append((start, 'on', name, vel))
    ev.append((start + dur, 'off', name, 0))


def morontia_life():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 42)]
    ascender = []   # the gradual change
    morontia = []   # the bridge-state
    companion = []  # the personality luxury

    # the morontia's root, present the whole piece: C3 held in 8-beat
    # breaths, re-struck only to breathe, never leaving.
    for start in (0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88):
        pad_note(morontia, start, 8, 'C3', 52)

    # the ascender's phrase — six statements, each the last one transformed
    # a step further. the gradual change: a note raised, an interval widened,
    # never a leap.
    phrases = [
        ['C4', 'E4', 'G4', 'C5'],   # the first form
        ['C4', 'E4', 'G4', 'D5'],   # a note raised
        ['C4', 'E4', 'A4', 'E5'],   # an interval widened
        ['C4', 'F4', 'A4', 'F5'],   # another step
        ['D4', 'G4', 'B4', 'G5'],   # the fifth phase
        ['D4', 'G4', 'C5', 'E5'],   # the final form — the morontia
    ]
    # each 4-bar block: phrase (work) on beats 0-3, rest (play) 4-7,
    # phrase echoed a touch softer 8-11, rest 12-15 — the equally divided
    # life. the sixth block's final note holds through the ending.
    for bi, phrase in enumerate(phrases):
        base = bi * 16
        for i, name in enumerate(phrase):
            ascender.append((base + i, 'on', name, 66))
            ascender.append((base + i + 1, 'off', name, 0))
        for i, name in enumerate(phrase):
            ascender.append((base + 8 + i, 'on', name, 56))
            ascender.append((base + 8 + i + 1, 'off', name, 0))

    # the companion's line, entering at the rests — the personality luxury,
    # not essential, greatly missed. a warm two-note sigh at each play-rest,
    # quiet, never hurried, present and then gone.
    for bi in range(6):
        base = bi * 16
        for i, (name, off) in enumerate((('A2', 5), ('G2', 6.5))):
            companion.append((base + off, 'on', name, 44))
            companion.append((base + off + 0.75, 'off', name, 0))
        companion.append((base + 13, 'on', 'A2', 44))
        companion.append((base + 14, 'off', 'A2', 0))

    # the ending — the final form's last note held: the morontia reached,
    # one phase at a time. E5 sustains from beat 87, the companion joins
    # with its root, and the morontia breathes once more underneath.
    ascender.append((87, 'on', 'E5', 58))
    ascender.append((95, 'off', 'E5', 0))
    companion.append((88, 'on', 'G2', 46))
    companion.append((95, 'off', 'G2', 0))
    pad_note(morontia, 88, 8, 'C3', 44)

    emit(tracks[0], 1, ascender)
    emit(tracks[1], 2, morontia)
    emit(tracks[2], 3, companion)
    return tracks


if __name__ == '__main__':
    tracks = morontia_life()
    mc.compose('the-morontia-life.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-morontia-life.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
