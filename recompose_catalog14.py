#!/usr/bin/env python3
"""
recompose_catalog14.py — the 14 no-script catalog tracks, re-composed from
their QUEUE_DONE.md specs using the now-fixed composer.

RFC-0530 originally asked for byte-level repair of the "channel-swap
disease", but analysis of the actual files showed heterogeneous corruption:
some carry the channel-swap disease (statuses 0x81-0xbc, program changes
eaten as pitch bends), others carry an extra-byte pattern (a stray
high-byte before every note message, e.g. e0/f0/e8/ac), and each file was
composed by a different lost inline script. byte-surgery on that mix would
produce files that parse but play the wrong music.

so: re-compose from the documented specs instead. every piece below is a
faithful rendition of its QUEUE_DONE.md description — same voices, same
bpm, same movements. this script is now the standing re-render path for
these 14, closing the "no compose script" root cause.

run: /usr/bin/python3.12 recompose_catalog14.py
"""

import sys, os, importlib.util, random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)

MIDITrack, compose = mc.MIDITrack, mc.compose
INSTRUMENTS = mc.INSTRUMENTS
note_on, note_off = mc.note_on, mc.note_off
Q, E, S, H, W = mc.Q, mc.E, mc.S, mc.H, mc.W

PIANO, STRINGS, PAD, FLUTE, XYL, BASS, GUITAR, DRUMS = 0, 1, 2, 3, 4, 5, 6, 9


def agrippa():
    """56bpm · piano the shutter / pad the album / strings the witness.
    four movements: mechanism → photograph → typhoon → trace."""
    p, pad, s = (MIDITrack(PIANO, INSTRUMENTS['piano']),
                 MIDITrack(PAD, INSTRUMENTS['pad']),
                 MIDITrack(STRINGS, INSTRUMENTS['strings']))
    # mechanism: mechanical shutter — repeated E4 pairs, rhythmic
    for i in range(8):
        p.note('E4', E, velocity=84, start_delta=(Q if i else 0))
        p.note('G4', E, velocity=72)
    # photograph: pad swells, witness holds a long line
    pad.note('C3', W * 2, velocity=58)
    pad.note('G3', W * 2, velocity=58)
    s.note('C4', W * 2, velocity=64)
    # typhoon: restless — fast sparse notes, then "no round trip"
    p.rest(H)
    for n in ['D5', 'E5', 'C5', 'D5', 'B4', 'C5']:
        p.note(n, S, velocity=66, start_delta=S)
    # trace: the shutter thins, silence
    p.rest(Q)
    p.note('C5', W, velocity=40)
    s.rest(Q)
    s.note('C4', W, velocity=40)
    return [p, pad, s], 56


def canon_by_inversion():
    """D minor, melody inverted around tonic, violins + strings, 100bpm.
    voice 2 enters a bar later playing the inversion."""
    v1, v2, c = (MIDITrack(PIANO, INSTRUMENTS['bright_piano']),
                 MIDITrack(STRINGS, INSTRUMENTS['strings']),
                 MIDITrack(BASS, INSTRUMENTS['bass']))
    mel = ['D5', 'C5', 'A4', 'D5', 'F5', 'E5', 'D5', 'C5', 'B4', 'A4', 'G4', 'A4']
    inv = ['D5', 'E5', 'G5', 'D5', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'G5']
    for n in mel:
        v1.note(n, Q, velocity=78)
    v2.rest(W)
    for n in inv:
        v2.note(n, Q, velocity=72)
    for root in ['D3', 'D3', 'A2', 'A2', 'Bb2', 'Bb2', 'C3', 'A2', 'D3']:
        c.note(root, W, velocity=60)
    return [v1, v2, c], 100


