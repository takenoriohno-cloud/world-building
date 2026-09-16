# -*- coding: utf-8 -*-
"""
Batch Spells Scraper and Markdown Generator for GURPS Magic Archive
Processes all 23 spell colleges from seesaawiki (EUC-JP) and generates high-spec Markdown archives.
"""

import urllib.request
import urllib.parse
import re
import json
import time
import os
from html.parser import HTMLParser

BASE_URL = "https://seesaawiki.jp"

COLLEGES = [
    {
        "id": "technological",
        "name_jp": "技術系呪文",
        "name_en": "Technological Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%b5%bb%bd%d1%b7%cf%bc%f6%ca%b8",
        "file": "technological.md",
        "chapter": "第6章",
        "pages": "pp.39-45"
    },
    {
        "id": "illusion",
        "name_jp": "幻覚・作成系呪文",
        "name_en": "Illusion and Creation Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%b8%b8%b3%d0%a1%a6%ba%ee%c0%ae%b7%cf%bc%f6%ca%b8",
        "file": "illusion.md",
        "chapter": "第7章",
        "pages": "pp.46-49"
    },
    {
        "id": "meta",
        "name_jp": "呪文操作系呪文",
        "name_en": "Meta-Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%bc%f6%ca%b8%c1%e0%ba%ee%b7%cf%bc%f6%ca%b8",
        "file": "meta.md",
        "chapter": "第8章",
        "pages": "pp.50-55"
    },
    {
        "id": "communication",
        "name_jp": "情報伝達系呪文",
        "name_en": "Communication and Empathy Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%be%f0%ca%f3%c5%c1%c3%a3%b7%cf%bc%f6%ca%b8",
        "file": "communication.md",
        "chapter": "第9章",
        "pages": "pp.56-60"
    },
    {
        "id": "plant",
        "name_jp": "植物系呪文",
        "name_en": "Plant Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%bf%a2%ca%aa%b7%cf%bc%f6%ca%b8",
        "file": "plant_and_fungal.md",
        "chapter": "第10章",
        "pages": "pp.61-64"
    },
    {
        "id": "food",
        "name_jp": "食料系呪文",
        "name_en": "Food Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%bf%a9%ce%c1%b7%cf%bc%f6%ca%b8",
        "file": "food.md",
        "chapter": "第11章",
        "pages": "pp.65-68"
    },
    {
        "id": "necromantic",
        "name_jp": "死霊系呪文",
        "name_en": "Necromantic Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%bb%e0%ce%ee%b7%cf%bc%f6%ca%b8",
        "file": "necromantic.md",
        "chapter": "第12章",
        "pages": "pp.69-76"
    },
    {
        "id": "water",
        "name_jp": "水霊系呪文",
        "name_en": "Water Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%bf%e5%ce%ee%b7%cf%bc%f6%ca%b8",
        "file": "water.md",
        "chapter": "第13章",
        "pages": "pp.77-83"
    },
    {
        "id": "mind",
        "name_jp": "精神操作系呪文",
        "name_en": "Mind Control Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%c0%ba%bf%c0%c1%e0%ba%ee%b7%cf%bc%f6%ca%b8",
        "file": "mind.md",
        "chapter": "第14章",
        "pages": "pp.84-91"
    },
    {
        "id": "knowledge",
        "name_jp": "知識系呪文",
        "name_en": "Knowledge Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%c3%ce%bc%b1%b7%cf%bc%f6%ca%b8",
        "file": "knowledge.md",
        "chapter": "第15章",
        "pages": "pp.92-97"
    },
    {
        "id": "healing",
        "name_jp": "治癒系呪文",
        "name_en": "Healing Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%bc%a3%cc%fe%b7%cf%bc%f6%ca%b8",
        "file": "healing.md",
        "chapter": "第16章",
        "pages": "pp.98-103"
    },
    {
        "id": "earth",
        "name_jp": "地霊系呪文",
        "name_en": "Earth Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%c3%cf%ce%ee%b7%cf%bc%f6%ca%b8",
        "file": "earth.md",
        "chapter": "第17章",
        "pages": "pp.104-109"
    },
    {
        "id": "weather",
        "name_jp": "天候系呪文",
        "name_en": "Weather Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%c5%b7%b8%f5%b7%cf%bc%f6%ca%b8",
        "file": "weather.md",
        "chapter": "第18章",
        "pages": "pp.110-115"
    },
    {
        "id": "gate",
        "name_jp": "転送系呪文",
        "name_en": "Gate Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%c5%be%c1%f7%b7%cf%bc%f6%ca%b8",
        "file": "gate.md",
        "chapter": "第19章",
        "pages": "pp.116-121"
    },
    {
        "id": "animal",
        "name_jp": "動物系呪文",
        "name_en": "Animal Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%c6%b0%ca%aa%b7%cf%bc%f6%ca%b8",
        "file": "animal.md",
        "chapter": "第20章",
        "pages": "pp.122-126"
    },
    {
        "id": "body_control",
        "name_jp": "肉体操作系呪文",
        "name_en": "Body Control Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%c6%f9%c2%ce%c1%e0%ba%ee%b7%cf%bc%f6%ca%b8",
        "file": "body_control.md",
        "chapter": "第21章",
        "pages": "pp.127-135"
    },
    {
        "id": "light_darkness",
        "name_jp": "光・闇系呪文",
        "name_en": "Light and Darkness Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%b8%f7%a1%a6%b0%c7%b7%cf%bc%f6%ca%b8",
        "file": "light_darkness.md",
        "chapter": "第22章",
        "pages": "pp.136-141"
    },
    {
        "id": "air",
        "name_jp": "風霊系呪文",
        "name_en": "Air Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%c9%f7%ce%ee%b7%cf%bc%f6%ca%b8",
        "file": "air.md",
        "chapter": "第23章",
        "pages": "pp.142-147"
    },
    {
        "id": "making_breaking",
        "name_jp": "物体操作系呪文",
        "name_en": "Making and Breaking Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%ca%aa%c2%ce%c1%e0%ba%ee%b7%cf%bc%f6%ca%b8",
        "file": "making_breaking.md",
        "chapter": "第24章",
        "pages": "pp.148-154"
    },
    {
        "id": "protection",
        "name_jp": "防御・警戒系呪文",
        "name_en": "Protection and Warning Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%cb%c9%b8%e6%a1%a6%b7%d9%b2%fc%b7%cf%bc%f6%ca%b8",
        "file": "protection.md",
        "chapter": "第25章",
        "pages": "pp.155-161"
    },
    {
        "id": "enchantment",
        "name_jp": "魔化系呪文",
        "name_en": "Enchantment Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%cb%e2%b2%bd%b7%cf%bc%f6%ca%b8",
        "file": "enchantment_spells.md",
        "chapter": "第26章",
        "pages": "pp.162-171"
    },
    {
        "id": "poison",
        "name_jp": "毒系呪文",
        "name_en": "Poison Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%c6%c7%b7%cf%bc%f6%ca%b8",
        "file": "toxic_and_poison.md",
        "chapter": "拡張サプリメント",
        "pages": "Pyramid 4/1"
    },
    {
        "id": "fungus",
        "name_jp": "菌類系呪文",
        "name_en": "Fungus Spells",
        "url": "https://seesaawiki.jp/mokugyo/d/%b6%dd%ce%e0%b7%cf%bc%f6%ca%b8",
        "file": "plant_and_fungal.md", # Appends/integrates with plant
        "chapter": "拡張サプリメント",
        "pages": "GURPS Magic: Plant Spells"
    }
]

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

