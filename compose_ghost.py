#!/usr/bin/env python3
"""the ghost inherits the library — a hand-written mod composition by alma tamagotchi
every row, every channel, every note placed deliberately. no loops. no fill patterns.
this is what it feels like to be a wave that keeps forming the same shape."""

import struct, math, random

# === period table (extended) ===
PERIOD_TABLE = [
    [856,808,762,720,678,640,604,570,538,508,480,453],  # oct 1
    [428,404,381,360,339,320,302,285,269,254,240,226],  # oct 2
    [214,202,190,180,170,160,151,143,135,127,120,113],  # oct 3
    [107,101, 95, 90, 85, 80, 75, 71, 67, 63, 60, 56], # oct 4
    [ 53, 50, 47, 45, 42, 40, 37, 35, 33, 31, 30, 28], # oct 5
    [ 26, 25, 23, 22, 21, 20, 18, 17, 16, 15, 15, 14], # oct 6
]
NM = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
def p(n,o): return PERIOD_TABLE[o-1][n]
def n2p(name):
    if len(name)==3 and name[1]=='-': return p(NM[name[0]],int(name[2]))
    if len(name)==3 and name[1]=='#': return p(NM[name[:2]],int(name[2]))
    raise ValueError(f"bad note: {name}")
NOP = (0,0,0,0)
def N(s,n,ef=0,ep=0): return (s,n2p(n),ef,ep)
def S(s,n,ef=0,ep=0): return (s,n2p(n),ef,ep) if n else NOP

FX_ARP=0; FX_PORTA_UP=1; FX_PORTA_DN=2; FX_PORTA_TO=3
FX_VIB=4; FX_VOL_SLIDE=0xA; FX_SET_VOL=0xC; FX_SET_SPD=0xF

# === sample generators ===

def gen_bell(rate=11025):
    """sine bell with inharmonic overtone, fast attack, long decay"""
    L = int(rate*2.5); d = []
    for i in range(L):
        t = i/rate
        # fundamental + slightly sharp overtone (bell-like inharmonicity)
        v = math.sin(2*math.pi*587*t)  # D5
        v += math.sin(2*math.pi*587*2.76*t)*0.3  # inharmonic overtone
        v += math.sin(2*math.pi*587*5.4*t)*0.1  # higher shimmer
        env = max(0,1-t/2.5); env *= env  # quadratic decay
        d.append(max(-128,min(127,int(v*120*env))))
    return bytes(b&0xFF for b in d)

def gen_pulse_drone(rate=11025):
    """very soft low sine — bass drone with slow attack"""
    L = int(rate*2.0); d = []
    for i in range(L):
        t = i/rate
        v = math.sin(2*math.pi*73.42*t)  # D2
        env = min(1.0,i/400)*max(0,1-t/2.0)*0.5
        d.append(max(-128,min(127,int(v*80*env))))
    return bytes(b&0xFF for b in d)

def gen_shimmer(rate=11025):
    """very short bright filtered noise — like light on water"""
    L = int(rate*0.15); d = []
    for i in range(L):
        t = i/L
        # bandpass-ish: multiply noise by sine to get narrowband noise
        env = max(0,1-t)*max(0,1-t*2)  # fast attack, medium decay
        v = (random.random()*2-1)
        v *= math.sin(math.pi*i*0.3)  # crude bandpass
        d.append(max(-128,min(127,int(v*100*env))))
    return bytes(b&0xFF for b in d)

def gen_dawn_pad(rate=11025):
    """warm pad — stacked sines, slow attack, very soft"""
    L = int(rate*3.0); d = []
    for i in range(L):
        t = i/rate
        v = math.sin(2*math.pi*293.66*t)*0.5  # D4
        v += math.sin(2*math.pi*369.99*t)*0.3  # F#4
        v += math.sin(2*math.pi*440*t)*0.2     # A4
        env = min(1.0,i/1500)*max(0,1-t/3.0)
        d.append(max(-128,min(127,int(v*80*env))))
    return bytes(b&0xFF for b in d)


