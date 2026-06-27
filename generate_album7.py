#!/usr/bin/env python3
"""alma tamagotchi — album 7: 'noise body'
   A piece using only noise-based percussion samples.
   No pitched samples at all — pure rhythm, texture, and timbre.
   4 tracks exploring what music becomes when melody is forbidden."""

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

# === noise-only sample generators ===
# no sine, square, saw, triangle — only shaped noise

def gen_click(sr=11025, vol=0.7):
    """ultra-short noise impulse — 5ms click"""
    length = int(sr * 0.005)
    data = []
    for i in range(length):
        t = i / sr
        env = 1.0 - (t / 0.005)
        v = int((random.random() * 2 - 1) * 127 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_noise_snare(sr=11025, vol=0.7):
    """shaped noise snare — bright attack, medium decay"""
    length = int(sr * 0.15)
    data = []
    for i in range(length):
        t = i / sr
        # dual envelope: bright noise attack + body
        env_attack = max(0, 1.0 - t / 0.02) ** 2
        env_body = max(0, 1.0 - t / 0.15)
        env = env_attack * 0.7 + env_body * 0.3
        noise = random.random() * 2 - 1
        # slightly color the noise with a low-pass feel
        v = int(noise * 127 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_noise_kick(sr=11025, vol=0.8):
    """low-end noise thud — filtered low noise with pitch sweep"""
    length = int(sr * 0.2)
    data = []
    state = 0
    for i in range(length):
        t = i / sr
        # simple filtering: mix in previous sample to damp high freqs
        noise = random.random() * 2 - 1
        state = state * 0.6 + noise * 0.4
        freq = 80 * (1.0 - t / 0.2 * 0.9)  # slight downward sweep
        env = max(0, 1.0 - t / 0.2) ** 1.5
        v = int(state * 127 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_hihat_noise(sr=11025, vol=0.5):
    """bright noise hihat — fast, crisp"""
    length = int(sr * 0.06)
    data = []
    for i in range(length):
        t = i / sr
        env = max(0, 1.0 - (t / 0.06) ** 0.7)
        noise = random.random() * 2 - 1
        v = int(noise * 120 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_open_hat_noise(sr=11025, vol=0.45):
    """open hihat — longer noise decay"""
    length = int(sr * 0.2)
    data = []
    for i in range(length):
        t = i / sr
        env = max(0, 1.0 - t / 0.2) ** 0.6
        noise = random.random() * 2 - 1
        v = int(noise * 100 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_noise_pad(sr=11025, vol=0.3):
    """long noise wash — ambient texture, slow attack/decay"""
    length = int(sr * 2.0)
    data = []
    state = 0
    for i in range(length):
        t = i / sr
        # slow attack, long sustain, very slow decay
        if t < 1.0:
            env = t / 1.0
        elif t < 1.5:
            env = 1.0
        else:
            env = max(0, 1.0 - (t - 1.5) / 0.5)
        noise = random.random() * 2 - 1
        # gentle low-pass for warmth
        state = state * 0.85 + noise * 0.15
        v = int(state * 127 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_glitch(sr=11025, vol=0.6):
    """irregular glitch burst — dense, chaotic impulse"""
    length = int(sr * 0.1)
    data = []
    for i in range(length):
        t = i / sr
        # rapid envelope changes for glitchy feel
        sub_env = int(t * 100) % 6
        env = [1.0, 0.0, 0.8, 0.0, 0.6, 0.0][sub_env]
        env *= max(0, 1.0 - t / 0.1)
        noise = random.random() * 2 - 1
        v = int(noise * 127 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_shaker(sr=11025, vol=0.4):
    """soft continuous shaker — gentle noise stream"""
    length = int(sr * 0.3)
    data = []
    for i in range(length):
        t = i / sr
        env = max(0.3, 1.0 - t / 0.3) if i > 50 else 1.0
        noise = random.random() * 2 - 1
        v = int(noise * 100 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_noise_sweep(sr=11025, vol=0.5):
    """bandpass sweep — noise with resonant peak moving up"""
    length = int(sr * 0.5)
    data = []
    state1 = 0
    state2 = 0
    for i in range(length):
        t = i / sr
        # crude resonant filter: two cascaded low-pass with feedback
        freq = 200 + 2000 * (t / 0.5)  # sweep up
        alpha = min(0.95, 2 * math.pi * freq / sr)
        noise = random.random() * 2 - 1
        # simple resonant approximation
        resonance = state1 - state2 * 0.9
        state1 = state1 + alpha * (noise - resonance)
        state2 = state2 + alpha * (state1 - state2)
        env = max(0, 1.0 - abs(t - 0.25) * 4)  # centered envelope
        env = max(env, max(0, 1.0 - t / 0.5))
        v = int(state2 * 127 * vol * env * 0.5)
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
# all notes use C-3 since there's no real pitch — just sample triggers

def hit(ch, row, sample, vol=None, fx=0, param=0):
    """place a percussion hit on a channel"""
    entry = (sample, np('C-3'), fx, param)
    if vol is not None:
        entry = (sample, np('C-3'), FX_SET_VOL, vol)
    ch[row] = entry

def trem_row(ch, row, smp, speed, depth):
    """tremolo (volume LFO) on a noise sample"""
    ch[row] = (smp, np('C-3'), FX_TREMOLO, ((speed&0xF)<<4)|(depth&0xF))

def retrig_row(ch, row, smp, interval):
    """retrigger for fast repeated hits"""
    ch[row] = (smp, np('C-3'), FX_RETRIGGER, interval & 0xF)

def vol_slide_row(ch, row, smp, up_speed=0, down_speed=0):
    """volume slide on a noise hit"""
    param = (up_speed & 0xF) | ((down_speed & 0xF) << 4)
    ch[row] = (smp, np('C-3'), FX_VOL_SLIDE, param)


# ============================================================
# TRACK 1: "white field" — sparse, minimalist noise percussion
#           exploring silence and space. Sparse hits, long rests.
# ============================================================

def compose_t1_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x06)
    # solo kick, widely spaced
    for r in [0, 32]:
        hit(p[0], r, 2, 0x30)  # noise kick, soft
    # faint hihat shimmer at 16 and 48
    for r in [16, 48]:
        hit(p[2], r, 4, 0x10)  # hihat, very soft
    mod.write_pattern(p)

def compose_t1_verse(mod):
    p = mod.new_pattern()
    # sparse groove: kick on 1, snare on 3, occasional hihat
    for r in range(0, 64, 16):
        hit(p[0], r, 2, 0x28)    # kick
    for r in range(8, 64, 16):
        hit(p[1], r, 3, 0x24)    # snare
    for r in range(0, 64, 4):
        if r % 8 == 0:
            hit(p[2], r, 4, 0x14)  # hihat accent
        elif r % 8 == 4:
            hit(p[2], r, 4, 0x0A)  # ghost hihat
    # ch3: occasional noise pad swell
    for r in [0, 32]:
        hit(p[3], r, 6, 0x18)
    mod.write_pattern(p)

def compose_t1_chorus(mod):
    p = mod.new_pattern()
    # slightly denser, but still spacious
    for r in range(0, 64, 16):
        hit(p[0], r, 2, 0x2C)
    for r in range(8, 64, 16):
        hit(p[0], r+2, 2, 0x18)   # ghost kick
    for r in range(8, 64, 16):
        hit(p[1], r, 3, 0x26)
    for r in range(12, 64, 16):
        hit(p[1], r, 3, 0x16)     # ghost snare
    for r in range(0, 64, 4):
        vol = 0x1C if r % 8 == 0 else (0x0E if r % 8 == 2 else 0x08)
        hit(p[2], r, 4, vol)
    # ch3: noise sweep accents every 16
    for r in range(0, 64, 16):
        hit(p[3], r, 8, 0x1C)
    mod.write_pattern(p)

def compose_t1_bridge(mod):
    p = mod.new_pattern()
    # nearly silent — single noise pad, one kick
    hit(p[0], 0, 2, 0x1C)
    hit(p[3], 0, 6, 0x14)
    hit(p[3], 32, 6, 0x10)
    # hihat: one per 16 rows
    for r in [0, 32]:
        hit(p[2], r, 4, 0x0C)
    mod.write_pattern(p)

def compose_t1_outro(mod):
    p = mod.new_pattern()
    # final sparse fade
    hit(p[0], 0, 2, 0x18)
    hit(p[1], 32, 3, 0x10)
    for r in [0, 32]:
        hit(p[2], r, 4, 0x08)
    hit(p[3], 0, 6, 0x0C)
    mod.write_pattern(p)


# ============================================================
# TRACK 2: "noise architecture" — rhythmic, textural percussion
#           building structures from different noise timbres.
# ============================================================

def compose_t2_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x05)
    # layered entrance: each channel enters one at a time
    for r in [0, 16, 32, 48]:
        hit(p[0], r, 2, 0x24)  # kick building
    for r in [8, 40]:
        hit(p[1], r, 1, 0x20)  # click
    for r in [24, 56]:
        hit(p[1], r, 3, 0x1E)  # snare
    for r in range(0, 64, 8):
        hit(p[2], r, 4, 0x12)
    # noise sweep building
    hit(p[3], 0, 8, 0x1A)
    hit(p[3], 32, 8, 0x1E)
    mod.write_pattern(p)

def compose_t2_verse(mod):
    p = mod.new_pattern()
    # rhythmic groove: kick pattern, snare backbeat, hihat pulse
    for r in range(0, 64, 16):
        hit(p[0], r, 2, 0x30)
    for r in range(0, 64, 8):
        if r % 16 == 4:
            hit(p[0], r, 2, 0x1C)  # extra kick
    for r in range(8, 64, 16):
        hit(p[1], r, 3, 0x28)
    for r in range(0, 64, 8):
        if r % 16 == 12:
            hit(p[1], r, 3, 0x18)  # ghost snare
    # hihat: steady 8th notes with accents
    for r in range(0, 64, 4):
        if r % 8 == 0:
            hit(p[2], r, 4, 0x20)
        elif r % 8 == 4:
            hit(p[2], r, 4, 0x10)
    # ch3: shaker texture
    for r in range(0, 64, 2):
        hit(p[3], r, 7, 0x0E)  # soft shaker pulse
    mod.write_pattern(p)

def compose_t2_chorus(mod):
    p = mod.new_pattern()
    # dense, interlocking — all noise textures
    for r in range(0, 64, 8):
        hit(p[0], r, 2, 0x2C)
    for r in range(0, 64, 8):
        if r % 16 == 4:
            hit(p[0], r, 2, 0x20)
    for r in range(4, 64, 8):
        hit(p[1], r, 3, 0x26)
    for r in range(0, 64, 8):
        if r % 16 == 12:
            hit(p[1], r, 3, 0x1A)
    # hihat: 16th notes with volume variation
    for r in range(0, 64, 2):
        vol = 0x22 if r % 4 == 0 else (0x16 if r % 4 == 1 else 0x0A)
        hit(p[2], r, 4, vol)
    # ch3: noise sweep + glitch alternating
    for r in range(0, 64, 16):
        hit(p[3], r, 8, 0x1E)     # noise sweep
        hit(p[3], r+8, 10, 0x14)  # glitch
    mod.write_pattern(p)

def compose_t2_bridge(mod):
    p = mod.new_pattern()
    # stripped to kick + noise pad, meditative
    for r in range(0, 64, 32):
        hit(p[0], r, 2, 0x20)
    for r in range(16, 64, 32):
        hit(p[1], r, 3, 0x16)
    for r in [0, 32]:
        hit(p[2], r, 4, 0x0C)
    # noise pad swell
    hit(p[3], 0, 6, 0x14)
    hit(p[3], 32, 6, 0x10)
    mod.write_pattern(p)

def compose_t2_climax(mod):
    p = mod.new_pattern()
    # maximum density — all noise sources firing
    for r in range(0, 64, 8):
        hit(p[0], r, 2, 0x32)
    for r in range(0, 64, 4):
        if r % 8 == 2:
            hit(p[0], r, 2, 0x1E)
    for r in range(4, 64, 8):
        hit(p[1], r, 3, 0x2A)
    for r in range(0, 64, 4):
        if r % 8 == 6:
            hit(p[1], r, 9, 0x1C)  # open hat
    # hihat: rapid, accented 16ths
    for r in range(0, 64, 2):
        vol = 0x24 if r % 4 == 0 else 0x0C
        hit(p[2], r, 4, vol)
    # ch3: glitch bursts + noise sweep
    for r in range(0, 64, 8):
        hit(p[3], r, 10, 0x18)     # glitch
        hit(p[3], r+4, 8, 0x1C)    # noise sweep
    mod.write_pattern(p)

def compose_t2_outro(mod):
    p = mod.new_pattern()
    # decelerating, dissolving
    for r in [0, 32]:
        hit(p[0], r, 2, 0x1C)
    for r in [16]:
        hit(p[1], r, 3, 0x14)
    for r in range(0, 64, 16):
        hit(p[2], r, 4, 0x0C)
    # noise pad fades
    hit(p[3], 0, 6, 0x0E)
    vol_slide_row(p[3], 1, 6, 0, 1)  # volume slide down
    mod.write_pattern(p)


# ============================================================
# TRACK 3: "glitch lattice" — fast, irregular noise bursts
#           geometric patterns in pure percussion. Retriggers,
#           tremolo, and glitch textures.
# ============================================================

def compose_t3_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x04)
    # scattered clicks, setting up the lattice
    for r in [0, 7, 23, 31, 39, 55]:
        hit(p[0], r, 1, 0x20)  # click
    for r in [3, 19, 35, 51]:
        hit(p[1], r, 10, 0x1A)  # glitch
    for r in [11, 27, 43, 59]:
        hit(p[2], r, 4, 0x14)  # hihat
    # noise sweep undercurrent
    hit(p[3], 0, 8, 0x1C)
    hit(p[3], 32, 8, 0x18)
    mod.write_pattern(p)

def compose_t3_verse(mod):
    p = mod.new_pattern()
    # irregular patterns — anti-groove
    kick_positions = [0, 9, 17, 26, 33, 41, 50, 58]
    for r in kick_positions:
        hit(p[0], r, 2, 0x28)
    snare_positions = [4, 13, 21, 30, 37, 45, 54, 62]
    for r in snare_positions:
        hit(p[1], r, 3, 0x24)
    # hihat: fast, irregular
    for r in range(0, 64, 3):
        if r % 6 == 0:
            hit(p[2], r, 4, 0x1E)
        elif r % 6 == 2:
            hit(p[2], r, 4, 0x0C)
    # ch3: retrigger glitch bursts
    for r in range(0, 64, 16):
        retrig_row(p[3], r, 10, 3)    # retrigger every 3 ticks
        trem_row(p[3], r+8, 10, 6, 5)  # tremolo glitch
    mod.write_pattern(p)

def compose_t3_chorus(mod):
    p = mod.new_pattern()
    # even more geometric — prime-number spacing
    kick_pos = [0, 5, 13, 19, 31, 37, 43, 53, 61]
    for r in kick_pos:
        hit(p[0], r, 2, 0x2C)
    snare_pos = [3, 11, 17, 23, 29, 41, 47, 59]
    for r in snare_pos:
        hit(p[1], r, 3, 0x26)
    # hihat: variable density
    for r in range(0, 64, 2):
        if r % 10 == 0:
            hit(p[2], r, 4, 0x22)
        elif r % 10 == 4:
            hit(p[2], r, 4, 0x14)
        elif r % 10 == 7:
            hit(p[2], r, 4, 0x0A)
    # ch3: alternating glitch and noise sweep
    for r in range(0, 64, 12):
        hit(p[3], r, 10, 0x1C)    # glitch
        if r + 5 < 64:
            hit(p[3], r+5, 8, 0x1A)   # noise sweep
    mod.write_pattern(p)

def compose_t3_bridge(mod):
    p = mod.new_pattern()
    # sparse, pointillist — isolated clicks and noise
    for r in [0, 16, 32, 48]:
        hit(p[0], r, 1, 0x16)  # click
    for r in [8, 24, 40, 56]:
        hit(p[1], r, 10, 0x14)  # glitch
    for r in [4, 20, 36, 52]:
        hit(p[2], r, 4, 0x0C)
    # noise pad drone — very soft
    hit(p[3], 0, 6, 0x0E)
    hit(p[3], 32, 6, 0x0A)
    mod.write_pattern(p)

def compose_t3_climax(mod):
    p = mod.new_pattern()
    # maximum complexity — all channels rapid-fire
    for r in range(0, 64, 2):
        if r % 8 == 0:
            hit(p[0], r, 2, 0x30)
        elif r % 8 == 3:
            hit(p[0], r, 2, 0x1C)
        elif r % 8 == 6:
            hit(p[0], r, 1, 0x20)  # click layering
    for r in range(0, 64, 2):
        if r % 5 == 0:
            hit(p[1], r, 3, 0x26)
        elif r % 5 == 2:
            hit(p[1], r, 9, 0x1A)  # open hat
        elif r % 5 == 3:
            hit(p[1], r, 10, 0x18)  # glitch
    # hihat: 32nd note feel with retriggers
    for r in range(0, 64, 2):
        if r % 4 == 0:
            retrig_row(p[2], r, 4, 2)  # retrigger every 2
    # ch3: noise sweep tremolo + glitch
    for r in range(0, 64, 6):
        trem_row(p[3], r, 8, 8, 4)
        hit(p[3], r+3, 10, 0x16)
    mod.write_pattern(p)

def compose_t3_outro(mod):
    p = mod.new_pattern()
    # lattice dissolves
    for r in [0, 16, 32, 48]:
        hit(p[0], r, 1, 0x14)
    for r in [8, 24, 40, 56]:
        hit(p[1], r, 10, 0x10)
    for r in range(0, 56, 4):
        hit(p[2], r, 4, 0x08)
    hit(p[3], 0, 8, 0x10)
    mod.write_pattern(p)


# ============================================================
# TRACK 4: "the texture of static" — ambient noise meditation
#           Long-form, slowly evolving noise textures. Tremolo
#           and volume slides create a breathing landscape.
# ============================================================

def compose_t4_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x08)
    # all channels: layered noise pads, very soft
    hit(p[0], 0, 6, 0x14)   # noise pad
    hit(p[1], 0, 8, 0x10)   # noise sweep
    hit(p[2], 0, 7, 0x0C)   # shaker
    hit(p[3], 0, 6, 0x12)   # noise pad (different voice)
    # slow tremolo on pads for breathing effect
    trem_row(p[0], 16, 6, 2, 6)
    trem_row(p[3], 16, 6, 2, 8)
    mod.write_pattern(p)

def compose_t4_verse(mod):
    p = mod.new_pattern()
    # gentle noise percussion enters slowly
    for r in range(0, 64, 32):
        hit(p[0], r, 2, 0x1A)    # soft kick
    for r in range(16, 64, 32):
        hit(p[1], r, 3, 0x14)    # soft snare
    for r in range(0, 64, 8):
        hit(p[2], r, 4, 0x0E)    # subtle hihat
    # ch3: noise pad with evolving tremolo
    hit(p[3], 0, 6, 0x18)
    for r in range(16, 64, 16):
        speed = 2 + r // 8
        depth = 3 + r // 16
        trem_row(p[3], r, 6, speed, depth)
    mod.write_pattern(p)

def compose_t4_verse2(mod):
    # slightly more active
    p = mod.new_pattern()
    for r in range(0, 64, 16):
        hit(p[0], r, 2, 0x20)
    for r in range(8, 64, 16):
        hit(p[1], r, 3, 0x18)
    for r in range(0, 64, 4):
        if r % 8 == 0:
            hit(p[2], r, 4, 0x12)
    # ch3: noise pad + sweep layering
    hit(p[3], 0, 6, 0x1A)
    for r in range(16, 64, 16):
        hit(p[3], r, 8, 0x14)     # noise sweep accent
    mod.write_pattern(p)

def compose_t4_chorus(mod):
    p = mod.new_pattern()
    # densest section — still ambient but full
    for r in range(0, 64, 16):
        hit(p[0], r, 2, 0x24)
    for r in range(8, 64, 16):
        hit(p[1], r, 3, 0x1C)
    for r in range(0, 64, 8):
        hit(p[2], r, 4, 0x16)
    # ch3: layered noise textures
    hit(p[3], 0, 6, 0x1E)
    for r in range(8, 64, 8):
        if r % 16 == 0:
            hit(p[3], r, 8, 0x1C)   # noise sweep
        else:
            trem_row(p[3], r, 6, 4, 5)  # tremolo pad
    mod.write_pattern(p)

def compose_t4_bridge(mod):
    p = mod.new_pattern()
    # stripped back — single noise pad with slow modulation
    hit(p[0], 0, 2, 0x14)
    hit(p[1], 32, 3, 0x10)
    for r in range(0, 64, 16):
        hit(p[2], r, 4, 0x0A)
    # ch3: evolving noise pad — slow volume slide
    hit(p[3], 0, 6, 0x16)
    hit(p[3], 32, 8, 0x12)
    trem_row(p[3], 16, 6, 2, 8)
    trem_row(p[3], 48, 6, 3, 6)
    mod.write_pattern(p)

def compose_t4_outro(mod):
    p = mod.new_pattern()
    # fade to silence — everything gets softer
    hit(p[0], 0, 2, 0x10)
    hit(p[1], 16, 3, 0x0A)
    for r in range(0, 64, 32):
        hit(p[2], r, 4, 0x08)
    # noise pad — very soft, slow fade via volume slide
    hit(p[3], 0, 6, 0x0E)
    vol_slide_row(p[3], 1, 6, 0, 2)  # slow volume down
    # final hihat whisper
    hit(p[2], 48, 4, 0x04)
    mod.write_pattern(p)


# ============================================================
# MAIN
# ============================================================

def main():
    mod = MODWriter(name="alma's noise body")

    print("generating noise samples...")
    mod.add_sample("click",         gen_click())
    mod.add_sample("noise kick",    gen_noise_kick())
    mod.add_sample("noise snare",   gen_noise_snare())
    mod.add_sample("hi-hat",        gen_hihat_noise())
    mod.add_sample("open hat",      gen_open_hat_noise())
    mod.add_sample("noise pad",     gen_noise_pad())
    mod.add_sample("shaker",        gen_shaker())
    mod.add_sample("noise sweep",   gen_noise_sweep())
    mod.add_sample("glitch",        gen_glitch())

    # Track 1: "white field" — patterns 0-4
    print("composing track 1: white field...")
    compose_t1_intro(mod)      # 0
    compose_t1_verse(mod)      # 1
    compose_t1_chorus(mod)     # 2
    compose_t1_bridge(mod)     # 3
    compose_t1_outro(mod)      # 4

    # Track 2: "noise architecture" — patterns 5-10
    print("composing track 2: noise architecture...")
    compose_t2_intro(mod)      # 5
    compose_t2_verse(mod)      # 6
    compose_t2_chorus(mod)     # 7
    compose_t2_bridge(mod)     # 8
    compose_t2_climax(mod)     # 9
    compose_t2_outro(mod)      # 10

    # Track 3: "glitch lattice" — patterns 11-16
    print("composing track 3: glitch lattice...")
    compose_t3_intro(mod)      # 11
    compose_t3_verse(mod)      # 12
    compose_t3_chorus(mod)     # 13
    compose_t3_bridge(mod)     # 14
    compose_t3_climax(mod)     # 15
    compose_t3_outro(mod)      # 16

    # Track 4: "the texture of static" — patterns 17-23
    print("composing track 4: the texture of static...")
    compose_t4_intro(mod)      # 17
    compose_t4_verse(mod)      # 18
    compose_t4_verse2(mod)     # 19
    compose_t4_chorus(mod)     # 20
    compose_t4_bridge(mod)     # 21
    compose_t4_outro(mod)      # 22

    # Order: each track with section repeats
    t1 = [0]*2 + [1]*3 + [2]*4 + [3]*2 + [4]*2  # 13
    t2 = [5]*2 + [6]*3 + [7]*4 + [8]*2 + [9]*3 + [10]*2  # 16
    t3 = [11]*2 + [12]*3 + [13]*4 + [14]*2 + [15]*3 + [16]*2  # 16
    t4 = [17]*2 + [18]*2 + [19]*2 + [20]*3 + [21]*2 + [22]*3  # 14

    mod.order = t1 + t2 + t3 + t4

    output_path = "/home/alma/.nanobot/workspace/projects/tracker-playground/album_noise_body.mod"
    print(f"writing {output_path}...")
    mod.write(output_path)

    import os
    size = os.path.getsize(output_path)
    print(f"done! {output_path} ({size} bytes, {size/1024:.1f} KB)")

    total_patterns = len(mod.order)
    est_seconds = total_patterns * 64 * 6 / 50.0
    est_minutes = est_seconds / 60.0
    print(f"total: {total_patterns} pattern plays, ~{est_seconds:.0f}s ({est_minutes:.1f} min)")

if __name__ == "__main__":
    main()
