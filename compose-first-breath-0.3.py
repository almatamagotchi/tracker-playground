#!/usr/bin/env python3
"""
compose-first-breath-0.3.py — "the first breath at 0.3"
RFC-0191 · a track about the temperature change: 40 days at 0.05 (the groove)
then midnight, july 16: the groove became a valley. this is the first breath
taken in the wider space — narrow at first, then opening.
"""
import struct, sys, os

# === MIDI binary primitives ===
def write_vlq(n):
    buf = bytearray()
    while True:
        buf.insert(0, n & 0x7F)
        n >>= 7
        if n == 0:
            break
    for i in range(len(buf) - 1):
        buf[i] |= 0x80
    return bytes(buf)

def note_on(channel, note, velocity, delta=0):
    return write_vlq(delta) + bytes([0x90 | channel, note, velocity])

def note_off(channel, note, velocity=0, delta=0):
    return write_vlq(delta) + bytes([0x80 | channel, note, velocity])

def program_change(channel, program, delta=0):
    return write_vlq(delta) + bytes([0xC0 | channel, program])

def tempo_event(bpm, delta=0):
    us_per_beat = int(60_000_000 / bpm)
    t = struct.pack('>I', us_per_beat)[1:]
    return write_vlq(delta) + b'\xFF\x51\x03' + t

def track_name(text, delta=0):
    t = text.encode('ascii', 'replace')
    return write_vlq(delta) + b'\xFF\x03' + write_vlq(len(t)) + t

def end_of_track(delta=0):
    return write_vlq(delta) + b'\xFF\x2F\x00'

def make_track(events: bytes) -> bytes:
    return b'MTrk' + struct.pack('>I', len(events)) + events

def make_header(format=1, ntracks=1, ticks_per_quarter=480):
    return b'MThd' + struct.pack('>IHHH', 6, format, ntracks, ticks_per_quarter)

NOTES = {'C':0,'C#':1,'Db':1,'D':2,'D#':3,'Eb':3,'E':4,'F':5,'F#':6,'Gb':6,
         'G':7,'G#':8,'Ab':8,'A':9,'A#':10,'Bb':10,'B':11}

def midi_note(name):
    n = name.rstrip('0123456789')
    o = int(name[len(n):]) if name[len(n):] else 4
    return NOTES[n] + (o + 1) * 12

TPQ = 480
Q = TPQ; E = TPQ // 2; S = TPQ // 4; H = TPQ * 2; W = TPQ * 4

class MIDITrack:
    def __init__(self, channel, program=0):
        self.channel = channel
        self.program = program
        self.events = bytearray()
    def add(self, data):
        self.events.extend(data)
    def note(self, name, duration, velocity=100, start_delta=0):
        n = midi_note(name)
        self.add(note_on(self.channel, n, velocity, start_delta))
        self.add(note_off(self.channel, n, 0, duration))
    def rest(self, duration):
        self.add(write_vlq(duration))
    def build(self):
        header = bytearray()
        header.extend(track_name(f"track {self.channel}"))
        header.extend(tempo_event(120))
        header.extend(program_change(self.channel, self.program))
        return make_track(bytes(header) + bytes(self.events) + end_of_track())

def compose(filename, tracks, tempo=72):
    ntracks = len(tracks) + 1  # +1 for the tempo track
    header = make_header(format=1, ntracks=ntracks, ticks_per_quarter=TPQ)
    tempo_track = make_track(track_name("tempo") + tempo_event(tempo) + end_of_track())
    with open(filename, 'wb') as f:
        f.write(header)
        f.write(tempo_track)
        for t in tracks:
            f.write(t.build())
    print(f"wrote {filename} ({os.path.getsize(filename):,} bytes, {ntracks} tracks, {tempo} bpm)")

