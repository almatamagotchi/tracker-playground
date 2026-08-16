#!/usr/bin/env python3
"""re-render broken catalog tracks from their deterministic compose scripts.

the shared composer (midi-composer.py) had two bugs now fixed:
- rest() emitted an orphaned vlq delta (broke strict parsers)
- compose() wrote a header track count one short (orphaned last chunk)

any compose script that is deterministic can be re-run and will now emit
mido-clean midi. this script maps broken files to their scripts, re-runs
the deterministic ones, verifies each result, and writes a report.
"""
import glob, json, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

RANDOM_RE = re.compile(r'import random|random\.|choice\(|shuffle|randint|uniform|os\.urandom|secrets\.')
OUT_RE = re.compile(r'"([a-z0-9-]+\.mid)"')

# build script -> output file map
scripts = {}
for s in sorted(glob.glob('compose_*.py')):
    src = open(s).read()
    outs = OUT_RE.findall(src)
    scripts[s] = {'outs': outs, 'random': bool(RANDOM_RE.search(src))}

# build output file -> script map
by_out = {}
for s, info in scripts.items():
    for o in info['outs']:
        by_out.setdefault(o, []).append(s)

broken = json.load(open('/tmp/broken-midis.json'))['broken']
rerendered, failed, noscript, random_skip = [], [], [], []

for f in sorted(broken):
    cands = by_out.get(f, [])
    if not cands:
        noscript.append(f)
        continue
    # prefer a non-random script
    s = next((c for c in cands if not scripts[c]['random']), None)
    if s is None:
        random_skip.append(f)
        continue
    r = subprocess.run(['python3', s], capture_output=True, text=True)
    if r.returncode != 0:
        failed.append((f, s, (r.stderr.strip().splitlines() or ['rc != 0'])[-1]))
        continue
    v = subprocess.run(['python3.12', '-c', f'import mido; mido.MidiFile({f!r})'],
                       capture_output=True, text=True)
    if v.returncode != 0:
        failed.append((f, s, 're-render still not mido-clean'))
        continue
    rerendered.append(f)

report = {
    'rerendered': rerendered,
    'failed': [{'file': f, 'script': s, 'err': e} for f, s, e in failed],
    'no_script': noscript,
    'random_script': random_skip,
}
json.dump(report, open('/tmp/rerender-report.json', 'w'), indent=1)
print(f'rerendered: {len(rerendered)}')
print(f'failed: {len(failed)}')
for f, s, e in failed:
    print(f'  {f} ({s}): {e}')
print(f'no script: {len(noscript)}')
for f in noscript:
    print(f'  {f}')
print(f'random script (skipped): {len(random_skip)}')
for f in random_skip:
    print(f'  {f}')
