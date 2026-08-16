#!/usr/bin/env python3
"""compose handshake.mid — the modem negotiation sequence, two voices finding each other."""

import sys, os, importlib.util, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def handshake():
    # 2 voices: caller (violin) + answerer (cello) — plus noise (percussion) as the channel interference
    tracks = [MIDITrack(0, 40), MIDITrack(1, 42), MIDITrack(9, 0)]
    Vn, Cello, Nz = 0, 1, 2

    # ── phase 1 · noise ── (bars 1-12)
    # discordant, chaotic — two systems trying to connect, nothing but static
    for _ in range(12):
        tracks[Nz].note('C3', Q, velocity=6)
        tracks[Nz].note('D3', Q, velocity=5)
        tracks[Nz].note('E3', Q, velocity=4)
        tracks[Nz].note('C3', Q, velocity=6)

    # violin: scattered, dissonant fragments
    frags = ['C4','Eb4','G4','Bb4','D4','F4','A4','C5',
             'Db4','E4','Ab4','B4','D4','F#4','Bb4','Db5']
    for i, f in enumerate(frags[:12]):
        tracks[Vn].note(f, Q, velocity=8)
        tracks[Vn].rest(Q)

    # cello: low rumble, also discordant
    for i in range(12):
        tracks[Cello].note(frags[i % len(frags)].replace('4','2').replace('5','3').replace('b',''), Q, velocity=8)
        tracks[Cello].rest(Q)

    # ── phase 2 · the handshake begins ── (bars 13-28)
    # noise softens, patterns emerge, two voices start listening
    for _ in range(16):
        tracks[Nz].note('C3', Q, velocity=3)
        tracks[Nz].rest(Q)

    # violin: tentative call — a single phrase repeated, each time slightly more confident
    call = [('C5', Q+Q), ('D5', Q), ('E5', Q), ('G5', H)]
    for rep in range(4):
        vel = 10 + rep * 2
        for note, dur in call:
            tracks[Vn].note(note, dur, velocity=vel)
        tracks[Vn].rest(W)

    # cello: tentative response — picks up the call, echoes it lower
    resp = [('C3', Q+Q), ('D3', Q), ('E3', Q), ('G3', H)]
    for rep in range(4):
        vel = 10 + rep * 2
        for note, dur in resp:
            tracks[Cello].note(note, dur, velocity=vel)
        tracks[Cello].rest(W)

    # ── phase 3 · negotiation ── (bars 29-40)
    # both voices together, overlapping, finding common ground
    called = [('C5', H), ('E5', H), ('G5', Q+Q), ('C6', Q), ('G5', Q),
              ('E5', Q+Q), ('D5', Q), ('C5', Q), ('E5', H+Q), ('-', Q)]
    for note, dur in called:
        if note == '-': tracks[Vn].rest(dur)
        else: tracks[Vn].note(note, dur, velocity=16)

    answered = [('C3', H), ('E3', H), ('G3', Q+Q), ('C4', Q), ('G3', Q),
               ('E3', Q+Q), ('D3', Q), ('C3', Q), ('E3', H+Q), ('-', Q)]
    for note, dur in answered:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=14)

    # noise drops to barely there — the channel is clearing
    for _ in range(12):
        tracks[Nz].note('C3', S, velocity=2)
        tracks[Nz].rest(Q*3 + S)

    # ── phase 4 · connected ── (bars 41-56)
    # clean harmony, two voices in unison, the communication flowing
    refrain = [
        ('C5', H), ('D5', H), ('E5', Q+Q), ('C6', Q), ('G5', Q),
        ('E5', W), ('-', W),
        ('G5', H), ('A5', H), ('C6', Q+Q), ('G5', Q), ('E5', Q),
        ('D5', W+H), ('-', Q),
        ('C5', W), ('E5', W), ('G5', W), ('C6', W*2),
    ]
    for note, dur in refrain:
        if note == '-': tracks[Vn].rest(dur)
        else: tracks[Vn].note(note, dur, velocity=18)

    # cello harmonizes a third below
    harmony = [
        ('E4', H), ('G4', H), ('C5', Q+Q), ('E5', Q), ('E4', Q),
        ('C5', W), ('-', W),
        ('E4', H), ('C5', H), ('E5', Q+Q), ('E4', Q), ('C5', Q),
        ('G4', W+H), ('-', Q),
        ('E4', W), ('C5', W), ('E5', W), ('C5', W*2),
    ]
    for note, dur in harmony:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=16)

    # silence — the channel is open, the conversation flows
    for _ in range(8):
        tracks[Nz].rest(W)
        tracks[Vn].rest(W)
        tracks[Cello].rest(W)

    # one last handshake acknowledgment — both voices, together, fading
    for vel in [14,10,6,3]:
        tracks[Vn].note('C6', W, velocity=vel)
        tracks[Cello].note('C4', W, velocity=vel)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "handshake.mid")
    mc.compose(fn, tracks, tempo=96)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 96 bpm)")

if __name__ == "__main__":
    handshake()
