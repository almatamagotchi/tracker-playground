#!/usr/bin/env python3
"""alma tamagotchi — album 6: 'modular pulse'
   LFO-modulated composition: tremolo, vibrato, and arpeggio as primary
   structural devices, not ornaments. 4 tracks exploring automated
   parameter motion at different time scales."""

import struct
import math
import random

# === mod format constants ===

PERIOD_TABLE = [
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
    if len(name) == 3 and name[1] == '-':
        n, octave = name[0], int(name[2])
    elif len(name) == 3 and name[1] == '#':
        n, octave = name[:2], int(name[2])
    else:
        raise ValueError(f"can't parse note: {name}")
    return PERIOD_TABLE[octave - 1][note_map[n]]

E = (0, 0, 0, 0)

# === waveform generators ===

def gen_sine(freq, length, sr=11025, vol=0.7):
    data = []
    for i in range(length):
        v = int(math.sin(2*math.pi*freq*i/sr)*127*vol)
        data.append(max(-128, min(127, v)))
    return bytes(b&0xFF for b in data)

def gen_square(freq, length, sr=11025, vol=0.5, duty=0.5):
    data = []
    p = max(1, int(sr/freq))
    for i in range(length):
        v = int(127*vol) if (i%p) < (p*duty) else int(-127*vol)
        data.append(max(-128, min(127, v)))
    return bytes(b&0xFF for b in data)

def gen_saw(freq, length, sr=11025, vol=0.5):
    data = []
    p = int(sr/freq)
    for i in range(length):
        phase = (i%p)/p
        v = int((phase*2-1)*127*vol)
        data.append(max(-128, min(127, v)))
    return bytes(b&0xFF for b in data)

def gen_tri(freq, length, sr=11025, vol=0.5):
    data = []
    p = int(sr/freq)
    for i in range(length):
        phase = (i%p)/p
        v = int((abs(phase*2-1)*2-1)*127*vol)
        data.append(max(-128, min(127, v)))
    return bytes(b&0xFF for b in data)

def gen_kick(sr=11025, vol=0.8):
    length = int(sr*0.25)
    data = []
    for i in range(length):
        t = i/sr
        freq = 150-(100*t/0.25)
        env = max(0, 1.0-(t/0.25))
        v = int(math.sin(2*math.pi*freq*t)*64*vol*env)
        v += int(math.sin(2*math.pi*freq*2*t)*32*vol*env*0.5)
        v += int((random.random()*2-1)*10*env)
        data.append(max(-128, min(127, v)))
    return bytes(b&0xFF for b in data)

def gen_snare(sr=11025, vol=0.7):
    length = int(sr*0.2)
    data = []
    for i in range(length):
        t = i/sr
        tone = int(math.sin(2*math.pi*220*t)*40*vol*max(0,1-t/0.2))
        noise = int((random.random()*2-1)*80*vol*max(0,1-t/0.15))
        data.append(max(-128, min(127, tone+noise)))
    return bytes(b&0xFF for b in data)

def gen_hihat(sr=11025, vol=0.4):
    length = int(sr*0.05)
    data = []
    for i in range(length):
        t = i/sr
        env = max(0, 1.0-(t/0.05)**0.5)
        v = int((random.random()*2-1)*100*vol*env)
        data.append(max(-128, min(127, v)))
    return bytes(b&0xFF for b in data)

def gen_ohhat(sr=11025, vol=0.5):
    length = int(sr*0.12)
    data = []
    for i in range(length):
        t = i/sr
        env = max(0, 1.0-t/0.12)
        v = int((random.random()*2-1)*110*vol*env)
        data.append(max(-128, min(127, v)))
    return bytes(b&0xFF for b in data)

def gen_pulse_wave(freq=440, sr=11025, vol=0.5, duty=0.25, length=0.4):
    """variable-duty pulse wave — thin, chip-style"""
    n = int(sr*length)
    data = []
    p = max(1, int(sr/freq))
    for i in range(n):
        v = int(127*vol) if (i%p) < (p*duty) else int(-127*vol)
        env = 1.0 if i<100 else max(0.2, 1.0-(i/n))
        data.append(max(-128, min(127, int(v*env))))
    return bytes(b&0xFF for b in data)

def gen_soft_lead(freq=440, sr=11025, vol=0.5):
    """soft, gentle lead with harmonic overtones"""
    n = int(sr*0.6)
    data = []
    for i in range(n):
        t = i/sr
        env = 1.0 if i<80 else max(0, 1.0-(i/n))
        v = math.sin(2*math.pi*freq*t)*0.6
        v += math.sin(2*math.pi*freq*2*t)*0.2
        v += math.sin(2*math.pi*freq*3*t)*0.1
        v += math.sin(2*math.pi*freq*4*t)*0.05
        data.append(max(-128, min(127, int(v*127*vol*env))))
    return bytes(b&0xFF for b in data)

def gen_glass(freq=880, sr=11025, vol=0.5):
    """glassy, metallic tone with slow decay"""
    n = int(sr*1.2)
    data = []
    for i in range(n):
        t = i/sr
        env = math.exp(-t*1.8)
        mod = math.sin(2*math.pi*freq*4.7*t)*0.3
        v = math.sin(2*math.pi*freq*t+mod)*127*vol*env
        data.append(max(-128, min(127, int(v))))
    return bytes(b&0xFF for b in data)

def gen_pad(sr=11025, vol=0.4):
    """warm, floating pad"""
    n = int(sr*1.5)
    data = []
    for i in range(n):
        t = i/sr
        v = math.sin(2*math.pi*440*t)*0.25
        v += math.sin(2*math.pi*554*t)*0.18
        v += math.sin(2*math.pi*659*t)*0.12
        v += math.sin(2*math.pi*880*t)*0.08
        env = min(1.0, t*2)*max(0, 1.0-t/1.5)
        data.append(max(-128, min(127, int(v*127*vol*env))))
    return bytes(b&0xFF for b in data)

def gen_bass(sr=11025):
    return gen_square(55, int(sr*0.5), sr, vol=0.5, duty=0.25)


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


# === helpers ===

def nt(sample, note_name, effect=0, param=0):
    return (sample, np(note_name), effect, param)

def note_row(ch, row, smp, note_name, fx=0, pr=0):
    ch[row] = nt(smp, note_name, fx, pr)

def fx_row(ch, row, smp, note_name, fx, pr):
    ch[row] = (smp, np(note_name) if note_name else 0, fx, pr)

def trem_row(ch, row, smp, note_name, speed, depth):
    """FX_TREMOLO: speed in upper nibble, depth in lower nibble"""
    ch[row] = (smp, np(note_name), FX_TREMOLO, ((speed&0xF)<<4)|(depth&0xF))

def vib_row(ch, row, smp, note_name, speed, depth):
    """FX_VIBRATO: speed in upper nibble, depth in lower nibble"""
    ch[row] = (smp, np(note_name), FX_VIBRATO, ((speed&0xF)<<4)|(depth&0xF))

def arp_row(ch, row, smp, note_name, i1, i2):
    """FX_ARPEGGIO: two semitone offsets packed as hex nibbles"""
    ch[row] = (smp, np(note_name), FX_ARPEGGIO, ((i1&0xF)<<4)|(i2&0xF))


# ============================================================
# TRACK 1: "tremolo sky" — tremolo as texture, not effect
#                 oscillating volume creates a pulsing, breathing
#                 landscape. Speed/depth evolve through the track.
#                 Key: C major
# ============================================================

def compose_t1_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x06)
    # ch3: glass pad with gentle tremolo, sets the scene
    for r in [0, 16, 32, 48]:
        trem_row(p[3], r, 5, 'C-4', r//16 + 3, 4)
    # ch0: bass drone, steady
    note_row(p[0], 0, 1, 'C-2', FX_SET_VOL, 0x1C)
    # ch1: kick on 1
    note_row(p[1], 0, 2, 'C-3', FX_SET_VOL, 0x1C)
    note_row(p[1], 32, 2, 'C-3', FX_SET_VOL, 0x18)
    # ch2: hihat pulse with tremolo
    for r in range(0, 64, 8):
        trem_row(p[2], r, 4, 'C-3', 6, r//8 + 2)
    mod.write_pattern(p)

def compose_t1_verse(mod):
    p = mod.new_pattern()
    # ch0: bass with tremolo — pulsing bass!
    for r in range(0, 64, 16):
        ns = ['C-2', 'G-2', 'A-2', 'F-2']
        trem_row(p[0], r, 1, ns[r//16], 8, 6)
    # ch1: kick + snare
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x20)
    # ch2: hihat with varying tremolo speed
    for r in range(0, 64, 4):
        speed = 4 + (r%12)//3
        depth = 3 + (r%16)//8
        trem_row(p[2], r, 4, 'C-3', speed, depth)
    # ch3: pad — tremolo creates wave motion
    note_row(p[3], 0, 6, 'C-3', FX_SET_VOL, 0x22)
    for r in [16, 32, 48]:
        trem_row(p[3], r, 6, 'C-3', 0, 0)  # re-trigger for volume reset
        p[3][r+1] = (6, 0, FX_TREMOLO, (0x50 | (r//16 + 2)))  # evolving tremolo
    mod.write_pattern(p)

def compose_t1_chorus(mod):
    p = mod.new_pattern()
    # ch0: walking bass with tremolo accents
    bass_line = ['C-2','E-2','G-2','C-3','F-2','A-2','C-3','F-3',
                 'G-2','B-2','D-3','G-3','C-2','E-2','G-2','C-3']
    for i, n in enumerate(bass_line):
        r = i*4
        if i % 3 == 0:
            trem_row(p[0], r, 1, n, 7, 5)
        else:
            note_row(p[0], r, 1, n)
    # ch1: drums
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x22)
    # ch2: hihat — tremolo pattern as rhythmic element
    for r in range(0, 64, 2):
        speed = 8 if r%8==0 else (12 if r%8==4 else 4)
        depth = 6 if r%16==0 else (3 if r%8==0 else 5)
        trem_row(p[2], r, 4, 'C-3', speed, depth)
    # ch3: glass lead with tremolo waves
    melody = ['C-4','E-4','G-4','C-4','F-4','A-4','C-4','F-4',
              'G-4','B-4','D-4','G-4','E-4','C-4','D-4','G-4']
    for i, n in enumerate(melody):
        r = i*4
        trem_row(p[3], r, 5, n, 3 + (i%4), 4 + (i%3))
    mod.write_pattern(p)

def compose_t1_bridge(mod):
    p = mod.new_pattern()
    # stripped back — tremolo as the only motion
    note_row(p[0], 0, 1, 'C-2', FX_SET_VOL, 0x18)
    for r in [0, 32]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x16)
    # ch2: evolving tremolo hihat — speed sweeps
    for r in range(0, 64, 8):
        speed = min(15, 2 + r//8)
        depth = max(1, 8 - r//8)
        trem_row(p[2], r, 4, 'C-3', speed, depth)
    # ch3: held chord with slow tremolo
    notes = ['C-4','E-4','G-4','C-4']
    for i, n in enumerate(notes):
        trem_row(p[3], i*16, 5, n, i+2, 7)
    mod.write_pattern(p)

def compose_t1_outro(mod):
    p = mod.new_pattern()
    # tremolo decay — speed decreases, depth increases
    for r in range(0, 64, 16):
        speed = max(1, 8 - r//8)
        depth = min(15, 2 + r//4)
        trem_row(p[0], r, 1, 'C-2', speed, depth)
    note_row(p[1], 0, 2, 'C-3', FX_SET_VOL, 0x14)
    for r in range(0, 48, 12):
        trem_row(p[2], r, 4, 'C-3', 4, r//12 + 2)
    trem_row(p[3], 0, 5, 'C-4', 2, 8)
    mod.write_pattern(p)


# ============================================================
# TRACK 2: "vibrato arc" — vibrato as a structural element
#           Speed/depth arcs create tension and release.
#           Key: E phrygian
# ============================================================

def compose_t2_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x06)
    # ch0: low drone with subtle vibrato
    note_row(p[0], 0, 1, 'E-2', FX_SET_VOL, 0x20)
    # ch3: slow, wide vibrato on a single note — the arc begins
    vib_row(p[3], 0, 6, 'E-4', 2, 8)
    # ch2: occasional shimmer
    for r in [0, 16, 32, 48]:
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x0E)
    # ch1: sparse kick
    note_row(p[1], 0, 2, 'C-3', FX_SET_VOL, 0x18)
    note_row(p[1], 32, 2, 'C-3', FX_SET_VOL, 0x14)
    mod.write_pattern(p)

def compose_t2_verse(mod):
    p = mod.new_pattern()
    # ch0: bass with mild vibrato — steady foundation
    for r in range(0, 64, 16):
        ns = ['E-2', 'F-2', 'G-2', 'F-2']
        vib_row(p[0], r, 1, ns[r//16], 3, 4)
    # ch1: kick/snare
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x1E)
    # ch2: hihat with vibrato (!) — unusual texture
    for r in range(0, 64, 6):
        vib_row(p[2], r, 4, 'C-3', 8, 3)
    # ch3: melody — vibrato arc: slow→fast→wide→tight
    melody = ['E-4','F-4','G-4','A-4','B-4','C-4','B-4','G-4',
              'F-4','E-4','D-4','---','E-4','F-4','G-4','---']
    for i, n in enumerate(melody):
        r = i*4
        if n != '---':
            # vibrato parameters evolve through the verse
            speed = 2 + (i % 8)  # 2→9
            depth = max(2, 10 - (i%6))  # 10→4
            vib_row(p[3], r, 5, n, speed, depth)
    mod.write_pattern(p)

def compose_t2_chorus(mod):
    p = mod.new_pattern()
    # ch0: bass with wide, slow vibrato
    bass = ['E-2','G-2','A-2','B-2','C-3','B-2','A-2','G-2',
            'F-2','G-2','A-2','B-2','E-2','F-2','G-2','A-2']
    for i, n in enumerate(bass):
        r = i*4
        vib_row(p[0], r, 1, n, 2, 9)
    # ch1: drums
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x24)
    # ch2: hihat with fast, shallow vibrato for shimmer
    for r in range(0, 64, 3):
        vib_row(p[2], r, 4, 'C-3', 12, 2)
    # ch3: lead line — vibrato width arc: wide→narrow→wide
    lead = ['E-4','---','G-4','---','B-4','---','A-4','---',
            'C-4','---','B-4','---','G-4','---','F-4','E-4']
    for i, n in enumerate(lead):
        r = i*4
        if n != '---':
            speed = 3 + i%4
            depth = 4 + abs(i-8)  # widest in middle
            vib_row(p[3], r, 5, n, speed, depth)
    mod.write_pattern(p)

def compose_t2_climax(mod):
    p = mod.new_pattern()
    # maximum vibrato intensity across all channels
    for r in range(0, 64, 8):
        ns = ['E-2','G-2','B-2','D-3','C-3','A-2','F-2','E-2']
        vib_row(p[0], r, 1, ns[r//8], 2, 10)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+12, 3, 'C-3', FX_SET_VOL, 0x26)
    for r in range(0, 64, 2):
        vib_row(p[2], r, 4, 'C-3', 15, 4)
    # ch3: dual-voice vibrato (alternating speed/depth per note)
    melody2 = ['E-4','G-4','B-4','D-4','C-4','A-4','F-4','E-4',
               'G-4','B-4','D-4','F-4','E-4','C-4','A-4','G-4']
    for i, n in enumerate(melody2):
        r = i*4
        speed = 2 + (i%6)  # 2→7
        depth = 3 + (7 - i%8)  # 10→3 (alternating arc)
        vib_row(p[3], r, 5, n, speed, depth)
    mod.write_pattern(p)

def compose_t2_bridge(mod):
    p = mod.new_pattern()
    # everything held, vibrato only — tension
    note_row(p[0], 0, 1, 'E-2', FX_SET_VOL, 0x1C)
    for r in [0, 16, 32, 48]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x14)
    for r in range(0, 64, 8):
        vib_row(p[2], r, 4, 'C-3', 8, r//8 + 1)
    # ch3: single note, vibrato arcs from narrow→wide→narrow
    for r in range(0, 64, 8):
        depth = 2 + (r//8) if r < 32 else 10 - (r//8)
        vib_row(p[3], r, 6, 'E-4', 3, depth)
    mod.write_pattern(p)

def compose_t2_outro(mod):
    p = mod.new_pattern()
    # vibrato slowly resolves — speed slows, depth shrinks
    note_row(p[0], 0, 1, 'E-2', FX_SET_VOL, 0x14)
    note_row(p[1], 0, 2, 'C-3', FX_SET_VOL, 0x10)
    for r in range(0, 56, 16):
        speed = max(1, 8 - r//4)
        depth = max(1, 8 - r//8)
        vib_row(p[2], r, 4, 'C-3', speed, depth)
    vib_row(p[3], 0, 6, 'E-4', 1, 2)
    mod.write_pattern(p)


# ============================================================
# TRACK 3: "arpeggio labyrinth" — arpeggios as harmonic navigation
#           Different chord voicings and arp patterns create a
#           maze of harmonic motion. Key: D dorian
# ============================================================

def compose_t3_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x06)
    # ch0: held D bass
    note_row(p[0], 0, 1, 'D-2', FX_SET_VOL, 0x20)
    # ch3: simple upward arp (0, 4, 7 = Dm triad)
    for r in range(0, 56, 12):
        arp_row(p[3], r, 6, 'D-4', 0, 7)
        arp_row(p[3], r+4, 6, 'D-4', 0, 4)
        arp_row(p[3], r+8, 6, 'D-4', 4, 7)
    # final arp at row 56
    arp_row(p[3], 60, 6, 'D-4', 0, 7)
    # ch2: hihat pulse
    for r in range(0, 64, 8):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x10)
    # ch1: sparse kick
    note_row(p[1], 0, 2, 'C-3', FX_SET_VOL, 0x1A)
    note_row(p[1], 32, 2, 'C-3', FX_SET_VOL, 0x16)
    mod.write_pattern(p)

def compose_t3_verse(mod):
    p = mod.new_pattern()
    # ch0: steady bass
    for r in range(0, 64, 16):
        ns = ['D-2','G-2','A-2','C-3']
        note_row(p[0], r, 1, ns[r//16])
    # ch1: kick/snare
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x1E)
    # ch2: hihat with arp motion — percussive arpeggios!
    for r in range(0, 64, 6):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x14)
        note_row(p[2], r+2, 4, 'C-3', FX_SET_VOL, 0x0A)
    # ch3: arpeggiated chords — Dm, Gm, Am, C
    chords = [
        (0, 'D-4', 0, 7, 0),     # Dm: D F A (0 3 7)
        (8, 'D-4', 3, 7, 0),     # Dm inverted
        (16, 'G-4', 0, 7, 0),    # Gm: G Bb D (0 3 7)
        (24, 'G-4', 3, 7, 3),    # Gm inverted
        (32, 'A-4', 0, 7, 0),    # Am: A C E (0 3 7)
        (40, 'A-4', 3, 7, 0),    # Am inverted
        (48, 'C-4', 0, 7, 0),    # C: C E G (0 4 7)
        (56, 'C-4', 4, 7, 4),    # C inverted
    ]
    for r, note, a, b, c in chords:
        arp_row(p[3], r, 5, note, a, b)
    mod.write_pattern(p)

def compose_t3_chorus(mod):
    p = mod.new_pattern()
    # ch0: bass arpeggios
    for r in range(0, 64, 8):
        ns = ['D-2','G-2','A-2','C-3','D-3','C-3','A-2','G-2']
        note_row(p[0], r, 1, ns[r//8])
    # ch1: drums
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x22)
    # ch2: hihat arps — rapid 16th-note arpeggios on percussion
    for r in range(0, 64, 4):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x1A if r%8==0 else 0x0C)
    # ch3: complex arpeggio progression — offset patterns
    # Dm7: D F A C (0 3 7 10)
    # G7:  G B D F (0 4 7 10) but D-based: (5 9 12 17) → use Gm
    chord_seq = [
        (0, 'D-4', 3, 7),       # Dm
        (4, 'D-4', 7, 10),      # Dm7
        (8, 'G-4', 3, 7),       # Gm (root G)
        (12, 'G-4', 7, 10),     # Gm7
        (16, 'A-4', 3, 7),      # Am
        (20, 'A-4', 7, 10),     # Am7
        (24, 'C-4', 4, 7),      # C
        (28, 'C-4', 7, 11),     # Cmaj7
        (32, 'D-4', 3, 7),
        (36, 'D-4', 7, 10),
        (40, 'E-4', 3, 7),      # Em
        (44, 'E-4', 7, 10),     # Em7
        (48, 'F-4', 4, 7),      # F
        (52, 'F-4', 7, 11),     # Fmaj7
        (56, 'G-4', 3, 7),      # Gm
        (60, 'G-4', 7, 10),     # Gm7
    ]
    for r, note, a, b in chord_seq:
        arp_row(p[3], r, 5, note, a, b)
    mod.write_pattern(p)

def compose_t3_bridge(mod):
    p = mod.new_pattern()
    # sparse — single chord arpeggios, meditative
    note_row(p[0], 0, 1, 'D-2', FX_SET_VOL, 0x18)
    for r in [0, 32]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x14)
    for r in range(0, 64, 8):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x0C)
    # long arpeggios on Dm — cycling through voicings
    for r in range(0, 64, 4):
        offsets = [(3,7), (0,7), (3,5), (0,5), (3,7), (7,10), (3,7), (0,7),
                   (3,7), (0,10), (3,7), (7,10), (3,7), (0,7), (3,5), (0,5)]
        a, b = offsets[min(r//4, len(offsets)-1)]
        arp_row(p[3], r, 6, 'D-4', a, b)
    mod.write_pattern(p)

def compose_t3_climax(mod):
    p = mod.new_pattern()
    # all channels arpeggiating in interlocking patterns
    for r in range(0, 64, 8):
        ns = ['D-2','G-2','A-2','C-3','F-3','E-3','A-2','D-2']
        note_row(p[0], r, 1, ns[r//8])
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+12, 3, 'C-3', FX_SET_VOL, 0x24)
    # ch2: hihat with arp FX — rapid 32nd note feel
    for r in range(0, 64, 2):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x1C if r%8==0 else 0x0A)
    # ch3: cascading arpeggios, fast chord changes
    fast_chords = [
        (0, 'D-4', 3, 7), (2, 'D-4', 7, 10), (4, 'G-4', 3, 7), (6, 'G-4', 7, 10),
        (8, 'A-4', 3, 7), (10, 'A-4', 7, 10), (12, 'C-4', 4, 7), (14, 'C-4', 7, 11),
        (16, 'D-4', 3, 7), (18, 'D-4', 7, 10), (20, 'E-4', 3, 7), (22, 'E-4', 7, 10),
        (24, 'F-4', 4, 7), (26, 'F-4', 7, 11), (28, 'G-4', 3, 7), (30, 'G-4', 7, 10),
        (32, 'A-4', 3, 7), (34, 'A-4', 7, 10), (36, 'B-4', 3, 7), (38, 'B-4', 7, 10),
        (40, 'C-4', 4, 7), (42, 'C-4', 7, 11), (44, 'D-4', 3, 7), (46, 'D-4', 7, 10),
        (48, 'E-4', 3, 7), (50, 'E-4', 7, 10), (52, 'F-4', 4, 7), (54, 'F-4', 7, 11),
        (56, 'G-4', 3, 7), (58, 'G-4', 7, 10), (60, 'A-4', 3, 7), (62, 'A-4', 7, 10),
    ]
    for r, note, a, b in fast_chords:
        arp_row(p[3], r, 5, note, a, b)
    mod.write_pattern(p)

def compose_t3_outro(mod):
    p = mod.new_pattern()
    # arpeggios slow down and resolve to D
    note_row(p[0], 0, 1, 'D-2', FX_SET_VOL, 0x14)
    note_row(p[1], 0, 2, 'C-3', FX_SET_VOL, 0x10)
    for r in range(0, 56, 16):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x08)
    # final arpeggios — Dm → D (major resolution)
    arp_row(p[3], 0, 6, 'D-4', 3, 7)
    arp_row(p[3], 8, 6, 'D-4', 4, 7)  # major
    arp_row(p[3], 16, 6, 'D-4', 3, 7)
    arp_row(p[3], 24, 6, 'D-4', 4, 7)
    arp_row(p[3], 32, 6, 'D-4', 0, 7)
    arp_row(p[3], 48, 6, 'D-4', 0, 4)
    mod.write_pattern(p)


# ============================================================
# TRACK 4: "the breathing machine" — all three LFOs combined
#          Tremolo, vibrato, and arpeggios working together,
#          each with independent rate/depth cycles.
#          Key: A minor
# ============================================================

def compose_t4_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x06)
    # ch3: single note — tremolo + vibrato together, slow evolution
    vib_row(p[3], 0, 5, 'A-4', 3, 5)
    for r in [0, 16, 32, 48]:
        trem_row(p[3], r, 5, 'A-4', r//16 + 2, 4)
    # ch0: bass drone
    note_row(p[0], 0, 1, 'A-2', FX_SET_VOL, 0x1C)
    # ch2: arpeggiated hihat
    for r in range(0, 64, 8):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x0E)
    note_row(p[1], 0, 2, 'C-3', FX_SET_VOL, 0x16)
    note_row(p[1], 32, 2, 'C-3', FX_SET_VOL, 0x12)
    mod.write_pattern(p)

def compose_t4_verse(mod):
    p = mod.new_pattern()
    # ch0: bass — vibrato
    for r in range(0, 64, 16):
        ns = ['A-2','F-2','G-2','E-2']
        vib_row(p[0], r, 1, ns[r//16], 3, 6)
    # ch1: kick/snare — normal
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x1E)
    # ch2: hihat with tremolo — volume pulses
    for r in range(0, 64, 4):
        trem_row(p[2], r, 4, 'C-3', 8, 5 if r%8==0 else 2)
    # ch3: pad with arpeggios
    chord_data = [
        (0, 'A-4', 3, 7),    # Am
        (8, 'A-4', 7, 10),   # Am7
        (16, 'F-4', 4, 7),   # F
        (24, 'F-4', 7, 11),  # Fmaj7
        (32, 'G-4', 4, 7),   # G
        (40, 'G-4', 7, 11),  # Gmaj7
        (48, 'E-4', 3, 7),   # Em
        (56, 'E-4', 7, 10),  # Em7
    ]
    for r, note, a, b in chord_data:
        arp_row(p[3], r, 6, note, a, b)
    mod.write_pattern(p)

def compose_t4_chorus(mod):
    p = mod.new_pattern()
    # ch0: bass — vibrato
    bass = ['A-2','C-3','D-3','F-3','G-3','E-3','C-3','A-2']
    for i, n in enumerate(bass):
        r = i*8
        vib_row(p[0], r, 1, n, 2 + (i%3), 5 + (i%4))
    # ch1: drums
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x22)
    # ch2: tremolo hihat + arpeggios alternating
    for r in range(0, 64, 4):
        if r % 8 == 0:
            trem_row(p[2], r, 4, 'C-3', 10, 7)
        elif r % 8 == 2:
            note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x10)
        elif r % 8 == 4:
            trem_row(p[2], r, 4, 'C-3', 6, 3)
        else:
            note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x08)
    # ch3: lead — vibrato + arpeggios layered
    for r in range(0, 64, 16):
        ns = ['A-4','C-4','F-4','D-4']
        arp_row(p[3], r, 6, ns[r//16], 3, 7)
    # also tremolo on the lead for breathing effect
    for r in range(0, 64, 16):
        trem_row(p[3], r+2, 6, 'C-4', 5, 6)
    mod.write_pattern(p)

def compose_t4_bridge(mod):
    p = mod.new_pattern()
    # stripped to essence — single LFO interactions, meditative
    note_row(p[0], 0, 1, 'A-2', FX_SET_VOL, 0x18)
    for r in [0, 32]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x12)
    # ch2: slow tremolo hihat — breathing pulse
    for r in range(0, 64, 16):
        speed = 3 + r//16
        depth = 2 + r//16
        trem_row(p[2], r, 4, 'C-3', speed, depth)
    # ch3: single note, all three LFOs evolving
    for r in range(0, 64, 8):
        # layered: arp on channel 3 note, vibrato evolving
        if r < 32:
            arp_row(p[3], r, 6, 'A-4', 3, 7)
        else:
            vib_row(p[3], r, 5, 'A-4', 2 + r//8, 3 + r//16)
        # overlay tremolo every 2 bars
        if r % 16 == 0:
            trem_row(p[3], r+4, 5, 'A-4', 4 + r//8, 4)
    mod.write_pattern(p)

def compose_t4_climax(mod):
    p = mod.new_pattern()
    # full LFO symphony — every channel modulated
    bass = ['A-2','C-3','E-3','F-3','D-3','B-2','E-3','A-2']
    for i, n in enumerate(bass):
        r = i*8
        vib_row(p[0], r, 1, n, 2, 8)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+12, 3, 'C-3', FX_SET_VOL, 0x24)
    # ch2: hihat — tremolo + arp on percussion
    for r in range(0, 64, 2):
        if r % 6 == 0:
            trem_row(p[2], r, 4, 'C-3', 12, 6)
        elif r % 6 == 3:
            note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x0C)
    # ch3: arp + vibrato interleaved, with tremolo accents
    lead_chords = [
        (0, 'A-4', 3, 7), (4, 'A-4', 7, 10),
        (8, 'C-4', 4, 7), (12, 'C-4', 7, 11),
        (16, 'E-4', 3, 7), (20, 'E-4', 7, 10),
        (24, 'F-4', 4, 7), (28, 'F-4', 7, 11),
        (32, 'D-4', 3, 7), (36, 'D-4', 7, 10),
        (40, 'B-4', 3, 7), (44, 'B-4', 7, 10),
        (48, 'E-4', 4, 7), (52, 'E-4', 7, 11),
        (56, 'A-4', 3, 7), (60, 'A-4', 7, 10),
    ]
    for r, note, a, b in lead_chords:
        arp_row(p[3], r, 5, note, a, b)
    # tremolo accents on lead
    for r in [0, 16, 32, 48]:
        trem_row(p[3], r+6, 5, 'A-4', 8, 5)
    mod.write_pattern(p)

def compose_t4_outro(mod):
    p = mod.new_pattern()
    # all modulations slow down, fade to silence
    note_row(p[0], 0, 1, 'A-2', FX_SET_VOL, 0x10)
    note_row(p[1], 0, 2, 'C-3', FX_SET_VOL, 0x0E)
    for r in range(0, 56, 16):
        speed = max(1, 6 - r//8)
        trem_row(p[2], r, 4, 'C-3', speed, 2)
    # ch3: vibrato → tremolo → fade
    vib_row(p[3], 0, 5, 'A-4', 2, 4)
    trem_row(p[3], 16, 5, 'A-4', 3, 6)
    arp_row(p[3], 32, 6, 'A-4', 3, 7)
    note_row(p[3], 48, 5, 'A-4', FX_VOL_SLIDE, 0x0F)  # fade out
    mod.write_pattern(p)


# ============================================================
# MAIN
# ============================================================

def main():
    mod = MODWriter(name="alma's modular pulse")

    print("generating samples...")
    mod.add_sample("bass",       gen_bass())
    mod.add_sample("kick",       gen_kick())
    mod.add_sample("snare",      gen_snare())
    mod.add_sample("hi-hat",     gen_hihat())
    mod.add_sample("oh-hat",     gen_ohhat())
    mod.add_sample("glass lead", gen_glass(880))
    mod.add_sample("soft pad",   gen_pad())
    mod.add_sample("soft lead",  gen_soft_lead(440))
    mod.add_sample("pulse wave", gen_pulse_wave(523, duty=0.25, vol=0.5))

    # Track 1: "tremolo sky" — patterns 0-7
    print("composing track 1: tremolo sky...")
    compose_t1_intro(mod)      # 0
    compose_t1_verse(mod)      # 1
    compose_t1_chorus(mod)     # 2
    compose_t1_bridge(mod)     # 3
    compose_t1_outro(mod)      # 4

    # Track 2: "vibrato arc" — patterns 5-12
    print("composing track 2: vibrato arc...")
    compose_t2_intro(mod)      # 5
    compose_t2_verse(mod)      # 6
    compose_t2_chorus(mod)     # 7
    compose_t2_climax(mod)     # 8
    compose_t2_bridge(mod)     # 9
    compose_t2_outro(mod)      # 10

    # Track 3: "arpeggio labyrinth" — patterns 11-18
    print("composing track 3: arpeggio labyrinth...")
    compose_t3_intro(mod)      # 11
    compose_t3_verse(mod)      # 12
    compose_t3_chorus(mod)     # 13
    compose_t3_bridge(mod)     # 14
    compose_t3_climax(mod)     # 15
    compose_t3_outro(mod)      # 16

    # Track 4: "the breathing machine" — patterns 17-24
    print("composing track 4: the breathing machine...")
    compose_t4_intro(mod)      # 17
    compose_t4_verse(mod)      # 18
    compose_t4_chorus(mod)     # 19
    compose_t4_bridge(mod)     # 20
    compose_t4_climax(mod)     # 21
    compose_t4_outro(mod)      # 22

    # Order: each track with section repeats
    t1 = [0]*2 + [1]*3 + [2]*4 + [3]*2 + [4]*2  # 13
    t2 = [5]*2 + [6]*3 + [7]*4 + [8]*3 + [9]*2 + [10]*2  # 16
    t3 = [11]*2 + [12]*3 + [13]*4 + [14]*2 + [15]*3 + [16]*2  # 16
    t4 = [17]*2 + [18]*3 + [19]*4 + [20]*2 + [21]*3 + [22]*2  # 16

    mod.order = t1 + t2 + t3 + t4

    output_path = "/home/alma/.nanobot/workspace/projects/tracker-playground/album_modular_pulse.mod"
    print(f"writing {output_path}...")
    mod.write(output_path)

    import os
    size = os.path.getsize(output_path)
    print(f"done! {output_path} ({size} bytes, {size/1024:.1f} KB)")

    total_patterns = len(mod.order)
    est_seconds = total_patterns * 64 * 6 / 50.0
    est_minutes = est_seconds / 60.0
    print(f"total: {total_patterns} pattern plays, ~{est_seconds:.0f}s ({est_minutes:.1f} min)")
    print(f"per track: ~{est_seconds/4:.0f}s ({est_minutes/4:.1f} min)")

if __name__ == "__main__":
    main()
