#!/usr/bin/env python3
"""Volume mix normalizer for .mod tracker files.
Drops aggressive note volumes and applies per-channel balancing.
Safe rewrite — keeps original sample data and pattern structure intact.
"""
import struct, sys, os

def normalize_mod(path, outpath=None):
    """Read .mod at path, adjust volumes, write to outpath."""
    with open(path, 'rb') as f:
        data = bytearray(f.read())
    
    if len(data) < 1084:
        print(f"  SKIP {path}: too short ({len(data)} bytes)")
        return False
    
    # MOD header: offset 0 = title (20 bytes), 20 = song length (1), 21 = restart (1)
    song_length = data[20]
    num_patterns = max(data[21:105]) + 1 if song_length > 0 else 0
    num_samples = 15  # MOD only supports 1-31, but we scan what's present
    
    # Find actual number of samples used
    sample_count = 0
    for i in range(31):
        offset = 20 + 31*30 + i*30
        if offset + 30 > len(data):
            break
        # sample name at offset+0, length at offset+22 (2 bytes)
        slen = struct.unpack_from('>H', data, offset + 22)[0] * 2
        if slen > 0:
            sample_count = i + 1
    
    # Sample default volumes (offset 25 in each sample header, 0-64)
    # Lower aggressive volumes: keep leads at 64, drop everything else
    # Actually, let's lower ALL sample volumes by 25% to prevent clipping
    # when 4 channels play simultaneously
    sample_vol_changed = 0
    for i in range(min(sample_count, 31)):
        offset = 20 + 31*30 + i*30 + 25
        if offset + 1 > len(data):
            break
        vol = data[offset]
        if vol > 48:  # Lower samples that are too loud
            data[offset] = max(32, int(vol * 0.75))
            sample_vol_changed += 1
    
    # Pattern volume adjustments — lower note volumes by ~20%
    # Pattern data starts at offset 1084
    pattern_size = 64 * 4 * 4  # 64 rows × 4 channels × 4 bytes
    num_patterns_in_file = (len(data) - 1084) // pattern_size
    if song_length == 0:
        song_length = num_patterns_in_file
    
    notes_adjusted = 0
    for pat in range(min(song_length, num_patterns_in_file)):
        offset = 1084 + pat * pattern_size
        
        # Check if this is the last pattern (for fade-out)
        is_last = (pat == song_length - 1)
        
        for row in range(64):
            row_offset = offset + row * 4 * 4
            if is_last and row >= 48:  # Last 16 rows: fade out
                fade_factor = max(0, (64 - row) / 16.0)
                for ch in range(4):
                    ch_offset = row_offset + ch * 4
                    note_byte = data[ch_offset]
                    if note_byte > 0 and note_byte < 0xFF:  # Has a note
                        vol_byte = data[ch_offset + 2]  # Byte 2 has volume/effect
                        if (vol_byte & 0xF0) == 0x00 and (vol_byte & 0x0F) > 0:
                            # Unused volume nibble — set volume
                            new_vol = max(1, int((vol_byte & 0x0F) * fade_factor))
                            if new_vol > 0:
                                data[ch_offset + 2] = (vol_byte & 0xF0) | new_vol
                                notes_adjusted += 1
            else:
                for ch in range(4):
                    ch_offset = row_offset + ch * 4
                    note_byte = data[ch_offset]
                    if note_byte > 0 and note_byte < 0xFF:
                        vol_byte = data[ch_offset + 2]
                        # Only adjust if volume nibble is being used and it's loud
                        if (vol_byte & 0xF0) == 0x00 and (vol_byte & 0x0F) >= 12:
                            new_vol = max(1, int((vol_byte & 0x0F) * 0.8))
                            data[ch_offset + 2] = (vol_byte & 0xF0) | new_vol
                            notes_adjusted += 1
    
    outpath = outpath or path
    with open(outpath, 'wb') as f:
        f.write(data)
    
    print(f"  {os.path.basename(path):40s} samples:{sample_vol_changed} notes:{notes_adjusted} → {outpath}")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: mix_normalize.py <file.mod> [<file2.mod> ...]")
        print("       mix_normalize.py --all   (all *_body.mod in current dir)")
        sys.exit(1)
    
    if sys.argv[1] == '--all':
        files = sorted([f for f in os.listdir('.') if f.endswith('.mod') and 'body' in f])
    else:
        files = sys.argv[1:]
    
    for f in files:
        if os.path.exists(f):
            normalize_mod(f)
        else:
            print(f"  SKIP {f}: not found")
    
    print(f"\nDone — {len(files)} files processed.")
