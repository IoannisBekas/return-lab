import json, subprocess, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

git_modified = set([f.replace('public/content/figures/', '') for f in subprocess.check_output(['git', 'diff', '--name-only']).decode('utf-8').splitlines() if f.startswith('public/content/figures/')])

with open('true_scans.json', encoding='utf-8') as f:
    true_scans = json.load(f)

remaining = [s for s in true_scans if s['asset'] not in git_modified]
print(f"Total true scans: {len(true_scans)}")
print(f"Modified: {len(true_scans) - len(remaining)}")
print(f"Remaining: {len(remaining)}")

by_reading = defaultdict(list)
for r in remaining:
    rd = r['readings'][0] if r['readings'] else 'unknown'
    by_reading[rd].append(r)

for rd, items in sorted(by_reading.items()):
    print(f"\n=== {rd} ({len(items)} figures) ===")
    for item in items:
        alt = item['alts'][0] if item['alts'] else ''
        print(f"  {item['asset']} ({item['actual_size'][0]}x{item['actual_size'][1]}) - {alt[:70]}")
