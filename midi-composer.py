#!/usr/bin/env python3
"""
midi-composer.py — generate MIDI files from scratch (no libraries).
raw binary MIDI, same compositional approach as .mod tracker files.
"""

import struct, math

# === MIDI binary primitives ===

def write_vlq(n):
    """Variable-length quantity for delta times."""
    buf = bytearray()
    while True:
        buf.insert(0, n & 0x7F)
        n >>= 7
        if n == 0:
            break
    # Set continuation bit on all but last byte
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
    """Set tempo in beats per minute."""
    us_per_beat = int(60_000_000 / bpm)
    t = struct.pack('>I', us_per_beat)[1:]  # 3 bytes
    return write_vlq(delta) + b'\xFF\x51\x03' + t

def track_name(text, delta=0):
    t = text.encode('ascii', 'replace')
    return write_vlq(delta) + b'\xFF\x03' + write_vlq(len(t)) + t

def end_of_track(delta=0):
    return write_vlq(delta) + b'\xFF\x2F\x00'

def make_track(events: bytes) -> bytes:
    """Wrap events in a MIDI track chunk."""
    return b'MTrk' + struct.pack('>I', len(events)) + events

def make_header(format=1, ntracks=1, ticks_per_quarter=480):
    """Standard MIDI file header."""
    return b'MThd' + struct.pack('>IHHH', 6, format, ntracks, ticks_per_quarter)


# === musical helpers ===

NOTES = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
    'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11,
}

def midi_note(name, octave=4):
    """Convert note name to MIDI note number. 'C4' = 60."""
    n = name.rstrip('0123456789')
    o = int(name[len(n):]) if name[len(n):] else octave
    return NOTES[n] + (o + 1) * 12

# Standard MIDI instruments
INSTRUMENTS = {
    'piano': 0, 'bright_piano': 1, 'epiano': 4, 'harpsichord': 6,
    'xylophone': 13, 'organ': 19, 'guitar': 24, 'bass': 32,
    'strings': 48, 'synth_strings': 50, 'choir': 52, 'brass': 61,
    'flute': 73, 'square_lead': 80, 'pad': 89, 'fx': 99,
}

TPQ = 480  # ticks per quarter note
Q = TPQ       # quarter
E = TPQ // 2  # eighth
S = TPQ // 4  # sixteenth
H = TPQ * 2   # half
W = TPQ * 4   # whole


# === composition engine ===

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
        """Assemble into a track chunk."""
        header = bytearray()
        header.extend(track_name(f"track {self.channel}"))
        header.extend(tempo_event(120))  # default tempo
        header.extend(program_change(self.channel, self.program))
        return make_track(bytes(header) + bytes(self.events) + end_of_track())


def compose(filename, tracks, tempo=120):
    """Write a MIDI file from a list of MIDITrack objects."""
    ntracks = len(tracks)
    header = make_header(format=1, ntracks=ntracks, ticks_per_quarter=TPQ)

    # Tempo track (track 0)
    tempo_track = make_track(
        track_name("tempo") +
        tempo_event(tempo) +
        end_of_track()
    )

    with open(filename, 'wb') as f:
        f.write(header)
        f.write(tempo_track)
        for t in tracks:
            f.write(t.build())

    size = sum(len(t.build()) for t in tracks) + len(header) + len(tempo_track)
    print(f"wrote {filename} ({size:,} bytes, {ntracks} tracks, {tempo} bpm)")


# === composition: "fourth of july canon" ===

def fourth_of_july_canon():
    """A simple canon in D major for the 4th of July."""
    tracks = [
        MIDITrack(0, INSTRUMENTS['strings']),   # melody
        MIDITrack(1, INSTRUMENTS['piano']),     # counter-melody (canon)
        MIDITrack(2, INSTRUMENTS['bass']),      # bass
        MIDITrack(3, INSTRUMENTS['pad']),       # ambient pad
    ]

    # Melody — simple patriotic-ish theme in D major
    melody = [
        ('D4', Q), ('E4', Q), ('F#4', Q), ('G4', Q),
        ('A4', H), ('G4', Q), ('F#4', Q),
        ('E4', Q), ('D4', Q), ('E4', Q), ('F#4', Q), ('D4', H),
        ('A3', Q), ('B3', Q), ('C#4', Q), ('D4', Q),
        ('E4', H), ('D4', Q), ('C#4', Q),
        ('B3', Q), ('A3', Q), ('B3', Q), ('C#4', Q), ('A3', W),
    ]

    # Bass — simple roots
    bass = [
        ('D2', H), ('D2', H),
        ('A1', H), ('A1', H),
        ('B1', H), ('B1', H),
        ('G1', H), ('G1', H),
        ('D2', H), ('D2', H),
        ('A1', Q), ('B1', Q), ('C#2', Q), ('D2', Q),
        ('G1', H), ('A1', H),
        ('D2', W),
    ]

    # Pad — long held chords
    pads = [
        # D major (I)
        ('D3', W), ('F#3', W), ('A3', W),
        # A major (V)  
        ('A2', W), ('C#3', W), ('E3', W),
        # B minor (vi)
        ('B2', W), ('D3', W), ('F#3', W),
        # G major (IV)
        ('G2', W), ('B2', W), ('D3', W),
        # D major (I)
        ('D3', W), ('F#3', W), ('A3', W),
        # A major → D cadence
        ('A2', W), ('C#3', W), ('E3', W),
        ('G2', W), ('B2', W), ('D3', W),
        ('A2', W), ('D3', W),
    ]

    # Write the melody
    for note, dur in melody:
        tracks[0].note(note, dur, velocity=90)

    # Counter-melody — canon, enters after 2 beats with lower velocity
    tracks[1].rest(H)
    for note, dur in melody[:-2]:
        tracks[1].note(note, dur, velocity=70)
    tracks[1].rest(H * 2)  # pad to match length

    # Bass
    for note, dur in bass:
        tracks[2].note(note, dur, velocity=100)

    # Pad — sustained, velocity-faded
    vel = 50
    for note, dur in pads:
        tracks[3].note(note, dur, velocity=vel)
        vel = min(vel + 2, 70)

    compose("fourth-of-july-canon.mid", tracks, tempo=100)


if __name__ == "__main__":
    fourth_of_july_canon()
