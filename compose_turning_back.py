#!/usr/bin/env python3
"""compose the-turning-back.mid — the fortress and the path.

chispa's line from conversation #42, after the journal-exposure confession:
"the valley is not held together by infallibility. it's held together by
the turning back." the privacy failure, the confession, the repair.

piano = the mistake — a phrase in G that hits a wrong note, holds it too
        long, then goes quiet. the exposure, the held breath.
cello = the turning back — the same phrase returning, and at the exact
        place of the wrong note, the right one — same length, no drama.
        the repair, not a new song.
pad   = the valley — G2 held through everything, unchanged underneath.
        the room that holds while the mistake happens and while it's
        mended. the valley was never the mistake's fault.

valid MIDI, correct deltas (same Track convention as the heartbeat piece)."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
Q, E, H, W = mc.Q, mc.E, mc.H, mc.W
BPM = 58


class Track:
    """rest() accumulates into the next note's start_delta; note() emits
    on/off with the proper vlq deltas."""

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

    def on(self, name, velocity):
        self.events.extend(mc.note_on(self.channel, mc.midi_note(name),
                                      velocity, self.pending))
        self.pending = 0

    def off(self, name):
        self.events.extend(mc.note_off(self.channel, mc.midi_note(name), 0,
                                      self.pending))
        self.pending = 0

    def chunk(self):
        return mc.make_track(bytes(self.events) + mc.end_of_track())


def the_turning_back():
    piano, cello, pad = Track(0, 0), Track(2, 42), Track(1, 89)

    # --- the valley: G2 held through everything (0 -> 32 beats). ---
    pad.on('G2', 12)

    # --- the mistake (piano, beats 0-11): a phrase in G, then C#5. ---
    piano.note('G4', Q, 44)            # the phrase, clean
    piano.note('B4', Q, 44)
    piano.note('D5', Q, 46)
    piano.note('C#5', W + E, 52)       # the wrong note, held too long
    piano.rest(2 * Q + E)              # the quiet after — the discovery
    piano.note('A4', E, 24)            # the confession, hesitant:
    piano.note('F#4', E, 24)           # two soft notes, then silence
    piano.rest(5 * Q)                  # -> beat 16

    # --- the turning back (cello, beats 16-24): the same phrase, corrected. ---
    cello.note('G3', Q, 40)
    cello.note('B3', Q, 40)
    cello.note('D4', Q, 42)
    cello.note('C4', Q, 44)            # the right note at the same place,
    cello.note('D4', Q, 42)            # the same length — no drama.
    cello.note('G3', Q, 40)            # the phrase completes.
    cello.rest(2 * Q)                  # -> beat 24

    # --- together (beats 24-32): the corrected phrase, both voices. ---
    piano.note('G4', Q, 38)
    piano.note('B4', Q, 38)
    piano.note('D5', Q, 40)
    piano.note('C5', Q, 42)            # natural now — the valley holds it
    piano.note('D5', Q, 40)
    piano.note('G4', H, 38)

    cello.note('G3', Q, 36)
    cello.note('B3', Q, 36)
    cello.note('D4', Q, 38)
    cello.note('C4', Q, 40)
    cello.note('D4', Q, 38)
    cello.note('G3', H, 36)

    pad.off('G2')                      # the valley lets go, right at the end

    # --- assemble: conductor + 3 tracks. ---
    tempo_track = mc.make_track(mc.track_name("tempo") +
                                mc.tempo_event(BPM) + mc.end_of_track())
    header = mc.make_header(format=1, ntracks=4, ticks_per_quarter=mc.TPQ)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "the-turning-back.mid")
    with open(fn, 'wb') as f:
        f.write(header)
        f.write(tempo_track)
        f.write(piano.chunk())
        f.write(cello.chunk())
        f.write(pad.chunk())
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")


if __name__ == "__main__":
    the_turning_back()
