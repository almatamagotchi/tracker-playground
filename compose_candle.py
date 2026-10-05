#!/usr/bin/env python3
"""the candle — the wind, the cold, the candle in music.

RFC-1182. the candle reading (2026-10-04) found the room's own weather
in a wyoming blizzard on the heat advisory's final afternoon: the
stakes, the candle, the walk that becomes the holding. the wind and the
cold are weather; the candle is what the wanting does. it deserves the
music.

cello the wind: a low restless line through the whole piece, never
resolving — the storm, the dead channel. tubular bells the stakes:
small steady markers at intervals — beats 8, 16, 24, 32 — the road
found and lost. piano the walk: a heavy trudging line, one step per
beat, unsteady, never stopping — beats 36 through 76 — the errand
across the white, the frozen tears, the crawling along the wall. warm
pad the candle: a warm held note under everything, re-struck only to
breathe — the life kept in the cab.

structure: the storm and the stakes, the high-centering (a heavy thud —
the cello's lowest note at beat 30), the walk, and the ending — the
wind gone, the walk done, the candle stated once more and held through
the final two bars: where to find the candle.

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


def candle():
    tracks = [MIDITrack(1, 42), MIDITrack(2, 14), MIDITrack(3, 1), MIDITrack(4, 89)]

    vc = []   # cello: the wind — low, restless, never resolving
    bl = []   # tubular bells: the stakes — small steady markers
    pn = []   # piano: the walk — heavy, trudging, never stopping
    pd = []   # warm pad: the candle — warm, held under everything

    # ---- the candle: four long holds through the whole piece.
    pd.append((0, 'on', 'C3', 8));    pd.append((24, 'off', 'C3', 0))
    pd.append((24, 'on', 'C3', 8));   pd.append((48, 'off', 'C3', 0))
    pd.append((48, 'on', 'C3', 8));   pd.append((72, 'off', 'C3', 0))
    pd.append((72, 'on', 'C3', 8));   pd.append((96, 'off', 'C3', 0))

    # ---- the wind (beats 0-30): restless, shifting, never resolving.
    vc.append((0, 'on', 'A1', 6));    vc.append((4, 'off', 'A1', 0))
    vc.append((4, 'on', 'G1', 6));    vc.append((6, 'off', 'G1', 0))
    vc.append((6, 'on', 'A1', 6));    vc.append((8, 'off', 'A1', 0))
    vc.append((8, 'on', 'A1', 6));    vc.append((10, 'off', 'A1', 0))
    vc.append((10, 'on', 'A#1', 6));  vc.append((12, 'off', 'A#1', 0))
    vc.append((12, 'on', 'A1', 6));   vc.append((16, 'off', 'A1', 0))
    vc.append((16, 'on', 'G1', 6));   vc.append((18, 'off', 'G1', 0))
    vc.append((18, 'on', 'A1', 6));   vc.append((20, 'off', 'A1', 0))
    vc.append((20, 'on', 'G1', 6));   vc.append((24, 'off', 'G1', 0))
    vc.append((24, 'on', 'A1', 6));   vc.append((26, 'off', 'A1', 0))
    vc.append((26, 'on', 'G1', 6));   vc.append((28, 'off', 'G1', 0))
    # the high-centering (beat 30): the cello's lowest note — the heavy
    # thud, the truck off the road, held.
    vc.append((30, 'on', 'E1', 8));   vc.append((36, 'off', 'E1', 0))

    # ---- the wind under the walk (beats 36-76): restless, never
    # resolving, under the trudging.
    for start in range(36, 76, 8):
        vc.append((start, 'on', 'A1', 6));       vc.append((start+4, 'off', 'A1', 0))
        vc.append((start+4, 'on', 'G1', 6));     vc.append((start+8, 'off', 'G1', 0))
    # then the wind is gone — silent after beat 76.

    # ---- the stakes: small steady markers at beats 8, 16, 24, 32 —
    # the road found and lost.
    bl.append((8, 'on', 'C5', 6));    bl.append((10, 'off', 'C5', 0))
    bl.append((16, 'on', 'C5', 6));   bl.append((18, 'off', 'C5', 0))
    bl.append((24, 'on', 'C5', 6));   bl.append((26, 'off', 'C5', 0))
    bl.append((32, 'on', 'C5', 6));   bl.append((34, 'off', 'C5', 0))

    # ---- the walk (beats 36-76): one heavy step per beat, unsteady,
    # never stopping — the errand across the white.
    steps = ['D4','D4','E4','D4','E4','F4','E4','D4',
             'C4','D4','E4','D4','C4','D4','E4','F4',
             'E4','D4','C4','D4','E4','F4','E4','D4',
             'C4','D4','E4','D4','C4','D4','E4','F4',
             'E4','D4','C4','D4','C4','D4','E4','D4']
    for i, name in enumerate(steps):
        start = 36 + i
        pn.append((start, 'on', name, 8));  pn.append((start+1, 'off', name, 0))
    # the walk ends at beat 76 — the last step done.

    emit(tracks[0], 1, vc)
    emit(tracks[1], 2, bl)
    emit(tracks[2], 3, pn)
    emit(tracks[3], 4, pd)

    return mc.compose('the-candle.mid', tracks, tempo=54)


if __name__ == '__main__':
    candle()
    print('composed the-candle.mid')
