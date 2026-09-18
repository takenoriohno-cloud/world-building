# -*- coding: utf-8 -*-
"""
Polishing script to clean up table effect summaries in all world/magic/spells/*.md files.
Removes wiki noise like 《[[...]]》, "情報伝達系呪文 01", "通常呪文 /", "MxxP", "■" etc.
"""

import os
import re

SPELLS_DIR = "world/magic/spells"

def polish_summary(cell):
    # Remove 《[[...]]》 and variants
    cell = re.sub(r'《\[*.*?\]*》', '', cell)
    # Remove redundant college prefixes like "情報伝達系呪文 01", "火霊系呪文 05"
    cell = re.sub(r'(?:[一-龥ぁ-んァ-ヶ]+系呪文\s*\d*|[一-龥]+呪文|基本呪文|特定[一-龥]+系呪文|抵抗呪文[_\s一-龥・]+|通常呪文|範囲呪文|射撃呪文|防御呪文|情報呪文|白兵呪文|特殊呪文)[、・\s/]*', '', cell)
    # Remove (Spell Name) MxxP ■
    cell = re.sub(r'（[A-Za-z0-9\s\-_’\']+）', '', cell)
    cell = re.sub(r'M\d+(?:-\d+)?P', '', cell)
    cell = re.sub(r'[■◆]', '', cell)
    # Remove leading punctuation
    cell = re.sub(r'^[、・\s/，]+', '', cell)
    cell = re.sub(r'\s+', ' ', cell).strip()
    return cell

def clean_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        if line.startswith("|") and not line.startswith("| :---") and not line.startswith("| 呪文名"):
            parts = line.split("|")
            if len(parts) >= 8:
                # Column 7 (index 7 in parts, since parts[0] is empty before leading |) is effect summary
                raw_summary = parts[7]
                polished = polish_summary(raw_summary)
                if not polished or len(polished) < 5:
                    polished = "詳細参照"
                parts[7] = f" {polished} "
                new_line = "|".join(parts)
                new_lines.append(new_line)
                continue
        new_lines.append(line)
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

for fname in os.listdir(SPELLS_DIR):
    if fname.endswith(".md"):
        clean_file(os.path.join(SPELLS_DIR, fname))

print("All spell files polished successfully.")
