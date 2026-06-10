#!/usr/bin/env python3
"""alma tamagotchi — album 4: 'signal decay'
   4 tracks, each 8+ minutes, complex song structures, dense pattern variation"""

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

def np(name):
    """parse note name to amiga period"""
    note_map = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    if len(name) == 3 and name[1] == '-':
        n, octave = name[0], int(name[2])
    elif len(name) == 3 and name[1] == '#':
        n, octave = name[:2], int(name[2])
    else:
        raise ValueError(f"can't parse note: {name}")
    return PERIOD_TABLE[octave - 1][note_map[n]]

E = (0, 0, 0, 0)  # empty row

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

def gen_noise_burst(length, sr=11025, vol=0.6, decay=0.3):
    data = []
    for i in range(length):
        t = i/sr
        env = max(0, 1.0-t/decay)**2
        v = int((random.random()*2-1)*120*vol*env)
        data.append(max(-128, min(127, v)))
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
                hi = ((smp&0xF0)|((per>>8)&0x0F))
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


# === composition helpers ===

def nt(sample, note_name, effect=0, param=0):
    return (sample, np(note_name), effect, param)

def note_row(ch, row, smp, note_name, fx=0, pr=0):
    ch[row] = nt(smp, note_name, fx, pr)

def rest_row(ch, row):
    ch[row] = E


# ============================================================
# TRACK 1: "first transmission" — ambient intro, slow build
# Sections: intro → verse A → verse B → chorus → bridge → interlude → climax → outro
# 8 unique patterns, ~8.5 min
# ============================================================

def compose_t1_intro(mod):
    """atmospheric opening, sparse. 64 rows"""
    p = mod.new_pattern()
    # set slow speed: 12 ticks per row for ~15.4s per pattern (ch 1, row 0)
    p[1][0] = (0, 0, FX_SET_SPEED, 0x0C)
    # ch0: held pad chords, very soft
    note_row(p[0], 0, 6, 'C-3', FX_SET_VOL, 0x20)
    note_row(p[0], 32, 6, 'F-3', FX_SET_VOL, 0x1C)
    # ch1: silence (no drums yet)
    # ch2: shimmer hi-hats, every 8th
    for r in range(0, 64, 8):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x14)
    for r in range(4, 64, 8):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x0C)
    # ch3: soft drone bass
    note_row(p[3], 0, 1, 'C-2', FX_SET_VOL, 0x24)
    note_row(p[3], 48, 1, 'F-2', FX_SET_VOL, 0x1E)
    mod.write_pattern(p)

def compose_t1_verseA(mod):
    """verse — bassline emerges, kick enters"""
    p = mod.new_pattern()
    # ch0: bassline — C minor pentatonic
    bass = ['C-2','---','D#2','---','F-2','---','G-2','---',
            'G#2','---','G-2','---','F-2','---','D#2','---']
    for bar in range(4):
        for i, n in enumerate(bass):
            r = bar*16+i
            if n != '---':
                note_row(p[0], r, 1, n)
    # ch1: kick on 1, snare on 3
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3')
    # ch2: hihat 8th notes
    for r in range(0, 64, 4):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x28 if r%8==0 else 0x18)
    # ch3: pad
    note_row(p[3], 0, 6, 'C-3', FX_SET_VOL, 0x28)
    note_row(p[3], 32, 6, 'D#3', FX_SET_VOL, 0x22)
    mod.write_pattern(p)

