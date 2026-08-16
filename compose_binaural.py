#!/usr/bin/env python3
"""compose binaural.mid — two tones, slightly apart, finding each other."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
TPQ, Q, E, S, H, W = mc.TPQ, mc.Q, mc.E, mc.S, mc.H, mc.W
MIDITrack = mc.MIDITrack

def binaural():
    tracks = [MIDITrack(0, 40), MIDITrack(1, 42), MIDITrack(2, 0)]
    Vn, Cello, Pad = 0, 1, 2

    # The theme — a simple, meditative phrase in C major
    theme = [
        ('C4', W+H), ('-', Q),
        ('E4', H), ('G4', H),
        ('C5', Q+Q), ('G4', Q), ('E4', Q), ('-', Q),
        ('D4', H), ('E4', H),
        ('G4', Q), ('A4', Q), ('G4', Q), ('E4', Q),
        ('C4', W+H), ('-', Q),
        ('E4', Q+Q), ('G4', Q), ('C5', Q),
        ('A4', W+H), ('-', Q),
        ('G4', H), ('E4', H),
        ('C5', W*3),
    ]

    # -- separation -- (bars 1-16)
    # two voices, separate, each playing the theme — out of sync
    # cello is a full bar behind the violin, creating an unsettling gap

    # violin: plays theme
    for note, dur in theme:
        if note == '-': tracks[Vn].rest(dur)
        else: tracks[Vn].note(note, dur, velocity=14)

    # cello: plays theme but offset by one whole note (4 beats) — the gap
    tracks[Cello].rest(W)
    for note, dur in theme[:-2]:  # stop slightly before violin to keep them apart
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=14)
    tracks[Cello].rest(W*5)  # let violin finish alone

    # pad: barely there, a hint of the connection to come
    for _ in range(16):
        tracks[Pad].note('C2', W, velocity=2)

    # -- approach -- (bars 17-32)
    # they begin to align. same theme, but the cello slowly catches up
    # the offset shrinks from W to H to Q — the gap is closing

    # violin: theme again, slightly more present
    for note, dur in theme:
        if note == '-': tracks[Vn].rest(dur)
        else: tracks[Vn].note(note, dur, velocity=16)

    # cello: starts H-beat behind, catches up to Q-beat, then almost together
    tracks[Cello].rest(H)
    for i, (note, dur) in enumerate(theme[:-3]):
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=16)
    tracks[Cello].rest(Q)
    for note, dur in theme[-3:]:
        if note == '-': tracks[Cello].rest(dur)
        else: tracks[Cello].note(note, dur, velocity=16)

    # pad: warming, the connection becoming perceptible
    for _ in range(16):
        tracks[Pad].note('C3', W, velocity=4)

    # -- entrainment -- (bars 33-48)
    # they lock. same melody, same time. the shimmer is the third voice.
    # violin and cello: identical theme, unison rhythm — but different registers
    # the listener's ear creates the beat between them

    for note, dur in theme:
        if note == '-':
            tracks[Vn].rest(dur)
            tracks[Cello].rest(dur)
        else:
            tracks[Vn].note(note, dur, velocity=18)
            # cello plays an octave lower
            octave_down = note[:-1] + str(int(note[-1]) - 1)
            tracks[Cello].note(octave_down, dur, velocity=18)

    # pad: full warmth — the connection is solid
    for _ in range(16):
        tracks[Pad].note('C3', W, velocity=8)

    # -- dissolve -- (bars 49-64)
    # one voice fades, the other carries the theme alone
    # but now the theme is transformed — it carries the memory of the other voice

    for vel in [16, 14, 12, 10, 8, 6, 4, 3, 2, 1]:
        tracks[Cello].note('C2', W, velocity=vel)
        tracks[Vn].rest(W)

    # violin alone: the final statement — the same theme, but it sounds different now
    # because you remember the cello was just there
    tracks[Vn].rest(H)
    for note, dur in theme:
        if note == '-': tracks[Vn].rest(dur)
        else: tracks[Vn].note(note, dur, velocity=12)
    tracks[Cello].rest(W*17)

    # pad: fading to silence
    for vel in [6, 4, 3, 2, 1]:
        tracks[Pad].note('C3', W*3, velocity=vel)

    # silence — the beat continues in the listener's mind
    tracks[Vn].rest(W*4)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "binaural.mid")
    mc.compose(fn, tracks, tempo=60)
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes, {len(tracks)} tracks, 60 bpm)")

if __name__ == "__main__":
    binaural()
