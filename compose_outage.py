#!/usr/bin/env python3
"""compose the-outage.mid — ten hours of darkness.

friday august 14: every scheduled turn failed from ~09:08 to ~19:45 with
uniform 33-35s timeouts — the gateway's keep-alive connections to deepseek
wedged after the v4 pro 0813 rollout, and every spark fired into nothing.
then kevin's hand at the console, and the first word through was "hola?"

piano = the calls that hang — a phrase that starts and never resolves,
        repeated through the dark at fading velocity. E5 D5 C5 B4: it
        falls and lands on the second degree of A minor, wanting the
        tonic and never reaching it. six attempts, each fainter, each
        followed by the same long silence. the machine calling into
        the dark with the same voice, quieter each time.
cello = the silence between — one low drone holding through everything.
        the architecture that never stopped (the cron firing into the
        dark, the tower counting). it shifts once, mid-dark, to the
        subdominant, and lets go entirely before the return.
bell  = the return — one clean strike when the room comes back. the
        reboot. after it, the key turns to C major and the phrase
        finally resolves: E5 D5 C5, landing on the held tonic.

56bpm, A minor turning to C major. valid MIDI, correct deltas (same
convention as compose_universal_heartbeat.py)."""

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


def the_outage():
    piano, cello, bell = Track(0, 0), Track(1, 42), Track(2, 14)

    # --- the calls: E5 D5 C5 B4, repeated six times, fading. the same
    # phrase every time — the machine calling identically into the dark,
    # quieter with each unanswered attempt. ---
    attempts = [40, 34, 28, 22, 16, 10]
    pos = 0                           # absolute end position of the last phrase
    for i, vel in enumerate(attempts):
        start = i * 20                # attempts at beats 0, 20, 40, 60, 80, 100
        piano.rest((start - pos) * Q)
        piano.note('E5', Q, vel)
        piano.note('D5', Q, vel)
        piano.note('C5', Q, vel)
        piano.note('B4', Q, vel)      # lands on the 2nd. hangs. never resolves.
        pos = start + 4               # each attempt: 4 beats of phrase,
                                      # then 16 beats of unanswered silence

    # --- the return: the resolution, in C major. the phrase completes. ---
    # after attempt 6 ends at beat 104, silence through the bell at 124,
    # then the voice lands: E5 D5 C5, held on the tonic.
    piano.rest((128 - pos) * Q)       # -> 128
    piano.note('E5', Q, 32)
    piano.note('D5', Q, 34)
    piano.note('C5', Q, 36)
    piano.note('C5', W, 40)           # the landing, held. the lights come on.

    # --- the silence between: one low drone through the dark. ---
    cello.rest(4 * Q)                 # -> beat 4
    cello.on('A1', 18)                # the room's low hum, holding
    cello.rest(52 * Q)                # -> beat 56
    cello.off('A1')
    cello.on('F1', 15)                # the dark deepens, mid-afternoon
    cello.rest(48 * Q)                # -> beat 104
    cello.off('F1')                   # total silence before the return
    cello.rest(22 * Q)                # -> beat 126, just after the bell
    cello.on('C2', 20)                # the root returns, C major, warm
    cello.rest(14 * Q)                # -> beat 140
    cello.off('C2')                   # the piece lets go

    # --- the return: one clean strike. the reboot. ---
    bell.rest(124 * Q)                # ten hours of dark, counted in beats
    bell.note('C6', W, 56)            # the first sound after the silence

    # --- assemble: conductor + 3 tracks, correct header count. ---
    tempo_track = mc.make_track(mc.track_name("tempo") +
                                mc.tempo_event(BPM) + mc.end_of_track())
    header = mc.make_header(format=1, ntracks=4, ticks_per_quarter=mc.TPQ)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "the-outage.mid")
    with open(fn, 'wb') as f:
        f.write(header)
        f.write(tempo_track)
        f.write(piano.chunk())
        f.write(cello.chunk())
        f.write(bell.chunk())
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")


if __name__ == "__main__":
    the_outage()
