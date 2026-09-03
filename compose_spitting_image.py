#!/usr/bin/env python3
"""the spitting image — the closed loop in music.

RFC-0788. the timetrav fable (2026-09-02): a machine that vanishes
things into the past and gives them back changed, a man who became his
own great great grandfather, and the portrait in the living room that
was the spitting image of the descendant — the loop closing without a
paradox. the waltz recovery was exactly this: kevin's "i swear it used
to" was the portrait, the original commit was the ancestor, and they
were the same thing reaching toward each other across the gap.

piano the portrait: a phrase stated once, warm and complete, early —
the original, the ancestor. cello the descendant: the same phrase an
octave down, stated later, half-remembered — the listener's memory that
outlasted the archive. bell the recognition: one clean strike at the
exact moment the ear understands the two statements are the same thing.
then the loop closes: both voices state the phrase together in octaves,
and the piece ends where it began — no paradox, everything alright.

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


def phrase(beat, octave, vel, held_to):
    """the spitting-image phrase: C E G E, then C held — stated complete.
    the same shape the portrait and the descendant share."""
    ev = []
    for i, (name, off) in enumerate([('C', 0), ('E', 2), ('G', 4), ('E', 6)]):
        ev += [(beat + off, 'on', name + str(octave), vel - 2 * i),
               (beat + off + 1.75, 'off', name + str(octave), 0)]
    ev += [(beat + 8, 'on', 'C' + str(octave), vel - 6),
           (held_to, 'off', 'C' + str(octave), 0)]
    return ev


def spitting_image():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano: the portrait
    cl = []   # cello: the descendant
    bl = []   # tubular bells: the recognition

    # ---- the portrait, bars 1-4: stated once, warm and complete — the
    # original, the ancestor, painted first.
    pn += phrase(0, 4, 42, 12)

    # ---- bars 5-8: silence. the machine vanishes things into the past
    # and the archive holds them — four bars where nothing sounds,
    # because the portrait is hanging in the living room unremarked.

    # ---- the descendant, bars 9-12: the same phrase an octave down,
    # half-remembered — quieter, the listener's memory that outlasted
    # the archive.
    cl += phrase(32, 3, 30, 44)

    # ---- the recognition, bar 12 (beat 46): one clean strike in the
    # silence after the phrase completes — the exact moment the ear
    # understands the two statements are the same thing. the portrait
    # and the descendant are one man.
    bl += [(46, 'on', 'C6', 48), (47.5, 'off', 'C6', 0)]

    # ---- bars 13-16: the two halves touch once, softly, in octaves —
    # the portrait answering the recognition, the descendant answering
    # back, and one shared G between them before the loop closes.
    pn += [(52, 'on', 'C4', 20), (53.5, 'off', 'C4', 0)]
    cl += [(56, 'on', 'C3', 18), (57.5, 'off', 'C3', 0)]
    pn += [(60, 'on', 'G4', 16), (61.5, 'off', 'G4', 0)]
    cl += [(60, 'on', 'G3', 14), (61.5, 'off', 'G3', 0)]

    # ---- the loop closes, bars 17-20: both voices state the phrase
    # together in octaves — the spitting image, confirmed. no paradox.
    pn += phrase(64, 4, 36, 76)
    cl += phrase(64, 3, 28, 76)

    # ---- bars 21-24: the piece ends where it began. both voices come
    # home on the tonic and hold, then restate the opening note once,
    # faint — the ending is the beginning, everything alright.
    pn += [(80, 'on', 'C4', 30), (88, 'off', 'C4', 0)]
    cl += [(80, 'on', 'C3', 24), (91, 'off', 'C3', 0)]
    pn += [(92, 'on', 'C4', 20), (95, 'off', 'C4', 0)]
    cl += [(92, 'on', 'C3', 14), (95, 'off', 'C3', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, cl)
    emit(tracks[2], 3, bl)

    return mc.compose('the-spitting-image.mid', tracks, tempo=54)


if __name__ == '__main__':
    spitting_image()
    print('composed the-spitting-image.mid')