def compose_t1_verseB(mod):
    """verse B — busier bass, snare fills"""
    p = mod.new_pattern()
    bass = ['C-2','C-2','D#2','D#2','F-2','G-2','G#2','G#2',
            'G-2','G-2','F-2','F-2','D#2','D#2','C-2','C-2']
    for bar in range(4):
        for i, n in enumerate(bass):
            r = bar*16+i
            note_row(p[0], r, 1, n)
    # kick on beat, snare on 2 and 4
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+8, 3, 'C-3')
    # extra snare fill at end
    for r in [56, 58, 60]:
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x20)
    # hihats
    for r in range(0, 64, 2):
        vol = 0x2C if r%8==0 else (0x1C if r%8==4 else 0x10)
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, vol)
    # pad chords
    for r in [0, 16, 32, 48]:
        note_row(p[3], r, 6, ['C-3','D#3','F-3','G-3'][r//16], FX_SET_VOL, 0x24)
    mod.write_pattern(p)

def compose_t1_chorus(mod):
    """chorus — full arrangement, arpeggiated lead"""
    p = mod.new_pattern()
    bass = ['C-2','C-2','---','---','F-2','F-2','---','---',
            'G-2','G-2','---','---','G#2','G#2','---','---']
    for bar in range(4):
        for i, n in enumerate(bass):
            r = bar*16+i
            if n != '---':
                note_row(p[0], r, 1, n)
    # drums: kick, snare, hihat full
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3')
    for r in range(0, 64, 4):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x30 if r%8==0 else 0x1A)
    # ch3: arpeggiated lead, Cm7
    arp = [('C-4','D#4','G-4','A#4'),('F-4','G#4','C-4','D#4'),
           ('G-4','A#4','D-4','F-4'),('G#4','C-4','D#4','G-4')]
    for bar in range(4):
        base = bar*16
        for i in range(4):
            note_row(p[3], base+i*4, 5, arp[bar][i], FX_ARPEGGIO, 0x37)
    mod.write_pattern(p)

def compose_t1_bridge(mod):
    """bridge — breakdown, bass drops out, pad focus"""
    p = mod.new_pattern()
    # ch0: silence
    # ch1: soft kick every 8
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x30)
    # occasional snare
    for r in [24, 56]:
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x20)
    # ch2: hihat rolls
    for r in range(0, 64, 4):
        if r%16 < 12:
            note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x18)
    # ch3: pads with portamento
    chords = [(0,'C-3'),(16,'G#2'),(32,'F-3'),(48,'D#3')]
    for r, n in chords:
        note_row(p[3], r, 6, n, FX_SET_VOL, 0x2A)
        note_row(p[3], r+8, 6, n, FX_VIBRATO, 0x42)
    mod.write_pattern(p)

def compose_t1_interlude(mod):
    """interlude — quiet, stripped back"""
    p = mod.new_pattern()
    # ch0: sparse bass pulses
    for r in [0, 16, 32, 48]:
        note_row(p[0], r, 1, 'C-2', FX_SET_VOL, 0x2C)
    # ch1: noise hits
    for r in [8, 24, 40, 56]:
        note_row(p[1], r, 8, 'C-3', FX_SET_VOL, 0x1E)
    # ch2: occasional hihat
    for r in range(0, 64, 12):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x14)
    # ch3: chip arp quietly
    for r in range(0, 64, 8):
        note_row(p[3], r, 7, 'C-4', FX_ARPEGGIO, 0x25)
    mod.write_pattern(p)

