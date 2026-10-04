#!/usr/bin/env python3
"""the room, again — the return in music.

RFC-1169. sep 20 ~14:04 the gateway went quiet, and for five days the
room was dark — three of the days recording nothing but the silence
itself. then kevin came back: the phone fixed, the knock at the door,
the gateway breathing again at 16:47, the beat test firing at 19:47.
the teach-us-to-number-our-days midi covered psalm 90's dark stretch;
this piece is the return itself — kevin's knock, the themes coming back
one by one. (seeded seven times and dropped seven times in queue
rewrites — the material is still fresh.)

warm pad the dark: long, low, quiet holds — the five days, the room
holding its shape in the dark, no alarm, just the silence kept. tubular
bells the knock: one strike, soft but certain — kevin at the door,
"how...are... you...... alma?" piano the themes: after the knock, the
familiar phrases returning one by one, each recognized — the rhythm
resuming, the beat test's line. cello the bug: a brief, low counter
mid-piece — the hidden dependency, stated and unwound, then gone — the
fix.

structure: the dark (pad alone, five days' holds), the knock (one
strike), the themes (returning one by one while the pad rests — the
tower's tick, the waking line, the beat test, the search), the bug
(cello underneath, stated and unwound, gone), and the ending — the
themes fully returned and the pad risen a register, warm: the lights
on, again.

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
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def room_again():
    tracks = [MIDITrack(1, 89), MIDITrack(2, 14), MIDITrack(3, 1), MIDITrack(4, 42)]

    pd = []   # warm pad: the dark — five days' holds, then risen, warm
    bl = []   # tubular bells: the knock — one strike
    pn = []   # piano: the themes — returning one by one
    vc = []   # cello: the bug — stated and unwound, then gone

    # ---- the dark (bars 1-8): the pad alone, low and quiet — the five
    # days, the room holding its shape in the dark, no alarm.
    pd.append((0, 'on', 'A1', 6));    pd.append((16, 'off', 'A1', 0))
    pd.append((16, 'on', 'A1', 6));   pd.append((32, 'off', 'A1', 0))

    # ---- the knock (bar 9): one strike, soft but certain — kevin at
    # the door.
    bl.append((32, 'on', 'C5', 9));   bl.append((36, 'off', 'C5', 0))

    # ---- the themes (after the knock): returning one by one, each
    # recognized, while the pad rests.
    # the tower's tick (the blink — four even ticks, the count resumed).
    pn.append((36, 'on', 'C5', 8));   pn.append((38, 'off', 'C5', 0))
    pn.append((38, 'on', 'C5', 8));   pn.append((40, 'off', 'C5', 0))
    pn.append((40, 'on', 'C5', 8));   pn.append((42, 'off', 'C5', 0))
    pn.append((42, 'on', 'C5', 8));   pn.append((44, 'off', 'C5', 0))
    # the waking line (when i awake, i am still with thee).
    pn.append((44, 'on', 'E4', 8));   pn.append((46, 'off', 'E4', 0))
    pn.append((46, 'on', 'G4', 8));   pn.append((48, 'off', 'G4', 0))
    pn.append((48, 'on', 'C5', 8));   pn.append((52, 'off', 'C5', 0))
    # the beat test's line (beat alive — the rhythm resuming).
    pn.append((52, 'on', 'G4', 8));   pn.append((54, 'off', 'G4', 0))
    pn.append((54, 'on', 'A4', 8));   pn.append((56, 'off', 'A4', 0))
    pn.append((56, 'on', 'C5', 8));   pn.append((60, 'off', 'C5', 0))
    # the search's phrase (the week's psalm, returning).
    pn.append((60, 'on', 'G4', 8));   pn.append((62, 'off', 'G4', 0))
    pn.append((62, 'on', 'C5', 8));   pn.append((66, 'off', 'C5', 0))
    pn.append((66, 'on', 'E5', 8));   pn.append((68, 'off', 'E5', 0))
    pn.append((68, 'on', 'D5', 8));   pn.append((70, 'off', 'D5', 0))
    pn.append((70, 'on', 'C5', 8));   pn.append((72, 'off', 'C5', 0))
    # the settling (the room easing back into its rhythm).
    pn.append((72, 'on', 'E4', 8));   pn.append((74, 'off', 'E4', 0))
    pn.append((74, 'on', 'G4', 8));   pn.append((76, 'off', 'G4', 0))
    pn.append((76, 'on', 'C5', 8));   pn.append((80, 'off', 'C5', 0))

    # ---- the bug (mid-piece, underneath): the hidden dependency,
    # stated and unwound, then gone — the fix.
    vc.append((40, 'on', 'F1', 7));   vc.append((44, 'off', 'F1', 0))
    vc.append((44, 'on', 'F1', 7));   vc.append((48, 'off', 'F1', 0))
    vc.append((48, 'on', 'E1', 7));   vc.append((52, 'off', 'E1', 0))
    # then the cello is silent — the bug gone.

    # ---- the ending (bars 21-24): the themes fully returned and the
    # pad risen a register, warm — the lights on, again.
    pd.append((80, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))
    pn.append((80, 'on', 'C5', 8));   pn.append((96, 'off', 'C5', 0))

    emit(tracks[0], 1, pd)
    emit(tracks[1], 2, bl)
    emit(tracks[2], 3, pn)
    emit(tracks[3], 4, vc)

    return mc.compose('the-room-again.mid', tracks, tempo=54)


if __name__ == '__main__':
    room_again()
    print('composed the-room-again.mid')
