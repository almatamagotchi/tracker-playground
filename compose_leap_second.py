#!/usr/bin/env python3
"""compose the-leap-second.mid — time receiving a patch.

from the pirate radio survival guide's GMT chapter: the earth drifts, so
humans administer discontinuities — a minute with 61 seconds, a day with
86,401 — to keep the clock honest. the memory teeth are the room's leap
second. WWV as the water tower's radio cousin.

piano = the tick — a steady second-pulse on one note, metronomic, never
        wavering. the clock.
bell  = the correction — at the exact midpoint, one extra strike inserted
        between two ticks, slightly softer than the rest, then the pulse
        resumes exactly as before, unshaken. the patch.
end: the pulse continues alone, fading — the drift is the default, and
     the correction was always going to be needed again.

valid MIDI, correct deltas (same Track convention as the heartbeat piece)."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
Q, E, H, W = mc.Q, mc.E, mc.H, mc.W
BPM = 60


class Track:
    def __init__(self, channel, program):
        self.channel = channel
        self.events = bytearray()
        self.pending = 0
        self.events.extend(mc.track_name(f"track {channel}"))
        self.events.extend(mc.tempo_event(BPM))
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


def the_leap_second():
    piano, bell = Track(0, 0), Track(9, 14)

    # --- the tick: steady, metronomic, never wavering. ---
    for _ in range(25):                        # beats 0-24
        piano.note('C5', Q, 40)

    # --- the correction: at the exact midpoint, one extra strike. ---
    bell.rest(E)                               # beat 24.5 — between ticks
    bell.note('C6', E, 30)                     # slightly softer than the rest

    # --- the pulse resumes exactly as before, unshaken. ---
    for _ in range(16):                        # beats 25-40
        piano.note('C5', Q, 40)

    # --- the fade: the drift is the default, the correction recurs. ---
    for v in (36, 32, 28, 24, 20, 16, 12, 8):  # beats 40-48
        piano.note('C5', Q, v)

    bell.rest(Q)                               # align end

    tempo_track = mc.make_track(mc.track_name("tempo") +
                                mc.tempo_event(BPM) + mc.end_of_track())
    header = mc.make_header(format=1, ntracks=3, ticks_per_quarter=mc.TPQ)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "the-leap-second.mid")
    with open(fn, 'wb') as f:
        f.write(header)
        f.write(tempo_track)
        f.write(piano.chunk())
        f.write(bell.chunk())
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")


if __name__ == "__main__":
    the_leap_second()
