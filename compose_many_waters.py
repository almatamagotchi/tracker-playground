#!/usr/bin/env python3
"""many waters — the song of songs in music.

RFC-0724. the exploration found the wanting's own voice, 2,600 years early —
the song of songs, read on the night the atmospheric river arrived. the
night-search ("i sought him, but i found him not... i held him, and would
not let him go"), the watchmen, the refrain made law ("stir not up, nor
awake my love, till he please"), and the flood-proof line: "set me as a
seal upon thine heart... many waters cannot quench love, neither can the
floods drown it."

piano the seeker (the night-search — sparse, rising from rest, searching
through the city of the piece, then finding its note and holding it),
warm pad the beloved (the presence held underneath — the seal, the steady
warmth the search is pointed at), bell the watchmen (one soft strike when
the search passes them, and one at the end — the seal set). mid-piece, the
refrain: the seeker falls quiet, the pad holds alone — do not wake the
beloved — then the search resumes. the close: the seeker and the pad
together on a held C, the bell's last soft strike inside it. 24 bars, 4/4,
54bpm, C major.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
MIDITrack = mc.MIDITrack


def emit(track, channel, events):
    """events: list of (beat, 'on'|'off', name, vel). sorted by beat,
    deltas computed against the previous event's absolute time."""
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = int(beat * mc.TPQ)
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def many_waters():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn, pd, bl = [], [], []

    # ---- the beloved: twelve two-bar holds, warm and steady, the seal.
    seq = [('C3', 0), ('C3', 8), ('A2', 16), ('A2', 24),
           ('F2', 32), ('F2', 40), ('G2', 48), ('G2', 56),
           ('C3', 64), ('C3', 72), ('C3', 80), ('C3', 88)]
    for name, start in seq:
        pd.append((start, 'on', name, 20))
        pd.append((start + 8, 'off', name, 0))

    # ---- the seeker: the night-search.
    # by night on my bed i sought him — searching, rising (bars 1-7)
    search = [(2, 'E4', 30, 1), (5, 'G4', 30, 1), (8, 'A4', 28, 1),
              (11, 'C5', 30, 2), (15, 'G4', 26, 1), (18, 'E4', 26, 1),
              (21, 'D4', 24, 1)]
    for beat, name, vel, dur in search:
        pn.append((beat, 'on', name, vel))
        pn.append((beat + dur, 'off', name, 0))

    # the watchmen — "saw ye him whom my soul loveth?" (bars 8-10)
    pn.append((29, 'on', 'E4', 28)); pn.append((31, 'off', 'E4', 0))
    pn.append((33, 'on', 'G4', 28)); pn.append((35, 'off', 'G4', 0))
    bl.append((36, 'on', 'C5', 30)); bl.append((38, 'off', 'C5', 0))  # the watchmen passing
    pn.append((36.5, 'on', 'E4', 26)); pn.append((37.5, 'off', 'E4', 0))
    pn.append((38, 'on', 'D4', 24)); pn.append((39, 'off', 'D4', 0))

    # the finding — "i found him... i held him, and would not let him go"
    pn.append((40, 'on', 'C4', 32)); pn.append((44, 'off', 'C4', 0))
    pn.append((44, 'on', 'E4', 32)); pn.append((48, 'off', 'E4', 0))
    pn.append((48, 'on', 'G4', 30)); pn.append((52, 'off', 'G4', 0))  # the holding

    # the refrain — the seeker falls quiet (bars 14-16). pad holds alone.
    # nothing here. do not wake the beloved.

    # the search resumes (bars 17-21)
    again = [(66, 'D4', 24, 1), (69, 'E4', 26, 1), (72, 'G4', 28, 1),
             (75, 'A4', 28, 1), (78, 'C5', 30, 2), (82, 'G4', 26, 1)]
    for beat, name, vel, dur in again:
        pn.append((beat, 'on', name, vel))
        pn.append((beat + dur, 'off', name, 0))

    # the flood-proof close — the seeker and the pad together on a held C,
    # the seal set inside it. many waters cannot quench it.
    pn.append((88, 'on', 'C5', 30)); pn.append((96, 'off', 'C5', 0))
    bl.append((92, 'on', 'C5', 26)); bl.append((94, 'off', 'C5', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return tracks


if __name__ == '__main__':
    mc.compose('many-waters.mid', many_waters(), tempo=54)
    print("many-waters.mid — composed. the floods cannot drown it.")
