import json, os, sys
from PIL import Image
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

with open('blurry_scans.json', encoding='utf-8') as f:
    scans = json.load(f)

print(f"Checking {len(scans)} candidates...")

true_blurry = []
already_clean = []

for s in scans:
    path = os.path.join('public/content/figures', s['asset'])
    im = Image.open(path).convert('RGB')
    arr = np.array(im)
    # Check background: white or near white pixels (> 240 in all channels)
    mask = (arr[:, :, 0] > 240) & (arr[:, :, 1] > 240) & (arr[:, :, 2] > 240)
    bg_pixels = arr[mask]
    if len(bg_pixels) > 0:
        std_per_channel = np.std(bg_pixels, axis=0)
        max_std = np.max(std_per_channel)
        # Check unique colors in near-white region
        # If std is high or many noisy shades, it's scanned
        unique_colors_in_bg = len(np.unique(bg_pixels, axis=0))
        if max_std > 1.2 and unique_colors_in_bg > 30:
            true_blurry.append((s, max_std, unique_colors_in_bg))
        else:
            already_clean.append((s, max_std, unique_colors_in_bg))
    else:
        true_blurry.append((s, 999, 999))

print(f"Confirmed blurry scans: {len(true_blurry)}")
print(f"Clean vector/modern: {len(already_clean)}")

print("\n--- ALREADY CLEAN / VECTOR ---")
for s, std, unq in already_clean:
    rd = s['readings'][0] if s['readings'] else 'unknown'
    print(f"  {s['asset']} (std={std:.2f}, unq={unq}) in {rd}")

print("\n--- CONFIRMED BLURRY SCANS ---")
for s, std, unq in true_blurry:
    rd = s['readings'][0] if s['readings'] else 'unknown'
    alt = s['alts'][0] if s['alts'] else ''
    print(f"  {s['asset']} ({s['size'][0]}x{s['size'][1]}, std={std:.2f}) in {rd} - {alt[:60]}")

with open('confirmed_blurry.json', 'w', encoding='utf-8') as out:
    json.dump([s for s, _, _ in true_blurry], out, indent=2)
