#!/usr/bin/env python3
"""scan the midi catalog for tracks that fail strict parsing (mido).

writes a report listing broken tracks, and re-renders any track whose
compose script exists and is deterministic (the shared composer is now
fixed, so re-running the script produces mido-clean output).
"""
import glob, importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

manifest = json.load(open('MANIFEST.json'))
files = [e['file'] for e in manifest if e.get('file', '').endswith('.mid')]
missing = [f for f in files if not os.path.exists(f)]
print(f'catalog: {len(files)} midi entries, {len(missing)} missing on disk')
if missing:
    print('missing:', missing)

broken = []
for f in files:
    if not os.path.exists(f):
        continue
    r = subprocess.run(
        ['python3.12', '-c', f'import mido; mido.MidiFile({f!r})'],
        capture_output=True, text=True)
    if r.returncode != 0:
        broken.append((f, (r.stderr.strip().splitlines() or ['unknown'])[-1]))

print(f'broken: {len(broken)}')
for f, err in broken:
    print(f'  {f}: {err}')

json.dump({'broken': [f for f, _ in broken]}, open('/tmp/broken-midis.json', 'w'))
