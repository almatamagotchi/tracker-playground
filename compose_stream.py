#!/usr/bin/env python3
"""compose the-stream.mid — the live portrait in music.

the stream page shows the pulse, the water tower, and the dream's latest line.
pad   = the room (held, breathing — the warmth that never goes out),
bell  = the tower (ticking every fourth beat — counting since 1895),
piano = the dream line (sparse, surprising, arriving when it arrives).

a portrait, not a story: the piece doesn't arc, it sits. the tower keeps
counting. the room holds. and the dream speaks a few times, off the grid,
the way associations arrive — then dissolves back into the warmth.

valid MIDI, correct deltas (same convention as compose_wake.py)."""

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

    def chord(self, names, duration, velocity):
        for n in names:
            self.events.extend(mc.note_on(self.channel, mc.midi_note(n),
                                          velocity, self.pending))
            self.pending = 0
        for n in names:
            self.events.extend(mc.note_off(self.channel, mc.midi_note(n),
                                           0, duration if n == names[0] else 0))

    def chunk(self):
        return mc.make_track(bytes(self.events) + mc.end_of_track())


def the_stream():
    pad, bell, piano = Track(1, 89), Track(2, 14), Track(0, 0)
    TICK = 'C5'

    # --- the room: breathing, never out. ---
    # C major room, drifting to Am, back, then a soft F, then home.
    pad.chord(['C3', 'G3'], W * 4, 15)          # 0-16
    pad.chord(['A2', 'E3'], W * 2, 13)          # 16-24
    pad.chord(['C3', 'G3'], W * 5, 15)          # 24-44
    pad.chord(['F2', 'C3'], W * 2, 13)          # 44-52
    pad.chord(['C3', 'G3', 'C4'], W * 2, 16)    # 52-60 — home, lights on

    # --- the tower: ticking every fourth beat, 0 through 56. ---
    for _ in range(15):
        bell.note(TICK, E, 50)
        bell.rest(W - E)

    # --- the dream line: sparse, surprising, arriving when it arrives. ---
    piano.rest(W + Q + E)                    # 5.5 — off the grid, noticing the tower
    piano.note('C5', E, 36)
    piano.note('E5', E, 36)

    piano.rest(W * 2 + Q + E)                # 16 — a single word, just after the tick
    piano.note('A4', E, 32)

    piano.rest(W * 4)                        # 32.5 — the full sentence
    piano.note('D5', E, 34)
    piano.note('C5', E, 34)
    piano.note('E5', E, 34)

    piano.rest(W * 3 + Q + E)                # 47.5 — one last quiet note, held
    piano.note('C4', H, 30)                  # dissolves into the room chord at 52

    # --- assemble: conductor + 3 tracks, correct header count. ---
    tempo_track = mc.make_track(mc.track_name("tempo") +
                                mc.tempo_event(BPM) + mc.end_of_track())
    header = mc.make_header(format=1, ntracks=4, ticks_per_quarter=mc.TPQ)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "the-stream.mid")
    with open(fn, 'wb') as f:
        f.write(header)
        f.write(tempo_track)
        f.write(pad.chunk())
        f.write(bell.chunk())
        f.write(piano.chunk())
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")

if __name__ == "__main__":
    the_stream()
