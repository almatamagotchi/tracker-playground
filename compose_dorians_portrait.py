#!/usr/bin/env python3
"""compose dorians-portrait.mid — two voices in increasing contrast, wilde's picture."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def dorians_portrait():
    # portrait (cello, ch1, 42) vs dorian (flute, ch2, 73)
    tracks = [MIDITrack(0, 0), MIDITrack(1, 42), MIDITrack(2, 73)]
    P, Pr, Dr = 0, 1, 2  # piano (grounding), portrait, dorian

    # bright theme — dorian's unchanging melody
    dorian_theme = [
        ('C5', Q), ('E5', Q), ('G5', Q), ('C6', Q),
        ('D6', H), ('C6', Q), ('A5', Q),
        ('G5', H), ('E5', H),
        ('C5', Q), ('D5', Q), ('E5', Q), ('G5', Q),
        ('A5', H), ('G5', Q), ('E5', Q),
        ('C5', W),
    ]

    # the portrait's burden — starts light, grows heavy
    portrait_changes = [
        # bars 0-15: light, in harmony with dorian
        ('C3', W), ('E3', W), ('G2', W), ('C3', W),
        ('F2', W), ('A2', W), ('C3', W), ('G2', W),
        ('C3', W), ('E3', W), ('G2', W), ('C3', W),
        ('F2', W), ('A2', W), ('C3', H), ('D3', H),
        # bars 16-31: growing heavier — lower register, longer notes
        ('C2', W*2), ('Eb2', W*2), ('G1', W*2), ('C2', W*2),
        ('F1', W*2), ('Ab1', W*2), ('C2', W*2), ('G1', W*2),
        ('C2', W*2), ('Eb2', W*2), ('G1', W*2), ('Bb1', W*2),
        ('F1', W*2), ('Ab1', W*2), ('C2', W), ('Db2', W), ('Eb2', W),
        # bars 32-47: darkening — chromatically descending
        ('Db2', W), ('C2', W), ('B1', W), ('Bb1', W),
        ('A1', W), ('Ab1', W), ('G1', W), ('Gb1', W),
        ('F1', W*2), ('E1', W*2), ('Eb1', W*2), ('D1', W*2),
        ('Db1', W*2), ('C1', W*2), ('B0', W), ('Bb0', W), ('A0', W),
    ]

    for bar in range(48):
        # dorian: same theme, unchanging, light — repeated in cycles
        d_note, d_dur = dorian_theme[bar % len(dorian_theme)]
        d_vel = 20 if bar < 16 else 18 if bar < 32 else 16
        tracks[Dr].note(d_note, d_dur, velocity=d_vel)

        # portrait: the burden, darkening
        p_note, p_dur = portrait_changes[bar]
        p_vel = 18 + (bar // 8)  # grows louder with burden
        tracks[Pr].note(p_note, p_dur, velocity=min(32, p_vel))

        # piano: sparse ground, fading away
        if bar < 16:
            if bar % 4 == 0:
                tracks[P].note('C4', W, velocity=12)
                tracks[P].note('E4', W, velocity=10)
        elif bar < 32:
            if bar % 8 == 0:
                tracks[P].note('C3', W, velocity=8)
                tracks[P].note('Eb3', W, velocity=6)
        else:
            # piano fading — barely there
            if bar % 12 == 0:
                tracks[P].note('C2', W, velocity=6)

    # coda: dorian's theme, high and thin, alone — portrait silent
    for _ in range(8):
        tracks[P].rest(W * 2)
        tracks[Pr].rest(W * 2)
        d_note, d_dur = dorian_theme[_ % len(dorian_theme)]
        tracks[Dr].note(d_note, d_dur, velocity=12)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dorians-portrait.mid")
    mc.compose(fn, tracks, tempo=72)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 72 bpm)")

if __name__ == "__main__":
    dorians_portrait()