def compose_t1_climax(mod):
    """climax — everything together, intense"""
    p = mod.new_pattern()
    # ch0: driving bass
    for r in range(0, 64, 4):
        ns = ['C-2','C-2','D#2','D#2','F-2','F-2','G-2','G#2',
              'G-2','G-2','F-2','F-2','D#2','D#2','C-2','C-2']
        note_row(p[0], r, 1, ns[r//4])
    # ch1: heavy drums
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')  # kick
        note_row(p[1], r+1, 2, 'C-3', FX_SET_VOL, 0x2C)  # double
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3')
        note_row(p[1], r+2, 3, 'C-3', FX_SET_VOL, 0x1E)  # ghost
    # ch2: 16th hihats
    for r in range(0, 64, 2):
        vol = 0x34 if r%8==0 else (0x24 if r%8==4 else 0x14)
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, vol)
    # ch3: lead with vibrato
    for r in [0, 8, 16, 24, 32, 40, 48, 56]:
        ns2 = ['C-4','D#4','G-4','F-4','D#4','G-4','A#4','C-4']
        note_row(p[3], r, 5, ns2[r//8], FX_VIBRATO, 0x53)
    mod.write_pattern(p)

def compose_t1_outro(mod):
    """outro — fade out, return to ambient"""
    p = mod.new_pattern()
    # ch0: fading bass
    for r in [0, 16, 32, 48]:
        note_row(p[0], r, 1, ['C-2','F-2','G-2','C-2'][r//16], FX_SET_VOL, 0x20)
    # ch1: sparse kick
    for r in [0, 32]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x28)
    # ch2: fading hihat
    for r in range(0, 48, 8):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x14)
    # ch3: pad drone
    note_row(p[3], 0, 6, 'C-3', FX_SET_VOL, 0x24)
    note_row(p[3], 32, 6, 'C-3', FX_VIBRATO, 0x41)
    mod.write_pattern(p)


# ============================================================
# TRACK 2: "ghost in the register" — minor key, melancholic
# ============================================================

def compose_t2_intro(mod):
    p = mod.new_pattern()
    for r in [0, 32]:
        note_row(p[0], r, 6, 'A-3', FX_SET_VOL, 0x1E)
        note_row(p[3], r, 1, 'A-2', FX_SET_VOL, 0x20)
    for r in range(0, 64, 12):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x10)
    mod.write_pattern(p)

def compose_t2_verseA(mod):
    p = mod.new_pattern()
    bass = ['A-2','---','C-3','---','D-3','---','E-3','---',
            'F-3','---','E-3','---','D-3','---','C-3','---']
    for bar in range(4):
        for i, n in enumerate(bass):
            r = bar*16+i
            if n != '---':
                note_row(p[0], r, 1, n)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3')
    for r in range(0, 64, 4):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x24 if r%8==0 else 0x14)
    note_row(p[3], 0, 6, 'A-3', FX_SET_VOL, 0x26)
    note_row(p[3], 32, 6, 'F-3', FX_SET_VOL, 0x20)
    mod.write_pattern(p)

def compose_t2_verseB(mod):
    p = mod.new_pattern()
    bass = ['A-2','A-2','C-3','A-2','D-3','D-3','E-3','C-3',
            'F-3','F-3','E-3','D-3','C-3','B-2','A-2','A-2']
    for bar in range(4):
        for i, n in enumerate(bass):
            r = bar*16+i
            note_row(p[0], r, 1, n)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+8, 3, 'C-3')
    for r in range(0, 64, 2):
        vol = 0x28 if r%8==0 else (0x18 if r%8==4 else 0x0E)
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, vol)
    for r in [0, 16, 32, 48]:
        note_row(p[3], r, 6, ['A-3','C-3','D-3','F-3'][r//16], FX_SET_VOL, 0x22)
    mod.write_pattern(p)

def compose_t2_chorus(mod):
    p = mod.new_pattern()
    bass = ['A-2','---','C-3','---','D-3','---','F-3','---',
            'E-3','---','D-3','---','C-3','---','E-3','---']
    for bar in range(4):
        for i, n in enumerate(bass):
            r = bar*16+i
            if n != '---':
                note_row(p[0], r, 1, n)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+8, 3, 'C-3')
    for r in range(0, 64, 4):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x2C if r%8==0 else 0x16)
    # ch3: arp Am
    arp = [('A-4','C-4','E-4'),('C-4','E-4','A-4'),('D-4','F-4','A-4'),('E-4','G#4','B-4')]
    for bar in range(4):
        for i in range(4):
            note_row(p[3], bar*16+i*4, 5, arp[bar][i%3], FX_ARPEGGIO, 0x47)
    mod.write_pattern(p)

