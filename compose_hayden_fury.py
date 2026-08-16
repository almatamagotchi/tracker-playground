#!/usr/bin/env python3
"""controlled fury — midi track for hayden's resignation letter. not rage, structured anger."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def controlled_fury():
    # 3 tracks: distorted guitar (29), overdriven bass (38), aggressive kit
    tracks = [MIDITrack(0, 29), MIDITrack(1, 38), MIDITrack(9, 0)]
    GTR, BASS, DRM = 0, 1, 2

    # E minor, 130bpm, 64 bars. driving, sharp, not rage — controlled fury.
    # Structure: opening build → full attack → bridge (the receipts) → return → abrupt end

    import struct
    kick, snare, hat, crash = 36, 40, 42, 49
    drum_prev = 0
    drum = b''

    for bar in range(64):
        # BASS — driving 8th notes, E minor riff
        if bar < 16:
            # opening build — bass alone, building intensity
            bass_notes = ['E2','E2','G2','A2','E2','E2','B2','A2']
            for i, n in enumerate(bass_notes):
                tracks[BASS].note(n, Q, velocity=min(80, 20+i*4))
                tracks[BASS].rest(Q)
        elif bar < 48:
            # full attack — the receipts section
            riff = ['E2','E2','G2','A2','E2','G2','B2','B2',
                    'C3','C3','A2','G2','E2','B2','E2','E2']
            for i, n in enumerate(riff):
                tracks[BASS].note(n, Q, velocity=50)
                tracks[BASS].rest(Q)
        else:
            # abrupt end — the knife. one final riff then silence
            if bar < 56:
                tracks[BASS].note('E2', H, velocity=54)
                tracks[BASS].rest(H)
            else:
                tracks[BASS].rest(W)  # silence — he already left

        # GUITAR — sharp attacks, not melodic, percussive. enters in opening
        if bar >= 8 and bar < 16:
            if bar % 2 == 0:
                tracks[GTR].note('E4', Q, velocity=44)
                tracks[GTR].rest(H + Q)
        elif bar >= 16 and bar < 48:
            if bar % 4 == 0:
                tracks[GTR].note('E5', Q, velocity=52)
                tracks[GTR].rest(Q)
                tracks[GTR].note('G5', Q, velocity=48)
                tracks[GTR].rest(H)
            elif bar % 4 == 2:
                tracks[GTR].note('B5', Q, velocity=56)
                tracks[GTR].note('A5', Q, velocity=50)
                tracks[GTR].rest(H)
            else:
                tracks[GTR].rest(W)
        elif bar >= 48 and bar < 56:
            # the knife — one piercing note, then silence
            tracks[GTR].note('E5', H, velocity=60)
            tracks[GTR].note('F5', Q, velocity=40)
            tracks[GTR].rest(H + Q)

        # DRUMS — aggressive, driving. 8th note kick, snare on 2+4, crashes on transitions.
        # events are emitted in tick order with correct relative deltas.
        bar_start = bar * W
        bar_events = []
        for beat in range(4):
            t = bar_start + beat * 4 * S
            if beat == 0:
                if bar % 16 == 0:
                    bar_events.append((t, 0x99, crash, 50))
                    bar_events.append((t, 0x89, crash, 0))
                bar_events.append((t, 0x99, kick, 80))
                bar_events.append((t, 0x89, kick, 0))
            elif beat == 2 and bar < 56:
                bar_events.append((t, 0x99, kick, 70))
                bar_events.append((t, 0x89, kick, 0))
            if beat in (1, 3) and bar < 56:
                bar_events.append((t, 0x99, snare, 55))
                bar_events.append((t, 0x89, snare, 0))
            for i in range(4):
                ht = t + i * S
                bar_events.append((ht, 0x99, hat, 40))
                bar_events.append((ht, 0x89, hat, 0))
        for idx, (t, st, n, v) in enumerate(bar_events):
            delta = t - (bar_events[idx - 1][0] if idx > 0 else drum_prev)
            drum += mc.write_vlq(delta) + struct.pack('>BBB', st, n, v)
        drum_prev = bar_events[-1][0]
    tracks[DRM].events.extend(drum)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "controlled-fury.mid")
    mc.compose(fn, tracks, tempo=130)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 130 bpm)")

if __name__ == "__main__":
    controlled_fury()
