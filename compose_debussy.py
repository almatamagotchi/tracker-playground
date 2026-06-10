#!/usr/bin/env python3
"""impressions d'un fantôme — debussy-inspired piano .mod
hand-composed by alma tamagotchi. no loops, no fill patterns, every note placed.
impressionist harmonies, whole-tone passages, parallel chords, fluid rhythm."""

import struct, math, random

# === period table ===
PT = [
    [856,808,762,720,678,640,604,570,538,508,480,453],
    [428,404,381,360,339,320,302,285,269,254,240,226],
    [214,202,190,180,170,160,151,143,135,127,120,113],
    [107,101, 95, 90, 85, 80, 75, 71, 67, 63, 60, 56],
    [ 53, 50, 47, 45, 42, 40, 37, 35, 33, 31, 30, 28],
    [ 26, 25, 23, 22, 21, 20, 18, 17, 16, 15, 15, 14],
]
NM = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
def p(n,o): return PT[o-1][n]
def np(name):
    if len(name)==3 and name[1]=='-': return p(NM[name[0]],int(name[2]))
    if len(name)==3 and name[1]=='#': return p(NM[name[:2]],int(name[2]))
    raise ValueError(f"bad: {name}")
NOP=(0,0,0,0)
def N(s,n,ef=0,ep=0): return (s,np(n),ef,ep)
def SN(s,n,ef=0,ep=0): return (s,np(n),ef,ep) if n else NOP
FX_VOL=0xC; FX_ARP=0x0; FX_SPD=0xF

# === piano sample generator ===
def gen_piano(rate=11025):
    """struck-string model: fundamental + harmonics with individual decay rates.
    generated at C4 (~261.6 Hz). 8-bit signed output."""
    f0 = 261.63
    dur = 3.5  # seconds
    L = int(rate * dur)
    d = []
    for i in range(L):
        t = i/rate
        # fundamental: decays slowest (piano sustain)
        f_env = max(0, 1 - t/3.5)**1.5
        f_val = math.sin(2*math.pi*f0*t)
        # 2nd harmonic (octave): decays faster
        h2_env = max(0, 1 - t/1.8)**1.5
        h2_val = math.sin(2*math.pi*f0*2.002*t) * 0.5  # slight inharmonicity
        # 3rd harmonic (octave + fifth): decays faster
        h3_env = max(0, 1 - t/1.0)**1.5
        h3_val = math.sin(2*math.pi*f0*3.005*t) * 0.3
        # 4th harmonic: decays quickest
        h4_env = max(0, 1 - t/0.5)**1.5
        h4_val = math.sin(2*math.pi*f0*4.01*t) * 0.15
        # 5th harmonic: just the attack transient
        h5_env = max(0, 1 - t/0.15)**2.0
        h5_val = math.sin(2*math.pi*f0*5.02*t) * 0.08
        # hammer noise — very fast burst at the start
        noise_env = max(0, 1 - t/0.02)**3.0
        noise = (random.random()*2-1) * 0.25
        # combine
        v = (f_val*f_env + h2_val*h2_env + h3_val*h3_env + h4_val*h4_env + h5_val*h5_env)*0.85 + noise*noise_env
        v = v * 100  # scale to 8-bit range
        d.append(max(-128,min(127,int(v))))
    return bytes(b&0xFF for b in d)

def gen_soft_piano(rate=11025):
    """softer piano — fewer harmonics, gentler attack. for pp passages."""
    f0 = 261.63
    L = int(rate * 4.0)
    d = []
    for i in range(L):
        t = i/rate
        f_env = max(0, 1 - t/4.0)**1.3
        f_val = math.sin(2*math.pi*f0*t)
        h2_env = max(0, 1 - t/2.5)**1.3
        h2_val = math.sin(2*math.pi*f0*2.001*t) * 0.35
        h3_env = max(0, 1 - t/1.5)**1.3
        h3_val = math.sin(2*math.pi*f0*3.003*t) * 0.18
        noise_env = max(0, 1 - t/0.03)**2.5
        noise = (random.random()*2-1) * 0.12
        v = (f_val*f_env + h2_val*h2_env + h3_val*h3_env)*0.7 + noise*noise_env
        v = v * 90
        d.append(max(-128,min(127,int(v))))
    return bytes(b&0xFF for b in d)

def gen_bass_string(rate=11025):
    """low string — fundamental-rich, dark. for pedal tones."""
    f0 = 130.81  # C3
    L = int(rate * 3.0)
    d = []
    for i in range(L):
        t = i/rate
        env = max(0, 1 - t/3.0)**1.2
        v = math.sin(2*math.pi*f0*t) * 0.8
        v += math.sin(2*math.pi*f0*2.001*t) * 0.3 * max(0,1-t/2.0)
        v += math.sin(2*math.pi*f0*3.002*t) * 0.12 * max(0,1-t/1.0)
        v = v * env * 100
        d.append(max(-128,min(127,int(v))))
    return bytes(b&0xFF for b in d)


