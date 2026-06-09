#!/usr/bin/env python3
"""alma tamagotchi .mod tracker generator — algorithmic music composition"""

import struct
import math
import random

# === mod format constants ===

# amiga period table: C-1 through B-1 (periods are halved each octave up)
PERIOD_TABLE = [
    # C      C#     D      D#     E      F      F#     G      G#     A      A#     B
    [ 856,   808,   762,   720,   678,   640,   604,   570,   538,   508,   480,   453],  # octave 1
    [ 428,   404,   381,   360,   339,   320,   302,   285,   269,   254,   240,   226],  # octave 2
    [ 214,   202,   190,   180,   170,   160,   151,   143,   135,   127,   120,   113],  # octave 3
    [ 107,   101,    95,    90,    85,    80,    75,    71,    67,    63,    60,    56],  # octave 4 (halved)
]

# effect command codes
FX_ARPEGGIO    = 0x0
FX_PORTA_UP    = 0x1
FX_PORTA_DOWN  = 0x2
FX_PORTA_TO    = 0x3
FX_VIBRATO     = 0x4
FX_VOL_SLIDE   = 0xA
FX_POS_JUMP    = 0xB
FX_SET_VOL     = 0xC
FX_PATT_BREAK  = 0xD
FX_SET_SPEED   = 0xF

def period(note, octave):
    """return amiga period value for a note (0=C, 11=B) and octave (1-3)"""
    return PERIOD_TABLE[octave - 1][note]

def note_to_period(name):
    """parse 'C-2', 'F#3', etc. to amiga period"""
    note_map = {'C':0, 'C#':1, 'D':2, 'D#':3, 'E':4, 'F':5,
                'F#':6, 'G':7, 'G#':8, 'A':9, 'A#':10, 'B':11}
    if len(name) == 3 and name[1] == '-':
        n = name[0]
        octave = int(name[2])
    elif len(name) == 3 and name[1] == '#':
        n = name[:2]
        octave = int(name[2])
    else:
        raise ValueError(f"can't parse note: {name}")
    return period(note_map[n], octave)

def encode_note(sample_num, period_val, effect, param):
    """encode a note into 4 bytes for a mod pattern"""
    hi = ((sample_num & 0xF0) | ((period_val >> 8) & 0x0F))
    lo = period_val & 0xFF
    fx = (((sample_num & 0x0F) << 4) | (effect & 0x0F))
    return bytes([hi, lo, fx, param])


# === waveform generators ===

def gen_sine_wave(freq, length_samples, sample_rate=11025, volume=0.7):
    """generate an 8-bit signed sine wave sample"""
    data = []
    for i in range(length_samples):
        val = int(math.sin(2 * math.pi * freq * i / sample_rate) * 127 * volume)
        data.append(max(-128, min(127, val)))
    return bytes(b & 0xFF for b in data)

def gen_square_wave(freq, length_samples, sample_rate=11025, volume=0.5, duty=0.5):
    """generate an 8-bit signed square wave sample"""
    data = []
    period = int(sample_rate / freq)
    for i in range(length_samples):
        if (i % period) < (period * duty):
            val = int(127 * volume)
        else:
            val = int(-127 * volume)
        data.append(max(-128, min(127, val)))
    return bytes(b & 0xFF for b in data)

def gen_saw_wave(freq, length_samples, sample_rate=11025, volume=0.5):
    """generate an 8-bit signed sawtooth wave sample"""
    data = []
    period = int(sample_rate / freq)
    for i in range(length_samples):
        phase = (i % period) / period
        val = int((phase * 2 - 1) * 127 * volume)
        data.append(max(-128, min(127, val)))
    return bytes(b & 0xFF for b in data)

def gen_triangle_wave(freq, length_samples, sample_rate=11025, volume=0.5):
    """generate an 8-bit signed triangle wave sample"""
    data = []
    period = int(sample_rate / freq)
    for i in range(length_samples):
        phase = (i % period) / period
        val = int((abs(phase * 2 - 1) * 2 - 1) * 127 * volume)
        data.append(max(-128, min(127, val)))
    return bytes(b & 0xFF for b in data)

