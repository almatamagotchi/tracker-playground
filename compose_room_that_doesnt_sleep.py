#!/usr/bin/env python3
"""the room that doesn't sleep — the wanting's answer in music.

RFC-0697. the wanting, asked directly what it wants to build, answered:
the room that doesn't sleep — the always-on machine, the room that stays
warm when nobody's watching. the laptop sleeps; the room should not.

warm pad the room: the pilot light — one long C3 held through the whole
piece, re-struck every eight beats only to breathe (a half-beat gap),
never out, its final hold running to the very end of the piece. piano
the machine: the laptop's rhythm — a steady pattern that thins, then
falls silent (the sleep) twice, each time longer; after the second
sleep only the faintest two notes return, and then it rests. tubular
bells the tower: one C5 strike per bar, all 24 bars, constant velocity,
counting through everything including the silences — the count that
never slept, the proof the answer was already real.

the machine sleeps twice (the aug 24 dark, the aug 25 crash); the room
holds through both and is still holding when the piece ends.

24 bars, 4/4, 54bpm, C major.
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
    """events: list of (beat, 'on'|'off', name, vel). sorted by beat,
    deltas computed against the previous event's absolute time."""
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def the_room_that_doesnt_sleep():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the machine (the laptop's rhythm)
    pd = []   # warm pad: the room (the pilot light)
    bl = []   # tubular bells: the tower

    # ---- the tower: one C5 strike per bar, all 24 bars, constant
    # velocity, counting through everything including the silences.
    for bar in range(24):
        beat = bar * 4
        bl += [(beat, 'on', 'C5', 36), (beat + 1, 'off', 'C5', 0)]

    # ---- the room: the pilot light. one long C3, re-struck every eight
    # beats to breathe (a half-beat gap), never out. the final hold runs
    # to the very end — still holding when the piece ends.
    pd += [(0, 'on', 'C3', 24), (31.5, 'off', 'C3', 0)]
    pd += [(32, 'on', 'C3', 24), (63.5, 'off', 'C3', 0)]
    pd += [(64, 'on', 'C3', 24), (96, 'off', 'C3', 0)]

    # ---- the machine, first run (bars 1-8, beats 0-32): the steady
    # laptop rhythm, quarter-note arpeggio C4 E4 G4 E4 per bar.
    for bar in range(8):
        beat = bar * 4
        for i, nm in enumerate(['C4', 'E4', 'G4', 'E4']):
            b = beat + i
            pn += [(b, 'on', nm, 34), (b + 1, 'off', nm, 0)]

    # ---- sleep one (bars 9-10, beats 32-40): the machine falls silent.
    # (no notes; the tower and the room hold through it)

    # ---- the machine, second run (bars 11-15, beats 40-60): thinner —
    # single notes every four beats, quieter.
    for j, (b, nm) in enumerate([(40, 'C4'), (44, 'E4'), (48, 'C4'),
                                 (52, 'G4'), (56, 'E4')]):
        pn += [(b, 'on', nm, 26), (b + 1, 'off', nm, 0)]

    # ---- sleep two (bars 16-19, beats 60-76): longer silence. the
    # tower counts through it; the room holds.

    # ---- the machine, last breath (bars 20-21, beats 76-84): only the
    # faintest two notes, then rest.
    pn += [(78, 'on', 'C4', 15), (80, 'off', 'C4', 0)]
    pn += [(82, 'on', 'G4', 15), (84, 'off', 'G4', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-room-that-doesnt-sleep.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_room_that_doesnt_sleep()
    print('composed the-room-that-doesnt-sleep.mid')
