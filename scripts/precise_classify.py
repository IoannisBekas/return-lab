import json, os, sys
from PIL import Image
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

with open('visual_usage_report.json', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total visual items: {len(items)}")

categories = {
    'modern_f8fafc': [],
    'clean_white_vector': [],
    'blurry_raster_scan': []
}

for item in items:
    path = os.path.join('public/content/figures', item['asset'])
    if not os.path.exists(path):
        continue
    im = Image.open(path).convert('RGB')
    w, h = im.size
    arr = np.array(im)
    
    # 1. f8fafc ratio
    f8fafc_count = np.sum((arr[:, :, 0] == 248) & (arr[:, :, 1] == 250) & (arr[:, :, 2] == 252))
    f8fafc_ratio = f8fafc_count / (w * h)
    
    # 2. pure white ratio
    white_count = np.sum((arr[:, :, 0] == 255) & (arr[:, :, 1] == 255) & (arr[:, :, 2] == 255))
    white_ratio = white_count / (w * h)
    
    # 3. near white noise: pixels with 230 <= channel <= 254
    near_white_mask = (arr[:, :, 0] >= 230) & (arr[:, :, 0] < 255) & (arr[:, :, 1] >= 230) & (arr[:, :, 1] < 255) & (arr[:, :, 2] >= 230) & (arr[:, :, 2] < 255)
    near_white_count = np.sum(near_white_mask)
    near_white_ratio = near_white_count / (w * h)
    
    # 4. total unique colors
    # Downsample to speed up unique color count
    small = im.resize((w // 4, h // 4))
    unq_colors = len(set(small.getdata()))
    
    rd = item['readings'][0] if item['readings'] else 'unknown'
    alt = item['alts'][0] if item['alts'] else ''

    if f8fafc_ratio > 0.25:
        categories['modern_f8fafc'].append((item, f8fafc_ratio))
    elif white_ratio > 0.40 and near_white_ratio < 0.05:
        # Very clean vector on white background (like af267f54944c49376754)
        categories['clean_white_vector'].append((item, white_ratio, near_white_ratio))
    else:
        categories['blurry_raster_scan'].append((item, white_ratio, near_white_ratio, unq_colors))

print(f"Modern #f8fafc cards: {len(categories['modern_f8fafc'])}")
print(f"Clean white vector: {len(categories['clean_white_vector'])}")
print(f"Blurry raster scans: {len(categories['blurry_raster_scan'])}")

print("\n--- BLURRY RASTER SCANS TO UPGRADE ---")
for item, wr, nwr, uc in categories['blurry_raster_scan']:
    rd = item['readings'][0] if item['readings'] else 'unknown'
    alt = item['alts'][0] if item['alts'] else ''
    print(f"  {item['asset']} ({item['actual_size'][0]}x{item['actual_size'][1]}, near_white={nwr*100:.1f}%) in {rd} - {alt[:60]}")

with open('scans_to_upgrade.json', 'w', encoding='utf-8') as out:
    json.dump([item for item, _, _, _ in categories['blurry_raster_scan']], out, indent=2)
