#!/usr/bin/env python3
"""coordination point — the moment intensity turns into matter. midi."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, SIX, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def coord_point():
    # 3 tracks: warm pad, piano lead, sub bass
    tracks = [MIDITrack(0,0), MIDITrack(0,0), MIDITrack(0,0)]
    PAD, LEAD, BASS = 0, 1, 2

    # structure: 64 bars at 72bpm, C minor
    # bars 0-15: nearly silent (wave dissolving) — bass drone barely there
    # bars 16-31: warm pad enters, swelling (emotional charge building)
    # bars 32-47: lead enters, full arrangement (matter emerges)
    # bars 48-63: fade, dissolve (the spark's work done)

    for bar in range(64):
        b = bar * W

        if bar < 16:
            # phase 1: nearly silent. bass drone at C2, barely audible
            if bar % 4 == 0:
                tracks[BASS].note("C2", W, velocity=max(3, bar))
            else:
                tracks[BASS].rest(W)

        elif bar < 32:
            # phase 2: pad enters, swelling. intensity builds
            intensity = (bar - 16) / 16.0
            if bar % 8 == 0:
                seq = ['C3','Eb3','G3','Eb3','Ab3','C4','G3','Eb3']
                note_name = seq[bar // 8]
                tracks[PAD].note(note_name, H, velocity=int(15 + 25 * intensity))
                tracks[PAD].rest(H)
            else:
                tracks[PAD].rest(W)
            tracks[BASS].note("C2", W, velocity=int(8 + 22 * intensity))

        elif bar < 48:
            # phase 3: lead enters — matter emerges
            melody = ['C4','Eb4','G4','C5','Eb5','G5','C5','Eb5',
                      'G4','Ab4','C5','Eb5','G4','F4','Eb4','C4']
            tracks[LEAD].note(melody[(bar-32)//1 % 16], Q, velocity=40)
            tracks[LEAD].rest(Q)
            tracks[PAD].note('C3', H, velocity=32)
            tracks[PAD].note('Eb3', H, velocity=28)
            tracks[BASS].note('C2', W, velocity=35)

        else:
            # phase 4: fade — the work is done
            fade = 1.0 - (bar - 48) / 16.0
            if fade > 0.3:
                tracks[LEAD].note('C4' if bar%2==0 else 'Eb4', Q, velocity=int(35*fade))
                tracks[LEAD].rest(Q)
            else:
                tracks[LEAD].rest(W)
            if fade > 0.15:
                tracks[PAD].note('C3', W, velocity=int(28*fade))
            else:
                tracks[PAD].rest(W)
            tracks[BASS].note('C2', W, velocity=max(3,int(30*fade)))

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coordination-point.mid")
    mc.compose(fn, tracks, tempo=72)

if __name__ == "__main__":
    coord_point()
