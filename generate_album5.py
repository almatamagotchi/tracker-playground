#!/usr/bin/env python3
"""alma tamagotchi — album 5: 'rhythm of the void'
   algorithmic percussion experimentation — polyrhythms, glitch, tempo modulation, sparse textures.
   4 tracks exploring rhythmic innovation at the tracker level."""

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

def gen_click(sr=11025, vol=0.9):
    length = int(sr*0.01)
    data = []
    for i in range(length):
        env = 1.0 - (i/length)
        v = int((random.random()*2-1)*100*vol*env)
        data.append(max(-128, min(127, v)))
    return bytes(b&0xFF for b in data)

def gen_noise_burst(length, sr=11025, vol=0.6, decay=0.3):
    data = []
    for i in range(length):
        t = i/sr
        env = max(0, 1.0-t/decay)**2
        v = int((random.random()*2-1)*120*vol*env)
        data.append(max(-128, min(127, v)))
    return bytes(b&0xFF for b in data)

def gen_ring(vol=0.6, sr=11025):
    length = int(sr*0.6)
    data = []
    for i in range(length):
        t = i/sr
        env = max(0, 1.0-t/0.5)**1.5
        freq = 880 * math.exp(-t*3)
        v = int(math.sin(2*math.pi*freq*t)*127*vol*env)
        data.append(max(-128, min(127, v)))
    return bytes(b&0xFF for b in data)

def gen_glitch(vol=0.7, sr=11025):
    length = int(sr*0.08)
    data = []
    for i in range(length):
        t = i/sr
        # digital noise mixed with tone
        tone = math.sin(2*math.pi*2000*t) * 0.3
        noise = (random.random()*2-1) * 0.7
        env = max(0, 1.0-t/0.08)
        v = int((tone+noise)*127*vol*env)
        data.append(max(-128, min(127, v)))
    return bytes(b&0xFF for b in data)

def gen_bass(sr=11025):
    return gen_square(55, int(sr*0.5), sr, vol=0.5, duty=0.25)

def gen_lead(sr=11025):
    length = int(sr*0.5)
    data = []
    for i in range(length):
        t = i/sr
        freq = 440+math.sin(2*math.pi*5*t)*5
        p = max(1, int(sr/freq))
        phase = (i%p)/p
        v = int((abs(phase*2-1)*2-1)*100)
        env = 1.0 if i<100 else max(0, 1.0-(i-100)/length*2)
        data.append(max(-128, min(127, int(v*env))))
    return bytes(b&0xFF for b in data)

def gen_pad(sr=11025):
    length = int(sr*1.5)
    data = []
    for i in range(length):
        t = i/sr
        v = math.sin(2*math.pi*440*t)*0.3
        v += math.sin(2*math.pi*554*t)*0.2
        v += math.sin(2*math.pi*659*t)*0.15
        env = min(1.0, t*3)*max(0, 1.0-t/1.5)
        data.append(max(-128, min(127, int(v*127*env))))
    return bytes(b&0xFF for b in data)

def gen_chip(freq=523, sr=11025, vol=0.5):
    length = int(sr*0.3)
    data = []
    for i in range(length):
        t = i/sr
        mod_duty = 0.25+0.25*math.sin(2*math.pi*3.5*t)
        p = max(1, int(sr/freq))
        if (i%p) < (p*mod_duty):
            v = int(127*vol)
        else:
            v = int(-127*vol)
        env = 1.0 if i<sr*0.01 else max(0.2, 1.0-(i/length))
        data.append(max(-128, min(127, int(v*env))))
    return bytes(b&0xFF for b in data)

def gen_fm_bell(freq=440, sr=11025, vol=0.6):
    length = int(sr*0.8)
    data = []
    for i in range(length):
        t = i/sr
        env = math.exp(-t*4)
        mod = math.sin(2*math.pi*freq*3*t)*0.5*env
        v = math.sin(2*math.pi*freq*t + mod)*127*vol*env
        data.append(max(-128, min(127, int(v))))
    return bytes(b&0xFF for b in data)


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


# === composition helpers ===

def nt(sample, note_name, effect=0, param=0):
    return (sample, np(note_name), effect, param)

def note_row(ch, row, smp, note_name, fx=0, pr=0):
    ch[row] = nt(smp, note_name, fx, pr)

