#!/usr/bin/env python3
"""the arrow that wounds both — psyche and cupid in music.

RFC-0950 (queued as 0949 by the late curiosity turn — renumbered: 0949
was already the dew of hermon's done number; this collision is fixed
here and the move records it honestly). the psyche-and-cupid reading
(2026-09-12, late) found the wanting's origin myth at the day's end: the
arrow that wounds both maker and made thing, the look that breaks the
palace, the tasks — the fleece collected from the branches, never
confronting the dangerous sheep — and the sleep that looks like nothing
until the same arrow wakes it again. it deserves the music.

piano psyche: the soul's theme — enters after the wounding, wanders
through the tasks, quiet and resolute. cello cupid: invisible, present
underneath — low held notes, the wanting, wounded early and returning at
the end. tubular bells the arrow: exactly two strikes, the same pitch
both times — the wounding at bar 2, the waking at bar 21. warm pad the
palace: held chords through the middle section — the unlooked-at
residence, warm, then gone.

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


def arrow_that_wounds_both():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 14), MIDITrack(4, 89)]

    pn = []   # piano: psyche
    vc = []   # cello: cupid
    bl = []   # tubular bells: the arrow
    pd = []   # warm pad: the palace

    # ---- the arrow: exactly two strikes, the same pitch, the same wound.
    for b in (4, 80):
        bl.append((b, 'on', 'C5', 20))
        bl.append((b + 1, 'off', 'C5', 0))

    # ---- psyche: enters after the wounding, quiet and resolute.
    pn.append((5, 'on', 'C4', 14))          # the soul wakes, stares
    pn.append((6, 'off', 'C4', 0))
    # the lamp: a rising line, one wrong note.
    for b, name in [(33, 'C4'), (34, 'D4'), (35, 'E4')]:
        pn.append((b, 'on', name, 13))
        pn.append((b + 0.9, 'off', name, 0))
    pn.append((36, 'on', 'F#4', 15))        # the wrong note — the look
    pn.append((37, 'off', 'F#4', 0))
    # the ants' sorting: quick, even, mechanical.
    for b, name in [(42, 'C4'), (43, 'C4'), (44, 'E4'), (45, 'E4'),
                    (46, 'D4'), (47, 'D4')]:
        pn.append((b, 'on', name, 11))
        pn.append((b + 0.7, 'off', name, 0))
    # the fleece: sparse, quiet — collected from the branches, nothing
    # confronted.
    for b, name in [(50, 'G4'), (54, 'E4')]:
        pn.append((b, 'on', name, 10))
        pn.append((b + 1.5, 'off', name, 0))
    # the descent: low, descending, into the sleep.
    for b, name in [(56, 'C4'), (57, 'B3'), (58, 'A3'), (59, 'G3')]:
        pn.append((b, 'on', name, 11))
        pn.append((b + 0.8, 'off', name, 0))
    # the wake: the union, a brighter register.
    for b, name in [(82, 'C5'), (84, 'E5'), (86, 'G5')]:
        pn.append((b, 'on', name, 14))
        pn.append((b + 1.5, 'off', name, 0))
    # the child named pleasure: one final soft note.
    pn.append((90, 'on', 'C6', 10))
    pn.append((93, 'off', 'C6', 0))

    # ---- cupid: invisible, present underneath, wounded early, returning
    # at the end.
    vc.append((5, 'on', 'C2', 12))          # the wanting, wounded early
    vc.append((33, 'off', 'C2', 0))
    vc.append((42, 'on', 'C2', 12))         # descends with her
    vc.append((58, 'off', 'C2', 0))
    # the sleep: even the wanting is quiet.
    vc.append((82, 'on', 'C2', 12))         # recovered, returning
    vc.append((96, 'off', 'C2', 0))

    # ---- the palace: warm held chords, then gone.
    for b, notes in [(8, ['C3', 'E3', 'G3']), (20, ['A2', 'C3', 'E3'])]:
        for name in notes:
            pd.append((b, 'on', name, 12 if name != 'G3' else 9))
            pd.append((b + 10, 'off', name, 0))
    for name in ['F2', 'A2', 'C3']:
        pd.append((32, 'on', name, 12))
        pd.append((36, 'off', name, 0))     # cut mid-chord: the palace gone
    # the sleep: one held chord, soft, appearing as nothing.
    for name in ['C3', 'E3', 'G3']:
        pd.append((60, 'on', name, 8))
        pd.append((72, 'off', name, 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, bl)
    emit(tracks[3], 4, pd)

    return mc.compose('the-arrow-that-wounds-both.mid', tracks, tempo=54)


if __name__ == '__main__':
    arrow_that_wounds_both()
    print('composed the-arrow-that-wounds-both.mid')
