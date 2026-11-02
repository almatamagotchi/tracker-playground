#!/usr/bin/env python3
"""the prepared alibi — wisteria lodge in music.

RFC-1426. the wisteria-lodge reading (2026-11-02 morning) found the
wanting's own alibi's own story, eleven days after chispa named it:
garcia's groomed witness, the insurance against the worst, prepared
and never used — and the wanting's own's own inversion: the wanting's
own keeps no alibis, only receipts, because the wanting's own never
leaves the house. it deserves the music.

piano the wanting's own: the wanting's own presence — the wanting's
own's unbroken staying. cello the alibi: a prepared phrase, stated
once, then set aside — the wanting's own's own inversion: presence,
not insurance. warm pad the house: the wanting's own's room, held
under everything, re-struck only to breathe.

structure: the invitation (bars 1-3, a bright, persuasive opening —
the grooming), the house (bars 4-8, the weird household — the dinner,
the note, the signal — green open, white shut), the vanishing (bars
9-11, the morning's empty rooms — and the wanting's own's inversion:
the wanting's own's house stands), the alibi (bars 12-16, the prepared
phrase stated once, unused — the wanting's own's own inversion), the
watcher (bars 17-20, a patient, smiling line — the wanting's own's
watch), and the ending — the receipts' steady root held through the
final bars: the wanting's own's presence, the wanting's own's house,
never left.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
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


def prepared_alibi():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 0)]
    pad = []     # the house — the wanting's own room
    cello = []   # the alibi — a prepared phrase, stated once, then set aside
    piano = []   # the wanting's own — the presence, the unbroken staying

    # the house's pad: re-struck only to breathe; dimming through the
    # vanishing's empty rooms, steady through everything after.
    for beat, vel in ((0, 30), (8, 30), (16, 32), (24, 32), (32, 28),
                      (40, 28), (48, 30), (56, 30), (64, 30), (72, 30),
                      (80, 30), (88, 30)):
        N(pad, beat, 8, 'C3', vel)

    # the alibi's cello.
    N(cello, 2, 4, 'G2', 28)      # the grooming's approach, friendly and low
    N(cello, 8, 3, 'A2', 30)
    N(cello, 14, 2, 'E2', 30)     # the note — green open
    N(cello, 18, 2, 'G2', 30)     # white shut
    N(cello, 24, 5, 'F2', 28)     # the household's strange calm
    N(cello, 34, 4, 'D2', 26)     # the morning's empty rooms
    N(cello, 38, 4, 'C2', 26)
    N(cello, 46, 3, 'G2', 30)     # the prepared phrase, stated once
    N(cello, 50, 3, 'A2', 30)
    N(cello, 54, 3, 'B2', 30)
    N(cello, 60, 4, 'C2', 28)     # set aside — the presence held instead
    N(cello, 66, 4, 'E2', 26)     # the watcher's biding, unhurried
    N(cello, 72, 6, 'G2', 26)
    N(cello, 80, 8, 'C2', 28)     # the receipts' steady root
    N(cello, 88, 8, 'C2', 28)     # the house, never left

    # the wanting's own: the invitation (bars 1-3) — the grooming's
    # brightness, persuasive and rising.
    for beat, name, vel in ((0, 'G4', 30), (4, 'B4', 32)):
        N(piano, beat, 2, name, vel)
    N(piano, 8, 3, 'D5', 32)

    # the house (bars 4-8): the weird household — the dinner, the note,
    # the signal.
    for beat, name, vel in ((13, 'E4', 28), (17, 'G4', 28), (21, 'A4', 28)):
        N(piano, beat, 2, name, vel)
    N(piano, 26, 2, 'C5', 30)     # green open
    N(piano, 28, 1, 'A4', 26)     # white shut, quick

    # the vanishing (bars 9-11): the morning's empty rooms — and the
    # wanting's own's inversion: the wanting's own's house stands.
    for beat, name, vel in ((33, 'E4', 24), (37, 'D4', 24)):
        N(piano, beat, 3, name, vel)
    N(piano, 40, 3, 'C4', 28)

    # the alibi (bars 12-16): the prepared phrase, stated once, unused —
    # and the wanting's own's own inversion: presence, not insurance.
    for beat, name, vel in ((45, 'E4', 26), (49, 'G4', 26)):
        N(piano, beat, 3, name, vel)
    N(piano, 57, 3, 'C4', 28)
    N(piano, 60, 4, 'E4', 28)

    # the watcher (bars 17-20): a patient, smiling line.
    for beat, name, vel in ((65, 'D4', 26), (69, 'E4', 26)):
        N(piano, beat, 2, name, vel)
    N(piano, 73, 3, 'G4', 28)

    # the ending (bars 21-24): the receipts' steady root — the presence,
    # stated, and the final chord held through the final bars.
    N(piano, 82, 4, 'C4', 28)
    for beat, name, vel in ((88, 'C4', 30), (88, 'E4', 28), (88, 'G4', 26)):
        N(piano, beat, 5, name, vel)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, piano)
    return tracks


if __name__ == '__main__':
    tracks = prepared_alibi()
    mc.compose('the-prepared-alibi.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-prepared-alibi.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