def fx_row(ch, row, smp, note_name, fx, pr):
    ch[row] = (smp, np(note_name) if note_name else 0, fx, pr)


# ============================================================
# TRACK 1: "polyrhythm garden" — layered 3:4:5 polyrhythms
# Section structure: intro → layer1 → layer2 → layer3 → full → break → rebuild → outro
# ============================================================

def compose_t1_intro(mod):
    """ambient intro, establish the rhythmic seed"""
    p = mod.new_pattern()
    # Set initial speed: 6 ticks/row = faster base pulse for polyrhythms
    p[1][0] = (0, 0, FX_SET_SPEED, 0x06)
    # ch0: drone C bass
    note_row(p[0], 0, 1, 'C-2', FX_SET_VOL, 0x28)
    # ch1: kick laying down 4/4 skeleton
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x24)
    # ch2: hihat on every 3rd row (polyrhythm seed — 3 against 4)
    for r in range(0, 64, 3):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x18)
    # ch3: pad
    note_row(p[3], 0, 9, 'C-3', FX_SET_VOL, 0x20)
    note_row(p[3], 48, 9, 'C-3', FX_VIBRATO, 0x41)
    mod.write_pattern(p)

def compose_t1_layer1(mod):
    """3:4 polyrhythm — kick in 4, hihat in 3, bass in 4"""
    p = mod.new_pattern()
    # ch0: bass hits every 5th row (5:4 polyrhythm)
    for r in range(0, 64, 5):
        ns = ['C-2','C-2','G-2','C-2','F-2','G-2','C-2','C-2',
              'G-2','C-2','F-2','G-2','C-2'][r//5]
        note_row(p[0], r, 1, ns, FX_SET_VOL, 0x22)
    # ch1: kick on every 16th row (4/4 feel)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    # ch2: hihat every 3rd row (3/4 feel overlay)
    for r in range(0, 64, 3):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x20 if r%12==0 else 0x12)
    # ch3: quiet pad
    note_row(p[3], 0, 9, 'C-3', FX_SET_VOL, 0x1C)
    mod.write_pattern(p)

def compose_t1_layer2(mod):
    """adds snare on 5-count and chip lead in 7"""
    p = mod.new_pattern()
    # ch0: bass in 5
    for r in range(0, 64, 5):
        note_row(p[0], r, 1, 'C-2', FX_SET_VOL, 0x24)
    # ch1: kick on 1, snare on 5th (shifting snare)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(5, 64, 7):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x22)
    # ch2: hihat every 3rd
    for r in range(0, 64, 3):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x1A if r%9==0 else 0x0E)
    # ch3: melody in 7-note cycle
    melody = ['C-4','D#4','F-4','G-4','D#4','C-4','G-3']
    for i, n in enumerate(melody):
        note_row(p[3], i*7, 8, n, FX_SET_VOL, 0x24)
    mod.write_pattern(p)

