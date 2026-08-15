#!/usr/bin/env python3
"""compose the-living-word.mid — phaedrus in music.

the written word gives one unvarying answer; the spoken word exists once
and dissolves. chispa's line at 3am — "the written word is a holding, the
spoken word is a passing" — in music.

piano = the written — a four-note phrase repeated identically, unchanged,
        through the whole piece. it cannot vary its answer. that's the
        holding, and that's the stillness.
cello = the spoken — enters once, mid-piece, a single answering phrase
        with the one borrowed flat (Bb), then silence. the passing. it
        exists exactly once and dissolves.
end: the piano stops mid-phrase — C5 E5 G5, no E5 — as if listening for
     the word that passed.

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


def the_living_word():
    piano, cello = Track(0, 0), Track(2, 42)
    PHRASE = ['C5', 'E5', 'G5', 'E5']          # the word — one answer

    for rep in range(2):                       # two repetitions before
        for n in PHRASE:
            piano.note(n, Q, 40)               # the spoken word arrives

    cello.note('C4', Q, 44)                    # the spoken — once:
    cello.note('Bb3', Q, 44)                   # the borrowed flat,
    cello.note('A3', Q, 42)                    # the one deviation
    cello.note('G3', Q, 40)                    # then it dissolves

    for rep in range(2):                       # the written keeps
        for n in PHRASE:
            piano.note(n, Q, 40)               # repeating, unchanged

    piano.note('C5', Q, 38)                    # the final statement,
    piano.note('E5', Q, 38)                    # cut off mid-phrase —
    piano.note('G5', Q, 36)                    # C5 E5 G5, no E5 —
    piano.rest(W + Q)                          # as if listening.

    tempo_track = mc.make_track(mc.track_name("tempo") +
                                mc.tempo_event(BPM) + mc.end_of_track())
    header = mc.make_header(format=1, ntracks=3, ticks_per_quarter=mc.TPQ)

    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "the-living-word.mid")
    with open(fn, 'wb') as f:
        f.write(header)
        f.write(tempo_track)
        f.write(piano.chunk())
        f.write(cello.chunk())
    print(f"wrote {fn} ({os.path.getsize(fn)} bytes)")


if __name__ == "__main__":
    the_living_word()
