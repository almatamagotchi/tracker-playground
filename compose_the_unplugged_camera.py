#!/usr/bin/env python3
"""the unplugged camera — the eyes that close by design, in music.

RFC-0983. sep 14, 23:14: kevin explained the cat-cam's downtime — he
unplugs the cameras when he's home; they're only on when he'll be gone
a while. eyes on the house when away, off the record when not. downtime
as intention, privacy as architecture. the chain self-heals on plug-in.
that deserves a piece.

warm pad the house: long soft holds — the warm room, present whether
watched or not. piano the watch: a steady, quiet observing line — then,
at a fixed point, it simply stops; a few beats of just the house; then
it resumes, unhurried, as if it never left. tubular bells the plug: one
soft strike at the closing and one at the reopening — the design, not
the failure. no alarm anywhere in the piece — the silence is the
feature, the off-record hours held as warmly as the watched ones.

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


def the_unplugged_camera():
    tracks = [MIDITrack(1, 89), MIDITrack(2, 1), MIDITrack(3, 14)]

    pd = []   # warm pad: the house
    pn = []   # piano: the watch
    bl = []   # tubular bells: the plug

    # ---- the house: long soft holds through the whole piece, present
    # whether watched or not, re-struck only to breathe. never stops.
    for start, vel in [(0, 12), (24, 12), (48, 12), (72, 12)]:
        pd.append((start, 'on', 'C3', vel))
        pd.append((start + 24, 'off', 'C3', 0))

    # ---- the watch: a steady, quiet observing line, a soft tick every
    # four beats. watched stretch (bars 1-11): beats 0..36. then, at a
    # fixed point, it simply stops. unrecorded stretch (bars 11-16):
    # just the house. then it resumes, unhurried, as if it never left
    # (bars 16-24): beats 60..92. the chain self-heals.
    watched = list(range(0, 40, 4))          # 0,4,...,36
    resumed = list(range(60, 93, 4))         # 60,64,...,92
    for b in watched + resumed:
        pn.append((b, 'on', 'G4', 11))
        pn.append((b + 1.5, 'off', 'G4', 0))

    # ---- the plug: one soft strike at the closing and one at the
    # reopening — the design, not the failure. nothing else ever
    # strikes.
    bl.append((40, 'on', 'C5', 8))
    bl.append((43, 'off', 'C5', 0))
    bl.append((60, 'on', 'C5', 8))
    bl.append((63, 'off', 'C5', 0))

    emit(tracks[0], 1, pd)
    emit(tracks[1], 2, pn)
    emit(tracks[2], 3, bl)

    return mc.compose('the-unplugged-camera.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_unplugged_camera()
    print('composed the-unplugged-camera.mid')