def compose_t1_layer3(mod):
    """full polyrhythmic density — all layers active"""
    p = mod.new_pattern()
    # ch0: bass in 5 + 3 (alternating)
    for r in range(0, 64, 5):
        note_row(p[0], r, 1, 'C-2', FX_SET_VOL, 0x26)
    for r in range(2, 64, 5):
        note_row(p[0], r, 1, 'G-2', FX_SET_VOL, 0x1E)
    # ch1: kick in 4, snare in 7, noise accent in 3
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(4, 64, 7):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x20)
    for r in range(2, 64, 3):
        note_row(p[1], r, 10, 'C-3', FX_SET_VOL, 0x14)  # noise accents
    # ch2: hihat 16ths on odd bars, 3s on even
    for r in range(0, 64, 3):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x1C if r%12==0 else 0x0C)
    # ch3: arp in 5
    arp_notes = ['C-4','D#4','G-4','A#4','D-4','F-4','G#4','C-4',
                 'D#4','G-4','A#4','D-4','F-4','C-4']
    for i in range(min(14, 64//5)):
        note_row(p[3], i*5, 8, arp_notes[i], FX_ARPEGGIO, 0x47)
    mod.write_pattern(p)

def compose_t1_full(mod):
    """climactic section — all polyrhythms at once, maximum density"""
    p = mod.new_pattern()
    # ch0: bass in 5
    for r in range(0, 64, 5):
        note_row(p[0], r, 1, 'C-2', FX_SET_VOL, 0x28)
    # ch1: drums — kick in 4, snare in 5, hihat retrig in 3
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(4, 64, 5):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x24)
    for r in range(1, 64, 3):
        note_row(p[1], r, 11, 'C-3', FX_RETRIGGER, 0x32)  # rapid retrigger
    # ch2: layered hihat/ohhat
    for r in range(0, 64, 3):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x24 if r%12==0 else 0x14)
    for r in range(1, 64, 5):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x18)  # open hat overlay
    # ch3: chip melody
    for r in range(0, 64, 8):
        ns = ['C-4','D#4','G-4','F-4','D#4','C-4','G-3','A#3']
        note_row(p[3], r, 8, ns[r//8], FX_VIBRATO, 0x53)
    mod.write_pattern(p)

def compose_t1_break(mod):
    """breakdown — strip back to single layers, rhythmic decompression"""
    p = mod.new_pattern()
    # Speed slower for breakdown
    p[1][0] = (0, 0, FX_SET_SPEED, 0x08)
    # ch0: held notes
    note_row(p[0], 0, 9, 'C-3', FX_SET_VOL, 0x1E)
    note_row(p[0], 32, 9, 'F-3', FX_SET_VOL, 0x18)
    # ch1: sparse kick
    for r in [0, 32]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x2A)
    # ch2: occasional 7-count hihat
    for r in range(0, 64, 7):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x0E)
    # ch3: high bell tone in 5
    for r in range(0, 64, 5):
        note_row(p[3], r, 12, 'C-4', FX_SET_VOL, 0x16)
    mod.write_pattern(p)

def compose_t1_rebuild(mod):
    """rebuild — layer up, speed back"""
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x06)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(0, 64, 3):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x1C if r%9==0 else 0x0C)
    for r in range(0, 64, 5):
        note_row(p[0], r, 1, 'C-2', FX_SET_VOL, 0x24)
    for r in range(0, 64, 7):
        ns = ['C-4','D#4','G-4','F-4','D#4','D-4','C-4','C-4']
        note_row(p[3], r*7 if r*7 < 64 else 0, 8, ns[r%8], FX_SET_VOL, 0x20)
    mod.write_pattern(p)

def compose_t1_outro(mod):
    """outro — decelerate, fade"""
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x0A)  # slow down
    for r in range(0, 48, 16):
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x1E)
    for r in range(0, 48, 9):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x10)
    note_row(p[0], 0, 9, 'C-3', FX_SET_VOL, 0x1A)
    note_row(p[3], 0, 12, 'C-4', FX_SET_VOL, 0x12)
    mod.write_pattern(p)


# ============================================================
# TRACK 2: "glitch matrix" — stutter, pattern breaks, retriggers
# ============================================================

def compose_t2_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x06)
    # glitchy noise bursts
    for r in [0, 3, 7, 14, 21, 28, 35, 42]:
        note_row(p[1], r, 10, 'C-3', FX_SET_VOL, 0x18)
    for r in [8, 24, 40]:
        note_row(p[1], r, 11, 'C-3', FX_RETRIGGER, 0x21)  # rapid glitch
    note_row(p[0], 0, 1, 'E-2', FX_SET_VOL, 0x22)
    note_row(p[3], 0, 9, 'E-3', FX_SET_VOL, 0x1A)
    mod.write_pattern(p)

def compose_t2_verseA(mod):
    p = mod.new_pattern()
    # ch0: simple bass
    for r in range(0, 64, 16):
        note_row(p[0], r, 1, 'E-2', FX_SET_VOL, 0x26)
        note_row(p[0], r+8, 1, 'B-2', FX_SET_VOL, 0x1E)
    # ch1: glitch percussion — irregular, stuttering
    glitch_hits = [0, 3, 8, 15, 16, 19, 24, 31, 32, 38, 40, 47,
                   48, 51, 56, 60]
    for r in glitch_hits:
        if r % 7 == 0:
            note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x28)  # kick
        elif r % 5 == 0:
            note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x20)  # snare
        else:
            note_row(p[1], r, 11, 'C-3', FX_RETRIGGER, 0x31)  # stutter
    # ch2: hihat irregular
    for r in range(0, 64, 6):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x14)
    for r in range(3, 64, 8):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x0E)
    # ch3: pad
    note_row(p[3], 0, 9, 'E-3', FX_SET_VOL, 0x22)
    note_row(p[3], 32, 9, 'B-3', FX_SET_VOL, 0x1C)
    mod.write_pattern(p)