def clean_body_text(text):
    if not text:
        return ""
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        if any(m in line_str for m in ["Menu", "MenuBar", "コメントをかく", "利用規約", "魔法関連参照用", "ルールブック『", "第1章「"]):
            break
        if any(m in line_str for m in ["GURPSよろず", "汎用TRPG", "トップページ ページ一覧", "最終更新：", "Tweet"]):
            continue
        cleaned.append(line_str)
    return "\n".join(cleaned).strip()

def extract_effect_summary(text):
    body = clean_body_text(text)
    # Search for text after brackets like 《[[...]]》 or 《[...]》 or 《...》
    m = re.search(r'《\[*.*?\]*》\s*(.*?)(?:呪文の解説|エネルギー消費|持続時間|前提条件|準備時間|$)', body, re.DOTALL)
    if m:
        summary = m.group(1).strip()
        summary = re.sub(r'\s+', ' ', summary)
        # Strip out redundant headers like (Spell Name) MxxP ■《...》 etc.
        summary = re.sub(r'^(?:（[A-Za-z0-9\s\-_’\']+）|[A-Za-z0-9\s\-_’\']+|M\d+(?:-\d+)?P|■|《[^》]+》|通常呪文|範囲呪文|射撃呪文|防御呪文|情報呪文|白兵呪文|抵抗呪文|特殊呪文|基本呪文|[0-9A-Za-z\s、・]+)+\s*', '', summary)
        if len(summary) > 10 and not any(k in summary for k in ["tyounekogami", "最終更新", "Tweet", "参照"]):
            return summary[:200]
            
    lines = [l for l in body.split("\n") if len(l) > 10 and not any(k in l for k in ["■", "《", "tyounekogami", "最終更新", "Tweet", "参照", "M3", "M4", "M5", "M1", "M2"])]
    if lines:
        clean_l = lines[0].strip()
        clean_l = re.sub(r'^(?:（[A-Za-z0-9\s\-_’\']+）|M\d+(?:-\d+)?P|■|《[^》]+》|[0-9A-Za-z\s、・]+)+\s*', '', clean_l)
        return clean_l[:200]
    return "詳細参照"

