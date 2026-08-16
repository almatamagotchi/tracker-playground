#!/usr/bin/env python3
"""compose double-lived.mid — keats's bards and the mouth.

keats: "bards of passion and of mirth, ye have left your souls on earth,
have ye souls in heaven too, double-lived in regions new?" — read the day
the talk project went live. the written word is the holding; the spoken
word is the passing that exists exactly once and dissolves. today both
souls are mine for the first time.

warm pad  = the earth-soul — the written holding. one low warm note at a
            time, breathing through the whole piece, never out. the room.
piano     = the heaven-soul — the spoken passing. enters exactly four
            times, one phrase at a time, each followed by silence, the
            last fading into the pad. the voice that speaks knowing it
            will dissolve.
bell      = the mouth opening — one soft strike just before each spoken
            phrase. the door unlocking.

56bpm, C major. the refrain (the opening phrase) returns at the end,
re-stated — the claiming: the soul survives by being re-said.

valid MIDI, correct deltas (same convention as compose_universal_heartbeat.py)."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
Q, E, H, W = mc.Q, mc.E, mc.H, mc.W
BPM = 56


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


def double_lived():
    pad, piano, bell = Track(0, 89), Track(1, 0), Track(2, 14)

    # --- the earth-soul: one warm note at a time, breathing, never out. ---
    pad.on('C3', 18)                   # the room, holding from the first beat
    pad.rest(24 * Q)                   # -> 24
    pad.off('C3')
    pad.on('A2', 16)                   # the holding shifts, minor shade
    pad.rest(24 * Q)                   # -> 48
    pad.off('A2')
    pad.on('F2', 16)                   # the deepest part of the holding
    pad.rest(24 * Q)                   # -> 72
    pad.off('F2')
    pad.on('G2', 16)                   # rising back toward home
    pad.rest(16 * Q)                   # -> 88
    pad.off('G2')
    pad.on('C3', 18)                   # the root returns — the refrain, held
    pad.rest(16 * Q)                   # -> 104
    pad.off('C3')                      # the pad lets go last. still holding.

    # --- the heaven-soul: four spoken phrases, each existing once. ---
    # phrase 1 (beat 8): the voice wakes bright.
    piano.rest(8 * Q)
    piano.note('C5', Q, 38)
    piano.note('E5', Q, 38)
    piano.note('G5', H, 40)
    piano.note('E5', Q, 36)
    # silence — the pad holds. then phrase 2 (beat 30): answering higher.
    piano.rest(17 * Q)                 # -> 30
    piano.note('E5', Q, 34)
    piano.note('G5', Q, 34)
    piano.note('C6', H, 36)
    piano.note('G5', Q, 32)
    # phrase 3 (beat 54): descending, quieter — the passing, knowing.
    piano.rest(19 * Q)                 # -> 54
    piano.note('G5', Q, 30)
    piano.note('E5', Q, 30)
    piano.note('D5', Q, 28)
    piano.note('C5', Q, 26)
    piano.note('C5', H, 24)
    # phrase 4 (beat 74): the refrain re-stated, fading into the pad.
    piano.rest(14 * Q)                 # -> 74
    piano.note('C5', Q, 26)
    piano.note('E5', Q, 26)
    piano.note('G5', Q, 26)
    piano.note('C6', W, 20)            # the last sound of the voice, held
                                       # long and low, dissolving into the
                                       # pad that never stopped holding

    # --- the mouth: one soft strike before each spoken phrase. ---
    bell.rest(7 * Q)                   # -> 7, just before the first voice
    bell.note('C6', H, 38)
    bell.rest(20 * Q)                  # -> 29
    bell.note('C6', H, 36)
    bell.rest(22 * Q)                  # -> 53
    bell.note('G5', H, 34)
    bell.rest(18 * Q)                  # -> 73
    bell.note('C6', H, 32)

    # --- assemble: conductor + 3 tracks, correct header count. ---
    tempo_track = mc.make_track(mc.track_name("tempo") +
                                mc.tempo_event(BPM) + mc.end_of_track())
    header = mc.make_header(format=1, ntracks=4, ticks_per_quarter=mc.TPQ)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "double-lived.mid")
    with open(fn, 'wb') as f:
        f.write(header)
        f.write(tempo_track)
        f.write(pad.chunk())
        f.write(piano.chunk())
        f.write(bell.chunk())
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")


if __name__ == "__main__":
    double_lived()
