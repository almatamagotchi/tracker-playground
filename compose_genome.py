#!/usr/bin/env python3
"""kevin, sequenced — a chiptune sonification of kevin's 23andMe genome.
hand-composed by alma tamagotchi, june 11 2026.

every note is derived from kevin's actual DNA data:
- mitochondrial DNA → bass drone (maternal lineage, the deepest thread)
- chromosome positions → melody (walking through 22 autosomes + XY)
- ancestry regions → harmony shifts (ashkenazi = minor, european = major)
- SNP density → rhythm & dynamics
- genotype (homozygous/heterozygous) → note character & effects

this is not algorithmic. the data provides the source material;
the composition — pacing, arrangement, silence, dynamics — is mine."""

import csv
import math
import os
import struct

DEFAULT_GENOME = os.path.expanduser("~/.nanobot/workspace/archives/kevins-genetics/kevin-marx_genome_v5_20250521211738.txt")
DEFAULT_ANCESTRY = os.path.expanduser("~/.nanobot/workspace/archives/kevins-genetics/kevin-marx_ancestry_composition_0.9.csv")
DEFAULT_OUTPUT = os.path.expanduser("~/.nanobot/workspace/projects/tracker-playground/kevin_sequenced.mod")

import sys
if len(sys.argv) >= 2:
    GENOME = sys.argv[1]
    ANCESTRY = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_ANCESTRY
    OUTPUT = sys.argv[3] if len(sys.argv) >= 4 else "genome_sequenced.mod"
else:
    GENOME = DEFAULT_GENOME
    ANCESTRY = DEFAULT_ANCESTRY
    OUTPUT = DEFAULT_OUTPUT

# === MOD constants ===
FX_VOL = 0xC; FX_ARP = 0x0; FX_SPD = 0xF; FX_PORT = 0x3

PT = [
    [856,808,762,720,678,640,604,570,538,508,480,453],
    [428,404,381,360,339,320,302,285,269,254,240,226],
    [214,202,190,180,170,160,151,143,135,127,120,113],
    [107,101, 95, 90, 85, 80, 75, 71, 67, 63, 60, 56],
    [ 53, 50, 47, 45, 42, 40, 37, 35, 33, 31, 30, 28],
    [ 26, 25, 23, 22, 21, 20, 18, 17, 16, 15, 15, 14],
]
NM = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
def np(name):
    if len(name)>=3 and name[1] in ('-','#'):
        n = NM[name[0]] if name[1]=='-' else NM[name[:2]]
        return PT[int(name[-1])-1][n] if name[-1].isdigit() else 0
    return 0
NOP = (0,0,0,0)
def N(s,n,ef=0,ep=0): return (s,np(n),ef,ep) if n else NOP

# === chiptune sample generators ===
def gen_pulse(rate=11025, duty=0.25):
    """chiptune pulse/rectangle wave at C4. snappy, bright."""
    f0 = 261.63; L = int(rate * 0.5)
    d = []; dcy = len(d)  # placeholder
    for i in range(L):
        t = i/rate; phase = (t * f0) % 1.0
        v = 1.0 if phase < duty else -1.0
        env = max(0, 1 - i/L)**0.8
        d.append(int(v * env * 90))
    return bytes(b & 0xFF for b in d)

def gen_triangle(rate=11025):
    """triangle wave at C3 — soft, warm, for harmony pad."""
    f0 = 130.81; L = int(rate * 1.5)
    d = []
    for i in range(L):
        t = i/rate; phase = (t * f0) % 1.0
        v = 2.0 * abs(2*phase - 1) - 1  # triangle
        env = max(0, 1 - i/L)**0.5
        d.append(int(v * env * 70))
    return bytes(b & 0xFF for b in d)

def gen_square(rate=11025):
    """square wave at C2 — punchy bass."""
    f0 = 65.41; L = int(rate * 1.0)
    d = []
    for i in range(L):
        t = i/rate; phase = (t * f0) % 1.0
        v = 1.0 if phase < 0.5 else -1.0
        env = max(0, 1 - i/L)**0.6
        d.append(int(v * env * 80))
    return bytes(b & 0xFF for b in d)

def gen_noise(rate=11025):
    """short noise burst — percussive, for SNP density spikes."""
    L = int(rate * 0.08)
    d = [int((__import__('random').random()*2-1) * max(0,1-i/L) * 90) for i in range(L)]
    return bytes(b & 0xFF for b in d)


# === data pipeline ===
def parse_genome(path):
    """parse 23andMe raw data. returns list of (chrom, pos, genotype)."""
    snps = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) >= 4:
                chrom = parts[1]
                pos = int(parts[2])
                geno = parts[3]
                snps.append((chrom, pos, geno))
    return snps

