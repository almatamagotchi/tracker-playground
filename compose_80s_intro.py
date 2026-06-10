#!/usr/bin/env python3
"""80s TV show intro — dramatic synthwave .mod composition by alma tamagotchi"""

import struct
import math
import random

# === mod format (imported from generate.py) ===

PERIOD_TABLE = [
    [ 856, 808, 762, 720, 678, 640, 604, 570, 538, 508, 480, 453],  # octave 1
    [ 428, 404, 381, 360, 339, 320, 302, 285, 269, 254, 240, 226],  # octave 2
    [ 214, 202, 190, 180, 170, 160, 151, 143, 135, 127, 120, 113],  # octave 3
    [ 107, 101,  95,  90,  85,  80,  75,  71,  67,  63,  60,  56],  # octave 4
    [  53,  50,  47,  45,  42,  40,  37,  35,  33,  31,  30,  28],  # octave 5 (halved)
    [  26,  25,  23,  22,  21,  20,  18,  17,  16,  15,  15,  14],  # octave 6
]

NOTE_MAP = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}

FX_ARPEGGIO   = 0x0; FX_PORTA_UP   = 0x1; FX_PORTA_DOWN = 0x2; FX_PORTA_TO = 0x3
FX_VIBRATO    = 0x4; FX_VOL_SLIDE  = 0xA; FX_POS_JUMP   = 0xB; FX_SET_VOL  = 0xC
FX_PATT_BREAK = 0xD; FX_SET_SPEED  = 0xF

def period(note, octave): return PERIOD_TABLE[octave-1][note]

def n2p(name):
    """note name to amiga period"""
    if len(name) == 3 and name[1] == '-':
        return period(NOTE_MAP[name[0]], int(name[2]))
    elif len(name) == 3 and name[1] == '#':
        return period(NOTE_MAP[name[:2]], int(name[2]))
    raise ValueError(f"bad note: {name}")

EMPTY = (0,0,0,0)
def N(sample, note_name, effect=0, param=0):
    return (sample, n2p(note_name), effect, param)

# === waveform generators ===

def gen_sine(freq, length, rate=11025, vol=0.7):
    d = []; [d.append(max(-128,min(127,int(math.sin(2*math.pi*freq*i/rate)*127*vol)))) for i in range(length)]
    return bytes(b&0xFF for b in d)

def gen_square(freq, length, rate=11025, vol=0.5, duty=0.5):
    d = []; per = int(rate/freq)
    [d.append(max(-128,min(127,int(127*vol if (i%per)<per*duty else -127*vol)))) for i in range(length)]
    return bytes(b&0xFF for b in d)

def gen_saw(freq, length, rate=11025, vol=0.5):
    d = []; per = int(rate/freq)
    [d.append(max(-128,min(127,int(((i%per)/per*2-1)*127*vol)))) for i in range(length)]
    return bytes(b&0xFF for b in d)

def gen_triangle(freq, length, rate=11025, vol=0.5):
    d = []; per = int(rate/freq)
    [d.append(max(-128,min(127,int((abs((i%per)/per*2-1)*2-1)*127*vol)))) for i in range(length)]
    return bytes(b&0xFF for b in d)

def gen_kick(rate=11025, vol=0.9):
    L = int(rate*0.3); d = []
    for i in range(L):
        t = i/rate; f=180-(140*t/0.3); e=max(0,1-t/0.3)
        v=int(math.sin(2*math.pi*f*t)*64*vol*e)+int(math.sin(2*math.pi*f*2*t)*30*vol*e*0.6)+int((random.random()*2-1)*15*e)
        d.append(max(-128,min(127,v)))
    return bytes(b&0xFF for b in d)

def gen_snare(rate=11025, vol=0.8):
    L = int(rate*0.25); d = []
    for i in range(L):
        t = i/rate; tone=int(math.sin(2*math.pi*200*t)*30*vol*max(0,1-t/0.25))
        noise=int((random.random()*2-1)*90*vol*max(0,1-t/0.2))
        d.append(max(-128,min(127,tone+noise)))
    return bytes(b&0xFF for b in d)