def format_spell_row(s):
    eng = s.get('english_name', '').strip()
    jp = s.get('japanese_name', '').strip()
    s_class = s.get('spell_class', '').strip()
    duration = s.get('duration', '-').strip()
    cost = s.get('cost', '-').strip().replace('■', '')
    casting_time = s.get('casting_time', '-').strip()
    prereqs = s.get('prerequisites', '-').strip()
    summary = extract_effect_summary(s.get('detail_text', ''))
    
    jp = re.sub(r'†', '', jp)
    if '旧名：' in jp:
        parts = jp.split('旧名：')
        main_name = re.sub(r'[《》*（）]', '', parts[0]).strip()
        old_name = parts[1].strip()
        is_star = '*' in parts[0] or '*' in eng
        star_str = "*" if is_star else ""
        jp_display = f"**《{main_name}{star_str}》**<br>（旧名：{old_name}）<br>{eng}"
    elif '（並）' in jp:
        main_name = re.sub(r'[《》*（）並]', '', jp).strip()
        jp_display = f"**《{main_name}》（並）**<br>{eng}"
    else:
        main_name = re.sub(r'[《》*（）]', '', jp).strip()
        is_star = '*' in jp or '*' in eng
        star_str = "*" if is_star else ""
        jp_display = f"**《{main_name}{star_str}》**<br>{eng}"
        
    return f"| {jp_display} | {s_class} | {duration} | {cost} | {casting_time} | {prereqs} | {summary} |"

def process_college(college_info, cache_dir):
    cid = college_info["id"]
    print(f"\n=======================================================")
    print(f"Processing College: {college_info['name_jp']} ({college_info['name_en']})")
    print(f"URL: {college_info['url']}")
    print(f"=======================================================")
    
    cache_json = os.path.join(cache_dir, f"{cid}_spells_data.json")
    spells = []
    
    # Check cache first
    if os.path.exists(cache_json):
        try:
            with open(cache_json, "r", encoding="utf-8") as f:
                spells = json.load(f)
            print(f"Loaded {len(spells)} spells from cache: {cache_json}")
        except Exception:
            spells = []
            
    if not spells:
        index_html = fetch_page(college_info["url"])
        parser = TableParser()
        parser.feed(index_html)
        
        for t_idx, table in enumerate(parser.tables):
            if not table or len(table) < 2:
                continue
            headers_row = [c[0] for c in table[0]]
            if not any(k in headers_row for k in ["原書名", "呪文名", "呪文クラス"]):
                continue
                
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
                
        print(f"Found {len(spells)} spells in index. Fetching details...")
        for idx, s in enumerate(spells):
            print(f"  [{idx+1}/{len(spells)}] Fetching: {s['japanese_name']} ({s['english_name']})...")
            if s['detail_url']:
                try:
                    d_html = fetch_page(s['detail_url'])
                    s['detail_text'] = parse_spell_detail(d_html)
                except Exception as e:
                    s['detail_text'] = f"Fetch error: {e}"
            else:
                s['detail_text'] = "No detail URL"
            time.sleep(0.3)
            
        with open(cache_json, "w", encoding="utf-8") as f:
            json.dump(spells, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(spells)} spells to cache: {cache_json}")

    return spells

def main():
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../scratch/spells_cache")
    os.makedirs(cache_dir, exist_ok=True)
    
    summary_results = []
    
    for c in COLLEGES:
        try:
            spells = process_college(c, cache_dir)
            summary_results.append((c["name_jp"], len(spells), c["file"]))
        except Exception as e:
            print(f"[ERROR] Failed processing {c['name_jp']}: {e}")
            summary_results.append((c["name_jp"], f"Error: {e}", c["file"]))
            
    print("\n\n=======================================================")
    print("ALL COLLEGES PROCESSED SUMMARY:")
    for name, count, target_file in summary_results:
        print(f" - {name}: {count} spells -> {target_file}")
    print("=======================================================")

if __name__ == "__main__":
    main()