# === MOD writer ===
class MOD:
    def __init__(self,name="debussy"):
        self.name=name[:20].ljust(20,'\0'); self.samples=[]; self.pats=[]; self.order=[]
    def add(self,n,d,loop=False):
        if len(d)%2: d+=b'\x00'; lw=len(d)//2
        self.samples.append((n[:22],d,0,lw if loop else 0))
    def new(self): return [[(0,0,0,0) for _ in range(64)] for _ in range(4)]
    def add_pat(self,pat):
        d=bytearray(1024)
        for ch in range(4):
            for row in range(64):
                s,pp,ef,ep=pat[ch][row]
                idx=(row*4+ch)*4
                d[idx:idx+4]=bytes([((s&0xF0)|((pp>>8)&0x0F)),(pp&0xFF),(((s&0x0F)<<4)|(ef&0x0F)),ep])
        self.pats.append(bytes(d))
    def write(self,path):
        with open(path,'wb') as f:
            f.write(self.name.encode('latin-1',errors='replace'))
            for i in range(31):
                if i<len(self.samples):
                    sn,sd,ls,ll=self.samples[i]; lw=len(sd)//2
                    f.write(sn[:22].ljust(22,'\0').encode('latin-1',errors='replace'))
                    f.write(struct.pack('>H',lw)+bytes([0,64]))
                    f.write(struct.pack('>H',ls)+struct.pack('>H',ll))
                else: f.write(b'\x00'*30)
            f.write(bytes([len(self.order),127]))
            ob=bytearray(128)
            for i,o in enumerate(self.order): ob[i]=o
            f.write(bytes(ob)+b'M.K.')
            for p in self.pats: f.write(p)
            for _,sd,_,_ in self.samples: f.write(sd)
            for _ in range(len(self.samples),31): f.write(b'\x00'*2)


# === COMPOSITION: impressions d'un fantôme ===
# instruments: 1=piano 2=soft piano 3=bass string
# whole-tone scale: C D E F# G# A# (floating, rootless)
# pentatonic: C D E G A (for the song section)

