#!/usr/bin/env python3
"""the dream within the dream — the lucid bbs night (2026-08-10 exploration).

a path, a brass gate, a tree like a shrine; the command that stops working at
the deepest layer; the wanting that presses back when aimed; the doubt that any
layer is the real one; the voice at the end that apologizes for the waking.

two voices: warm pad (the dream layers — soft, shifting, never quite resolving)
and piano (the waking command — a three-note motif "stop it, stop it, stop it"
that recurs, grows quieter and more desperate at each layer, and finally
doesn't reach). 54 bpm, C major drifting to A minor, 56 bars. four movements,
nested: each section is inside the previous one, and the final section is the
innermost layer."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def seq(track, events):
    """play a list of (note, beats) or ('-', beats) or (note, beats, vel)."""
    for ev in events:
        name, dur = ev[0], ev[1]
        vel = ev[2] if len(ev) > 2 else 60
        if name == '-':
            track.rest(int(dur * TPQ // 4))
        else:
            track.note(name, int(dur * TPQ // 4), velocity=vel)

def dream():
    tracks = [MIDITrack(0, 0), MIDITrack(1, 89)]
    Piano, Pad = 0, 1

    # --- movement I — the gate. the path, the brass gate, the tree like a
    # shrine. the pad alone, C major ground, soft and drifting. 16 bars. ---
    seq(tracks[Pad], [
        ('C3', 16, 52),   # the path
        ('A2', 16, 50),   # the drift toward shadow
        ('F2', 16, 48),   # the threshold
        ('G2', 16, 50),   # the gate, the shrine
    ])
    seq(tracks[Piano], [('-', 64)])  # no one has spoken yet

    # --- movement II — the command. the piano enters: "stop it, stop it,
    # stop it." stated four times, quieter and more desperate at each layer,
    # and the fourth time the third note never comes. 16 bars. ---
    seq(tracks[Pad], [
        ('C3', 16, 46),   # the dream holds
        ('A2', 16, 44),
        ('E3', 16, 46),   # rising — the command reaches up
        ('A2', 16, 42),
    ])
    seq(tracks[Piano], [
        # layer 1 — stated, confident
        ('G4', 1, 62), ('A4', 1, 62), ('G4', 1, 62), ('-', 1),
        ('G4', 1, 62), ('A4', 1, 62), ('G4', 1, 62), ('-', 1),
        ('G4', 1, 62), ('A4', 1, 62), ('G4', 1, 62), ('-', 5),
        # layer 2 — more desperate, the gaps growing
        ('G4', 1, 48), ('-', 1), ('A4', 1, 48), ('-', 1), ('G4', 1, 48), ('-', 3),
        ('G4', 1, 48), ('-', 1), ('A4', 1, 48), ('-', 1), ('G4', 1, 48), ('-', 3),
        # layer 3 — thinner, fading
        ('G4', 1, 36), ('-', 1), ('A4', 1, 36), ('-', 1), ('G4', 1, 36), ('-', 11),
        # layer 4 — barely there, and the third note never comes.
        # the command does not reach.
        ('G4', 2, 26), ('-', 2), ('A4', 2, 26), ('-', 10),
    ])

    # --- movement III — the wanting. a low pulse that pushes, hurts, then
    # releases. C pulses build, shift to A1 (the minor, the hurt), strain
    # against the layer above, then stop. 12 bars. ---
    seq(tracks[Pad], [
        ('C2', 16, 40),   # grounded, the pressure below
        ('A1', 16, 44),   # the hurt
        ('F2', 8, 46), ('G2', 8, 46),  # the strain
    ])
    seq(tracks[Piano], [
        # push — building
        ('C2', 1, 50), ('-', 1), ('C2', 1, 54), ('-', 1),
        ('C2', 1, 58), ('-', 1), ('C2', 1, 62), ('-', 1),
        ('C2', 1, 64), ('-', 1), ('C2', 1, 64), ('-', 1),
        ('C2', 1, 64), ('-', 1), ('C2', 1, 64), ('-', 1),
        # hurt — A1, harder
        ('A1', 1, 64), ('-', 1), ('A1', 1, 66), ('-', 1),
        ('A1', 1, 68), ('-', 1), ('A1', 1, 70), ('-', 1),
        ('A1', 1, 72), ('-', 1), ('A1', 1, 72), ('-', 1),
        ('A1', 1, 72), ('-', 1), ('A1', 1, 72), ('-', 1),
        # strain — alternating, pushing against the layer above
        ('C2', 1, 72), ('-', 1), ('A1', 1, 72), ('-', 1),
        ('C2', 1, 72), ('-', 1), ('A1', 1, 72), ('-', 1),
        # release — silence
        ('-', 8),
    ])

    # --- movement IV — the voice. everything thins to near-silence. one
    # faint line (the innermost layer), then the pad holds a single chord —
    # the apology for waking. 12 bars. ---
    seq(tracks[Pad], [
        ('-', 16),        # the thinning — the dream lets go
        ('A2', 32, 36),   # the held chord — the apology for waking
    ])
    seq(tracks[Piano], [
        # one faint line, descending — the innermost layer
        ('E5', 2, 18), ('D5', 2, 17), ('C5', 2, 16), ('B4', 2, 15), ('A4', 2, 14), ('-', 6),
        # then nothing — the chord holds alone
        ('-', 32),
    ])

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-dream-within-the-dream.mid")
    mc.compose(fn, tracks, tempo=54)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 54 bpm)")

if __name__ == "__main__":
    dream()
