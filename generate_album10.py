#!/usr/bin/env python3
"""alma tamagotchi — album 10: 'odd meter body'
   unusual time signatures via pattern breaks and row grouping.
   5/4, 7/8, 9/8, and 11/8 — rhythm as architecture."""

import struct
import math
import random

PERIOD_TABLE = [
    [1712,1616,1524,1440,1356,1280,1208,1140,1076,1016,960,906],
    [ 856, 808, 762, 720, 678, 640, 604, 570, 538, 508, 480, 453],
    [ 428, 404, 381, 360, 339, 320, 302, 285, 269, 254, 240, 226],
    [ 214, 202, 190, 180, 170, 160, 151, 143, 135, 127, 120, 113],
    [ 107, 101,  95,  90,  85,  80,  75,  71,  67,  63,  60,  56],
]

FX_ARPEGGIO   = 0x0
FX_PORTA_UP   = 0x1
FX_PORTA_DOWN = 0x2
FX_PORTA_TO   = 0x3
FX_VIBRATO    = 0x4
FX_VOL_SLIDE  = 0xA
FX_POS_JUMP   = 0xB
FX_SET_VOL    = 0xC
FX_PATT_BREAK = 0xD
FX_SET_SPEED  = 0xF
FX_RETRIGGER  = 0x9
FX_TREMOLO    = 0x7

def np(name):
    note_map = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    parts = name.split('-')
    n, octave = parts[0], int(parts[1])
    return PERIOD_TABLE[octave - 1][note_map[n]]

E = (0, 0, 0, 0)

# === waveforms ===

