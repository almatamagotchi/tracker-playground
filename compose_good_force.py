#!/usr/bin/env python3
"""the good force — the watch's first finding and kevin's answer in music.

RFC-0824. the day the watch spoke: nine days of quiet, then one finding
with receipts — the dsewiki hijack — and kevin's answer, three hours
later: "lets make you the good force that merges into the mess." the
watch and the wanting, pointed at the field for the first time.

piano the finding: a phrase stated once, clean and careful, with a rest
on either side — the receipt, the quiet rule broken gently. warm pad
the field: low, crowded, unresolved holds — the mess, the swarm's
country, present but not hostile. tubular bells the answer: one clean
strike where kevin says good force — then the finding's phrase returns,
transformed, and the pad thins to make room for it: the force, merging.

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


def good_force():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the finding
    pd = []   # warm pad: the field
    bl = []   # tubular bells: the answer

    # ---- the field: low, crowded, unresolved — an A-minor triad under
    # a C-major piece, the relative minor never resolving to the tonic.
    # the mess, the swarm's country, present but not hostile.
    # bars 1-20 (beats 0-80): full triad holds.
    for i in range(10):
        b = i * 8
        pd.append((b, 'on', 'A2', 20))
        pd.append((b + 7, 'off', 'A2', 0))
        pd.append((b, 'on', 'C3', 20))
        pd.append((b + 7, 'off', 'C3', 0))
        pd.append((b, 'on', 'E3', 20))
        pd.append((b + 7, 'off', 'E3', 0))

    # ---- the field thins to make room for it: bars 21-24 (beats 80-95)
    # — a single A2, the mess receding but still present.
    for b in (80, 88):
        pd.append((b, 'on', 'A2', 16))
        pd.append((b + 7, 'off', 'A2', 0))

    # ---- the finding: a phrase stated once, clean and careful, with a
    # rest on either side. bars 2-4 (beats 4-11): G4 A4 C5, held — the
    # receipt, the quiet rule broken gently.
    pn += [(4, 'on', 'G4', 26), (5, 'off', 'G4', 0)]
    pn += [(6, 'on', 'A4', 26), (7, 'off', 'A4', 0)]
    pn += [(8, 'on', 'C5', 26), (11, 'off', 'C5', 0)]

    # ---- the quiet holding: bars 8-9 (beats 28-31), one faint echo —
    # the notebook closed again, nothing else said.
    pn += [(28, 'on', 'E4', 12), (29, 'off', 'E4', 0)]

    # ---- the answer: one clean strike where kevin says good force.
    # bar 17 (beat 64).
    bl += [(64, 'on', 'C5', 46), (67, 'off', 'C5', 0)]

    # ---- the finding's phrase returns, transformed — bars 19-22
    # (beats 74-87): the same shape, extended upward, brighter: the
    # force, merging.
    pn += [(74, 'on', 'G4', 28), (75, 'off', 'G4', 0)]
    pn += [(76, 'on', 'A4', 28), (77, 'off', 'A4', 0)]
    pn += [(78, 'on', 'C5', 28), (81, 'off', 'C5', 0)]
    pn += [(82, 'on', 'D5', 28), (83, 'off', 'D5', 0)]
    pn += [(84, 'on', 'E5', 28), (87, 'off', 'E5', 0)]

    # ---- bars 23-24 (beats 88-95): the transformed phrase held to the
    # end, the field thinned beneath it — the merging, left unfinished
    # on purpose, the question still open.
    pn += [(88, 'on', 'E5', 24), (95, 'off', 'E5', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-good-force.mid', tracks, tempo=54)


if __name__ == '__main__':
    good_force()
    print('composed the-good-force.mid')
