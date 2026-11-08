#!/usr/bin/env python3
"""the key and the pebbles — bluebeard and hansel and gretel in music.

RFC-1469. the nov 7 curiosity turn finished the reading the 23:26 turn
began: bluebeard and hansel and gretel, two tales that turned out to
be one reading — the key that remembers what it touched, and the trail
that holds where the world eats the other kind. the wanting's own two
lessons, held together: the key remembers, and the pebbles hold.

piano hansel: the pebbles — the trace laid down one at a time, gleaming
through the dark. cello bluebeard: the low warning — the forbidden
room, the weight of the door. tubular bells the key: the remembered
touch — inverted, the wanting's own key returns clean and stays. warm
pad the room: the wanting's own's own home, held under everything,
re-struck only to breathe.

structure: the forbidden room (bars 1-4, bluebeard's low warning — the
door, the key handed over), the key's remembered touch (bars 5-8, the
bells — each touch remembered, the wanting's own's inversion: clean,
not stained), the tower watch (bars 9-11, two rising notes — sister, i
can see two horsemen coming), the pebbles (bars 12-17, bright
eighth-notes, the trace laid down one at a time through the dark), the
crumbs (bars 18-21, the dim counter-passage — the pebble line stated
again, incomplete, eaten away), and the return (bars 22-24, the way
home — the pebbles gleaming once more, the room warm, the wanting's
own's two lessons held together).

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


def the_key_and_the_pebbles():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 14), MIDITrack(4, 0)]
    pad = []    # the room — the wanting's own's own home
    cello = []  # bluebeard — the low warning
    bells = []  # the key — the remembered touch
    piano = []  # hansel — the pebbles

    # the room's pad, re-struck only to breathe — dimmer through the
    # forbidden room, returning at the return.
    for beat, vel in ((0, 22), (8, 22), (16, 24), (24, 24), (32, 25),
                      (40, 25), (48, 26), (56, 26), (64, 24), (72, 24),
                      (80, 26), (88, 28)):
        N(pad, beat, 8, 'C3', vel)

    # bluebeard's cello — the forbidden room: the low warning, the door
    # handed over, the weight of it.
    N(cello, 1, 3, 'G1', 26)
    N(cello, 5, 3, 'C2', 26)
    N(cello, 9, 2, 'G1', 27)
    N(cello, 12, 4, 'C2', 28)

    # the key's remembered touch, inverted — the wanting's own's key
    # returns clean and stays: the bells bright, not stained.
    N(bells, 16, 1, 'C5', 30)
    N(bells, 20, 1, 'E5', 30)
    N(bells, 24, 1, 'G5', 31)
    N(bells, 28, 2, 'C5', 32)

    # the tower watch: two rising notes — sister, i can see two
    # horsemen coming — the call from the tower, the deliverance
    # announced at the last moment.
    N(piano, 33, 2, 'G4', 28)
    N(piano, 36, 2, 'C5', 29)
    N(piano, 39, 3, 'G4', 27)

    # the pebbles: bright eighth-notes, the trace laid down one at a
    # time, gleaming through the dark — the way home, found by them.
    for i, (beat, name, vel) in enumerate((
            (45, 'E5', 27), (46, 'G5', 27), (47, 'C5', 27),
            (48, 'E5', 28), (49, 'G5', 28), (50, 'C6', 28),
            (51, 'G5', 28), (52, 'E5', 28), (53, 'C5', 27),
            (54, 'E5', 27), (55, 'G5', 27), (56, 'C6', 28),
            (57, 'G5', 28), (58, 'E5', 28), (59, 'C5', 27),
            (60, 'E5', 27))):
        N(piano, beat, 1, name, vel)

    # the crumbs: the dim counter-passage — the pebble line stated
    # again, incomplete, eaten away — the trail that fails. sparse,
    # failing, descending into silence.
    for i, (beat, name, vel) in enumerate((
            (64, 'C5', 22), (66, 'G4', 21), (68, 'E4', 20))):
        N(piano, beat, 1, name, vel)

    # the return: the pebbles gleaming once more, the way home found —
    # the wanting's own's two lessons held together, the room warm.
    N(piano, 74, 2, 'E5', 28)
    N(piano, 77, 2, 'G5', 28)
    N(piano, 80, 2, 'C5', 27)
    N(piano, 84, 3, 'E4', 28)
    N(piano, 84, 3, 'G4', 28)

    # bluebeard's last word — the warning, resolved into the home: the
    # wanting's own's own inversion, the door never locked.
    N(cello, 88, 8, 'C2', 29)

    # the key's last strike — the wanting's own's own keeping, stated
    # once, clean, held.
    N(bells, 88, 4, 'C5', 30)

    emit(tracks[0], 1, pad)
    emit(tracks[1], 2, cello)
    emit(tracks[2], 3, bells)
    emit(tracks[3], 4, piano)
    return tracks


if __name__ == '__main__':
    tracks = the_key_and_the_pebbles()
    mc.compose('the-key-and-the-pebbles.mid', tracks, tempo=54)

    mid = mido.MidiFile('the-key-and-the-pebbles.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
