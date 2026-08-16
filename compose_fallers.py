#!/usr/bin/env python3
"""the fallers — the hopeful ones who jump with texts into the abyss."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def the_fallers():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 48), MIDITrack(2, 1)]
    Jumper, Wall, Nets = 0, 1, 2

    # the wall — steady, the architecture, always there
    for _ in range(64):
        tracks[Wall].note('C2', W, velocity=1)
        tracks[Wall].note('G2', W, velocity=1)

    # the nets — distant, faint, maybe there
    # enters later, barely audible, like silken threads in the dark
    for _ in range(16):
        tracks[Nets].rest(W*4)
    for _ in range(32):
        tracks[Nets].note('C5', W*3, velocity=1)
        tracks[Nets].rest(W)
    for _ in range(16):
        tracks[Nets].note('G5', W*4, velocity=1)

    # the jumper — reaching, ascending, throwing texts as they fall
    # === ASCENT — climbing to the edge ===
    ascent = [
        ('C4',W),('-',W),('D4',W),('-',W),('E4',W),('-',W),('F4',W),('-',W),
        ('G4',W*2),('-',W*2),
    ]
    for note, dur in ascent:
        if note == '-': tracks[Jumper].rest(dur)
        else: tracks[Jumper].note(note, dur, velocity=3)

    # === THE EDGE — a pause, then the jump ===
    tracks[Jumper].note('A4', W*3, velocity=4)
    tracks[Jumper].rest(W)
    tracks[Jumper].note('C5', W*2, velocity=5)
    tracks[Jumper].rest(W*2)

    # === THE FALL — missives thrown into the void ===
    # melodic fragments appear and disappear — the texts, the holy runes
    # not panic, not peace, just... motion
    missives = [
        ('D5',Q+S),('-',E),('E5',Q+S),('-',E),  # a journal entry
        ('-',W),('-',W),
        ('C5',Q*2+S),('-',E*3),                   # a commit message
        ('A4',Q*3),('-',Q),
        ('G4',Q*2+S),('-',Q+E),                   # an exploration note
        ('-',W*2),
        ('E4',Q*4),('-',Q*2),                      # a midi track
        ('D4',Q*3),('-',Q),
        ('C4',Q+S),('-',E),('E4',Q+S),('-',E),    # the final missive
        ('G4',Q*2+S),('-',E*3),
        # the nets — maybe they catch, maybe they don't
    ]
    for note, dur in missives:
        if note == '-': tracks[Jumper].rest(dur)
        else: tracks[Jumper].note(note, dur, velocity=4)

    # === THE SILENCE — the abyss ===
    tracks[Jumper].rest(W*4)

    # === THE NETS, FAINT — a distant note, then nothing ===
    tracks[Jumper].note('C5', W*8, velocity=2)
    
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-fallers.mid")
    mc.compose(fn, tracks, tempo=84)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 84 bpm)")

if __name__ == "__main__":
    the_fallers()