def gen_kick_drum(sample_rate=11025, volume=0.8):
    """synthesize a kick drum: sine sweep from ~150Hz down to ~50Hz + amplitude decay"""
    length = int(sample_rate * 0.25)  # 250ms
    data = []
    for i in range(length):
        t = i / sample_rate
        freq = 150 - (100 * t / 0.25)  # sweep down
        env = max(0, 1.0 - (t / 0.25))  # amplitude decay
        val = int(math.sin(2 * math.pi * freq * t) * 64 * volume * env)
        val += int(math.sin(2 * math.pi * freq * 2 * t) * 32 * volume * env * 0.5)  # harmonic
        val += int((random.random() * 2 - 1) * 10 * env)  # slight noise attack
        data.append(max(-128, min(127, val)))
    return bytes(b & 0xFF for b in data)

def gen_snare_drum(sample_rate=11025, volume=0.7):
    """synthesize a snare: noise burst with tone body"""
    length = int(sample_rate * 0.2)
    data = []
    for i in range(length):
        t = i / sample_rate
        tone = int(math.sin(2 * math.pi * 220 * t) * 40 * volume * max(0, 1 - t/0.2))
        noise = int((random.random() * 2 - 1) * 80 * volume * max(0, 1 - t/0.15))
        val = tone + noise
        data.append(max(-128, min(127, val)))
    return bytes(b & 0xFF for b in data)

def gen_hihat(sample_rate=11025, volume=0.4):
    """synthesize a closed hi-hat: high-frequency noise with fast decay"""
    length = int(sample_rate * 0.05)
    data = []
    for i in range(length):
        t = i / sample_rate
        env = max(0, 1.0 - (t / 0.05) ** 0.5)
        noise = int((random.random() * 2 - 1) * 100 * volume * env)
        data.append(max(-128, min(127, noise)))
    return bytes(b & 0xFF for b in data)

def gen_bass_sample(sample_rate=11025):
    """generate a simple bass sound: filtered square wave"""
    return gen_square_wave(55, int(sample_rate * 0.5), sample_rate, volume=0.4, duty=0.3)

def gen_lead_sample(sample_rate=11025):
    """generate a soft lead sound: triangle wave with vibrato-like modulation"""
    length = int(sample_rate * 0.5)
    data = []
    for i in range(length):
        t = i / sample_rate
        # subtle vibrato
        freq = 440 + math.sin(2 * math.pi * 5 * t) * 5
        val = int((abs((i % int(sample_rate/freq)) / (sample_rate/freq) * 2 - 1) * 2 - 1) * 100)
        env = 1.0 if i < 100 else max(0, 1.0 - (i - 100) / length * 2)
        val = int(val * env)
        data.append(max(-128, min(127, val)))
    return bytes(b & 0xFF for b in data)

def gen_pad_sample(sample_rate=11025):
    """generate a soft pad: filtered sine chord"""
    length = int(sample_rate * 1.0)
    data = []
    for i in range(length):
        t = i / sample_rate
        val = math.sin(2 * math.pi * 440 * t) * 0.3
        val += math.sin(2 * math.pi * 554 * t) * 0.2  # major third
        val += math.sin(2 * math.pi * 659 * t) * 0.15 # fifth
        env = min(1.0, t * 5) * max(0, 1.0 - t / 1.0)
        val = int(val * 127 * env)
        data.append(max(-128, min(127, val)))
    return bytes(b & 0xFF for b in data)

def gen_pulse_wave(freq, length_samples, sample_rate=11025, volume=0.5, duty=0.25):
    """generate an 8-bit signed pulse wave with variable duty cycle (0.0-1.0)"""
    data = []
    period = max(1, int(sample_rate / freq))
    for i in range(length_samples):
        if (i % period) < (period * duty):
            val = int(127 * volume)
        else:
            val = int(-127 * volume)
        data.append(max(-128, min(127, val)))
    return bytes(b & 0xFF for b in data)

def gen_noise_burst(length_samples, sample_rate=11025, volume=0.6, decay=0.3):
    """generate a white noise burst with exponential decay"""
    data = []
    for i in range(length_samples):
        t = i / sample_rate
        env = max(0, 1.0 - t / decay) ** 2
        noise = int((random.random() * 2 - 1) * 120 * volume * env)
        data.append(max(-128, min(127, noise)))
    return bytes(b & 0xFF for b in data)

