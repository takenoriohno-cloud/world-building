# -*- coding: utf-8 -*-
import json

with open('scratch/spells_cache/fungus_spells_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for i in [0, 1, 10]:
    s = d[i]
    print(f"=== {s.get('japanese_name')} ===")
    lines = [l.strip() for l in s.get('detail_text', '').split('\n') if l.strip()]
    for l in lines[10:25]:
        print(" ", l)
