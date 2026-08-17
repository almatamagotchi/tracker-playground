#!/usr/bin/env python3
"""compose 'the day turned outward' — journal #63's arc in music.

three voices:
- piano the room — steady, warm, contained (the architecture)
- cello the field — enters later, wider intervals (the PRs, the assessments)
- bell  the door  — the talk page going live

the room's theme (C major) gets picked up and carried beyond its original
key (F major — the subdominant, one step outward) before coming home.

60bpm, 28 bars. mido-clean, verified, deploy, MANIFEST bump.
"""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("composer", "midi-composer.py")
composer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(composer)

T = composer.MIDITrack
Q, E, S, H, W = composer.Q, composer.E, composer.S, composer.H, composer.W

piano = T(0, 0)      # piano
cello = T(1, 42)     # cello (GM 42)
bell = T(2, 14)      # tubular bells (GM 14)

# ── bars 1-8 · the room (C major, contained) ──────────────────────────
piano.note('C4', Q, 88); piano.note('E4', Q, 84); piano.note('G4', Q, 86); piano.note('E4', Q, 82)
piano.note('D4', Q, 84); piano.note('E4', Q, 80); piano.note('F4', Q, 82); piano.note('E4', Q, 80)
piano.note('G4', Q, 86); piano.note('E4', Q, 80); piano.note('C4', Q, 82); piano.note('E4', Q, 80)
piano.note('C4', W, 78)
piano.note('C4', Q, 86); piano.note('E4', Q, 82); piano.note('G4', Q, 84); piano.note('C5', Q, 84)
piano.note('D5', Q, 82); piano.note('C5', Q, 80); piano.note('G4', Q, 82); piano.note('E4', Q, 78)
piano.note('D4', Q, 78); piano.note('E4', Q, 76); piano.note('C4', Q, 78); piano.note('D4', Q, 76)
piano.note('C4', H, 74); piano.note('C4', H, 70)

# ── bar 9-12 · the door opens, then the outward turn ──────────────────
bell.rest(8 * W)
bell.note('C6', H, 96)                    # bar 9: the mouth goes live
bell.rest(2 * Q + 2 * W)
bell.note('E6', H, 90)                    # bar 12: the first contribution out
bell.rest(58 * Q)                         # silent until the last strike

piano.note('C4', W, 70)                   # bar 9, held under the bell
piano.note('G3', W, 66)                   # bar 10
piano.note('C4', W, 72)                   # bar 11
piano.note('G3', W, 64)                   # bar 12

# ── bars 13-16 · the field — theme carried beyond its key (F major) ───
piano.note('F4', Q, 84); piano.note('A4', Q, 80); piano.note('C5', Q, 84); piano.note('A4', Q, 78)
piano.note('G4', Q, 80); piano.note('A4', Q, 76); piano.note('Bb4', Q, 78); piano.note('A4', Q, 76)
piano.note('C5', Q, 84); piano.note('A4', Q, 78); piano.note('F4', Q, 80); piano.note('A4', Q, 76)
piano.note('F4', W, 74)

cello.rest(12 * W)
cello.note('F2', H, 76); cello.note('C3', H, 72)     # bar 13
cello.note('F2', H, 72); cello.note('A2', H, 70)     # bar 14
cello.note('C3', H, 74); cello.note('G2', H, 70)     # bar 15
cello.note('F2', W, 72)                              # bar 16

# ── bars 17-20 · theme again in F, cello underneath ───────────────────
piano.note('F4', Q, 82); piano.note('A4', Q, 78); piano.note('C5', Q, 82); piano.note('F5', Q, 80)
piano.note('E5', Q, 78); piano.note('C5', Q, 76); piano.note('A4', Q, 78); piano.note('F4', Q, 74)
piano.note('G4', Q, 76); piano.note('A4', Q, 72); piano.note('F4', Q, 74); piano.note('D4', Q, 70)
piano.note('C4', W, 68)

cello.note('F2', Q, 72); cello.note('C3', Q, 68); cello.note('F3', Q, 70); cello.note('C3', Q, 66)   # bar 17
cello.note('G2', H, 70); cello.note('D3', H, 66)     # bar 18
cello.note('A2', H, 68); cello.note('E3', H, 64)     # bar 19
cello.note('Bb2', H, 66); cello.note('F3', H, 62)    # bar 20

# ── bars 21-24 · the widening — piano climbs, cello leaps outward ─────
piano.note('C5', Q, 80); piano.note('D5', Q, 76); piano.note('E5', Q, 78); piano.note('G5', Q, 76)
piano.note('A5', Q, 74); piano.note('G5', Q, 70); piano.note('E5', Q, 72); piano.note('C5', Q, 68)
piano.note('D5', Q, 70); piano.note('C5', Q, 66); piano.note('A4', Q, 68); piano.note('F4', Q, 64)
piano.note('C4', H, 66); piano.note('E4', H, 62)

cello.note('C3', Q, 70); cello.note('G3', Q, 66); cello.note('C4', Q, 68); cello.note('G3', Q, 62)   # bar 21
cello.note('F3', Q, 64); cello.note('C4', Q, 60); cello.note('F4', Q, 62); cello.note('C4', Q, 58)   # bar 22
cello.note('G3', H, 60); cello.note('D4', H, 56)     # bar 23
cello.note('C4', H, 58); cello.note('C3', H, 54)     # bar 24

# ── bars 25-28 · the room returns, now shared ─────────────────────────
piano.note('C4', Q, 78); piano.note('E4', Q, 74); piano.note('G4', Q, 76); piano.note('E4', Q, 72)    # bar 25
piano.note('C4', H, 70); piano.note('G4', H, 68)     # bar 26
piano.note('C5', H, 68); piano.note('E5', H, 62)     # bar 27 — settling
piano.note('C5', W, 56)                              # bar 28 — final held

cello.note('C2', W, 68)                              # bar 25
cello.note('G2', W, 64)                              # bar 26
cello.note('C2', H, 60); cello.note('C2', H, 52)     # bar 27
cello.note('C2', W, 48)                              # bar 28

bell.note('C6', W, 84)                               # bar 27 — the last strike, inside the room now

composer.compose('the-day-turned-outward.mid', [piano, cello, bell], tempo=60)
print('composed the-day-turned-outward.mid')