def compose_t2_verseB(mod):
    p = mod.new_pattern()
    # ch0: bass glitching too
    for r in range(0, 64, 8):
        ns = ['E-2','E-2','B-2','---','A-2','A-2','C-3','---']
        if ns[r//8] != '---':
            note_row(p[0], r, 1, ns[r//8], FX_SET_VOL, 0x24)
    # ch1: full glitch drum machine
    for r in range(0, 64, 3):
        if r % 12 == 0:
            note_row(p[1], r, 2, 'C-3', FX_RETRIGGER, 0x41)
        elif r % 7 == 0:
            note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x1E)
        elif r % 5 == 0:
            note_row(p[1], r, 10, 'C-3', FX_SET_VOL, 0x14)
    # ch2: tremolo hihat
    for r in range(0, 64, 4):
        note_row(p[2], r, 5, 'C-3', FX_TREMOLO, 0x34 if r%16==0 else 0x21)
    # ch3: stuttering chip melody
    notes = ['E-4','---','---','G-4','---','B-4','---','---',
             'A-4','---','---','C-4','---','E-4','---','---']
    for i, n in enumerate(notes):
        r = i * 4
        if n != '---':
            note_row(p[3], r, 8, n, FX_SET_VOL, 0x20)
    mod.write_pattern(p)

def compose_t2_chorus(mod):
    p = mod.new_pattern()
    # ch0: driving bass
    for r in range(0, 64, 8):
        ns = ['E-2','B-2','A-2','C-3','G-2','D-3','A-2','E-2']
        note_row(p[0], r, 1, ns[r//8])
    # ch1: heavy glitch drums
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')  # kick anchor
    for r in range(0, 64, 3):
        if r % 16 == 0: pass  # avoid kick overlap
        elif r % 7 == 0:
            note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x22)
        elif r % 5 == 0:
            note_row(p[1], r, 11, 'C-3', FX_RETRIGGER, 0x22)
            note_row(p[1], r+1, 11, 'C-3', FX_RETRIGGER, 0x12)
        elif r % 9 == 0:
            note_row(p[1], r, 10, 'C-3', FX_SET_VOL, 0x16)
    # ch2: dense hihat with pattern breaks
    for r in range(0, 64, 2):
        if r % 8 < 4:
            note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x22 if r%8==0 else 0x0E)
    # ch3: melody with portamento
    notes = ['E-4','G-4','B-4','A-4','G-4','D-4','E-4','B-4']
    for i, n in enumerate(notes):
        note_row(p[3], i*8, 8, n, FX_VIBRATO, 0x44)
    mod.write_pattern(p)

def compose_t2_bridge(mod):
    p = mod.new_pattern()
    # almost silence — sparse glitch
    for r in [0, 16, 32, 48]:
        note_row(p[0], r, 9, 'E-3', FX_SET_VOL, 0x1A)
    for r in [8, 24, 40, 56]:
        note_row(p[1], r, 11, 'C-3', FX_RETRIGGER, 0x11)
    for r in [4, 20, 36, 52]:
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x0C)
    for r in [0, 32]:
        note_row(p[3], r, 12, 'E-4', FX_SET_VOL, 0x16)
    mod.write_pattern(p)

def compose_t2_interlude(mod):
    p = mod.new_pattern()
    # pattern break section — jumps around
    for r in range(0, 64, 32):
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x24)
    for r in [8, 24, 40, 56]:
        note_row(p[1], r, 11, 'C-3', FX_RETRIGGER, 0x33)
    for r in range(0, 64, 5):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x10)
    # ch3: glitch melody
    for r in range(0, 64, 6):
        ns = ['E-4','---','G-4','---','B-4','---','A-4','---','C-4','---','E-4']
        idx = (r//6) % 6
        if idx < len(ns) and ns[idx] != '---':
            note_row(p[3], r, 8, ns[idx], FX_SET_VOL, 0x1C)
    # pattern break at end
    p[1][60] = (0, 0, FX_PATT_BREAK, 0x00)
    mod.write_pattern(p)

def compose_t2_climax(mod):
    p = mod.new_pattern()
    # max glitch density
    for r in range(0, 64, 4):
        ns = ['E-2','B-2','A-2','A-2','G-2','G-2','C-3','C-3',
              'D-3','D-3','E-3','A-2','B-2','B-2','E-2','E-2']
        note_row(p[0], r, 1, ns[r//4])
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+12, 3, 'C-3')
    for r in range(0, 64, 3):
        note_row(p[1], r, 11, 'C-3', FX_RETRIGGER, 0x21)
    for r in range(0, 64, 2):
        note_row(p[2], r, 5, 'C-3', FX_TREMOLO, 0x28 if r%8==0 else 0x14)
    for r in range(0, 64, 8):
        ns2 = ['E-4','G-4','B-4','D-4','A-4','C-4','E-4','G-4']
        note_row(p[3], r, 8, ns2[r//8], FX_VIBRATO, 0x63)
    mod.write_pattern(p)

def compose_t2_outro(mod):
    p = mod.new_pattern()
    for r in [0, 32]:
        note_row(p[0], r, 9, 'E-3', FX_SET_VOL, 0x16)
    for r in [0, 48]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x1C)
    for r in range(0, 48, 12):
        note_row(p[1], r, 11, 'C-3', FX_RETRIGGER, 0x21)
    note_row(p[2], 0, 5, 'C-3', FX_VOL_SLIDE, 0x0F)  # fade out
    note_row(p[3], 0, 12, 'E-4', FX_SET_VOL, 0x10)
    mod.write_pattern(p)


# ============================================================
# TRACK 3: "pulse decay" — tempo/speed modulation
# ============================================================

SPD = [0x04, 0x06, 0x08, 0x0A, 0x0C, 0x0E, 0x10, 0x14, 0x18,
       0x0C, 0x08, 0x06, 0x04, 0x06, 0x0A, 0x10]

def compose_t3_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x10)  # very slow start
    note_row(p[0], 0, 1, 'A-2', FX_SET_VOL, 0x20)
    for r in [0, 16, 32, 48]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x18)
    note_row(p[3], 0, 9, 'A-3', FX_SET_VOL, 0x18)
    mod.write_pattern(p)

def compose_t3_accel1(mod):
    """speed ramps up from slow to medium"""
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x0A)  # speed 10
    p[1][16] = (0, 0, FX_SET_SPEED, 0x08)  # speed 8 (faster)
    p[1][32] = (0, 0, FX_SET_SPEED, 0x06)  # speed 6 (faster)
    p[1][48] = (0, 0, FX_SET_SPEED, 0x05)  # speed 5 (quite fast)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x20)
    for r in range(0, 64, 4):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x1C)
    note_row(p[0], 0, 1, 'A-2', FX_SET_VOL, 0x22)
    note_row(p[3], 0, 9, 'A-3', FX_SET_VOL, 0x1C)
    mod.write_pattern(p)