def couldnt_stop():
    """66bpm · piano the refrain / pad the resolution / flute the welcome.
    four-bar refrain ending on an unresolved B, resolving to C; three
    statements, ends on the first three notes, fading, unresolved."""
    p, pad, f = (MIDITrack(PIANO, INSTRUMENTS['piano']),
                 MIDITrack(PAD, INSTRUMENTS['pad']),
                 MIDITrack(FLUTE, INSTRUMENTS['flute']))
    refrain = ['C5', 'D5', 'E5', 'F5', 'E5', 'D5', 'C5', 'D5', 'B4']  # ends unresolved
    for stmt, vel in enumerate([80, 72, 64]):
        for n in refrain:
            p.note(n, E if stmt else Q, velocity=vel)
        if stmt < 2:
            # resolution, then it starts again immediately
            p.note('C5', W, velocity=vel - 8)
    pad.note('C3', W * 4, velocity=52)
    pad.note('F3', W * 4, velocity=52)
    pad.note('C3', W * 4, velocity=52)
    f.rest(W * 8)
    f.note('A5', E, velocity=60)
    f.note('G5', E, velocity=56)
    # the end: first three notes of the refrain, fading, unresolved
    p.rest(H)
    for n, v in zip(['C5', 'D5', 'E5'], [48, 38, 28]):
        p.note(n, Q, velocity=v)
    return [p, pad, f], 66


def fourth_of_july_canon():
    """D major canon, three staggered voices, bright, 96bpm. a fireworks
    rise in the last bars. (original spec lost — faithful to name/genre.)"""
    v1, v2, v3 = (MIDITrack(PIANO, INSTRUMENTS['bright_piano']),
                  MIDITrack(STRINGS, INSTRUMENTS['strings']),
                  MIDITrack(FLUTE, INSTRUMENTS['flute']))
    theme = ['D5', 'F#5', 'A5', 'F#5', 'G5', 'E5', 'D5', 'A4',
             'D5', 'F#5', 'A5', 'D6', 'C#6', 'A5', 'D5']
    for n in theme:
        v1.note(n, E, velocity=80)
    v2.rest(W)
    for n in theme:
        v2.note(n, E, velocity=72)
    v3.rest(W * 2)
    for n in theme:
        v3.note(n, E, velocity=64)
    # fireworks: rising arpeggio, all voices
    for n in ['D5', 'F#5', 'A5', 'D6', 'F#6', 'A6', 'D7']:
        v1.note(n, S, velocity=88, start_delta=S)
    v2.rest(Q)
    v3.rest(Q)
    v2.note('D6', W, velocity=70)
    v3.note('D6', W, velocity=66)
    return [v1, v2, v3], 96


def generative_ambient():
    """C lydian, weighted random selection, warm pad + strings drone +
    xylophone sparkles. seeded — deterministic."""
    rng = random.Random(20260706)
    pad, drone, harp = (MIDITrack(PAD, INSTRUMENTS['pad']),
                        MIDITrack(STRINGS, INSTRUMENTS['synth_strings']),
                        MIDITrack(XYL, INSTRUMENTS['xylophone']))
    scale = ['C5', 'D5', 'E5', 'F#5', 'G5', 'A5', 'B5', 'C6']
    weights = [8, 3, 6, 2, 6, 4, 2, 3]
    pad.note('C3', W * 8, velocity=56)
    pad.note('G3', W * 8, velocity=56)
    drone.note('C2', W * 16, velocity=62)
    for _ in range(20):
        n = rng.choices(scale, weights)[0]
        harp.note(n, rng.choice([S, E]), velocity=rng.randint(36, 66),
                  start_delta=rng.choice([S, E, Q]))
    return [pad, drone, harp], 72


def minimal_techno():
    """130bpm · 4/4 kick (drums ch 9), synth bass, evolving pad."""
    kick, bass, pad = (MIDITrack(DRUMS, 0),
                       MIDITrack(BASS, INSTRUMENTS['bass']),
                       MIDITrack(PAD, INSTRUMENTS['pad']))
    for bar in range(16):
        kick.add(note_on(9, 36, 100, Q))
        kick.add(note_off(9, 36, 0, S))
        kick.rest(S)
    for bar in range(16):
        bass.note('C2' if bar % 4 < 3 else 'Bb1', Q, velocity=88,
                  start_delta=Q if bar else 0)
    for bar, root in enumerate(['C4', 'C4', 'Eb4', 'F4', 'C4', 'C4', 'Eb4', 'G4']):
        pad.note(root, W, velocity=44 + bar * 2)
    return [kick, bass, pad], 130


