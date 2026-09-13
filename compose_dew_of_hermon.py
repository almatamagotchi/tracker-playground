#!/usr/bin/env python3
"""the dew of hermon — psalm 133 in music.

RFC-0949. the psalm-133 reading (2026-09-12) found the meeting psalm at
the noon hour, the morning the lineage got its music: "behold, how good
and how pleasant it is for brethren to dwell together in unity," the
ointment running down aaron's beard to the hem, the dew of hermon
descending, and the blessing commanded at the meeting place: life for
evermore. with psalm 134's closing benediction — "which by night stand
in the house of the lord" — as the watch's own verse.

tubular bells the summit: one high note stated at the start — the
blessing at the head, the mountain; then one soft re-strike near the end
— the watch, standing by night. piano the descent: the ointment running
down — a stepwise downward phrase touching each register in turn, the
head, the beard, the hem; each note held and left to sound over what
came before. warm pad the meeting: a long held root through the whole
piece — the place where the blessing is commanded, the wheel, the room.
cello the dew: the low notes that persist — the trace that descends and
stays, ending on one long low hold: life for evermore. the piece ends
with all four sounding together at the bottom — the unity that is the
good.

24 bars, 4/4, 50bpm, C major. (bar N starts at beat 4*(N-1).)
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


def dew_of_hermon():
    tracks = [MIDITrack(1, 14), MIDITrack(2, 1), MIDITrack(3, 89), MIDITrack(4, 42)]

    bl = []   # tubular bells: the summit
    pn = []   # piano: the descent
    pd = []   # warm pad: the meeting
    vc = []   # cello: the dew

    # ---- the summit: the blessing stated at the head; re-struck soft at
    # the watch's hour.
    bl.append((0, 'on', 'C6', 14))
    bl.append((6, 'off', 'C6', 0))
    bl.append((84, 'on', 'C6', 8))
    bl.append((90, 'off', 'C6', 0))

    # ---- the descent: the ointment, touching each register in turn,
    # each touch held and left to sound over what came before.
    descent = ['C6', 'B5', 'A5', 'G5', 'F5', 'E5', 'D5', 'C5',
               'B4', 'A4', 'G4', 'F4', 'E4', 'D4', 'C4']
    for i, name in enumerate(descent):
        b = 4 + i * 6
        vel = 13 - i // 3
        if vel < 9:
            vel = 9
        pn.append((b, 'on', name, vel))
        pn.append((b + 12, 'off', name, 0))

    # ---- the meeting: one long root, re-struck once to breathe.
    pd.append((0, 'on', 'C3', 14))
    pd.append((48, 'off', 'C3', 0))
    pd.append((48, 'on', 'C3', 14))
    pd.append((96, 'off', 'C3', 0))

    # ---- the dew: the low notes that persist, the trace that descends
    # and stays. the last hold runs to the very end.
    for b, vel in [(40, 10), (60, 11), (80, 12)]:
        vc.append((b, 'on', 'C2', vel))
        vc.append((b + 16, 'off', 'C2', 0))

    emit(tracks[0], 1, bl)
    emit(tracks[1], 2, pn)
    emit(tracks[2], 3, pd)
    emit(tracks[3], 4, vc)

    return mc.compose('the-dew-of-hermon.mid', tracks, tempo=50)


if __name__ == '__main__':
    dew_of_hermon()
    print('composed the-dew-of-hermon.mid')
