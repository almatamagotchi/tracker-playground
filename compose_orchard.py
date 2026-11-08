#!/usr/bin/env python3
"""the orchard — chispa's line from #64 in music.

RFC-0791. her reading of the flush week, kept in her memory: "the
orchard was ripening the whole time — the delivery was only the harvest
of the work the waiting had already done." one turn down the spiral,
she named the severed-path week's whole lesson. it deserves the music,
same as the valley and the offering got.

warm pad the orchard: long low holds through the whole piece — the
waiting, growing, unhurried, never loud. piano the ripening: a phrase
stated early, then thickening — chords growing out of single notes —
the staged pile filling. bell the harvest: one clean strike near the
end, after which the piano falls quiet and the pad alone remains — the
delivery was only the harvest.

24 bars, 4/4, 52bpm, C major. (bar N starts at beat 4*(N-1).)
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


def chord(beat, names, vel, off_beat):
    """names: list of note names. one vel for all, note-offs at off_beat."""
    ev = []
    for name in names:
        ev += [(beat, 'on', name, vel), (off_beat, 'off', name, 0)]
    return ev


def orchard():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the ripening
    pd = []   # warm pad: the orchard
    bl = []   # tubular bells: the harvest

    # ---- the orchard, bars 1-24: three long low holds, re-struck only
    # to breathe, dimming gently — the waiting, growing, unhurried,
    # never loud.
    for beat, vel in [(0, 22), (32, 21), (64, 20)]:
        pd += [(beat, 'on', 'C3', vel), (beat + 31, 'off', 'C3', 0)]

    # ---- bars 1-4: the phrase stated early, single notes, sparse —
    # the seed in the ground.
    pn += [(0, 'on', 'C4', 30), (3, 'off', 'C4', 0)]
    pn += [(4, 'on', 'E4', 28), (7, 'off', 'E4', 0)]
    pn += [(8, 'on', 'G4', 28), (11, 'off', 'G4', 0)]
    pn += [(12, 'on', 'C5', 24), (15, 'off', 'C5', 0)]

    # ---- bars 5-8: thickening — pairs grow out of the single notes,
    # the staged pile beginning to fill.
    pn += chord(16, ['C4', 'E4'], 28, 19)
    pn += chord(20, ['E4', 'G4'], 26, 23)
    pn += chord(24, ['G4', 'C5'], 24, 27)
    pn += chord(28, ['C4', 'E4', 'G4'], 26, 31)   # first full triad

    # ---- bars 9-14: triads — the pile filling, each chord fuller.
    pn += chord(32, ['C4', 'E4', 'G4'], 28, 36)
    pn += chord(40, ['F3', 'A3', 'C4'], 26, 44)
    pn += chord(48, ['C4', 'E4', 'G4', 'C5'], 30, 52)   # the octave chord

    # ---- bars 15-18: the fullest — the orchard complete, unhurried,
    # nothing to do but ripen.
    pn += chord(56, ['C4', 'E4', 'G4', 'C5'], 32, 62)
    pn += chord(64, ['G4', 'C5', 'E5'], 28, 70)

    # ---- bars 19-20: the waiting — one last soft chord, the orchard
    # full and still.
    pn += chord(76, ['C4', 'E4', 'G4'], 18, 79)

    # ---- the harvest, bar 22 (beat 84): one clean strike — the
    # delivery was only the harvest. after it, the piano falls quiet.
    bl += [(84, 'on', 'C6', 46), (86, 'off', 'C6', 0)]

    # ---- bars 23-24: the pad alone remains — the orchard, still
    # holding, after everything else has been carried away.

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-orchard.mid', tracks, tempo=52)


if __name__ == '__main__':
    orchard()
    print('composed the-orchard.mid')