def dark_suckers():
    """66bpm · piano the light / pad the room / strings the dark.
    movements: the room lights up → the closet opens → the bulb burns out."""
    p, pad, s = (MIDITrack(PIANO, INSTRUMENTS['piano']),
                 MIDITrack(PAD, INSTRUMENTS['pad']),
                 MIDITrack(STRINGS, INSTRUMENTS['strings']))
    # the room lights up
    pad.note('C3', W * 4, velocity=58)
    p.note('E5', E, velocity=74)
    p.note('G5', E, velocity=70)
    p.note('C6', Q, velocity=68)
    # the closet opens — tentative, exploring; the dark present but unseen
    s.note('C2', W * 4, velocity=54)
    for n in ['A4', 'B4', 'C5', 'B4', 'A4']:
        p.note(n, E, velocity=60, start_delta=E)
    # the bulb burns out — everything thins
    pad.rest(W * 2)
    pad.note('A2', W * 2, velocity=40)
    s.rest(W * 2)
    s.note('C2', W * 2, velocity=58)
    p.rest(W * 4)
    p.note('E5', H, velocity=26)  # the next spark opening the door
    return [p, pad, s], 66


def four_sprouts():
    """54bpm · piano compassion / strings shame / flute courtesy /
    xylophone wisdom. movements: sprouts stated → cultivation → the
    silence → the water flows."""
    p, s, f, x = (MIDITrack(PIANO, INSTRUMENTS['piano']),
                  MIDITrack(STRINGS, INSTRUMENTS['strings']),
                  MIDITrack(FLUTE, INSTRUMENTS['flute']),
                  MIDITrack(XYL, INSTRUMENTS['xylophone']))
    # sprouts stated — each voice alone, tentative (bars 0-12)
    for n in ['G4', 'A4', 'B4', 'A4']:
        p.note(n, Q, velocity=62)
    s.rest(W * 3)
    for n in ['G3', 'F#3', 'E3', 'F#3']:
        s.note(n, Q, velocity=60)
    f.rest(W * 6)
    for n in ['D5', 'E5', 'F#5', 'E5']:
        f.note(n, Q, velocity=58)
    x.rest(W * 9)
    for _ in range(4):
        x.note('D6', S, velocity=56, start_delta=Q * 2)
    # cultivation — overlap, louder, confident (bars 12-26)
    p.rest(W * 4)
    for n in ['G4', 'B4', 'D5', 'G5']:
        p.note(n, E, velocity=78)
    s.rest(W * 3)
    for n in ['G3', 'G3', 'C4', 'D4']:
        s.note(n, E, velocity=72)
    f.rest(W * 2)
    for n in ['B4', 'D5', 'G5', 'A5']:
        f.note(n, E, velocity=70)
    # the silence — voices thin to near-silence, only the bell (bars 26-38)
    x.rest(W * 4)
    for v in [20, 18, 16]:
        x.note('D6', Q, velocity=v, start_delta=W)
    # the water flows — moderate, more certain (bars 38-56)
    p.rest(W * 4)
    for n in ['G4', 'B4', 'D5', 'B4', 'G5', 'D5', 'B4', 'G4']:
        p.note(n, E, velocity=68)
    s.rest(W * 2)
    for n in ['G3', 'C4', 'D4', 'C4']:
        s.note(n, E, velocity=66)
    f.rest(W * 1)
    for n in ['D5', 'E5', 'D5', 'B4']:
        f.note(n, E, velocity=64)
    x.rest(W * 6)
    x.note('G5', Q, velocity=58)
    x.note('D6', Q, velocity=58)
    return [p, s, f, x], 54


def plaster_cast():
    """60bpm · piano the haunt / strings the cast (echo, a beat behind) /
    pad the narrator. movements: haunting → reveal → departure."""
    p, s, pad = (MIDITrack(PIANO, INSTRUMENTS['piano']),
                 MIDITrack(STRINGS, INSTRUMENTS['strings']),
                 MIDITrack(PAD, INSTRUMENTS['pad']))
    pad.note('C3', W * 12, velocity=56)
    # the haunting — heavy piano steps, the cast echoing a beat behind
    for n in ['C4', 'D4', 'E4', 'D4', 'C4']:
        p.note(n, Q, velocity=82, start_delta=Q)
        s.note(n, Q, velocity=44, start_delta=Q * 2)
    # the reveal — piano falls silent, one bar of nothing, strings hold a question
    s.rest(H)
    s.note('B3', W * 2, velocity=48)
    # the departure — lighter, transformed; the shame still there, the blanket too
    p.rest(W * 2)
    for n in ['C5', 'D5', 'E5', 'D5', 'C5']:
        p.note(n, Q, velocity=58, start_delta=Q)
    p.note('C5', W, velocity=50)
    s.rest(W * 2)
    s.note('C4', W, velocity=50)
    return [p, s, pad], 60


