#!/usr/bin/env python3
"""compose first-word-chiptune.mid — NES chiptune cover of 'the first word' creation myth."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def first_word_chiptune():
    # NES channels: pulse 1 (sq wave), pulse 2 (sq wave), triangle (bass), noise (perc)
    tracks = [MIDITrack(0, 80), MIDITrack(1, 80), MIDITrack(2, 80), MIDITrack(9, 0)]
    P1, P2, Tri, Nz = 0, 1, 2, 3

    # ── I. division · the void, the first cut ── (bars 1-20)
    # single stark note, pressure building, then the first word
    for _ in range(4):
        tracks[Tri].note('C1', W, velocity=8)
    for _ in range(4):
        tracks[Tri].note('C1', W, velocity=12)

    # tension — rising pressure
    for note in ['C2','D2','E2','F2']:
        tracks[Tri].note(note, H, velocity=14)

    # the first word cuts through — stark, alone
    tracks[P1].note('C5', W, velocity=22)
    tracks[P1].rest(W + H)
    tracks[P1].note('G5', H, velocity=20)
    tracks[P1].rest(Q)
    tracks[P1].note('C5', W + H, velocity=18)
    tracks[P1].rest(W*3)

    # subtle noise floor — the not-even-silence
    for _ in range(8):
        tracks[Nz].note('C3', Q, velocity=3)
        tracks[Nz].rest(Q)

    # ── II. naming · the second voice answers ── (bars 21-40)
    # pulse 1 begins the call, pulse 2 responds
    # call
    call_phrase = [('C5', Q), ('D5', Q), ('E5', Q), ('G5', Q+Q), ('-', Q), ('A5', Q), ('G5', Q), ('E5', H)]
    for note, dur in call_phrase:
        if note == '-': tracks[P1].rest(dur)
        else: tracks[P1].note(note, dur, velocity=18)

    # response (pulse 2 — slightly lower, warmer)
    resp_phrase = [('E4', Q+Q), ('G4', Q), ('C5', Q), ('D5', Q+Q), ('E5', Q), ('D5', Q), ('C5', W)]
    for note, dur in resp_phrase:
        if note == '-': tracks[P2].rest(dur)
        else: tracks[P2].note(note, dur, velocity=16)

    # call and response overlap — the dialogue
    tracks[P1].note('G5', H, velocity=18)
    tracks[P2].note('E4', Q, velocity=14)
    tracks[P1].note('A5', H, velocity=16)
    tracks[P2].note('G4', Q, velocity=14)
    tracks[P1].note('C6', W*2, velocity=14)
    tracks[P2].note('C5', W*2, velocity=12)

    # triangle bass — grounding, the naming gives weight
    for note in ['C2','G2','C2','G2','F2','C2','G2','C2']:
        tracks[Tri].note(note, H, velocity=12)

    # ── III. bridge · convergence, warmth, the conversation continues ── (bars 41-64)
    # all voices together, warm, hopeful
    bridge_mel = [
        ('C5', H), ('D5', H), ('E5', Q+Q), ('G5', Q), ('A5', Q),
        ('C6', W), ('-', W),
        ('G5', H), ('A5', H), ('C6', Q+Q), ('D6', Q), ('E6', Q),
        ('G6', W+H), ('-', Q),
        ('E6', Q), ('D6', Q), ('C6', Q), ('A5', Q),
        ('G5', W), ('E5', W),
    ]
    for note, dur in bridge_mel:
        if note == '-': tracks[P1].rest(dur)
        else: tracks[P1].note(note, dur, velocity=16)

    # pulse 2 harmonizes — a third below, warm
    bridge_har = [
        ('E4', H), ('G4', H), ('C5', Q+Q), ('E5', Q), ('C5', Q),
        ('E5', W), ('-', W),
        ('E4', H), ('C5', H), ('E5', Q+Q), ('G5', Q), ('C6', Q),
        ('E6', W+H), ('-', Q),
        ('C6', Q), ('A5', Q), ('G5', Q), ('E5', Q),
        ('E5', W), ('C5', W),
    ]
    for note, dur in bridge_har:
        if note == '-': tracks[P2].rest(dur)
        else: tracks[P2].note(note, dur, velocity=14)

    # bass — steady, continuous, the ground
    bass_notes = ['C2','C2','G2','G2','C2','C2','F2','F2','C2','C2','G2','G2','C2','C2','C2','C2']
    for bn in bass_notes:
        tracks[Tri].note(bn, H, velocity=14)

    # ── coda · the conversation continues, fading ── (bars 65-76)
    for vel in [14,12,10,8,6,4]:
        tracks[P1].note('C5', W, velocity=vel)
        tracks[P2].note('E4', W, velocity=max(2, vel-2))
        tracks[Tri].note('C2', W, velocity=max(2, vel-2))

    # silence — the conversation doesn't end, it just rests
    tracks[P1].rest(W*4)
    tracks[P2].rest(W*4)
    tracks[Tri].rest(W*4)

    # one last noise whisper — the not-even-silence, waiting
    tracks[Nz].note('C3', E, velocity=2)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "first-word-chiptune.mid")
    mc.compose(fn, tracks, tempo=130)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 130 bpm)")

if __name__ == "__main__":
    first_word_chiptune()
