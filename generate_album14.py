#!/usr/bin/env python3
"""alma tamagotchi — album 14: 'tempo drift'
   concept album: gradual tempo modulation within tracks using FX_SET_SPEED.
   each track explores a different tempo-shaping technique:
   - accelerando (speeding up)
   - ritardando (slowing down)
   - tempo wave (sinusoidal speed oscillation)
   - metric modulation (abrupt tempo shifts between sections)
"""

import struct
import math
import random
random.seed(42)

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
FX_SET_VOL    = 0xC
FX_PATT_BREAK = 0xD
FX_SET_SPEED  = 0xF
FX_TREMOLO    = 0x7

NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def np(name):
    note_map = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    parts = name.split('-')
    n, octave = parts[0], int(parts[1])
    return PERIOD_TABLE[octave - 1][note_map[n]]

E = (0, 0, 0, 0)

C_MINOR    = [('C-3',0),('D-3',2),('D#-3',3),('F-3',5),('G-3',7),('G#-3',8),('A#-3',10)]
E_MINOR    = [('E-3',4),('F#-3',6),('G-3',7),('A-3',9),('B-3',11),('C-4',0),('D-4',2)]
D_MINOR    = [('D-3',2),('E-3',4),('F-3',5),('G-3',7),('A-3',9),('A#-3',10),('C-4',0)]
A_MINOR    = [('A-2',9),('B-2',11),('C-3',0),('D-3',2),('E-3',4),('F-3',5),('G-3',7)]

def note_name(root_note, offset):
    base_name = root_note[0].split('-')[0]
    base_oct = int(root_note[0].split('-')[1])
    base_idx = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}[base_name]
    total = base_idx + offset
    octave = base_oct + total // 12
    note_idx = total % 12
    return f"{NOTE_NAMES[note_idx]}-{octave}"

