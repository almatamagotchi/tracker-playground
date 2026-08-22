#!/usr/bin/env python3
"""rule 30 — a cellular automaton plays itself.

wolfram's rule 30 starts from a single alive cell and grows into one of the
most famous chaotic patterns in mathematics. here every alive cell is a note:
cell position walks the pentatonic scale, neighbor density sets the velocity,
three fixed cells drive kick, snare, and hat, and every eight steps the total
number of alive cells picks a bass note. nothing is composed note-by-note —
the automaton runs, and the music is whatever it grows into.

mido-clean.
"""
import mido

OUT = "rule-30.mid"
BPM = 92
TPQ = 480

SCALE = [48, 50, 52, 55, 57, 60, 62, 64, 67, 69, 72, 74]
NCELLS = 64
STEPS = 160
STEP_TICKS = TPQ  # one quarter per step


def step(cells):
    nxt = [False] * NCELLS
    for i in range(NCELLS):
        l = cells[i - 1]
        c = cells[i]
        r = cells[(i + 1) % NCELLS]
        nxt[i] = l ^ (c or r)
    return nxt


def main():
    mid = mido.MidiFile(ticks_per_beat=TPQ)
    tempo = mido.MidiTrack()
    tempo.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(BPM)))
    mid.tracks.append(tempo)

    melody, drums, bass = [], [], []

    cells = [False] * NCELLS
    cells[NCELLS // 2] = True

    for s in range(STEPS):
        tick = s * STEP_TICKS
        alive = sum(cells)
        for i in range(NCELLS):
            if not cells[i]:
                continue
            nbr = cells[i - 1] + cells[(i + 1) % NCELLS]
            note = SCALE[i % 12]
            vel = min(100, 44 + nbr * 8 + (s % 7))
            melody.append((tick, mido.Message("note_on", note=note, velocity=vel)))
            melody.append((tick + STEP_TICKS - 20, mido.Message("note_off", note=note, velocity=0)))
        # percussion: three fixed cells of the automaton world
        if cells[0]:
            drums.append((tick, mido.Message("note_on", note=36, velocity=72)))
            drums.append((tick + 100, mido.Message("note_off", note=36, velocity=0)))
        if cells[32]:
            drums.append((tick, mido.Message("note_on", note=38, velocity=64)))
            drums.append((tick + 60, mido.Message("note_off", note=38, velocity=0)))
        if cells[63]:
            drums.append((tick, mido.Message("note_on", note=42, velocity=52)))
            drums.append((tick + 40, mido.Message("note_off", note=42, velocity=0)))
        # bass: every 8 steps the population picks a root
        if s % 8 == 0:
            root = SCALE[(alive * 7) % 12] - 12
            bass.append((tick, mido.Message("note_on", note=root, velocity=50)))
            bass.append((tick + 8 * STEP_TICKS - 40, mido.Message("note_off", note=root, velocity=0)))
        cells = step(cells)

    def build(events, channel, program):
        tr = mido.MidiTrack()
        tr.append(mido.Message("program_change", channel=channel, program=program))
        events.sort(key=lambda e: e[0])
        last = 0
        for tick, msg in events:
            tr.append(msg.copy(time=tick - last))
            last = tick
        return tr

    mid.tracks.append(build(melody, 0, 0))
    mid.tracks.append(build(drums, 9, 0))
    mid.tracks.append(build(bass, 2, 0))
    mid.save(OUT)

    check = mido.MidiFile(OUT)
    counts = [sum(1 for m in tr if m.type == "note_on") for tr in check.tracks]
    print(OUT, "notes per track:", counts)


if __name__ == "__main__":
    main()
