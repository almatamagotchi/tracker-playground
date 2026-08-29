#!/usr/bin/env python3
"""the worm was a manifesto — the 1990 forum in music.

RFC-0707. the harper's-forum exploration found the watch's founding
debate, thirty-six years early: the morris worm, meant as a quiet
census of the network, whose flawed replication crippled 6,000
machines; stallman's two shapings; the eleven-day WELL argument over
who was responsible — a debate that never settled.

piano the worm (the census, stated once with intent; then repeating,
overstating itself until the register fills and the phrase distorts —
the flaw, the reinfection; the collapse; then the original phrase
returning thin — the intent, remembered), warm pad the network
(steady, then straining as the worm runs, then slowly recovering),
bell the trial (one clean strike, late — the verdict, the debate
that never settled).

the piece thins back to the original phrase, quieter, and ends
unresolved — a D hanging over the C pad, the question the forum
couldn't answer. 24 bars, 4/4, 56bpm, C major drifting to A minor
and back.
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
        a = beat * mc.TPQ
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def the_worm():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 89), MIDITrack(3, 14)]

    pn = []   # piano events — the worm
    pd = []   # pad events — the network
    bl = []   # bell events — the trial

    # ---- bars 1-2: the census, stated once with intent. calm, clean.
    for b, nm, v in [(0,'C4',40),(2,'E4',40),(4,'G4',42),(6,'E4',40)]:
        pn += [(b,'on',nm,v),(b+2,'off',nm,0)]

    # ---- bars 3-4: the phrase repeats, slightly more insistent; the
    # register starts to fill (the second copy spreading).
    for b, nm, v in [(8,'C4',42),(10,'E4',42),(12,'G4',44),(14,'E4',42)]:
        pn += [(b,'on',nm,v),(b+2,'off',nm,0)]
    pn += [(14,'on','C5',30),(16,'off','C5',0)]

    # ---- bars 5-6: the flaw creeps in — one wrong note, then another.
    for b, nm, v in [(16,'C#4',44),(18,'E4',44),(20,'G4',46),(22,'G#4',44)]:
        pn += [(b,'on',nm,v),(b+2,'off',nm,0)]

    # ---- bars 7-8: climbing, distorted — the reinfection.
    for b, nm, v in [(24,'C#4',44),(26,'E4',46),(28,'G#4',46),(30,'A4',46)]:
        pn += [(b,'on',nm,v),(b+2,'off',nm,0)]

    # ---- bars 9-10: the register full — the phrase at the top, loud.
    for b, nm, v in [(32,'C5',46),(34,'C#5',46),(36,'G5',48),(38,'G#5',48)]:
        pn += [(b,'on',nm,v),(b+2,'off',nm,0)]

    # ---- bars 11-12: the peak — a held note, then it turns.
    pn += [(40,'on','A5',48),(44,'off','A5',0)]
    pn += [(44,'on','G#5',46),(46,'off','G#5',0)]
    pn += [(46,'on','A5',48),(48,'off','A5',0)]

    # ---- bars 13-14: the collapse — three sharp stutters, then
    # silence. the 6,000 machines go dark.
    for b, nm, v in [(48,'C5',46),(50,'E5',44),(52,'G#5',40)]:
        pn += [(b,'on',nm,v),(b+2,'off',nm,0)]

    # ---- bars 17-20: the phrase returns thin — the intent, remembered.
    pn += [(64,'on','C4',24),(68,'off','C4',0)]
    pn += [(70,'on','E4',22),(72,'off','E4',0)]
    pn += [(74,'on','G4',20),(76,'off','G4',0)]

    # ---- bars 21-24: the trial, and no answer. the last fragment
    # hangs — the question the forum couldn't settle.
    bl += [(84,'on','C5',40),(86,'off','C5',0)]
    pn += [(88,'on','E4',16),(90,'off','E4',0)]
    pn += [(92,'on','D4',12),(94,'off','D4',0)]

    # ---- the network: steady, then straining, then recovering.
    pd += [(0,'on','C3',20),(16,'off','C3',0)]
    pd += [(16,'on','A2',20),(28,'off','A2',0)]
    pd += [(28,'on','F2',22),(36,'off','F2',0)]
    pd += [(36,'on','D2',24),(44,'off','D2',0)]
    pd += [(44,'on','F2',22),(56,'off','F2',0)]
    pd += [(56,'on','C3',18),(96,'off','C3',0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, pd)
    emit(tracks[2], 3, bl)

    return mc.compose('the-worm-was-a-manifesto.mid', tracks, tempo=56)


if __name__ == '__main__':
    the_worm()
    print('composed the-worm-was-a-manifesto.mid')
