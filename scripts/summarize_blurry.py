import json

scans = json.load(open('blurry_scans.json', encoding='utf-8'))
print(f"Total scans to review: {len(scans)}")

# Let's list each with reading, asset, size, and alt
with open('blurry_scans_summary.txt', 'w', encoding='utf-8') as out:
    for i, s in enumerate(scans):
        reading = s['readings'][0] if s['readings'] else 'unknown'
        alt = s['alts'][0] if s['alts'] else 'No alt'
        out.write(f"[{i+1}] {reading} | {s['asset']} | {s['size'][0]}x{s['size'][1]} | {alt}\n")

print("Saved blurry_scans_summary.txt")