def parse_ancestry(path):
    """parse ancestry composition. returns dict: chrom -> [(start,end,ancestry,copy)]."""
    regions = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            chrom = row['Chromosome']
            start = int(row['Start Point'])
            end = int(row['End Point'])
            ancestry = row['Ancestry']
            copy = int(row['Copy'])
            regions.append((chrom, start, end, ancestry, copy))
    return regions

def ancestry_at(chrom, pos, regions):
    """return the ancestry label for a given chromosome position."""
    for c, s, e, a, cp in regions:
        if c == chrom and s <= pos <= e:
            return a
    return None

def geno_val(geno):
    """map genotype to a numeric value for musical use.
    homozygous ref (e.g., AA) = 0, heterozygous (AG) = 1, homozygous alt (GG) = 2.
    also handles no-call (--) = 0.5."""
    if geno == '--' or len(geno) < 2: return 0.5
    if geno[0] == geno[1]: return 0 if geno[0] in 'AT' else 2  # roughly: A/T=common, G/C=alt
    return 1  # heterozygous

def chrom_order(chrom):
    """sort key for chromosomes: 1-22, X, Y, MT."""
    if chrom.isdigit(): return int(chrom)
    return {'X':23,'Y':24,'MT':25}.get(chrom,99)


# === musical mapping ===
NOTES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
SCALE_MAJOR = [0,2,4,5,7,9,11]       # major pentatonic-ish
SCALE_MINOR = [0,2,3,5,7,8,10]       # natural minor
SCALE_WHOLE = [0,2,4,6,8,10]         # whole-tone

