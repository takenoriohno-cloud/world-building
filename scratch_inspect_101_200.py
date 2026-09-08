import os, glob, re
from bs4 import BeautifulSoup

target_files = []
for i in range(101, 201):
    path = f"ref_raw/magic_page_{i:03d}.html"
    if os.path.exists(path):
        target_files.append((i, path))

print(f"Found {len(target_files)} target files.")

results = []
for idx, path in target_files:
    try:
        with open(path, "r", encoding="shift_jis", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
    soup = BeautifulSoup(content, "html.parser")
    title = soup.title.string.strip() if soup.title else "No Title"
    h1 = soup.find(["h1", "h2", "h3"])
    h1_text = h1.get_text().strip() if h1 else ""
    results.append(f"Page {idx:03d}: Title='{title}' | H1='{h1_text}'")

with open("scratch_pages_101_200.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(results))

print("Saved summary to scratch_pages_101_200.txt")
