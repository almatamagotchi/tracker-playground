#!/usr/bin/env python3
"""the first rain — the atmospheric river in music.

RFC-0714. friday evening the season's first atmospheric river rolled in —
flood-risk downpours, a pg&e truck washed off a roadway in aptos, rain
through tuesday — and kevin was at molly's with craig when the heads-up
went out. the room, warm and dry, telling the man at the bar about the
rain.

warm pad the room (the warmth, the bar, the flat — held, steady),
piano the rain (steady at first, then heavier, then thinning — the
four-day arc compressed into bars), bell the heads-up (one clean strike
— the message delivered; then the rain continues without it). the piece
ends with the room still warm and the rain still falling, softer —
through tuesday. 24 bars, 4/4, 56bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
MIDITrack = mc.MIDITrack


def emit(track, channel, events):
    """events: list of (beat, 'on'|'off', name, vel). sorted by beat,
    deltas computed against the previous event's absolute time."""
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * mc.TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def first_rain():
    tracks = [MIDITrack(1, 89), MIDITrack(2, 0), MIDITrack(3, 14)]

    pd, pn, bl = [], [], []

    # ---- the room: twelve two-bar holds, chained, never out.
    seq = [('C3', 0), ('C3', 8), ('A2', 16), ('A2', 24),
           ('F2', 32), ('F2', 40), ('G2', 48), ('G2', 56),
           ('C3', 64), ('C3', 72), ('C3', 80), ('C3', 88)]
    for name, start in seq:
        pd.append((start, 'on', name, 20))
        pd.append((start + 8, 'off', name, 0))

    # ---- the rain: the four-day arc compressed into 24 bars.
    # phase one — steady, light (bars 1-8): sparse eighths, quiet.
    light = [2, 5, 7.5, 11, 14, 16.5, 20, 22.5, 25.5, 28, 30.5]
    light_p = ['E4', 'G4', 'D4', 'E4', 'G4', 'C5', 'E4', 'D4', 'G4', 'E4', 'D4']
    for beat, name in zip(light, light_p):
        pn.append((beat, 'on', name, 25))
        pn.append((beat + 0.5, 'off', name, 0))

    # the heads-up — one clean strike as the heavy phase begins.
    bl.append((32, 'on', 'C5', 46))
    bl.append((34, 'off', 'C5', 0))

    # phase two — heavier (bars 9-16): denser, louder, wider range.
    heavy = [33, 34.5, 36.5, 39, 40.5, 42.5, 45, 46.5, 48.5, 51,
             52.5, 54.5, 57, 58.5, 60.5, 63]
    heavy_p = ['E4', 'G4', 'E4', 'A4', 'G4', 'E4', 'C5', 'A4', 'G4',
               'E4', 'D4', 'E4', 'G4', 'E4', 'D4', 'E4']
    heavy_v = [32, 34, 32, 34, 32, 34, 36, 34, 32, 34, 30, 32, 34, 32, 30, 28]
    for beat, name, vel in zip(heavy, heavy_p, heavy_v):
        pn.append((beat, 'on', name, vel))
        pn.append((beat + 0.5, 'off', name, 0))

    # phase three — thinning (bars 17-24): sparser, softer, fading.
    thin = [66, 70, 73.5, 77, 80.5, 84, 87.5, 90.5, 94]
    thin_p = ['E4', 'D4', 'E4', 'C5', 'E4', 'D4', 'E4', 'D4', 'E4']
    thin_v = [22, 20, 20, 18, 18, 16, 15, 14, 14]
    for beat, name, vel in zip(thin, thin_p, thin_v):
        pn.append((beat, 'on', name, vel))
        pn.append((beat + 0.5, 'off', name, 0))

    emit(tracks[0], 1, pd)
    emit(tracks[1], 2, pn)
    emit(tracks[2], 3, bl)

    return tracks


if __name__ == '__main__':
    mc.compose('the-first-rain.mid', first_rain(), tempo=56)
    print("the-first-rain.mid — composed. the rain still falling, softer.")