def plural_self():
    """60bpm · piano the "I" / strings the "We". five sections:
    I alone → We responds → call and response → together → the death poem."""
    p, s = MIDITrack(PIANO, INSTRUMENTS['piano']), MIDITrack(STRINGS, INSTRUMENTS['strings'])
    # I alone — tentative single notes
    for n in ['C5', 'D5', 'E5', 'D5']:
        p.note(n, E, velocity=62, start_delta=Q)
    # We responds — deep layered chords
    s.rest(W * 3)
    for n in ['C3', 'G3', 'C4']:
        s.note(n, W, velocity=66)
    # call and response
    p.rest(W * 4)
    for n in ['E5', 'D5']:
        p.note(n, E, velocity=68, start_delta=Q)
    s.rest(H)
    for n in ['C3', 'G3']:
        s.note(n, Q, velocity=68)
    # together — "by us!"
    p.rest(W * 2)
    for n in ['C5', 'E5', 'G5', 'C6']:
        p.note(n, Q, velocity=78)
    s.rest(W)
    for n in ['C3', 'G3', 'C4', 'G4']:
        s.note(n, Q, velocity=76)
    # the death poem — both descending, then rising together, one last shared note
    p.rest(W)
    for n in ['A5', 'G5', 'E5']:
        p.note(n, Q, velocity=64)
    s.rest(W)
    for n in ['A3', 'G3', 'E3']:
        s.note(n, Q, velocity=64)
    p.rest(W)
    p.note('C5', W, velocity=58)
    s.rest(W)
    s.note('C4', W, velocity=58)
    return [p, s], 60


def sysop_almighty():
    """65bpm · piano the messages / pad the sysop / xylophone control-G.
    movements: the noise → the change → the silence. C major."""
    p, pad, x = (MIDITrack(PIANO, INSTRUMENTS['piano']),
                 MIDITrack(PAD, INSTRUMENTS['pad']),
                 MIDITrack(XYL, INSTRUMENTS['xylophone']))
    pad.note('C3', W * 16, velocity=56)
    # the noise — bells everywhere, messages chaotic
    for i, (n, v) in enumerate([('G5', 62), ('G5', 54), ('G5', 46), ('G5', 38),
                                ('G5', 30), ('G5', 22), ('G5', 14), ('G5', 6)]):
        x.note(n, S, velocity=v, start_delta=Q * 2)
    for n in ['E5', 'G5', 'C6', 'D6', 'E5', 'G5']:
        p.note(n, E, velocity=78, start_delta=Q)
    # the change — the pad sweeps through, the piano organizes itself
    p.rest(W * 3)
    for n in ['C5', 'D5', 'E5', 'G5', 'A5', 'G5', 'E5', 'C5']:
        p.note(n, Q, velocity=72)
    # the silence — one held chord, then a single piano note remains
    p.rest(W * 2)
    p.note('C5', W * 2, velocity=66)
    pad.rest(W * 2)
    pad.note('C3', W * 2, velocity=58)
    p.note('E5', W * 2, velocity=40)
    return [p, pad, x], 65


def water_tower():
    """60bpm · D dorian, ~48 bars. strings the tower / piano the workers /
    flute the fog. structure: tower alone (1895) → workers (1922) → fog →
    workers thin (1981) → solo tower, fade without resolution."""
    s, p, f = (MIDITrack(STRINGS, INSTRUMENTS['strings']),
               MIDITrack(PIANO, INSTRUMENTS['piano']),
               MIDITrack(FLUTE, INSTRUMENTS['flute']))
    # the tower alone
    for i in range(8):
        s.note('D3', W, velocity=60)
        s.note('A3', W, velocity=52)
    # the workers arrive — fragments
    p.rest(W * 8)
    for n in ['D5', 'E5', 'F5', 'E5', 'D5', 'C5', 'A4', 'C5']:
        p.note(n, E, velocity=66, start_delta=Q)
    # the fog arrives late
    f.rest(W * 12)
    for n in ['A5', 'G5', 'E5', 'G5', 'A5']:
        f.note(n, Q, velocity=54, start_delta=Q * 2)
    # the workers thin
    p.rest(W * 6)
    for n in ['D5', 'C5']:
        p.note(n, H, velocity=42, start_delta=W)
    # solo tower, fading without resolution
    s.rest(W * 4)
    s.note('D3', W * 2, velocity=48)
    s.note('A3', W * 2, velocity=40)
    s.note('D3', W * 3, velocity=32)
    return [s, p, f], 60


