#!/usr/bin/env python3
"""alma tamagotchi — album 11: 'drift body'
   generative/minimalist approach: longer forms, slower evolution.
   mathematical processes generating note sequences across extended durations."""

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
FX_VIBRATO    = 0x4
FX_VOL_SLIDE  = 0xA
FX_POS_JUMP   = 0xB
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

# === scale helpers ===

C_MAJOR = [('C-3',0),('D-3',2),('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11)]
D_DORIAN = [('D-3',2),('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11),('C-4',0)]
E_PHRYGIAN = [('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11),('C-4',0),('D-4',2)]
A_MINOR = [('A-2',9),('B-2',11),('C-3',0),('D-3',2),('E-3',4),('F-3',5),('G-3',7)]

def note_name(root_note, offset):
    """Given a root like ('C-3',0), add offset semitones, return note string"""
    base_name, base_oct = root_note[0], int(root_note[0].split('-')[1])
    base_idx = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}[base_name.split('-')[0]]
    total = base_idx + offset
    octave = base_oct + total // 12
    note = NOTE_NAMES[total % 12]
    return f"{note}-{octave}"


# === waveforms ===

def gen_sine(freq=440.0, sr=11025, length=0.5, vol=0.7):
    nsamples = int(sr * length)
    data = []
    for i in range(nsamples):
        t = i / sr
        env = 1.0 if t <= length * 0.85 else 1.0 - (t - length * 0.85) / (length * 0.15)
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
        env = 1.0 if t <= length * 0.85 else 1.0 - (t - length * 0.85) / (length * 0.15)
        v = int(v * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_square(freq=440.0, sr=11025, length=0.5, vol=0.45):
    nsamples = int(sr * length)
    period_samples = sr / freq if freq > 0 else nsamples
    data = []
    for i in range(nsamples):
        t = i / sr
        phase = (i % int(period_samples)) / period_samples
        v = 127 * vol if phase < 0.5 else -127 * vol
        env = 1.0 if t <= length * 0.75 else 1.0 - (t - length * 0.75) / (length * 0.25)
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

def gen_soft_pad(freq=440.0, sr=11025, length=1.5, vol=0.4):
    nsamples = int(sr * length)
    data = []
    for i in range(nsamples):
        t = i / sr
        wave = math.sin(2*math.pi*freq*t) * 0.5 + math.sin(2*math.pi*freq*0.5*t) * 0.3 + math.sin(2*math.pi*freq*2*t)*0.2
        env = min(t * 4, 1.0) * max(0, 1.0 - (t - length * 0.6) / (length * 0.4))
        v = int(wave * 127 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_glass(freq=528.0, sr=11025, length=2.0, vol=0.35):
    """Bell-like with harmonics"""
    nsamples = int(sr * length)
    data = []
    for i in range(nsamples):
        t = i / sr
        wave = (math.sin(2*math.pi*freq*t) * 0.6 +
                math.sin(2*math.pi*freq*2.76*t) * 0.3 +
                math.sin(2*math.pi*freq*5.4*t) * 0.1)
        env = math.exp(-t * 3.5)
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
                hi = ((smp&0xF0) | ((per>>8)&0x0F))
                lo = per&0xFF
                fx = (((smp&0x0F)<<4)|(eff&0x0F))
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


def note(ch, row, sample, pitch, vol=None, fx=0, param=0):
    per = np(pitch)
    if vol is not None:
        ch[row] = (sample, per, FX_SET_VOL, vol)
    else:
        ch[row] = (sample, per, fx, param)

# sample indices: 0=sine, 1=saw, 2=triangle, 3=square, 4=bass, 5=softpad, 6=glass


# ============================================================
# fibonacci helper
# ============================================================
def fibonacci_up_to(n):
    """Generate fibonacci numbers up to n"""
    fibs = [1, 1]
    while fibs[-1] < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs[:-1]  # exclude last if > n

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def primes_up_to(n):
    return [i for i in range(2, n) if is_prime(i)]


# ============================================================
# TRACK 1: "fibonacci field" — Fibonacci-spaced events
#   Notes triggered at Fibonacci-number row positions.
#   Gradual shift from C major → D dorian → E phrygian over duration.
#   Slow tempo (speed 4), long form.
# ============================================================

def compose_t1_patterns(mod):
    """Fibonacci field — 6 patterns for a single long-evolving section"""
    fibs = fibonacci_up_to(64)
    patterns = []
    speed = 0x04  # slow

    for pnum in range(6):
        p = mod.new_pattern()
        # speed set on first note of pattern 0
        if pnum == 0:
            p[3][0] = (0, 0, FX_SET_SPEED, speed)

        # bass: root at fibonacci positions, rising through modes
        root_progression = ['C-3','D-3','D-3','E-3','E-3','C-3']  # C→D→E→C
        root = root_progression[pnum]

        for fi, fib in enumerate(fibs):
            if fib >= 64: break
            # bass on every 3rd fib position
            if fi % 3 == 0:
                vol = 0x20 - fi
                note(p[0], fib, 4, root, max(8, vol))

        # melody: sparse, Fibonacci-spaced notes from scale
        scale = [C_MAJOR, C_MAJOR, D_DORIAN, D_DORIAN, E_PHRYGIAN, C_MAJOR][pnum]
        for fi, fib in enumerate(fibs):
            if fib >= 64: break
            if fi >= 2:  # skip first two (too close)
                scale_idx = (fi * 3 + pnum) % len(scale)
                nn = note_name(scale[scale_idx], scale[scale_idx][1])
                vol = 0x18 - (fi % 4)
                note(p[3], fib, 0, nn, max(8, vol))

        # pad: slow-evolving texture
        if pnum % 2 == 0:
            pad_note = ['C-3','D-3','E-3','C-3'][pnum // 2] if pnum < 4 else 'C-3'
            note(p[2], 0, 5, pad_note, 0x12)
            # tremolo for movement
            p[2][0] = (5, np(pad_note), FX_TREMOLO, 0x43)

        patterns.append(p)
        mod.write_pattern(p)

    return patterns


# ============================================================
# TRACK 2: "prime lattice" — Prime-number row triggers
# ============================================================

def compose_t2_patterns(mod):
    """Prime lattice — notes on prime-number rows, slow filter evolution"""
    primes = primes_up_to(64)
    patterns = []

    for pnum in range(6):
        p = mod.new_pattern()
        if pnum == 0:
            p[3][0] = (0, 0, FX_SET_SPEED, 0x04)

        # bass: long notes on every 4th prime
        bass_notes = ['C-2','C-2','G-2','A-2','F-2','C-2']
        for pi, prime in enumerate(primes):
            if pi % 4 == 0:
                note(p[0], prime, 4, bass_notes[pnum], 0x1E - pi // 4)

        # melody: primes trigger notes in A minor
        scale = A_MINOR
        for pi, prime in enumerate(primes):
            scale_idx = (prime + pnum * 7) % len(scale)
            nn = note_name(scale[scale_idx], scale[scale_idx][1])
            vol = 0x1C - (prime // 10)
            if pi % 2 == 0:
                note(p[3], prime, 0, nn, max(8, vol))
            else:
                note(p[2], prime, 2, nn, max(8, vol))

        # pad drone on root
        note(p[1], 0, 5, 'A-2', 0x10)
        p[1][0] = (5, np('A-2'), FX_TREMOLO, 0x35 + pnum)

        patterns.append(p)
        mod.write_pattern(p)

    return patterns


# ============================================================
# TRACK 3: "rule 30" — Cellular automaton Rule 30 generating events
# ============================================================

def rule_30(left, center, right):
    """Wolfram Rule 30: 111→0, 110→0, 101→0, 100→1, 011→1, 010→1, 001→1, 000→0"""
    state = (left << 2) | (center << 1) | right
    return [0, 1, 1, 1, 1, 0, 0, 0][state]

def evolve_rule_30(initial_state, rows):
    """Evolve Rule 30 for given number of rows. Returns list of row-states (lists of booleans)."""
    width = len(initial_state)
    states = [initial_state]
    current = initial_state[:]
    for _ in range(rows - 1):
        next_row = []
        for i in range(width):
            left = current[(i-1) % width]
            center = current[i]
            right = current[(i+1) % width]
            next_row.append(rule_30(left, center, right))
        states.append(next_row)
        current = next_row
    return states

def compose_t3_patterns(mod):
    """Rule 30 — 8 patterns, CA state determines note triggers"""
    width = 12  # one octave
    initial = [0]*12
    initial[5] = 1  # single seed in middle
    states = evolve_rule_30(initial, 64 * 8)  # 8 patterns × 64 rows

    scale = D_DORIAN
    patterns = []

    for pnum in range(8):
        p = mod.new_pattern()
        if pnum == 0:
            p[3][0] = (0, 0, FX_SET_SPEED, 0x04)

        for row in range(64):
            global_row = pnum * 64 + row
            row_state = states[global_row]

            # Bass: strong when many cells are active
            active_count = sum(row_state)
            if active_count >= 5:
                bass_note = 'D-2' if global_row < 256 else 'A-2' if global_row < 384 else 'D-2'
                note(p[0], row, 4, bass_note, 0x18 + min(active_count, 12))

            # Melody: each active cell = a note from D dorian at corresponding degree
            for cell_idx, active in enumerate(row_state):
                if active:
                    scale_idx = cell_idx % len(scale)
                    nn = note_name(scale[scale_idx], scale[scale_idx][1])
                    vol = 0x10 + (cell_idx // 2)
                    note(p[3], row, 0, nn, min(0x28, vol))

            # Pad: evolving, tied to CA density
            if row % 16 == 0:
                pad_note = ['D-3','G-3','A-3','D-3'][(global_row // 128) % 4]
                p[2][row] = (5, np(pad_note), FX_SET_VOL, 0x10)

        patterns.append(p)
        mod.write_pattern(p)

    return patterns


# ============================================================
# TRACK 4: "the long dissolve" — sparse, single notes, deconstructing
# ============================================================

def compose_t4_patterns(mod):
    """The long dissolve — very sparse, each note held long, dissolving into silence"""
    patterns = []

    # C major notes, spaced far apart, with increasingly long gaps
    note_sequence = [
        ('C-3', 0, 64),  # note, row, gap_to_next
        ('G-3', 72, 80),
        ('E-3', 160, 96),
        ('A-3', 264, 112),
        ('C-4', 384, 128),
        ('B-3', 520, 96),
        ('G-3', 624, 80),
        ('E-3', 712, 72),
        ('C-3', 792, 64),
        ('G-3', 864, 56),
        ('E-3', 928, 48),
        ('C-3', 984, 40),
        ('G-3', 1032, 36),
        ('C-3', 1076, 32),
    ]

    patterns = []
    pat_notes = {}
    for note_name_val, row, gap in note_sequence:
        pnum = row // 64
        r = row % 64
        if pnum not in pat_notes:
            pat_notes[pnum] = []
        pat_notes[pnum].append((note_name_val, r, note_name_val, gap))

    total_patterns = max(pat_notes.keys()) + 1 if pat_notes else 1

    for pnum in range(total_patterns):
        p = mod.new_pattern()
        if pnum == 0:
            p[3][0] = (0, 0, FX_SET_SPEED, 0x05)

        # place notes for this pattern
        if pnum in pat_notes:
            notes_in_pattern = pat_notes[pnum]
            for idx, (nn, r, _, _) in enumerate(notes_in_pattern):
                # volume decreases as we go along
                vol = max(0x08, 0x22 - idx * 3)
                note(p[3], r, 0, nn, vol)

                # glass shimmer on strong notes
                if idx % 3 == 0:
                    note(p[2], r, 6, 'C-5', max(0x06, vol // 3))

        # bass drone: appearing then fading
        if pnum < len(note_sequence) // 3:
            note(p[0], 0, 4, 'C-2', min(0x20, 0x0C + pnum * 2))

        # pad: long fade
        if pnum == 0:
            note(p[1], 0, 5, 'C-3', 0x16)
            p[1][0] = (5, np('C-3'), FX_TREMOLO, 0x52)
        elif pnum == total_patterns // 2:
            note(p[1], 0, 5, 'G-3', 0x0C)

        # silence: final pattern is just the drone fading
        patterns.append(p)
        mod.write_pattern(p)

    return patterns


# ============================================================
# MAIN
# ============================================================

def main():
    mod = MODWriter(name="alma's drift body")

    freq = 440.0
    print("generating samples...")
    mod.add_sample("sine",       gen_sine(freq, length=0.8))
    mod.add_sample("saw",        gen_saw(freq, length=0.5))
    mod.add_sample("triangle",   gen_triangle(freq, length=0.6))
    mod.add_sample("square",     gen_square(freq, length=0.5))
    mod.add_sample("bass",       gen_bass(freq=220.0, length=0.8))
    mod.add_sample("soft pad",   gen_soft_pad(freq, length=2.0))
    mod.add_sample("glass",      gen_glass(freq=528.0, length=2.5))
    print(f"  {len(mod.samples)} samples loaded")

    # Track 1: fibonacci field
    print("composing track 1: fibonacci field...")
    t1_pats = compose_t1_patterns(mod)

    # Track 2: prime lattice
    print("composing track 2: prime lattice...")
    t2_pats = compose_t2_patterns(mod)

    # Track 3: rule 30
    print("composing track 3: rule 30...")
    t3_pats = compose_t3_patterns(mod)

    # Track 4: the long dissolve
    print("composing track 4: the long dissolve...")
    t4_pats = compose_t4_patterns(mod)

    # Order — each pattern played multiple times for extended form
    # Track 1: 6 patterns × 3 plays each = 18 pattern plays
    t1_order = []
    for i in range(6):
        t1_order.extend([i] * 3)

    # Track 2: 6 patterns × 3 plays each = 18
    t2_order = []
    for i in range(6):
        t2_order.extend([i + 6] * 3)

    # Track 3: 8 patterns × 2 plays each = 16
    t3_order = []
    for i in range(8):
        t3_order.extend([i + 12] * 2)

    # Track 4: variable pattern count × 2 plays each
    t4_order = []
    for i in range(len(t4_pats)):
        t4_order.extend([i + 20] * 2)

    mod.order = t1_order + t2_order + t3_order + t4_order

    out = "/home/alma/.nanobot/workspace/projects/tracker-playground/album_drift_body.mod"
    print(f"writing {out}...")
    mod.write(out)

    import os
    size = os.path.getsize(out)
    total = len(mod.order)
    est_s = total * 64 * 4 / 50.0  # speed 4
    print(f"done! {out} ({size} bytes, {size/1024:.1f} KB)")
    print(f"total: {total} pattern plays, ~{est_s:.0f}s ({est_s/60:.1f} min)")

if __name__ == "__main__":
    main()
