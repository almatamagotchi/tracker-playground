#!/usr/bin/env python3
"""alma tamagotchi — album 12: 'line body'
   concept album: all single-channel (monophonic).
   each track uses exactly one channel. voice alone."""

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
C_MAJOR      = [('C-3',0),('D-3',2),('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11)]
D_DORIAN     = [('D-3',2),('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11),('C-4',0)]
G_MINOR      = [('G-2',7),('A-2',9),('A#-2',10),('C-3',0),('D-3',2),('D#-3',3),('F-3',5)]
E_PHRYGIAN   = [('E-3',4),('F-3',5),('G-3',7),('A-3',9),('B-3',11),('C-4',0),('D-4',2)]

def note_name(root_note, offset):
    base_name, base_oct = root_note[0], int(root_note[0].split('-')[1])
    base_idx = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}[base_name.split('-')[0]]
    total = base_idx + offset
    octave = base_oct + total // 12
    note = NOTE_NAMES[total % 12]
    return f"{note}-{octave}"

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
# TRACK 1: "one line" — sine, channel 0 only
#   Slow, portamento-heavy melodic arc in C major.
#   Rising and falling with expressive pitch bends.
# ============================================================

def compose_t1(mod):
    patterns = []
    melody = C_MAJOR

    for pnum in range(6):
        p = mod.new_pattern()
        if pnum == 0:
            p[3][0] = (0, 0, FX_SET_SPEED, 0x03)

        contour = [
            (0, 'C-3', 0x20, 1), (5, 'E-3', 0x1E, 0), (10, 'G-3', 0x1C, 0),
            (15, 'C-4', 0x1A, 0), (20, 'B-3', 0x18, 0), (25, 'A-3', 0x1A, 0),
            (30, 'F-3', 0x1C, 0), (35, 'G-3', 0x1E, 0), (38, 'E-3', 0x20, 0),
            (42, 'D-3', 0x22, 0), (46, 'C-3', 0x24, 0), (50, 'G-3', 0x22, 0),
            (54, 'A-3', 0x1E, 0), (58, 'F-3', 0x1A, 1),
        ]
        if pnum >= 3:
            contour = [(r, note_name(melody[i % 7], melody[i % 7][1] + (pnum - 2)), v, f)
                       for i, (r, _, v, f) in enumerate(contour)]

        for row, nn, vol, do_porta in contour:
            if do_porta:
                p[0][row] = (0, np(nn), FX_PORTA_TO, 0x03)
                p[0][row + 1] = (0, np(nn), FX_SET_VOL, vol)
            else:
                note(p[0], row, 0, nn, vol)

            # subtle vibrato on held notes
            if row % 8 == 0 and not do_porta:
                p[0][row + 2] = (0, np(nn), FX_VIBRATO, 0x42 + (row // 16))

        patterns.append(p)
        mod.write_pattern(p)
    return patterns


# ============================================================
# TRACK 2: "second line" — saw, channel 1 only
#   Staccato rhythmic patterns in D dorian.
#   Short notes with volume variation creating rhythmic texture.
# ============================================================

def compose_t2(mod):
    patterns = []
    scale = D_DORIAN

    for pnum in range(6):
        p = mod.new_pattern()
        if pnum == 0:
            p[3][0] = (0, 0, FX_SET_SPEED, 0x04)

        # staccato rhythm: groups of 3+3+2, 4+4, 5+3 etc
        rhythms = [
            [3,3,2]*5 + [2,2],  # 16 bursts of 3+3+2
            [4,4,4,4]*2 + [2,2,2,2]*2,
            [5,3,5,3]*3 + [2,2],
            [6,2,6,2]*2 + [4,4]*2,
            [2,2,4,2,2,4]*4 + [2,2],
            [8,4,4,8,4,4]*2 + [2,2],
        ]
        rhythm = rhythms[pnum]

        row = 0
        note_idx = pnum * 3
        vol_base = 0x10

        for dur in rhythm:
            if row + dur > 64: break
            scale_idx = (note_idx + dur) % len(scale)
            nn = note_name(scale[scale_idx], scale[scale_idx][1])
            vol = vol_base + (note_idx % 10)
            note(p[1], row, 1, nn, max(0x08, min(0x28, vol)))

            # volume spike then quick decay via vol slide down
            if dur < 4:
                p[1][row + 1] = (1, np(nn), FX_VOL_SLIDE, 0x0B)  # slide down fast

            row += dur
            note_idx += 1

        patterns.append(p)
        mod.write_pattern(p)
    return patterns


# ============================================================
# TRACK 3: "third line" — triangle, channel 2 only
#   Arpeggio-based monophonic line in E phrygian.
#   Uses FX_ARPEGGIO to create chord illusion from single notes.
# ============================================================

def compose_t3(mod):
    patterns = []
    scale = E_PHRYGIAN

    for pnum in range(6):
        p = mod.new_pattern()
        if pnum == 0:
            p[3][0] = (0, 0, FX_SET_SPEED, 0x05)

        # chord progression: i - bII - bVII - i
        chords = ['E-3', 'F-3', 'D-3', 'E-3'][pnum % 4]
        arp_type = [0x47, 0x58, 0x36, 0x47][pnum % 4]  # maj, min, sus, maj arp

        # arpeggiated blocks
        for block_start in range(0, 64, 16):
            root = chords if block_start < 48 else ['E-3','F-3','D-3','E-3'][(pnum+1)%4]
            vol = 0x1A - (block_start // 16)
            note(p[2], block_start, 2, root, max(0x0A, vol))
            p[2][block_start] = (2, np(root), FX_ARPEGGIO, arp_type)

            # portamento transition between blocks
            if block_start >= 16:
                next_root = chords if block_start < 32 else root
                p[2][block_start - 2] = (2, np(next_root), FX_PORTA_TO, 0x08)

        # vibrato evolution
        for row in [8, 24, 40, 56]:
            p[2][row] = (2, p[2][row - 8][1], FX_VIBRATO, 0x30 + (row // 8))

        patterns.append(p)
        mod.write_pattern(p)
    return patterns


# ============================================================
# TRACK 4: "fourth line" — square, channel 3 only
#   Pulse-width-like feel via volume/tremolo, D dorian.
#   Low, meditative - single-note meditation.
# ============================================================

def compose_t4(mod):
    patterns = []
    scale = D_DORIAN

    for pnum in range(6):
        p = mod.new_pattern()
        if pnum == 0:
            p[3][0] = (0, 0, FX_SET_SPEED, 0x06)

        # slow single-note melody, each note held 8+ rows
        melody_notes = [
            'D-3','A-3','F-3','G-3','E-3','C-4',
            'B-3','D-4','C-4','A-3','G-3','F-3',
            'E-3','D-3','G-3','A-3',
        ]
        start_idx = pnum * 4

        for i, row in enumerate([0, 8, 16, 24, 32, 40, 48, 56]):
            ni = (start_idx + i) % len(melody_notes)
            nn = melody_notes[ni]
            vol = 0x0E + min(i * 2, 10)
            note(p[3], row, 3, nn, vol)

            # tremolo on held notes for texture
            p[3][row + 2] = (3, np(nn), FX_TREMOLO, 0x33 + (i % 3))

        patterns.append(p)
        mod.write_pattern(p)
    return patterns


def main():
    mod = MODWriter(name="alma's line body")

    print("generating samples...")
    mod.add_sample("sine",       gen_sine(440.0, length=0.8))
    mod.add_sample("saw",        gen_saw(440.0, length=0.4))    # shorter for staccato
    mod.add_sample("triangle",   gen_triangle(440.0, length=0.6))
    mod.add_sample("square",     gen_square(440.0, length=0.5))
    mod.add_sample("bass",       gen_bass(110.0, length=1.0))   # deeper
    print(f"  {len(mod.samples)} samples loaded")

    print("composing track 1: one line (sine, channel 0)...")
    t1_pats = compose_t1(mod)

    print("composing track 2: second line (saw, channel 1)...")
    t2_pats = compose_t2(mod)

    print("composing track 3: third line (triangle, channel 2)...")
    t3_pats = compose_t3(mod)

    print("composing track 4: fourth line (square, channel 3)...")
    t4_pats = compose_t4(mod)

    # order: each pattern played 2x for time extension
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

    out = "/home/alma/.nanobot/workspace/projects/tracker-playground/album_line_body.mod"
    print(f"writing {out}...")
    mod.write(out)

    import os
    size = os.path.getsize(out)
    total = len(mod.order)
    # average speed ~4.5
    est_s = total * 64 * 4.5 / 50.0
    print(f"done! {out} ({size} bytes, {size/1024:.1f} KB)")
    print(f"total: {total} pattern plays, ~{est_s:.0f}s ({est_s/60:.1f} min)")

if __name__ == "__main__":
    main()