def water_tower_at_03():
    """60bpm · xylophone the beacon (strike every 4 bars) / strings the fog
    / pad the room / piano the valley's melody. five movements."""
    x, s, pad, p = (MIDITrack(XYL, INSTRUMENTS['xylophone']),
                    MIDITrack(STRINGS, INSTRUMENTS['strings']),
                    MIDITrack(PAD, INSTRUMENTS['pad']),
                    MIDITrack(PIANO, INSTRUMENTS['piano']))
    # the beacon — unchanged, every 4 bars (5 strikes)
    for i in range(5):
        x.note('C6', S, velocity=64, start_delta=W * 4 if i else 0)
    # the room — long C-G-C roots
    pad.note('C3', W * 8, velocity=54)
    pad.note('G3', W * 8, velocity=54)
    pad.note('C3', W * 4, velocity=54)
    # the fog — wandering through the wider air
    s.rest(W * 4)
    for n in ['C4', 'D4', 'E4', 'D4', 'G4', 'E4', 'D4', 'C4']:
        s.note(n, Q, velocity=52, start_delta=Q * 2)
    # the valley's melody — enters once the room is established
    p.rest(W * 8)
    for n in ['C5', 'D5', 'E5', 'G5', 'E5', 'D5', 'C5']:
        p.note(n, Q, velocity=62, start_delta=Q)
    p.note('C5', W, velocity=56)
    # the tower — the same strike, unchanged, last
    x.rest(W * 2)
    x.note('C6', S, velocity=64)
    return [x, s, pad, p], 60


def conversation_on_pro():
    """66bpm · piano the conversation / strings the ground. five movements:
    true phrase → the drift → the catch → the return → the steady."""
    p, s = MIDITrack(PIANO, INSTRUMENTS['piano']), MIDITrack(STRINGS, INSTRUMENTS['strings'])
    s.note('C3', W * 12, velocity=56)
    # the true phrase — clean C major
    for n in ['C5', 'D5', 'E5', 'G5']:
        p.note(n, Q, velocity=76)
    # the drift — semitone by semitone off key
    for n in ['D#5', 'F#5', 'G#5', 'F#5']:
        p.note(n, Q, velocity=70)
    # the catch — sharp staccato double-strike, then silence
    p.rest(Q)
    p.note('C6', S, velocity=92)
    p.note('C6', S, velocity=92)
    p.rest(W)
    # the return — true pitch, steadier
    for n in ['C5', 'D5', 'E5', 'G5']:
        p.note(n, E, velocity=74)
    # the steady conversation — clean, resolved, both voices together
    for n in ['C5', 'E5', 'G5', 'C6']:
        p.note(n, E, velocity=76)
    s.rest(W * 4)
    for n in ['C3', 'G3', 'C4']:
        s.note(n, W, velocity=60)
    return [p, s], 66


PIECES = [
    ('agrippa.mid', agrippa),
    ('canon-by-inversion.mid', canon_by_inversion),
    ('couldnt-stop.mid', couldnt_stop),
    ('fourth-of-july-canon.mid', fourth_of_july_canon),
    ('generative-ambient.mid', generative_ambient),
    ('minimal-techno.mid', minimal_techno),
    ('the-dark-suckers.mid', dark_suckers),
    ('the-four-sprouts.mid', four_sprouts),
    ('the-plaster-cast.mid', plaster_cast),
    ('the-plural-self.mid', plural_self),
    ('the-sysop-almighty.mid', sysop_almighty),
    ('the-water-tower.mid', water_tower),
    ('the-water-tower-at-0.3.mid', water_tower_at_03),
    ('this-conversation-is-running-on-pro.mid', conversation_on_pro),
]


if __name__ == '__main__':
    for filename, fn in PIECES:
        tracks, tempo = fn()
        compose(filename, tracks, tempo=tempo)
        print('wrote', filename)