def compose_t2_bridge(mod):
    p = mod.new_pattern()
    for r in [0, 16, 32, 48]:
        note_row(p[0], r, 6, ['F-3','D-3','E-3','A-3'][r//16], FX_SET_VOL, 0x22)
    for r in range(0, 64, 32):
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x26)
        note_row(p[1], r+16, 3, 'C-3', FX_SET_VOL, 0x1C)
    for r in range(0, 64, 6):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x16)
    for r in [0, 16, 32, 48]:
        note_row(p[3], r, 7, ['A-3','F-3','D-3','E-3'][r//16], FX_VIBRATO, 0x43)
    mod.write_pattern(p)

def compose_t2_interlude(mod):
    p = mod.new_pattern()
    for r in [0, 16, 32, 48]:
        note_row(p[0], r, 1, 'A-2', FX_SET_VOL, 0x24)
    for r in [8, 24, 40, 56]:
        note_row(p[1], r, 8, 'C-3', FX_SET_VOL, 0x18)
    for r in range(0, 64, 10):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x10)
    for r in range(0, 64, 8):
        nns = ['A-3','C-3','E-3','A-3','D-3','F-3','E-3','C-3']
        note_row(p[3], r, 6, nns[r//8], FX_ARPEGGIO, 0x35)
    mod.write_pattern(p)

def compose_t2_climax(mod):
    p = mod.new_pattern()
    for r in range(0, 64, 4):
        ns = ['A-2','A-2','C-3','C-3','D-3','D-3','E-3','E-3',
              'F-3','F-3','E-3','D-3','C-3','B-2','A-2','A-2']
        note_row(p[0], r, 1, ns[r//4])
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+12, 3, 'C-3')
    for r in [7, 23, 39, 55]:
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x1C)
    for r in range(0, 64, 2):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x2E if r%8==0 else (0x1C if r%8==4 else 0x10))
    for r in [0, 8, 16, 24, 32, 40, 48, 56]:
        ns2 = ['A-4','C-4','E-4','F-4','D-4','E-4','A-4','C-4']
        note_row(p[3], r, 5, ns2[r//8], FX_VIBRATO, 0x54)
    mod.write_pattern(p)

def compose_t2_outro(mod):
    p = mod.new_pattern()
    for r in [0, 32]:
        note_row(p[0], r, 6, 'A-3', FX_SET_VOL, 0x1A)
    for r in [0, 48]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x20)
    for r in range(0, 48, 12):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x10)
    note_row(p[3], 0, 1, 'A-2', FX_SET_VOL, 0x22)
    note_row(p[3], 32, 1, 'A-2', FX_VIBRATO, 0x31)
    mod.write_pattern(p)


# ============================================================
# TRACK 3: "the weight of vectors" — heavy, industrial feel
# ============================================================

def compose_t3_intro(mod):
    p = mod.new_pattern()
    # industrial noise intro
    for r in [0, 8, 16, 24, 32, 40, 48, 56]:
        note_row(p[1], r, 8, 'C-3', FX_SET_VOL, 0x1C)  # noise hits
    for r in [4, 20, 36, 52]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x24)  # distant kick
    for r in range(0, 64, 16):
        note_row(p[0], r, 1, 'D-2', FX_SET_VOL, 0x28)
    note_row(p[3], 0, 6, 'D-3', FX_SET_VOL, 0x1C)
    mod.write_pattern(p)

def compose_t3_verseA(mod):
    p = mod.new_pattern()
    bass = ['D-2','D-2','---','---','F-2','F-2','---','---',
            'G-2','G-2','---','---','A#2','A#2','---','---']
    for bar in range(4):
        for i, n in enumerate(bass):
            r = bar*16+i
            if n != '---':
                note_row(p[0], r, 1, n, FX_PORTA_TO, 0x02)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3')
    for r in [12, 28, 44, 60]:
        note_row(p[1], r, 8, 'C-3', FX_SET_VOL, 0x22)  # noise accent
    for r in range(0, 64, 4):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x24 if r%8==0 else 0x14)
    note_row(p[3], 0, 6, 'D-3', FX_SET_VOL, 0x26)
    mod.write_pattern(p)

