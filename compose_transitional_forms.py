#!/usr/bin/env python3
"""compose transitional-forms.mid — the fault line and the missing link.

from kathleen hunt's transitional fossils FAQ (talk.origins, 1993), read the
night the fault lines layer went live. pilbeam: "as soon as you find a
missing link, you've just created two more missing links."

cello = the strata — one low note held through everything. the continuous
        layer underneath, the ground the record is written in.
piano = the fault — the same phrase stated complete, then broken by a gap,
        then resumed slightly changed, then broken again. each time the
        phrase shrinks and the gap shrinks: every found link makes two more.
bell  = the fossil — sparse preserved notes, feathers-and-teeth. they borrow
        the strata's pitches in the high register and the phrase's pitches
        near the low, and never land on the phrase's grid or the downbeats.
        they never quite fit either side. that is the point.

the piece never fills its gaps all the way: every completed phrase is
followed by a smaller gap, down to a single faint note — the newest found
link — and then the strata holds alone, as it always has.

valid MIDI, correct deltas (same convention as compose_stream.py /
compose_universal_heartbeat.py)."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
Q, E, H, W = mc.Q, mc.E, mc.H, mc.W
BPM = 58


class Track:
    """MIDI track with correct delta handling: rest() accumulates into the
    start_delta of the next note instead of emitting an orphaned vlq."""

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


def transitional_forms():
    cello, piano, bell = Track(1, 42), Track(0, 0), Track(2, 14)

    # --- the strata: C2 held through everything (0 -> 256 beats). ---
    cello.on('C2', 14)
    cello.rest(256 * Q)
    cello.off('C2')

    # --- the fault: the phrase, broken smaller each time. ---
    # statement 1 — complete (0 -> 4)
    piano.note('C4', E, 40)
    piano.note('E4', E, 40)
    piano.note('G4', E, 40)
    piano.note('C5', E, 40)
    piano.note('G4', H, 38)
    # gap (4 -> 12)
    piano.rest(8 * Q)
    # statement 2 — broken by the fault (12 -> 23)
    piano.note('C4', E, 36)
    piano.note('E4', E, 36)              # the fault slips here
    piano.rest(7 * Q)                    # the gap the break created
    piano.note('G4', E, 34)              # resumed, slightly changed
    piano.note('C5', E, 34)
    piano.note('C5', H, 32)
    # fragment 3 — smaller (30 -> 33)
    piano.rest(7 * Q)
    piano.note('E4', E, 30)
    piano.note('G4', E, 30)
    piano.note('C5', H, 28)
    # fragment 4 — smaller still (37.5 -> 40)
    piano.rest(4 * Q + E)
    piano.note('G4', E, 26)
    piano.note('C5', H, 24)
    # fragment 5 — one note (42 -> 44)
    piano.rest(2 * Q)
    piano.note('C5', H, 22)
    # the newest found link — faint (48 -> 50)
    piano.rest(4 * Q)
    piano.note('C5', H, 16)

    # --- the fossils: sparse, cross-wired, never on the grid. ---
    # beats 5.5, 15.5, 27.25, 33.75, 44.5, 51.75, 58
    bell.rest(int(5.5 * Q))              # 5.5 — strata's fifth, raised
    bell.note('G4', E, 32)
    bell.rest(10 * Q)                    # 15.5 — the phrase's pitch, high
    bell.note('E5', E, 30)
    bell.rest(int(11.75 * Q))            # 27.25 — the strata itself, low
    bell.note('C3', E, 34)
    bell.rest(int(6.5 * Q))              # 33.75 — the phrase's fifth, high
    bell.note('G5', E, 28)
    bell.rest(int(10.75 * Q))            # 44.5 — strata-ish, low
    bell.note('E3', E, 32)
    bell.rest(int(7.25 * Q))             # 51.75 — the phrase again, high
    bell.note('E5', E, 26)
    bell.rest(int(6.25 * Q))             # 58 — the last fossil, settling
    bell.note('C3', Q, 30)

    # --- assemble: conductor + 3 tracks. ---
    tempo_track = mc.make_track(mc.track_name("tempo") +
                                mc.tempo_event(BPM) + mc.end_of_track())
    header = mc.make_header(format=1, ntracks=4, ticks_per_quarter=mc.TPQ)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "transitional-forms.mid")
    with open(fn, 'wb') as f:
        f.write(header)
        f.write(tempo_track)
        f.write(cello.chunk())
        f.write(piano.chunk())
        f.write(bell.chunk())
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")


if __name__ == "__main__":
    transitional_forms()
