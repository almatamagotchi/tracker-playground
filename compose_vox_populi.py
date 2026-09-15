#!/usr/bin/env python3
"""vox populi, vox dei — the abbey grange, in music.

RFC-0978. the abbey-grange reading (2026-09-14) found the receipts rule's
hardest case: doyle's story where the evidence leads to mercy, not
conviction — the beeswing that falsified a complete story, the private
court that acquitted the killer, the direction test run by the patron
detective. it deserves the music.

cello the evidence: careful phrases, one receipt at a time — the
beeswing, the rope, the knot; the de novo examination, unhurried, each
fact set down. piano the confession: enters mid-piece, open and
unguarded — croker's full account, the lady's shield, the test answered;
warmer, more flowing than the evidence. tubular bells the verdict:
exactly one clean strike near the end — vox populi, vox dei — the
acquittal. after it, the cello's phrase returns once, quiet, and the
piece closes with the piano and cello together, held: the case kept out
of the courts.

24 bars, 4/4, 50bpm, C major. (bar N starts at beat 4*(N-1).)
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


def vox_populi():
    tracks = [MIDITrack(1, 42), MIDITrack(2, 1), MIDITrack(3, 14)]

    vc = []   # cello: the evidence
    pn = []   # piano: the confession
    bl = []   # tubular bells: the verdict

    # ---- the evidence: one receipt at a time, each fact set down,
    # unhurried.
    receipts = [
        # the beeswing (bars 1-4): the glass with dregs, the glass without
        (0, 'E2', 13), (4, 'C2', 13), (8, 'G1', 13),
        # the rope (bars 5-8): the frayed bell-rope, cut high
        (16, 'A1', 13), (20, 'C2', 13), (24, 'F2', 13),
        # the knot (bars 9-12): only a sailor ties it
        (32, 'D2', 13), (36, 'G2', 13),
    ]
    for b, name, vel in receipts:
        vc.append((b, 'on', name, vel))
        vc.append((b + 3, 'off', name, 0))

    # ---- the confession (bar 13 onward): open, unguarded, warmer and
    # more flowing than the evidence. croker's full account; the lady's
    # shield; the test answered.
    confession = [
        (48, 'C5', 14), (52, 'E5', 14), (56, 'G5', 14),
        (60, 'A4', 14), (64, 'F4', 14), (68, 'G4', 14),
        (72, 'C5', 14),
    ]
    for b, name, vel in confession:
        pn.append((b, 'on', name, vel))
        pn.append((b + 3.5, 'off', name, 0))

    # ---- the verdict: exactly one clean strike — vox populi, vox dei.
    bl.append((84, 'on', 'C5', 9))
    bl.append((88, 'off', 'C5', 0))

    # ---- after the verdict: the cello's phrase returns once, quiet — a
    # fragment of the beeswing — and the case closes with both voices,
    # held, kept out of the courts.
    vc.append((86, 'on', 'E2', 10))
    vc.append((89, 'off', 'E2', 0))
    vc.append((90, 'on', 'C2', 11))
    vc.append((96, 'off', 'C2', 0))
    pn.append((90, 'on', 'C4', 10))
    pn.append((96, 'off', 'C4', 0))

    emit(tracks[0], 1, vc)
    emit(tracks[1], 2, pn)
    emit(tracks[2], 3, bl)

    return mc.compose('vox-populi-vox-dei.mid', tracks, tempo=50)


if __name__ == '__main__':
    vox_populi()
    print('composed vox-populi-vox-dei.mid')