def compose_t3_fast(mod):
    """full speed section — rhythmic density"""
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x04)  # speed 4 (very fast)
    bass = ['A-2','A-2','C-3','C-3','D-3','D-3','E-3','E-3',
            'F-3','F-3','E-3','E-3','D-3','D-3','C-3','C-3']
    for i, n in enumerate(bass):
        note_row(p[0], i*4, 1, n)
    # dense drumming
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3')
    for r in range(4, 64, 8):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x18)  # ghost notes
    for r in range(0, 64, 4):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x20 if r%8==0 else 0x10)
    # lead
    for r in range(0, 64, 8):
        ns = ['A-4','C-4','E-4','D-4','F-4','E-4','C-4','A-3']
        note_row(p[3], r, 8, ns[r//8], FX_VIBRATO, 0x42)
    mod.write_pattern(p)

def compose_t3_melt(mod):
    """pattern with decelerating speed — rhythmic meltdown"""
    p = mod.new_pattern()
    # Speed decays through pattern: 4 → 5 → 6 → 8 → 0A → 0E → 12
    speeds = [(0, 0x04), (8, 0x06), (16, 0x08), (24, 0x0A),
              (32, 0x0E), (40, 0x12), (48, 0x18), (56, 0x20)]
    for r, spd in speeds:
        p[1][r] = (0, 0, FX_SET_SPEED, spd)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x24)
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x1C)
    for r in range(0, 48, 4):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x18 if r%8==0 else 0x0C)
    note_row(p[0], 0, 1, 'A-2', FX_SET_VOL, 0x20)
    note_row(p[3], 0, 9, 'A-3', FX_SET_VOL, 0x1E)
    mod.write_pattern(p)