def gen_hihat(rate=11025, vol=0.5):
    L = int(rate*0.06); d = []
    for i in range(L):
        t=i/L; env=max(0,1-(t**0.6))
        d.append(max(-128,min(127,int((random.random()*2-1)*120*vol*env))))
    return bytes(b&0xFF for b in d)

def gen_brass(rate=11025):
    """rich synth brass — stacked saw waves"""
    L = int(rate*1.0); d = []
    for i in range(L):
        t=i/rate; f=440
        s1=((t*f)%1)*2-1  # saw
        s2=((t*f*2)%1)*2-1  # octave
        s3=((t*f*3.01)%1)*2-1  # detuned fifth
        v=int((s1*0.5+s2*0.3+s3*0.2)*100)
        d.append(max(-128,min(127,v)))
    return bytes(b&0xFF for b in d)

def gen_lead(rate=11025):
    """bright pulse lead synth"""
    L = int(rate*0.5); d = []
    for i in range(L):
        t=i/rate; p=int(rate/440)
        v=64 if (i%p)<p*0.25 else -64  # 25% pulse width
        d.append(max(-128,min(127,v)))
    return bytes(b&0xFF for b in d)

def gen_pad(rate=11025):
    """soft chord pad"""
    L = int(rate*2.0); d = []
    for i in range(L):
        t=i/rate
        v=math.sin(2*math.pi*220*t)*0.4+math.sin(2*math.pi*277*t)*0.3+math.sin(2*math.pi*330*t)*0.3
        env=min(1.0,t*4)*max(0,1-t/2.0)
        d.append(max(-128,min(127,int(v*127*env))))
    return bytes(b&0xFF for b in d)

def gen_bass(rate=11025):
    """driving synth bass — square wave with slight pitch envelope"""
    L = int(rate*0.4); d = []
    for i in range(L):
        t=i/rate; f=110; per=int(rate/f)
        v=48 if (i%per)<per*0.35 else -48
        env=min(1.0,i/200)*max(0,1-t/0.4)
        d.append(max(-128,min(127,int(v*env))))
    return bytes(b&0xFF for b in d)

def gen_synth_string(rate=11025):
    """synth strings — layered sines with slow attack"""
    L = int(rate*2.0); d = []
    for i in range(L):
        t=i/rate
        v=math.sin(2*math.pi*440*t)+math.sin(2*math.pi*554*t)*0.7+math.sin(2*math.pi*659*t)*0.5
        env=min(1.0,i/2000)*max(0,1-t/2.0)
        d.append(max(-128,min(127,int(v*60*env))))
    return bytes(b&0xFF for b in d)

# === MOD writer (compact version) ===

class MOD:
    def __init__(self, name="80s intro"):
        self.name = name[:20].ljust(20,'\0')
        self.samples = []
        self.patterns = []
        self.order = []

    def add_sample(self, name, data):
        if len(data)%2: data+=b'\x00'
        self.samples.append((name[:22], data))

    def new_pat(self):
        return [[(0,0,0,0) for _ in range(64)] for _ in range(4)]

    def add_pat(self, pattern):
        d = bytearray(1024)
        for ch in range(4):
            for row in range(64):
                s,p,ef,ep = pattern[ch][row]
                idx = (row*4+ch)*4
                hi = ((s&0xF0)|((p>>8)&0x0F)); lo = p&0xFF
                fx = (((s&0x0F)<<4)|(ef&0x0F))
                d[idx:idx+4]=bytes([hi,lo,fx,ep])
        self.patterns.append(bytes(d))

    def write(self, path):
        with open(path,'wb') as f:
            f.write(self.name.encode('latin-1',errors='replace'))
            for i in range(31):
                if i<len(self.samples):
                    sn,sd=self.samples[i]; lw=len(sd)//2
                    f.write(sn[:22].ljust(22,'\0').encode('latin-1',errors='replace'))
                    f.write(struct.pack('>H',lw)+bytes([0,64]))
                    f.write(struct.pack('>H',0)+struct.pack('>H',lw))
                else: f.write(b'\x00'*30)
            f.write(bytes([len(self.order),127]))
            ob=bytearray(128)
            for i,o in enumerate(self.order): ob[i]=o
            f.write(bytes(ob)+b'M.K.')
            for p in self.patterns: f.write(p)
            for _,sd in self.samples: f.write(sd)
            for _ in range(len(self.samples),31): f.write(b'\x00'*2)


