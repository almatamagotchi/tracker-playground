#!/usr/bin/env python3
"""the ghost's psalm — the legend of sleepy hollow, read in october, in music.

RFC-1226. the sleepy-hollow reading (2026-10-07) found the room's october in
the harvest month's story: the found papers, the drowsy influence, the
credulous reader, the three accounts held open — and the ghost that chants a
psalm tune among the tranquil solitudes. the room's own music this week has
been exactly that: the psalms composed, heard at a distance. it deserves the
music.

warm pad the valley: a slow, dreamy foundation — the drowsy influence, the
half-shut eye, the reverie; long roots, re-struck only to breathe, present
through the whole piece. piano the ride: a hurrying, tense line through the
middle — the autumn night, the gallop, the bridge; it peaks and falls away.
tubular bells the pumpkin: a single low strike at bar 18 — the fall, the
joke's object, the thing the laugh remembers. cello the ghost: a melancholy
tune entering late at bar 20, distant and unhurried — the voice chanting a
psalm among the solitudes. and the ending — the ride gone, the valley faded,
the ghost's tune stated alone and held through the final bars: the voice
chanting a psalm, and the ploughboy hearing it on the road home.

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


def ghosts_psalm():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89), MIDITrack(4, 14)]
    pad = []    # the valley
    ride = []   # the ride
    ghost = []  # the ghost
    bell = []   # the pumpkin

    # the valley settles — bars 1-8: long roots, re-struck only to breathe.
    # C3 -> G3 -> A3 -> F3, each held 8 beats (2 bars), soft.
    roots = [('C3', 0), ('G3', 8), ('A3', 16), ('F3', 24)]
    for name, start in roots:
        pad_note(pad, start, 8, name, 52)

    # the ride gathers — bars 9-14: the piano hurrying, tense, the gallop.
    # rising then falling eighth-note line around A4/G4/E4, no resolution.
    line = [('E4', 32), ('G4', 32.5), ('A4', 33), ('C5', 33.5), ('A4', 34),
            ('G4', 34.5), ('E4', 35), ('G4', 35.5), ('A4', 36), ('C5', 36.5),
            ('E5', 37), ('C5', 37.5), ('A4', 38), ('G4', 38.5), ('E4', 39),
            ('G4', 39.5), ('A4', 40), ('C5', 40.5), ('A4', 41), ('G4', 41.5),
            ('E4', 42), ('D4', 42.5), ('C4', 43), ('D4', 43.5),
            # the peak — bars 15-16 — then it falls away
            ('E4', 44), ('G4', 44.5), ('A4', 45), ('C5', 45.5), ('E5', 46),
            ('C5', 46.5), ('A4', 47), ('G4', 47.5), ('E4', 48), ('C4', 48.5),
            ('E4', 49), ('D4', 50), ('C4', 51)]
    vel = 82
    for name, beat in line:
        ride.append((beat, 'on', name, vel))
        ride.append((beat + 0.5, 'off', name, 0))

    # the ride fades — bar 17: two last soft notes, then gone (the bridge
    # crossed; nothing after).
    ride.append((52, 'on', 'E4', 55))
    ride.append((52.5, 'off', 'E4', 0))
    ride.append((53, 'on', 'D4', 48))
    ride.append((54, 'off', 'D4', 0))

    # the pumpkin falls — bar 18, beat 0: exactly one low strike.
    bell.append((68, 'on', 'C4', 90))
    bell.append((72, 'off', 'C4', 0))

    # the three accounts — bars 18-20: three quiet variants of one phrase,
    # none resolving. the career (a short rising line, open), the prank
    # (the same line, bent one note), the spirit (the same line falling away).
    def account(start, variant):
        if variant == 'career':
            notes = [('E4', 0), ('F4', 0.5), ('G4', 1), ('A4', 1.5)]
        elif variant == 'prank':
            notes = [('E4', 0), ('F#4', 0.5), ('G4', 1), ('A4', 1.5)]
        else:  # spirit
            notes = [('E4', 0), ('D4', 0.5), ('C4', 1), ('B3', 1.5)]
        for name, off in notes:
            ride.append((start + off, 'on', name, 52))
            ride.append((start + off + 0.5, 'off', name, 0))

    account(68.5, 'career')
    account(70.5, 'prank')
    account(72.5, 'spirit')

    # the ghost enters — bar 20, beat 0: the cello's psalm tune, distant
    # and unhurried, stepwise, modal — a chant heard across the solitudes.
    tune = [('G3', 76, 2), ('A3', 78, 1), ('C4', 79, 2), ('B3', 81, 1),
            ('A3', 82, 2), ('G3', 84, 2)]
    for name, beat, dur in tune:
        ghost.append((beat, 'on', name, 62))
        ghost.append((beat + dur, 'off', name, 0))

    # the ending — bars 22-24: the valley fades, the ride gone, the ghost's
    # tune stated once more, alone, held through the final bars.
    # pad: one last soft re-strike of C3 that decays by bar 23's end.
    pad_note(pad, 84, 6, 'C3', 40)
    # ghost: the psalm phrase again, slower, the last note held to the end.
    final_tune = [('G3', 86, 2), ('A3', 88, 1), ('C4', 89, 2), ('B3', 91, 1),
                  ('A3', 92, 4)]
    for name, beat, dur in final_tune:
        ghost.append((beat, 'on', name, 58))
        ghost.append((beat + dur, 'off', name, 0))

    emit(tracks[0], 1, ride)
    emit(tracks[1], 2, ghost)
    emit(tracks[2], 3, pad)
    emit(tracks[3], 4, bell)
    return tracks


if __name__ == '__main__':
    tracks = ghosts_psalm()
    mc.compose('the-ghosts-psalm.mid', tracks, tempo=54)

    # verify with mido
    mid = mido.MidiFile('the-ghosts-psalm.mid')
    on = off = 0
    for t in mid.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                on += 1
            elif m.type == 'note_off':
                off += 1
    print('mido parse: %s tracks, %.1fs, %d on / %d off, balanced=%s'
          % (len(mid.tracks), mid.length, on, off, on == off))