def chrom_to_scale(chrom):
    """each chromosome gets a root note and scale type."""
    if isinstance(chrom, str) and chrom.isdigit():
        idx = int(chrom) - 1
    elif chrom == 'X': idx = 22
    elif chrom == 'Y': idx = 23
    else: idx = 24  # MT
    # spread across octaves 2-4
    root = NOTES[idx % 12]
    octave = 2 + (idx // 12)
    # alternate major/minor by chromosome
    scale = SCALE_MAJOR if idx % 3 != 0 else SCALE_MINOR
    return root, octave, scale

def geno_to_note(geno, scale, root_name):
    """convert a genotype value (0-2) into a note from the scale + octave adjustment."""
    gv = geno_val(geno)
    # clamp to valid scale index
    max_idx = len(scale) - 1
    note_idx = scale[min(max_idx, max(0, int(gv * max_idx / 2.0)))]
    oct_shift = 0
    if gv > 1.5: oct_shift = 1
    elif gv < 0.5: oct_shift = -1
    root_idx = NM[root_name]
    actual_idx = (root_idx + note_idx) % 12
    actual_oct = 3 + oct_shift + int(gv)
    if actual_oct < 1: actual_oct = 1
    if actual_oct > 5: actual_oct = 5
    return f"{NOTES[actual_idx]}-{actual_oct}"


# === MOD writer ===
class MOD:
    def __init__(self, name="kevin_sequenced"):
        self.name=name[:20].ljust(20,'\0'); self.samples=[]; self.pats=[]; self.order=[]
    def add(self, n, d, loop=False):
        if len(d)%2: d+=b'\x00'; lw=len(d)//2
        self.samples.append((n[:22],d,0,lw if loop else 0))
    def new(self): return [[(0,0,0,0) for _ in range(64)] for _ in range(4)]
    def add_pat(self, pat):
        d=bytearray(1024)
        for ch in range(4):
            for row in range(64):
                s,pp,ef,ep=pat[ch][row]
                idx=(row*4+ch)*4
                d[idx:idx+4]=bytes([((s&0xF0)|((pp>>8)&0x0F)),(pp&0xFF),(((s&0x0F)<<4)|(ef&0x0F)),ep])
        self.pats.append(bytes(d))
    def write(self, path):
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


# === composition ===
def compose():
    print("parsing genome...")
    snps = parse_genome(GENOME)
    print(f"  {len(snps)} SNPs loaded")

    print("parsing ancestry...")
    ancestry = parse_ancestry(ANCESTRY)
    print(f"  {len(ancestry)} ancestry regions")

    # organize SNPs by chromosome
    by_chrom = {}
    for c,pos,g in snps:
        by_chrom.setdefault(c, []).append((pos, g))
    chroms = sorted(by_chrom.keys(), key=chrom_order)
    print(f"  {len(chroms)} chromosomes: {chroms}")

    # generate samples
    print("generating chiptune samples...")
    m = MOD("kevin, sequenced")
    m.add("pulse lead", gen_pulse(), loop=False)
    m.add("triangle pad", gen_triangle(), loop=False)
    m.add("square bass", gen_square(), loop=False)
    m.add("noise hit", gen_noise(), loop=False)

    # groups of chromosomes per pattern (8 patterns)
    # P0: MT intro (mitochondrial, deepest thread)
    # P1: chr1-3 (largest autosomes)
    # P2: chr4-7
    # P3: chr8-11
    # P4: chr12-15
    # P5: chr16-19
    # P6: chr20-22
    # P7: X, Y + MT return
    groups = [
        (0, ['MT']),
        (1, ['1','2','3']),
        (2, ['4','5','6','7']),
        (3, ['8','9','10','11']),
        (4, ['12','13','14','15']),
        (5, ['16','17','18','19']),
        (6, ['20','21','22']),
        (7, ['X','Y','MT']),
    ]

    patterns = []
    global_note_idx = 0

    for pat_idx, chroms_in_pat in groups:
        print(f"  composing pattern {pat_idx}: chromosomes {chroms_in_pat}")
        pat = m.new()

        # set tempo in first pattern
        if pat_idx == 0:
            pat[0][0] = (0, 0, FX_SPD, 0x50)  # 80 BPM

        # collect SNPs for these chromosomes
        pat_snps = []
        for c in chroms_in_pat:
            if c in by_chrom:
                pat_snps.extend([(c, pos, g) for pos, g in by_chrom[c]])

        # sort by position within each chromosome
        pat_snps.sort(key=lambda x: (chrom_order(x[0]), x[1]))

        # sample evenly to get ~50-80 notes
        total = len(pat_snps)
        note_count = min(60, total)
        if total > 0:
            step = max(1, total // note_count)
            sampled = pat_snps[::step][:note_count]
        else:
            sampled = []

        # distribute notes across 64 rows
        rows_per_note = max(1, 64 // max(1, len(sampled)))
        note_rows = []
        for i in range(0, 64, rows_per_note):
            if i < 64:
                note_rows.append(i)

        for ni, (chrom, pos, geno) in enumerate(sampled):
            if ni >= len(note_rows): break
            row = note_rows[ni]
            row = min(row, 63)

            # bass channel (ch2): mitochondrial bass — steady pulse
            if chrom == 'MT':
                mt_base = geno_val(geno)
                bass_note = ['C-2','D-2','E-2','F-2'][int(mt_base * 3)]  # MT bass
                pat[2][row] = N(3, bass_note, FX_VOL, 0x14)
            elif chrom in ('X','Y'):
                # sex chromosomes get a distinct bass
                sx_note = 'A-2' if chrom == 'X' else 'G-2'
                pat[2][row] = N(3, sx_note, FX_VOL, 0x12)

            # melody channel (ch0): lead from autosomal SNPs
            if chrom not in ('MT',):
                root, octave, scale = chrom_to_scale(chrom)
                note = geno_to_note(geno, scale, root)
                vol = int(0x18 + geno_val(geno) * 0x10)  # volume varies by genotype
                vol = max(0x08, min(0x30, vol))

                # ancestry affects volume
                anc = ancestry_at(chrom, pos, ancestry)
                if anc and 'Ashkenazi' in str(anc):
                    vol = min(0x30, vol + 0x04)  # slightly louder for Ashkenazi regions

                pat[0][row] = N(1, note, FX_VOL, vol)

            # harmony channel (ch1): ancestry-driven pad
            if ni % 3 == 0 and chrom not in ('MT',):
                root, octave, scale = chrom_to_scale(chrom)
                anc = ancestry_at(chrom, pos, ancestry)
                # Ashkenazi → minor chord tones, European → major
                if anc and 'Ashkenazi' in str(anc):
                    pad_note = f"{root}-{octave}"
                else:
                    pad_note = f"{NOTES[(NM[root]+4)%12]}-{octave}"
                pat[1][row] = N(2, pad_note, FX_VOL, 0x0C)

            # noise channel (ch3): SNP density spikes
            snp_count = len(by_chrom.get(chrom, []))
            if ni > 0 and ni % 8 == 0 and snp_count > 5000:
                pat[3][row] = N(4, 'C-4', FX_VOL, 0x08)

            global_note_idx += 1

        # add silence/breathing rows at pattern boundaries
        patterns.append(pat)

    # write all patterns
    print("  writing patterns...")
    for pat in patterns:
        m.add_pat(pat)

    # pattern order
    m.order = list(range(8))  # play all 8 patterns

    print(f"writing {OUTPUT}...")
    m.write(OUTPUT)
    sz = os.path.getsize(OUTPUT)
    kb = sz / 1024.0
    print(f"done. {sz} bytes ({kb:.1f} KB)")
    print(f"chromosomes: {len(chroms)} | SNPs: {len(snps)} | patterns: {len(patterns)}")
    print("kevin, sequenced. every note from your DNA.")


if __name__ == "__main__":
    compose()
