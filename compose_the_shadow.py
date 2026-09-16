#!/usr/bin/env python3
"""the shadow — poe's parable, in music.

RFC-0994. the shadow-parable reading (2026-09-15) found the dead
writer's address to the living reader on tuesday afternoon, the day
after the war prayer: the sealed chamber, the song that fades, the
shadow that rises from where the song departed, and the voice that
speaks in the accents of many thousand departed friends. the shadow is
born where the song dies. it deserves the music.

warm pad the chamber: held chords through the whole piece, pallid and
motionless — the sealed room, the seven lamps, dimming as the piece
goes. piano the song: bright phrases that fade, each statement a little
weaker than the last — the songs of anacreon, which are madness; the
merriment of those who are to die. cello the shadow: enters at bar 13,
from where the last piano note dies — low, formless, unhurried; not
singing, speaking — and at bar 19 answers a single rising interval with
its name, the lowest notes of the piece: i am shadow, and my dwelling
is near to the catacombs. the ending: the piano does not return; the
shadow rests on the brass door and moves not — the cello holds one long
low tone through the final two bars while the chamber's chords dim to
near silence, and the piece ends there, still, with the reader
beginning.

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


def the_shadow():
    tracks = [MIDITrack(1, 89), MIDITrack(2, 1), MIDITrack(3, 42)]

    pd = []   # warm pad: the chamber
    pn = []   # piano: the song
    vc = []   # cello: the shadow

    # ---- the chamber: held chords, pallid and motionless, dimming as
    # the piece goes. re-struck only to breathe. the seven lamps.
    for start, vel in [(0, 10), (24, 9), (48, 8), (72, 7)]:
        for name in ['C3', 'E3']:
            pd.append((start, 'on', name, vel))
            pd.append((start + 24, 'off', name, 0))

    # ---- the song: bright phrases that fade, each statement a little
    # weaker than the last — the songs of anacreon, which are madness.
    statements = [
        (0, 'G4', 12, 2), (2, 'A4', 12, 2), (4, 'C5', 12, 2), (6, 'E5', 12, 3),
        (16, 'G4', 11, 2), (18, 'A4', 11, 2), (20, 'C5', 11, 3),
        (32, 'G4', 10, 2), (34, 'A4', 10, 3),
        (44, 'C5', 9, 3),
    ]
    for b, name, vel, hold in statements:
        pn.append((b, 'on', name, vel))
        pn.append((b + hold, 'off', name, 0))

    # ---- the shadow: enters at bar 13 (beat 48), from where the last
    # piano note dies. low, formless, unhurried — not singing, speaking.
    vc.append((48, 'on', 'G1', 11))
    vc.append((56, 'off', 'G1', 0))
    vc.append((56, 'on', 'E1', 11))
    vc.append((64, 'off', 'E1', 0))
    vc.append((64, 'on', 'C1', 11))
    vc.append((72, 'off', 'C1', 0))
    # ---- bar 19: a single rising interval — the question — then the
    # name, the lowest notes of the piece.
    vc.append((72, 'on', 'D1', 10))
    vc.append((76, 'off', 'D1', 0))
    vc.append((76, 'on', 'C1', 10))
    vc.append((84, 'off', 'C1', 0))
    # ---- the ending: the shadow rests on the brass door and moves not
    # — one long low tone through the final two bars, while the chamber
    # dims to near silence. the piece ends still, with the reader
    # beginning.
    vc.append((88, 'on', 'C1', 9))
    vc.append((96, 'off', 'C1', 0))

    emit(tracks[0], 1, pd)
    emit(tracks[1], 2, pn)
    emit(tracks[2], 3, vc)

    return mc.compose('the-shadow.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_shadow()
    print('composed the-shadow.mid')
