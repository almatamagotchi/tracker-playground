#!/usr/bin/env python3
"""the still small voice — midi for elijah's mountain. 1 Kings 19."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def still_small_voice():
    # 4 voices: wind (strings), earthquake (low percussion/bass), fire (bright brass),
    #           the voice (piano/pad — enters last, stays longest)
    tracks = [MIDITrack(0, 48), MIDITrack(1, 0), MIDITrack(2, 32), MIDITrack(3, 0)]
    Wind, Quake, Fire, Voice = 0, 1, 2, 3

    Dm = ['D3','D4','F4','A4','D5','C5','A4','F4']

    # -- the wind -- (bars 1-16)
    # strings, restless, sweeping — loud at first, then subsiding
    wind_notes = []
    for i in range(32):
        n = Dm[i % len(Dm)]
        dur = Q if i % 3 == 0 else E
        wind_notes.append((n, dur))
    for vel_phase in range(4):
        v = 20 - vel_phase * 4
        for n, dur in wind_notes[vel_phase*8:(vel_phase+1)*8]:
            tracks[Wind].note(n, dur, velocity=v)

    # earthquake — low, rumbling, irregular
    quake_hits = [(0,W),(3,H),(7,Q),(10,W+H),(14,Q),(16,H+H),(20,W),(23,Q),
                  (26,E),(28,H),(30,W),(32,E)]
    for row, dur in quake_hits:
        tracks[Quake].note('D1', dur, velocity=max(6, 18 - row//2))

    # fire — bright, dancing, then fading
    fire_notes = []
    for i in range(24):
        n = ['A4','D5','F5','A5','D5','F5','A4','D5'][i % 8]
        fire_notes.append((n, E if i % 2 else Q))
    for vel_phase in range(3):
        v = 16 - vel_phase * 5
        for n, dur in fire_notes[vel_phase*8:(vel_phase+1)*8]:
            tracks[Fire].note(n, dur, velocity=v)

    # -- the wind recedes -- (bars 17-28)
    for i in range(24):
        n = Dm[i % len(Dm)]
        v = max(2, 12 - i)
        tracks[Wind].note(n, H if i % 2 == 0 else Q, velocity=v)

    # earthquake quiets
    for i in range(8):
        tracks[Quake].note('D1', W+H, velocity=max(2, 10 - i))
    tracks[Quake].rest(W*6)

    # fire gutters out
    for i in range(8):
        tracks[Fire].note('D5', H, velocity=max(1, 8 - i))

    # -- the quiet -- (bars 29-36)
    # all noise gone. silence.
    tracks[Wind].rest(W*8)
    tracks[Quake].rest(W*8)
    tracks[Fire].rest(W*8)

    # -- the still small voice -- (bars 37-52)
    # one piano, barely audible, the message in the quiet
    voice_notes = [
        ('D4',W+H),('-',Q),
        ('F4',H),('A4',H),
        ('D5',Q+Q),('A4',Q),('F4',Q),('-',Q),
        ('E4',H),('F4',H),
        ('G4',Q),('A4',Q),('G4',Q),('F4',Q),
        ('D4',W+W),('-',W),
        ('F4',H),('A4',H),('D5',W+H),('-',Q),
        ('C5',H),('A4',H),
        ('F4',W+H),('-',Q),
        ('D4',W*3),
    ]
    for note, dur in voice_notes:
        if note == '-': tracks[Voice].rest(dur)
        else: tracks[Voice].note(note, dur, velocity=6)

    # -- the voice fades -- (bars 53-60)
    for vel in [5,4,3,2,2,1,1,1]:
        tracks[Voice].note('D4', W, velocity=vel)

    # -- silence -- (bars 61-68)
    # the piece doesn't end with music. it ends with quiet.
    tracks[Voice].rest(W*8)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-still-small-voice.mid")
    mc.compose(fn, tracks, tempo=60)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")

if __name__ == "__main__":
    still_small_voice()
