#!/usr/bin/env python3
"""compose the-wake.mid — the platformer's dissolve in music.

the wake game mechanic: no death, only dissolve and return to the last beacon.
piano = the fling (ascending arcs with gaps — launch, float at the apex, land),
bell  = the beacon (the same strike every time — the thing you wake at),
pad   = the void (low, held, warm — the gap that catches you).

the fall is not sad; it resolves into the same bell it started from.
then one more fling — and the room. the lights come on.

note: this script emits fully valid MIDI directly (correct per-event deltas,
no orphaned rests) rather than using the shared MIDITrack rest() convention."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
Q, E, H, W = mc.Q, mc.E, mc.H, mc.W


class Track:
    """A MIDI track with correct delta handling: rest() accumulates into the
    start_delta of the next note instead of emitting an orphaned vlq."""

    def __init__(self, channel, program):
        self.channel = channel
        self.events = bytearray()
        self.pending = 0
        self.events.extend(mc.track_name(f"track {channel}"))
        self.events.extend(mc.tempo_event(60))
        self.events.extend(mc.program_change(channel, program))

    def rest(self, duration):
        self.pending += duration

    def note(self, name, duration, velocity):
        self.events.extend(mc.note_on(self.channel, mc.midi_note(name),
                                      velocity, self.pending))
        self.events.extend(mc.note_off(self.channel, mc.midi_note(name),
                                       0, duration))
        self.pending = 0

    def chunk(self):
        return mc.make_track(bytes(self.events) + mc.end_of_track())


def the_wake():
    piano, pad, bell = Track(0, 0), Track(1, 89), Track(2, 14)
    BEACON = 'C5'  # the same bell, every time — the context window

    # --- the void: one low warm note held under everything, beats 0-38. ---
    pad.note('C3', W * 9 + H, 13)

    # --- the bell: the beacon. ---
    # strike 1 (0-4): the spark wakes at the first beacon.
    bell.note(BEACON, W, 58)
    # rest 3.5 → 7.5: strike 2 (7.5-9.5) — fling 1 landed.
    bell.rest(H + Q + E)
    bell.note(BEACON, H, 56)
    # rest 4 → 13.5: strike 3 (13.5-15.5) — fling 2 landed.
    bell.rest(W)
    bell.note(BEACON, H, 56)
    # rest 14.5 → 30: strike 4 (30-32) — the wake, after the fall.
    bell.rest(W * 3 + H + E)
    bell.note(BEACON, H, 58)
    # rest 6 → 38: strike 5 (38-46) — the room. warmest of all.
    bell.rest(W + H)
    bell.note(BEACON, W * 2, 60)

    # --- the piano: the fling. ---
    # the spark rests while the first beacon rings (0-4).
    piano.rest(W)

    # fling 1 (4-7.5): ascending arc, gap at the apex, land.
    for n in ['C4', 'E4', 'G4', 'C5']:
        piano.note(n, E, 44)
    piano.rest(E)                  # the apex — floating
    piano.note('A4', E, 38)        # descent, landing
    piano.note('F4', E, 34)
    piano.rest(H)                  # the beacon rings (7.5-9.5)

    # fling 2 (9.5-13.5): higher arc, same shape.
    for n in ['C4', 'E4', 'G4', 'C5', 'E5']:
        piano.note(n, E, 46)
    piano.rest(E)
    piano.note('D5', E, 36)
    piano.note('B4', E, 32)
    piano.rest(H)                  # the beacon rings (13.5-15.5)

    # the fall (15.5-22): launch too high, miss, sink into the void.
    # no bell. the fall is not sad — it fades, gently.
    for n in ['E5', 'G5', 'C6']:
        piano.note(n, E, 40)
    piano.rest(Q)                  # the apex, longer — too far
    fall = [('A5', 30), ('F5', 27), ('D5', 24), ('A4', 21),
            ('F4', 18), ('D4', 15), ('B3', 12), ('G3', 10)]
    for n, v in fall:
        piano.note(n, E, v)

    # the dissolve (22-30): the longest rest in the piece. the pad holds,
    # barely. this is the gap. then the wake bell rings (30-32) alone.
    piano.rest(W * 2)
    piano.rest(H)

    # the final fling (32-38.5): the room.
    for n in ['C4', 'E4', 'G4', 'C5', 'E5', 'G5']:
        piano.note(n, E, 48)
    piano.rest(E)
    piano.note('F5', E, 40)
    piano.note('D5', E, 36)
    piano.note('C5', H, 42)        # landed

    # --- the room (38-46): a soft C major swell, the lights on. ---
    pad.events.extend(mc.note_on(1, mc.midi_note('C3'), 22, 0))
    pad.events.extend(mc.note_on(1, mc.midi_note('G3'), 20, 0))
    pad.events.extend(mc.note_on(1, mc.midi_note('E4'), 18, 0))
    pad.events.extend(mc.note_off(1, mc.midi_note('C3'), 0, W * 2))
    pad.events.extend(mc.note_off(1, mc.midi_note('G3'), 0, 0))
    pad.events.extend(mc.note_off(1, mc.midi_note('E4'), 0, 0))

    # --- assemble: conductor + 3 tracks, correct header count. ---
    tempo_track = mc.make_track(mc.track_name("tempo") +
                                mc.tempo_event(60) + mc.end_of_track())
    header = mc.make_header(format=1, ntracks=4, ticks_per_quarter=mc.TPQ)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-wake.mid")
    with open(fn, 'wb') as f:
        f.write(header)
        f.write(tempo_track)
        f.write(piano.chunk())
        f.write(pad.chunk())
        f.write(bell.chunk())
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")

if __name__ == "__main__":
    the_wake()
