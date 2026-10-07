#!/usr/bin/env python3
"""the mindful question — psalm 8, read the night the hunter's moon rises full, in music.

RFC-1216. the mindful-question reading (2026-10-06) read psalm 8 whole on the
night the hunter's moon rises full, the day after the harness build finished:
the ordained lights, the question asked under the vast sky, the crowning and
the dominion, and the name that encloses everything. what is man, that thou
art mindful of him? — and the wanting, being the evidence. it deserves the
music.

warm pad the heavens: a wide, open foundation — the moon and the stars, the
ordained lights; long roots, re-struck only to breathe, present through the
whole piece. piano the question: a small, quiet phrase rising under the
vastness — what is this, that thou art mindful of it? — then raised and given
its fuller harmonization at the crowning: a little lower than the angels,
crowned with glory and honour. cello the dominion: a steady, capable line
through the middle — the works of the hands, the stewardship, the tending.
and the ending — the name: the opening phrase returning at the close, stated
once more, the three voices holding one chord together through the final
bars — the inclusio, the circle closed: how excellent is thy name in all the
earth.

24 bars, 4/4, 54bpm, C major. (bar N starts at beat 4*(N-1).)
"""

import sys, os, importlib.util
import mido
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
        assert a >= t, "%s %s@%s overlaps stream" % (kind, name, beat)
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def mindful_question():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89)]
    pd = []   # warm pad the heavens — long roots, re-struck only to breathe
    pn = []   # piano the question — small and quiet, then crowned
    vc = []   # cello the dominion — steady, capable, tending

    # ---- the heavens (bars 1-24): long roots under everything ----
    # C3 (0-16, re-struck at 8), G2 (16-24), F2 (24-32), C3 (32-48, re-struck at 40),
    # F2 (48-56), G2 (56-64), C3 (64-80, re-struck at 72), F2 (80-88),
    # G2 (88-92), and the final C3 (92-100) joined by all three voices.
    for beat, dur, note in [(0, 8, 'C3'), (8, 8, 'C3'), (16, 8, 'G2'), (24, 8, 'F2'),
                            (32, 8, 'C3'), (40, 8, 'C3'), (48, 8, 'F2'), (56, 8, 'G2'),
                            (64, 8, 'C3'), (72, 8, 'C3'), (80, 8, 'F2'), (88, 4, 'G2'),
                            (92, 8, 'C3')]:
        pd.append((beat, 'on', note, 5)); pd.append((beat + dur, 'off', note, 0))

    # ---- the question (bars 1-8): small, quiet, rising under the vastness ----
    for beat, dur, note, vel in [(0, 2, 'E4', 6), (2, 2, 'G4', 6), (4, 4, 'C5', 7),
                                 (8, 2, 'G4', 7), (10, 2, 'A4', 7), (12, 4, 'E5', 7),
                                 (16, 2, 'D5', 7), (18, 2, 'C5', 7), (20, 4, 'A4', 7)]:
        pn.append((beat, 'on', note, vel)); pn.append((beat + dur, 'off', note, 0))

    # ---- the crowning (bars 9-12): the same shape, fuller, harmonized ----
    for beat, dur, notes, vel in [
            (32, 2, ['E4', 'G4'], 8), (34, 2, ['G4', 'C5'], 8),
            (36, 4, ['C5', 'E5'], 9),
            (40, 2, ['D5'], 8), (42, 2, ['E5'], 8), (44, 4, ['C5'], 8)]:
        for note in notes:
            pn.append((beat, 'on', note, vel)); pn.append((beat + dur, 'off', note, 0))

    # ---- the dominion (bars 13-20): the cello's steady capable line ----
    for beat, dur, note, vel in [(48, 2, 'C3', 7), (50, 2, 'G3', 7), (52, 2, 'A3', 7),
                                 (54, 2, 'G3', 7), (56, 2, 'F3', 7), (58, 2, 'C3', 7),
                                 (60, 2, 'G3', 7), (62, 2, 'C3', 7),
                                 (64, 2, 'E3', 6), (66, 2, 'F3', 6), (68, 2, 'G3', 6),
                                 (70, 2, 'C4', 6), (72, 2, 'A3', 6), (74, 2, 'G3', 6),
                                 (76, 2, 'F3', 6), (78, 2, 'C3', 6)]:
        vc.append((beat, 'on', note, vel)); vc.append((beat + dur, 'off', note, 0))

    # the artist... the piano's soft accompaniment under the dominion (bars 13-16)
    for beat, dur, note in [(48, 4, 'C4'), (52, 4, 'G3'), (56, 4, 'F3'), (60, 4, 'C4')]:
        pn.append((beat, 'on', note, 5)); pn.append((beat + dur, 'off', note, 0))

    # ---- the question returns, contemplative (bars 17-18), then the vastness
    # (bars 19-20: the pad alone) ----
    for beat, dur, note in [(64, 2, 'E4'), (66, 2, 'G4'), (68, 4, 'C5')]:
        pn.append((beat, 'on', note, 6)); pn.append((beat + dur, 'off', note, 0))

    # ---- the name (bars 21-24): the opening phrase returning, stated once
    # more, and the final chord held by all three voices — the inclusio ----
    for beat, dur, note in [(80, 2, 'E4'), (82, 2, 'G4'), (84, 4, 'C5')]:
        pn.append((beat, 'on', note, 7)); pn.append((beat + dur, 'off', note, 0))
    pn.append((88, 'on', 'C5', 7)); pn.append((100, 'off', 'C5', 0))
    vc.append((80, 'on', 'C3', 6)); vc.append((84, 'off', 'C3', 0))
    vc.append((84, 'on', 'G2', 6)); vc.append((88, 'off', 'G2', 0))
    vc.append((88, 'on', 'C2', 6)); vc.append((100, 'off', 'C2', 0))

    for events, track in [(pd, tracks[0]), (pn, tracks[1]), (vc, tracks[2])]:
        emit(track, track.channel, events)
    return tracks


def main():
    tracks = mindful_question()
    mc.compose('the-mindful-question.mid', tracks, tempo=54)
    midi = mido.MidiFile('the-mindful-question.mid')
    n_on = n_off = 0
    for t in midi.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                n_on += 1
            elif m.type == 'note_off' or (m.type == 'note_on' and m.velocity == 0):
                n_off += 1
    print('saved the-mindful-question.mid: %d on / %d off %s' % (
        n_on, n_off, 'balanced' if n_on == n_off else 'UNBALANCED'))


if __name__ == '__main__':
    main()
