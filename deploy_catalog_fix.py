#!/usr/bin/env python3
"""deploy the repaired catalog files to the VPS as one tar pipe."""
import json, subprocess, os

rep = json.load(open('/tmp/rerender-report.json'))
fixed = list(rep['rerendered'])
if 'craigs-whisky.mid' not in fixed:
    fixed.append('craigs-whisky.mid')

tar_path = '/tmp/catalog-fix.tar'
subprocess.run(['tar', '-cf', tar_path] + fixed, check=True)
print(f'{len(fixed)} files tarballed')

cmd = (f'cat {tar_path} | ssh tamagotchi '
       f'"cd /usr/local/www/alma/music/midi && sudo tar -xf - && echo deployed"')
r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print(r.stdout, r.stderr)
if r.returncode != 0:
    raise SystemExit('deploy failed')
print('deployed')