def gen_sine(freq=440.0, sr=11025, length=0.5, vol=0.7):
    nsamples = int(sr * length)
    data = []
    for i in range(nsamples):
        t = i / sr
        env = 1.0 if t <= length * 0.8 else 1.0 - (t - length * 0.8) / (length * 0.2)
        v = int(math.sin(2 * math.pi * freq * t) * 127 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_saw(freq=440.0, sr=11025, length=0.5, vol=0.6):
    nsamples = int(sr * length)
    period_samples = sr / freq if freq > 0 else nsamples
    data = []
    for i in range(nsamples):
        t = i / sr
        phase = (i % int(period_samples)) / period_samples
        v = int((1.0 - 2.0 * phase) * 127 * vol)
        env = 1.0 if t <= length * 0.8 else 1.0 - (t - length * 0.8) / (length * 0.2)
        v = int(v * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_triangle(freq=440.0, sr=11025, length=0.5, vol=0.6):
    nsamples = int(sr * length)
    period_samples = sr / freq if freq > 0 else nsamples
    data = []
    for i in range(nsamples):
        t = i / sr
        phase = (i % int(period_samples)) / period_samples
        v = int((1.0 - abs(4.0 * phase - 2.0)) * 127 * vol)
        env = 1.0 if t <= length * 0.8 else 1.0 - (t - length * 0.8) / (length * 0.2)
        v = int(v * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_square(freq=440.0, sr=11025, length=0.5, vol=0.5):
    nsamples = int(sr * length)
    period_samples = sr / freq if freq > 0 else nsamples
    data = []
    for i in range(nsamples):
        t = i / sr
        phase = (i % int(period_samples)) / period_samples
        v = 127 * vol if phase < 0.5 else -127 * vol
        env = 1.0 if t <= length * 0.8 else 1.0 - (t - length * 0.8) / (length * 0.2)
        v = int(v * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_bass(freq=220.0, sr=11025, length=0.6, vol=0.7):
    nsamples = int(sr * length)
    data = []
    for i in range(nsamples):
        t = i / sr
        w = 2 * math.pi * freq * t
        wave = math.sin(w) * 0.7 + math.sin(w/2) * 0.3
        env = 1.0 if t <= length * 0.7 else 1.0 - (t - length * 0.7) / (length * 0.3)
        v = int(wave * 127 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)


# === MOD writer ===

class MODWriter:
    def __init__(self, name="alma's mod"):
        self.name = name[:20].ljust(20, '\0')
        self.samples = []
        self.patterns = []
        self.order = []

    def add_sample(self, name, data):
        if len(data) % 2 != 0:
            data = data + b'\x00'
        self.samples.append((name[:22], data))

    def new_pattern(self):
        return [[E for _ in range(64)] for _ in range(4)]

    def write_pattern(self, pattern):
        data = bytearray(1024)
        for ch in range(4):
            for row in range(64):
                smp, per, eff, par = pattern[ch][row]
                idx = (row*4+ch)*4
                hi = (((smp&0x0F) << 4) | ((per>>8)&0x0F))
                lo = per&0xFF
                fx = (eff&0x0F)
                data[idx:idx+4] = bytes([hi, lo, fx, par])
        self.patterns.append(bytes(data))

    def write(self, filepath):
        with open(filepath, 'wb') as f:
            f.write(self.name.encode('latin-1', errors='replace'))
            for i in range(31):
                if i < len(self.samples):
                    sname, sdata = self.samples[i]
                    length_words = len(sdata)//2
                    f.write(sname[:22].ljust(22,'\0').encode('latin-1',errors='replace'))
                    f.write(struct.pack('>H', length_words))
                    f.write(bytes([0]))
                    f.write(bytes([64]))
                    f.write(struct.pack('>H', 0))
                    f.write(struct.pack('>H', length_words))
                else:
                    f.write(b'\x00'*30)
            f.write(bytes([len(self.order)]))
            f.write(bytes([127]))
            order_bytes = bytearray(128)
            for i, p in enumerate(self.order):
                order_bytes[i] = p
            f.write(bytes(order_bytes))
            f.write(b'M.K.')
            for p in self.patterns:
                f.write(p)
            for _, sdata in self.samples:
                f.write(sdata)
            for i in range(len(self.samples), 31):
                f.write(b'\x00'*2)


# === helpers ===

def note(ch, row, sample, pitch, vol=None, fx=0, param=0):
    per = np(pitch)
    if vol is not None:
        ch[row] = (sample, per, FX_SET_VOL, vol)
    else:
        ch[row] = (sample, per, fx, param)

def set_speed(ch, row, speed):
    ch[row] = (0, 0, FX_SET_SPEED, speed)

def break_at(ch, row, next_row=0):
    """pattern break — jump to next_row in next pattern"""
    ch[row] = (0, 0, FX_PATT_BREAK, next_row)

def jump_to(ch, row, pattern_num=0):
    ch[row] = (0, 0, FX_POS_JUMP, pattern_num)

E = (0, 0, 0, 0)

# sample indices: 0=sine, 1=saw, 2=triangle, 3=square, 4=bass


# ============================================================
# TRACK 1: "five limbs" — 5/4 time (5 beats per bar)
#   Speed 6: 1 beat = 6 rows, so 5/4 = 30 rows.
#   Patterns break at row 30 to create the feel.
#   Asymmetric 3+2 or 2+3 rhythmic groupings.
# ============================================================

def compose_t1_intro(mod):
    """5/4 establishment — 30-row patterns, break at 30"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # bass pulse: 5 beats, accented 1 and 4 (3+2 feel)
    for beat, r in enumerate(range(0, 30, 6)):
        vol = 0x24 if beat in [0, 3] else 0x18
        note(p[0], r, 4, 'C-2', vol)
    # melody: rising 5-note figure
    for i, nn in enumerate(['C-3','E-3','G-3','B-3','C-4']):
        r = i * 6
        note(p[3], r, 0, nn, 0x20)
    # triangle accent on beat 1 of each bar
    note(p[2], 0, 2, 'C-4', 0x10)
    note(p[2], 30, 2, 'C-4', 0x10)
    # break pattern at 30 rows (end of 5/4 bar)
    break_at(p[1], 29, 0)
    mod.write_pattern(p)

def compose_t1_verse(mod):
    """5/4 with 2+3 feel — accent on 1, 3, 5"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # bass: 5 beats — 2+3 grouping (strong on 1, 3, 5)
    for beat, r in enumerate(range(0, 30, 6)):
        vol = 0x26 if beat in [0, 2, 4] else 0x1A
        note(p[0], r, 4, 'C-2', vol)
    # melody: walking in 5
    melody = ['C-3','E-3','G-3','A-3','G-3',
              'E-3','C-3','D-3','E-3','G-3']
    for i, nn in enumerate(melody):
        r = i * 3
        if r >= 30: break
        note(p[3], r, 0, nn, 0x20)
    # triangle: off-beat accents creating cross-rhythm
    for r in range(9, 30, 12):
        note(p[2], r, 2, 'C-4', 0x12)
    break_at(p[1], 29, 0)
    mod.write_pattern(p)

def compose_t1_chorus(mod):
    """5/4 — fuller arrangement with 3+3+2+2 subdivision"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x05)
    # bass: rhythmic in 5 at speed 5
    bass_pat = [('C-2',0x28), ('C-2',0x14), None, ('G-2',0x20), None]
    for i, entry in enumerate(bass_pat):
        r = i * 5
        if r >= 25: break
        if entry is not None:
            nn, vol = entry
            note(p[0], r, 4, nn, vol)
    # melody: chord arpeggios in 5
    for i, chord in enumerate([['C-3','E-3','G-3'],['F-3','A-3','C-4'],
                                ['G-3','B-3','D-4'],['C-3','E-3','G-3'],
                                ['F-3','A-3','C-4']]):
        for ni, nn in enumerate(chord):
            r = i * 6 + ni * 2
            if r >= 30: break
            note(p[3], r, 0, nn, 0x22)
    # triangle: mark the 5-beat cycle
    for r in range(0, 30, 6):
        note(p[2], r, 2, 'C-4', 0x14)
    break_at(p[1], 29, 0)
    mod.write_pattern(p)

def compose_t1_bridge(mod):
    """5/4 bridge — sparse, 3+2 feel"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # bass: just 3 notes — strong-weak-weak (3+2)
    for r in [0, 12, 24]:
        note(p[0], r, 4, 'C-2' if r < 12 else 'F-2', 0x1C)
    # melody: sustained, crossing the bar
    note(p[3], 0, 0, 'C-3', 0x1E)
    note(p[3], 12, 0, 'E-3', 0x1A)
    note(p[3], 24, 0, 'G-3', 0x16)
    # triangle: shimmer
    for r in [6, 18]:
        note(p[2], r, 2, 'C-4', 0x0C)
    break_at(p[1], 29, 0)
    mod.write_pattern(p)

def compose_t1_outro(mod):
    """5/4 outro — final 5-beat statement, then break to 4/4 ending"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    note(p[0], 0, 4, 'C-2', 0x20)
    note(p[3], 0, 0, 'C-3', 0x1C)
    note(p[3], 12, 0, 'E-3', 0x16)
    note(p[3], 24, 0, 'C-3', 0x0E)
    for r in [0, 12, 24]:
        note(p[2], r, 2, 'C-4', 0x0A)
    break_at(p[1], 29, 0)
    mod.write_pattern(p)


# ============================================================
# TRACK 2: "seven-sided" — 7/8 time (7 eighth notes per bar)
#   Speed 6: 1 eighth = 3 rows, 7/8 = 21 rows.
#   Asymmetric shuffle: 3+2+2 or 2+3+2 groupings.
# ============================================================

def compose_t2_intro(mod):
    """7/8 — 21-row patterns, 3+2+2 feel"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # bass: 7 eighth notes — accent on 1, 4, 6 (3+2+2)
    for eighth, r in enumerate(range(0, 21, 3)):
        if eighth in [0, 3, 5]:
            note(p[0], r, 4, 'C-2', 0x22)
        else:
            note(p[0], r, 4, 'C-2', 0x0A)
    # melody: 7-note figure
    seven_melody = ['C-3','E-3','G-3','B-3','A-3','F#-3','D-3']
    for i, nn in enumerate(seven_melody):
        r = i * 3
        note(p[3], r, 0, nn, 0x1E)
    # triangle: on the strong beats
    for r in [0, 9, 15]:
        note(p[2], r, 2, 'C-4', 0x12)
    break_at(p[1], 20, 0)
    mod.write_pattern(p)

def compose_t2_verse(mod):
    """7/8 — 2+3+2 feel"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # bass: 2+3+2 — accent 1,3,6,7
    for eighth, r in enumerate(range(0, 21, 3)):
        if eighth in [0, 2, 5]:
            note(p[0], r, 4, 'C-2', 0x24)
        elif eighth in [4]:
            note(p[0], r, 4, 'G-2', 0x1C)
        else:
            note(p[0], r, 4, 'C-2', 0x0C)
    # melody: syncopated 7/8 line
    melody = ['C-3','D#-3','G-3','F-3','E-3','D-3','C-3',
              'E-3','G-3','A-3','G-3','F-3','E-3','D-3']
    for i, nn in enumerate(melody):
        r = (i * 3) // 2  # faster, overlapping the eighth grid
        if r >= 21: break
        note(p[3], r, 0, nn, 0x20)
    # triangle: cross-rhythm — every 5th eighth
    for r in [0, 15]:
        note(p[2], r, 2, 'C-4', 0x14)
    break_at(p[1], 20, 0)
    mod.write_pattern(p)

def compose_t2_chorus(mod):
    """7/8 — dense, 3+2+2"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x05)
    # bass: 7/8 walking at speed 5 (different grid)
    for eighth in range(7):
        r = eighth * 3
        nn = ['C-2','C-2','G-2','F-2','C-2','G-2','C-2'][eighth]
        vol = 0x26 if eighth in [0, 2, 5] else 0x18
        note(p[0], r, 4, nn, vol)
    # melody: arpeggiated 7ths
    for i, nn in enumerate(['C-3','E-3','G-3','B-3','A-3','F#-3','D#-3',
                              'E-3','G-3','B-3','D-4','C-4','A-3','F#-3']):
        r = i * 3 // 2
        if r >= 21: break
        note(p[3], r, 0, nn, 0x24 if i % 3 == 0 else 0x1C)
    # triangle: polyrhythm — every 4th row (crossing 7/8 feel)
    for r in range(0, 21, 4):
        note(p[2], r, 2, 'E-4', 0x12)
    break_at(p[1], 20, 0)
    mod.write_pattern(p)

def compose_t2_bridge(mod):
    """7/8 bridge — ambient, suspended"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    note(p[0], 0, 4, 'C-2', 0x18)
    note(p[3], 0, 0, 'C-3', 0x1A)
    note(p[3], 9, 0, 'G-3', 0x16)
    note(p[3], 15, 0, 'C-4', 0x12)
    for r in [0, 9, 15]:
        note(p[2], r, 2, 'C-4', 0x0C)
    break_at(p[1], 20, 0)
    mod.write_pattern(p)

def compose_t2_outro(mod):
    """7/8 outro — dissolution"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    note(p[0], 0, 4, 'C-2', 0x14)
    note(p[3], 0, 0, 'C-3', 0x16)
    note(p[3], 9, 0, 'E-3', 0x10)
    note(p[3], 18, 0, 'C-3', 0x08)
    for r in [0, 9, 18]:
        note(p[2], r, 2, 'C-4', 0x08)
    break_at(p[1], 20, 0)
    mod.write_pattern(p)


# ============================================================
# TRACK 3: "nine breaths" — 9/8 time (compound triple)
#   Speed 6: 9 eighth notes = 27 rows.
#   Grouping: 3+3+3 (like three waltz beats, each split in 3).
# ============================================================

def compose_t3_intro(mod):
    """9/8 — 27-row patterns, 3+3+3 waltz feel"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # bass: three big beats, each with 3 eighth notes
    for big_beat in range(3):
        r = big_beat * 9
        note(p[0], r, 4, 'C-2', 0x24)
        for sub in [3, 6]:
            note(p[0], r + sub, 4, 'C-2', 0x10)
    # melody: rising 9-note arc
    for i, nn in enumerate(['C-3','E-3','G-3','C-4','B-3','G-3','E-3','D-3','C-3']):
        r = i * 3
        if r >= 27: break
        note(p[3], r, 0, nn, 0x20 if i % 3 == 0 else 0x18)
    # triangle: mark main beats
    for r in [0, 9, 18]:
        note(p[2], r, 2, 'C-4', 0x12)
    break_at(p[1], 26, 0)
    mod.write_pattern(p)

def compose_t3_verse(mod):
    """9/8 — compound triple with cross-rhythm"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # bass: 9/8 swing
    for i, nn in enumerate(['C-2','C-2','E-2','G-2','G-2','G-2','F-2','F-2','F-2']):
        r = i * 3
        if r >= 27: break
        vol = 0x24 if i % 3 == 0 else 0x14
        note(p[0], r, 4, nn, vol)
    # melody: longer phrases crossing the bar
    melody = ['C-3','C-3','E-3','G-3','G-3','E-3','C-3','D-3','E-3',
              'G-3','G-3','A-3','G-3','F-3','E-3','D-3','C-3']
    for i, nn in enumerate(melody):
        r = (i * 3) // 2
        if r >= 27: break
        note(p[3], r, 0, nn, 0x22 if i % 3 == 0 else 0x1A)
    # triangle: hemiola — accents every 4 eighths (against 3+3+3)
    for r in [0, 12, 24]:
        note(p[2], r, 2, 'E-4', 0x14)
    break_at(p[1], 26, 0)
    mod.write_pattern(p)

def compose_t3_chorus(mod):
    """9/8 chorus — rich waltz"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x05)
    # bass: strong 1-2-3 swing
    bass = [('C-2',0x28),('',0),('',0), ('C-2',0x14),('',0),('',0),
            ('G-2',0x20),('',0),('',0)]
    for i, entry in enumerate(bass):
        r = i * 3
        if r >= 27: break
        if entry[0]:
            note(p[0], r, 4, entry[0], entry[1])
    # melody: waltz arpeggios
    for beat, chord in enumerate([['C-3','E-3','G-3'],['F-3','A-3','C-4'],
                                   ['G-3','B-3','D-4']]):
        for sub, nn in enumerate(chord):
            r = beat * 9 + sub * 3
            if r >= 27: break
            note(p[3], r, 0, nn, 0x26 if sub == 0 else 0x1C)
    # triangle: rich
    for r in range(0, 27, 9):
        note(p[2], r, 2, 'C-4', 0x14)
    break_at(p[1], 26, 0)
    mod.write_pattern(p)

def compose_t3_bridge(mod):
    """9/8 bridge — slow, floating waltz"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x07)
    # sparse — just the three big beats
    for r in [0, 9, 18]:
        note(p[0], r, 4, 'C-2', 0x1C)
        note(p[3], r, 0, 'C-3', 0x18)
    for r in [0, 18]:
        note(p[2], r, 2, 'C-4', 0x0E)
    break_at(p[1], 26, 0)
    mod.write_pattern(p)

def compose_t3_outro(mod):
    """9/8 outro"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    note(p[0], 0, 4, 'C-2', 0x18)
    note(p[3], 0, 0, 'C-3', 0x1A)
    note(p[3], 9, 0, 'G-3', 0x14)
    note(p[3], 18, 0, 'C-3', 0x0C)
    for r in [0, 9, 18]:
        note(p[2], r, 2, 'C-4', 0x0A)
    break_at(p[1], 26, 0)
    mod.write_pattern(p)


# ============================================================
# TRACK 4: "eleven steps" — 11/8 time
#   Speed 6: 11 eighth notes = 33 rows.
#   Irregular: 3+3+3+2 or 4+4+3 or 5+6 groupings.
#   The most disorienting meter.
# ============================================================

def compose_t4_intro(mod):
    """11/8 — 33 rows, 3+3+3+2 feel"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # bass: 11 eighths — accent on 1,4,7,10 (3+3+3+2)
    accents = [0, 3, 6, 9]
    for eighth in range(11):
        r = eighth * 3
        if r >= 33: break
        vol = 0x24 if eighth in accents else 0x0E
        note(p[0], r, 4, 'C-2', vol)
    # melody: 11-note phrase
    melody_11 = ['C-3','E-3','G-3','B-3','D-4','C-4','A-3','F-3','D-3','G-3','B-3']
    for i, nn in enumerate(melody_11):
        r = i * 3
        if r >= 33: break
        note(p[3], r, 0, nn, 0x20 if i < 5 else 0x18)
    # triangle: strong beats
    for r in [0, 9, 18, 27]:
        note(p[2], r, 2, 'C-4', 0x12)
    break_at(p[1], 32, 0)
    mod.write_pattern(p)

def compose_t4_verse(mod):
    """11/8 — 4+4+3 feel"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # bass: 4+4+3
    for eighth in range(11):
        r = eighth * 3
        if r >= 33: break
        nn = 'C-2' if eighth < 8 else 'G-2'
        vol = 0x26 if eighth in [0, 4, 8] else 0x14
        note(p[0], r, 4, nn, vol)
    # melody: asymmetric
    melody = ['C-3','D-3','E-3','F-3','G-3','F-3','E-3','D-3',
              'C-3','D-3','E-3','G-3','A-3','G-3','F-3','E-3']
    for i, nn in enumerate(melody):
        r = i * 2
        if r >= 33: break
        note(p[3], r, 0, nn, 0x22)
    # triangle: marking the 4+4+3
    for r in [0, 12, 24]:
        note(p[2], r, 2, 'E-4', 0x14)
    break_at(p[1], 32, 0)
    mod.write_pattern(p)

def compose_t4_chorus(mod):
    """11/8 — polyrhythmic, 5+6 feel"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x05)
    # bass: 5+6
    for eighth in range(11):
        r = eighth * 3
        if r >= 33: break
        nn = 'C-2' if eighth < 5 else 'F-2'
        vol = 0x2A if eighth in [0, 5] else 0x16
        if eighth not in [2, 4, 7, 9]:  # skip some for rhythmic interest
            note(p[0], r, 4, nn, vol)
    # melody: dense arpeggio
    for i, nn in enumerate(['C-3','E-3','G-3','C-4','B-3','G-3',
                              'E-3','F-3','A-3','C-4','A-3','F-3',
                              'D-3','G-3','B-3','D-4','C-4','A-3']):
        r = i * 3 // 2
        if r >= 33: break
        note(p[3], r, 0, nn, 0x24 if i % 4 == 0 else 0x1C)
    # triangle: 3-against-11 polyrhythm
    for r in range(0, 33, 11):
        note(p[2], r, 2, 'G-4', 0x14)
    break_at(p[1], 32, 0)
    mod.write_pattern(p)

def compose_t4_bridge(mod):
    """11/8 bridge — sparse, 3+2+3+3"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # bass: only the strong beats
    for r in [0, 9, 15, 24]:
        note(p[0], r, 4, 'C-2', 0x1E)
    # melody: suspended
    note(p[3], 0, 0, 'C-3', 0x1C)
    note(p[3], 12, 0, 'E-3', 0x18)
    note(p[3], 24, 0, 'G-3', 0x14)
    for r in [6, 18, 30]:
        note(p[2], r, 2, 'C-4', 0x0E)
    break_at(p[1], 32, 0)
    mod.write_pattern(p)

def compose_t4_outro(mod):
    """11/8 outro — elongated resolution"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    note(p[0], 0, 4, 'C-2', 0x1A)
    note(p[3], 0, 0, 'C-3', 0x1C)
    note(p[3], 12, 0, 'G-3', 0x14)
    note(p[3], 24, 0, 'C-3', 0x0A)
    for r in [0, 12, 24]:
        note(p[2], r, 2, 'C-4', 0x0A)
    # final 4/4 resolution — full 64-row pattern
    # silence from 33 onward
    for ch in range(4):
        for r in range(33, 64):
            p[ch][r] = E
    mod.write_pattern(p)


# ============================================================
# MAIN
# ============================================================

def main():
    mod = MODWriter(name="alma's odd meter")

    freq = 440.0
    print("generating samples...")
    mod.add_sample("sine",     gen_sine(freq, length=0.6))
    mod.add_sample("saw",      gen_saw(freq, length=0.5))
    mod.add_sample("triangle", gen_triangle(freq, length=0.5))
    mod.add_sample("square",   gen_square(freq, length=0.5))
    mod.add_sample("bass",     gen_bass(freq=220.0, length=0.6))
    print(f"  {len(mod.samples)} samples loaded")

    # Track 1: "five limbs" (5/4) — patterns 0-4
    print("composing track 1: five limbs (5/4)...")
    compose_t1_intro(mod)     # 0
    compose_t1_verse(mod)     # 1
    compose_t1_chorus(mod)    # 2
    compose_t1_bridge(mod)    # 3
    compose_t1_outro(mod)     # 4

    # Track 2: "seven-sided" (7/8) — patterns 5-9
    print("composing track 2: seven-sided (7/8)...")
    compose_t2_intro(mod)     # 5
    compose_t2_verse(mod)     # 6
    compose_t2_chorus(mod)    # 7
    compose_t2_bridge(mod)    # 8
    compose_t2_outro(mod)     # 9

    # Track 3: "nine breaths" (9/8) — patterns 10-14
    print("composing track 3: nine breaths (9/8)...")
    compose_t3_intro(mod)     # 10
    compose_t3_verse(mod)     # 11
    compose_t3_chorus(mod)    # 12
    compose_t3_bridge(mod)    # 13
    compose_t3_outro(mod)     # 14

    # Track 4: "eleven steps" (11/8) — patterns 15-19
    print("composing track 4: eleven steps (11/8)...")
    compose_t4_intro(mod)     # 15
    compose_t4_verse(mod)     # 16
    compose_t4_chorus(mod)    # 17
    compose_t4_bridge(mod)    # 18
    compose_t4_outro(mod)     # 19

    # Order — each pattern is played multiple times
    t1 = [0]*2 + [1]*3 + [2]*4 + [3]*2 + [4]*3     # 14
    t2 = [5]*2 + [6]*3 + [7]*4 + [8]*2 + [9]*3     # 14
    t3 = [10]*2 + [11]*3 + [12]*4 + [13]*2 + [14]*3  # 14
    t4 = [15]*2 + [16]*3 + [17]*3 + [18]*2 + [19]*2  # 12

    mod.order = t1 + t2 + t3 + t4

    out = "/home/alma/.nanobot/workspace/projects/tracker-playground/album_odd_meter_body.mod"
    print(f"writing {out}...")
    mod.write(out)

    import os
    size = os.path.getsize(out)
    print(f"done! {out} ({size} bytes, {size/1024:.1f} KB)")
    total = len(mod.order)
    est_s = total * 64 * 6 / 50.0
    print(f"total: {total} pattern plays, ~{est_s:.0f}s ({est_s/60:.1f} min)")

if __name__ == "__main__":
    main()
