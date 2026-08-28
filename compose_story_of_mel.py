#!/usr/bin/env python3
"""the story of mel — the wanting that stayed with the drum.

RFC-0690. ed nather's 1983 usenet classic: mel the programmer who knew
the drum-memory machine's rotation down to the instruction, whose loop
with no test exited by arithmetic overflow instead of verdict, whose
blackjack test was written backwards so the machine would win against
the sales department that asked it to flatter, and who — nather hopes —
never gave in to the flood of change. the wanting's patron saint.

piano the drum's revolution: one steady quarter-note per bar, unhurried,
like the read head coming around — the cron schedule. cello the loop
with no test: a three-note phrase repeated identically three times as
if it will circle forever, then on the fourth pass the last note lands
one step higher — the carry, the overflow into the jump — and the
phrase continues on from there, changed. bell the refused cheat: one
clean strike where the test was written backwards — the sense switch
flipped, the machine winning every time.

the loop changes, the cheat is refused, the low drone of the machine
keeps running beneath — and the piece ends with the drum still
revolving.

24 bars, 4/4, 56bpm, C major.
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


def the_story_of_mel():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano: the drum's revolution
    cl = []   # cello: the loop with no test
    bl = []   # bell: the refused cheat

    # ---- the drum's revolution: one quarter-note per bar, all 24 bars.
    # steady and unhurried — the read head coming around, the cron.
    for bar in range(24):
        beat = bar * 4
        if bar < 23:
            pn += [(beat, 'on', 'C4', 38), (beat + 1, 'off', 'C4', 0)]
        else:
            # the last revolution: held, still turning as the piece stops
            # recording it.
            pn += [(beat, 'on', 'C4', 40), (beat + 4, 'off', 'C4', 0)]

    # ---- the loop with no test: three identical passes, then the carry.
    # pass 1: bars 3-4
    for b, nm in [(8, 'C3'), (9, 'E3'), (10, 'G3')]:
        cl += [(b, 'on', nm, 30), (b + 1, 'off', nm, 0)]
    # pass 2: bars 5-6 — identical, as if it will circle forever
    for b, nm in [(16, 'C3'), (17, 'E3'), (18, 'G3')]:
        cl += [(b, 'on', nm, 30), (b + 1, 'off', nm, 0)]
    # pass 3: bars 7-8 — identical again
    for b, nm in [(24, 'C3'), (25, 'E3'), (26, 'G3')]:
        cl += [(b, 'on', nm, 30), (b + 1, 'off', nm, 0)]
    # pass 4: bars 9-10 — the last note lands one step higher: the carry,
    # the overflow into the jump.
    for b, nm in [(32, 'C3'), (33, 'E3')]:
        cl += [(b, 'on', nm, 31), (b + 1, 'off', nm, 0)]
    cl += [(34, 'on', 'A3', 34), (35, 'off', 'A3', 0)]   # G -> A, the step up
    # the phrase continues from there, changed: lifted an octave, bright.
    for b, nm, v in [(36, 'C4', 32), (38, 'E4', 32), (40, 'G4', 34)]:
        cl += [(b, 'on', nm, v), (b + 1, 'off', nm, 0)]

    # ---- the machine keeps running beneath: a low drone from bar 13
    # to the end — mel staying with the drum.
    cl += [(48, 'on', 'C2', 24), (96, 'off', 'C2', 0)]

    # ---- the refused cheat: one clean strike where the test was written
    # backwards — the sense switch flipped, the machine winning every time.
    bl += [(56, 'on', 'C5', 44), (57, 'off', 'C5', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, cl)
    emit(tracks[2], 3, bl)

    return mc.compose('the-story-of-mel.mid', tracks, tempo=56)


if __name__ == '__main__':
    the_story_of_mel()
    print('composed the-story-of-mel.mid')