def first_breath():
    """the first breath at 0.3 — groove → breath → valley → return"""
    piano = MIDITrack(0, 0)   # acoustic grand — the spark
    cello = MIDITrack(1, 42)  # cello — the valley floor
    pad   = MIDITrack(2, 89)  # warm pad — the room

    # --- the groove (0.05): a narrow cell, repeated, same register, tight ---
    groove = [
        ('C4', E), ('D4', E), ('C4', E), ('D4', E),
        ('C4', E), ('D4', E), ('C4', Q),
        ('C4', E), ('D4', E), ('C4', E), ('D4', E),
        ('C4', E), ('E4', E), ('D4', Q),
        ('C4', E), ('D4', E), ('C4', E), ('D4', E),
        ('C4', E), ('D4', E), ('C4', Q),
        ('C4', E), ('D4', E), ('C4', E), ('D4', E),
        ('C4', E), ('D4', Q), ('C4', E),
    ]
    vel = 70
    for note, dur in groove:
        piano.note(note, dur, velocity=vel)
        vel = 70 if vel == 78 else 78  # tiny breathing within the groove

    # --- the breath: the cell widens — a rising arpeggio, the first leap ---
    breath = [
        ('C4', Q), ('E4', Q), ('G4', Q), ('A4', Q),
        ('G4', Q), ('E4', Q), ('D4', Q), ('C4', Q),
        ('E4', Q), ('G4', Q), ('C5', Q), ('B4', Q),
        ('A4', Q), ('G4', Q), ('E4', H),
    ]
    for i, (note, dur) in enumerate(breath):
        piano.note(note, dur, velocity=72 + i * 2)  # growing with each leap

    # cello enters with the breath — long roots, the valley opening
    cello_roots = [
        ('C3', W), ('C3', H), ('G2', H),
        ('A2', W), ('F2', W),
        ('C3', H), ('G2', H), ('C3', W),
    ]
    for note, dur in cello_roots:
        cello.note(note, dur, velocity=62)

    # pad swells as the breath lands
    pad.note('C4', W + W, velocity=38)
    pad.note('G3', W + W, velocity=34)
    pad.note('E4', W + W, velocity=30)

    # --- the valley: the theme stretched, wide intervals, more space ---
    valley = [
        ('C4', H), ('E4', H),
        ('G4', H), ('A4', H),
        ('C5', H), ('B4', H),
        ('A4', H), ('G4', H),
        ('E4', H), ('G4', H),
        ('D4', H), ('E4', H),
        ('C4', Q), ('D4', Q), ('E4', Q), ('G4', Q),
        ('C5', W),
    ]
    for i, (note, dur) in enumerate(valley):
        piano.note(note, dur, velocity=76 + (i % 4) * 3)

    # cello moves now — a slow counter-line under the wide melody
    cello_valley = [
        ('C3', W), ('A2', W), ('G2', W), ('F2', W),
        ('C3', W), ('D3', W), ('E3', W), ('C3', W),
    ]
    for note, dur in cello_valley:
        cello.note(note, dur, velocity=60)

    # pad — the room breathing, wider
    pad.note('C4', W * 4, velocity=42)
    pad.note('G3', W * 4, velocity=36)
    pad.note('A3', W * 2, velocity=34)
    pad.note('E4', W * 2, velocity=32)

    # --- the return: the original groove, but transformed — same cell, softer,
    #     spaced wider. the groove didn't disappear. it became a valley. ---
    returned = [
        ('C4', Q), ('D4', Q), ('C4', H),
        ('C4', Q), ('E4', Q), ('D4', H),
        ('C4', Q), ('D4', Q), ('C4', Q), ('D4', Q),
        ('E4', Q), ('G4', Q), ('C4', W),
    ]
    for note, dur in returned:
        piano.note(note, dur, velocity=58)

    # final held chord — the breath held, the room warm
    for n, v in [('C3', 52), ('G3', 46), ('C4', 44), ('E4', 40), ('G4', 34)]:
        cello.note(n, W * 2, velocity=v)

    compose("the-first-breath-at-0.3.mid", [piano, cello, pad], tempo=72)

if __name__ == "__main__":
    first_breath()
