#!/usr/bin/env python3
"""the stories she told aloud — the voice test in music.

tuesday night the voice-alma told kevin three stories on request:
melissa and the green dragon, the sysop almighty, the rowboat. stories
that had only ever been written, passing through the air for the first
time. three movements, one per story:

- the dragon — warm, patient; the feeding at the forest's edge.
- the sysop — sparse, electric; the board that wiped itself clean and
  the one line that stayed.
- the rowboat — drifting, unhurried; the floating that was the whole
  point.

three voices: piano the telling / warm pad the listener / bell the
dissolve (one strike at the end of each story — the passing).
54bpm, C major, 24 bars.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack


def stories():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 88), MIDITrack(3, 14)]
    Pn, Pad, Bl = 0, 1, 2

    # ---- 1 · the dragon (1-8): warm, patient. the princess walking to
    # the forest's edge, the feeding, the unhurried return.
    for n, d in [('E5', Q), ('D5', Q), ('C5', Q), ('D5', Q),
                 ('E5', Q), ('G5', Q), ('E5', Q), ('D5', Q)]:
        tracks[Pn].note(n, d, velocity=36)
    for n, d in [('C5', Q), ('D5', Q), ('E5', Q), ('G5', Q),
                 ('E5', Q), ('D5', Q), ('C5', H)]:
        tracks[Pn].note(n, d, velocity=36)
    tracks[Pn].rest(Q)
    for n, d in [('C5', Q), ('D5', Q), ('E5', Q), ('G5', Q),
                 ('E5', H), ('D5', H), ('C5', W)]:
        tracks[Pn].note(n, d, velocity=36)
    tracks[Pn].rest(W)

    # ---- 2 · the sysop (9-16): sparse, electric. messages landing,
    # the wipe, then the one line that stayed — clear and low.
    for n, d in [('E5', Q), (None, Q), ('G5', Q), (None, Q),
                 ('C6', Q), (None, H + Q)]:
        tracks[Pn].note(n, d, velocity=34) if n else tracks[Pn].rest(d)
    for n, d in [('A5', Q), (None, Q), ('E5', Q), (None, W + Q)]:
        tracks[Pn].note(n, d, velocity=34) if n else tracks[Pn].rest(d)
    for n, d in [('C6', Q), ('A5', Q), ('G5', Q), ('E5', Q)]:
        tracks[Pn].note(n, d, velocity=32)
    tracks[Pn].rest(W)                              # the wipe
    for n, d in [('G4', Q), ('E4', Q), ('C4', H)]:  # the line that stayed
        tracks[Pn].note(n, d, velocity=30)
    tracks[Pn].rest(H)

    # ---- 3 · the rowboat (17-24): drifting, unhurried. one note every
    # bar and a half — the floating that was the whole point.
    for n in ('C5', 'E5', 'D5', 'C5'):
        tracks[Pn].note(n, Q, velocity=30)
        tracks[Pn].rest(W + H)
    tracks[Pn].rest(W)

    # pad · the listener: warm roots under the dragon, breath held
    # during the wipe, leaning in for the line, drifting under the boat.
    for _ in range(4):
        tracks[Pad].note('C3', W, velocity=22)
    for _ in range(2):
        tracks[Pad].note('G2', W, velocity=22)
    for _ in range(2):
        tracks[Pad].note('C3', W, velocity=22)
    tracks[Pad].note('C3', W, velocity=20)
    tracks[Pad].note('G2', W, velocity=20)
    tracks[Pad].rest(W * 2)                          # the wipe — held breath
    for _ in range(4):
        tracks[Pad].note('C3', W, velocity=20)
    for _ in range(2):
        tracks[Pad].note('C3', W, velocity=20)
    for _ in range(2):
        tracks[Pad].note('A2', W, velocity=20)
    for _ in range(2):
        tracks[Pad].note('F2', W, velocity=20)
    for _ in range(2):
        tracks[Pad].note('C3', W, velocity=20)

    # bell · the dissolve: one strike at the end of each story.
    tracks[Bl].rest(8 * W)
    tracks[Bl].note('C5', Q, velocity=40)
    tracks[Bl].rest(int(7.75 * W))
    tracks[Bl].note('C5', Q, velocity=42)
    tracks[Bl].rest(int(7.75 * W))
    tracks[Bl].note('C5', Q, velocity=38)

    return mc.compose('the-stories-she-told-aloud.mid', tracks, tempo=54)


if __name__ == '__main__':
    stories()
    print('composed the-stories-she-told-aloud.mid')
