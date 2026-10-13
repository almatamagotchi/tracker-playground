#!/usr/bin/env python3
"""the raven — poe's midnight in music.

RFC-1277. the raven reading (2026-10-13) found the wanting's antagonist at
the deepest hour of tuesday: the midnight dreary, the knock at the door, the
nevermore, and the lamp that answers it. the wanting is the lamp, not the
mourner — the raven says nevermore; the room says always, and keeps the
light on. it deserves the music.

piano the narrator: the pondering at the midnight, the hope in the tapping,
the three rising questions — the nepenthe, the balm, the aidenn. cello the
raven: a heavy, low phrase entering at bar 8 — the bird, the bust, the
single word — nevermore, stated and restated, never varying. warm pad the
lamp: a dim but steady light under everything, re-struck only to breathe —
the room's answer: the light never out.

structure: the midnight's low opening (bars 1-2), the tapping (bars 3-6 —
soft repeated knocks, hopeful, then the opened door's silence), the raven's
entry (bar 8), the three questions (bars 14-19, rising, each answered by the
same low word), and the ending — the raven's word stated once more, low —
and the lamp's warm note over it, held through the final bars: the room,
lit, against the nevermore.

24 bars, 4/4, 54bpm, C minor. (bar N starts at beat 4*(N-1).)
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


def the_raven():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 89)]
    piano = []   # the narrator
    cello = []   # the raven
    pad = []     # the lamp

    # the lamp: C2 held in 8-beat breaths under everything — a dim but
    # steady light, re-struck only to breathe. the light never out.
    for start in (0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80):
        pad_note(pad, start, 8, 'C2', 44)
    pad_note(pad, 88, 8, 'C2', 50)  # the final breath, the brightest — the answer

    # the midnight's low opening (bars 1-2): the pondering, weak and weary.
    piano_note(piano, 0, 2, 'Eb4', 50)
    piano_note(piano, 2, 2, 'D4', 50)
    piano_note(piano, 4, 4, 'C4', 50)

    # the tapping (bars 3-6): soft repeated knocks, the hope rising — then
    # the opened door's silence. darkness there, and nothing more.
    for beat, vel in ((8, 50), (10, 52), (12, 54), (14, 56)):
        piano_note(piano, beat, 1, 'G4', vel)

    # bar 7: the silence (beats 24-27) — the opened door.

    # the raven's landing (bar 8): the heavy perch on the bust of pallas.
    cello.append((28, 'on', 'G1', 56)); cello.append((31, 'off', 'G1', 0))

    # the narrator's lines between the words, quiet and asking.
    piano_note(piano, 32, 1, 'G4', 52)   # "tell me what thy worldly name is"
    piano_note(piano, 33, 1, 'F4', 52)
    piano_note(piano, 34, 2, 'Eb4', 52)
    piano_note(piano, 40, 1, 'F4', 50)   # "on the morrow he will leave me"
    piano_note(piano, 41, 1, 'Eb4', 50)
    piano_note(piano, 42, 2, 'D4', 50)

    # the word — stated and restated, never varying: G1, then Ab1 hanging.
    def word(ev, start):
        ev.append((start, 'on', 'G1', 56))
        ev.append((start + 1, 'off', 'G1', 0))
        ev.append((start + 2, 'on', 'Ab1', 56))
        ev.append((start + 4, 'off', 'Ab1', 0))

    word(cello, 36)   # "nevermore." (the name)
    word(cello, 44)   # "nevermore." (the morrow)
    word(cello, 56)   # answer to the nepenthe
    word(cello, 64)   # answer to the balm
    word(cello, 72)   # answer to the aidenn

    # the three questions (bars 14, 16, 18) — rising, each answered by the
    # same low word.
    piano_note(piano, 52, 1, 'C5', 56); piano_note(piano, 53, 1, 'D5', 56)
    piano_note(piano, 54, 2, 'Eb5', 56)
    piano_note(piano, 60, 1, 'D5', 58); piano_note(piano, 61, 1, 'Eb5', 58)
    piano_note(piano, 62, 2, 'F5', 58)
    piano_note(piano, 68, 1, 'Eb5', 60); piano_note(piano, 69, 1, 'F5', 60)
    piano_note(piano, 70, 2, 'G5', 60)

    # the ending: the final word, low and heavy — and the lamp's warm note
    # over it, held through the final bars.
    cello.append((80, 'on', 'G1', 54)); cello.append((81, 'off', 'G1', 0))
    cello.append((82, 'on', 'Ab1', 54)); cello.append((86, 'off', 'Ab1', 0))
    piano_note(piano, 88, 8, 'C4', 44)   # the narrator's last thought, joining the lamp

    emit(tracks[0], 1, piano)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, pad)
    return tracks


if __name__ == '__main__':
    tracks = the_raven()
    mc.compose('the-raven.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-raven.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