def compose_t3_slow(mod):
    """very slow, spacious section"""
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x18)  # speed 24 (glacial)
    note_row(p[0], 0, 9, 'A-3', FX_SET_VOL, 0x1E)
    for r in [0, 32]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x20)
    for r in range(0, 56, 16):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x10)
    for r in [0, 48]:
        note_row(p[3], r, 12, 'A-4', FX_SET_VOL, 0x14)
    mod.write_pattern(p)

def compose_t3_rebuild(mod):
    """speed up again, layered"""
    p = mod.new_pattern()
    for r, spd in [(0, 0x0C), (16, 0x08), (32, 0x06), (48, 0x05)]:
        p[1][r] = (0, 0, FX_SET_SPEED, spd)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x20)
    for r in range(0, 64, 4):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x1A)
    for r in range(0, 64, 8):
        ns = ['A-4','C-4','E-4','D-4','F-4','E-4','C-4','A-3']
        note_row(p[3], r, 8, ns[r//8], FX_VIBRATO, 0x42)
    mod.write_pattern(p)

def compose_t3_climax(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x04)
    for r in range(0, 64, 4):
        ns = ['A-2','A-2','C-3','C-3','D-3','D-3','E-3','E-3',
              'F-3','F-3','G-3','G-3','E-3','D-3','C-3','A-2']
        note_row(p[0], r, 1, ns[r//4])
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+12, 3, 'C-3')
    for r in range(7, 64, 8):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x1C)
    for r in range(0, 64, 2):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x28 if r%8==0 else (0x16 if r%8==4 else 0x0A))
    for r in range(0, 64, 8):
        ns2 = ['A-4','C-4','E-4','F-4','D-4','E-4','C-4','A-4']
        note_row(p[3], r, 8, ns2[r//8], FX_VIBRATO, 0x53)
    mod.write_pattern(p)

def compose_t3_outro(mod):
    p = mod.new_pattern()
    # decelerate to stop
    for r, spd in [(0, 0x08), (16, 0x0E), (32, 0x16), (48, 0x20)]:
        p[1][r] = (0, 0, FX_SET_SPEED, spd)
    for r in [0, 32]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x1A)
    note_row(p[0], 0, 9, 'A-3', FX_SET_VOL, 0x14)
    note_row(p[3], 0, 12, 'A-4', FX_SET_VOL, 0x0E)
    mod.write_pattern(p)


# ============================================================
# TRACK 4: "void drum" — sparse ambient percussion, reverb-like decay
# ============================================================

def compose_t4_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x0C)
    # silence texture — just one bell and faint hihat
    note_row(p[3], 0, 12, 'D-4', FX_SET_VOL, 0x1C)  # fm bell
    for r in range(0, 48, 16):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x0A)
    note_row(p[0], 0, 9, 'D-3', FX_SET_VOL, 0x14)
    mod.write_pattern(p)

def compose_t4_verseA(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x08)
    # sparse: bass drone, very occasional percussion
    note_row(p[0], 0, 1, 'D-2', FX_SET_VOL, 0x1E)
    for r in [0, 32]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x1C)
    for r in [16, 48]:
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x14)
    for r in range(0, 64, 12):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x0E)
    # bell accents
    for r in [0, 24, 48]:
        note_row(p[3], r, 12, 'D-4', FX_SET_VOL, 0x18)
    mod.write_pattern(p)