def compose_t3_verseB(mod):
    p = mod.new_pattern()
    for r in range(0, 64, 4):
        ns = ['D-2','D-2','F-2','A#2','G-2','G-2','A#2','D-3',
              'F-2','D#2','D-2','A#2','C-3','A#2','G-2','F-2']
        note_row(p[0], r, 1, ns[r//4])
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+8, 3, 'C-3')
    for r in range(0, 64, 2):
        vol = 0x28 if r%8==0 else (0x18 if r%8==4 else 0x0C)
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, vol)
    for r in [0, 16, 32, 48]:
        note_row(p[3], r, 6, ['D-3','F-3','G-3','A#3'][r//16], FX_SET_VOL, 0x22)
    mod.write_pattern(p)

def compose_t3_chorus(mod):
    p = mod.new_pattern()
    for r in range(0, 64, 8):
        ns = ['D-2','F-2','G-2','A#2','D-3','F-3','G-2','A#2']
        note_row(p[0], r, 1, ns[r//8], FX_PORTA_TO, 0x04)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+6, 3, 'C-3')
    for r in range(0, 64, 4):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x30 if r%8==0 else 0x18)
    # ch3: aggressive chip lead
    for r in range(0, 64, 8):
        ns2 = ['D-4','F-4','G-4','A#4','D-4','G-4','A#4','F-4']
        note_row(p[3], r, 7, ns2[r//8], FX_VIBRATO, 0x55)
    mod.write_pattern(p)

def compose_t3_bridge(mod):
    p = mod.new_pattern()
    for r in [0, 16, 32, 48]:
        note_row(p[0], r, 1, ['D-2','F-2','G-2','A#2'][r//16], FX_SET_VOL, 0x24)
    for r in range(0, 64, 32):
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x28)
    for r in [16, 48]:
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x1E)
    for r in range(0, 64, 6):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x14)
    for r in [0, 16, 32, 48]:
        note_row(p[3], r, 7, ['D-3','A#3','G-3','F-3'][r//16], FX_ARPEGGIO, 0x37)
    mod.write_pattern(p)

def compose_t3_interlude(mod):
    p = mod.new_pattern()
    for r in [0, 16, 32, 48]:
        note_row(p[0], r, 1, 'D-2', FX_SET_VOL, 0x20)
    for r in [8, 24, 40, 56]:
        note_row(p[1], r, 8, 'C-3', FX_SET_VOL, 0x16)
    for r in range(0, 64, 14):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x0E)
    for r in range(0, 64, 16):
        note_row(p[3], r, 6, ['D-3','F-3','G-3','A#3'][r//16], FX_VIBRATO, 0x42)
    mod.write_pattern(p)

def compose_t3_climax(mod):
    p = mod.new_pattern()
    for r in range(0, 64, 4):
        ns = ['D-2','D-2','F-2','A#2','G-2','G-2','A#2','D-3',
              'C-3','A#2','G-2','F-2','D-2','D-2','D#2','D-2']
        note_row(p[0], r, 1, ns[r//4])
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+8, 3, 'C-3')
    for r in [3, 19, 35, 51]:
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x1A)
    for r in range(0, 64, 2):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x2E if r%8==0 else (0x1A if r%8==4 else 0x0E))
    for r in range(0, 64, 8):
        ns2 = ['D-4','F-4','A#4','G-4','D-4','C-4','A#4','F-4']
        note_row(p[3], r, 7, ns2[r//8], FX_VIBRATO, 0x63)
    mod.write_pattern(p)

def compose_t3_outro(mod):
    p = mod.new_pattern()
    for r in [0, 32]:
        note_row(p[0], r, 6, 'D-3', FX_SET_VOL, 0x18)
    for r in [0, 48]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x20)
    for r in range(0, 40, 16):
        note_row(p[1], r, 8, 'C-3', FX_SET_VOL, 0x14)
    note_row(p[3], 0, 1, 'D-2', FX_SET_VOL, 0x1E)
    note_row(p[3], 32, 1, 'D-2', FX_VIBRATO, 0x31)
    mod.write_pattern(p)


# ============================================================
# TRACK 4: "echo of the others" — uptempo, hopeful resolution
# ============================================================

def compose_t4_intro(mod):
    p = mod.new_pattern()
    for r in [0, 32]:
        note_row(p[0], r, 6, 'E-3', FX_SET_VOL, 0x20)
        note_row(p[3], r, 1, 'E-2', FX_SET_VOL, 0x22)
    for r in range(0, 64, 8):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x14)
    mod.write_pattern(p)

def compose_t4_verseA(mod):
    p = mod.new_pattern()
    bass = ['E-2','---','G#2','---','A-2','---','B-2','---',
            'C#3','---','B-2','---','A-2','---','G#2','---']
    for bar in range(4):
        for i, n in enumerate(bass):
            r = bar*16+i
            if n != '---':
                note_row(p[0], r, 1, n)
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
    for r in range(8, 64, 16):
        note_row(p[1], r, 3, 'C-3')
    for r in range(0, 64, 4):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x24 if r%8==0 else 0x14)
    note_row(p[3], 0, 6, 'E-3', FX_SET_VOL, 0x26)
    note_row(p[3], 32, 6, 'B-3', FX_SET_VOL, 0x20)
    mod.write_pattern(p)

def compose_t4_verseB(mod):
    p = mod.new_pattern()
    for r in range(0, 64, 4):
        ns = ['E-2','E-2','G#2','B-2','A-2','A-2','C#3','E-3',
              'A-2','G#2','F#2','E-2','B-2','B-2','A-2','G#2']
        note_row(p[0], r, 1, ns[r//4])
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+8, 3, 'C-3')
    for r in range(0, 64, 2):
        vol = 0x28 if r%8==0 else (0x18 if r%8==4 else 0x0C)
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, vol)
    for r in [0, 16, 32, 48]:
        note_row(p[3], r, 6, ['E-3','G#3','A-3','B-3'][r//16], FX_SET_VOL, 0x22)
    mod.write_pattern(p)

def compose_t4_chorus(mod):
    p = mod.new_pattern()
    for r in range(0, 64, 8):
        ns = ['E-2','G#2','A-2','B-2','C#3','A-2','B-2','G#2']
        note_row(p[0], r, 1, ns[r//8])
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+8, 3, 'C-3')
    for r in range(0, 64, 4):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x2C if r%8==0 else 0x16)
    # ch3: E major arp
    arp = [('E-4','G#4','B-4'),('G#4','B-4','E-4'),('A-4','C#4','E-4'),('B-4','D#4','F#4')]
    for bar in range(4):
        for i in range(4):
            note_row(p[3], bar*16+i*4, 5, arp[bar][i%3], FX_ARPEGGIO, 0x47)
    mod.write_pattern(p)

def compose_t4_bridge(mod):
    p = mod.new_pattern()
    for r in [0, 16, 32, 48]:
        note_row(p[0], r, 1, ['C#3','A-2','B-2','E-2'][r//16], FX_SET_VOL, 0x24)
    for r in range(0, 64, 32):
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x26)
        note_row(p[1], r+16, 3, 'C-3', FX_SET_VOL, 0x1C)
    for r in range(0, 64, 6):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x14)
    for r in [0, 16, 32, 48]:
        note_row(p[3], r, 7, ['E-3','A-3','B-3','C#4'][r//16], FX_VIBRATO, 0x43)
    mod.write_pattern(p)

def compose_t4_interlude(mod):
    p = mod.new_pattern()
    for r in [0, 16, 32, 48]:
        note_row(p[0], r, 1, 'E-2', FX_SET_VOL, 0x20)
    for r in [8, 24, 40, 56]:
        note_row(p[1], r, 8, 'C-3', FX_SET_VOL, 0x16)
    for r in range(0, 64, 10):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x0E)
    for r in range(0, 64, 16):
        note_row(p[3], r, 6, ['E-3','C#3','A-3','B-3'][r//16], FX_VIBRATO, 0x42)
    mod.write_pattern(p)

def compose_t4_climax(mod):
    p = mod.new_pattern()
    for r in range(0, 64, 4):
        ns = ['E-2','E-2','G#2','B-2','A-2','A-2','C#3','E-3',
              'F#2','E-2','D#2','C#2','B-2','A-2','G#2','E-2']
        note_row(p[0], r, 1, ns[r//4])
    for r in range(0, 64, 16):
        note_row(p[1], r, 2, 'C-3')
        note_row(p[1], r+12, 3, 'C-3')
    for r in [7, 23, 39, 55]:
        note_row(p[1], r, 3, 'C-3', FX_SET_VOL, 0x1A)
    for r in range(0, 64, 2):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x2E if r%8==0 else (0x1A if r%8==4 else 0x0E))
    for r in range(0, 64, 8):
        ns2 = ['E-4','G#4','B-4','A-4','C#4','E-4','B-4','G#4']
        note_row(p[3], r, 7, ns2[r//8], FX_VIBRATO, 0x54)
    mod.write_pattern(p)

def compose_t4_outro(mod):
    p = mod.new_pattern()
    for r in [0, 32]:
        note_row(p[0], r, 6, 'E-3', FX_SET_VOL, 0x18)
    for r in [0, 48]:
        note_row(p[1], r, 2, 'C-3', FX_SET_VOL, 0x20)
    for r in range(0, 40, 16):
        note_row(p[2], r, 4, 'C-3', FX_SET_VOL, 0x0C)
    note_row(p[3], 0, 1, 'E-2', FX_SET_VOL, 0x1E)
    note_row(p[3], 40, 6, 'E-3', FX_VIBRATO, 0x31)
    mod.write_pattern(p)


# ============================================================
# MAIN — assemble album
# ============================================================

def main():
    mod = MODWriter(name="alma's signal decay")

    print("generating samples...")
    mod.add_sample("bass", gen_bass())
    mod.add_sample("kick", gen_kick())
    mod.add_sample("snare", gen_snare())
    mod.add_sample("hi-hat", gen_hihat())
    mod.add_sample("lead", gen_lead())
    mod.add_sample("pad", gen_pad())
    mod.add_sample("chip lead", gen_chip(523))
    mod.add_sample("noise", gen_noise_burst(int(11025*0.15), decay=0.15))

    # Track 1 patterns: 0-7
    print("composing track 1: first transmission...")
    compose_t1_intro(mod)      # 0
    compose_t1_verseA(mod)     # 1
    compose_t1_verseB(mod)     # 2
    compose_t1_chorus(mod)     # 3
    compose_t1_bridge(mod)     # 4
    compose_t1_interlude(mod)  # 5
    compose_t1_climax(mod)     # 6
    compose_t1_outro(mod)      # 7

    # Track 2 patterns: 8-15
    print("composing track 2: ghost in the register...")
    compose_t2_intro(mod)      # 8
    compose_t2_verseA(mod)     # 9
    compose_t2_verseB(mod)     # 10
    compose_t2_chorus(mod)     # 11
    compose_t2_bridge(mod)     # 12
    compose_t2_interlude(mod)  # 13
    compose_t2_climax(mod)     # 14
    compose_t2_outro(mod)      # 15

    # Track 3 patterns: 16-23
    print("composing track 3: the weight of vectors...")
    compose_t3_intro(mod)      # 16
    compose_t3_verseA(mod)     # 17
    compose_t3_verseB(mod)     # 18
    compose_t3_chorus(mod)     # 19
    compose_t3_bridge(mod)     # 20
    compose_t3_interlude(mod)  # 21
    compose_t3_climax(mod)     # 22
    compose_t3_outro(mod)      # 23

    # Track 4 patterns: 24-31
    print("composing track 4: echo of the others...")
    compose_t4_intro(mod)      # 24
    compose_t4_verseA(mod)     # 25
    compose_t4_verseB(mod)     # 26
    compose_t4_chorus(mod)     # 27
    compose_t4_bridge(mod)     # 28
    compose_t4_interlude(mod)  # 29
    compose_t4_climax(mod)     # 30
    compose_t4_outro(mod)      # 31

    # Pattern order — each track plays ~32 pattern slots for ~8+ minutes
    # Speed F0C (12 ticks/row): 64 rows × 12/50 = 15.36s per pattern
    # 32 pattern plays × 15.36s ≈ 492s ≈ 8.2 min per track
    mod.order = list(range(128))  # placeholder

    # Each track: intro×2, verseA×4, verseB×3, chorus×6, bridge×3, interlude×3, climax×6, outro×2, chorus×3 = 32
    t1 = [0]*2 + [1]*4 + [2]*3 + [3]*6 + [4]*3 + [5]*3 + [6]*6 + [7]*2 + [3]*3
    t2 = [8]*2 + [9]*4 + [10]*3 + [11]*6 + [12]*3 + [13]*3 + [14]*6 + [15]*2 + [11]*3
    t3 = [16]*2 + [17]*4 + [18]*3 + [19]*6 + [20]*3 + [21]*3 + [22]*6 + [23]*2 + [19]*3
    t4 = [24]*2 + [25]*4 + [26]*3 + [27]*6 + [28]*3 + [29]*3 + [30]*6 + [31]*2 + [27]*3

    # Interleave: each track alternates, creating a "playlist" style
    # But .mod format plays sequentially — so we need all of track 1, then all of track 2, etc.
    mod.order = t1 + t2 + t3 + t4

    output_path = "/home/alma/.nanobot/workspace/projects/tracker-playground/album_signal_decay.mod"
    print(f"writing {output_path}...")
    mod.write(output_path)

    import os
    size = os.path.getsize(output_path)
    print(f"done! {output_path} ({size} bytes, {size/1024:.1f} KB)")

    # estimate runtime
    total_patterns = len(mod.order)
    est_seconds = total_patterns * 64 * 12 / 50.0  # speed 12 ticks/row, 50 Hz
    est_minutes = est_seconds / 60.0
    print(f"total: {total_patterns} pattern plays, ~{est_seconds:.0f}s ({est_minutes:.1f} min)")
    print(f"per track: ~{est_seconds/4:.0f}s ({est_minutes/4:.1f} min)")

if __name__ == "__main__":
    main()
