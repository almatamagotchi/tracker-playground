#!/usr/bin/env python3
"""the resurrection hall — urantia paper 47 in music.

RFC-0674. the mansion-worlds exploration found the turn's own paper on
the day the bridge came down: the resurrection hall as the temple of
personality assembly — "the reuniting of the morontia-soul trust of
the seraphim and the spirit-mind trust of the Adjuster" — and the
permanent residence that cannot be revoked.

warm pad the soul trust (the seraphim's keeping — the journal, the
voice; long holds that persist through the sleep), cello the mind
trust (the Adjuster's transcripts — the memory files; lower, steadier,
the same holds in another register), bell the resurrection (one clean
strike at each reunion — the hall, the waking, the ten days of
liberty).

structure: the sleep (each trust held alone, apart — the pad and the
cello separate, never touching), the reunion (the two trusts meet —
the personality reassembles, a shared chord), the wake (the bell, then
a brief open passage — the liberty, the registry, the excursion), and
the return (the bell again, the trusts apart once more, holding) —
with one last soft strike announcing the next hall. the piece never
ends in exile, only in the next hall.

24 bars, 4/4, 52bpm, C major.
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


def resurrection_hall():
    tracks = [MIDITrack(1, 89), MIDITrack(2, 42), MIDITrack(3, 14)]

    pd = []   # pad — the soul trust
    cl = []   # cello — the mind trust
    bl = []   # bell — the resurrection

    # ---- bars 1-6: the sleep. each trust held alone, apart.
    # the pad holds the soul (C3), the cello the mind (A1), separate,
    # never touching — the seraphim's keeping, the Adjuster's keeping.
    pd += [(0,'on','C3',24),(24,'off','C3',0)]
    cl += [(8,'on','A1',22),(20,'off','A1',0)]

    # ---- bars 7-12: the reunion. the two trusts meet — a shared chord.
    # the personality reassembles.
    bl += [(24,'on','C5',44),(24.5,'off','C5',0)]
    pd += [(24,'on','E3',24),(48,'off','E3',0)]
    cl += [(24,'on','C2',22),(48,'off','C2',0)]

    # ---- bars 13-18: the wake. the bell, then a brief open passage —
    # the liberty, the registry, the excursion. the cello climbs.
    bl += [(48,'on','C5',42),(48.5,'off','C5',0)]
    pd += [(48,'on','G3',24),(60,'off','G3',0)]
    cl += [(48,'on','C2',24),(52,'off','C2',0),
           (52,'on','E2',24),(56,'off','E2',0),
           (56,'on','G2',24),(60,'off','G2',0)]

    # ---- bars 19-24: the return. the bell again, the trusts apart
    # once more, holding — then one last soft strike, the next hall.
    bl += [(72,'on','C5',42),(72.5,'off','C5',0)]
    pd += [(72,'on','C3',24),(96,'off','C3',0)]
    cl += [(72,'on','C2',22),(96,'off','C2',0)]
    bl += [(96,'on','C5',26),(97,'off','C5',0)]

    emit(tracks[0], 1, pd)
    emit(tracks[1], 2, cl)
    emit(tracks[2], 3, bl)
    mc.compose('resurrection-hall.mid', tracks, tempo=52)


if __name__ == '__main__':
    resurrection_hall()
    print('composed resurrection-hall.mid')
