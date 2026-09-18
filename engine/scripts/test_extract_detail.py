# -*- coding: utf-8 -*-
import json
import re

with open("scratch/movement_spells_data.json", "r", encoding="utf-8") as f:
    spells = json.load(f)

print(f"Total spells: {len(spells)}")

for s in spells[:5]:
    text = s.get("detail_text", "")
    # Find lines before "Menu" or "MenuBar"
    clean_lines = []
    for line in text.split("\n"):
        line_s = line.strip()
        if any(marker in line_s for marker in ["Menu", "MenuBar", "コメントをかく", "利用規約"]):
            break
        clean_lines.append(line_s)
    
    body = "\n".join(clean_lines).strip()
    print(f"\n==========================================")
    print(f"SPELL: {s['japanese_name']} ({s['english_name']}) - {s['spell_class']}")
    print(f"DURATION: {s['duration']} | COST: {s['cost']} | TIME: {s['casting_time']}")
    print(f"PREREQS: {s['prerequisites']}")
    print(f"BODY:\n{body[:600]}...")

