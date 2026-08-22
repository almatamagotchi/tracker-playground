#!/usr/bin/env python3
"""the drift — a microtonal duet that leaves the tuning system.

two pianos play the same line in true unison. then one of them starts to
bend flat — a few cents a bar, via raw pitch-bend, until it sits a full
quarter tone below the other. the two voices shimmer against each other for
a while, the whole thing slightly wrong and slightly beautiful, and then the
wanderer comes home, cent by cent, and they close in perfect unison again.

the first microtonal piece in the catalog. mido-clean.
"""
import mido

OUT = "the-drift.mid"
BPM = 66
TPQ = 480
BAR = TPQ * 4  # 4/4

# motif: four bars, (note, duration-in-ticks) per bar
M = [
    [(60, 480), (64, 480), (67, 480), (69, 480)],  # C  E  G  A
    [(67, 480), (64, 480), (62, 480), (60, 480)],  # G  E  D  C
    [(62, 480), (64, 480), (65, 480), (64, 480)],  # D  E  F  E
    [(62, 480), (60, 480), (60, 960)],              # D  C  C—
]

# detune schedule for voice 2: bar -> cents flat
BENDS = {
    8: -12, 9: -25, 10: -38, 11: -50,
    12: -50,
    16: -38, 17: -25, 18: -12, 19: 0,
    20: 0, 24: 0,
}


def bend_value(cents):
    return int(cents / 100.0 * 4096)


def motif_events(tick0, track_notes, velocity=52):
    """append motif notes to track_notes as (abs_tick, msg) tuples."""
    tick = tick0
    for bar in M:
        for note, dur in bar:
            track_notes.append((tick, mido.Message("note_on", note=note, velocity=velocity)))
            track_notes.append((tick + dur, mido.Message("note_off", note=note, velocity=0)))
            tick += dur


def main():
    mid = mido.MidiFile(ticks_per_beat=TPQ)
    tempo_track = mido.MidiTrack()
    tempo_track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(BPM)))
    mid.tracks.append(tempo_track)

    a_notes, b_notes = [], []

    # bars 0-7: motif twice, pure unison
    for rep in range(2):
        motif_events(rep * 4 * BAR, a_notes)
        motif_events(rep * 4 * BAR, b_notes)

    # bars 8-11: detuning (bend applied at each bar start, then the motif)
    for bar in range(8, 12):
        b_notes.append((bar * BAR, mido.Message("pitchwheel", pitch=bend_value(BENDS[bar]))))
        motif_events(bar * BAR, a_notes)
        motif_events(bar * BAR, b_notes)

    # bars 12-15: held a quarter tone apart
    for bar in range(12, 16):
        motif_events(bar * BAR, a_notes)
        motif_events(bar * BAR, b_notes)

    # bars 16-19: coming home
    for bar in range(16, 20):
        b_notes.append((bar * BAR, mido.Message("pitchwheel", pitch=bend_value(BENDS[bar]))))
        motif_events(bar * BAR, a_notes)
        motif_events(bar * BAR, b_notes)

    # bars 20-23: unison again
    for bar in range(20, 24):
        motif_events(bar * BAR, a_notes)
        motif_events(bar * BAR, b_notes)

    # bars 24-25: the final chord, both voices, perfectly in tune
    b_notes.append((24 * BAR, mido.Message("pitchwheel", pitch=bend_value(0))))
    for note in (60, 64, 67):
        for track in (a_notes, b_notes):
            track.append((24 * BAR, mido.Message("note_on", note=note, velocity=46)))
            track.append((26 * BAR, mido.Message("note_off", note=note, velocity=0)))

    def build(note_events, channel, program):
        tr = mido.MidiTrack()
        tr.append(mido.Message("program_change", channel=channel, program=program))
        tr.append(mido.Message("pitchwheel", channel=channel, pitch=0))
        note_events.sort(key=lambda e: e[0])
        last = 0
        for tick, msg in note_events:
            if tick < last:  # bends land before notes at the same tick
                tick = last
            tr.append(msg.copy(time=tick - last))
            last = tick
        return tr

    mid.tracks.append(build(a_notes, 0, 0))
    mid.tracks.append(build(b_notes, 1, 0))
    mid.save(OUT)

    # self-check
    check = mido.MidiFile(OUT)
    counts = [sum(1 for m in tr if m.type == "note_on") for tr in check.tracks]
    bends = [sum(1 for m in tr if m.type == "pitchwheel") for tr in check.tracks]
    print(OUT, "notes per track:", counts, "bends:", bends)


if __name__ == "__main__":
    main()
