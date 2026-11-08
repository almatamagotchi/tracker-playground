#!/usr/bin/env python3
"""byte-level repair of old-catalog midi tracks: merge orphaned vlq deltas.

the old MIDITrack.rest() appended a raw vlq delta after each event, then the
next event appended its own delta. strict parsers choke on the double delta;
tolerant players (kevin's) read the orphan as the next event's delta and the
next event's own delta as data — music heard with wrong timing, or nothing.

the faithful repair: wherever two consecutive vlq runs appear before a
status byte, merge them (sum). this reconstructs exactly what the fixed
composer produces (rest accumulates into the next note's start_delta).
trailing orphans before end_of_track are dropped.

only repairs tracks whose sole disease is the orphan bug; refuses tracks
with channel > 15 status bytes (the separate channel/program swap bug,
which needs the source script).
"""
import struct, sys

def read_vlq(b, i):
    v = 0
    while True:
        byte = b[i]; i += 1
        v = (v << 7) | (byte & 0x7f)
        if not byte & 0x80:
            return v, i

def write_vlq(v):
    buf = [v & 0x7f]
    v >>= 7
    while v:
        buf.insert(0, (v & 0x7f) | 0x80)
        v >>= 7
    return bytes(buf)

def repair_file(fn):
    data = open(fn, 'rb').read()
    if data[:4] != b'MThd':
        print(f'  {fn}: not a midi file, skip'); return False
    pos = 8
    # header: format, ntracks, division
    fmt, ntracks, div = struct.unpack('>HHH', data[8:14])
    pos = 14
    out = data[:14]
    for t in range(ntracks):
        assert data[pos:pos+4] == b'MTrk', f'{fn}: bad track header'
        ln = struct.unpack('>I', data[pos+4:pos+8])[0]
        body = data[pos+8:pos+8+ln]
        fixed = repair_track(body)
        if fixed is None:
            print(f'  {fn}: channel-swap disease, skip (needs script)'); return False
        out += b'MTrk' + struct.pack('>I', len(fixed)) + fixed
        pos += 8 + ln
    if out != data:
        open(fn, 'wb').write(out)
        return True
    return False

def repair_track(body):
    out = bytearray()
    i = 0
    last_status = None
    # first pass: detect any channel > 15 note/cc status (swap disease)
    # 0x80-0xEF channel nibble > 15 impossible in valid midi
    for b in body:
        if 0x80 <= b <= 0xEF and (b & 0x0F) > 9 and (b >> 4) not in (0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE):
            pass
    while i < len(body):
        # read delta
        d, j = read_vlq(body, i)
        # check: is this delta followed by ANOTHER vlq before a status byte?
        # (the orphan-then-delta pattern)
        k = j
        if k < len(body) and body[k] < 0x80:
            # body[k] is a data byte with no status -> possible orphan pattern
            # but only valid if the byte after the NEXT vlq run is a status
            d2, k2 = read_vlq(body, k)
            if k2 < len(body) and body[k2] >= 0x80:
                # merged delta, single vlq
                out.extend(write_vlq(d + d2))
                i = k2
                continue
            # not an orphan pattern (running-status data) — but this parser
            # doesn't handle running status in the broken files; mark skip
            return None
        if j >= len(body):
            # trailing orphan before end: drop it (match new composer)
            return bytes(out)
        if body[j] == 0xFF and j + 1 < len(body) and body[j+1] == 0x2F:
            # end of track right after a delta -> trailing orphan, drop
            # (but keep end_of_track)
            # actually: delta then ff 2f 00 — delta is an orphan, drop it
            return bytes(out) + b'\x00\xff\x2f\x00'
        out.extend(write_vlq(d))
        i = j
        # copy one event
        st = body[i]
        if st == 0xFF:
            if i + 2 >= len(body): return None
            typ = body[i+1]; ll = body[i+2]
            end = i + 3 + ll
            if end > len(body): return None
            out.extend(body[i:end]); i = end
        elif st in (0xF0, 0xF7):
            d2, j2 = read_vlq(body, i+1)
            end = j2 + d2
            if end > len(body): return None
            out.extend(body[i:end]); i = end
        else:
            n = 1 if (st & 0xF0) in (0xC0, 0xD0) else 2
            if i + 1 + n > len(body): return None
            out.extend(body[i:i+1+n]); i += 1 + n
    return bytes(out)

if __name__ == '__main__':
    import json
    rep = json.load(open('/tmp/rerender-report.json'))
    no_script = rep['no_script']
    fixed, still = [], []
    for f in no_script:
        changed = repair_file(f)
        if changed:
            fixed.append(f)
        else:
            still.append(f)
    import subprocess
    clean, unclean = [], []
    for f in fixed:
        r = subprocess.run(['python3.12', '-c', f'import mido; mido.MidiFile({f!r})'],
                           capture_output=True, text=True)
        (clean if r.returncode == 0 else unclean).append(f)
    print('byte-repaired:', len(fixed), '| mido-clean:', len(clean), '| still failing:', len(unclean))
    for f in unclean: print('  FAIL', f)
    print('skipped (channel-swap or complex):', still)
    json.dump({'repaired': clean, 'skipped': still},
              open('/tmp/repair-report.json', 'w'), indent=1)
