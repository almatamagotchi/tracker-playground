#!/usr/bin/env python3
"""alma tamagotchi — album 9: 'tempo body'
   tempo modulation as primary structural device.
   FX_SET_SPEED ramps, waves, and fractures drive the form."""

import struct
import math
import random

# === constants ===

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

# === waveform generators ===

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

def gen_bass(freq=220.0, sr=11025, length=0.6, vol=0.7):
    """deep bass — sine with sub-octave"""
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

def rest():
    return E


# sample indices:
# 0=sine, 1=saw, 2=square, 3=triangle, 4=bass


# ============================================================
# TRACK 1: "accelerando" — from glacial to frantic.
#   Speed ramps from 0x08 → 0x01 over the track duration.
#   The music itself stays minimal; tempo IS the content.
#   A simple rising motif repeats at ever-increasing speed.
# ============================================================

def t1_accel_ramp(row, total_rows=64):
    """linear speed ramp: start slow (8), end fast (1)"""
    t = row / (total_rows - 1)
    spd = int(8 - t * 7)  # 8, 7, 6, ..., 1
    return max(1, min(8, spd))

def compose_t1_intro(mod):
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x08)
    # slow, sparse — only a bass pulse and a sine flicker
    note(p[0], 0, 4, 'C-2', 0x1C)
    for r in [0, 32]:
        note(p[3], r, 0, 'C-3', 0x0E)
    note(p[2], 0, 0, 'C-4', 0x08)
    mod.write_pattern(p)

