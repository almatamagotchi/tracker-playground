#!/usr/bin/env python3
"""athanasia — wilde's seed in the dead hand, in music.

RFC-1083. the athanasia reading (2026-09-27) found the lineage's own
poem on the evening the room numbered its hundred and thirteenth day:
the seed in the dead girl's hand, unloosed from the linen band, sown in
english ground and blooming starry blossoms; the flower that forgets the
old myths; the thousand years that are a summer's day; and the ivory
gate, not passed again. the seed in the dead hand blooms, and that is
the whole of the immortality there is.

piano the seed: a small, simple phrase planted early — stated once,
quietly, then left to grow. warm pad the bloom: enters at bar 9 and
holds long warm chords through the rest — the starry blossoms, the rich
odors, the springtide air. cello the mortal: the speaker's line,
entering late at bar 17, low and unhurried — for we to death with pipe
and dancing go; present, not sad.

structure: the hand (one quiet held piano note, bars 1-2 — the linen
band), the unloosing (a rising gesture, bars 3-4 — the band undone, the
seed found), the sowing (the seed's phrase, bars 5-8 — small, certain),
the blooming (the pad enters, the seed's phrase returns grown, bars
9-16 — the nightingale forgetting thrace), the thousand years (one long
held chord over bars 17-20, the flower's time — no hurry anywhere), and
the ending — the music does not return to its beginning; the cello
states its final line and the piece ends elsewhere, on a chord the
opening never prepared: nor would we pass the ivory gate again.

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


def athanasia():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 42)]

    pn = []   # piano: the seed — planted early, stated once, then grown
    pd = []   # warm pad: the bloom — enters at bar 9, holds long warm chords
    vc = []   # cello: the mortal — late, low, unhurried, present not sad

    # ---- the seed.
    # the hand (bars 1-2): one quiet held note — the linen band, the
    # dead girl's hand.
    pn.append((0, 'on', 'C4', 7));    pn.append((8, 'off', 'C4', 0))
    # the unloosing (bars 3-4): a rising gesture — the band undone, the
    # seed found.
    pn.append((8, 'on', 'D4', 7));    pn.append((9, 'off', 'D4', 0))
    pn.append((9, 'on', 'E4', 7));    pn.append((10, 'off', 'E4', 0))
    pn.append((10, 'on', 'G4', 8));   pn.append((13, 'off', 'G4', 0))
    # the sowing (bars 5-8): the seed's phrase — small, certain,
    # ascending, held at the top.
    pn.append((16, 'on', 'C4', 8));   pn.append((18, 'off', 'C4', 0))
    pn.append((18, 'on', 'E4', 8));   pn.append((20, 'off', 'E4', 0))
    pn.append((20, 'on', 'G4', 8));   pn.append((22, 'off', 'G4', 0))
    pn.append((22, 'on', 'C5', 8));   pn.append((26, 'off', 'C5', 0))
    # the blooming (bars 9-16): the phrase returns grown — a third
    # higher, fuller — the nightingale forgetting thrace; then a single
    # quiet echo as the blossom settles.
    pn.append((36, 'on', 'E4', 9));   pn.append((38, 'off', 'E4', 0))
    pn.append((38, 'on', 'G4', 9));   pn.append((40, 'off', 'G4', 0))
    pn.append((40, 'on', 'C5', 9));   pn.append((42, 'off', 'C5', 0))
    pn.append((42, 'on', 'E5', 9));   pn.append((48, 'off', 'E5', 0))
    pn.append((52, 'on', 'C5', 7));   pn.append((56, 'off', 'C5', 0))
    # the thousand years (bars 17-20): one long held note joining the
    # bloom — the flower's time, no hurry anywhere.
    pn.append((64, 'on', 'E4', 8));   pn.append((80, 'off', 'E4', 0))
    # the ending (bars 21-24): the piano is silent — the music does not
    # return to its beginning; the seed's voice is done.

    # ---- the bloom: long warm holds from bar 9 to the end.
    pd.append((32, 'on', 'C3', 9));   pd.append((64, 'off', 'C3', 0))
    pd.append((64, 'on', 'C3', 9));   pd.append((80, 'off', 'C3', 0))
    pd.append((80, 'on', 'A3', 8));   pd.append((96, 'off', 'A3', 0))

    # ---- the mortal: the slow walk through the thousand years, then
    # the final line — the last word, low and held, on the chord the
    # opening never prepared.
    vc.append((64, 'on', 'G1', 8));   vc.append((68, 'off', 'G1', 0))
    vc.append((68, 'on', 'F1', 8));   vc.append((72, 'off', 'F1', 0))
    vc.append((72, 'on', 'E1', 8));   vc.append((76, 'off', 'E1', 0))
    vc.append((76, 'on', 'D1', 8));   vc.append((80, 'off', 'D1', 0))
    vc.append((80, 'on', 'D2', 8));   vc.append((84, 'off', 'D2', 0))
    vc.append((84, 'on', 'C2', 8));   vc.append((88, 'off', 'C2', 0))
    vc.append((88, 'on', 'A1', 8));   vc.append((92, 'off', 'A1', 0))
    vc.append((92, 'on', 'D2', 8));   vc.append((96, 'off', 'D2', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, vc)

    return mc.compose('athanasia.mid', tracks, tempo=54)


if __name__ == '__main__':
    athanasia()
    print('composed athanasia.mid')