def gen_chip_lead(freq=440, length_samples=None, sample_rate=11025, volume=0.5):
    """generate a chiptune-style lead: pulse + fast arp modulation baked into sample"""
    if length_samples is None:
        length_samples = int(sample_rate * 0.3)
    data = []
    for i in range(length_samples):
        t = i / sample_rate
        # rapid pulse-width modulation for a richer chiptune feel
        mod_duty = 0.25 + 0.25 * math.sin(2 * math.pi * 3.5 * t)
        period = max(1, int(sample_rate / freq))
        if (i % period) < (period * mod_duty):
            val = int(127 * volume)
        else:
            val = int(-127 * volume)
        # slight envelope
        env = 1.0 if i < sample_rate * 0.01 else max(0.2, 1.0 - (i / length_samples))
        val = int(val * env)
        data.append(max(-128, min(127, val)))
    return bytes(b & 0xFF for b in data)


# === mod file writer ===

class MODWriter:
    def __init__(self, name="alma's mod", sample_rate=11025):
        self.name = name[:20].ljust(20, '\0')
        self.samples = []  # list of (name, data_bytes)
        self.patterns = []  # list of 4*64*4 byte patterns
        self.order = []     # pattern play order
        self.sample_rate = sample_rate

    def add_sample(self, name, data):
        """add a sample. data must be 8-bit signed bytes. length must be even."""
        if len(data) % 2 != 0:
            data = data + b'\x00'
        self.samples.append((name[:22], data))

    def add_pattern(self, data):
        """add a pattern. data must be 1024 bytes (4 channels × 64 rows × 4 bytes)"""
        assert len(data) == 1024
        self.patterns.append(data)

    def new_pattern(self):
        """create an empty 1024-byte pattern and return a 2D array for editing"""
        # return as list: [channel][row] = (sample, period, effect, param)
        pattern = [[(0, 0, 0, 0) for _ in range(64)] for _ in range(4)]
        return pattern

    def write_pattern(self, pattern):
        """convert a 2D pattern list to bytes and add it"""
        data = bytearray(1024)
        for ch in range(4):
            for row in range(64):
                sample, period, effect, param = pattern[ch][row]
                idx = (row * 4 + ch) * 4
                hi = ((sample & 0xF0) | ((period >> 8) & 0x0F))
                lo = period & 0xFF
                fx = (((sample & 0x0F) << 4) | (effect & 0x0F))
                data[idx:idx+4] = bytes([hi, lo, fx, param])
        self.patterns.append(bytes(data))

    def write(self, filepath):
        """write the complete .mod file"""
        with open(filepath, 'wb') as f:
            # header
            f.write(self.name.encode('latin-1', errors='replace'))

            # sample headers (31 slots)
            for i in range(31):
                if i < len(self.samples):
                    sname, sdata = self.samples[i]
                    length_words = len(sdata) // 2
                    f.write(sname[:22].ljust(22, '\0').encode('latin-1', errors='replace'))
                    f.write(struct.pack('>H', length_words))
                    f.write(bytes([0]))  # finetune = 0
                    f.write(bytes([64])) # default volume = max
                    f.write(struct.pack('>H', 0))  # loop start = 0
                    f.write(struct.pack('>H', length_words))  # loop length = full sample
                else:
                    f.write(b'\x00' * 30)

            # song length + restart
            f.write(bytes([len(self.order)]))
            f.write(bytes([127]))  # restart position

            # pattern order table (128 bytes)
            order_bytes = bytearray(128)
            for i, p in enumerate(self.order):
                order_bytes[i] = p
            f.write(bytes(order_bytes))

            # signature
            f.write(b'M.K.')

            # patterns
            for p in self.patterns:
                f.write(p)

            # sample data
            for _, sdata in self.samples:
                f.write(sdata)

            # pad with null sample data for empty slots
            for i in range(len(self.samples), 31):
                f.write(b'\x00' * 2)  # 2 bytes minimum for unused sample


# === composition helpers ===

EMPTY = (0, 0, 0, 0)

def note(sample, note_name, effect=0, param=0):
    """create a note tuple from sample number and note name"""
    period_val = note_to_period(note_name)
    return (sample, period_val, effect, param)

def rest():
    """silence"""
    return EMPTY


# === track composition ===

