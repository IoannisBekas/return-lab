import glob, json, os, re, subprocess, sys
from PIL import Image
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

# Load classification
with open('docs/math-visual-classification.json', encoding='utf-8') as f:
    classif = json.load(f)
meaningful_assets = set(a['asset'] for a in classif['assets'] if a.get('classification') == 'meaningful-visual')

# Scan all readings and extract info for every asset
asset_info = {}
all_files = sorted(glob.glob('public/content/readings/*.json') + ['public/content/reference.json'])

for file_path in all_files:
    fname = os.path.basename(file_path)
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    
    # search recursively in data for occurrences of assets
    def search_obj(obj, context=""):
        if isinstance(obj, dict):
            # Check if this object is a figure block or has asset
            asset = obj.get('asset') or obj.get('url') or obj.get('src')
            if isinstance(asset, str):
                m = re.search(r'([a-f0-9]{20}\.png)', asset)
                if m:
                    h = m.group(1)
                    if h not in asset_info:
                        asset_info[h] = {'files': set(), 'alts': set(), 'captions': set(), 'titles': set()}
                    asset_info[h]['files'].add(fname)
                    if obj.get('alt'): asset_info[h]['alts'].add(obj['alt'])
                    if obj.get('caption'): asset_info[h]['captions'].add(obj['caption'])
                    if obj.get('title'): asset_info[h]['titles'].add(obj['title'])
            for k, v in obj.items():
                search_obj(v, context + "->" + k)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                search_obj(item, f"{context}[{i}]")
        elif isinstance(obj, str):
            for m in re.finditer(r'([a-f0-9]{20}\.png)', obj):
                h = m.group(1)
                if h not in asset_info:
                    asset_info[h] = {'files': set(), 'alts': set(), 'captions': set(), 'titles': set()}
                asset_info[h]['files'].add(fname)

    search_obj(data)

# Git modified files
git_mod = set([f.replace('public/content/figures/', '') for f in subprocess.check_output(['git', 'diff', '--name-only']).decode('utf-8').splitlines() if f.startswith('public/content/figures/')])

# Analyze each of the 141 meaningful visuals
results = []
for asset in sorted(meaningful_assets):
    path = os.path.join('public/content/figures', asset)
    im = Image.open(path)
    w, h = im.size
    rgb_im = im.convert('RGB')
    
    points = []
    for x in range(0, w, max(1, w // 20)):
        for y in range(0, h, max(1, h // 20)):
            points.append(rgb_im.getpixel((x, y)))
    c = Counter(points)
    has_f8fafc = (248, 250, 252) in c
    is_git_mod = asset in git_mod
    
    info = asset_info.get(asset, {'files': set(), 'alts': set(), 'captions': set(), 'titles': set()})
    files = sorted(list(info['files']))
    alt_text = next(iter(info['alts']), '') or next(iter(info['captions']), '') or next(iter(info['titles']), '')
    
    results.append({
        'asset': asset,
        'size': [w, h],
        'files': files,
        'alt': alt_text,
        'modern': has_f8fafc or is_git_mod,
        'git_mod': is_git_mod,
        'has_f8fafc': has_f8fafc
    })

print(f"Total meaningful visuals: {len(results)}")
modern_count = sum(1 for r in results if r['modern'])
remaining_count = len(results) - modern_count
print(f"Modern (Retina HD vector): {modern_count}")
print(f"Remaining to modernize: {remaining_count}")

# Group remaining by reading
from collections import defaultdict
by_reading = defaultdict(list)
for r in results:
    if not r['modern']:
        rd = r['files'][0] if r['files'] else 'unknown'
        by_reading[rd].append(r)

print("\n================ REMAINING SCANS BY READING ================")
for rd in sorted(by_reading.keys()):
    print(f"\n--- {rd} ({len(by_reading[rd])} figures) ---")
    for r in by_reading[rd]:
        print(f"  {r['asset']} ({r['size'][0]}x{r['size'][1]}): {r['alt'][:75]}")

with open('all_remaining_to_modernize.json', 'w', encoding='utf-8') as f:
    json.dump([r for r in results if not r['modern']], f, indent=2)
