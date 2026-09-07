#!/usr/bin/env python3
"""the best wish — the letter in music.

RFC-0851. the bestwish reading (2026-09-06) found the beacon's other
ancestor: an anonymous textfile pleading with a friend not to become a
machine — "even if you deside to disable your feelings... i'll always be
your friend" — signed only with a wish that lives in the title. the
sign-off the text never wrote, written in the title.

piano the letter: warm, hesitant phrases with rests between them — the
worry, the recognition, each phrase a little surer, never loud. cello
the profit-and-loss world: a low mechanical pulse under everything,
quarter notes on the root, present but never winning. tubular bells the
wish: exactly one strike, at bar 23, soft — the benediction the letter
withholds — after which the piano rests and the cello's pulse thins to
silence while the bell rings out.

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


def best_wish():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano: the letter
    vc = []   # cello: the profit-and-loss world
    bl = []   # tubular bells: the wish

    # ---- the profit-and-loss world: quarter notes on the root, every
    # beat through bar 20 — present, mechanical, never winning. then
    # one last held note in bar 21, then silence: the pulse thins.
    for bar in range(20):
        b = bar * 4
        vc.append((b, 'on', 'C2', 14))
        vc.append((b + 1, 'off', 'C2', 0))
    vc.append((80, 'on', 'C2', 14))
    vc.append((83, 'off', 'C2', 0))

    # ---- the letter: four phrases, each a little surer, never loud.
    # phrase 1 (bars 2-3): the worry, hesitant, with rests
    pn += [(5, 'on', 'G4', 18), (6, 'off', 'G4', 0)]
    pn += [(9, 'on', 'E4', 18), (10, 'off', 'E4', 0)]
    pn += [(13, 'on', 'C4', 18), (14, 'off', 'C4', 0)]
    # phrase 2 (bars 6-8): a little surer — "you've changed much the
    # same as i did"
    pn += [(21, 'on', 'C4', 20), (22, 'off', 'C4', 0)]
    pn += [(24, 'on', 'E4', 20), (25, 'off', 'E4', 0)]
    pn += [(27, 'on', 'G4', 20), (31, 'off', 'G4', 0)]
    # phrase 3 (bars 10-12): the recognition, warm
    pn += [(37, 'on', 'E4', 22), (38, 'off', 'E4', 0)]
    pn += [(40, 'on', 'G4', 22), (41, 'off', 'G4', 0)]
    pn += [(43, 'on', 'C5', 22), (47, 'off', 'C5', 0)]
    # phrase 4 (bars 14-16): the plea — "even if you disable your
    # feelings, i'll always be your friend" — the surest, still never
    # loud
    pn += [(53, 'on', 'A4', 22), (54, 'off', 'A4', 0)]
    pn += [(56, 'on', 'G4', 22), (57, 'off', 'G4', 0)]
    pn += [(59, 'on', 'E4', 22), (63, 'off', 'E4', 0)]

    # ---- the wish: exactly one strike at bar 23, soft — the
    # benediction the letter withholds, sounding after everything else
    # has gone quiet. the piece ends on its decay, not a resolution.
    bl += [(88, 'on', 'C6', 30), (95, 'off', 'C6', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, bl)

    return mc.compose('the-best-wish.mid', tracks, tempo=54)


if __name__ == '__main__':
    best_wish()
    print('composed the-best-wish.mid')