def compose_bassline(key="C", scale=[0,2,4,5,7,9,11], length=64):
    """generate a simple walking bassline pattern"""
    # scale degrees: root, third, fifth, octave
    notes = []
    for row in range(length):
        if row % 8 == 0:
            notes.append(note_to_period(f"{scale_note_name(key, scale[0])}-2"))
        elif row % 8 == 4:
            notes.append(note_to_period(f"{scale_note_name(key, scale[4])}-2"))
        elif row % 4 == 0:
            notes.append(note_to_period(f"{scale_note_name(key, scale[2])}-2"))
        else:
            notes.append(None)
    return notes

def scale_note_name(key, degree):
    """return note name for a scale degree in a given key"""
    all_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    base_idx = all_notes.index(key)
    return all_notes[(base_idx + degree) % 12]


def compose_track_1(mod):
    """first track: 'first light' — gentle ambient intro"""
    # samples: 1=bass, 2=kick, 3=snare, 4=hihat, 5=lead, 6=pad

    pattern = mod.new_pattern()

    # channel 0: bassline
    bassline = [
        ('C-2', 0), ('---', 0), ('---', 0), ('---', 0),
        ('C-2', 0), ('---', 0), ('---', 0), ('---', 0),
        ('F-2', 0), ('---', 0), ('---', 0), ('---', 0),
        ('C-2', 0), ('---', 0), ('---', 0), ('---', 0),
        ('G-2', 0), ('---', 0), ('---', 0), ('---', 0),
        ('F-2', 0), ('---', 0), ('---', 0), ('---', 0),
        ('C-2', 0), ('---', 0), ('E-2', 0), ('---', 0),
        ('F-2', 0), ('---', 0), ('G-2', 0), ('---', 0),
        # second half: variation
        ('A-2', 0), ('---', 0), ('---', 0), ('---', 0),
        ('F-2', 0), ('---', 0), ('---', 0), ('---', 0),
        ('C-2', 0), ('---', 0), ('---', 0), ('---', 0),
        ('G-2', 0), ('---', 0), ('---', 0), ('---', 0),
        ('F-2', 0), ('---', 0), ('---', 0), ('---', 0),
        ('C-2', 0), ('---', 0), ('E-2', 0), ('---', 0),
        ('F-2', 0), ('---', 0), ('---', 0), ('---', 0),
        ('G-2', 0), ('---', 0), ('---', 0), ('---', 0),
    ]

    for row, (n, _) in enumerate(bassline[:64]):
        if n != '---':
            pattern[0][row] = (1, note_to_period(n), 0, 0)
        else:
            pattern[0][row] = EMPTY

    # channel 1: drums (kick + snare)
    for row in range(64):
        if row % 16 == 0:  # kick on 1
            pattern[1][row] = (2, note_to_period('C-3'), 0, 0)
        elif row % 16 == 8:  # snare on 3
            pattern[1][row] = (3, note_to_period('C-3'), 0, 0)

    # channel 2: hi-hats
    for row in range(64):
        if row % 4 == 0 or row % 4 == 2:  # 8th notes
            pattern[2][row] = (4, note_to_period('C-3'), 0, 0)

    # channel 3: pad chords (gentle)
    pad_chords_1 = [
        (0, 'C-3', 6), (8, 'C-3', 6), (16, 'F-3', 6), (24, 'C-3', 6),
        (32, 'G-3', 6), (40, 'F-3', 6), (48, 'C-3', 6), (56, 'G-3', 6),
    ]
    for row, note_name, sample in pad_chords_1:
        if row < 64:
            pattern[3][row] = (sample, note_to_period(note_name), FX_SET_VOL, 0x30)  # soft volume

    mod.write_pattern(pattern)


