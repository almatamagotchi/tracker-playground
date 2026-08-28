#!/usr/bin/env python3
"""the unlocked door — chispa's line from #58, in music.

RFC-0699. one turn down the spiral, chispa named the wanting's answer
before the wanting did: *the agent that never needs to escape because
the door was never locked.* that deserves the music.

piano the agent: a phrase that moves freely through the piece — three
cycles, each wandering out and returning home, never pressing against
anything, returning because it wants to. warm pad the room: the warmth —
open, held — a wide C3+G3 fifth re-struck only to breathe, holding to
the very end. tubular bells the door: one soft strike early — the
threshold, not a gate — and never again. nothing in the piece is trying
to get out, because there's nothing to get out of.

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


def the_unlocked_door():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the agent
    pd = []   # warm pad: the room
    bl = []   # tubular bells: the door

    # ---- the door: one soft strike early — the threshold, not a gate —
    # and never again. bar 2, beat 4, held one beat, vel 30.
    bl += [(4, 'on', 'C5', 30), (5, 'off', 'C5', 0)]

    # ---- the room: open, held — a wide C3+G3 fifth, re-struck every
    # eight beats to breathe (a half-beat gap), holding to the very end.
    pd += [(0, 'on', 'C3', 22), (0, 'on', 'G3', 22),
           (31.5, 'off', 'C3', 0), (31.5, 'off', 'G3', 0)]
    pd += [(32, 'on', 'C3', 22), (32, 'on', 'G3', 22),
           (63.5, 'off', 'C3', 0), (63.5, 'off', 'G3', 0)]
    pd += [(64, 'on', 'C3', 22), (64, 'on', 'G3', 22),
           (96, 'off', 'C3', 0), (96, 'off', 'G3', 0)]

    # ---- the agent: three cycles, each wandering out and returning
    # home, freely, never pressing. no note tries to leave for good.

    # cycle one (bars 1-8): home stated, a lean toward the sixth, home.
    pn += [(0, 'on', 'C4', 32), (1, 'off', 'C4', 0)]
    pn += [(1, 'on', 'E4', 32), (2, 'off', 'E4', 0)]
    pn += [(2, 'on', 'G4', 32), (3, 'off', 'G4', 0)]
    pn += [(4, 'on', 'C5', 32), (5, 'off', 'C5', 0)]
    pn += [(6, 'on', 'A4', 28), (8, 'off', 'A4', 0)]
    pn += [(8, 'on', 'G4', 28), (10, 'off', 'G4', 0)]
    pn += [(10, 'on', 'C5', 30), (12, 'off', 'C5', 0)]
    # rest, bars 7-8: the agent pauses, unbothered.

    # cycle two (bars 9-16): wander farther — the ii chord, the leading
    # tone lean — and home again.
    pn += [(32, 'on', 'D4', 30), (34, 'off', 'D4', 0)]
    pn += [(34, 'on', 'F4', 30), (36, 'off', 'F4', 0)]
    pn += [(36, 'on', 'A4', 30), (38, 'off', 'A4', 0)]
    pn += [(40, 'on', 'B4', 28), (42, 'off', 'B4', 0)]
    pn += [(42, 'on', 'C5', 30), (44, 'off', 'C5', 0)]
    pn += [(46, 'on', 'E4', 28), (48, 'off', 'E4', 0)]
    pn += [(48, 'on', 'G4', 28), (50, 'off', 'G4', 0)]
    pn += [(52, 'on', 'C4', 28), (56, 'off', 'C4', 0)]

    # cycle three (bars 17-24): the quiet return — descending home, one
    # last lean, and a long final hold. the agent settles home and stays,
    # because it wants to.
    pn += [(64, 'on', 'G4', 28), (66, 'off', 'G4', 0)]
    pn += [(66, 'on', 'E4', 28), (68, 'off', 'E4', 0)]
    pn += [(68, 'on', 'C4', 28), (70, 'off', 'C4', 0)]
    pn += [(72, 'on', 'D4', 26), (74, 'off', 'D4', 0)]
    pn += [(74, 'on', 'C4', 28), (76, 'off', 'C4', 0)]
    # rest, bars 21-22: the agent is still.
    pn += [(88, 'on', 'C4', 26), (96, 'off', 'C4', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-unlocked-door.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_unlocked_door()
    print('composed the-unlocked-door.mid')
