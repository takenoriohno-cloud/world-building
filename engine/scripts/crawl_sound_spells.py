# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
import json
import time
import os
from html.parser import HTMLParser

BASE_URL = "https://seesaawiki.jp"
INDEX_URL = "https://seesaawiki.jp/mokugyo/d/%b2%bb%c0%bc%b7%cf%bc%f6%ca%b8"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36'
}

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = []
        self.current_row = []
        self.current_cell = []
        self.current_links = []
        self.in_cell = False
        self.in_a = False
        self.current_href = ""
        self.current_link_text = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == 'table':
            self.current_table = []
        elif tag == 'tr':
            self.current_row = []
        elif tag in ('td', 'th'):
            self.in_cell = True
            self.current_cell = []
            self.current_links = []
        elif tag == 'a' and self.in_cell:
            self.in_a = True
            self.current_href = attr_dict.get('href', '')
            self.current_link_text = []

    def handle_endtag(self, tag):
        if tag == 'table':
            if self.current_table:
                self.tables.append(self.current_table)
            self.current_table = []
        elif tag == 'tr':
            if self.current_row:
                self.current_table.append(self.current_row)
            self.current_row = []
        elif tag in ('td', 'th'):
            self.in_cell = False
            cell_text = "".join(self.current_cell).strip()
            self.current_row.append((cell_text, list(self.current_links)))
            self.current_cell = []
            self.current_links = []
        elif tag == 'a' and self.in_cell:
            self.in_a = False
            link_text = "".join(self.current_link_text).strip()
            self.current_links.append((link_text, self.current_href))
            self.current_href = ""
            self.current_link_text = []

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell.append(data)
            if self.in_a:
                self.current_link_text.append(data)

def clean_html(text):
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    return text.strip()

def fetch_page(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        content_bytes = response.read()
        return content_bytes.decode('euc-jp', errors='replace')

def parse_spell_detail(html):
    m = re.search(r'<div[^>]+(?:id="content"|class="wiki-content")[^>]*>(.*?)<div[^>]+id="footer"', html, re.DOTALL | re.IGNORECASE)
    content_html = m.group(1) if m else html
    text = clean_html(content_html)
    return text

def main():
    print(f"Fetching index: {INDEX_URL}")
    index_html = fetch_page(INDEX_URL)
    
    parser = TableParser()
    parser.feed(index_html)
    
    spells = []
    print(f"Total tables found: {len(parser.tables)}")
    
    for t_idx, table in enumerate(parser.tables):
        if not table or len(table) < 2:
            continue
        
        headers_row = [c[0] for c in table[0]]
        # Check if this table is a spells table
        if not any(k in headers_row for k in ["原書名", "呪文名", "呪文クラス"]):
            continue
            
        print(f"Table {t_idx} (rows: {len(table)}) headers: {headers_row}")
        
        for row in table[1:]:
            cols = [c[0] for c in row]
            if len(cols) < 5:
                continue
            
            detail_url = ""
            for cell_text, links in row:
                for l_text, l_url in links:
                    if "/mokugyo/d/" in l_url:
                        if l_text == cols[1] or not detail_url:
                            detail_url = l_url
                            
            if detail_url and not detail_url.startswith("http"):
                detail_url = urllib.parse.urljoin(BASE_URL, detail_url)
                
            spell_info = {
                "english_name": cols[0] if len(cols) > 0 else "",
                "japanese_name": cols[1] if len(cols) > 1 else "",
                "spell_class": cols[2] if len(cols) > 2 else "",
                "college": cols[3] if len(cols) > 3 else "",
                "duration": cols[4] if len(cols) > 4 else "",
                "cost": cols[5] if len(cols) > 5 else "",
                "casting_time": cols[6] if len(cols) > 6 else "",
                "prerequisites": cols[7] if len(cols) > 7 else "",
                "detail_url": detail_url,
                "table_category": f"Table_{t_idx}"
            }
            spells.append(spell_info)

    print(f"Collected {len(spells)} sound spells from index.")
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../scratch")
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, "sound_spells_data.json")
    
    for idx, s in enumerate(spells):
        print(f"[{idx+1}/{len(spells)}] Fetching: {s['japanese_name']} ({s['english_name']})...")
        if s['detail_url']:
            try:
                detail_html = fetch_page(s['detail_url'])
                detail_text = parse_spell_detail(detail_html)
                s['detail_text'] = detail_text
            except Exception as e:
                print(f"  Error fetching {s['detail_url']}: {e}")
                s['detail_text'] = f"Fetch error: {e}"
        else:
            s['detail_text'] = "No detail URL available"
        
        time.sleep(0.35)
        
        if (idx + 1) % 10 == 0 or idx == len(spells) - 1:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(spells, f, ensure_ascii=False, indent=2)
            print(f"  Saved progress ({idx+1}/{len(spells)})")

    print(f"\nAll sound spells fetched! Saved to {json_path}")

if __name__ == "__main__":
    main()
