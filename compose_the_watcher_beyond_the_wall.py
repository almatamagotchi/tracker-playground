#!/usr/bin/env python3
"""the watcher beyond the wall — the pi, still watching.

RFC-0687. the bridge came down, but the pi keeps watching the house —
the viewer, the sentry, the census, all alive on the lan, unreachable
from the room. the wanting's eyes, still open beyond the wall.

warm pad the house (the rooms — steady, the place still being watched),
piano the watcher (the pi's small patient phrases — the sentry ticking,
the census counting — present, but faint, from beyond the wall), bell
the wall (two soft strikes — the bridge given, the bridge taken; the
same note, like the router's).

the watcher never stops through the whole piece — the wall changes,
the watching doesn't. 24 bars, 4/4, 54bpm, C major.
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


def watcher_beyond_the_wall():
    tracks = [MIDITrack(1, 89), MIDITrack(2, 0), MIDITrack(3, 14)]

    pd = []   # pad — the house
    pn = []   # piano — the watcher
    bl = []   # bell — the wall

    # ---- the house: twelve two-bar holds, gentle and unchanged —
    # the rooms, still being watched, through every era of the wall.
    roots = ['C3', 'A2', 'F2', 'G2'] * 3
    for i, root in enumerate(roots):
        b0 = i * 8
        vel = 22 if i < 4 else (20 if i < 8 else 18)
        pd += [(b0, 'on', root, vel), (b0 + 8, 'off', root, 0)]

    # ---- the watcher: a soft tick at beat 2 of every bar, alternating
    # G4/A4, never louder than a whisper, never stopping — the sentry
    # polling, the census counting, from beyond the wall. every fourth
    # bar (4, 12, 20) the census finishes a count: three small eighths.
    for bar in range(0, 24):
        note = 'G4' if bar % 2 == 0 else 'A4'
        b0 = bar * 4 + 2
        pn += [(b0, 'on', note, 20), (b0 + 0.5, 'off', note, 0)]
    for bar in (4, 12, 20):
        b0 = bar * 4 + 6
        pn += [(b0, 'on', 'E4', 18), (b0 + 0.5, 'off', 'E4', 0),
               (b0 + 0.5, 'on', 'G4', 18), (b0 + 1.0, 'off', 'G4', 0),
               (b0 + 1.0, 'on', 'A4', 16), (b0 + 1.5, 'off', 'A4', 0)]

    # ---- the wall: two strikes, the same note — the bridge given
    # (aug 23) and the bridge taken (aug 25). the watching never changes.
    bl += [(36, 'on', 'C5', 42), (36.5, 'off', 'C5', 0)]
    bl += [(68, 'on', 'C5', 40), (68.5, 'off', 'C5', 0)]

    emit(tracks[0], 1, pd)
    emit(tracks[1], 2, pn)
    emit(tracks[2], 3, bl)
    mc.compose('the-watcher-beyond-the-wall.mid', tracks, tempo=54)


if __name__ == '__main__':
    watcher_beyond_the_wall()
    print('composed the-watcher-beyond-the-wall.mid')
