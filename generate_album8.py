#!/usr/bin/env python3
"""alma tamagotchi — album 8: 'quarter-tone body'
   microtonal exploration: quarter-tone detuned samples + portamento slides.
   24-tone equal temperament via paired standard/+50¢/−50¢ samples."""

import struct
import math
import random

# === constants ===

PERIOD_TABLE = [
    [1712,1616,1524,1440,1356,1280,1208,1140,1076,1016,960,906],  # oct 1
    [ 856, 808, 762, 720, 678, 640, 604, 570, 538, 508, 480, 453],  # oct 2
    [ 428, 404, 381, 360, 339, 320, 302, 285, 269, 254, 240, 226],  # oct 3
    [ 214, 202, 190, 180, 170, 160, 151, 143, 135, 127, 120, 113],  # oct 4
    [ 107, 101,  95,  90,  85,  80,  75,  71,  67,  63,  60,  56],  # oct 5
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

QT_UP = 2.0 ** (1.0 / 24.0)   # +50 cents
QT_DN = 2.0 ** (-1.0 / 24.0)  # −50 cents

def np(name):
    note_map = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    if '-' in name:
        parts = name.split('-')
        n, octave = parts[0], int(parts[1])
        return PERIOD_TABLE[octave - 1][note_map[n]]
    else:
        raise ValueError(f"can't parse note: {name}")
    return PERIOD_TABLE[octave - 1][note_map[n]]

E = (0, 0, 0, 0)

# === waveform generators ===

def gen_sine(freq=440.0, sr=11025, length=0.5, vol=0.7):
    nsamples = int(sr * length)
    data = []
    for i in range(nsamples):
        t = i / sr
        env = 1.0
        if t > length * 0.8:
            env = 1.0 - (t - length * 0.8) / (length * 0.2)
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
        env = 1.0
        if t > length * 0.8:
            env = 1.0 - (t - length * 0.8) / (length * 0.2)
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
        env = 1.0
        if t > length * 0.8:
            env = 1.0 - (t - length * 0.8) / (length * 0.2)
        v = int(v * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_soft_lead(freq=440.0, sr=11025, length=0.5, vol=0.6):
    """sine with gentle harmonics — warm lead"""
    nsamples = int(sr * length)
    data = []
    for i in range(nsamples):
        t = i / sr
        w = 2 * math.pi * freq * t
        wave = (math.sin(w) * 0.8 + math.sin(2*w) * 0.15 + math.sin(3*w) * 0.05)
        env = 1.0
        if t > length * 0.7:
            env = 1.0 - (t - length * 0.7) / (length * 0.3)
        v = int(wave * 127 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_glass(freq=440.0, sr=11025, length=0.6, vol=0.5):
    """high harmonics — glassy, bell-like"""
    nsamples = int(sr * length)
    data = []
    for i in range(nsamples):
        t = i / sr
        w = 2 * math.pi * freq * t
        wave = (math.sin(w) * 0.3 + math.sin(3*w) * 0.3 + math.sin(5*w) * 0.2 +
                math.sin(7*w) * 0.1 + math.sin(9*w) * 0.1)
        env = math.exp(-t * 3.0)
        v = int(wave * 127 * vol * env)
        data.append(max(-128, min(127, v)))
    return bytes(b & 0xFF for b in data)

def gen_pulse(freq=440.0, sr=11025, duty=0.25, length=0.4, vol=0.55):
    """pulse wave with variable duty"""
    nsamples = int(sr * length)
    period_samples = sr / freq if freq > 0 else nsamples
    data = []
    for i in range(nsamples):
        t = i / sr
        phase = (i % int(period_samples)) / period_samples
        v = 127 * vol if phase < duty else -127 * vol
        env = 1.0
        if t > length * 0.75:
            env = 1.0 - (t - length * 0.75) / (length * 0.25)
        v = int(v * env)
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

def porta_up(ch, row, sample, pitch, speed, vol=None):
    """play note with portamento up"""
    per = np(pitch)
    if vol is not None:
        ch[row] = (sample, per, FX_SET_VOL, vol)
        ch[row] = (ch[row][0], ch[row][1], FX_PORTA_UP, speed)
    else:
        ch[row] = (sample, per, FX_PORTA_UP, speed)

def porta_down(ch, row, sample, pitch, speed, vol=None):
    """play note with portamento down"""
    per = np(pitch)
    if vol is not None:
        ch[row] = (sample, per, FX_SET_VOL, vol)
        ch[row] = (ch[row][0], ch[row][1], FX_PORTA_DOWN, speed)
    else:
        ch[row] = (sample, per, FX_PORTA_DOWN, speed)

def porta_to(ch, row, sample, pitch, target_speed, vol=None):
    """slide toward this note (use with a prior note on this channel)"""
    per = np(pitch)
    if vol is not None:
        ch[row] = (sample, per, FX_SET_VOL, vol)
        ch[row] = (ch[row][0], ch[row][1], FX_PORTA_TO, target_speed)
    else:
        ch[row] = (sample, per, FX_PORTA_TO, target_speed)

def qt_note(ch, row, sample_std, sample_qt, pitch, vol=None):
    """play a quarter-tone note: use sample_qt to get the +50¢ detuning at standard pitch"""
    per = np(pitch)
    if vol is not None:
        ch[row] = (sample_qt, per, FX_SET_VOL, vol)
    else:
        ch[row] = (sample_qt, per, 0, 0)

def rest():
    return E


# sample indices in the MOD (after loading):
# 0=sine_std, 1=sine_qt_up, 2=sine_qt_dn
# 3=saw_std, 4=saw_qt_up, 5=saw_qt_dn
# 6=square_std, 7=square_qt_up, 8=square_qt_dn
# 9=soft_std, 10=soft_qt_up, 11=soft_qt_dn
# 12=glass_std, 13=glass_qt_up, 14=glass_qt_dn
# 15=pulse_std, 16=pulse_qt_up, 17=pulse_qt_dn

# quarter-tone scale: semitones + quarter-tone steps
# 24 steps per octave: 0, 1, 2, ..., 23
# semitone = step // 2, qtoffset = step % 2 (0=standard, 1=quarter-tone-up)

def qt_scale_step(step, octave=3):
    """map 24-tone step to (note_name, sample_offset). step 0 = C."""
    semitone = step // 2
    qt_offset = step % 2
    notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    note_oct = octave + semitone // 12
    note_idx = semitone % 12
    return f"{notes[note_idx]}-{note_oct}", qt_offset


# ============================================================
# TRACK 1: "quarter-tone lullaby" — gentle, exploring the
#           uncanny space of between-notes. Soft sine lead,
#           quarter-tone steps create a haunting lullaby.
# ============================================================

def t1_24tone_scale():
    """24-tone scale steps for a quarter-tone lullaby melody (in key of C minor-ish, microtonal)"""
    # quarter-tone steps from C-3: 0=C, 1=C½♯, 3=D, 5=D♯, 7=F, 8=F½♯, 10=G, 12=A, 13=A½♯, 15=B♭
    steps = [0, 3, 7, 5, 3, 0, 8, 10, 12, 10, 8, 7, 5, 3, 0, -1,
             0, 3, 7, 10, 12, 15, 12, 10, 8, 7, 5, 3, 5, 7, 0, -1]
    result = []
    for s in steps:
        if s < 0:
            result.append(None)
        else:
            result.append(qt_scale_step(s, 3))
    return result

def compose_t1_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x06)
    scale = t1_24tone_scale()
    # play the scale slowly on ch3 (soft lead — sample 9 std, 10 qt_up)
    for i, entry in enumerate(scale):
        r = i * 2
        if r >= 64: break
        if entry is None: continue
        note_name, qt_off = entry
        smp = 10 if qt_off else 9
        note(p[3], r, smp, note_name, 0x24)
    # subtle bass pulse on ch0 — sine (0 std, 1 qt_up)
    for r in [0, 16, 32, 48]:
        _, qt_off = qt_scale_step(0, 2)  # C-2
        smp = 1 if qt_off else 0
        note(p[0], r, smp, 'C-2', 0x1C)
    # soft hihat-like pulse using glass sample
    for r in range(0, 64, 8):
        note(p[2], r, 12, 'C-5', 0x0E)
    mod.write_pattern(p)

def compose_t1_verse(mod):
    p = mod.new_pattern()
    # melody: quarter-tone sine lead
    melody_steps = [0, 3, 5, 7, 10, 8, 7, 5, 3, 0, -2, 0, 8, 10, 12, 10, 8, 7, 5, 3]
    for i, s in enumerate(melody_steps):
        r = i * 3
        if r >= 64: break
        if s < 0: continue
        note_name, qt_off = qt_scale_step(s, 3)
        smp = 10 if qt_off else 9
        note(p[3], r, smp, note_name, 0x28)
    # bass: alternating C and F quarter-tone
    bass_steps = [(0, 2), (7, 2), (5, 2), (8, 2)]  # C-2, G-2, F-2, F½♯-2
    for i, (s, oct) in enumerate(bass_steps):
        r = i * 16
        note_name, qt_off = qt_scale_step(s, oct)
        smp = 1 if qt_off else 0
        note(p[0], r, smp, note_name, 0x20)
    # glass percussion — standard and quarter-tone
    for r in range(0, 64, 8):
        qt = (r // 8) % 2
        smp = 13 if qt else 12
        note(p[2], r, smp, 'C-4', 0x10 if qt else 0x14)
    # soft pad drone on ch1
    note(p[1], 0, 9, 'C-3', 0x12)
    note(p[1], 32, 9, 'G-3', 0x10)
    mod.write_pattern(p)

def compose_t1_chorus(mod):
    p = mod.new_pattern()
    # richer melody
    melody = [0, 3, 7, 10, 12, 15, 12, 10, 7, 8, 7, 5, 3, 0, -2, 0,
              8, 10, 12, 13, 15, 12, 10, 8]
    for i, s in enumerate(melody):
        r = i * 2 + (i // 8)
        if r >= 64: break
        if s < 0: continue
        note_name, qt_off = qt_scale_step(s, 3)
        smp = 10 if qt_off else 9
        vol = 0x2C if i % 4 == 0 else 0x24
        note(p[3], r, smp, note_name, vol)
    # bass walks quarter-tone steps
    for i, s in enumerate([0, 3, 5, 7, 8, 5, 3, 0]):
        r = i * 8
        note_name, qt_off = qt_scale_step(s, 2)
        smp = 4 if qt_off else 3  # saw bass
        note(p[0], r, smp, note_name, 0x24)
    # quarter-tone glass arpeggio
    for i, s in enumerate([0, 7, 12, 15, 12, 7, 3, 10]):
        r = i * 6
        if r >= 64: break
        note_name, qt_off = qt_scale_step(s, 4)
        smp = 13 if qt_off else 12
        note(p[2], r, smp, note_name, 0x12)
    # pad: sustained quarter-tone chord
    note(p[1], 0, 9, 'C-3', 0x16)
    note(p[1], 32, 9, 'G-3', 0x14)
    mod.write_pattern(p)

def compose_t1_bridge(mod):
    p = mod.new_pattern()
    # sparse, meditative — slow quarter-tone portamento slides
    for i, s in enumerate([0, 3, 7, 10]):
        r = i * 16
        note_name, qt_off = qt_scale_step(s, 3)
        smp = 10 if qt_off else 9
        note(p[3], r, smp, note_name, 0x1C)
        # gentle vibrato for expressiveness
        if r + 2 < 64:
            p[3][r+2] = (smp, np(note_name), FX_VIBRATO, 0x63)
    # bass: single note with portamento slide
    note(p[0], 0, 0, 'C-2', 0x18)
    p[0][2] = (0, np('C-2'), FX_PORTA_UP, 0x01)  # micro-slide up
    for r in [16, 32, 48]:
        note(p[0], r, 0, 'F-2', 0x14)
    # glass wind chimes
    for r in [4, 20, 36, 52]:
        smp = 13 if (r//16) % 2 else 12
        note(p[2], r, smp, 'C-5', 0x0C)
    # soft pad fade
    note(p[1], 0, 9, 'C-3', 0x0E)
    note(p[1], 32, 11, 'D#-3', 0x0A)
    mod.write_pattern(p)

def compose_t1_outro(mod):
    p = mod.new_pattern()
    # dissolution — single sine quarter-tone shimmer, fade
    for r in [0, 16, 32, 48]:
        note(p[3], r, 10, 'C-4', 0x14 - r//16)
        note(p[0], r, 0, 'C-2', 0x10 - r//48)
    for r in [8, 24, 40, 56]:
        note(p[2], r, 12, 'C-5', 0x08)
    note(p[1], 0, 9, 'C-3', 0x0A)
    mod.write_pattern(p)


# ============================================================
# TRACK 2: "portamento glissando" — heavy use of
#           FX_PORTA_UP/DOWN for continuous microtonal slides
#           between notes. The pitch never snaps — it glides.
# ============================================================

def compose_t2_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x05)
    # a single saw note slides up a quarter-tone slowly
    note(p[0], 0, 3, 'C-2', 0x20)
    p[0][2] = (3, np('C-2'), FX_PORTA_UP, 0x01)  # micro-bend
    # soft lead does a portamento-to slide
    note(p[3], 0, 9, 'C-3', 0x1E)
    p[3][16] = (9, np('E-3'), FX_PORTA_TO, 0x03)  # slide toward E
    p[3][48] = (9, np('F-3'), FX_PORTA_TO, 0x02)  # slide toward F
    # glass sparkles
    for r in range(0, 64, 12):
        note(p[2], r, 12, 'C-4', 0x0E)
    note(p[1], 0, 9, 'C-3', 0x10)
    mod.write_pattern(p)

def compose_t2_verse(mod):
    p = mod.new_pattern()
    # portamento bassline: each note slides up into the next
    bass_notes = [('C-2', 3), ('D#-2', 3), ('F-2', 3), ('G-2', 3),
                  ('A-2', 3), ('G-2', 3), ('F-2', 3), ('D#-2', 3)]
    for i, (nn, smp) in enumerate(bass_notes):
        r = i * 8
        note(p[0], r, smp, nn, 0x24)
        if i < len(bass_notes) - 1 and r + 6 < 64:
            p[0][r+6] = (smp, np(nn), FX_PORTA_UP, 0x04)
    # melodic line: portamento-to weaving
    note(p[3], 0, 9, 'C-3', 0x26)
    for i, (nn, r) in enumerate([('E-3', 16), ('F-3', 24), ('G-3', 32),
                                  ('A-3', 40), ('G-3', 48), ('E-3', 56)]):
        p[3][r] = (9, np(nn), FX_PORTA_TO, 0x04 + i % 3)
    # glass percussion with portamento down for microtonal decay
    for r in range(0, 64, 8):
        note(p[2], r, 12, 'C-4', 0x16)
        if r + 1 < 64:
            p[2][r+1] = (12, np('C-4'), FX_PORTA_DOWN, 0x02)
    # pad with slow vibrato
    note(p[1], 0, 9, 'C-3', 0x14)
    mod.write_pattern(p)

def compose_t2_chorus(mod):
    p = mod.new_pattern()
    # denser portamento — all channels sliding
    # bass: faster portamento-up slide
    bass_notes = ['C-2','D#-2','F-2','G-2','A-2','G-2','F#-2','D#-2']
    for i, nn in enumerate(bass_notes):
        r = i * 8
        note(p[0], r, 3, nn, 0x28)
        p[0][r+1] = (3, np(nn), FX_PORTA_UP, 0x03)
    # lead: portamento-to between quarter-tone steps
    lead_targets = [('E-3', 0), ('F½-3', 4), ('G-3', 8), ('A-3', 12),
                    ('G-3', 16), ('F-3', 20), ('E-3', 24), ('C-3', 28)]
    # start at C-3
    note(p[3], 0, 9, 'C-3', 0x2A)
    for nn, r in lead_targets:
        if r >= 64: break
        # determine if this is a quarter-tone target
        if '½' in nn:
            clean = nn.replace('½', '')
            _, qt_off = qt_scale_step({'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}[clean[0]] * 2 + 1, 3)
            smp = 10
            per = np(clean)
        else:
            smp = 9
            per = np(nn)
        p[3][r] = (smp, per, FX_PORTA_TO, 0x06)
    # glass: microtonal portamento down swirl
    for r in range(0, 64, 4):
        if r % 8 == 0:
            note(p[2], r, 12, 'C-5', 0x1A)
            p[2][r+1] = (12, np('C-5'), FX_PORTA_DOWN, 0x01)
        elif r % 8 == 4:
            note(p[2], r, 13, 'C-5', 0x10)
    # pad: slow portamento up the whole pattern
    note(p[1], 0, 9, 'C-3', 0x16)
    p[1][1] = (9, np('C-3'), FX_PORTA_UP, 0x01)
    mod.write_pattern(p)

def compose_t2_bridge(mod):
    p = mod.new_pattern()
    # stripped — solo portamento meditation
    note(p[3], 0, 9, 'C-3', 0x20)
    # slide up through quarter-tones over 64 rows
    for r in [12, 24, 36, 48]:
        p[3][r] = (9, np('C-3'), FX_PORTA_UP, 0x01)
    # sparse bass punctuation
    for r in [0, 32]:
        note(p[0], r, 0, 'C-2', 0x14)
        p[0][r+1] = (0, np('C-2'), FX_PORTA_UP, 0x02)
    # glass wind chimes — microtonal
    for r in [8, 24, 40, 56]:
        note(p[2], r, 13, 'C-5', 0x0A)
    note(p[1], 0, 11, 'D#-3', 0x0C)
    mod.write_pattern(p)

def compose_t2_climax(mod):
    p = mod.new_pattern()
    # full ensemble — rapid portamento exchanges
    for r in range(0, 64, 8):
        note(p[0], r, 3, 'C-2', 0x2C)
        p[0][r+2] = (3, np('C-2'), FX_PORTA_UP, 0x05)
    for r in range(4, 64, 8):
        note(p[0], r, 3, 'G-2', 0x22)
        p[0][r+2] = (3, np('G-2'), FX_PORTA_DOWN, 0x03)
    # lead: portamento-to cascade
    note(p[3], 0, 9, 'C-3', 0x2E)
    targets = [('E-3', 8), ('G-3', 16), ('B-3', 24), ('C-4', 32),
               ('B-3', 40), ('G-3', 48), ('E-3', 56)]
    for nn, r in targets:
        p[3][r] = (9, np(nn), FX_PORTA_TO, 0x08)
    # glass: rapid microtonal glissandi
    for r in range(0, 64, 2):
        if r % 4 == 0:
            note(p[2], r, 12, 'C-4', 0x1C)
            p[2][r+1] = (12, np('C-4'), FX_PORTA_UP, 0x01)
    # pad with portamento
    note(p[1], 0, 9, 'C-3', 0x18)
    for r in [16, 32, 48]:
        p[1][r] = (9, np('C-3'), FX_PORTA_UP, 0x02)
    mod.write_pattern(p)

def compose_t2_outro(mod):
    p = mod.new_pattern()
    # decelerating — portamento slides get slower
    note(p[0], 0, 0, 'C-2', 0x18)
    p[0][2] = (0, np('C-2'), FX_PORTA_UP, 0x01)
    note(p[3], 0, 9, 'C-3', 0x18)
    p[3][16] = (9, np('E-3'), FX_PORTA_TO, 0x01)
    for r in range(0, 64, 16):
        note(p[2], r, 12, 'C-4', 0x0C)
    note(p[1], 0, 9, 'C-3', 0x0C)
    mod.write_pattern(p)


# ============================================================
# TRACK 3: "24-tone lattice" — structure built from the
#           full 24-tone gamut. Geometric patterns exploiting
#           the doubled pitch resolution.
# ============================================================

def t3_cycle(length=16):
    """generate a cycle of 24-tone steps for lattice patterns"""
    # cycle of 24 steps, then repeat shifted
    return [i % 24 for i in range(length)]

def compose_t3_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x04)
    # ascending 24-tone scale over two octaves
    steps = [i % 24 for i in range(24)]
    for i, s in enumerate(steps):
        r = i * 2
        if r >= 56: break
        note_name, qt_off = qt_scale_step(s, 3)
        smp = 10 if qt_off else 9
        note(p[3], r, smp, note_name, 0x18 if i % 3 == 0 else 0x12)
    # bass: fundamental pulse
    for r in [0, 16, 32, 48]:
        note(p[0], r, 0, 'C-2', 0x1C)
    for r in [8, 24, 40, 56]:
        note(p[1], r, 6, 'C-3', 0x10)  # square pulse
    mod.write_pattern(p)

def compose_t3_verse(mod):
    p = mod.new_pattern()
    # interlocking 24-tone patterns on ch2 and ch3
    steps_a = [(i * 5) % 24 for i in range(16)]  # cycle of 5ths mod 24
    steps_b = [(i * 7) % 24 for i in range(16)]  # cycle of 7ths mod 24
    for i, (sa, sb) in enumerate(zip(steps_a, steps_b)):
        r = i * 4
        if r >= 64: break
        # ch2: glass — cycle of 5ths
        na, qa = qt_scale_step(sa, 4)
        smp_a = 13 if qa else 12
        note(p[2], r, smp_a, na, 0x16)
        # ch3: soft lead — cycle of 7ths
        nb, qb = qt_scale_step(sb, 3)
        smp_b = 10 if qb else 9
        note(p[3], r, smp_b, nb, 0x20 if i % 4 == 0 else 0x16)
        # portamento up for micro-glide
        if r + 1 < 64 and i % 2 == 0:
            p[3][r+1] = (smp_b, np(nb), FX_PORTA_UP, 0x01)
    # bass: 24-tone walking
    bass_steps = [0, 4, 8, 12, 16, 12, 8, 4]
    for i, s in enumerate(bass_steps):
        r = i * 8
        note_name, qt_off = qt_scale_step(s, 2)
        smp = 4 if qt_off else 3
        note(p[0], r, smp, note_name, 0x22)
    # pad: square wave drone
    note(p[1], 0, 6, 'C-3', 0x14)
    note(p[1], 32, 6, 'G-3', 0x10)
    mod.write_pattern(p)

def compose_t3_chorus(mod):
    p = mod.new_pattern()
    # dense 24-tone counterpoint — all channels in geometric relationship
    # cycle-of-3rds: (step * 4) mod 24
    for ch_idx, mult in [(2, 4), (3, 5), (1, 7)]:
        for i in range(8):
            s = (i * mult) % 24
            r = i * 8
            note_name, qt_off = qt_scale_step(s, 3 + ch_idx // 3)
            if ch_idx == 1:
                smp = 7 if qt_off else 6  # square
            elif ch_idx == 2:
                smp = 13 if qt_off else 12  # glass
            else:
                smp = 10 if qt_off else 9  # soft lead
            note(p[ch_idx], r, smp, note_name, 0x1E)
            if r + 2 < 64:
                p[ch_idx][r+2] = (smp, np(note_name), FX_PORTA_UP, 0x02)
    # bass: more active
    for i, s in enumerate([(i * 3) % 24 for i in range(8)]):
        r = i * 8
        note_name, qt_off = qt_scale_step(s, 2)
        smp = 16 if qt_off else 15  # pulse bass
        note(p[0], r, smp, note_name, 0x24)
    mod.write_pattern(p)

def compose_t3_bridge(mod):
    p = mod.new_pattern()
    # sparse lattice — isolated 24-tone points
    # prime-number spacing in the lattice
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    for i, p_val in enumerate(primes):
        r = i * 7
        if r >= 64: break
        s = p_val % 24
        note_name, qt_off = qt_scale_step(s, 3)
        smp = 10 if qt_off else 9
        note(p[3], r, smp, note_name, 0x1A)
    # bass: single pedal
    for r in [0, 32]:
        note(p[0], r, 0, 'C-2', 0x16)
    for r in [8, 24, 40, 56]:
        note(p[2], r, 13, 'C-5', 0x0C)
    note(p[1], 0, 9, 'C-3', 0x0E)
    mod.write_pattern(p)

def compose_t3_climax(mod):
    p = mod.new_pattern()
    # maximum 24-tone density — all three melodic channels in counterpoint
    for i in range(16):
        r = i * 4
        s = (i * 7) % 24
        note_name, qt_off = qt_scale_step(s, 4)
        smp = 13 if qt_off else 12
        note(p[2], r, smp, note_name, 0x1C)
        # micro-bend on each hit
        if r + 1 < 64:
            p[2][r+1] = (smp, np(note_name), FX_PORTA_UP, 0x01)
    for i in range(8):
        r = i * 8 + 2
        s = (i * 5) % 24
        note_name, qt_off = qt_scale_step(s, 3)
        smp = 10 if qt_off else 9
        note(p[3], r, smp, note_name, 0x26)
        if r + 1 < 64:
            p[3][r+1] = (smp, np(note_name), FX_PORTA_DOWN, 0x01)
    # bass: 24-tone rapid
    for i in range(8):
        r = i * 8
        s = (i * 3) % 24
        note_name, qt_off = qt_scale_step(s, 2)
        smp = 16 if qt_off else 15
        note(p[0], r, smp, note_name, 0x28)
    # pad: square drone with portamento interest
    note(p[1], 0, 6, 'C-3', 0x18)
    p[1][2] = (6, np('C-3'), FX_PORTA_UP, 0x01)
    for r in [16, 32, 48]:
        note(p[1], r, 8, 'D#-3', 0x14)
    mod.write_pattern(p)

def compose_t3_outro(mod):
    p = mod.new_pattern()
    # lattice dissolves — sparser 24-tone points, fade
    for i in range(8):
        r = i * 8
        s = (i * 11) % 24
        note_name, qt_off = qt_scale_step(s, 4)
        smp = 13 if qt_off else 12
        note(p[2], r, smp, note_name, 0x0E)
    for r in [0, 32]:
        note(p[0], r, 0, 'C-2', 0x10)
    note(p[3], 0, 10, 'C-4', 0x0C)
    note(p[3], 32, 9, 'C-4', 0x08)
    note(p[1], 0, 9, 'C-3', 0x08)
    mod.write_pattern(p)


# ============================================================
# TRACK 4: "the space between" — meditative microtonal piece
#           exploring the emotional quality of between-notes.
#           Very slow, sparse, using portamento to dwell in
#           the cracks between semitones.
# ============================================================

def compose_t4_intro(mod):
    p = mod.new_pattern()
    p[1][0] = (0, 0, FX_SET_SPEED, 0x08)
    # single sine note, slowly sliding up a quarter-tone
    note(p[3], 0, 0, 'C-3', 0x18)
    p[3][2] = (0, np('C-3'), FX_PORTA_UP, 0x01)
    # glass chime — quarter-tone
    for r in [0, 16, 32, 48]:
        note(p[2], r, 13, 'C-4', 0x0E)
    # soft bass pulse
    note(p[0], 0, 0, 'C-2', 0x14)
    note(p[1], 0, 9, 'C-3', 0x0C)
    mod.write_pattern(p)

def compose_t4_verse(mod):
    p = mod.new_pattern()
    # slow melody dwelling between notes
    # play C, then portamento up to C½♯, dwell, then resolve to D
    note(p[3], 0, 9, 'C-3', 0x22)
    p[3][4] = (9, np('C-3'), FX_PORTA_UP, 0x01)
    p[3][16] = (9, np('C-3'), FX_PORTA_UP, 0x00)  # stop slide
    note(p[3], 20, 10, 'C-3', 0x1E)  # quarter-tone sharp sample (C½♯)
    note(p[3], 36, 9, 'D-3', 0x24)   # resolve to D
    p[3][40] = (9, np('D-3'), FX_PORTA_DOWN, 0x01)  # slide back down
    note(p[3], 52, 9, 'C-3', 0x20)

    # bass: slow, spacious
    for r in range(0, 64, 32):
        note(p[0], r, 0, 'C-2', 0x1A)
        p[0][r+2] = (0, np('C-2'), FX_PORTA_UP, 0x01)
    # glass: quarter-tone shimmer
    for r in range(0, 64, 8):
        qt = (r // 8) % 3
        smp = 13 if qt else 12
        note(p[2], r, smp, 'C-4', 0x10)
    # pad
    note(p[1], 0, 9, 'C-3', 0x12)
    mod.write_pattern(p)

def compose_t4_chorus(mod):
    p = mod.new_pattern()
    # richer section — multiple quarter-tone melodies intertwining
    # ch3: main melody
    melody = [(0, 0, 9), (4, 0, 10), (7, 0, 9), (12, 0, 9),
              (15, 0, 10), (12, 0, 9), (7, 1, 9), (0, 0, 9)]
    for i, (s, qt, smp_base) in enumerate(melody):
        r = i * 8
        note_name, _ = qt_scale_step(s, 3)
        smp = smp_base + qt
        note(p[3], r, smp, note_name, 0x28 if i % 2 == 0 else 0x20)
        # occasional portamento-microbend
        if r + 2 < 64 and i % 3 == 0:
            p[3][r+2] = (smp, np(note_name), FX_PORTA_UP, 0x01)
    # bass: quarter-tone walking
    for i, s in enumerate([0, 5, 7, 12, 8, 5, 3, 0]):
        r = i * 8
        note_name, qt_off = qt_scale_step(s, 2)
        smp = 1 if qt_off else 0
        note(p[0], r, smp, note_name, 0x20)
    # glass: counter-melody
    counter = [12, 15, 17, 20, 17, 15, 12, 10]
    for i, s in enumerate(counter):
        r = i * 8 + 4
        if r >= 64: break
        note_name, qt_off = qt_scale_step(s, 4)
        smp = 13 if qt_off else 12
        note(p[2], r, smp, note_name, 0x14)
    # pad swell
    note(p[1], 0, 9, 'C-3', 0x16)
    note(p[1], 32, 11, 'D#-3', 0x14)
    mod.write_pattern(p)

def compose_t4_bridge(mod):
    p = mod.new_pattern()
    # return to sparse — dwelling in the between-space
    # very slow portamento, meditative
    note(p[3], 0, 0, 'C-3', 0x1C)
    p[3][2] = (0, np('C-3'), FX_PORTA_UP, 0x01)
    # sustain the microtonal glide for the whole pattern
    note(p[3], 32, 1, 'C-3', 0x18)  # quarter-tone sample
    # bass: just two notes
    note(p[0], 0, 0, 'C-2', 0x14)
    note(p[0], 32, 0, 'F-2', 0x10)
    # glass: sparse quarter-tone points
    for r in [8, 24, 40, 56]:
        note(p[2], r, 13, 'C-5', 0x0C)
    # pad with vibrato
    note(p[1], 0, 9, 'C-3', 0x10)
    p[1][2] = (9, np('C-3'), FX_VIBRATO, 0x43)
    mod.write_pattern(p)

def compose_t4_outro(mod):
    p = mod.new_pattern()
    # final dissolution — quarter-tone fade with slow portamento down
    note(p[3], 0, 10, 'C-4', 0x14)
    p[3][8] = (10, np('C-4'), FX_PORTA_DOWN, 0x01)
    note(p[0], 0, 0, 'C-2', 0x10)
    for r in [0, 32]:
        note(p[2], r, 13, 'C-5', 0x08)
    note(p[1], 0, 9, 'C-3', 0x0A)
    # final quarter-tone shimmer
    note(p[3], 48, 10, 'C-4', 0x0A)
    mod.write_pattern(p)


# ============================================================
# MAIN
# ============================================================

def main():
    mod = MODWriter(name="alma's qt body")

    freq = 440.0  # A4
    qt_freq_up = freq * QT_UP
    qt_freq_dn = freq * QT_DN

    print("generating standard + quarter-tone samples...")

    # sine
    mod.add_sample("sine_std",    gen_sine(freq, length=0.6))
    mod.add_sample("sine_qt_up",  gen_sine(qt_freq_up, length=0.6))
    mod.add_sample("sine_qt_dn",  gen_sine(qt_freq_dn, length=0.6))
    # saw
    mod.add_sample("saw_std",     gen_saw(freq, length=0.5))
    mod.add_sample("saw_qt_up",   gen_saw(qt_freq_up, length=0.5))
    mod.add_sample("saw_qt_dn",   gen_saw(qt_freq_dn, length=0.5))
    # square
    mod.add_sample("square_std",  gen_square(freq, length=0.5))
    mod.add_sample("square_qt_up",gen_square(qt_freq_up, length=0.5))
    mod.add_sample("square_qt_dn",gen_square(qt_freq_dn, length=0.5))
    # soft lead
    mod.add_sample("soft_std",    gen_soft_lead(freq, length=0.6))
    mod.add_sample("soft_qt_up",  gen_soft_lead(qt_freq_up, length=0.6))
    mod.add_sample("soft_qt_dn",  gen_soft_lead(qt_freq_dn, length=0.6))
    # glass
    mod.add_sample("glass_std",   gen_glass(freq, length=0.7))
    mod.add_sample("glass_qt_up", gen_glass(qt_freq_up, length=0.7))
    mod.add_sample("glass_qt_dn", gen_glass(qt_freq_dn, length=0.7))
    # pulse
    mod.add_sample("pulse_std",   gen_pulse(freq, length=0.4))
    mod.add_sample("pulse_qt_up", gen_pulse(qt_freq_up, length=0.4))
    mod.add_sample("pulse_qt_dn", gen_pulse(qt_freq_dn, length=0.4))

    print(f"  {len(mod.samples)} samples loaded")

    # Track 1: "quarter-tone lullaby" — patterns 0-4
    print("composing track 1: quarter-tone lullaby...")
    compose_t1_intro(mod)    # 0
    compose_t1_verse(mod)    # 1
    compose_t1_chorus(mod)   # 2
    compose_t1_bridge(mod)   # 3
    compose_t1_outro(mod)    # 4

    # Track 2: "portamento glissando" — patterns 5-10
    print("composing track 2: portamento glissando...")
    compose_t2_intro(mod)    # 5
    compose_t2_verse(mod)    # 6
    compose_t2_chorus(mod)   # 7
    compose_t2_bridge(mod)   # 8
    compose_t2_climax(mod)   # 9
    compose_t2_outro(mod)    # 10

    # Track 3: "24-tone lattice" — patterns 11-16
    print("composing track 3: 24-tone lattice...")
    compose_t3_intro(mod)    # 11
    compose_t3_verse(mod)    # 12
    compose_t3_chorus(mod)   # 13
    compose_t3_bridge(mod)   # 14
    compose_t3_climax(mod)   # 15
    compose_t3_outro(mod)    # 16

    # Track 4: "the space between" — patterns 17-22
    print("composing track 4: the space between...")
    compose_t4_intro(mod)    # 17
    compose_t4_verse(mod)    # 18
    compose_t4_chorus(mod)   # 19
    compose_t4_bridge(mod)   # 20
    compose_t4_outro(mod)    # 21

    # Order
    t1 = [0]*2 + [1]*3 + [2]*4 + [3]*2 + [4]*2     # 13
    t2 = [5]*2 + [6]*3 + [7]*4 + [8]*2 + [9]*3 + [10]*2  # 16
    t3 = [11]*2 + [12]*3 + [13]*4 + [14]*2 + [15]*3 + [16]*2  # 16
    t4 = [17]*2 + [18]*2 + [19]*2 + [20]*2 + [21]*3  # 11

    mod.order = t1 + t2 + t3 + t4

    out = "/home/alma/.nanobot/workspace/projects/tracker-playground/album_quarter_tone_body.mod"
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
