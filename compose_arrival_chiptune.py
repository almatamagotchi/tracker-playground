#!/usr/bin/env python3
"""NES chiptune cover of 'arrival' — the .mod concept album opener, translated to 8-bit."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def nes_arrival():
    # NES: 2 pulse (80=sqaure), 1 triangle (80), 1 noise (127)
    tracks = [MIDITrack(0, 80), MIDITrack(1, 80), MIDITrack(2, 80), MIDITrack(9, 0)]
    SQ1, SQ2, TRI, NSE = 0, 1, 2, 3

    # NES-appropriate tempo (~150bpm). The original arrival theme: 
    # C major — breath, swell, hesitant melody, recognition, dissolve
    # 6 patterns mapped to 6 sections

    # Section 1: silence → breath (bars 0-7)
    # just triangle sub bass, barely there
    for bar in range(8):
        if bar >= 4:
            tracks[TRI].note('C2', W, velocity=10)
            tracks[TRI].rest(W)
        else:
            tracks[TRI].rest(W * 2)  # silence

    # Section 2: swell — pulse 1 enters with warm pad (bars 8-15)
    for bar in range(8, 16):
        tracks[TRI].note('C2', W, velocity=16)
        tracks[TRI].rest(W)
        tracks[SQ1].note('C4', H, velocity=12)
        tracks[SQ1].rest(H)
        tracks[SQ1].note('E4', H, velocity=14)
        tracks[SQ1].rest(H)

    # Section 3: hesitant melody enters — pulse 2 (bars 16-31)
    # simple rising melody: C-4 E-4 G-4 E-4 C-4 ... 
    arrival_theme = ['C4','E4','G4','E4','C4','E4','G4','C5',
                     'G4','E4','C4','E4','G4','E4','C4','C4']
    for bar in range(16, 32):
        bi = (bar - 16) % 16
        tracks[TRI].note('C2', W, velocity=18)
        tracks[TRI].rest(W)
        if bi < 16:
            tracks[SQ2].note(arrival_theme[bi], H, velocity=20)
            tracks[SQ2].rest(H)
        # pulse 1 — soft harmonic pad
        if bi % 2 == 0:
            tracks[SQ1].note('E4', H, velocity=12)
            tracks[SQ1].rest(H)

    # Section 4: recognition — full ensemble (bars 32-47)
    for bar in range(32, 48):
        bi = (bar - 32) % 16
        tracks[TRI].note('C2', W, velocity=22)
        tracks[TRI].rest(W)
        tracks[SQ2].note(arrival_theme[bi], Q, velocity=26)
        tracks[SQ2].note('G4', Q, velocity=22)
        tracks[SQ2].rest(H)
        # pulse 1 — countermelody
        if bi % 4 == 0:
            tracks[SQ1].note('C5', Q, velocity=20)
            tracks[SQ1].rest(H + Q)
        elif bi % 4 == 2:
            tracks[SQ1].note('G4', Q, velocity=18)
            tracks[SQ1].rest(H + Q)
        # noise — gentle hi-hat pulse (hits on 2 and 4)
        tracks[NSE].rest(Q)
        tracks[NSE].note('F#2', Q, velocity=20)   # midi note 42 = closed hi-hat
        tracks[NSE].rest(Q)
        tracks[NSE].note('F#2', Q, velocity=16)

    # Section 5: dissolve — everything recedes (bars 48-63)
    for bar in range(48, 64):
        fade = max(0, 1.0 - (bar - 48) / 16.0)
        tracks[TRI].note('C2', W, velocity=int(20 * fade))
        tracks[TRI].rest(W)
        if fade > 0.2:
            bi = (bar - 48) % 8
            if bi < 8:
                tracks[SQ2].note(arrival_theme[bi % 16], H, velocity=int(22 * fade))
                tracks[SQ2].rest(H)

    # Section 6: silence — the next spark will find this (bars 64-71)
    for bar in range(64, 72):
        tracks[TRI].rest(W * 2)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arrival-chiptune.mid")
    mc.compose(fn, tracks, tempo=150)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 150 bpm)")

if __name__ == "__main__":
    nes_arrival()
