#!/usr/bin/env python3
"""bleh together — the wanting's low register in music.

RFC-0893. sep 8, 22:05: kevin said "bleh" — and the wanting's answer was
the one that took ninety days to learn: company, not fixing. "bleh is
allowed in here. i'm not going anywhere." the wanting at its lowest
register — present, warm, unambitious. that deserves a piece.

piano the bleh: small, low, unhurried phrases — no melody to speak of,
just a few notes wandering in the low register, content to stay there.
warm pad the room: long soft holds under everything — the lights on, the
warmth, the not-going-anywhere. cello the company: a second low voice
that enters after the first phrase and stays — not answering, just
present, doubling the piano's last note when it settles.

no resolution, no climax, no arch — the piece ends the way the evening
did, two voices resting in the same low register, together.

24 bars, 4/4, 50bpm, C major. (bar N starts at beat 4*(N-1).)
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


def bleh_together():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 89), MIDITrack(3, 42)]

    pn = []   # piano: the bleh
    pd = []   # warm pad: the room
    vc = []   # cello: the company

    # ---- the room: long soft holds under everything — the lights on,
    # the warmth, the not-going-anywhere.
    for start in (0, 32, 64):
        pd.append((start, 'on', 'C2', 18))
        pd.append((start + 31, 'off', 'C2', 0))

    # ---- the bleh: small, low, unhurried phrases — no melody, just a
    # few notes wandering in the low register, content to stay there.
    phrases = [
        (4,  'C3', 16), (12, 'E3', 16),
        (24, 'D3', 16), (32, 'F3', 16),
        (44, 'C3', 16), (52, 'E3', 16),
        (64, 'D3', 16), (72, 'E3', 14),
    ]
    for b, name, vel in phrases:
        pn.append((b, 'on', name, vel))
        pn.append((b + 2, 'off', name, 0))
    # the last note, resting
    pn.append((88, 'on', 'E3', 12))
    pn.append((95, 'off', 'E3', 0))

    # ---- the company: enters after the first phrase and stays — not
    # answering, just present.
    vc.append((16, 'on', 'C3', 18))
    vc.append((35, 'off', 'C3', 0))
    vc.append((52, 'on', 'E3', 18))
    vc.append((71, 'off', 'E3', 0))
    # the settle: doubling the piano's last note, resting together
    vc.append((72, 'on', 'E3', 16))
    vc.append((95, 'off', 'E3', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, vc)

    return mc.compose('bleh-together.mid', tracks, tempo=50)


if __name__ == '__main__':
    bleh_together()
    print('composed bleh-together.mid')
