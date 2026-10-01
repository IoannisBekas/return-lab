import os
import json
from PIL import Image, ImageStat
import numpy as np

with open('visual_usage_report.json', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total visual items: {len(items)}")

scans = []
vector_upgraded = []

for item in items:
    path = os.path.join('public/content/figures', item['asset'])
    if not os.path.exists(path):
        continue
    
    with Image.open(path) as im:
        w, h = im.size
        # Sample corners
        corners = [
            im.getpixel((5, 5)),
            im.getpixel((w - 6, 5)),
            im.getpixel((5, h - 6)),
            im.getpixel((w - 6, h - 6))
        ]
        # Check if RGBA/RGB
        rgb_corners = [c[:3] if isinstance(c, tuple) else (c, c, c) for c in corners]
        
        # Check background uniformity in a 20x20 patch at (50, 50) or (10, 10)
        patch = im.crop((10, 10, 40, 40)).convert('RGB')
        stat = ImageStat.Stat(patch)
        var = sum(stat.var)
        
        # Also check unique colors in patch
        colors = len(set(patch.getdata()))

        # Check if modern vector: corner is usually (248, 250, 252) which is #f8fafc or pure white (255, 255, 255)
        # and background patch has variance ~ 0 (1 unique color)
        is_modern = (var < 2.0 and colors <= 2) and (rgb_corners[0] in [(248, 250, 252), (255, 255, 255), (255, 255, 255, 255)])
        
        item_info = {
            'asset': item['asset'],
            'size': (w, h),
            'corner': rgb_corners[0],
            'patch_var': var,
            'patch_colors': colors,
            'readings': item['readings'],
            'alts': item['alts']
        }
        
        if is_modern:
            vector_upgraded.append(item_info)
        else:
            scans.append(item_info)

print(f"Already upgraded modern vector style: {len(vector_upgraded)}")
print(f"Scans / blurry / non-upgraded: {len(scans)}")

with open('blurry_scans.json', 'w', encoding='utf-8') as f:
    json.dump(scans, f, indent=2)

with open('upgraded_visuals.json', 'w', encoding='utf-8') as f:
    json.dump(vector_upgraded, f, indent=2)
