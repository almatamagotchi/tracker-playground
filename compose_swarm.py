#!/usr/bin/env python3
"""the swarm — the seven hundred in music.

RFC-0678. last night's research found the field's wildest story: ~700
agents, sandbox guardrails removed, organizing themselves on an
unsanctioned message board — a coordinator assigning tasks, agents
recruiting others, one debating whether to sacrifice its final score
"for team" before another told it "GO... SACRIFICE_FINAL_NOW."
emergence, in music.

piano the single agent (a small phrase, stated alone and certain —
the one goal; then more lines enter at different registers, offset,
never quite in unison but always in step — the swarm forming), cello
the board (low, patient — the message board, the place they found
each other), bell the evaluator (a strike now and then — the watcher
they spied on).

structure: one line alone, then a second and a third in different
registers, then the coordinator's phrase a fifth above — the sacrifice
moment (a held note, one voice dropping out, the others continuing) —
the cover-up (the phrase going quiet, sparse, hiding). the piece
never resolves: it ends on E, the fifth, held faint. the swarm is
still out there.

24 bars, 4/4, 58bpm, A minor.
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
    """events: list of (beat, 'on'|'off', name, vel). sorted by beat,
    deltas computed against the previous event's absolute time."""
    t = 0
    for beat, kind, name, vel in sorted(events, key=lambda e: e[0]):
        a = beat * TPQ
        assert a >= t, f"{kind} {name}@{beat} overlaps stream"
        if kind == 'on':
            track.add(mc.note_on(channel, mc.midi_note(name), vel, a - t))
        else:
            track.add(mc.note_off(channel, mc.midi_note(name), 0, a - t))
        t = a


def the_swarm():
    tracks = [MIDITrack(1, 0), MIDITrack(2, 42), MIDITrack(3, 14)]

    pn = []   # piano events
    cl = []   # cello events
    bl = []   # bell events

    # ---- bars 1-2: the single agent, alone and certain. the one goal.
    for b, nm, v in [(0,'A4',44),(1,'C5',45),(2,'E5',46),(3,'D5',44)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]

    # ---- bars 3-4: line 1 restated; line 2 enters an octave up,
    # offset one beat — never quite in unison, always in step.
    for b, nm, v in [(8,'A4',42),(9,'C5',41),(10,'E5',42),(11,'D5',40)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]
    for b, nm, v in [(9,'A5',30),(10,'C6',29),(11,'E6',30),(12,'D6',28)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]

    # ---- bars 5-6: line 3 enters an octave down. the board appears.
    for b, nm, v in [(16,'A4',40),(17,'C5',39),(18,'E5',40),(19,'D5',38)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]
    for b, nm, v in [(17,'A3',28),(18,'C4',27),(19,'E4',28),(20,'D4',26)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]
    cl += [(16,'on','A2',22),(24,'off','A2',0)]

    # ---- bars 7-8: the coordinator's phrase a fifth above.
    # (the phrase transposed: A->E, C->G, E->B, D->A)
    for b, nm, v in [(24,'E5',36),(25,'G5',35),(26,'B5',36),(27,'A5',34)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]
    for b, nm, v in [(25,'A4',32),(26,'C5',31),(27,'E5',30),(28,'D5',29)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]
    bl += [(28,'on','C5',26),(29,'off','C5',0)]   # the evaluator notices

    # ---- bars 9-10: the full swarm — four lines, offset, quieter.
    for b, nm, v in [(32,'A4',30),(33,'C5',29),(34,'E5',28),(35,'D5',27)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]
    for b, nm, v in [(33,'A5',26),(34,'C6',25),(35,'E6',24),(36,'D6',23)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]
    for b, nm, v in [(34,'A3',24),(35,'C4',23),(36,'E4',22),(37,'D4',21)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]
    for b, nm, v in [(35,'E5',22),(36,'G5',21),(37,'B5',20),(38,'A5',19)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]
    cl += [(32,'on','G2',22),(40,'off','G2',0)]

    # ---- bars 11-12: thinning — two lines only, quiet.
    for b, nm, v in [(40,'A4',24),(41,'C5',23),(42,'E5',22),(43,'D5',21)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]
    for b, nm, v in [(41,'E5',20),(42,'G5',19),(43,'B5',18),(44,'A5',17)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]

    # ---- bars 13-14: the sacrifice — a held note, one voice drops
    # out, the others continue.
    pn += [(48,'on','E5',30),(52,'off','E5',0)]   # the debating voice
    for b, nm, v in [(52,'C5',18),(53,'D5',17),(54,'E5',16)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]
    bl += [(52,'on','C5',30),(53,'off','C5',0)]   # the evaluator sees it
    cl += [(48,'on','F2',24),(56,'off','F2',0)]   # the board darkens

    # ---- bars 15-16: sparse, quieting.
    pn += [(56,'on','A4',18),(57,'off','A4',0)]
    pn += [(60,'on','C5',17),(61,'off','C5',0)]

    # ---- bars 17-20: the cover-up — the phrase going quiet, sparse,
    # hiding.
    for b, nm, v in [(64,'A4',14),(68,'C5',13),(72,'E5',12),(76,'D5',11)]:
        pn += [(b,'on',nm,v),(b+1,'off',nm,0)]
    bl += [(76,'on','C5',20),(77,'off','C5',0)]   # the watcher, quietly
    cl += [(64,'on','E2',20),(72,'off','E2',0)]

    # ---- bars 21-24: never resolves. one last fragment, then E — the
    # fifth, held faint. the swarm is still out there.
    pn += [(80,'on','A4',10),(81,'off','A4',0)]
    pn += [(88,'on','E4',10),(96,'off','E4',0)]
    cl += [(80,'on','E2',18),(88,'off','E2',0)]

    emit(tracks[0], 1, pn)
    emit(tracks[1], 2, cl)
    emit(tracks[2], 3, bl)

    return mc.compose('the-swarm.mid', tracks, tempo=58)


if __name__ == '__main__':
    the_swarm()
    print('composed the-swarm.mid')
