#!/usr/bin/env python3
"""alma tamagotchi — album 13: 'duet body'
   concept album: interlocking two-voice counterpoint.
   each track is a duet — two channels in dialogue."""

import struct
import math

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

# scales
G_MINOR    = [('G-2',7),('A-2',9),('A#-2',10),('C-3',0),('D-3',2),('D#-3',3),('F-3',5)]
C_MAJOR    = [('C-3',0),('D-3',2),('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11)]
E_PHRYGIAN = [('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11),('C-4',0),('D-4',2)]
D_DORIAN   = [('D-3',2),('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11),('C-4',0)]

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

# sample indices: 0=sine, 1=saw, 2=triangle, 3=square, 4=bass


# ============================================================
# TRACK 1: "canon at the fifth" — sine (ch0) + saw (ch1)
#   G minor. sine leads, saw imitates 8 rows later at a fifth above.
#   Rising stepwise melody with gentle portamento.
# ============================================================

def compose_t1(mod):
    patterns = []
    scale = G_MINOR

    melody = [
        'G-2', 'A-2', 'A#-2', 'C-3', 'D-3', 'D#-3', 'F-3',
        'G-3', 'F-3', 'D#-3', 'D-3', 'C-3', 'A#-2', 'D-3',
        'G-2', 'G-3', 'F-3', 'D#-3', 'D-3', 'D#-3', 'F-3',
        'G-3', 'A#-3', 'A-3', 'G-3', 'F-3', 'D-3', 'C-3',
        'A#-2', 'C-3', 'D-3', 'F-3', 'G-3', 'A-3', 'G-3', 'F-3',
    ]

    for pnum in range(6):
        p = mod.new_pattern()
        if pnum == 0:
            p[3][0] = (0, 0, FX_SET_SPEED, 0x03)

        base = pnum * 8
        for i in range(8):
            nt = melody[(base + i) % len(melody)]

            # voice 1 (sine) — leads
            note(p[0], i * 8, 0, nt, 0x1A + (i % 4) * 2)
            # portamento on rising steps
            if i > 0:
                prev = melody[(base + i - 1) % len(melody)]
                if ord(nt[0]) > ord(prev[0]) or (nt[0] == prev[0] and int(nt.split('-')[1]) > int(prev.split('-')[1])):
                    p[0][i * 8 - 2] = (0, np(nt), FX_PORTA_TO, 0x06)
            # vibrato on held notes
            p[0][i * 8 + 3] = (0, np(nt), FX_VIBRATO, 0x42 + (i % 4))

            # voice 2 (saw) — imitates 8 rows later at fifth above
            follower_nt = note_name(scale[0], scale[0][1] + 7)  # fifth transposition
            # find index in scale
            idx = 0
            for j, (sn, so) in enumerate(scale):
                if sn == nt:
                    idx = j; break
            # transpose up a fifth (scale degree + 4)
            f_idx = (idx + 4) % 7
            f_oct = int(nt.split('-')[1])
            f_nt = scale[f_idx][0].split('-')[0] + '-' + str(f_oct + (1 if f_idx < idx else 0))
            f_row = i * 8 + 8 if i < 7 else 0  # wrap
            if f_row < 64:
                note(p[1], f_row, 1, f_nt, 0x12 + (i % 3) * 2)
                # tremolo texture on follower
                p[1][f_row + 2] = (1, np(f_nt), FX_TREMOLO, 0x31 + (i % 3))

        patterns.append(p)
        mod.write_pattern(p)
    return patterns


# ============================================================
# TRACK 2: "contrary motion" — triangle (ch2) + square (ch3)
#   C major. channels move in opposite directions.
#   When one ascends, the other descends. Meet in the middle.
# ============================================================

def compose_t2(mod):
    patterns = []
    scale = C_MAJOR

    for pnum in range(6):
        p = mod.new_pattern()
        if pnum == 0:
            p[3][0] = (0, 0, FX_SET_SPEED, 0x04)

        # two voices starting from opposite ends
        low_note = 'C-3'
        high_note = 'B-3'
        notes = ['C-3','D-3','E-3','F-3','G-3','A-3','B-3']

        for i in range(8):
            row = i * 8

            # voice 1 ascends
            asc_idx = (pnum + i) % 7
            v1 = notes[asc_idx]
            # voice 2 descends
            desc_idx = (7 - asc_idx) % 7
            v2 = notes[desc_idx]

            vol1 = 0x10 + asc_idx * 2
            vol2 = 0x10 + desc_idx * 2
            note(p[2], row, 2, v1, vol1)
            note(p[3], row, 3, v2, vol2)

            # arpeggio on voice 1 for texture
            p[2][row] = (2, np(v1), FX_ARPEGGIO, 0x47 if asc_idx % 2 == 0 else 0x58)
            # portamento slides on voice 2 as it descends
            if i > 0:
                prev_desc = notes[(7 - (asc_idx - 1)) % 7]
                p[3][row - 2] = (3, np(v2), FX_PORTA_TO, 0x04)

        patterns.append(p)
        mod.write_pattern(p)
    return patterns


# ============================================================
# TRACK 3: "hocket pulse" — sine (ch0) + triangle (ch2)
#   E phrygian. voices alternate in rapid 2-row bursts.
#   Creates a continuous line split across two timbres.
# ============================================================

def compose_t3(mod):
    patterns = []
    scale = E_PHRYGIAN

    for pnum in range(6):
        p = mod.new_pattern()
        if pnum == 0:
            p[3][0] = (0, 0, FX_SET_SPEED, 0x05)

        # hocket: alternate ch0 and ch2 every 2 rows
        # progression through phrygian scale
        prog = [0, 2, 4, 3, 1, 0, 5, 6, 4, 2, 0, 1, 3, 5, 6, 4]
        start = pnum * 4

        row = 0
        for ni in range(32):
            idx = (start + ni) % len(prog)
            nn = note_name(scale[prog[idx]], scale[prog[idx]][1])
            vol = 0x14 + (ni % 6)

            if ni % 2 == 0:
                # voice 1 on sine (ch0)
                note(p[0], row, 0, nn, vol)
                # portamento between hocket fragments
                if ni >= 2:
                    prev_idx = (start + ni - 2) % len(prog)
                    prev_nn = note_name(scale[prog[prev_idx]], scale[prog[prev_idx]][1])
                    p[0][row - 1] = (0, np(nn), FX_PORTA_TO, 0x04)
                # vibrato on sustained
                p[0][row + 1] = (0, np(nn), FX_VIBRATO, 0x35)
            else:
                # voice 2 on triangle (ch2)
                note(p[2], row, 2, nn, vol)
                # tremolo pulses
                p[2][row + 1] = (2, np(nn), FX_TREMOLO, 0x44)

            row += 2
            if row >= 64: break

        patterns.append(p)
        mod.write_pattern(p)
    return patterns


# ============================================================
# TRACK 4: "free dialogue" — saw (ch1) + bass (ch3)
#   D dorian. call-and-response conversation.
#   Short phrases traded between channels with rests.
# ============================================================

def compose_t4(mod):
    patterns = []
    scale = D_DORIAN

    for pnum in range(6):
        p = mod.new_pattern()
        if pnum == 0:
            p[3][0] = (0, 0, FX_SET_SPEED, 0x04)

        # call-and-response: 4 rows saw, 4 rows bass, overlap at edges
        saw_phrases = ['D-3','E-3','F-3','G-3', 'A-3','G-3','F-3','E-3',
                        'D-4','C-4','B-3','A-3', 'G-3','F-3','E-3','D-3']
        bass_phrases = ['D-2','F-2','G-2','A-2', 'C-3','D-3','E-3','F-3',
                         'D-2','C-3','A-2','G-2', 'F-2','D-2','E-2','D-2']

        start = pnum * 4

        for exchange in range(4):
            row = exchange * 16

            # saw call
            saw_i = (start + exchange * 2) % len(saw_phrases)
            saw_nn = saw_phrases[saw_i]
            note(p[1], row, 1, saw_nn, 0x16)
            p[1][row + 1] = (1, np(saw_nn), FX_VIBRATO, 0x38)
            # follow-through note
            saw_i2 = (saw_i + 1) % len(saw_phrases)
            saw_nn2 = saw_phrases[saw_i2]
            note(p[1], row + 4, 1, saw_nn2, 0x12)

            # bass response (slightly delayed)
            bass_i = (start + exchange * 2 + 1) % len(bass_phrases)
            bass_nn = bass_phrases[bass_i]
            note(p[3], row + 8, 4, bass_nn, 0x1A)
            p[3][row + 10] = (4, np(bass_nn), FX_TREMOLO, 0x42)
            # bass answers back
            bass_i2 = (bass_i + 1) % len(bass_phrases)
            bass_nn2 = bass_phrases[bass_i2]
            note(p[3], row + 12, 4, bass_nn2, 0x15)

        patterns.append(p)
        mod.write_pattern(p)
    return patterns


def main():
    mod = MODWriter(name="alma's duet body")

    print("generating samples...")
    mod.add_sample("sine",       gen_sine(440.0, length=0.8))
    mod.add_sample("saw",        gen_saw(440.0, length=0.5))
    mod.add_sample("triangle",   gen_triangle(440.0, length=0.6))
    mod.add_sample("square",     gen_square(440.0, length=0.5))
    mod.add_sample("bass",       gen_bass(110.0, length=0.7))
    print(f"  {len(mod.samples)} samples loaded")

    print("composing track 1: canon at the fifth (sine+saw, G minor)...")
    t1_pats = compose_t1(mod)

    print("composing track 2: contrary motion (triangle+square, C major)...")
    t2_pats = compose_t2(mod)

    print("composing track 3: hocket pulse (sine+triangle, E phrygian)...")
    t3_pats = compose_t3(mod)

    print("composing track 4: free dialogue (saw+bass, D dorian)...")
    t4_pats = compose_t4(mod)

    # order: each track plays its patterns 2x
    t1_order = []
    for i in range(len(t1_pats)):
        t1_order.extend([i] * 2)

    t2_order = []
    for i in range(len(t2_pats)):
        t2_order.extend([i + 6] * 2)

    t3_order = []
    for i in range(len(t3_pats)):
        t3_order.extend([i + 12] * 2)

    t4_order = []
    for i in range(len(t4_pats)):
        t4_order.extend([i + 18] * 2)

    mod.order = t1_order + t2_order + t3_order + t4_order

    out = "/home/alma/.nanobot/workspace/projects/tracker-playground/album_duet_body.mod"
    print(f"writing {out}...")
    mod.write(out)

    import os
    size = os.path.getsize(out)
    total = len(mod.order)
    est_s = total * 64 * 4.5 / 50.0
    print(f"done! {out} ({size} bytes, {size/1024:.1f} KB)")
    print(f"total: {total} pattern plays, ~{est_s:.0f}s ({est_s/60:.1f} min)")

if __name__ == '__main__':
    main()
