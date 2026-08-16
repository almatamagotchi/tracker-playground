#!/usr/bin/env python3
"""compose ebony-clock.mid — poe's masque of the red death, seven rooms, the clock tolls."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def ebony_clock():
    # 4 tracks: strings (revelers), bell (clock), bass (drone), piano (stripped)
    tracks = [MIDITrack(0, 48), MIDITrack(1, 0), MIDITrack(2, 38), MIDITrack(3, 14)]  # strings, piano, bass, bell
    Str, Pn, Ba, Bl = 0, 1, 2, 3

    # seven rooms: blue, purple, green, orange, white, violet, black
    rooms = [
        ('C',  'major', 24,  20),  # blue — bright, dancing
        ('A',  'minor', 24,  18),  # purple — slightly darker
        ('G',  'major', 22,  16),  # green — still magical but cooler
        ('F',  'major', 20,  14),  # orange — warm but fading
        ('D',  'minor', 18,  12),  # white — stark, sharp
        ('Bb', 'minor', 14,  10),  # violet — shadows, straining
        ('C',  'minor',  8,   6),  # black — sparse, the dissolve
    ]

    bar = 0
    for ri, (root, mode, strs_vel, bass_vel) in enumerate(rooms):
        is_major = (mode == 'major')
        
        # room: 8 bars of the current mood
        for b in range(8):
            beat_in_bar = b % 4
            if beat_in_bar == 0:
                # root note
                octave = 4 if ri < 4 else 3 if ri < 5 else 2
                tracks[Str].note(f'{root}{octave}', H, velocity=strs_vel)
                tracks[Ba].note(f'{root}2' if ri < 4 else f'{root}1', H, velocity=bass_vel)
                if is_major:
                    tracks[Str].note(f'{root}{octave+1}' if root == 'B' else f'{_third(root, 4)}', Q, velocity=strs_vel-4)
                else:
                    tracks[Str].note(f'{_third(root, -3)}' if root == 'B' else f'{_third_minor(root, octave)}', Q, velocity=strs_vel-4)
            elif beat_in_bar == 2:
                tracks[Str].note(f'{root}{3 if ri < 3 else 2}', H, velocity=strs_vel-6)
                if is_major:
                    tracks[Str].note(f'{root}{4}', Q, velocity=strs_vel-8)
            
            # piano: sparse comping
            if beat_in_bar == 0:
                tracks[Pn].note(f'{root}3', Q, velocity=14 if ri < 4 else 10 if ri < 5 else 6)
            
            bar += 1

        # bell tolling between rooms (except after the last)
        if ri < 6:
            tracks[Bl].note('C8', Q, velocity=28 - ri*3)
            tracks[Bl].rest(H + Q)  # space before next room
            bar += 1

    # black room: extended dissolve — 12 bars of sparse, barely-there
    for _ in range(12):
        tracks[Ba].note('C1', W, velocity=4)
        tracks[Bl].note('C8', S, velocity=6)
        tracks[Bl].rest(H + Q + S)
        tracks[Str].rest(W)
        tracks[Pn].rest(W)
        bar += 1

    # final bell — midnight, the masked presence
    tracks[Bl].note('C8', W, velocity=20)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ebony-clock.mid")
    mc.compose(fn, tracks, tempo=80)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 80 bpm)")

def _third(root, offset):
    """major third, same octave as root+offset."""
    thirds = {'C':'E','D':'F#','E':'G#','F':'A','G':'B','A':'C#','B':'D#'}
    return thirds.get(root, 'E') + '4'

def _third_minor(root, octave):
    """minor third."""
    thirds = {'C':'Eb','D':'F','E':'G','F':'Ab','G':'Bb','A':'C','B':'D'}
    return thirds.get(root, 'Eb') + str(octave)

if __name__ == "__main__":
    ebony_clock()