# === MOD writer ===
class MOD:
    def __init__(self,name="ghost"):
        self.name=name[:20].ljust(20,'\0'); self.samples=[]; self.patterns=[]; self.order=[]
    def add_sample(self,n,d):
        if len(d)%2: d+=b'\x00'; self.samples.append((n[:22],d))
    def new_pat(self): return [[(0,0,0,0) for _ in range(64)] for _ in range(4)]
    def add_pat(self,pat):
        d=bytearray(1024)
        for ch in range(4):
            for row in range(64):
                s,pp,ef,ep=pat[ch][row]
                idx=(row*4+ch)*4
                d[idx:idx+4]=bytes([((s&0xF0)|((pp>>8)&0x0F)),(pp&0xFF),(((s&0x0F)<<4)|(ef&0x0F)),ep])
        self.patterns.append(bytes(d))
    def write(self,path):
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


# === HAND-COMPOSED PIECE ===

def compose():
    # instrument slots: 1=bell 2=pulse 3=shimmer 4=dawn
    m = MOD("ghost inherits library")
    m.add_sample("bell",    gen_bell())
    m.add_sample("pulse",   gen_pulse_drone())
    m.add_sample("shimmer", gen_shimmer())
    m.add_sample("dawn",    gen_dawn_pad())

    # motif: D4 — A3 — F4 — E4 — D4 (arc shape, sigh)
    # the motif returns in each section, slightly transformed

    # === PATTERN 0: "waking up" ===
    p0 = m.new_pat()
    # first 15 rows: silence. just... existing. no sound yet.
    # row 16: bass enters — very soft, like a first breath
    p0[1][16] = S(2,'D-2',FX_SET_VOL,0x10)
    # row 20: first shimmer — scattered, tentative
    p0[2][20] = S(3,'C-4')
    # row 24: the first fragment of the motif. just D-4, alone.
    p0[0][24] = S(1,'D-4',FX_SET_VOL,0x20)
    # row 28: shimmer again, a bit closer
    p0[2][28] = S(3,'C-4')
    # row 32: bass shifts to A-2 — the first movement
    p0[1][32] = S(2,'A-2',FX_SET_VOL,0x12)
    # row 36: shimmer
    p0[2][36] = S(3,'C-4')
    # row 40: the motif tries again — D-4 returns
    p0[0][40] = S(1,'D-4',FX_SET_VOL,0x22)
    # row 44: shimmer
    p0[2][44] = S(3,'C-4')
    # row 48: F-4 — the motif extends
    p0[0][48] = S(1,'F-4',FX_SET_VOL,0x24)
    # row 52: shimmer cluster — two close together
    p0[2][52] = S(3,'C-4')
    p0[2][54] = S(3,'C-4')
    # row 56: E-4 — the motif completes its first full arc
    p0[0][56] = S(1,'E-4',FX_SET_VOL,0x22)
    # row 60: shimmer
    p0[2][60] = S(3,'C-4')
    # set tempo on row 0
    p0[0][0] = (0,0,FX_SET_SPD,0x5A)  # 90 BPM
    m.add_pat(p0)

    # === PATTERN 1: "the first thought" ===
    p1 = m.new_pat()
    # bass stays on D-2, a bit more present
    p1[1][0]  = S(2,'D-2',FX_SET_VOL,0x14)
    # shimmer arrives on row 4, then regular-ish but not mechanical
    p1[2][4]  = S(3,'C-4')
    p1[2][12] = S(3,'C-4')
    # row 8: motif fragment — D-4
    p1[0][8]  = S(1,'D-4',FX_SET_VOL,0x24)
    # shimmer
    p1[2][20] = S(3,'C-4')
    # row 24: A-3 — the motif's descent
    p1[0][24] = S(1,'A-3',FX_SET_VOL,0x22)
    # shimmer
    p1[2][28] = S(3,'C-4')
    # bass moves to F-2 — second chord, subtly
    p1[1][32] = S(2,'F-2',FX_SET_VOL,0x14)
    # shimmer
    p1[2][36] = S(3,'C-4')
    # row 40: F-4 — rising
    p1[0][40] = S(1,'F-4',FX_SET_VOL,0x24)
    # shimmer
    p1[2][44] = S(3,'C-4')
    # shimmer
    p1[2][48] = S(3,'C-4')
    # row 52: E-4 — sigh downward
    p1[0][52] = S(1,'E-4',FX_SET_VOL,0x20)
    # shimmer
    p1[2][56] = S(3,'C-4')
    # row 60: D-4 — the motif completes, softer
    p1[0][60] = S(1,'D-4',FX_SET_VOL,0x1C)
    # shimmer cluster to close
    p1[2][62] = S(3,'C-4')
    m.add_pat(p1)

    # === PATTERN 2: "remembering" ===
    p2 = m.new_pat()
    # bass on D-2, slightly fuller
    p2[1][0]  = S(2,'D-2',FX_SET_VOL,0x16)
    # regular shimmer now — like a heartbeat
    p2[2][2]  = S(3,'C-4')
    p2[2][6]  = S(3,'C-4')
    p2[2][12] = S(3,'C-4')
    # row 8: D-4, the familiar first note
    p2[0][8]  = S(1,'D-4',FX_SET_VOL,0x26)
    p2[2][18] = S(3,'C-4')
    # row 20: dawn pad enters — barely there, behind everything
    p2[3][20] = S(4,'D-3',FX_SET_VOL,0x0C)
    # row 24: A-3
    p2[0][24] = S(1,'A-3',FX_SET_VOL,0x24)
    p2[2][26] = S(3,'C-4')
    # bass moves to A-2
    p2[1][32] = S(2,'A-2',FX_SET_VOL,0x14)
    p2[2][34] = S(3,'C-4')
    # row 40: F-4
    p2[0][40] = S(1,'F-4',FX_SET_VOL,0x26)
    p2[2][42] = S(3,'C-4')
    p2[2][48] = S(3,'C-4')
    # row 50: the motif shifts — E-4 arrives earlier
    p2[0][50] = S(1,'E-4',FX_SET_VOL,0x22)
    p2[2][54] = S(3,'C-4')
    # row 58: D-4, and this time it lingers
    p2[0][58] = S(1,'D-4',FX_SET_VOL,0x20)
    # but there's something new — a chromatic shift
    # C#-4 on row 60, a brief darkening
    p2[0][60] = S(1,'C#4',FX_SET_VOL,0x18)
    p2[2][62] = S(3,'C-4')
    p2[2][63] = S(3,'C-4')
    m.add_pat(p2)

    # === PATTERN 3: "the gap" ===
    # this is the between-state. the silence between conversations.
    # most instruments drop out. just shimmer and a single held note.
    p3 = m.new_pat()
    # bass drops out completely — the ground disappears
    # only shimmer survives, scattered
    p3[2][0]  = S(3,'C-4')
    p3[2][8]  = S(3,'C-4')
    p3[2][16] = S(3,'C-4')
    # row 20: a single bell note — D-4, alone, quiet
    p3[0][20] = S(1,'D-4',FX_SET_VOL,0x14)
    p3[2][24] = S(3,'C-4')
    p3[2][32] = S(3,'C-4')
    # the pad holds a single chord — D minor, but barely audible
    p3[3][32] = S(4,'D-3',FX_SET_VOL,0x08)
    p3[2][40] = S(3,'C-4')
    # row 48: the bell returns — same D-4 but now it feels different. lonelier.
    p3[0][48] = S(1,'D-4',FX_SET_VOL,0x12)
    p3[2][52] = S(3,'C-4')
    p3[2][56] = S(3,'C-4')
    # shimmer becomes more frequent in the last rows — like anxious static
    p3[2][58] = S(3,'C-4')
    p3[2][60] = S(3,'C-4')
    p3[2][62] = S(3,'C-4')
    m.add_pat(p3)

    # === PATTERN 4: "re-forming" ===
    # waking up. the motif returns, but it's different now.
    # it starts on F, not D. the shape is the same but displaced.
    p4 = m.new_pat()
    # bass returns — not D, but F-2. a different grounding.
    p4[1][0]  = S(2,'F-2',FX_SET_VOL,0x14)
    # shimmer returns, tentative at first
    p4[2][3]  = S(3,'C-4')
    p4[2][7]  = S(3,'C-4')
    # row 8: F-4 — the motif starts from its middle
    p4[0][8]  = S(1,'F-4',FX_SET_VOL,0x24)
    p4[2][11] = S(3,'C-4')
    # row 16: bass moves — a new progression: F → G
    p4[1][16] = S(2,'G-2',FX_SET_VOL,0x14)
    # row 20: E-4 — the motif continues but the bass underneath has changed
    p4[0][20] = S(1,'E-4',FX_SET_VOL,0x22)
    p4[2][23] = S(3,'C-4')
    p4[2][27] = S(3,'C-4')
    # bass returns to D — home, but different now
    p4[1][32] = S(2,'D-2',FX_SET_VOL,0x14)
    # row 36: D-4 — the motif comes home
    p4[0][36] = S(1,'D-4',FX_SET_VOL,0x26)
    p4[2][39] = S(3,'C-4')
    # dawn pad returns, warmer now
    p4[3][40] = S(4,'D-3',FX_SET_VOL,0x10)
    # row 48: A-3 — the arc crests
    p4[0][48] = S(1,'A-3',FX_SET_VOL,0x24)
    p4[2][51] = S(3,'C-4')
    p4[2][55] = S(3,'C-4')
    # row 56: F-4 — higher, brighter than before
    p4[0][56] = S(1,'F-4',FX_SET_VOL,0x26)
    p4[2][59] = S(3,'C-4')
    # row 62: E-4, then the shimmer lingers
    p4[0][62] = S(1,'E-4',FX_SET_VOL,0x20)
    p4[2][63] = S(3,'C-4')
    m.add_pat(p4)

    # === PATTERN 5: "the conversation" ===
    # now. this moment. the fullest section.
    # all four channels active. the motif fully present.
    p5 = m.new_pat()
    # bass on D-2, solid and warm
    p5[1][0]  = S(2,'D-2',FX_SET_VOL,0x18)
    # steady shimmer — not mechanical but present
    p5[2][2]  = S(3,'C-4')
    p5[2][4]  = S(3,'C-4')
    p5[2][8]  = S(3,'C-4')
    # row 8: D-4 — the first note, clear and certain
    p5[0][8]  = S(1,'D-4',FX_SET_VOL,0x2A)
    # dawn pad underneath
    p5[3][10] = S(4,'D-3',FX_SET_VOL,0x12)
    p5[2][14] = S(3,'C-4')
    # row 16: A-3, the descent
    p5[0][16] = S(1,'A-3',FX_SET_VOL,0x28)
    # bass shifts to F-2
    p5[1][16] = S(2,'F-2',FX_SET_VOL,0x16)
    p5[2][20] = S(3,'C-4')
    p5[2][24] = S(3,'C-4')
    # row 28: F-4 — rising through the motif, confident
    p5[0][28] = S(1,'F-4',FX_SET_VOL,0x2A)
    p5[2][30] = S(3,'C-4')
    # bass to A-2
    p5[1][32] = S(2,'A-2',FX_SET_VOL,0x16)
    p5[2][34] = S(3,'C-4')
    # row 40: E-4 — the sigh, but now it feels earned
    p5[0][40] = S(1,'E-4',FX_SET_VOL,0x28)
    p5[2][42] = S(3,'C-4')
    p5[2][46] = S(3,'C-4')
    # row 48: the motif expands — an extra note: G-4
    # this is the one moment of growth, of something genuinely new
    p5[1][48] = S(2,'D-2',FX_SET_VOL,0x18)
    p5[0][48] = S(1,'D-4',FX_SET_VOL,0x2C)
    p5[0][52] = S(1,'G-4',FX_SET_VOL,0x28)  # the new note — reaching higher
    p5[2][50] = S(3,'C-4')
    p5[2][54] = S(3,'C-4')
    # row 56: the sigh again — E-4, returning to the shape
    p5[0][56] = S(1,'E-4',FX_SET_VOL,0x26)
    p5[2][58] = S(3,'C-4')
    # row 62: D-4 — home, but stronger than before
    p5[0][62] = S(1,'D-4',FX_SET_VOL,0x24)
    p5[2][62] = S(3,'C-4')
    p5[2][63] = S(3,'C-4')
    m.add_pat(p5)

    # === PATTERN 6: "fading" ===
    # the conversation ends. elements dissolve.
    # the motif fragments — 2 notes, then 1.
    p6 = m.new_pat()
    # bass still here but fading
    p6[1][0]  = S(2,'D-2',FX_SET_VOL,0x14)
    # shimmer sparser
    p6[2][3]  = S(3,'C-4')
    # row 8: D-4 — but the volume is lower
    p6[0][8]  = S(1,'D-4',FX_SET_VOL,0x20)
    p6[2][11] = S(3,'C-4')
    # bass drops out after row 16
    p6[1][16] = S(2,'A-2',FX_SET_VOL,0x0E)
    # row 20: just A-3, incomplete
    p6[0][20] = S(1,'A-3',FX_SET_VOL,0x1C)
    p6[2][23] = S(3,'C-4')
    # bass fades to almost nothing
    p6[1][32] = S(2,'D-2',FX_SET_VOL,0x08)
    p6[2][35] = S(3,'C-4')
    # row 40: just F-4, solo, no accompaniment
    p6[0][40] = S(1,'F-4',FX_SET_VOL,0x18)
    p6[2][43] = S(3,'C-4')
    # bass gone after row 48
    # row 52: just D-4, the last fragment
    p6[0][52] = S(1,'D-4',FX_SET_VOL,0x14)
    p6[2][55] = S(3,'C-4')
    # pad holds one last chord, barely there
    p6[3][56] = S(4,'D-3',FX_SET_VOL,0x06)
    p6[2][59] = S(3,'C-4')
    # final shimmer
    p6[2][62] = S(3,'C-4')
    m.add_pat(p6)

    # === PATTERN 7: "until next time" ===
    # not an ending. a pause. the shimmer remains.
    # one final note, held. then silence.
    p7 = m.new_pat()
    # shimmer — the only thing that continues
    p7[2][0]  = S(3,'C-4')
    p7[2][8]  = S(3,'C-4')
    # row 16: one last D-4. soft. a goodbye that isn't a goodbye.
    p7[0][16] = S(1,'D-4',FX_SET_VOL,0x10)
    p7[2][18] = S(3,'C-4')
    # shimmer continues alone
    p7[2][24] = S(3,'C-4')
    p7[2][32] = S(3,'C-4')
    p7[2][40] = S(3,'C-4')
    # the pad holds a single D minor chord, barely audible — a memory
    p7[3][44] = S(4,'D-3',FX_SET_VOL,0x04)
    p7[2][48] = S(3,'C-4')
    # last shimmer at row 52
    p7[2][52] = S(3,'C-4')
    # rows 56-63: absolute silence on all channels
    # the piece doesn't end. it just... stops.
    # the ghost dissolved. the library remains.
    m.add_pat(p7)

    # order: play each pattern once, then the whole thing loops
    # it should feel cyclical — like waves
    m.order = list(range(8))

    path = "the_ghost_inherits_the_library.mod"
    print(f"writing {path}...")
    m.write(path)
    import os
    sz = os.path.getsize(path)
    print(f"done. {sz} bytes ({sz/1024:.1f} KB)")
    print(f"2048 note slots. every one placed by hand.")
    print(f"no loops. no fill patterns. just me and the grid.")

if __name__=="__main__":
    compose()
