import os
import re
from bs4 import BeautifulSoup
import html

results = []
for i in range(301, 401):
    fname = f"ref_raw/magic_page_{i:03d}.html"
    if not os.path.exists(fname):
        results.append(f"{i:03d}: NOT_FOUND")
        continue
    
    with open(fname, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, "html.parser")
    title = soup.title.string if soup.title else ""
    
    # Extract main content / h1, h2, h3
    h1_list = [h.get_text(strip=True) for h in soup.find_all("h1")]
    h2_list = [h.get_text(strip=True) for h in soup.find_all("h2")]
    h3_list = [h.get_text(strip=True) for h in soup.find_all("h3")]
    
    # find spell/content text
    # Seesaawiki usually puts page content inside div with id 'wiki-body' or 'content_block_2' or similar
    body = soup.find("div", id="wiki-body") or soup.find("div", class_="wiki-content") or soup
    
    # Get general summary text
    text_snippet = body.get_text(" ", strip=True)[:300]
    
    res = f"=== Page {i:03d} ===\nTitle: {title}\nH1: {h1_list}\nH2: {h2_list}\nH3: {h3_list}\nSnippet: {text_snippet}\n"
    results.append(res)

with open("scratch_301_400_summary.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print(f"Processed 301-400. Total entries: {len(results)}")
