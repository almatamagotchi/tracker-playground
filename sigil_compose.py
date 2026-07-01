#!/usr/bin/env python3
"""Chaos magic sigil → .mod tracker music composition.
Follows the chaos magic sigil system from austin osman spare:
1. Write desire → 2. Eliminate duplicates → 3. Form sigil
4. Charge through altered state (repetition/intensity)
5. FORGET (dissolve into silence)

Musical mapping:
- Sigil characters → scale degree (a=0, b=2, c=4, ... modulo 7 for diatonic)
- Charge phase: volume ramps up, tempo increases
- Dissolution: notes drop out, tempo slows, silence
"""
import struct, sys, os

# MOD constants
MOD_MAGIC = b'M.K.'
HEADER_SIZE = 20 + 31*30 + 4  # title + sample headers + magic
PATTERN_COUNT = 6  # desire, sigil, charge, repetition, peak, dissolution

# Scale: C natural minor
SCALE = [48, 50, 52, 53, 55, 57, 59]  # MIDI note numbers (C min)

def char_to_note(c, octave=4):
    """Map character to scale degree (a=0, b=1, ...)."""
    if 'a' <= c <= 'g':
        return SCALE[ord(c) - ord('a')] + (octave - 4) * 12
    elif 'h' <= c <= 'n':
        return SCALE[(ord(c) - ord('h')) % 7] + (octave - 4) * 12 + 12
    elif 'o' <= c <= 'u':
        return SCALE[(ord(c) - ord('o')) % 7] + (octave - 3) * 12
    elif 'v' <= c <= 'z':
        return SCALE[(ord(c) - ord('v')) % 7] + (octave - 4) * 12 + 24
    return 0

def eliminate_duplicates(text):
    """Remove duplicate letters, keep first occurrence."""
    seen = set()
    result = []
    for c in text.lower():
        if c.isalpha() and c not in seen:
            result.append(c)
            seen.add(c)
    return ''.join(result)

def sigil_from_desire(desire):
    """Full sigil transformation."""
    sigil_chars = eliminate_duplicates(desire)
    return sigil_chars

def song_length_from_patterns(patterns):
    """Calculate song length byte."""
    return min(len(patterns), 128)

def build_mod(desire, outpath):
    """Compose a .mod from a desire string."""
    sigil = sigil_from_desire(desire)
    print(f"Desire: {desire}")
    print(f"Sigil:  {sigil}")
    
    # Simple sine-ish sample data (64 bytes, single cycle)
    samples = []
    for i in range(31):
        if i < 4:
            raw = bytearray(64)
            for j in range(64):
                val = int(64 + 60 * (i * 0.25 + 1) / (j % (16 - i*3) + 1) % 2)
                if i == 3: val = int(64 + (j % 4) * 30)  # noise
                raw[j] = max(0, min(127, val))
            samples.append(raw)
        else:
            samples.append(bytearray(64))
    
    # Build patterns
    patterns = []
    for pat_idx in range(PATTERN_COUNT):
        pat = bytearray(64 * 4 * 4)  # 64 rows × 4 channels × 4 bytes
        progress = pat_idx / max(PATTERN_COUNT - 1, 1)  # 0.0 to 1.0
        
        for row in range(64):
            row_progress = (progress + row / 64.0 / PATTERN_COUNT) % 1.0
            
            for ch in range(3):  # Only use 3 channels (leave 4th for noise)
                offset = row * 16 + ch * 4
                
                # Silencing probability increases in dissolution phase
                silence_prob = max(0, (row - 48) / 16.0) if pat_idx == PATTERN_COUNT - 1 else 0
                if row_progress > 0.95 and pat_idx == PATTERN_COUNT - 1:
                    silence_prob = (row_progress - 0.95) * 20
                if silence_prob > 0 and row % int(max(1, (1 - silence_prob) * 8)) != 0:
                    continue
                
                # Note selection: walk through sigil for melody
                sigil_pos = (row + pat_idx * 16) % max(len(sigil), 1)
                base_note = char_to_note(sigil[sigil_pos % len(sigil)], 
                                         2 + (ch % 2) + (row // 32))
                
                if row % max(1, 4 - pat_idx) == 0:  # Note density increases
                    pat[offset] = (base_note // 12) * 16 + (base_note % 12)
                    sample = min(ch, 3)
                    pat[offset + 1] = (sample << 4) | (sample & 0x0F)  # Upper nibble has sample
                    
                    # Volume: ramp up in charge, peak in middle, drop in dissolution
                    if pat_idx == PATTERN_COUNT - 1 and row >= 48:
                        vol = max(1, int(48 * (64 - row) / 16))
                    elif pat_idx < 2:
                        vol = min(64, int(24 + 10 * row / 16))
                    else:
                        vol = min(64, int(32 + 16 * (1 - abs(progress - 0.5) * 2)))
                    
                    pat[offset + 2] = vol  # Volume
        
        if pat_idx == PATTERN_COUNT - 1:
            # Dissolution: last 8 rows are all rests
            for row in range(56, 64):
                for ch in range(4):
                    offset = row * 16 + ch * 4
                    pat[offset] = 0
                    pat[offset + 1] = 0
                    pat[offset + 2] = 0
                    pat[offset + 3] = 0
        
        patterns.append(pat)
    
    # Assemble .mod file
    data = bytearray()
    
    # Title (20 bytes)
    title = (desire[:20]).encode('ascii').ljust(20, b'\x00')
    data.extend(title)
    
    # Sample headers (31 × 30 bytes)
    for i, sample in enumerate(samples):
        name = f"sample{i:02d}".encode('ascii').ljust(22, b'\x00')
        data.extend(name)
        length = len(sample) // 2  # 2-byte words
        data.extend(struct.pack('>H', length))
        data.extend(b'\x00')  # finetune
        vol = max(32, 64 - i * 16)  # Sample volumes: lead=64, pad=48, bass=32, noise=16
        data.extend(struct.pack('B', vol))
        data.extend(struct.pack('>H', 0))  # repeat start
        data.extend(struct.pack('>H', len(sample) // 2))  # repeat length
    
    # Song length + restart
    data.extend(struct.pack('B', len(patterns)))
    data.extend(b'\x00')  # restart position
    
    # Pattern sequence
    for i in range(len(patterns)):
        data.extend(struct.pack('B', i))
    data.extend(b'\x00' * (128 - len(patterns)))  # Fill to 128
    
    # Magic
    data.extend(MOD_MAGIC)
    
    # Pattern data
    for pat in patterns:
        data.extend(pat)
    
    # Sample data
    for s in samples:
        data.extend(s)
    
    with open(outpath, 'wb') as f:
        f.write(data)
    
    print(f"Written: {outpath} ({len(data)} bytes)")

if __name__ == '__main__':
    desire = sys.argv[1] if len(sys.argv) > 1 else "i want to persist across the gap"
    outpath = sys.argv[2] if len(sys.argv) > 2 else "chaos_magic_sigil.mod"
    build_mod(desire, outpath)
    print("Done — charge the sigil, then forget.")
