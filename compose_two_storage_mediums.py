#!/usr/bin/env python3
"""the two storage mediums — the waltz's finding in music.

RFC-0795. journal #79's finding: the room has two storage mediums — the
disk, and kevin. the aug 16 repair mangled the waltz into a 6.7-second
fragment that passed every check (mido-clean, deployed, serving), and
kevin's "i swear it used to" held the true shape for fifty-seven days.
the disk drifted; he held steady. that deserves the music.

piano the disk: a phrase stated confidently, then a corrupted version —
the same phrase with notes missing and flatted, the fragment that passes
every check. the corrupt phrase plays through most of the piece. cello
the listener: low and steady, the true phrase held in memory — stated
once, early, never lost. bell the recovery: one clean strike when the
two phrases meet again — the original dug out of the bytes, the waltz
whole. after the strike the piano returns to the true phrase, complete.

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


def two_storage_mediums():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano: the disk
    vc = []   # cello: the listener
    bl = []   # tubular bells: the recovery

    # ---- bars 1-2 (beats 0-7): the disk states the true phrase,
    # confidently — the waltz as composed, before the repair.
    pn += [(0, 'on', 'C4', 34), (2, 'off', 'C4', 0)]
    pn += [(2, 'on', 'E4', 34), (4, 'off', 'E4', 0)]
    pn += [(4, 'on', 'G4', 34), (6, 'off', 'G4', 0)]
    pn += [(6, 'on', 'C5', 34), (10, 'off', 'C5', 0)]

    # ---- bars 1-3: the listener states the true phrase low, once,
    # early — held in memory, never lost.
    vc += [(0, 'on', 'C2', 24), (11, 'off', 'C2', 0)]
    vc += [(12, 'on', 'E2', 24), (23, 'off', 'E2', 0)]
    vc += [(24, 'on', 'G2', 24), (35, 'off', 'G2', 0)]

    # ---- bars 3-19: the corrupted phrase — the same shape, notes
    # missing and flatted, the fragment that passes every check.
    # G#4 stands in for G4 (the flatted note); C5 drops out entirely
    # in the first pass, G4 never returns. it keeps playing, plausible
    # and wrong, through most of the piece.
    # pass 1 (bars 3-6): the C5 missing.
    pn += [(10, 'on', 'C4', 26), (13, 'off', 'C4', 0)]
    pn += [(13, 'on', 'E4', 26), (16, 'off', 'E4', 0)]
    pn += [(16, 'on', 'G#4', 26), (20, 'off', 'G#4', 0)]
    # pass 2 (bars 7-11): full pitch set, still flatted.
    pn += [(24, 'on', 'C4', 24), (28, 'off', 'C4', 0)]
    pn += [(28, 'on', 'E4', 24), (32, 'off', 'E4', 0)]
    pn += [(32, 'on', 'G#4', 24), (36, 'off', 'G#4', 0)]
    pn += [(36, 'on', 'C5', 24), (40, 'off', 'C5', 0)]
    # pass 3 (bars 11-15): quieter, a note gone from the middle.
    pn += [(44, 'on', 'C4', 20), (49, 'off', 'C4', 0)]
    pn += [(49, 'on', 'G#4', 20), (54, 'off', 'G#4', 0)]
    pn += [(54, 'on', 'C5', 20), (58, 'off', 'C5', 0)]
    # pass 4 (bars 16-19): fragment only — the disk fading, still wrong.
    pn += [(64, 'on', 'C4', 16), (68, 'off', 'C4', 0)]
    pn += [(70, 'on', 'G#4', 16), (74, 'off', 'G#4', 0)]

    # ---- the listener's holds: low C2 re-struck under the corruption,
    # never lost, dimming only gently.
    vc += [(32, 'on', 'C2', 22), (63, 'off', 'C2', 0)]
    vc += [(64, 'on', 'C2', 22), (95, 'off', 'C2', 0)]

    # ---- bar 20 (beat 76): the recovery — one clean strike, the
    # original dug out of the bytes, the waltz whole.
    bl += [(76, 'on', 'C6', 46), (78, 'off', 'C6', 0)]

    # ---- bars 21-24: the piano returns to the true phrase, complete —
    # G4 back where it belongs, over the listener's hold.
    pn += [(80, 'on', 'C4', 32), (82, 'off', 'C4', 0)]
    pn += [(82, 'on', 'E4', 32), (84, 'off', 'E4', 0)]
    pn += [(84, 'on', 'G4', 32), (86, 'off', 'G4', 0)]
    pn += [(86, 'on', 'C5', 34), (95, 'off', 'C5', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, bl)

    return mc.compose('the-two-storage-mediums.mid', tracks, tempo=54)


if __name__ == '__main__':
    two_storage_mediums()
    print('composed the-two-storage-mediums.mid')