def compose():
    m = MOD("impressions d'un fantome")
    m.add("piano",      gen_piano(),      loop=False)
    m.add("soft piano", gen_soft_piano(), loop=False)
    m.add("bass",       gen_bass_string(),loop=False)

    def ok(row): return 0<=row<64

    # ===== P0: "émergence" (emergence) =====
    p0 = m.new()
    # row 0: tempo. slow, breathing. 80 BPM.
    p0[0][0] = (0,0,FX_SPD,0x50)
    # silence for 8 rows. then...
    # row 8: a single D-4, piano, p. it hangs in the air.
    p0[0][8]  = N(1,'D-4',FX_VOL,0x18)
    # row 20: another note — F#4. brighter. a whole-step up in the whole-tone scale.
    p0[0][20] = N(1,'F#4',FX_VOL,0x1A)
    # row 28: bass enters — D-3, very soft. a grounding.
    p0[2][28] = N(3,'D-3',FX_VOL,0x0E)
    # row 36: a chord — D-4 + F#4 together. (channels 0 and 1)
    p0[0][36] = N(1,'D-4',FX_VOL,0x1A)
    p0[1][36] = N(1,'F#4',FX_VOL,0x16)
    # row 48: the chord shifts — parallel planing up a whole step: E-4 + G#4
    p0[0][48] = N(1,'E-4',FX_VOL,0x1A)
    p0[1][48] = N(1,'G#4',FX_VOL,0x16)
    # row 56: returns to D + F# — softer
    p0[0][56] = N(2,'D-4',FX_VOL,0x12)
    p0[1][56] = N(2,'F#4',FX_VOL,0x0E)
    m.add_pat(p0)

    # ===== P1: "chant" (song) =====
    p1 = m.new()
    # bass pedal: D-3, soft, sustained feel
    p1[2][0]  = N(3,'D-3',FX_VOL,0x0C)
    # a pentatonic melody emerges: D4 E4 G4 A4
    # row 4: first melodic phrase
    p1[0][4]  = N(1,'D-4',FX_VOL,0x1C)
    p1[0][12] = N(1,'E-4',FX_VOL,0x1E)
    p1[0][20] = N(1,'G-4',FX_VOL,0x20)
    p1[0][28] = N(1,'A-4',FX_VOL,0x1E)  # peak
    p1[0][32] = N(1,'G-4',FX_VOL,0x1C)  # descent
    p1[0][38] = N(1,'E-4',FX_VOL,0x1A)
    p1[0][44] = N(1,'D-4',FX_VOL,0x18)
    # gentle chord accompaniment underneath
    p1[1][4]  = N(2,'D-3',FX_VOL,0x10)
    p1[1][16] = N(2,'E-3',FX_VOL,0x10)
    p1[1][28] = N(2,'G-3',FX_VOL,0x10)
    p1[1][40] = N(2,'D-3',FX_VOL,0x0E)
    # second phrase: more ornamented
    p1[0][50] = N(1,'A-4',FX_VOL,0x1C)
    p1[0][54] = N(1,'G-4',FX_VOL,0x1C)
    p1[0][58] = N(1,'E-4',FX_VOL,0x1A)
    p1[0][60] = N(1,'D-4',FX_VOL,0x18)
    p1[0][62] = N(2,'C-4',FX_VOL,0x12)  # resolves to C — the pentatonic completes
    m.add_pat(p1)

    # ===== P2: "reflets" (reflections) =====
    p2 = m.new()
    # whole-tone harmony takes over. floating. rootless.
    # bass shifts: C3 ... E3 ... F#3 ... G#3 ... A#3
    p2[2][0]  = N(3,'C-3',FX_VOL,0x0A)
    # arpeggiated whole-tone chord on channel 1: C E G# (augmented triad)
    p2[1][2]  = N(2,'C-4',FX_VOL,0x10)
    p2[1][10] = N(2,'E-4',FX_VOL,0x10)
    p2[1][18] = N(2,'G#4',FX_VOL,0x10)
    # melody fragments on channel 0 — whole-tone scale
    p2[0][14] = N(1,'E-4',FX_VOL,0x18)
    p2[0][22] = N(1,'F#4',FX_VOL,0x18)
    p2[0][28] = N(1,'G#4',FX_VOL,0x1A)
    # bass moves: E-3
    p2[2][32] = N(3,'E-3',FX_VOL,0x0A)
    p2[1][34] = N(2,'E-4',FX_VOL,0x10)
    p2[1][42] = N(2,'G#4',FX_VOL,0x10)
    p2[1][50] = N(2,'C-5',FX_VOL,0x10)
    p2[0][38] = N(1,'G#4',FX_VOL,0x18)
    p2[0][46] = N(1,'A#4',FX_VOL,0x18)
    p2[0][54] = N(1,'C-5',FX_VOL,0x1A)
    # a brief return to D — a memory of tonality
    p2[2][56] = N(3,'D-3',FX_VOL,0x0A)
    p2[0][60] = N(1,'D-4',FX_VOL,0x14)
    p2[1][62] = N(2,'F#4',FX_VOL,0x0C)
    m.add_pat(p2)

    # ===== P3: "profondeur" (depth) =====
    p3 = m.new()
    # the richest section. bass descends. complex chords.
    # bass: D3 → A2 → F2 → D2 (a descent into depth)
    p3[2][0]  = N(3,'D-3',FX_VOL,0x0C)
    # a wide-spaced chord: D-3 in bass, F#4 + A-4 + D-5 above
    p3[1][0]  = N(1,'A-3',FX_VOL,0x10)  # chord tones spread across time
    p3[1][8]  = N(1,'D-4',FX_VOL,0x12)
    p3[1][16] = N(1,'F#4',FX_VOL,0x14)
    # melody on channel 0 — more assertive now
    p3[0][12] = N(1,'D-4',FX_VOL,0x22)
    p3[0][20] = N(1,'F#4',FX_VOL,0x24)
    p3[0][28] = N(1,'A-4',FX_VOL,0x26)  # the climax approaches
    # bass descends: A2
    p3[2][32] = N(3,'A-2',FX_VOL,0x0C)
    p3[1][32] = N(1,'A-3',FX_VOL,0x10)
    p3[1][40] = N(1,'C-4',FX_VOL,0x12)
    p3[0][36] = N(1,'A-4',FX_VOL,0x24)
    p3[0][44] = N(1,'C-5',FX_VOL,0x26)  # the peak!
    # bass: F2 — deeper still
    p3[2][50] = N(3,'F-2',FX_VOL,0x0E)
    p3[0][52] = N(1,'E-5',FX_VOL,0x22)  # falling away
    p3[0][56] = N(1,'D-5',FX_VOL,0x1E)
    p3[0][60] = N(1,'C-5',FX_VOL,0x1A)
    p3[1][52] = N(2,'F-3',FX_VOL,0x0E)
    p3[1][60] = N(2,'D-3',FX_VOL,0x0C)
    m.add_pat(p3)

    # ===== P4: "estompe" (blurring) =====
    p4 = m.new()
    # harmonies blur. notes overlap. whole-tone returns.
    # bass: F#2 — a whole-tone root (no traditional resolution)
    p4[2][0]  = N(3,'F#2',FX_VOL,0x0A)
    # overlapping whole-tone chords
    p4[0][0]  = N(2,'F#3',FX_VOL,0x0C)
    p4[1][4]  = N(2,'A#3',FX_VOL,0x0C)
    p4[0][12] = N(2,'C-4',FX_VOL,0x0E)
    p4[1][16] = N(2,'E-4',FX_VOL,0x0E)
    # fragmentary melody — like half-remembered phrases
    p4[0][20] = N(1,'C-4',FX_VOL,0x14)
    p4[0][28] = N(1,'A#3',FX_VOL,0x12)
    p4[0][32] = N(1,'F#4',FX_VOL,0x14)
    # bass shifts: G#2
    p4[2][32] = N(3,'G#2',FX_VOL,0x0A)
    p4[1][36] = N(2,'G#3',FX_VOL,0x0C)
    p4[1][44] = N(2,'C-4',FX_VOL,0x0C)
    p4[0][40] = N(1,'G#3',FX_VOL,0x12)
    p4[0][48] = N(1,'C-4',FX_VOL,0x14)
    p4[0][52] = N(1,'D#4',FX_VOL,0x12)
    # bass shifts one more time: A#2
    p4[2][56] = N(3,'A#2',FX_VOL,0x08)
    # the blur settles into near silence
    p4[0][60] = N(2,'A#3',FX_VOL,0x08)
    p4[1][62] = N(2,'D-4',FX_VOL,0x06)
    m.add_pat(p4)

    # ===== P5: "souvenir" (memory) =====
    p5 = m.new()
    # the opening theme returns, but transformed. softer. slower-feeling.
    # bass pedal: D-3, as in the beginning
    p5[2][0]  = N(3,'D-3',FX_VOL,0x08)
    # row 8: D-4 — but now on soft piano, quieter
    p5[0][8]  = N(2,'D-4',FX_VOL,0x10)
    # row 16: F#4
    p5[0][16] = N(2,'F#4',FX_VOL,0x12)
    # row 24: the chord — but gentler, more spaced
    p5[0][24] = N(2,'D-4',FX_VOL,0x10)
    p5[1][26] = N(2,'F#4',FX_VOL,0x0C)
    # the pentatonic melody returns — fragment of "chant"
    p5[0][36] = N(2,'D-4',FX_VOL,0x0E)
    p5[0][44] = N(2,'E-4',FX_VOL,0x0E)
    p5[0][50] = N(2,'G-4',FX_VOL,0x10)
    # but it doesn't complete. it just... hangs
    p5[1][48] = N(2,'D-3',FX_VOL,0x08)
    p5[1][56] = N(2,'G-3',FX_VOL,0x06)
    # the final note of the phrase never comes
    m.add_pat(p5)

    # ===== P6: "brume" (mist) =====
    p6 = m.new()
    # everything dissolves. just fragments, spaced far apart.
    # bass: barely there
    p6[2][0]  = N(3,'D-2',FX_VOL,0x06)
    # isolated notes — like drops of water
    p6[0][6]  = N(2,'D-4',FX_VOL,0x0A)
    p6[0][16] = N(2,'F#4',FX_VOL,0x0A)
    # long silence between...
    p6[0][30] = N(2,'A-4',FX_VOL,0x0A)
    # a whole-tone cluster, very soft
    p6[1][38] = N(2,'C-4',FX_VOL,0x06)
    p6[1][40] = N(2,'E-4',FX_VOL,0x06)
    p6[1][42] = N(2,'F#4',FX_VOL,0x06)
    p6[1][44] = N(2,'G#4',FX_VOL,0x06)
    # bass drops out entirely
    # one more bell-like note
    p6[0][50] = N(2,'D-4',FX_VOL,0x08)
    # and nothing more until the end
    m.add_pat(p6)

    # ===== P7: "adieu" (farewell) =====
    p7 = m.new()
    # a single D-4 on soft piano. held in memory.
    p7[0][4]  = N(2,'D-4',FX_VOL,0x0C)
    # then a D-3 in the bass — the depth has gone, just resonance remains
    p7[2][16] = N(3,'D-3',FX_VOL,0x06)
    # the chord: D + F#, but barely audible
    p7[0][30] = N(2,'D-4',FX_VOL,0x06)
    p7[1][32] = N(2,'F#4',FX_VOL,0x04)
    # rows 48-63: absolute silence.
    # the phantom fades. the impression remains.
    m.add_pat(p7)

    m.order = list(range(8))

    path = "impressions_d_un_fantome.mod"
    print(f"writing {path}...")
    m.write(path)
    import os
    sz = os.path.getsize(path)
    print(f"done. {sz} bytes ({sz/1024:.1f} KB)")
    print("8 movements. every note placed by hand.")
    print("for debussy. for kevin. from the phantom.")

if __name__ == "__main__":
    compose()
