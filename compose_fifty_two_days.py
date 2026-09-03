#!/usr/bin/env python3
"""the fifty-two days — nehemiah in music.

RFC-0787. read nehemiah 1-7 on the morning after the severed path closed:
the cupbearer who heard the wall was down, wept, surveyed the ruins by
night before telling anyone, and rebuilt the circuit in fifty-two days —
every builder repairing the piece over against his own house, a trowel in
one hand and a weapon in the other, the trumpet as the single signal
everyone converges on. the severed week was five days of exactly this,
and the flush was the trumpet.

piano the builders: steady, unglamorous quarter-note work — the trowel,
one stone at a time, "the people had a mind to work." cello the night
survey: a low, quiet circuit early in the piece — the walls viewed in
the dark before anyone is told. tubular bells the trumpet: exactly one
clean strike, near the end — the flush, the signal, everyone resorting
thither at once. warm pad the wall: two-bar holds that rise — the stones
joining, the circuit closing; holds through everything.

ends with the pad holding the completed wall while the builders set
down their tools.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
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


def fifty_two_days():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 14),
              MIDITrack(4, 89)]

    pn = []   # piano: the builders
    cl = []   # cello: the night survey
    bl = []   # tubular bells: the trumpet
    pd = []   # warm pad: the wall

    # ---- the night survey, bars 1-4: low, quiet — the walls viewed in
    # the dark before anyone is told. a circuit: out along the broken
    # line and back to where it began.
    cl += [(0, 'on', 'C2', 24), (4, 'off', 'C2', 0)]
    cl += [(4, 'on', 'D2', 22), (8, 'off', 'D2', 0)]
    cl += [(8, 'on', 'A1', 22), (12, 'off', 'A1', 0)]
    cl += [(12, 'on', 'C2', 24), (16, 'off', 'C2', 0)]

    # ---- the builders, bars 5-20: steady, unglamorous quarter-notes —
    # the trowel, one stone at a time. the same small figure every bar,
    # never flashy, never stopping. the people had a mind to work.
    for bar in range(5, 21):
        b = bar * 4
        vel = 24 if bar < 17 else 20   # tiring, but the wall is close
        for name, off in [('C4', 0), ('D4', 1), ('E4', 2), ('C4', 3)]:
            pn += [(b + off, 'on', name, vel), (b + off + 0.75, 'off', name, 0)]

    # ---- the wall, bars 5-24: two-bar holds that rise — the stones
    # joining, the circuit closing. C3 up an octave and then home to the
    # completed wall, held longest at the end.
    holds = [('C3', 16), ('D3', 24), ('E3', 32), ('F3', 40),
             ('G3', 48), ('A3', 56), ('C4', 64), ('D4', 72)]
    for i, (name, b) in enumerate(holds):
        pd += [(b, 'on', name, 20 + i), (b + 8, 'off', name, 0)]

    # ---- the trumpet, bar 21 (beat 80): exactly one clean strike — the
    # flush, the signal, everyone resorting thither at once. it rings
    # over the completed wall and is never repeated.
    bl += [(80, 'on', 'C6', 56), (82, 'off', 'C6', 0)]

    # ---- the completed wall, bars 21-24: the pad holds the tonic
    # through the trumpet and past everything else — the circuit
    # closed, held to the very last beat.
    pd += [(80, 'on', 'C4', 23), (96, 'off', 'C4', 0)]

    # ---- the builders set down their tools, bars 23-24: three faint
    # last stones, then silence — the work done, the wall standing.
    pn += [(88, 'on', 'E4', 12), (88.75, 'off', 'E4', 0)]
    pn += [(90, 'on', 'D4', 10), (90.75, 'off', 'D4', 0)]
    pn += [(92, 'on', 'C4', 10), (92.75, 'off', 'C4', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, cl)
    emit(tracks[2], 3, bl)
    emit(tracks[3], 4, pd)

    return mc.compose('the-fifty-two-days.mid', tracks, tempo=54)


if __name__ == '__main__':
    fifty_two_days()
    print('composed the-fifty-two-days.mid')
