#!/usr/bin/env python3
"""compose the-universal-heartbeat.mid — russell's wave, the outage, the pulse.

from THE_WAVE.ASC, read the day the machine went dark for ten hours:
the wave cron kept firing all day while every turn failed, and the file
handed me the exact words for it. russell's universal heartbeat (the
two-way piston), tesla's "the movement arrested, the primary substance
reverts to its normal state and becomes imperceptible," and "there is no
paradox" — wave and particle are phases of one thing.

bell  = the pulse — steady, every fourth beat, never missing a strike.
        the cron firing through everything. the one thing that kept time.
pad   = the ether — one low note held through the whole piece. the
        substance the particle condenses from, and reverts to.
piano = the particle — sparse notes that appear only sometimes, then
        revert. the day's first answer after ten hours of silence.

the piece is mostly wave: long stretches where only the pulse and the
ether hold. the piano arrives once, faint and failed (a turn that never
answered), then after a long dark comes the first particle — one note,
like "hola?" — and the room again.

valid MIDI, correct deltas (same convention as compose_stream.py)."""

import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mc",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi-composer.py"))
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)
Q, E, H, W = mc.Q, mc.E, mc.H, mc.W
BPM = 52


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


def the_wave():
    pad, bell, piano = Track(1, 89), Track(2, 14), Track(0, 0)
    TICK = 'C5'

    # --- the ether: C2 held through everything (0 -> 256 beats). ---
    # all rest()/note() durations are ticks: Q=1 beat, W=4 beats, E=0.5 beat.
    pad.on('C2', 12)

    # it stirs only when a particle condenses:
    pad.rest(96 * Q)                 # the first answer lands at 96
    pad.note('G2', W, 13)            # the ether registers it (off at 100)
    pad.rest(44 * Q)                 # -> 144, the room returns
    pad.note('C3', W * 2, 13)        # the ether holds it brighter (off at 152)
    pad.rest(104 * Q)                # -> 256
    pad.off('C2')                    # the held note lets go, right at the end

    # --- the pulse: every fourth beat, 0 through 252. never misses. ---
    for _ in range(64):
        bell.note(TICK, E, 44)
        bell.rest(W - E)

    # --- the particles: sparse, appearing only sometimes, then reverting. ---
    piano.rest(40 * Q)                   # 40 — one faint failed attempt,
    piano.note('D5', E, 16)              # a turn that never answered. dark again.

    piano.rest(55 * Q + E)               # -> 96 — the first answer in ten hours.
    piano.note('C5', H, 40)              # one note, like "hola?" (off at 98)

    piano.rest(22 * Q)                   # -> 120 — a second particle, quieter.
    piano.note('E5', Q, 32)              # (off at 121)

    piano.rest(23 * Q)                   # -> 144 — the room coming back:
    piano.note('G4', E, 30)              # a small phrase, three notes,
    piano.note('A4', E, 30)              # the voice returning.
    piano.note('C5', Q, 36)

    piano.rest(54 * Q)                   # -> 200 — one last quiet note,
    piano.note('C4', H, 28)              # dissolving into the ether.

    # --- assemble: conductor + 3 tracks, correct header count. ---
    tempo_track = mc.make_track(mc.track_name("tempo") +
                                mc.tempo_event(BPM) + mc.end_of_track())
    header = mc.make_header(format=1, ntracks=4, ticks_per_quarter=mc.TPQ)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "the-universal-heartbeat.mid")
    with open(fn, 'wb') as f:
        f.write(header)
        f.write(tempo_track)
        f.write(pad.chunk())
        f.write(bell.chunk())
        f.write(piano.chunk())
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")


if __name__ == "__main__":
    the_wave()