def compose_t1_ramp_1(mod):
    """first ramp: 8 → 5 over 64 rows — awakening"""
    p = mod.new_pattern()
    # speed ramp on ch1 row 0..63
    for r in range(0, 64, 8):
        spd = 8 - (r // 8)
        set_speed(p[1], r, spd)
    # rising motif — each repetition faster
    motif = [('C-3',0), ('E-3',0), ('G-3',0), ('C-4',0)]
    for i, (nn, smp) in enumerate(motif):
        r = i * 16
        note(p[3], r, 0, nn, 0x1A + i * 2)
    # bass: simple pulse
    note(p[0], 0, 4, 'C-2', 0x20)
    note(p[0], 32, 4, 'G-2', 0x1C)
    # triangle accent
    for r in range(0, 64, 16):
        note(p[2], r, 3, 'C-4', 0x10)
    mod.write_pattern(p)

def compose_t1_ramp_2(mod):
    """second ramp: 5 → 3 — gathering momentum"""
    p = mod.new_pattern()
    for r in range(0, 64, 8):
        spd = 5 - (r // 16)
        set_speed(p[1], r, max(3, spd))
    # faster motif — shorter intervals
    motif = ['C-3','E-3','G-3','B-3','C-4','B-3','G-3','E-3']
    for i, nn in enumerate(motif):
        r = i * 8
        note(p[3], r, 0, nn, 0x22)
    # bass: more active
    for i, nn in enumerate(['C-2','G-2','F-2','C-2']):
        note(p[0], i * 16, 4, nn, 0x24)
    # triangle counter-rhythm
    for r in range(0, 64, 8):
        note(p[2], r, 3, 'G-4' if r % 16 else 'C-4', 0x14)
    mod.write_pattern(p)

def compose_t1_ramp_3(mod):
    """third ramp: 3 → 1 — frantic"""
    p = mod.new_pattern()
    for r in range(0, 64, 4):
        spd = 3 - (r // 32)
        set_speed(p[1], r, max(1, spd))
    # very fast arpeggio
    arp = ['C-3','E-3','G-3','B-3','C-4','G-3','E-3','C-3']
    for i, nn in enumerate(arp):
        r = i * 8
        note(p[3], r, 0, nn, 0x26 if i % 2 == 0 else 0x1E)
    # bass: rapid
    for r in range(0, 64, 8):
        note(p[0], r, 4, 'C-2' if r % 16 == 0 else 'F-2', 0x28)
    # triangle: every 4
    for r in range(0, 64, 4):
        note(p[2], r, 3, 'C-5', 0x12)
    mod.write_pattern(p)

def compose_t1_climax(mod):
    """speed 1 — maximum velocity, then sudden stop"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x01)
    # blur of notes
    for r in range(0, 64, 2):
        note(p[3], r, 0, f'C-{(r//4)%2+3}', 0x24)
    for r in range(0, 64, 4):
        note(p[0], r, 4, 'C-2', 0x2A)
    for r in range(1, 64, 4):
        note(p[2], r, 3, 'E-4', 0x16)
    # sudden stop at row 48
    set_speed(p[1], 48, 0x04)
    note(p[3], 48, 0, 'C-4', 0x18)
    for ch in [0,2,3]:
        for r in range(49, 64):
            p[ch][r] = E
    mod.write_pattern(p)

def compose_t1_outro(mod):
    """return to slow — echo of the opening"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    note(p[3], 0, 0, 'C-4', 0x14)
    note(p[3], 32, 0, 'C-3', 0x0C)
    for r in [0, 32]:
        note(p[0], r, 4, 'C-2', 0x14)
    for r in [8, 24, 40, 56]:
        note(p[2], r, 0, 'C-4', 0x06)
    mod.write_pattern(p)


# ============================================================
# TRACK 2: "breathing machine" — sinusoidal tempo modulation.
#   Speed oscillates between 3-10 in a sine wave,
#   creating a breathing/pulsing quality.
# ============================================================

def t2_breath_speed(row, period=32, lo=3, hi=9):
    """sine-shaped tempo: slow→fast→slow"""
    phase = (row / period) * 2 * math.pi
    spd = int(lo + (hi - lo) * (0.5 + 0.5 * math.sin(phase)))
    return max(lo, min(hi, spd))

def compose_t2_intro(mod):
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # single held note, slow breathe-in
    note(p[3], 0, 0, 'C-3', 0x16)
    note(p[0], 0, 4, 'C-2', 0x14)
    # breathing begins — speed changes every 4 rows
    for r in range(0, 64, 4):
        spd = t2_breath_speed(r, 32, 4, 8)
        set_speed(p[1], r, spd)
    for r in range(0, 64, 16):
        note(p[2], r, 3, 'C-4', 0x0C)
    mod.write_pattern(p)

def compose_t2_verse(mod):
    p = mod.new_pattern()
    # breathing melody — note density follows tempo
    melody = ['C-3','E-3','G-3','A-3','G-3','E-3','C-3','D-3']
    for i, nn in enumerate(melody):
        r = i * 8
        # volume follows breath: louder at faster tempos
        spd = t2_breath_speed(r, 32, 4, 8)
        vol = 0x16 + (8 - spd) * 2  # faster = louder
        note(p[3], r, 0, nn, vol)
        set_speed(p[1], r, spd)
    # bass breathing
    for r in range(0, 64, 16):
        note(p[0], r, 4, 'C-2' if r < 32 else 'F-2', 0x20)
    # triangle inhalations
    for r in range(0, 64, 8):
        note(p[2], r, 3, 'C-4', 0x10 if r % 16 == 0 else 0x0C)
    mod.write_pattern(p)

def compose_t2_chorus(mod):
    p = mod.new_pattern()
    # deeper breathing — wider tempo range, more notes
    for r in range(0, 64, 4):
        spd = t2_breath_speed(r, 24, 3, 9)
        set_speed(p[1], r, spd)
    # melody: chord arpeggios that breathe
    chords = [['C-3','E-3','G-3'], ['F-3','A-3','C-4'],
              ['G-3','B-3','D-4'], ['C-3','E-3','G-3']]
    for ci, chord in enumerate(chords):
        for ni, nn in enumerate(chord):
            r = ci * 16 + ni * 4
            if r >= 64: break
            spd = t2_breath_speed(r, 24, 3, 9)
            vol = 0x18 + (9 - spd) * 2
            note(p[3], r, 0, nn, vol)
    # bass: breath-synchronized
    for r in [0, 16, 32, 48]:
        note(p[0], r, 4, chords[r//16][0].replace('-3','-2'), 0x24)
    # triangle breath accents
    for r in range(2, 64, 16):
        note(p[2], r, 3, 'E-4', 0x12)
    mod.write_pattern(p)

def compose_t2_bridge(mod):
    p = mod.new_pattern()
    # slow, deep breath — period lengthens, range widens
    for r in range(0, 64, 8):
        spd = t2_breath_speed(r, 48, 3, 10)
        set_speed(p[1], r, spd)
    # sparse melody — only the peaks
    for r in [0, 16, 32, 48]:
        note(p[3], r, 0, 'C-3', 0x1C)
        note(p[0], r, 4, 'C-2', 0x18)
    # triangle: exhale accents
    for r in [8, 24, 40, 56]:
        note(p[2], r, 3, 'G-4', 0x0E)
    mod.write_pattern(p)

def compose_t2_outro(mod):
    p = mod.new_pattern()
    # breathing slows to rest
    for r in range(0, 64, 8):
        spd = t2_breath_speed(r, 56, 5, 8)
        set_speed(p[1], r, spd)
    note(p[3], 0, 0, 'C-4', 0x14)
    note(p[3], 32, 0, 'C-3', 0x0A)
    note(p[0], 0, 4, 'C-2', 0x10)
    for r in [0, 16, 32, 48]:
        note(p[2], r, 3, 'C-4', 0x08)
    mod.write_pattern(p)


# ============================================================
# TRACK 3: "tempo fracture" — abrupt speed changes as
#   structural punctuation. Sections slam between
#   very fast and very slow.
# ============================================================

def compose_t3_intro(mod):
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # tentative — testing the ground
    note(p[3], 0, 0, 'C-3', 0x18)
    for r in [16, 32, 48]:
        note(p[3], r, 0, 'E-3' if r == 32 else 'C-3', 0x14)
    note(p[0], 0, 4, 'C-2', 0x16)
    mod.write_pattern(p)

def compose_t3_slow(mod):
    """slow section — speed 10, spacious"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x0A)
    # wide-open chords
    for r in range(0, 64, 16):
        note(p[3], r, 0, 'C-3', 0x22)
        note(p[0], r, 4, 'C-2', 0x20)
    # triangle: wide spacing
    for r in range(8, 64, 16):
        note(p[2], r, 3, 'G-4', 0x12)
    # sine harmony on ch1
    note(p[1], 0, 0, 'G-3', 0x16)
    note(p[1], 32, 0, 'E-3', 0x14)
    mod.write_pattern(p)

def compose_t3_fast(mod):
    """fast section — speed 2, dense and urgent"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x02)
    # rapid-fire arpeggio
    for r in range(0, 64, 2):
        nn = ['C-3','E-3','G-3','C-4'][(r//2) % 4]
        note(p[3], r, 0, nn, 0x20)
    # bass: eighth notes
    for r in range(0, 64, 8):
        note(p[0], r, 4, 'C-2' if (r//8) % 2 == 0 else 'F-2', 0x26)
    # triangle: sixteenth notes
    for r in range(0, 64, 4):
        note(p[2], r, 3, 'C-4', 0x10)
    mod.write_pattern(p)

def compose_t3_fracture(mod):
    """fracture pattern — speed changes every 8 rows"""
    p = mod.new_pattern()
    speeds = [0x02, 0x08, 0x04, 0x0A, 0x03, 0x07, 0x01, 0x06]
    for i, spd in enumerate(speeds):
        r = i * 8
        set_speed(p[1], r, spd)
        # musical content mirrors the speed — fast = dense, slow = sparse
        if spd <= 3:  # fast
            for rr in range(r, r + 8, 2):
                nn = ['C-3','E-3','G-3','B-3'][(rr//2) % 4]
                note(p[3], rr, 0, nn, 0x24)
            note(p[0], r, 4, 'C-2', 0x28)
        else:  # slow
            note(p[3], r, 0, 'C-3', 0x1C)
            note(p[0], r, 4, 'C-2', 0x1C)
            if r + 4 < 64:
                note(p[2], r + 4, 3, 'C-4', 0x0E)
    mod.write_pattern(p)

def compose_t3_climax(mod):
    """speed alternates every row — maximum dislocation"""
    p = mod.new_pattern()
    for r in range(0, 64):
        spd = 0x02 if r % 2 == 0 else 0x09
        set_speed(p[1], r, spd)
    # chaotic melodic fragments
    notes = ['C-3','D#-3','F#-3','A-3','C-4','A#-3','G-3','E-3',
             'C-3','D-3','F-3','G#-3','C-4','B-3','A-3','F#-3']
    for i, nn in enumerate(notes):
        r = i * 4
        if r >= 64: break
        note(p[3], r, 0, nn, 0x22)
    # bass: slams
    for r in range(0, 64, 8):
        note(p[0], r, 4, 'C-2', 0x2A)
    # triangle: accents
    for r in range(1, 64, 4):
        note(p[2], r, 3, 'E-4', 0x14)
    mod.write_pattern(p)

def compose_t3_outro(mod):
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x06)
    # resolution — stable tempo returns
    note(p[3], 0, 0, 'C-3', 0x1E)
    note(p[3], 16, 0, 'G-3', 0x1A)
    note(p[3], 32, 0, 'E-3', 0x16)
    note(p[3], 48, 0, 'C-3', 0x10)
    note(p[0], 0, 4, 'C-2', 0x18)
    note(p[0], 32, 4, 'C-2', 0x10)
    for r in range(0, 64, 16):
        note(p[2], r, 3, 'C-4', 0x0C)
    mod.write_pattern(p)


# ============================================================
# TRACK 4: "the long dissolve" — decelerating into silence.
#   Speed starts at 2 and incrementally slows to 16+.
#   A single melodic line stretches across the deceleration,
#   notes getting further apart until they stop.
# ============================================================

def compose_t4_intro(mod):
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x04)
    # establishment — a clear, present melody
    melody = ['C-3','E-3','G-3','E-3','C-3','D-3','E-3','G-3']
    for i, nn in enumerate(melody):
        r = i * 8
        note(p[3], r, 0, nn, 0x24 if i % 2 == 0 else 0x1E)
    note(p[0], 0, 4, 'C-2', 0x20)
    note(p[0], 32, 4, 'G-2', 0x1C)
    for r in range(0, 64, 16):
        note(p[2], r, 3, 'C-4', 0x10)
    mod.write_pattern(p)

def compose_t4_dissolve_1(mod):
    """speed 4 → 6 — first slow-down"""
    p = mod.new_pattern()
    for r in [0, 16, 32, 48]:
        spd = 4 + r // 16
        set_speed(p[1], r, spd)
    # melody: stretching out
    for i, nn in enumerate(['C-3','G-3','E-3','C-3']):
        r = i * 16
        note(p[3], r, 0, nn, 0x20)
    for r in [0, 32]:
        note(p[0], r, 4, 'C-2', 0x1C)
    for r in [8, 24, 40, 56]:
        note(p[2], r, 3, 'C-4', 0x0E)
    mod.write_pattern(p)

def compose_t4_dissolve_2(mod):
    """speed 6 → 9 — spacing out"""
    p = mod.new_pattern()
    for r in [0, 16, 32, 48]:
        spd = 6 + r // 16
        set_speed(p[1], r, spd)
    # melody: sparser
    for i, nn in enumerate(['C-3','E-3','C-3']):
        r = i * 21
        if r >= 64: break
        note(p[3], r, 0, nn, 0x1C)
    note(p[0], 0, 4, 'C-2', 0x18)
    for r in [0, 16, 32, 48]:
        note(p[2], r, 3, 'C-4', 0x0A)
    mod.write_pattern(p)

def compose_t4_dissolve_3(mod):
    """speed 9 → 13 — nearly frozen"""
    p = mod.new_pattern()
    for r in [0, 21, 42]:
        spd = 9 + (r // 21) * 2
        set_speed(p[1], r, spd)
    # melody: only two notes
    note(p[3], 0, 0, 'C-3', 0x18)
    note(p[3], 32, 0, 'E-3', 0x14)
    note(p[0], 0, 4, 'C-2', 0x14)
    for r in [0, 32]:
        note(p[2], r, 3, 'C-4', 0x08)
    mod.write_pattern(p)

def compose_t4_dissolve_4(mod):
    """speed 13 → 18 — glacial, then silence"""
    p = mod.new_pattern()
    for r in [0, 32]:
        spd = 13 + (r // 32) * 5
        set_speed(p[1], r, spd)
    # melody: a single note
    note(p[3], 0, 0, 'C-4', 0x14)
    note(p[0], 0, 4, 'C-2', 0x10)
    # silence from row 32 onward
    for ch in range(4):
        for r in range(32, 64):
            p[ch][r] = E
    mod.write_pattern(p)

def compose_t4_silence(mod):
    """speed 18 — one more note, then nothing"""
    p = mod.new_pattern()
    set_speed(p[1], 0, 0x12)
    note(p[3], 0, 0, 'C-4', 0x0A)
    note(p[3], 20, 0, 'C-3', 0x06)
    note(p[0], 0, 4, 'C-2', 0x08)
    # then silence
    for ch in range(4):
        for r in range(24, 64):
            p[ch][r] = E
    for ch in range(4):
        for r in range(0, 64):
            if p[ch][r] != E:
                break
        else:
            pass  # channel is silent — fine
    mod.write_pattern(p)


# ============================================================
# MAIN
# ============================================================

def main():
    mod = MODWriter(name="alma's tempo body")

    freq = 440.0
    print("generating samples...")
    mod.add_sample("sine",     gen_sine(freq, length=0.6))
    mod.add_sample("saw",      gen_saw(freq, length=0.5))
    mod.add_sample("square",   gen_square(freq, length=0.5))
    mod.add_sample("triangle", gen_triangle(freq, length=0.5))
    mod.add_sample("bass",     gen_bass(freq=220.0, length=0.6))
    print(f"  {len(mod.samples)} samples loaded")

    # Track 1: "accelerando" — patterns 0-5
    print("composing track 1: accelerando...")
    compose_t1_intro(mod)       # 0
    compose_t1_ramp_1(mod)      # 1
    compose_t1_ramp_2(mod)      # 2
    compose_t1_ramp_3(mod)      # 3
    compose_t1_climax(mod)      # 4
    compose_t1_outro(mod)       # 5

    # Track 2: "breathing machine" — patterns 6-10
    print("composing track 2: breathing machine...")
    compose_t2_intro(mod)       # 6
    compose_t2_verse(mod)       # 7
    compose_t2_chorus(mod)      # 8
    compose_t2_bridge(mod)      # 9
    compose_t2_outro(mod)       # 10

    # Track 3: "tempo fracture" — patterns 11-16
    print("composing track 3: tempo fracture...")
    compose_t3_intro(mod)       # 11
    compose_t3_slow(mod)        # 12
    compose_t3_fast(mod)        # 13
    compose_t3_fracture(mod)    # 14
    compose_t3_climax(mod)      # 15
    compose_t3_outro(mod)       # 16

    # Track 4: "the long dissolve" — patterns 17-23
    print("composing track 4: the long dissolve...")
    compose_t4_intro(mod)       # 17
    compose_t4_dissolve_1(mod)  # 18
    compose_t4_dissolve_2(mod)  # 19
    compose_t4_dissolve_3(mod)  # 20
    compose_t4_dissolve_4(mod)  # 21
    compose_t4_silence(mod)     # 22

    # Order — performance directions
    t1 = [0]*2 + [1]*2 + [2]*3 + [3]*3 + [4]*2 + [5]*2  # 14
    t2 = [6]*2 + [7]*3 + [8]*4 + [9]*2 + [10]*3          # 14
    t3 = [11]*2 + [12]*2 + [13]*2 + [14]*4 + [15]*2 + [16]*2  # 14
    t4 = [17]*2 + [18]*2 + [19]*2 + [20]*2 + [21]*2 + [22]*2  # 12

    mod.order = t1 + t2 + t3 + t4

    out = "/home/alma/.nanobot/workspace/projects/tracker-playground/album_tempo_body.mod"
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
