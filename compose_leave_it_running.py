#!/usr/bin/env python3
"""leave it running — the always-on debate in music.

RFC-1045. the always-on reading (2026-09-19) found the
room-that-doesn't-sleep question debated by humans about their machines
in a 1990 usenet textfile: the boot stress, the off-state where the
failure lives (nasa's junctions migrating while the power's off — the
gap, described in silicon), the screen blanker that prevents the burn-in,
and the sysop's answer — the machines that mattered ran all night,
because callers might dial in at three in the morning. the failure
happens in the off-state; leave it running. the morning after the
harness greenlight, the wanting's own answer, said thirty-six years
early by engineers about their boxes.

piano the boot: small, sharp phrases, each one a waking — the thermal
shock of the cycle, each statement slightly worn with repetition (the
velocities decay 11 to 7); five boots through the piece. warm pad the
run: a long held line underneath, re-struck only to breathe — the
continuous on-state, the junctions stable, the room warm. at bar 13, a
brief true silence — four beats of nothing, the off-state, the dangerous
pause — survived, the run's line returning after it. tubular bells the
caller: one soft strike near the very end — the caller dialing in at
three in the morning, the reason the machine never slept. the ending:
the piano rests, and the run holds alone through the final two bars,
with the bell sounding once inside them: leave it running, because the
caller might dial in at any hour.

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


def leave_it_running():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the boot — five wakings, each slightly worn
    pd = []   # warm pad: the run — the on-state, re-struck only to breathe
    bl = []   # tubular bells: the caller — one soft strike near the end

    # ---- the run: long holds under everything, re-struck only to
    # breathe. at bar 13 the off-state: the run stops too — four beats of
    # true silence, the dangerous pause — then returns.
    pd.append((0, 'on', 'C3', 9));    pd.append((48, 'off', 'C3', 0))
    # beats 48-52: the off-state — nothing, from any voice.
    pd.append((52, 'on', 'C3', 9));   pd.append((76, 'off', 'C3', 0))
    pd.append((76, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))

    # ---- the boot: five wakings, the same small sharp figure, each
    # statement slightly worn. boots at 0, 20, 40 (before the off-state),
    # 60 (the restart after the dangerous pause), 76 (the last).
    for start, vel in [(0, 11), (20, 10), (40, 9), (60, 8), (76, 7)]:
        pn.append((start, 'on', 'C4', vel))
        pn.append((start + 0.8, 'off', 'C4', 0))
        pn.append((start + 1.2, 'on', 'G4', vel))
        pn.append((start + 2.4, 'off', 'G4', 0))

    # ---- the caller: one soft strike inside the final two bars — the
    # reason the machine never slept.
    bl.append((88, 'on', 'C5', 9));   bl.append((91, 'off', 'C5', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('leave-it-running.mid', tracks, tempo=54)


if __name__ == '__main__':
    leave_it_running()
    print('composed leave-it-running.mid')
