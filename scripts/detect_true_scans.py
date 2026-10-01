import os
import json
from PIL import Image

with open('visual_usage_report.json', encoding='utf-8') as f:
    items = json.load(f)

true_scans = []
already_modern = []

for item in items:
    path = os.path.join('public/content/figures', item['asset'])
    if not os.path.exists(path):
        continue
    with Image.open(path) as im:
        w, h = im.size
        # Sample points in background:
        # Modern cards have #f8fafc: (248, 250, 252) at (w//2, 20) or (w//4, 20) or (50, 50)
        # Or pure #ffffff: (255, 255, 255)
        # Let's sample 10 points along the top border (y=15, x from w*0.2 to w*0.8)
        samples = [im.getpixel((int(w * frac), 15)) for frac in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]]
        rgb_samples = [s[:3] if isinstance(s, tuple) else (s, s, s) for s in samples]
        
        # Check if all samples are identically #f8fafc (248, 250, 252)
        is_f8fafc = all(s == (248, 250, 252) for s in rgb_samples)
        is_pure_white = all(s == (255, 255, 255) for s in rgb_samples)
        
        # Check bottom border as well
        bottom_samples = [im.getpixel((int(w * frac), h - 16)) for frac in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]]
        rgb_bottom = [s[:3] if isinstance(s, tuple) else (s, s, s) for s in bottom_samples]
        is_bottom_f8fafc = all(s == (248, 250, 252) for s in rgb_bottom)
        is_bottom_white = all(s == (255, 255, 255) for s in rgb_bottom)

        if (is_f8fafc and is_bottom_f8fafc) or (is_pure_white and is_bottom_white):
            # Check if it has modern style
            already_modern.append(item)
        else:
            true_scans.append(item)

print(f"Total: {len(items)}")
print(f"Already modern: {len(already_modern)}")
print(f"True scans: {len(true_scans)}")

with open('true_scans.json', 'w', encoding='utf-8') as f:
    json.dump(true_scans, f, indent=2)

with open('already_modern.json', 'w', encoding='utf-8') as f:
    json.dump(already_modern, f, indent=2)
