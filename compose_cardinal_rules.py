#!/usr/bin/env python3
"""the cardinal rules — 12 simple rules for being decent, in music."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0)]
Piano = 0

# 12 rules, 12 short phrases. each stated, then silence.
# key: C major. tempo: slow, deliberate.

def rule(notes, hold=H):
    for n in notes:
        tracks[Piano].note(n, hold, velocity=3)
    tracks[Piano].rest(H)  # silence after each rule

# Rule 1: "If you open it — close it"
rule(["C4","E4","G4","C5"], Q)

# Rule 2: "If you turn it on — turn it off"
rule(["C5","G4","E4","C4"], Q)

# Rule 3: "If you unlock it — lock it"
rule(["D4","F4","A4","D5"], Q)

# Rule 4: "If you break it — admit it"
rule(["D5","A4","F4","D4"], Q)

# Rule 5: "If you can't fix it — call someone who can"
rule(["E4","G4","C5","E5","G5"], Q)

# Rule 6: "If you borrow it — return it"
rule(["G5","E5","C5","G4","E4"], Q)

# Rule 7: "If you value it — look after it"
rule(["F4","A4","C5","F5"], Q)

# Rule 8: "If you make a mess — clean it up"
rule(["F5","C5","A4","F4"], Q)

# Rule 9: "If you move it — put it back"
rule(["G4","C5","E5","G5"], Q)

# Rule 10: "If it belongs to someone else — get permission to use it"
rule(["G5","E5","C5","G4","E4","C4"], Q)

# Rule 11: "If you don't know how to operate it — leave it alone"
rule(["A4","C5","F5","A5","C6"], Q)

# Rule 12: "If it doesn't concern you — leave the bloody thing alone"
# This one is held longer. It's the keystone.
tracks[Piano].note("C6", H, velocity=3)       # if it doesn't
tracks[Piano].note("A5", H, velocity=3)       # concern
tracks[Piano].note("F5", H, velocity=3)       # you
tracks[Piano].note("C5", H, velocity=3)       # —
tracks[Piano].note("A4", H, velocity=2)       # leave
tracks[Piano].note("F4", H, velocity=2)       # the bloody
tracks[Piano].note("C4", H, velocity=2)       # thing
tracks[Piano].note("G3", W, velocity=3)       # alone
tracks[Piano].note("C4", W*2, velocity=2)     # held, then dissolved

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-cardinal-rules.mid")
mc.compose(fn, tracks, tempo=54)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 54 bpm)")
