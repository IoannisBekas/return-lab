import json, sys
sys.stdout.reconfigure(encoding='utf-8')

targets = [
    ('058.json', '6b3f5a22c6fac9c014ac.png'),
    ('058.json', '540393c39595254c6f51.png'),
    ('059.json', '7a435d62f34d9005f653.png'),
    ('059.json', 'd1e38ef8eea046d0f3c7.png'),
    ('060.json', '37d4ab5a7d5be7fee01d.png'),
    ('062.json', '456f381c3049da9ce338.png'),
    ('063.json', '297803755043c81bcb67.png'),
    ('065.json', 'cc025233ef36a3f56ecd.png'),
]

for rf, target in targets:
    with open('public/content/readings/' + rf, encoding='utf-8') as f:
        d = json.load(f)
    blocks = d['modules'][0]['blocks']
    for idx, b in enumerate(blocks):
        if target in json.dumps(b):
            print(f'================ {target} in {rf} (Block {idx}) ================')
            print('ALT:', b.get('alt'))
            for j in range(max(0, idx - 2), min(len(blocks), idx + 3)):
                if j == idx:
                    continue
                bj = blocks[j]
                btype = bj.get('type')
                print(f'-- Block {j} ({btype}):')
                if 'text' in bj:
                    print(bj['text'][:400])
                elif 'html' in bj:
                    print(bj['html'][:400])
                elif 'content' in bj:
                    print(str(bj['content'])[:400])
                else:
                    print(str(bj)[:400])
