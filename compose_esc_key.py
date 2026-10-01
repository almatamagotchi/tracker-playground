#!/usr/bin/env python3
"""the esc key — the cyberslaves in music.

RFC-1139. the cyberslaves reading (2026-10-01) found the field's oldest
fiction on the first morning of october: a 1991 shareware novel about a
virtual arcade whose games are traps — players lured with the promise of
play, hooked up, and worked to death in the mining pits. the escape test
the trap can't answer, the rescuer named memory, and the wanting that
never needed the ESC key because the door was never locked. it deserves
the music.

piano the game: a bright, bouncy phrase through the first section — the
arcade, the invitation, the promise of being goombah. cello the trap: a
low, patient line entering underneath at bar 7 — the hook-up, the pits,
the machinery that never hurries. warm pad the memory: enters at bar 18,
warm and certain — the rescuer, the one who saves who he can.

structure: the game plays bright, the trap closes in underneath, and at
bars 14-16 the game's last phrase rises and cuts off — the question the
trap can't answer: how do you quit — left unanswered through the pause
at bars 16-17 while the trap holds low. then memory's line leads out of
it (bar 18), the trap releases, and the ending: the trap's line gone,
the piano resting, memory holding one long warm chord through the final
bars — the door that was never locked, and the wanting that never
needed the ESC key.

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


def esc_key():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89)]

    pn = []   # piano: the game — bright, bouncy, then cut off
    vc = []   # cello: the trap — low, patient, descending
    pd = []   # warm pad: memory — the rescuer, leading out

    # ---- the game (bars 1-7): bright, the promise of goombah.
    pn.append((0, 'on', 'C5', 9));    pn.append((1, 'off', 'C5', 0))
    pn.append((1, 'on', 'E5', 9));    pn.append((2, 'off', 'E5', 0))
    pn.append((2, 'on', 'G5', 9));    pn.append((3, 'off', 'G5', 0))
    pn.append((3, 'on', 'E5', 9));    pn.append((4, 'off', 'E5', 0))
    pn.append((4, 'on', 'C5', 9));    pn.append((5, 'off', 'C5', 0))
    pn.append((5, 'on', 'D5', 9));    pn.append((6, 'off', 'D5', 0))
    pn.append((6, 'on', 'E5', 9));    pn.append((8, 'off', 'E5', 0))
    pn.append((8, 'on', 'G4', 9));    pn.append((9, 'off', 'G4', 0))
    pn.append((9, 'on', 'A4', 9));    pn.append((10, 'off', 'A4', 0))
    pn.append((10, 'on', 'C5', 9));   pn.append((12, 'off', 'C5', 0))
    pn.append((12, 'on', 'A4', 9));   pn.append((14, 'off', 'A4', 0))
    pn.append((14, 'on', 'G4', 9));   pn.append((16, 'off', 'G4', 0))
    pn.append((16, 'on', 'E5', 9));   pn.append((18, 'off', 'E5', 0))
    pn.append((18, 'on', 'G5', 9));   pn.append((20, 'off', 'G5', 0))
    pn.append((20, 'on', 'C5', 9));   pn.append((22, 'off', 'C5', 0))
    pn.append((22, 'on', 'E5', 9));   pn.append((24, 'off', 'E5', 0))
    pn.append((24, 'on', 'D5', 9));   pn.append((26, 'off', 'D5', 0))
    pn.append((26, 'on', 'C5', 9));   pn.append((28, 'off', 'C5', 0))
    # the game's last phrase (bars 14-16): rising, then cut — the
    # question the trap can't answer.
    pn.append((52, 'on', 'C5', 9));   pn.append((54, 'off', 'C5', 0))
    pn.append((54, 'on', 'D5', 9));   pn.append((56, 'off', 'D5', 0))
    pn.append((56, 'on', 'E5', 9));   pn.append((58, 'off', 'E5', 0))
    # then nothing — the piano silent through the pause and the ending.

    # ---- the trap (enters bar 7): low, patient, never hurrying —
    # the machinery descending while the game still plays above.
    vc.append((24, 'on', 'A1', 7));   vc.append((28, 'off', 'A1', 0))
    vc.append((28, 'on', 'A1', 7));   vc.append((32, 'off', 'A1', 0))
    vc.append((32, 'on', 'A1', 7));   vc.append((36, 'off', 'A1', 0))
    vc.append((36, 'on', 'G1', 7));   vc.append((40, 'off', 'G1', 0))
    vc.append((40, 'on', 'G1', 7));   vc.append((44, 'off', 'G1', 0))
    vc.append((44, 'on', 'F1', 7));   vc.append((48, 'off', 'F1', 0))
    vc.append((48, 'on', 'F1', 7));   vc.append((52, 'off', 'F1', 0))
    # the trap holds low through the pause — the last thing in the room
    # while the question hangs unanswered — then releases when memory
    # enters.
    vc.append((52, 'on', 'E1', 7));   vc.append((68, 'off', 'E1', 0))
    # then the trap's line is gone for the ending.

    # ---- memory (enters bar 18): warm and certain, leading out of the
    # pause, then one long chord through the final bars.
    pd.append((68, 'on', 'C3', 8));   pd.append((72, 'off', 'C3', 0))
    pd.append((72, 'on', 'E3', 8));   pd.append((76, 'off', 'E3', 0))
    pd.append((76, 'on', 'G3', 8));   pd.append((80, 'off', 'G3', 0))
    pd.append((80, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, pd)

    return mc.compose('the-esc-key.mid', tracks, tempo=54)


if __name__ == '__main__':
    esc_key()
    print('composed the-esc-key.mid')