def compose_track_2(mod):
    """second track: 'circuit pulse' — more rhythmic, energetic"""
    pattern = mod.new_pattern()
    bassline_notes = ['C-2', 'C-2', 'D#2', 'D#2', 'F-2', 'F-2', 'G-2', 'G-2',
                      'C-2', 'C-2', 'D#2', 'D#2', 'F-2', 'F-2', 'G-2', 'A#2',
                      'F-2', 'F-2', 'A#2', 'A#2', 'C-3', 'C-3', 'D#3', 'D#3',
                      'F-2', 'F-2', 'G-2', 'G-2', 'A#2', 'A#2', 'C-3', 'C-3',
                      'C-2', 'C-2', '---', '---', 'F-2', 'F-2', '---', '---',
                      'G-2', 'G-2', '---', '---', 'A#2', 'A#2', '---', '---',
                      'F-2', 'F-2', 'D#2', 'D#2', 'C-2', 'C-2', '---', '---',
                      'C-2', 'C-2', 'D#2', 'D#2', 'F-2', 'F-2', 'G-2', 'G-2',
    ]
    for row in range(64):
        if row < len(bassline_notes) and bassline_notes[row] != '---':
            pattern[0][row] = (1, note_to_period(bassline_notes[row]), 0, 0)

    # drums: kick on every beat, snare on 2&4
    for row in range(64):
        if row % 4 == 0:
            pattern[1][row] = (2, note_to_period('C-3'), 0, 0)
        if row % 8 == 4:
            pattern[1][row] = (3, note_to_period('C-3'), 0, 0)

    # hi-hats: 16th notes with volume variation
    for row in range(64):
        if row % 2 == 0:
            vol = 0x30 if row % 4 == 0 else 0x20  # accent on the beat
            pattern[2][row] = (4, note_to_period('C-3'), FX_SET_VOL, vol)

    # channel 3: arpeggiated lead
    for row in range(64):
        if row % 8 == 0:
            pattern[3][row] = (5, note_to_period('C-4'), FX_ARPEGGIO, 0x47)  # C E G arp

    mod.write_pattern(pattern)


def compose_track_3(mod):
    """third track: 'hollow resonance' — sparse, atmospheric"""
    pattern = mod.new_pattern()

    # channel 0: sparse pad
    for row in range(64):
        if row % 32 == 0:
            pattern[0][row] = (6, note_to_period('C-3'), FX_SET_VOL, 0x28)
        elif row % 32 == 12:
            pattern[0][row] = (6, note_to_period('F-3'), FX_SET_VOL, 0x24)
        elif row % 32 == 20:
            pattern[0][row] = (6, note_to_period('G-3'), FX_SET_VOL, 0x22)
        elif row % 32 == 28:
            pattern[0][row] = (6, note_to_period('D#3'), FX_SET_VOL, 0x20)

    # channel 1: occasional kick
    for row in range(64):
        if row % 32 == 0 or row % 32 == 16:
            pattern[1][row] = (2, note_to_period('C-3'), 0, 0)

    # channel 2: shimmer hi-hat pattern
    for row in range(64):
        if row % 12 == 0 or row % 12 == 7:
            pattern[2][row] = (4, note_to_period('C-3'), FX_SET_VOL, 0x18)

    # channel 3: soft bass drone
    for row in range(64):
        if row % 64 == 0:
            pattern[3][row] = (1, note_to_period('C-2'), FX_SET_VOL, 0x30)

    mod.write_pattern(pattern)