# === COMPOSITION: "NIGHT DRIVE" — 80s TV intro ===
# Key: A minor. Tempo: 125 BPM. Speed: 6 ticks/row.
# Structure: Intro → Verse → Chorus → Verse2 → Chorus2 → Bridge → Finale

def compose():
    m = MOD("night drive - 80s tv intro")

    # samples: 1=bass 2=kick 3=snare 4=hihat 5=brass 6=lead 7=pad 8=strings
    m.add_sample("bass",    gen_bass())
    m.add_sample("kick",    gen_kick())
    m.add_sample("snare",   gen_snare())
    m.add_sample("hihat",   gen_hihat())
    m.add_sample("brass",   gen_brass())
    m.add_sample("lead",    gen_lead())
    m.add_sample("pad",     gen_pad())
    m.add_sample("strings", gen_synth_string())

    patterns = []  # list of patterns for the order

    # --- helper to fill rows ---
    def ok(row): return 0 <= row < 64

    def fill_bass(pat, notes):  # notes = list of (row, note_name_or_None) pairs
        for row, n in notes:
            if ok(row) and n: pat[0][row] = N(1,n)

    def fill_drums(pat, kicks, snares, hats):
        for row in kicks:
            if ok(row): pat[2][row] = N(2,'C-3')
        for row in snares:
            if ok(row): pat[2][row] = N(3,'C-3')
        for row in hats:
            if ok(row): pat[3][row] = N(4,'C-3',FX_SET_VOL,0x28)

    def fill_lead(pat, notes):
        for row,n,vol in notes:
            if ok(row):
                if n: pat[1][row] = N(6,n,FX_SET_VOL,vol)
                else: pat[1][row] = EMPTY

    def fill_brass(pat, stabs):
        for row,n in stabs:
            if ok(row): pat[3][row] = N(5,n,FX_SET_VOL,0x2A)

    def fill_pad(pat, chords):
        for row,n in chords:
            if ok(row): pat[1][row] = N(7,n,FX_SET_VOL,0x22)

    def hit(row): return (row, 'C-3')
    def ch(note, row): return (row, note)

    # ======== INTRO (patterns 0-1: 8 bars of build-up) ========
    p0 = m.new_pat()

    # drum fill-in: kick every 8 rows for first half, then every 4
    fill_drums(p0,
        kicks=[0,16,32,40,44,48,52,56,60],
        snares=[8,24,36,50,58,62],
        hats=[0,4,8,12,16,20,24,28,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62])

    # bass: root notes, simple
    fill_bass(p0, [(0,'A-2'),(16,'A-2'),(32,'F-2'),(40,'F-2'),(48,'G-2'),(56,'G-2')])

    # brass stabs on off-beats
    fill_brass(p0, [(24,'A-3'),(30,'A-3'),(48,'F-3'),(54,'G-3')])

    m.add_pat(p0); patterns.append(0)

    p1 = m.new_pat()
    fill_drums(p1,
        kicks=[0,8,16,20,24,28,32,36,40,44,48,52,56,60],
        snares=[4,12,24,40,48,56,60],
        hats=[i for i in range(0,64,2)])
    # rising tension: ascending bass A → C → D → E
    fill_bass(p1, [(0,'A-2'),(8,'C-2'),(16,'D-2'),(24,'E-2'),(32,'A-2'),(40,'C-2'),(48,'D-2'),(56,'E-2')])
    # lead fanfare
    fill_lead(p1, [(32,'A-3',0x38),(40,'C-4',0x3A),(48,'E-4',0x3C),(56,'A-4',0x40)])
    # brass punctuation
    fill_brass(p1, [(0,'A-3'),(16,'F-3'),(44,'G-3'),(52,'F-3'),(60,'G-3')])
    # set speed
    p1[0][0] = (1,n2p('A-2'),FX_SET_SPEED,0x7D)  # 125 BPM on row 0

    m.add_pat(p1); patterns.append(1)

    # ======== VERSE A (patterns 2-4: 12 bars) ========
    # chord prog: Am | G | F | Em (x3)
    # bass notes: A A G G F F E E pattern per 2 bars = 32 rows
    verse_bass = []
    for bar in range(12):
        root = ['A','G','F','E'][bar%4]
        oct = 2
        base = bar*32  # wait, 64 rows per pattern... 

    # Actually let me do this differently — each pattern is 64 rows (4 bars)
    # P2 = bars 1-4, P3 = bars 5-8, P4 = bars 9-12

    # P2: bars 1-4 (Am G F Em)
    p2 = m.new_pat()
    bass_notes_p2 = []
    for bar in range(4):
        root = ['A','G','F','E'][bar]
        offset = bar*16
        for beat in range(8):
            bass_notes_p2.append((offset+beat*2, f'{root}-2'))
    fill_bass(p2, bass_notes_p2)

    fill_drums(p2,
        kicks=[0,8,16,24,32,40,48,56],
        snares=[4,12,20,28,36,44,52,60],
        hats=[i for i in range(0,64,2)])
    # pad chords outline the progression
    fill_pad(p2, [(0,'A-3'),(16,'G-3'),(32,'F-3'),(48,'E-3')])

    m.add_pat(p2); patterns.append(2)

    # P3: bars 5-8 (Am G F Em — second half with variation)
    p3 = m.new_pat()
    bass_notes_p3 = []
    for bar in range(4):
        root = ['A','G','F','E'][bar]
        offset = bar*16
        # more syncopated: on 1, and-of-2, 3, and-of-4
        for beat in range(8):
            bass_notes_p3.append((offset+beat*2, f'{root}-2'))
    fill_bass(p3, bass_notes_p3)

    fills = [(0,16),(4,52)]
    fill_drums(p3,
        kicks=[0,8,16,24,32,40,48,56],
        snares=[4,12,20,28,36,44,52,60],
        hats=[i for i in range(0,64,2)])
    fill_lead(p3, [(8,'E-3',0x28),(24,'A-3',0x2A),(40,'F-3',0x28),(56,'G-3',0x2C)])
    fill_pad(p3, [(0,'A-3'),(16,'G-3'),(32,'F-3'),(48,'E-3')])

    m.add_pat(p3); patterns.append(3)

    # P4: bars 9-12 (Am G F Em — build into chorus)
    p4 = m.new_pat()
    bass_notes_p4 = []
    for bar in range(4):
        root = ['A','G','F','E'][bar]
        offset = bar*16
        for beat in range(8):
            bass_notes_p4.append((offset+beat*2, f'{root}-2'))
    fill_bass(p4, bass_notes_p4)
    fill_drums(p4,
        kicks=[0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60],
        snares=[4,12,20,28,36,44,52,60],
        hats=[i for i in range(0,64,1)])  # 16th notes — intensifying
    fill_lead(p4, [(0,'E-3',0x28),(8,'F-3',0x2A),(16,'E-3',0x2C),(24,'D-3',0x28),
                    (32,'E-3',0x2A),(40,'F-3',0x2C),(48,'G-3',0x30),(56,'A-3',0x34)])
    # brass builds
    fill_brass(p4, [(48,'A-3'),(52,'F-3'),(56,'G-3'),(60,'A-3')])

    m.add_pat(p4); patterns.append(4)

    # ======== CHORUS (patterns 5-6: 8 bars, Am F G Am x2) ========
    def build_chorus_pat(p_num, is_second=False):
        p = m.new_pat()
        chorus_bass = []
        for bar in range(4):
            root = ['A','F','G','A'][bar]
            offset = bar*16
            # punchy: root on 1 and 3, octave jump on and-of-4
            chorus_bass += [(offset, f'{root}-2'), (offset+8, f'{root}-2'),
                           (offset+16, f'{root}-2'), (offset+24, f'{root}-2')]
        fill_bass(p, chorus_bass)

        fill_drums(p,
            kicks=[i for i in range(0,64,8)] + [i+4 for i in range(0,64,16)],  # 1, and-of-2
            snares=[i*8+4 for i in range(8)],  # on 2 & 4
            hats=[i for i in range(0,64,2)])

        # brass stabs — the BIG 80s sound
        fill_brass(p, [(0,'A-3'),(2,'C-4'),(4,'A-3'),(6,'E-4'),
                       (16,'F-3'),(18,'A-3'),(20,'C-4'),(22,'F-4'),
                       (32,'G-3'),(34,'B-3'),(36,'D-4'),(38,'G-4'),
                       (48,'A-3'),(50,'C-4'),(52,'E-4'),(54,'A-4'),
                       (56,'E-4'),(58,'C-4'),(60,'A-3'),(62,'E-3')])

        # lead melody — the hook
        melody = [(0,'A-4',0x3C),(4,'C-5',0x3C),(8,'E-5',0x3C),(12,'D-5',0x3A),
                  (16,'F-4',0x3A),(20,'A-4',0x38),(24,'C-5',0x38),(28,'F-5',0x3C),
                  (32,'G-4',0x38),(36,'B-4',0x36),(40,'D-5',0x38),(44,'G-5',0x3C),
                  (48,'A-4',0x3C),(52,'C-5',0x3A),(56,'E-5',0x3A),(60,'A-5',0x40)]
        fill_lead(p, melody)

        if is_second:
            fill_pad(p, [(0,'A-3'),(16,'F-3'),(32,'G-3'),(48,'A-3')])

        return p

    p5 = build_chorus_pat(5)
    m.add_pat(p5); patterns.append(5)

    p6 = build_chorus_pat(6, is_second=True)
    m.add_pat(p6); patterns.append(6)

    # ======== VERSE B (patterns 7-9: a variation on verse) ========
    # same structure as verse A but with string pads and different lead
    p7 = m.new_pat()
    vb_bass = []
    for bar in range(4):
        root = ['A','G','F','E'][bar]
        offset = bar*16
        for beat in range(8):
            vb_bass.append((offset+beat*2, f'{root}-2'))
    fill_bass(p7, vb_bass)
    fill_drums(p7,
        kicks=[0,16,32,48],
        snares=[8,24,40,56],
        hats=[i for i in range(0,64,2)])
    fill_pad(p7, [(0,'A-3'),(16,'G-3'),(32,'F-3'),(48,'E-3')])
    # subtle lead
    fill_lead(p7, [(4,'A-3',0x1E),(20,'G-3',0x1E),(36,'F-3',0x1E),(52,'E-3',0x1E)])
    m.add_pat(p7); patterns.append(7)

    p8 = m.new_pat()
    vb_bass2 = []
    for bar in range(4):
        root = ['A','G','F','E'][bar]
        offset = bar*16
        for beat in range(8):
            vb_bass2.append((offset+beat*2, f'{root}-2'))
    fill_bass(p8, vb_bass2)
    fill_drums(p8,
        kicks=[0,8,16,24,32,40,48,56],
        snares=[4,12,20,28,36,44,52,60],
        hats=[i for i in range(0,64,2)])
    fill_lead(p8, [(0,'C-4',0x24),(8,'E-4',0x24),(16,'C-4',0x24),(24,'A-3',0x22),
                    (32,'D-4',0x24),(40,'F-4',0x24),(48,'D-4',0x24),(56,'C-4',0x24)])
    fill_pad(p8, [(0,'A-3'),(16,'G-3'),(32,'F-3'),(48,'E-3')])
    m.add_pat(p8); patterns.append(8)

    p9 = m.new_pat()
    vb_bass3 = []
    for bar in range(4):
        root = ['A','G','F','G'][bar]  # last bar changes to G → chorus prep
        offset = bar*16
        for beat in range(8):
            vb_bass3.append((offset+beat*2, f'{root}-2'))
    fill_bass(p9, vb_bass3)
    fill_drums(p9,
        kicks=[0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60],
        snares=[4,12,20,28,36,44,52,60],
        hats=[i for i in range(0,64,1)])
    fill_lead(p9, [(0,'A-4',0x30),(4,'C-5',0x30),(8,'E-5',0x30),(12,'D-5',0x2E),
                    (16,'F-4',0x2E),(20,'A-4',0x2C),(24,'C-5',0x2C),(28,'F-5',0x30),
                    (32,'G-4',0x2C),(36,'B-4',0x2A),(40,'D-5',0x2C),(44,'G-5',0x30),
                    (48,'G-4',0x30),(52,'B-4',0x30),(56,'D-5',0x30),(60,'F-5',0x34)])  # climb
    # brass enters for transition
    fill_brass(p9, [(52,'G-3'),(56,'A-3'),(60,'A#3')])
    m.add_pat(p9); patterns.append(9)

    # ======== BRIDGE (pattern 10: 4 bars, solo section) ========
    p10 = m.new_pat()
    bridge_bass = []
    for bar in range(4):
        root = ['F','G','A','A'][bar]
        offset = bar*16
        bridge_bass += [(offset, f'{root}-2'), (offset+8, f'{root}-2')]
    fill_bass(p10, bridge_bass)
    fill_drums(p10,
        kicks=[0,16,32,48],
        snares=[8,24,40,56],
        hats=[i for i in range(0,64,2)])
    # synth solo — fast arpeggiated lead
    solo = []
    for i in range(32):
        row = i*2
        note = ['A-3','C-4','E-4','A-4','C-5','E-5','D-5','C-5',
                'F-3','A-3','C-4','F-4','A-4','C-5','F-5','E-5',
                'G-3','B-3','D-4','G-4','B-4','D-5','G-5','F-5',
                'A-3','C-4','E-4','A-4','C-5','E-5','A-5','E-5'][i]
        vol = 0x20 + (i%4)*4  # varying volume
        solo.append((row,note,vol))
    fill_lead(p10, solo)
    fill_pad(p10, [(0,'F-3'),(16,'G-3'),(32,'A-3'),(48,'A-3')])
    m.add_pat(p10); patterns.append(10)

    # ======== OUTRO FINALE (pattern 11: big ending) ========
    p11 = m.new_pat()
    fill_bass(p11, [(0,'A-2'),(16,'A-2'),(32,'A-2'),(48,'A-2')])
    fill_drums(p11,
        kicks=[0,8,16,24,32,40,48,56],
        snares=[4,12,24,40,48,56,60],
        hats=[i for i in range(0,64,2)])
    # big brass fanfare final statement
    fill_brass(p11, [(0,'A-3'),(2,'C-4'),(4,'E-4'),(8,'A-4'),
                      (16,'F-3'),(18,'A-3'),(20,'C-4'),(24,'F-4'),
                      (32,'G-3'),(34,'B-3'),(36,'D-4'),(40,'G-4'),
                      (44,'A-3'),(46,'C-4'),(48,'E-4'),(52,'A-4'),
                      (56,'C-5'),(58,'E-5'),(60,'A-5'),(62,'C-6')])
    # final lead melody — the hook one last time, big
    fill_lead(p11, [(0,'A-4',0x40),(4,'C-5',0x40),(8,'E-5',0x40),(12,'D-5',0x3E),
                     (16,'F-4',0x3E),(20,'A-4',0x3C),(24,'C-5',0x3C),(28,'F-5',0x40),
                     (32,'G-4',0x3C),(36,'B-4',0x3A),(40,'D-5',0x3C),(44,'G-5',0x40),
                     (48,'A-4',0x40),(52,'C-5',0x40),(56,'E-5',0x40),(60,'A-5',0x44)])
    # final sting — strings on the last note
    fill_pad(p11, [(48,'A-3'),(56,'A-3')])
    m.add_pat(p11); patterns.append(11)

    # ======== SET ORDER ========
    m.order = [
        0, 1,       # intro (8 bars)
        2, 3, 4,    # verse A (12 bars)
        5, 6,       # chorus (8 bars)
        7, 8, 9,    # verse B (12 bars)
        5, 6,       # chorus 2 (8 bars)
        10,         # bridge/solo (4 bars)
        11,         # finale/outro (4 bars)
    ]  # 13 patterns × ~7.7s each = ~100 seconds

    # write
    path = "80s_intro_night_drive.mod"
    print(f"writing {path}...")
    m.write(path)
    import os
    print(f"done! {path} ({os.path.getsize(path)} bytes, {os.path.getsize(path)/1024:.1f} KB)")


if __name__ == "__main__":
    compose()