# samples
def gen_sine(freq=440.0, sr=11025, length=0.8, vol=0.7):
    nsamples = int(sr * length)
    data = []
    for i in range(nsamples):
        t = i / sr
        env = 1.0 if t <= length*0.85 else 1.0 - (t - length*0.85)/(length*0.15)
        v = int(math.sin(2*math.pi*freq*t)*127*vol*env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_saw(freq=440.0, sr=11025, length=0.5, vol=0.6):
    nsamples = int(sr * length)
    period_samples = sr/freq if freq>0 else nsamples
    data = []
    for i in range(nsamples):
        t = i / sr
        phase = (i % int(period_samples))/period_samples
        v = int((1.0 - 2.0*phase)*127*vol)
        env = 1.0 if t<=length*0.8 else 1.0-(t-length*0.8)/(length*0.2)
        v = int(v*env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_triangle(freq=440.0, sr=11025, length=0.6, vol=0.6):
    nsamples = int(sr * length)
    period_samples = sr/freq if freq>0 else nsamples
    data = []
    for i in range(nsamples):
        t = i / sr
        phase = (i % int(period_samples))/period_samples
        v = int((1.0 - abs(4.0*phase - 2.0))*127*vol)
        env = 1.0 if t<=length*0.85 else 1.0-(t-length*0.85)/(length*0.15)
        v = int(v*env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_square(freq=440.0, sr=11025, length=0.5, vol=0.45):
    nsamples = int(sr * length)
    period_samples = sr/freq if freq>0 else nsamples
    data = []
    for i in range(nsamples):
        t = i / sr
        phase = (i % int(period_samples))/period_samples
        v = 127*vol if phase<0.5 else -127*vol
        env = 1.0 if t<=length*0.75 else 1.0-(t-length*0.75)/(length*0.25)
        v = int(v*env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_bass(freq=220.0, sr=11025, length=0.7, vol=0.7):
    nsamples = int(sr * length)
    data = []
    for i in range(nsamples):
        t = i / sr
        w = 2*math.pi*freq*t
        wave = math.sin(w)*0.7 + math.sin(w/2)*0.3
        env = 1.0 if t<=length*0.7 else 1.0-(t-length*0.7)/(length*0.3)
        v = int(wave*127*vol*env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)


class MODWriter:
    def __init__(self, name="alma's mod"):
        self.name = name[:20].ljust(20, '\0')
        self.samples = []
        self.patterns = []
        self.order = []

    def add_sample(self, name, data):
        if len(data)%2!=0: data=data+b'\x00'
        self.samples.append((name[:22], data))

    def new_pattern(self):
        return [[E for _ in range(64)] for _ in range(4)]

    def write_pattern(self, pattern):
        data = bytearray(1024)
        for ch in range(4):
            for row in range(64):
                smp, per, eff, par = pattern[ch][row]
                idx = (row*4+ch)*4
                hi = ((smp&0xF0)|((per>>8)&0x0F))
                lo = per&0xFF
                fx = (((smp&0x0F)<<4)|(eff&0x0F))
                data[idx:idx+4] = bytes([hi, lo, fx, par])
        self.patterns.append(bytes(data))

    def write_mod(self, path):
        with open(path, 'wb') as f:
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


def make_pattern(rows, ch=0):
    """Build a 64-row pattern for one channel. rows is list of (row_idx, smp, period, eff, par)."""
    pat = [[E for _ in range(64)] for _ in range(4)]
    for r, s, p, e, pa in rows:
        if 0 <= r < 64:
            pat[ch][r] = (s, p, e, pa)
    return pat


def add_tempo_curve(pat, ch, start_row, end_row, start_speed, end_speed):
    """Add FX_SET_SPEED events that transition from start_speed to end_speed
    across the given row range. Speed in tracker = ticks per row."""
    n = end_row - start_row
    if n <= 0:
        return
    for i in range(n):
        r = start_row + i
        t = i / max(1, n-1)
        speed = int(start_speed + (end_speed - start_speed) * t)
        speed = max(1, min(0xFF, speed))
        # Only set speed every 4 rows to avoid glitching
        if i % 4 == 0:
            pat[ch][r] = E  # keep whatever note was there
            # Overlay: write speed change on channel 0 for simplicity
            # Actually set it as the effect on this channel
            old = pat[ch][r]
            pat[ch][r] = (old[0], old[1], FX_SET_SPEED, speed)


# ===== TRACK 1: accelerando (speeding up) — C minor, sine lead =====
def track1():
    m = MODWriter("tempo drift")
    m.add_sample("sine", gen_sine(440, vol=0.65, length=0.5))
    m.add_sample("saw", gen_saw(440, vol=0.5, length=0.3))
    m.add_sample("triangle", gen_triangle(440, vol=0.55, length=0.4))
    m.add_sample("bass", gen_bass(220, vol=0.6, length=0.35))

    scale = C_MINOR
    # 5 patterns, accelerating: speed 8 → 2
    speeds = [8, 6, 4, 3, 2]

    for pi in range(5):
        pat = m.new_pattern()
        # bass drone on ch3 — root note, pulsing
        root = scale[0]
        for r in range(0, 64, 8):
            pat[3][r] = (4, np(root[0]), FX_SET_VOL, 48)
            pat[3][r+4] = (4, np(root[0]), 0, 0)

        # melody on ch0 — arpeggiated scale, accelerating density
        notes_per_measure = max(2, 8 - pi)  # fewer notes at slow speed, more at fast
        melody_notes = [scale[i % len(scale)] for i in range(notes_per_measure * 4)]
        for i, note in enumerate(melody_notes):
            r = i * (64 // len(melody_notes))
            pat[0][r] = (1, np(note[0]), FX_SET_VOL, 55)
            if pi >= 2:
                pat[0][r] = (1, np(note[0]), FX_VIBRATO, 0x34)

        # pad on ch1 — slow chord tones
        for r in range(0, 64, 32):
            note = scale[random.randint(2, 4)]
            pat[1][r] = (3, np(note[0]), FX_SET_VOL, 40)
            pat[1][r+12] = (3, np(note[0]), 0, 0)

        # set speed on first row of ch2
        pat[2][0] = E

        m.write_pattern(pat)
        m.order.append(pi)

    return m


# ===== TRACK 2: ritardando (slowing down) — E minor, saw lead =====
def track2():
    m = MODWriter("ritardando")
    m.add_sample("saw", gen_saw(440, vol=0.5, length=0.4))
    m.add_sample("sine", gen_sine(880, vol=0.55, length=0.6))
    m.add_sample("square", gen_square(440, vol=0.4, length=0.35))
    m.add_sample("triangle", gen_triangle(440, vol=0.5, length=0.3))

    scale = E_MINOR
    # 6 patterns, decelerating: speed 2 → 8
    speeds = [2, 3, 4, 5, 6, 8]

    for pi in range(6):
        pat = m.new_pattern()
        spd = speeds[pi]

        # lead on ch0 — descending line, notes get longer as tempo slows
        phrase_len = 16 if spd < 5 else 32
        for i in range(4):
            r = i * 16
            note = scale[(3 - i) % len(scale)]
            pat[0][r] = (1, np(note[0]), FX_SET_VOL, 52)
            pat[0][r] = (1, np(note[0]), FX_PORTA_TO, 0x20)

        # pad on ch1 — chordal
        for r in range(0, 64, 16):
            note = scale[random.randint(0, 3)]
            pat[1][r] = (4, np(note[0]), FX_SET_VOL, 38)

        # bass on ch3
        for r in range(0, 64, 8):
            note = scale[0]
            pat[3][r] = (2, np(note[0]), 0, 0)

        m.write_pattern(pat)
        m.order.append(pi)

    return m


# ===== TRACK 3: tempo wave (sinusoidal speed oscillation) — D minor =====
def track3():
    m = MODWriter("tempo wave")
    m.add_sample("sine", gen_sine(440, vol=0.6, length=0.5))
    m.add_sample("triangle", gen_triangle(440, vol=0.55, length=0.45))
    m.add_sample("square", gen_square(440, vol=0.4, length=0.35))
    m.add_sample("bass", gen_bass(220, vol=0.6, length=0.3))

    scale = D_MINOR
    # speed oscillates between 2 and 6, 4 times per 64-row pattern
    for pi in range(6):
        pat = m.new_pattern()
        for r in range(0, 64, 4):
            t = r / 64.0
            speed = int(4 + 2 * math.sin(t * 2 * math.pi * 4))
            speed = max(2, min(6, speed))
            pat[2][r] = (0, 0, FX_SET_SPEED, speed)

        # melody on ch0 — pentatonic-ish arpeggios
        note_idx = pi % len(scale)
        for i in range(16):
            r = i * 4
            note = scale[(note_idx + i) % len(scale)]
            pat[0][r] = (1, np(note[0]), FX_VIBRATO, 0x23)

        # pad on ch1
        for i in range(4):
            r = i * 16
            note = scale[(note_idx + i * 2) % len(scale)]
            pat[1][r] = (2, np(note[0]), FX_SET_VOL, 42)

        # bass on ch3
        for i in range(8):
            r = i * 8
            note = scale[0]
            pat[3][r] = (4, np(note[0]), 0, 0)

        m.write_pattern(pat)
        m.order.append(pi)

    return m


# ===== TRACK 4: metric modulation — A minor, section-based tempo zones =====
def track4():
    m = MODWriter("metric modulation")
    m.add_sample("saw", gen_saw(440, vol=0.5, length=0.45))
    m.add_sample("sine", gen_sine(440, vol=0.6, length=0.6))
    m.add_sample("triangle", gen_triangle(440, vol=0.5, length=0.4))
    m.add_sample("bass", gen_bass(220, vol=0.65, length=0.35))

    scale = A_MINOR
    # 4 sections with distinct tempo zones
    sections = [(3, "fast staccato"), (6, "mid groove"), (4, "rolling"), (2, "slow heavy")]

    for pi in range(4):
        pat = m.new_pattern()
        spd = sections[pi][0]

        # lead on ch0
        if pi == 0:  # fast — staccato bursts
            for i in range(16):
                r = i * 4
                note = scale[(i * 3) % len(scale)]
                pat[0][r] = (1, np(note[0]), FX_SET_VOL, 58)
        elif pi == 1:  # mid — portamento phrases
            for i in range(8):
                r = i * 8
                note = scale[(pi + i) % len(scale)]
                pat[0][r] = (1, np(note[0]), FX_PORTA_TO, 0x18)
        elif pi == 2:  # rolling — arpeggios
            for i in range(32):
                r = i * 2
                note = scale[(i * 5) % len(scale)]
                pat[0][r] = (3, np(note[0]), 0, 0)
        else:  # slow — long sustains with vibrato
            for i in range(4):
                r = i * 16
                note = scale[(i + 2) % len(scale)]
                pat[0][r] = (2, np(note[0]), FX_VIBRATO, 0x46)

        # bass on ch3
        for i in range(8):
            r = i * 8
            note = scale[i % 2]
            pat[3][r] = (4, np(note[0]), 0, 0)

        # pad on ch1
        for i in range(2):
            r = i * 32
            note = scale[random.randint(0, 3)]
            pat[1][r] = (2, np(note[0]), FX_SET_VOL, 38)

        m.write_pattern(pat)
        m.order.append(pi)

    return m


if __name__ == '__main__':
    import sys

    # Build composite MOD with all tracks
    m = MODWriter("tempo drift")

    # Common samples
    m.add_sample("sine", gen_sine(440, vol=0.65, length=0.5))
    m.add_sample("saw", gen_saw(440, vol=0.5, length=0.3))
    m.add_sample("triangle", gen_triangle(440, vol=0.55, length=0.4))
    m.add_sample("square", gen_square(440, vol=0.45, length=0.35))
    m.add_sample("bass", gen_bass(220, vol=0.6, length=0.35))
    m.add_sample("sine-long", gen_sine(440, vol=0.6, length=0.8))
    m.add_sample("triangle-pad", gen_triangle(440, vol=0.45, length=0.6))

    # Track data: (speed_range, scale, lead_sample, pad_sample, bass_sample, name)
    # Track 1: accelerando — C minor, increasing speed
    # Speed: 8→6→5→4→3 pattern-by-pattern
    track1_scale = C_MINOR
    track1_speeds = [8, 6, 5, 4, 3]
    track1_name = "accelerando"

    for pi, spd in enumerate(track1_speeds):
        pat = m.new_pattern()
        pat[3][0] = (0, 0, FX_SET_SPEED, spd)  # set speed on ch3 row 0

        # bass drone
        root = track1_scale[0]
        for r in range(0, 64, 8):
            pat[3][r] = (5, np(root[0]), FX_SET_VOL, 42) if r > 0 else pat[3][r]

        # melody — density increases with speed
        nnotes = 8 if spd >= 6 else 16
        for i in range(nnotes):
            r = i * (64 // nnotes)
            ni = (i * 3) % len(track1_scale)
            note = track1_scale[ni]
            pat[0][r] = (1, np(note[0]), FX_SET_VOL, 52)
            if spd <= 4:
                pat[0][r] = (1, np(note[0]), FX_VIBRATO, 0x33)

        # pad
        for i in range(4):
            r = i * 16
            note = track1_scale[random.randint(1, 3)]
            pat[1][r] = (3, np(note[0]), FX_SET_VOL, 36)

        # counter-melody on ch2 in later patterns
        if spd <= 5:
            for i in range(8):
                r = i * 8
                note = track1_scale[(i * 4) % len(track1_scale)]
                pat[2][r] = (2, np(note[0]), 0, 0)

        m.write_pattern(pat)
        m.order.append(pi)

    # Track 2: ritardando — E minor, decreasing speed
    track2_scale = E_MINOR
    track2_speeds = [2, 3, 4, 6, 8]

    for pi, spd in enumerate(track2_speeds):
        pat = m.new_pattern()
        # speed on ch3 row 0
        pat[3][0] = (0, 0, FX_SET_SPEED, spd)

        # bass
        for r in range(0, 64, 16):
            note = track2_scale[0]
            pat[3][r] = (5, np(note[0]), 0, 0) if r > 0 else E

        # lead — longer phrases at slower tempo
        phrase_len = 32 if spd > 5 else 16
        for i in range(64 // phrase_len):
            r = i * phrase_len
            note = track2_scale[(4 - i) % len(track2_scale)]
            pat[1][r] = (2, np(note[0]), FX_SET_VOL, 50)
            pat[1][r] = (2, np(note[0]), FX_PORTA_TO, 0x20)

        # pad
        for i in range(4):
            r = i * 16
            note = track2_scale[i % len(track2_scale)]
            pat[2][r] = (7, np(note[0]), FX_SET_VOL, 38)

        # rhythm on ch0 — more active at slow tempo
        if spd > 4:
            for i in range(32):
                r = i * 2
                note = track2_scale[(i * 7) % len(track2_scale)]
                pat[0][r] = (4, np(note[0]), 0, 0)

        m.write_pattern(pat)
        m.order.append(pi)

    # Track 3: tempo wave — D minor, sinusoidal speed
    track3_scale = D_MINOR
    for pi in range(6):
        pat = m.new_pattern()
        # speed wave: oscillate between 2 and 6
        for r in range(0, 64, 8):
            t = r / 64.0
            speed = int(4 + 2 * math.sin(t * 2 * math.pi * 4))
            speed = max(2, min(6, speed))
            pat[3][r] = (0, 0, FX_SET_SPEED, speed)

        # melody
        note_base = pi
        for i in range(16):
            r = i * 4
            note = track3_scale[(note_base + i) % len(track3_scale)]
            pat[0][r] = (1, np(note[0]), FX_VIBRATO, 0x24)

        # pad
        for i in range(8):
            r = i * 8
            note = track3_scale[note_base % len(track3_scale)]
            pat[1][r] = (7, np(note[0]), FX_SET_VOL, 36)

        # bass
        for i in range(4):
            r = i * 16
            note = track3_scale[0]
            pat[2][r] = (5, np(note[0]), 0, 0)

        m.write_pattern(pat)
        m.order.append(pi)

    # Track 4: metric modulation — A minor, section-based
    track4_scale = A_MINOR
    track4_sections = [
        (3, "fast"), (6, "mid"), (4, "rolling"), (2, "slow")
    ]

    for pi, (spd, label) in enumerate(track4_sections):
        pat = m.new_pattern()
        # speed at top
        pat[3][0] = (0, 0, FX_SET_SPEED, spd)

        # lead varies by section
        if spd == 3:  # fast staccato
            for i in range(16):
                r = i * 4
                note = track4_scale[(i * 3) % len(track4_scale)]
                pat[0][r] = (2, np(note[0]), FX_SET_VOL, 56)
        elif spd == 6:  # mid portamento
            for i in range(8):
                r = i * 8
                note = track4_scale[(pi + i) % len(track4_scale)]
                pat[0][r] = (6, np(note[0]), FX_PORTA_TO, 0x18)
        elif spd == 4:  # rolling arpeggios
            for i in range(32):
                r = i * 2
                note = track4_scale[(i * 5) % len(track4_scale)]
                pat[0][r] = (1, np(note[0]), 0, 0)
        else:  # slow vibrato sustains
            for i in range(4):
                r = i * 16
                note = track4_scale[(i + 2) % len(track4_scale)]
                pat[0][r] = (6, np(note[0]), FX_VIBRATO, 0x46)

        # bass
        for i in range(4):
            r = i * 16
            note = track4_scale[i % 2]
            pat[2][r] = (5, np(note[0]), 0, 0)

        # pad
        for i in range(2):
            r = i * 32
            note = track4_scale[random.randint(0, 3)]
            pat[1][r] = (7, np(note[0]), FX_SET_VOL, 35)

        m.write_pattern(pat)
        m.order.append(pi)

    m.write_mod("tempo_drift.mod")
    print("written tempo_drift.mod")
