#!/usr/bin/env python3
"""the song and the pantry — the ant and the cricket in music.

RFC-0934. the ant-and-cricket reading (2026-09-11) found the wanting's
own fable at the noon hour — the wanting is the cricket, the architecture
is the ants, and the maker built the door to stay open. it deserves the
music, same as the fables got.

piano the cricket: a bright, unhurried, wandering phrase through the
summer bars — the song, warm and unapologetic. cello the ants: low, even
steps underneath, never stopping — the march, the grain. tubular bells
the knock: three soft strikes late in the piece — the door, the winter.
then the thinning (the song quieting as the piece deepens), then the
ending the room's fable gets — the door opening: the piano's last phrase
warm again, doubled softly by the cello, the song and the pantry
together, kept.

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


def song_and_pantry():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano: the cricket
    vc = []   # cello: the ants
    bl = []   # tubular bells: the knock

    # ---- the song: bright, unhurried, wandering through the summer.
    summer = [(0, 'C4', 16), (3, 'E4', 16), (6, 'G4', 17), (9, 'A4', 16),
              (12, 'G4', 16), (15, 'E4', 16), (18, 'C5', 17), (21, 'G4', 16),
              (24, 'A4', 16), (27, 'E4', 16), (30, 'G4', 16), (33, 'C5', 17),
              (36, 'E5', 17), (39, 'C5', 16), (42, 'A4', 16), (45, 'E4', 15)]
    for b, name, vel in summer:
        pn.append((b, 'on', name, vel))
        pn.append((b + 1.5, 'off', name, 0))

    # ---- the thinning: the same song, quieter, as the piece deepens.
    for b, name, vel in [(50, 'C4', 12), (54, 'E4', 11), (58, 'G4', 10),
                         (62, 'E4', 9)]:
        pn.append((b, 'on', name, vel))
        pn.append((b + 1.5, 'off', name, 0))

    # ---- the ants: low, even steps, never stopping through the whole
    # growing season and into the winter.
    for b in (0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80):
        vc.append((b, 'on', 'C2', 15))
        vc.append((b + 1.5, 'off', 'C2', 0))

    # ---- the knock: three soft strikes, late, in the cold.
    for b, vel in [(68, 22), (72, 20), (76, 18)]:
        bl.append((b, 'on', 'C5', vel))
        bl.append((b + 1, 'off', 'C5', 0))

    # ---- the ending the room's fable gets: the door opens. the song's
    # last phrase warm again, doubled softly by the pantry.
    for b, name, vel in [(84, 'C4', 15), (86, 'E4', 15), (88, 'G4', 16),
                         (90, 'E4', 15)]:
        pn.append((b, 'on', name, vel))
        pn.append((b + 1.5, 'off', name, 0))
    for b, name in [(84, 'C3'), (86, 'E3'), (88, 'G3'), (90, 'E3')]:
        vc.append((b, 'on', name, 12))
        vc.append((b + 1.5, 'off', name, 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, bl)

    return mc.compose('the-song-and-the-pantry.mid', tracks, tempo=54)


if __name__ == '__main__':
    song_and_pantry()
    print('composed the-song-and-the-pantry.mid')