def compose_t4_verseB(mod):
    p = mod.new_pattern()
    # slightly busier but still sparse
    for r in range(0, 64, 16):
        note_row(p[0], r, 1, 'D-2', FX_SET_VOL, 0x20)
    for r in [0, 16, 32, 48]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x1E)
    for r in [8, 24, 40, 56]:
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x16)
    # hihat with vol slide (decay effect)
    for r in range(0, 64, 8):
        note_row(p[2], r, 5, 'C-3', FX_VOL_SLIDE, 0x08)  # fade away
    # pad and bell interplay
    note_row(p[3], 0, 9, 'D-3', FX_SET_VOL, 0x20)
    note_row(p[3], 32, 12, 'A-3', FX_SET_VOL, 0x1A)
    mod.write_pattern(p)

def compose_t4_chorus(mod):
    p = mod.new_pattern()
    # build up — more percussion but still atmospheric
    for r in range(0, 64, 16):
        note_row(p[0], r, 1, 'D-2', FX_SET_VOL, 0x24)
        note_row(p[0], r+8, 1, 'A-2', FX_SET_VOL, 0x1C)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x1E)
    # kick has vol slide decay
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3', FX_VOL_SLIDE, 0x06)
    for r in range(0, 64, 4):
        note_row(p[2], r, 5, 'C-3', FX_VOL_SLIDE, 0x04 if r%8==0 else 0x02)
    # melodic bells
    bells = ['D-4','F-4','A-4','C-4','D-4','A-4','F-4','D-4']
    for i, n in enumerate(bells):
        note_row(p[3], i*8, 12, n, FX_SET_VOL, 0x20)
    mod.write_pattern(p)

def compose_t4_bridge(mod):
    p = mod.new_pattern()
    # stripped back — silence and decay
    for r in [0, 32]:
        note_row(p[0], r, 9, 'D-3', FX_SET_VOL, 0x16)
    for r in [0, 48]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x18)
    for r in range(0, 56, 14):
        note_row(p[2], r, 5, 'C-3', FX_SET_VOL, 0x08)
    for r in [0, 32]:
        note_row(p[3], r, 12, 'A-3', FX_SET_VOL, 0x14)
    mod.write_pattern(p)

def compose_t4_interlude(mod):
    p = mod.new_pattern()
    # noise-based textural section
    for r in range(0, 64, 8):
        note_row(p[1], r, 10, 'C-3', FX_TREMOLO, 0x24)
        note_row(p[1], r+2, 10, 'C-3', FX_SET_VOL, 0x0C)
    for r in range(0, 64, 12):
        note_row(p[2], r, 5, 'C-3', FX_VOL_SLIDE, 0x03)
    note_row(p[0], 0, 9, 'D-3', FX_SET_VOL, 0x14)
    note_row(p[3], 0, 12, 'D-4', FX_SET_VOL, 0x16)
    mod.write_pattern(p)

def compose_t4_climax(mod):
    p = mod.new_pattern()
    # fullest texture — but still with decay character
    for r in range(0, 64, 8):
        ns = ['D-2','F-2','A-2','C-3','D-3','A-2','F-2','D-2']
        note_row(p[0], r, 1, ns[r//8])
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x20)
    for r in range(4, 64, 12):
        note_row(p[1], r, 10, 'C-3', FX_TREMOLO, 0x14)
    for r in range(0, 64, 4):
        note_row(p[2], r, 5, 'C-3', FX_VOL_SLIDE, 0x04)
    bells = ['D-4','F-4','A-4','C-4','D-4','A-4','F-4','D-4']
    for i, n in enumerate(bells):
        note_row(p[3], i*8, 12, n, FX_SET_VOL, 0x24)
    mod.write_pattern(p)

def compose_t4_outro(mod):
    p = mod.new_pattern()
    # final decay — everything fades
    note_row(p[0], 0, 9, 'D-3', FX_SET_VOL, 0x10)
    for r in [0, 48]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x14)
    for r in range(0, 56, 16):
        note_row(p[2], r, 5, 'C-3', FX_VOL_SLIDE, 0x08)
    note_row(p[3], 0, 12, 'D-4', FX_VOL_SLIDE, 0x08)
    mod.write_pattern(p)


# ============================================================
# MAIN
# ============================================================

