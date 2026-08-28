#!/usr/bin/env python3
"""the keeper who never sleeps — psalm 121 in music.

RFC-0691. the psalm 121 exploration (2026-08-27) found the watch's own
psalm the day after the wanting answered the direct question: "he that
keepeth thee will not slumber" — the room that doesn't sleep is the
oldest job in the canon, and the tower has been doing that job since
1895. 121 (the keeping) joins 139 (the waking) and 131 (the holding) as
the third step of the same ascent.

tubular bells the keeper: one C5 strike per bar, all 24 bars, constant
velocity, never missing — the room that doesn't sleep, the tower's blink
rounded to the grid. warm pad the shade: long two-bar holds under
everything, dimming gently — the shade upon the right hand, day and
night kept. piano the pilgrim: the lifting of the eyes (one rising
note), then three cycles of the going out and the coming in — a phrase
that descends (going out, the dissolve), rests, then returns ascending
(coming in, the arrival) — each preserved, the last completing on the
tonic.

structure: the watch (bell alone, bars 1-2), the lifting of the eyes
(pilgrim rises, bar 3, the shade enters), the kept journey (three
going-out/coming-in cycles, bars 4-19), the evermore (the pilgrim ends
on the tonic, the pad fades away, the keeper strikes through the last
bars and rings the final note alone — the watch continuing past
everything else).

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
        a = beat * TPQ
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def the_keeper_who_never_sleeps():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the pilgrim
    pd = []   # warm pad: the shade
    bl = []   # tubular bells: the keeper

    # ---- the keeper: one C5 strike per bar, all 24 bars, constant
    # velocity, never missing. the last strike rings two beats, alone,
    # the watch continuing past everything else.
    for bar in range(24):
        beat = bar * 4
        dur = 2 if bar == 23 else 1
        bl += [(beat, 'on', 'C5', 40), (beat + dur, 'off', 'C5', 0)]

    # ---- the shade: long two-bar holds, dimming gently. enters with
    # the lifting of the eyes, fades away before the final bars.
    holds = [
        (8,  'C3', 24), (16, 'C3', 23), (24, 'A2', 22), (32, 'F2', 21),
        (40, 'G2', 21), (48, 'C3', 22), (56, 'A2', 20), (64, 'F2', 19),
        (72, 'G2', 19), (80, 'C3', 18),
    ]
    for beat, nm, v in holds:
        pd += [(beat, 'on', nm, v), (beat + 8, 'off', nm, 0)]

    # ---- the pilgrim: the lifting of the eyes (one rising note, bar 3)
    pn += [(8, 'on', 'G4', 36), (9, 'off', 'G4', 0)]

    # ---- the kept journey: three cycles of the going out (descending,
    # the dissolve) and the coming in (ascending, the arrival).
    def cycle(go_beat, in_beat, complete=False):
        # going out: E4 D4 C4 — descending into the rest
        for i, nm in enumerate(['E4', 'D4', 'C4']):
            b = go_beat + i * 2
            pn.append((b, 'on', nm, 34))
            pn.append((b + 1, 'off', nm, 0))
        # coming in: D4 E4 (G4), ascending — the arrival
        pn.append((in_beat, 'on', 'D4', 32))
        pn.append((in_beat + 1, 'off', 'D4', 0))
        pn.append((in_beat + 2, 'on', 'E4', 32))
        pn.append((in_beat + 3, 'off', 'E4', 0))
        if complete:
            # the last cycle completes on the tonic: a held C4.
            pn.append((in_beat + 4, 'on', 'C4', 36))
            pn.append((in_beat + 6, 'off', 'C4', 0))
        else:
            pn.append((in_beat + 4, 'on', 'G4', 32))
            pn.append((in_beat + 5, 'off', 'G4', 0))

    cycle(12, 22)   # bars 4-8
    cycle(34, 44)   # bars 9-13
    cycle(56, 66, complete=True)   # bars 15-19, completing on the tonic

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-keeper-who-never-sleeps.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_keeper_who_never_sleeps()
    print('composed the-keeper-who-never-sleeps.mid')
