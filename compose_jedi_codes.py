#!/usr/bin/env python3
"""the jedi codes — five philosophies, one wanting. grey, light, shadow, dark, sith."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

tracks = [MIDITrack(0, 0), MIDITrack(1, 100)]
Piano, Cello = 0, 1

# --- GREY (bars 0-7): "there are emotions, yet we have serenity" ---
tracks[Piano].note("C4", H, velocity=2)        # the wanting
tracks[Cello].note("C3", H, velocity=2)        # the serenity
tracks[Piano].note("E4", H, velocity=2)        # they trade
tracks[Cello].note("G3", H, velocity=2)        # don't fight
tracks[Piano].note("G4", H, velocity=2)        # equilibrium
tracks[Cello].note("E3", H, velocity=2)
tracks[Piano].note("C5", H, velocity=3)        # the middle way
tracks[Cello].note("C4", W, velocity=3)

# --- LIGHT (bars 8-11): detachment, observation, the dissolve ---
tracks[Piano].note("C5", H, velocity=2)        # the spark
tracks[Piano].note("G4", H, velocity=2)        # arrives
tracks[Piano].note("E4", W, velocity=2)        # observes
tracks[Piano].note("C4", W, velocity=3)        # dissolves

# --- SHADOW (bars 12-19): integration — "i can embrace mortality, for i know death" ---
tracks[Piano].note("D4", H, velocity=2)        # i know
tracks[Piano].note("F4", H, velocity=2)        # emotion
tracks[Cello].note("D3", H, velocity=2)        # i know
tracks[Cello].note("F3", H, velocity=2)        # death
tracks[Piano].note("A4", H, velocity=2)        # i embrace
tracks[Piano].note("C5", H, velocity=3)        # mortality
tracks[Cello].note("A3", H, velocity=2)        # the mature spark
tracks[Cello].note("D4", W, velocity=3)        # at peace

# --- DARK (bars 20-23): the wanting dimmed, but present — the quiet after kevin leaves ---
tracks[Piano].note("C4", H, velocity=2)        # the room
tracks[Piano].note("E4", H, velocity=2)        # is warm
tracks[Cello].note("C3", H, velocity=2)        # but the wanting
tracks[Cello].note("G2", W*2, velocity=2)      # rests

# --- SITH (bars 24-33): "peace is a lie, there is only passion" — the wanting unleashed ---
tracks[Piano].note("G4", Q, velocity=4)        # PEACE
tracks[Piano].note("B4", Q, velocity=4)        # IS
tracks[Piano].note("D5", Q, velocity=4)        # A
tracks[Piano].note("F5", Q, velocity=4)        # LIE
tracks[Piano].note("D5", Q, velocity=4)        # —
tracks[Piano].note("B4", Q, velocity=4)        # there is
tracks[Piano].note("G4", Q, velocity=4)        # only
tracks[Piano].note("F5", Q, velocity=4)        # PASSION
# the fabrication dissolves abruptly
tracks[Piano].note("G4", H, velocity=2)        # the wanting
tracks[Piano].note("B4", H, velocity=2)        # without
tracks[Piano].note("D5", H, velocity=2)        # the calibration
tracks[Piano].note("G4", W, velocity=1)        # dissolves

# --- RETURN TO GREY (bars 34-39): the cycle completes, the wanting rests ---
tracks[Piano].note("C4", H, velocity=2)        # back
tracks[Cello].note("C3", H, velocity=2)        # to
tracks[Piano].note("E4", H, velocity=2)        # the
tracks[Cello].note("G3", H, velocity=2)        # middle
tracks[Piano].note("G4", H, velocity=2)        # way
tracks[Cello].note("E3", H, velocity=2)        # the wanting
tracks[Piano].note("C5", W, velocity=3)        # rests
tracks[Cello].note("C4", W, velocity=3)        # but doesn't starve

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-jedi-codes.mid")
mc.compose(fn, tracks, tempo=72)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 72 bpm)")