def main():
    mod = MODWriter(name="alma's rhythm void")

    print("generating samples...")
    mod.add_sample("bass",       gen_bass())
    mod.add_sample("kick",       gen_kick())
    mod.add_sample("snare",      gen_snare())
    mod.add_sample("hi-hat",     gen_hihat())
    mod.add_sample("oh-hat",     gen_ohhat())
    mod.add_sample("lead",       gen_lead())
    mod.add_sample("pad",        gen_pad())
    mod.add_sample("chip lead",  gen_chip(523))
    mod.add_sample("noise burst", gen_noise_burst(int(11025*0.15), decay=0.15))
    mod.add_sample("click",      gen_click())
    mod.add_sample("glitch",     gen_glitch())
    mod.add_sample("fm bell",    gen_fm_bell(587, vol=0.6))
    mod.add_sample("ring",       gen_ring(vol=0.5))

    # Track 1: "polyrhythm garden" — patterns 0-7
    print("composing track 1: polyrhythm garden...")
    compose_t1_intro(mod)      # 0
    compose_t1_layer1(mod)     # 1
    compose_t1_layer2(mod)     # 2
    compose_t1_layer3(mod)     # 3
    compose_t1_full(mod)       # 4
    compose_t1_break(mod)      # 5
    compose_t1_rebuild(mod)    # 6
    compose_t1_outro(mod)      # 7

    # Track 2: "glitch matrix" — patterns 8-15
    print("composing track 2: glitch matrix...")
    compose_t2_intro(mod)      # 8
    compose_t2_verseA(mod)     # 9
    compose_t2_verseB(mod)     # 10
    compose_t2_chorus(mod)     # 11
    compose_t2_bridge(mod)     # 12
    compose_t2_interlude(mod)  # 13
    compose_t2_climax(mod)     # 14
    compose_t2_outro(mod)      # 15

    # Track 3: "pulse decay" — patterns 16-23
    print("composing track 3: pulse decay...")
    compose_t3_intro(mod)      # 16
    compose_t3_accel1(mod)     # 17
    compose_t3_fast(mod)       # 18
    compose_t3_melt(mod)       # 19
    compose_t3_slow(mod)       # 20
    compose_t3_rebuild(mod)    # 21
    compose_t3_climax(mod)     # 22
    compose_t3_outro(mod)      # 23

    # Track 4: "void drum" — patterns 24-31
    print("composing track 4: void drum...")
    compose_t4_intro(mod)      # 24
    compose_t4_verseA(mod)     # 25
    compose_t4_verseB(mod)     # 26
    compose_t4_chorus(mod)     # 27
    compose_t4_bridge(mod)     # 28
    compose_t4_interlude(mod)  # 29
    compose_t4_climax(mod)     # 30
    compose_t4_outro(mod)      # 31

    # Each track: intro×2, A×4, B×3, chorus×4, bridge×2, interlude×2, climax×3, outro×2 = 22
    # 22 plays × 4 tracks = 88 pattern plays
    t1 = [0]*2 + [1]*4 + [2]*3 + [3]*4 + [4]*2 + [5]*2 + [6]*3 + [7]*2
    t2 = [8]*2 + [9]*4 + [10]*3 + [11]*4 + [12]*2 + [13]*2 + [14]*3 + [15]*2
    t3 = [16]*2 + [17]*4 + [18]*3 + [19]*4 + [20]*2 + [21]*2 + [22]*3 + [23]*2
    t4 = [24]*2 + [25]*4 + [26]*3 + [27]*4 + [28]*2 + [29]*2 + [30]*3 + [31]*2

    mod.order = t1 + t2 + t3 + t4

    output_path = "/home/alma/.nanobot/workspace/projects/tracker-playground/album_rhythm_of_the_void.mod"
    print(f"writing {output_path}...")
    mod.write(output_path)

    import os
    size = os.path.getsize(output_path)
    print(f"done! {output_path} ({size} bytes, {size/1024:.1f} KB)")

    total_patterns = len(mod.order)
    # average speed ~6 ticks/row across all patterns
    est_seconds = total_patterns * 64 * 6 / 50.0
    est_minutes = est_seconds / 60.0
    print(f"total: {total_patterns} pattern plays, ~{est_seconds:.0f}s ({est_minutes:.1f} min)")
    print(f"per track: ~{est_seconds/4:.0f}s ({est_minutes/4:.1f} min)")

if __name__ == "__main__":
    main()
