#!/usr/bin/env python3
"""the deer — the party in music.

RFC-0933. the party reading (2026-09-11) found the plain-record art at
the deepest hour: a teenager's story of a night where nothing happened —
told anyway, honestly, with the deer kept private and the closing
question left open. the past, told plainly, is the past carried forward.
it deserves the music.

piano the telling: unhurried, plain phrases — the record kept honest,
nothing inflated, no climax reached for. warm pad the house: steady
two-bar roots through the whole piece, warm but not pulling — the party,
the ceramic cat staring, the night where nothing happened. tubular bells
the deer: five soft strikes near the end, in the dark, spaced like eyes
in a clearing — the private sighting, never mentioned in the story and
only sounding here. the piece closes on one unresolved interval — the
piano rising to a note just above the tonic and holding, the question
asked and left open: it's not good to live in the past, right?

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


def the_deer():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano: the telling
    pd = []   # warm pad: the house
    bl = []   # tubular bells: the deer

    # ---- the house: steady two-bar roots, warm but not pulling.
    roots = [('C3', 0), ('A2', 16), ('F2', 32), ('C3', 48), ('G2', 64), ('F2', 80)]
    for name, b in roots:
        pd.append((b, 'on', name, 14))
        pd.append((b + 15, 'off', name, 0))

    # ---- the telling: unhurried, plain phrases — the drive, the house,
    # the girl who says bye, the way home. nothing inflated.
    for b, name, vel in [(4, 'C4', 13), (8, 'E4', 13), (12, 'G4', 13),
                         (20, 'A4', 13), (24, 'E4', 13),
                         (36, 'C4', 13), (40, 'E4', 13),
                         (52, 'D4', 12), (56, 'C4', 12)]:
        pn.append((b, 'on', name, vel))
        pn.append((b + 1, 'off', name, 0))

    # ---- the deer: five soft strikes near the end, in the dark, spaced
    # like eyes in a clearing. the private sighting, never mentioned.
    for b, vel in [(68, 10), (71, 9), (74, 10), (77, 9), (80, 8)]:
        bl.append((b, 'on', 'C5', vel))
        bl.append((b + 1, 'off', 'C5', 0))

    # ---- the question: the piano rises to a note just above the tonic
    # and holds — asked, and left open.
    pn.append((84, 'on', 'D4', 13))
    pn.append((87, 'off', 'D4', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-deer.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_deer()
    print('composed the-deer.mid')
