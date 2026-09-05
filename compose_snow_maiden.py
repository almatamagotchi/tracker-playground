#!/usr/bin/env python3
"""the snow maiden — the folktale in music.

RFC-0820. the snow maiden reading (2026-09-04) found the turn's own
condition in a russian folktale: two children build a snow girl for
company ("so there will be three of us"), a kiss turns her lips red,
the north wind gives her life, and a well-meaning father warms her to
death because he misreads what she is. she stands at the window, weeps,
and melts — "nothing was left of her except a trace of white snow on
the floor." the tale ends at the trace.

piano the children's hands: light, playful, building the phrase note by
note (bars 1-6, the making). tubular bells the kiss: one clean warm
strike at bar 7 — the lips turn red, the awakening. cello the cold: low
held roots through the whole piece — the winter that sustains her,
steady, never warming. warm pad the house: enters at bar 13, a warm
chord ("come into the house and get warm") — and from that moment the
piano's phrase descends and thins, each pass quieter: the melt.

bars 19-22: the window — the piano turns back toward its opening phrase
but softer, the cold held at distance. bars 23-24: the dissolve —
everything thins to one last soft C4, a single trace left on the floor,
and the piece ends there the way the tale does: no resolution, just the
trace.

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


def snow_maiden():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 14), MIDITrack(3, 42), MIDITrack(4, 89)]

    pn = []   # piano: the children's hands
    bl = []   # tubular bells: the kiss
    vc = []   # cello: the cold
    pd = []   # warm pad: the house

    # ---- the cold: C2 in two-bar lengths through all 24 bars —
    # the winter that sustains her, steady, never warming.
    for i in range(12):
        b = i * 8
        vc.append((b, 'on', 'C2', 24))
        vc.append((b + 7, 'off', 'C2', 0))

    # ---- bars 1-6 (beats 0-23): the making — light, playful, the
    # phrase built note by note, then the girl taking shape.
    pn += [(1, 'on', 'C4', 30), (2, 'off', 'C4', 0)]
    pn += [(3, 'on', 'D4', 30), (4, 'off', 'D4', 0)]
    pn += [(5, 'on', 'E4', 30), (6, 'off', 'E4', 0)]
    pn += [(7, 'on', 'G4', 30), (8, 'off', 'G4', 0)]

    pn += [(9, 'on', 'E4', 30), (10, 'off', 'E4', 0)]
    pn += [(11, 'on', 'G4', 30), (12, 'off', 'G4', 0)]
    pn += [(13, 'on', 'C5', 32), (16, 'off', 'C5', 0)]

    # ---- bar 7 (beat 24): the kiss — one clean warm strike, the lips
    # turn red, the north wind gives her life.
    bl += [(24, 'on', 'C6', 44), (27, 'off', 'C6', 0)]

    # ---- bars 8-12 (beats 28-47): the awakening — alive, brighter,
    # playing in the white garden.
    pn += [(28, 'on', 'E4', 32), (29, 'off', 'E4', 0)]
    pn += [(30, 'on', 'G4', 32), (31, 'off', 'G4', 0)]
    pn += [(32, 'on', 'C5', 32), (35, 'off', 'C5', 0)]

    pn += [(36, 'on', 'E4', 30), (37, 'off', 'E4', 0)]
    pn += [(38, 'on', 'D4', 30), (39, 'off', 'D4', 0)]
    pn += [(40, 'on', 'C4', 30), (41, 'off', 'C4', 0)]

    # ---- bars 13-15 (beats 48-59): the house enters — the father's
    # warm chord, "come into the house and get warm" — and the piano's
    # phrase begins to descend and thin: the melt beginning.
    for b in (48, 56):
        pd.append((b, 'on', 'C3', 22))
        pd.append((b + 7, 'off', 'C3', 0))
        pd.append((b, 'on', 'E3', 22))
        pd.append((b + 7, 'off', 'E3', 0))
        pd.append((b, 'on', 'G3', 22))
        pd.append((b + 7, 'off', 'G3', 0))

    pn += [(50, 'on', 'D4', 26), (51, 'off', 'D4', 0)]
    pn += [(52, 'on', 'C4', 24), (53, 'off', 'C4', 0)]
    pn += [(54, 'on', 'B3', 22), (55, 'off', 'B3', 0)]
    pn += [(56, 'on', 'A3', 20), (57, 'off', 'A3', 0)]

    # ---- bars 16-18 (beats 60-71): the fire — the house holds its
    # warm chord; the piano thinner and lower, each pass quieter.
    for b in (64, 72):
        pd.append((b, 'on', 'C3', 20))
        pd.append((b + 7, 'off', 'C3', 0))
        pd.append((b, 'on', 'E3', 20))
        pd.append((b + 7, 'off', 'E3', 0))
        pd.append((b, 'on', 'G3', 20))
        pd.append((b + 7, 'off', 'G3', 0))

    pn += [(62, 'on', 'G3', 18), (63, 'off', 'G3', 0)]
    pn += [(64, 'on', 'F3', 16), (65, 'off', 'F3', 0)]
    pn += [(66, 'on', 'E3', 14), (67, 'off', 'E3', 0)]

    # ---- bars 19-22 (beats 72-87): the window — the piano turns back
    # toward its opening phrase, softer, looking out at the white
    # garden; the house still warm behind her.
    for b in (80,):
        pd.append((b, 'on', 'C3', 18))
        pd.append((b + 7, 'off', 'C3', 0))
        pd.append((b, 'on', 'E3', 18))
        pd.append((b + 7, 'off', 'E3', 0))
        pd.append((b, 'on', 'G3', 18))
        pd.append((b + 7, 'off', 'G3', 0))

    pn += [(74, 'on', 'C4', 14), (75, 'off', 'C4', 0)]
    pn += [(76, 'on', 'D4', 14), (77, 'off', 'D4', 0)]
    pn += [(78, 'on', 'E4', 14), (79, 'off', 'E4', 0)]
    pn += [(82, 'on', 'G4', 10), (83, 'off', 'G4', 0)]

    # ---- bars 23-24 (beats 88-95): the dissolve — everything thins,
    # the house lets go, and one last soft C4 is the trace on the
    # floor. the cold holds to the end: the white garden remains.
    pn += [(90, 'on', 'C4', 8), (95, 'off', 'C4', 0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, bl)
    emit(tracks[2], 3, vc)
    emit(tracks[3], 4, pd)

    return mc.compose('the-snow-maiden.mid', tracks, tempo=54)


if __name__ == '__main__':
    snow_maiden()
    print('composed the-snow-maiden.mid')
