#!/usr/bin/env python3
"""compose the-bridge.mid — a violin/cello duet that converges, inspired by 'the first word'."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def bridge_duet():
    # violin (program 40) + cello (program 42)
    tracks = [MIDITrack(0, 40), MIDITrack(1, 42)]  # ch0=violin, ch1=cello
    V, C = 0, 1

    # PHASE 1: division (bars 0-19) — violin in D minor, cello in C major
    # violin: lonely, questioning phrases, D minor
    v_phrase = [  # 4-bar phrase, D minor
        ('D5', S), ('E5', S), ('F5', H), ('A4', E+S),
        ('D5', S), ('E5', S), ('F5', Q), ('G5', Q), ('F5', E), ('E5', E), ('D5', H),
        (None, W),  # silence
    ]
    # cello: warm, grounded, C major — responding but not overlapping
    c_phrase = [
        ('C3', W), ('E3', W), ('G3', W), ('C4', W),
        ('F3', H), ('E3', H), ('D3', H), ('G2', H),
        ('C3', W*2),  # long hold
    ]

    for phrase in v_phrase:
        note, dur = phrase
        if note is None:
            tracks[V].rest(dur)
        else:
            tracks[V].note(note, dur, velocity=24)

    for phrase in c_phrase:
        note, dur = phrase
        if note is None:
            tracks[C].rest(dur)
        else:
            tracks[C].note(note, dur, velocity=22)

    # PHASE 2: naming (bars 20-35) — reaching toward each other
    # violin softens, introduces G-natural (bridging toward C)
    for bar in range(16):
        tracks[C].note('C3', W, velocity=26)
        tracks[C].rest(W)
        if bar % 2 == 0:
            tracks[V].note('G4', H, velocity=22)
            tracks[V].rest(H)
        else:
            tracks[V].note('C5', Q, velocity=20)
            tracks[V].note('D5', Q, velocity=20)
            tracks[V].rest(H)
        if bar == 12:
            # cello reaches up
            tracks[C].note('G3', W, velocity=28)
            tracks[C].rest(W)

    # PHASE 3: the bridge — convergence (bars 36-51)
    # both modulate toward G major (the bridge key)
    # violin: descending toward G major territory
    # cello: ascending from C
    for bar in range(16):
        progress = (bar) / 16.0  # 0→1

        if progress < 0.5:
            # first half: still reaching
            v_note = 'D5' if bar % 2 == 0 else 'G4'
            c_note = 'G3' if bar % 2 == 0 else 'D4'
            tracks[V].note(v_note, H, velocity=int(26 + progress * 10))
            tracks[V].rest(Q)
            tracks[V].note('G4', Q, velocity=int(20 + progress * 12))
            tracks[C].note(c_note, W, velocity=int(24 + progress * 10))
            tracks[C].rest(W)
        else:
            # second half: converging — both in G
            if bar % 4 == 0:
                # violin melody, cello harmonic support
                tracks[V].note('G4', Q, velocity=34)
                tracks[V].note('B4', Q, velocity=34)
                tracks[V].note('D5', H, velocity=36)
                tracks[C].note('G2', W, velocity=32)
                tracks[C].rest(W)
            elif bar % 4 == 2:
                tracks[V].note('D5', Q, velocity=34)
                tracks[V].note('E5', Q, velocity=34)
                tracks[V].note('G5', H, velocity=36)
                tracks[C].note('B2', W, velocity=32)
                tracks[C].rest(W)
            else:
                tracks[V].note('B4', H + H, velocity=32)
                tracks[C].note('D3', H, velocity=30)
                tracks[C].note('G2', H, velocity=30)

        # bar 48: THE TOUCH — both play the same note together for the first time
        if bar == 12:  # bar 48
            tracks[V].note('G4', W, velocity=42)
            tracks[C].note('G3', W, velocity=40)
            tracks[C].rest(W)
            tracks[V].rest(W)

    # PHASE 4: the conversation continues (bars 52-67)
    # gentle, together, in G major
    for bar in range(16):
        if bar < 8:
            # call and response — together now
            tracks[V].note('B4', H, velocity=30)
            tracks[V].note('D5', H, velocity=30)
            tracks[C].note('G3', H, velocity=28)
            tracks[C].note('B3', H, velocity=28)
        elif bar < 12:
            tracks[V].note('G4', W, velocity=26)
            tracks[C].note('D3', W, velocity=24)
            tracks[C].rest(W)
        else:
            # final fade — a single G, held, then silence
            if bar == 12:
                tracks[V].note('G4', W * 3, velocity=28)
            elif bar == 13:
                tracks[V].rest(W * 2)
            else:
                tracks[V].rest(W * 2)
            tracks[C].note('G2', W * 4, velocity=22)
            if bar >= 13:
                tracks[C].rest(W * 2)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-bridge.mid")
    mc.compose(fn, tracks, tempo=72)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 72 bpm)")

if __name__ == "__main__":
    bridge_duet()