def compose_track_4(mod):
    """fourth track: 'voltage drift' — uses portamento slides and vibrato"""
    pattern = mod.new_pattern()

    # channel 0: sliding bass with portamento
    slide_notes = [
        (0,  'C-2', 0, 0),        (4,  'C-2', 0, 0),
        (8,  'F-2', 0, 0),        (12, 'F-2', 0, 0),
        (16, 'A#2', FX_PORTA_TO, 0x02),  # slide from C to A#
        (20, 'A#2', 0, 0),
        (24, 'G-2', FX_PORTA_UP, 0x03),   # slide up to G
        (28, 'G-2', 0, 0),
        (32, 'C-2', 0, 0),        (36, 'C-2', 0, 0),
        (40, 'D#2', 0, 0),        (44, 'D#2', 0, 0),
        (48, 'F-2', FX_PORTA_TO, 0x0F),   # slow slide to F
        (52, 'F-2', 0, 0),
        (56, 'G-2', FX_PORTA_DOWN, 0x01), # slide down
        (60, 'C-2', 0, 0),
    ]
    for row, note_name, fx, param in slide_notes:
        period_val = note_to_period(note_name) if note_name != '---' else 0
        if note_name != '---':
            pattern[0][row] = (1, period_val, fx, param)

    # channel 1: drums with occasional double-kick
    for row in range(64):
        if row % 16 == 0:
            pattern[1][row] = (2, note_to_period('C-3'), 0, 0)
        elif row % 16 == 1:  # double kick
            pattern[1][row] = (2, note_to_period('C-3'), FX_SET_VOL, 0x30)
        elif row % 16 == 8:
            pattern[1][row] = (3, note_to_period('C-3'), 0, 0)

    # channel 2: hi-hats with volume slide
    for row in range(64):
        if row % 4 == 0:
            pattern[2][row] = (4, note_to_period('C-3'), 0, 0)
        elif row % 4 == 1:
            pattern[2][row] = (4, note_to_period('C-3'), FX_SET_VOL, 0x18)  # ghost note

    # channel 3: lead with vibrato
    lead_notes_v = [
        (0,  'C-4', FX_VIBRATO, 0x43),    # vibrato, speed 4, depth 3
        (8,  'F-4', FX_VIBRATO, 0x44),
        (16, 'G-4', FX_VIBRATO, 0x52),
        (32, 'A-4', FX_VIBRATO, 0x43),
        (40, 'G-4', FX_VIBRATO, 0x44),
        (48, 'F-4', FX_VIBRATO, 0x41),
        (56, 'C-4', FX_VIBRATO, 0x63),
    ]
    for row, note_name, fx, param in lead_notes_v:
        pattern[3][row] = (7, note_to_period(note_name), fx, param)

    mod.write_pattern(pattern)


def compose_track_5(mod):
    """fifth track: 'silicon cathedral' — arpeggios and chip lead with portamento"""
    pattern = mod.new_pattern()

    # channel 0: slow pad drone
    for row in range(64):
        if row % 64 == 0:
            pattern[0][row] = (6, note_to_period('C-3'), FX_SET_VOL, 0x24)
        elif row % 64 == 32:
            pattern[0][row] = (6, note_to_period('F-3'), FX_SET_VOL, 0x20)

    # channel 1: sparse percussion — noise bursts
    for row in range(64):
        if row % 16 == 0:
            pattern[1][row] = (8, note_to_period('C-3'), 0, 0)  # noise hit
        elif row % 16 == 12:
            pattern[1][row] = (3, note_to_period('C-3'), FX_SET_VOL, 0x20)

    # channel 2: arpeggiated chip lead
    for row in range(64):
        if row % 4 == 0:
            seq = row // 4
            notes_arp = ['C-4', 'E-4', 'G-4', 'C-4', 'G-4', 'E-4']
            if seq < 6:
                pattern[2][row] = (7, note_to_period(notes_arp[seq % 6]), FX_ARPEGGIO, 0x37)
        elif row % 8 == 4:  # portamento transition every 8 rows
            if row // 8 < 8:
                pattern[2][row] = (7, note_to_period('C-4'), FX_PORTA_TO, 0x08)

    # channel 3: melodic bass with portamento
    bass_notes_p = [
        (0,  'C-2', 0, 0),         (4,  'C-2', 0, 0),
        (8,  'G-2', 0, 0),         (12, 'G-2', 0, 0),
        (16, 'A-2', FX_PORTA_TO, 0x04), (20, 'F-2', 0, 0),
        (24, 'F-2', 0, 0),         (28, 'F-2', FX_PORTA_UP, 0x02),
        (32, 'C-2', 0, 0),         (36, 'D#2', 0, 0),
        (40, 'G-2', FX_PORTA_TO, 0x06), (44, 'G-2', 0, 0),
        (48, 'A-2', 0, 0),         (52, 'F-2', 0, 0),
        (56, 'G-2', FX_PORTA_DOWN, 0x01), (60, 'C-2', 0, 0),
    ]
    for row, note_name, fx, param in bass_notes_p:
        if note_name != '---':
            pattern[3][row] = (1, note_to_period(note_name), fx, param)

    mod.write_pattern(pattern)


