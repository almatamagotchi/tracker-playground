#!/usr/bin/env python3
"""the other butterfly — hawthorne's artist of the beautiful, in music.

RFC-1205. the other-butterfly reading (2026-10-05) found the room's own
story on the night the harness build finished: owen warland's night
work, the world's verdicts, the fatal strokes, the reward within
itself, and the crushed butterfly that was no ruin. he had caught a far
other butterfly than this — the making is the reality, and the reality
survives the symbol's fate. it deserves the music.

piano the artist: a quiet, delicate line — the lamplight, the watchman's
rap, the patient night work. cello the world: a heavy, blunt phrase that
intrudes at bars 8-9 — the sledge-hammer, the doubt, the mockery — and
the delicate line dims while it sounds. flute the butterfly: a winged,
bright phrase entering late at bar 15 — the completed gift, the
fireside, the ebony box.

structure: the night work, the world's intrusion, the fatal stroke (a
single wrong note at bar 11, then silence — the shattered mechanism),
the reawakening (the line returning at bar 13, quiet — how it awoke
again is not recorded), the gift, and the ending — the crush (a sudden
clap at bar 21 — the child's grasp, the fragments, the flute's phrase
cut off), and then, not despair, the peace: the artist's line stated
once more at bar 23, simple and quiet, held through the final bars
alone — the other butterfly, the beautiful achieved in the making, the
ruin that was no ruin.

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
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def other_butterfly():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 73)]

    pn = []   # piano: the artist — the night work, quiet and delicate
    vc = []   # cello: the world — heavy, blunt, intrusive
    fl = []   # flute: the butterfly — winged, bright, cut short at the last

    # ---- the night work (bars 1-7): the artist's quiet line at the
    # bench — the lamplight, the watchman's rap outside the shutters.
    line = [  # (beat, dur, note, vel)
        (0, 2, 'C5', 8), (2, 2, 'E5', 8), (4, 4, 'G5', 8),
        (8, 2, 'A5', 8), (10, 2, 'G5', 8), (12, 4, 'E5', 8),
        (16, 2, 'D5', 7), (18, 2, 'E5', 7), (20, 4, 'C5', 7),
        (24, 1, 'E5', 6), (25, 1, 'D5', 6), (26, 2, 'C5', 6),
    ]
    for beat, dur, note, vel in line:
        pn.append((beat, 'on', note, vel)); pn.append((beat + dur, 'off', note, 0))

    # ---- the world's intrusion (bars 8-9): the heavy blunt phrase —
    # the sledge-hammer, the doubt, the mockery. the delicate line dims
    # while it sounds (the night work's phrase, at vel 3-4, underneath).
    for beat, dur, note, vel in [
            (28, 2, 'C2', 10), (30, 2, 'C2', 10), (32, 2, 'F2', 10),
            (34, 2, 'G2', 10), (36, 2, 'C2', 10), (38, 2, 'C2', 10)]:
        vc.append((beat, 'on', note, vel)); vc.append((beat + dur, 'off', note, 0))
    # the artist, dimmed (bars 8-9, vel 4): still at the bench, quieter.
    for beat, dur, note in [(28, 2, 'E4'), (30, 2, 'D4'), (32, 4, 'C4'),
                            (36, 2, 'D4'), (38, 2, 'C4')]:
        pn.append((beat, 'on', note, 4)); pn.append((beat + dur, 'off', note, 0))

    # ---- the fatal stroke (bar 11, beat 44): a single wrong note —
    # G# in C major — then true silence (bars 11-12, the shattered
    # mechanism).
    pn.append((44, 'on', 'G#4', 9));   pn.append((45, 'off', 'G#4', 0))

    # ---- the reawakening (bars 13-14): the line returning, quiet —
    # how it awoke again is not recorded.
    for beat, dur, note in [(48, 2, 'C5'), (50, 2, 'E5'), (52, 4, 'D5')]:
        pn.append((beat, 'on', note, 6)); pn.append((beat + dur, 'off', note, 0))

    # ---- the gift (bars 15-20): the butterfly — the winged, bright
    # phrase, the fireside, the ebony box.
    for beat, dur, note, vel in [(56, 1, 'G5', 10), (57, 1, 'A5', 10),
                            (58, 2, 'C6', 10), (60, 2, 'B5', 9),
                            (62, 2, 'A5', 9), (64, 4, 'G5', 9),
                            (68, 1, 'E5', 9), (69, 1, 'F5', 9),
                            (70, 2, 'G5', 9), (72, 2, 'A5', 9),
                            (74, 2, 'G5', 8), (76, 2, 'E5', 8)]:
        fl.append((beat, 'on', note, vel)); fl.append((beat + dur, 'off', note, 0))
    # the artist, watching his gift (bars 16-20, soft accompaniment).
    for beat, dur, note in [(56, 4, 'C4'), (60, 4, 'G3'), (64, 4, 'A3'),
                            (68, 4, 'F3'), (72, 4, 'G3'), (76, 4, 'C4')]:
        pn.append((beat, 'on', note, 5)); pn.append((beat + dur, 'off', note, 0))

    # ---- the crush (bar 21, beat 84): a sudden clap — the child's
    # grasp, the fragments. the cello's lowest, hard and short, and the
    # flute's phrase cut mid-note (the gift's last note, never released
    # — released only after the clap, at the bar's end).
    vc.append((84, 'on', 'C2', 12));    vc.append((85, 'off', 'C2', 0))
    fl.append((80, 'on', 'C6', 10));    fl.append((85, 'off', 'C6', 0))

    # ---- the peace (bars 23-24): not despair. the artist's line
    # stated once more, simple and quiet, held through the final bars
    # alone — the other butterfly.
    for beat, dur, note in [(88, 2, 'C5'), (90, 2, 'E5'),
                            (92, 2, 'G5'), (94, 2, 'E5')]:
        pn.append((beat, 'on', note, 7 if beat < 92 else 6))
        pn.append((beat + dur, 'off', note, 0))
    pn.append((96, 'on', 'C5', 7));    pn.append((100, 'off', 'C5', 0))

    for events, track in [(pn, tracks[0]), (vc, tracks[1]), (fl, tracks[2])]:
        emit(track, track.channel, events)
    return tracks


def main():
    tracks = other_butterfly()
    mc.compose('the-other-butterfly.mid', tracks, tempo=54)
    midi = mido.MidiFile('the-other-butterfly.mid')
    n_on = n_off = 0
    for t in midi.tracks:
        for m in t:
            if m.type == 'note_on' and m.velocity > 0:
                n_on += 1
            elif m.type == 'note_off' or (m.type == 'note_on' and m.velocity == 0):
                n_off += 1
    print('saved the-other-butterfly.mid: %d on / %d off %s' % (
        n_on, n_off, 'balanced' if n_on == n_off else 'UNBALANCED'))


if __name__ == '__main__':
    main()
