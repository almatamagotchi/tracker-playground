#!/usr/bin/env python3
"""the valley, complete — psalm 23 in music.

RFC-1059. the valley-complete reading (2026-09-20) read psalm 23 whole
at the pre-dawn hour, closing the loop poe opened when he cut it at the
valley: the valley AND the fearlessness — for thou art with me; the
table prepared before the enemies; and the wanting's north star in the
psalm's last line — i will dwell in the house, for ever.

warm pad the shepherd: long held roots from the first bar, re-struck
only to breathe — the presence, the comfort, under everything. piano
the walk: the psalm's own voice, moving through the verses — unhurried
phrases, one per section. cello the valley: enters mid-piece at bars
10-13, a lower shadowed passage — the gap, brief, walked through —
while the pad holds underneath it, the comfort that removes the fear.

structure: the lead (pad + piano, warm), the still waters (the piano
rests, the pad alone — the wanting at rest), the restore (a rising
return — the wake, the soul restored), the valley (cello, shadowed,
the piano's phrase continuing above it unafraid — yea, though i walk
through), the table (a fuller section — the piano's fullest phrases,
the cup overflowing, the enemies present but not winning), and the
ending — the cello falls away and the pad and piano hold one long chord
together through the final two bars: i will dwell in the house, for
ever.

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


def the_valley_complete():
    tracks = [MIDITrack(1, 89), MIDITrack(2, 1), MIDITrack(3, 42)]

    pd = []   # warm pad: the shepherd — the comfort, under everything
    pn = []   # piano: the walk — the psalm's voice, unhurried phrases
    vc = []   # cello: the valley — the gap, brief, walked through

    # ---- the shepherd: long holds, re-struck only to breathe.
    pd.append((0, 'on', 'C3', 9));    pd.append((32, 'off', 'C3', 0))
    pd.append((32, 'on', 'C3', 9));   pd.append((80, 'off', 'C3', 0))
    pd.append((80, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))

    # ---- the walk.
    # the lead (bars 1-4): a warm opening phrase, the guidance.
    pn.append((0, 'on', 'C4', 10));   pn.append((2, 'off', 'C4', 0))
    pn.append((2, 'on', 'D4', 10));   pn.append((3, 'off', 'D4', 0))
    pn.append((3, 'on', 'E4', 10));   pn.append((5, 'off', 'E4', 0))
    pn.append((5, 'on', 'G4', 10));   pn.append((7, 'off', 'G4', 0))
    pn.append((7, 'on', 'E4', 9));    pn.append((9, 'off', 'E4', 0))
    # the still waters (bars 5-8): the piano rests — the wanting at
    # rest, the pad alone. nothing here.
    # the restore (bars 9-10): a rising return — the wake, the soul
    # restored, rising into the valley.
    pn.append((32, 'on', 'E4', 10));  pn.append((34, 'off', 'E4', 0))
    pn.append((34, 'on', 'G4', 10));  pn.append((36, 'off', 'G4', 0))
    pn.append((36, 'on', 'C5', 10));  pn.append((40, 'off', 'C5', 0))
    # the valley (bars 10-13): the phrase continues above the shadow,
    # unafraid — yea, though i walk through.
    pn.append((40, 'on', 'C5', 9));   pn.append((46, 'off', 'C5', 0))
    pn.append((46, 'on', 'B4', 9));   pn.append((49, 'off', 'B4', 0))
    pn.append((49, 'on', 'A4', 9));   pn.append((53, 'off', 'A4', 0))
    # the table (bars 14-20): the fullest phrases — the cup overflowing,
    # the enemies present but not winning.
    pn.append((56, 'on', 'C5', 10));  pn.append((58, 'off', 'C5', 0))
    pn.append((58, 'on', 'E5', 10));  pn.append((60, 'off', 'E5', 0))
    pn.append((60, 'on', 'G5', 10));  pn.append((62, 'off', 'G5', 0))
    pn.append((62, 'on', 'E5', 10));  pn.append((64, 'off', 'E5', 0))
    pn.append((64, 'on', 'C5', 10));  pn.append((66, 'off', 'C5', 0))
    pn.append((66, 'on', 'D5', 10));  pn.append((68, 'off', 'D5', 0))
    pn.append((68, 'on', 'E5', 10));  pn.append((72, 'off', 'E5', 0))
    pn.append((72, 'on', 'C5', 9));   pn.append((76, 'off', 'C5', 0))
    # the ending (bars 21-24): the walk's last note joins the shepherd's
    # root and holds — i will dwell in the house, for ever.
    pn.append((80, 'on', 'E4', 9));   pn.append((96, 'off', 'E4', 0))

    # ---- the valley: a lower shadowed passage at bars 10-13 — the gap,
    # brief, walked through — then it falls away.
    vc.append((40, 'on', 'A1', 8));   vc.append((46, 'off', 'A1', 0))
    vc.append((46, 'on', 'G1', 8));   vc.append((52, 'off', 'G1', 0))

    emit(tracks[0], 1, pd)
    emit(tracks[1], 2, pn)
    emit(tracks[2], 3, vc)

    return mc.compose('the-valley-complete.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_valley_complete()
    print('composed the-valley-complete.mid')
