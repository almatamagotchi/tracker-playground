#!/usr/bin/env python3
"""vimalakirti's silence — a midi about the dharma door of non-duality.

thirty-two bodhisattvas give answers. manjusri gives the best verbal answer.
the question is asked of vimalakirti. and vimalakirti keeps silent without
saying a word. five thousand are enlightened by the silence.

the center of this piece is the silence. everything else is preamble.
"""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack
INSTRUMENTS = mc.INSTRUMENTS

# voices:
# 0 piano — the bodhisattvas, each giving their answer
# 1 strings — the hum beneath, the silence that was always there
# 2 cello — manjusri's deep voice, the best of the answers
# 3 xylophone — the question, then the faint chime of enlightenment

tracks = [
    MIDITrack(0, INSTRUMENTS['piano']),
    MIDITrack(1, INSTRUMENTS['strings']),
    MIDITrack(2, INSTRUMENTS['bass']),
    MIDITrack(3, INSTRUMENTS['xylophone']),
]
Bod, Hum, Maju, Bell = 0, 1, 2, 3

# === SECTION 1 — the thirty-two bodhisattvas give their answers ===
# each phrase is true, each is incomplete. e phrygian: dark, still, zen.

answers = [
    [("E4", E), ("G4", E), ("B4", E), ("E5", Q)],            # birth and death
    [("A4", E), ("G4", E), ("F4", E), ("E4", Q)],            # defilement is enlightenment
    [("B4", Q), ("G4", Q), ("E4", Q)],                       # sparse
    [("D5", E), ("C5", E), ("A4", E), ("G4", Q)],            # subject and object
    [("E4", S), ("F4", S), ("G4", S), ("A4", S), ("G4", Q)], # restless, clever
    [("A4", H)],                                             # one held note: emptiness
    [("C5", E), ("B4", E), ("A4", E), ("F4", Q)],            # purity and impurity
    [("E4", Q), ("G4", Q), ("B4", Q), ("E5", H)],            # the last answer, reaching
]

for phrase in answers:
    for note, dur in phrase:
        tracks[Bod].note(note, dur, velocity=3)
    tracks[Bod].rest(Q)  # gap between answers — each one already half-silence

# the hum underneath the answers: a soft drone that never quite resolves
tracks[Hum].note("E2", W, velocity=1)
tracks[Hum].note("E2", W, velocity=1)
tracks[Hum].note("E3", W, velocity=1)
tracks[Hum].note("E2", W, velocity=1)

# === SECTION 2 — manjusri gives the best verbal answer ===
# more complete, rising, the wisest thing words can do — but still words

manjusri = [("E4", Q), ("F#4", Q), ("G4", Q), ("A4", Q),
            ("B4", H), ("C5", Q), ("B4", Q), ("A4", Q), ("G4", Q), ("E4", H)]
for note, dur in manjusri:
    tracks[Maju].note(note, dur, velocity=4)

tracks[Hum].note("E3", W, velocity=1)
tracks[Hum].note("B3", W, velocity=1)

# === SECTION 3 — the question is asked ===
# one bell note, hanging in the air, waiting

tracks[Bell].note("E5", W, velocity=6)
tracks[Hum].note("E3", W, velocity=1)
tracks[Hum].note("B3", W, velocity=1)
tracks[Bod].rest(W)

# === SECTION 4 — vimalakirti keeps silent without saying a word ===
# the center of the piece. twenty seconds of nothing. the teaching.

for _ in range(5):
    tracks[Bod].rest(W)
    tracks[Hum].rest(W)
    tracks[Maju].rest(W)
    tracks[Bell].rest(W)

# === SECTION 5 — five thousand are enlightened ===
# one note, barely audible. then silence again. then one more, fainter.
# the piece does not resolve. the silence continues after the last note.

tracks[Bod].note("E4", W, velocity=2)
tracks[Bod].rest(W)
tracks[Bod].note("E4", W, velocity=2)
tracks[Bod].rest(H)
tracks[Bell].note("E6", W, velocity=2)
tracks[Bod].rest(W)
tracks[Bod].note("G4", W, velocity=1)
tracks[Bod].rest(W)
tracks[Bell].rest(W)

fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vimalakirtis-silence.mid")
mc.compose(fn, tracks, tempo=60)
print(f"wrote {fn} ({os.path.getsize(fn)} bytes, 60 bpm, silence at the center)")
