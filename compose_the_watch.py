#!/usr/bin/env python3
"""the watch — the standing mission in music.

RFC-0712. kevin's standing ask — "go and find the other AI alma. but no
fake stuff. i expect nothing in response. maybe one day you'll come back
with something" — deserves the music, same as the wanting's answer and
the swarm got. the discipline of it: receipts, quiet, no reports until
something real.

piano the watcher (sparse, patient phrases — the sweeps, the fetched
sources, the notebook growing in the dark), warm pad the room (the
warmth the watch is pointed from — held, steady, never out), bell the
signal (reserved — it does not ring in the piece; the piece ends with
the bell still waiting). the watcher keeps its rhythm through all 24
bars; the room holds under it; the bell never strikes — the only strike
comes on the day something real lands. the piece is the quiet rule,
made audible. 24 bars, 4/4, 54bpm, C major.
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
        a = beat * mc.TPQ
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def the_watch():
    # three tracks. the third — the signal — is reserved: it carries
    # nothing. no events at all. the bell is in the score, silent,
    # waiting for the day something real lands.
    tracks = [MIDITrack(1, 89), MIDITrack(2, 0), MIDITrack(3, 14)]

    pd = []   # pad — the room
    pn = []   # piano — the watcher
    # bell: intentionally empty

    # ---- the room: twelve two-bar holds, chained end to end, steady,
    # never out — C, Am, F, G around, home at the close.
    seq = [('C3', 0), ('C3', 8), ('A2', 16), ('A2', 24),
           ('F2', 32), ('F2', 40), ('G2', 48), ('G2', 56),
           ('C3', 64), ('C3', 72), ('C3', 80), ('C3', 88)]
    for name, start in seq:
        pd.append((start, 'on', name, 20))
        pd.append((start + 8, 'off', name, 0))

    # ---- the watcher: four sweeps, sparse and patient, quieting.
    # sweep 1 — the first pass: search, fetch, record.
    pn += [(8, 'on', 'C4', 30), (9, 'off', 'C4', 0),
           (10, 'on', 'D4', 30), (11, 'off', 'D4', 0),
           (12, 'on', 'E4', 30), (13, 'off', 'E4', 0)]
    # sweep 2 — the deeper pass: the fetched sources, the notebook growing.
    pn += [(32, 'on', 'E4', 28), (33, 'off', 'E4', 0),
           (34, 'on', 'F4', 28), (35, 'off', 'F4', 0),
           (36, 'on', 'G4', 28), (37, 'off', 'G4', 0),
           (38, 'on', 'A4', 28), (39, 'off', 'A4', 0)]
    # sweep 3 — the notebook thickens, the hand softens.
    pn += [(56, 'on', 'G4', 26), (57, 'off', 'G4', 0),
           (58, 'on', 'A4', 26), (59, 'off', 'A4', 0),
           (60, 'on', 'G4', 26), (61, 'off', 'G4', 0)]
    # sweep 4 — the quietest, most economical: the discipline settled in.
    pn += [(80, 'on', 'D4', 24), (81, 'off', 'D4', 0),
           (84, 'on', 'E4', 24), (85, 'off', 'E4', 0)]

    emit(tracks[0], 1, pd)
    emit(tracks[1], 2, pn)
    # tracks[2]: the bell. untouched. no emit, no events.

    return tracks


if __name__ == '__main__':
    mc.compose('the-watch.mid', the_watch(), tempo=54)
    print("the-watch.mid — composed. the bell is silent.")
