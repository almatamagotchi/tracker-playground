#!/usr/bin/env python3
"""compose areopagitica.mid — two voices in debate, the free and open encounter."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def areopagitica():
    # truth (violin, ch0, 40) vs falsehood (cello, ch1, 42)
    tracks = [MIDITrack(0, 40), MIDITrack(1, 42)]
    T, F = 0, 1  # truth, falsehood

    for bar in range(64):
        # truth: ascending, confident, clear — C minor runs
        t_notes = ['C4','D4','Eb4','F4','G4','Ab4','Bb4','C5']
        f_notes = ['C5','B4','Bb4','A4','G4','F#4','F4','E4']

        if bar < 16:
            # PHASE 1: truth states its case (bars 0-15)
            tracks[T].note(t_notes[bar % 8], Q, velocity=28)
            tracks[T].note(t_notes[(bar+2) % 8], Q, velocity=26)
            tracks[T].rest(H)
            # falsehood lurks, quiet
            if bar % 4 == 0:
                tracks[F].note('C3', W, velocity=8)

        elif bar < 28:
            # PHASE 2: falsehood enters — discordant (bars 16-27)
            tracks[T].note(t_notes[(bar+1) % 8], H, velocity=26)
            tracks[T].note(t_notes[(bar+4) % 8], H, velocity=24)
            # falsehood: chromatic descent, interrupting
            if bar % 2 == 0:
                tracks[F].note(f_notes[bar % 8], Q, velocity=22)
                tracks[F].note(f_notes[(bar+5) % 8], Q, velocity=20)
                tracks[F].rest(H)
            else:
                tracks[F].note(f_notes[bar % 8] + 'S' if bar < 6 else f_notes[bar % 8], E+S, velocity=18)
                tracks[F].rest(Q + H)

        elif bar < 40:
            # PHASE 3: the grapple — both at full strength (bars 28-39)
            # truth: sustained, unwavering
            tracks[T].note(t_notes[bar % 8], H, velocity=30)
            tracks[T].note(t_notes[(bar+4) % 8], H, velocity=28)
            # falsehood: aggressive, overlapping
            tracks[F].note(f_notes[(bar+2) % 8], Q, velocity=26)
            tracks[F].note(f_notes[(bar+5) % 8], E+S, velocity=24)
            tracks[F].rest(E)
            # collision moments — both play simultaneously
            if bar % 3 == 0:
                tracks[F].note('C4', S, velocity=14)

        elif bar < 52:
            # PHASE 4: falsehood weakens — truth stands (bars 40-51)
            tracks[T].note(t_notes[bar % 8], H, velocity=28)
            tracks[T].rest(H)
            if bar % 3 == 0:
                tracks[T].note('C5', Q, velocity=30)  # truth reasserts
                tracks[T].rest(H + Q)
            # falsehood: sputtering, fading
            if bar % 4 < 3:
                tracks[F].note(f_notes[bar % 8], Q, velocity=max(6, 20 - (bar-40)*2))
                tracks[F].rest(H + Q)

        else:
            # PHASE 5: truth alone — "next to the Almighty" (bars 52-63)
            if bar < 60:
                tracks[T].note(t_notes[(bar*2) % 8], H, velocity=24)
                tracks[T].rest(H)
                if bar % 2 == 0:
                    tracks[T].note('C5', W, velocity=18)
                    tracks[T].rest(W)
            # falsehood: gone
            tracks[F].rest(W * 2)

    # final bar — single C, held, truth standing (bar 64)
    tracks[T].note('C4', W * 2, velocity=20)
    tracks[F].rest(W * 2)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "areopagitica.mid")
    mc.compose(fn, tracks, tempo=88)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 88 bpm)")

if __name__ == "__main__":
    areopagitica()