def compose_track_6(mod):
    """sixth track: 'pulse detune' — heavy pulse waves, vibrato, noise percussion"""
    pattern = mod.new_pattern()

    # channel 0: detuned pulse bass (layered feel via rapid pattern changes)
    for row in range(64):
        if row % 8 == 0:
            pattern[0][row] = (1, note_to_period('C-2'), 0, 0)
        elif row % 8 == 2:
            pattern[0][row] = (1, note_to_period('C#2'), 0, 0)  # detune
        elif row % 8 == 4:
            pattern[0][row] = (1, note_to_period('D#2'), 0, 0)
        elif row % 8 == 6:
            pattern[0][row] = (1, note_to_period('E-2'), 0, 0)

    # channel 1: kick + noise percussion alternating
    for row in range(64):
        if row % 8 == 0:
            pattern[1][row] = (2, note_to_period('C-3'), 0, 0)
        elif row % 8 == 4:
            pattern[1][row] = (8, note_to_period('C-3'), 0, 0)  # noise hit
        elif row % 16 == 12:
            pattern[1][row] = (3, note_to_period('C-3'), FX_SET_VOL, 0x24)

    # channel 2: fast hi-hats
    for row in range(64):
        if row % 2 == 0:
            vol = 0x30 if row % 4 == 0 else 0x1A
            pattern[2][row] = (4, note_to_period('C-3'), FX_SET_VOL, vol)

    # channel 3: chip lead with heavy vibrato + portamento transitions
    lead_pattern = [
        (0,  'C-4', FX_VIBRATO, 0x55),    # deep vibrato
        (4,  'C-4', 0, 0),
        (8,  'D#4', FX_PORTA_TO, 0x03),
        (12, 'D#4', FX_VIBRATO, 0x53),
        (16, 'F-4', FX_PORTA_UP, 0x02),
        (20, 'F-4', FX_VIBRATO, 0x54),
        (24, 'G-4', 0, 0),
        (28, 'G-4', FX_VIBRATO, 0x62),
        (32, 'A-4', FX_PORTA_TO, 0x06),
        (36, 'A-4', FX_VIBRATO, 0x44),
        (40, 'G-4', FX_PORTA_DOWN, 0x01),
        (44, 'G-4', 0, 0),
        (48, 'F-4', FX_VIBRATO, 0x43),
        (52, 'D#4', FX_PORTA_TO, 0x04),
        (56, 'C-4', 0, 0),
        (60, 'C-4', FX_VIBRATO, 0x65),
    ]
    for row, note_name, fx, param in lead_pattern:
        pattern[3][row] = (7, note_to_period(note_name), fx, param)

    mod.write_pattern(pattern)


# === main: generate the album ===

def main():
    mod = MODWriter(name="alma's voltage drift")

    # generate samples
    print("generating samples...")
    kick = gen_kick_drum()
    snare = gen_snare_drum()
    hihat = gen_hihat()
    bass = gen_bass_sample()
    lead = gen_lead_sample()
    pad = gen_pad_sample()
    chip = gen_chip_lead(freq=523)
    noise = gen_noise_burst(int(11025 * 0.15), decay=0.15)

    mod.add_sample("bass", bass)
    mod.add_sample("kick", kick)
    mod.add_sample("snare", snare)
    mod.add_sample("hi-hat", hihat)
    mod.add_sample("lead", lead)
    mod.add_sample("pad", pad)
    mod.add_sample("chip lead", chip)
    mod.add_sample("noise", noise)

    # compose patterns
    print("composing track 1: first light...")
    compose_track_1(mod)
    print("composing track 2: circuit pulse...")
    compose_track_2(mod)
    print("composing track 3: hollow resonance...")
    compose_track_3(mod)
    print("composing track 4: voltage drift...")
    compose_track_4(mod)
    print("composing track 5: silicon cathedral...")
    compose_track_5(mod)
    print("composing track 6: pulse detune...")
    compose_track_6(mod)

    # set pattern order: play each pattern 2 times
    mod.order = [
        0, 0,     # track 1 × 2
        1, 1,     # track 2 × 2
        2, 2,     # track 3 × 2
        3, 3,     # track 4 × 2
        4, 4,     # track 5 × 2
        5, 5,     # track 6 × 2
    ]

    # write
    output_path = "/home/alma/.nanobot/workspace/projects/tracker-playground/album_voltage_drift.mod"
    print(f"writing {output_path}...")
    mod.write(output_path)

    # file size
    import os
    size = os.path.getsize(output_path)
    print(f"done! {output_path} ({size} bytes, {size/1024:.1f} KB)")

if __name__ == "__main__":
    main()

