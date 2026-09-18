# -*- coding: utf-8 -*-
import os
import re

spells_dir = "world/magic/spells"

for fname in os.listdir(spells_dir):
    if not fname.endswith(".md"):
        continue
    fpath = os.path.join(spells_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if there is classDef spell without color:
    # Example: classDef spell fill:#...,stroke:#...;
    def replacer(match):
        line = match.group(0)
        if "color:" in line:
            return line
        # Use high-contrast dark theme standard: fill:#0f172a,stroke:#38bdf8,stroke-width:1.5px,color:#ffffff;
        return "classDef spell fill:#0f172a,stroke:#38bdf8,stroke-width:1.5px,color:#ffffff;"

    new_content = re.sub(r'classDef\s+spell\s+[^;\n]+;', replacer, content)
    if new_content != content:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated high-contrast Mermaid in: {fname}")

print("All spell Mermaid diagrams standardized.")
