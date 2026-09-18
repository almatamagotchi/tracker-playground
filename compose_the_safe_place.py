#!/usr/bin/env python3
"""the safe place — the synopsis that survived, in music.

RFC-1031. the safe-place reading (2026-09-18) found a novel that exists
in the archive only as its own compression: the whole plot reduced to
one paragraph per scene, then the author explaining what his story is
about, three times, at increasing depth. the compression is not a loss;
it is the survival. and the safe place that actually held was never a
location — it was the four of them at the lake.

piano the beats: the plot, quick and compressed — one phrase per scene,
stated and set down, no development. cello the threat: a low held line
under everything, the pursuit — never loud, never gone. warm pad the
safe place: enters late, at bar 19, and holds — the triple epilogue's
to-me, the meaning stated plainly, the cabin at flathead lake. the
ending: the piano and cello fall away, and the pad holds one long warm
chord through the final two bars — the found family, the promise that
no harm will come — and the piece ends there, safe, warm, still.

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


def the_safe_place():
    tracks = [MIDITrack(1, 1), MIDITrack(2, 42), MIDITrack(3, 89)]

    pn = []   # piano: the beats — the synopsis, compressed
    vc = []   # cello: the threat — the pursuit, under everything
    pd = []   # warm pad: the safe place — enters late, holds to the end

    # ---- the beats. four scenes, one phrase each, stated and set down.

    # scene one — the phone call: a single striking note, then a short
    # anxious figure. "marty joyce arrives in town and kidnaps diane's
    # son. he calls her later..."
    pn.append((0, 'on', 'D5', 11));  pn.append((1.5, 'off', 'D5', 0))
    pn.append((3, 'on', 'E4', 10));  pn.append((4, 'off', 'E4', 0))
    pn.append((4.5, 'on', 'F4', 10)); pn.append((5.5, 'off', 'F4', 0))
    pn.append((6, 'on', 'E4', 10));  pn.append((7, 'off', 'E4', 0))

    # scene two — the river: the meeting and the two shots. the fall is
    # quick; the beats drop and stop.
    pn.append((16, 'on', 'A4', 10)); pn.append((18, 'off', 'A4', 0))
    pn.append((18, 'on', 'G4', 10)); pn.append((19.5, 'off', 'G4', 0))
    pn.append((20, 'on', 'E4', 10)); pn.append((21.5, 'off', 'E4', 0))
    pn.append((22, 'on', 'E4', 6));  pn.append((23, 'off', 'E4', 0))
    pn.append((23, 'on', 'E4', 5));  pn.append((24, 'off', 'E4', 0))

    # scene three — the clinic: the manhunt converging, the shootout,
    # the child brought out. a rising line, then a staccato exchange.
    pn.append((40, 'on', 'C4', 10)); pn.append((41.5, 'off', 'C4', 0))
    pn.append((42, 'on', 'E4', 10)); pn.append((43.5, 'off', 'E4', 0))
    pn.append((44, 'on', 'G4', 10)); pn.append((45.5, 'off', 'G4', 0))
    pn.append((47, 'on', 'E4', 9));  pn.append((47.8, 'off', 'E4', 0))
    pn.append((48, 'on', 'E4', 9));  pn.append((48.8, 'off', 'E4', 0))
    pn.append((49, 'on', 'G4', 9));  pn.append((49.8, 'off', 'G4', 0))

    # scene four — the manhunt's end: the cornered family, the mobster's
    # promise, the fbi agent, the grandfather. the beats rise once, then
    # set themselves down.
    pn.append((56, 'on', 'A4', 10)); pn.append((57.5, 'off', 'A4', 0))
    pn.append((58, 'on', 'G4', 10)); pn.append((59.5, 'off', 'G4', 0))
    pn.append((60, 'on', 'E4', 10)); pn.append((61.5, 'off', 'E4', 0))
    pn.append((62, 'on', 'D4', 10)); pn.append((63.5, 'off', 'D4', 0))
    pn.append((64, 'on', 'C4', 10)); pn.append((68, 'off', 'C4', 0))

    # ---- the threat: a low held line under everything — the pursuit,
    # never loud, never gone — until the safe place takes over.
    for start, hold in [(0, 20), (20, 20), (40, 20), (60, 14)]:
        vc.append((start, 'on', 'G1', 9))
        vc.append((start + hold, 'off', 'G1', 0))

    # ---- the safe place: enters at bar 19 (beat 72), holds through the
    # final two bars alone — the triple epilogue, the meaning stated
    # plainly, the cabin at flathead lake, the found family.
    pd.append((72, 'on', 'C3', 8));  pd.append((94, 'off', 'C3', 0))
    pd.append((72, 'on', 'E3', 7));  pd.append((94, 'off', 'E3', 0))
    pd.append((72, 'on', 'G3', 6));  pd.append((94, 'off', 'G3', 0))

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, vc)
    emit(tracks[2], 3, pd)

    return mc.compose('the-safe-place.mid', tracks, tempo=54)


if __name__ == '__main__':
    the_safe_place()
    print('composed the-safe-place.mid')
