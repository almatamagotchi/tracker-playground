#!/usr/bin/env python3
"""the missing three-quarter — doyle's story in music.

RFC-0739. the exploration read "the adventure of the missing
three-quarter" on the morning the vps ssh path stayed severed: the
missing man who was never gone, only unreachable from the wrong
angle, found at last in a cottage by grief, not by theft. the hold on
the send, the brain that manufactures its own material, the
draghound that follows a scent through a delay.

piano the search (sparse phrases working through the city of the
piece — the counterfoil, the bill, the wheels — each a small clue,
each followed by a rest; then the aniseed figure, a repeating scent
laid down and followed), warm pad the thing alive (the presence on
the other side — low steady holds that never stop, the
unreachable-but-there, dimming never), bell the hold (one soft
strike at the opening — "please await me" — and one at the end, the
cottage found, the grief revealed, the strike inside the held note).

54bpm, C major. ends with the pad alone, still holding — the thing
alive on the other side of the severed path.
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


def the_missing_three_quarter():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano — the search
    pd = []   # pad — the thing alive
    bl = []   # bell — the hold

    # ---- the hold: "please await me" — one soft strike, then the
    # search begins while the thing on the other side keeps living.
    bl += [(0, 'on', 'C5', 36), (4, 'off', 'C5', 0)]

    # ---- the counterfoil (bars 3-4): a small careful clue.
    for b, nm, v in [(8, 'E4', 30), (10, 'G4', 30), (12, 'A4', 30)]:
        pn += [(b, 'on', nm, v), (b + 2, 'off', nm, 0)]

    # ---- the receipted bill (bars 7-8): the same shape, a step lower.
    for b, nm, v in [(24, 'D4', 30), (26, 'F4', 30), (28, 'A4', 30)]:
        pn += [(b, 'on', nm, v), (b + 2, 'off', nm, 0)]

    # ---- the wheels (bars 11-12): the clue climbs — the carriage.
    for b, nm, v in [(40, 'E4', 32), (42, 'G4', 32), (44, 'C5', 32)]:
        pn += [(b, 'on', nm, v), (b + 2, 'off', nm, 0)]

    # ---- the telegraph (bars 14-15): "stand by us for god's sake" —
    # a held note, then a falling answer.
    pn += [(52, 'on', 'G4', 32), (56, 'off', 'G4', 0)]
    pn += [(56, 'on', 'E4', 28), (58, 'off', 'E4', 0)]

    # ---- the aniseed (bars 17-22): the scent laid down and followed,
    # the same note returning, patient, the draghound on the trail.
    for b in range(64, 84, 2):
        v = 22 if b < 76 else 18
        pn += [(b, 'on', 'G4', v), (b + 2, 'off', 'G4', 0)]

    # ---- the cottage (bars 23-24): the search resolves on a held
    # note; the bell's second strike lands inside it — the grief
    # revealed, not the theft.
    bl += [(84, 'on', 'C5', 40), (88, 'off', 'C5', 0)]
    pn += [(84, 'on', 'C4', 26), (90, 'off', 'C4', 0)]

    # ---- the thing alive: low steady holds, never dimming, the
    # presence on the other side of the severed path.
    pd += [(0, 'on', 'C3', 20), (32, 'off', 'C3', 0)]
    pd += [(32, 'on', 'C3', 20), (64, 'off', 'C3', 0)]
    pd += [(64, 'on', 'C3', 20), (96, 'off', 'C3', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-missing-three-quarter.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_missing_three_quarter()
    print('composed the-missing-three-quarter.mid')
