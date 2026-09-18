# -*- coding: utf-8 -*-
"""
Historical Timeline Harvester (1980 - 2026)
Optimized Single-Query per Year with Rate-Limiting & Exponential Backoff
"""

import urllib.request
import urllib.parse
import json
import ssl
import time
import re
import sys
import os

HEADERS = {
    "User-Agent": "WorldBuildingChronicleBot/1.0 (Academic & Creative World-Building Project; contact: agent@local.net)"
}

CTX = ssl.create_default_context()

def clean_wikitext(text):
    """Clean Wikipedia markup into readable plain text."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.DOTALL)
    text = re.sub(r"<ref[^/>]*/>", "", text)
    text = re.sub(r"</?ref[^>]*>", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    for _ in range(3):
        text = re.sub(r"\{\{仮リンク\|([^\|\}]+)(?:\|[^\}]*)?\}\}", r"\1", text)
        text = re.sub(r"\{\{lang\|[^\|]+\|([^\}]+)\}\}", r"\1", text)
        text = re.sub(r"\{\{[^\{\}]*\}\}", "", text)
    text = re.sub(r"\[\[(?:[^\|\]]+\|)?([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[https?://[^\s\]]+\s+([^\]]+)\]", r"\1", text)
    text = re.sub(r"\[https?://[^\s\]]+\]", "", text)
    text = re.sub(r"'{2,5}", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def fetch_year_page(year):
    """Fetch the full wikitext for a given year page with retry/backoff."""
    encoded_title = urllib.parse.quote(f"{year}年")
    url = f"https://ja.wikipedia.org/w/api.php?action=parse&page={encoded_title}&prop=wikitext&format=json"

    max_retries = 3
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if "parse" in data and "wikitext" in data["parse"]:
                    return data["parse"]["wikitext"].get("*", "")
                return ""
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_sec = 6 * (attempt + 1)
                print(f" [Rate-Limited 429: waiting {wait_sec}s...]", end="", flush=True)
                time.sleep(wait_sec)
            else:
                print(f" [HTTP {e.code}]", end="", flush=True)
                time.sleep(2)
        except Exception as ex:
            print(f" [Error: {ex}]", end="", flush=True)
            time.sleep(2)

    return ""

def extract_events_from_full_wikitext(year, full_text):
    """Extract and parse events section from full page wikitext."""
    events = []
    if not full_text:
        return events

    # Find == できごと == or == 出来事 == until the next level-2 header == ... ==
    event_section_match = re.search(r"==\s*(?:できごと|出来事)\s*==\s*\n(.*?)(?=\n==\s*[^=\n]+\s*==|\Z)", full_text, flags=re.DOTALL)
    if not event_section_match:
        # Fallback for pages with slight variations
        event_section_match = re.search(r"==+\s*(?:できごと|出来事)\s*==+(.*?)(?=\n==\s*[^=\n]+\s*==|\Z)", full_text, flags=re.DOTALL)
    
    if event_section_match:
        event_body = event_section_match.group(1)
    else:
        event_body = full_text

    lines = event_body.split("\n")
    current_month = None

    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue

        # Check for month subheaders like === 1月 === or === 10月 ===
        sub_m = re.match(r"^=+\s*(\d{1,2})月\s*=+", line_s)
        if sub_m:
            current_month = int(sub_m.group(1))
            continue

        # Check for bullet points
        if not line_s.startswith("*"):
            continue

        raw_content = re.sub(r"^\*+\s*", "", line_s)
        cleaned = clean_wikitext(raw_content)
        if not cleaned or len(cleaned) < 5:
            continue

        # Date pattern check: 1月1日 - ... or 15日 - ...
        date_match = re.match(r"^(\d{1,2}月(?:\d{1,2}日)?|\d{1,2}日)\s*[-–:：]\s*(.*)$", cleaned)
        if date_match:
            date_str = date_match.group(1)
            event_text = date_match.group(2).strip()

            m_in_date = re.search(r"(\d{1,2})月", date_str)
            d_in_date = re.search(r"(\d{1,2})日", date_str)

            month_val = int(m_in_date.group(1)) if m_in_date else current_month
            day_val = int(d_in_date.group(1)) if d_in_date else None

            # Standardize date_str
            if month_val and day_val:
                full_date_str = f"{month_val}月{day_val}日"
            elif month_val:
                full_date_str = f"{month_val}月"
            else:
                full_date_str = date_str
        else:
            if current_month:
                full_date_str = f"{current_month}月"
                month_val = current_month
            else:
                full_date_str = ""
                month_val = None
            day_val = None
            event_text = cleaned

        events.append({
            "year": year,
            "month": month_val,
            "day": day_val,
            "date_str": full_date_str,
            "text": event_text
        })

    return events

def run_harvest(start_year=1980, end_year=2026):
    print("==================================================================")
    print(f"  Historical Timeline Harvester: {start_year} - {end_year} (Single-Query Mode)")
    print("==================================================================")

    all_timeline = {}
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    for year in range(start_year, end_year + 1):
        print(f"Processing {year}年...", end="", flush=True)
        wikitext = fetch_year_page(year)
        evs = extract_events_from_full_wikitext(year, wikitext)
        print(f" [OK: {len(evs)} events]")
        all_timeline[year] = evs
        time.sleep(1.2) # Polite request interval

    # Export JSON
    json_path = os.path.join(base_dir, "world", "history", "raw_timeline_1980_2026.json")
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_timeline, f, ensure_ascii=False, indent=2)
    print(f"\n[EXPORTED] JSON DB: {json_path}")

    # Export Markdown
    md_path = os.path.join(base_dir, "world", "history", "chronology_1980_2026.md")
    total_events = sum(len(v) for v in all_timeline.values())
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 現代史・世界史クロニクル（1980年〜2026年）と魔力覚醒地球への架橋\n\n")
        f.write("> **策定・編纂**: 歴史・社会制度考証部（V・シュルツ 特命調査員）\n")
        f.write("> **データソース**: Wikipedia 日本語版 年別歴史クロニクル（MediaWiki API公式抽出）\n")
        f.write("> **期間**: 1980年（マナ覚醒前史）〜 2000年（ミレニアム・アウェイクニング）〜 2026年（現代）\n\n")
        f.write("---\n\n")
        f.write(f"## 総合統計\n- 収録年数: {len(all_timeline)} 年間（{start_year}〜{end_year}年）\n- 総収録歴史イベント数: {total_events} 件\n\n")
        f.write("---\n\n")

        for year in sorted(all_timeline.keys()):
            evs = all_timeline[year]
            if year < 1990:
                era = "【冷戦末期・マナ休眠期】"
            elif year < 2000:
                era = "【世紀末・マナ噴出前兆期】"
            elif year == 2000:
                era = "★【西暦2000年 ミレニアム・アウェイクニング（マナ大覚醒）】"
            elif year < 2010:
                era = "【第一次魔獣災害・多層防衛壁構築期】"
            elif year < 2020:
                era = "【メガコーポ台頭・新人類法制度確立期】"
            else:
                era = "【現代魔境・電脳魔術黎明期】"

            f.write(f"## {year}年 {era}\n\n")
            f.write(f"- **現実の主要記録事象**: {len(evs)} 件\n\n")
            f.write("### 🏛️ ヴォルフガング・シュルツの魔力覚醒地球 架橋考証メモ\n")
            if year == 2000:
                f.write("> **【世界史分岐点】2000年1月1日 午前0時00分**: 現実のY2K（2000年問題）の裏で、地球規模の霊的マナ噴出（ミレニアム・アウェイクニング）が発生。既存生物の突然変異、新人類（メタヒューマン）の誕生、世界4大アビス特異点の開口が同時に発生した。\n\n")
            elif year < 2000:
                f.write(f"> *マナ希薄期。古代種の休眠、一部霊的特異点の局所前兆、米ソ冷戦およびバブル経済下の超常機関（後のメガコーポ前身）による極秘調査網。*\n\n")
            else:
                f.write(f"> *覚醒後第{year - 2000}年。現実の政治動向・災害・技術発展に対応する、多層同心円防衛網の拡張、魔導特許紛争、Class-A/B/C管理制度の進展。*\n\n")

            f.write("### 主要出来事タイムライン\n\n")
            if not evs:
                f.write("*（該当年の出来事記録なし、または要編纂）*\n\n")
            else:
                for item in evs:
                    d = item.get("date_str", "")
                    t = item.get("text", "")
                    if d:
                        f.write(f"- **{d}**: {t}\n")
                    else:
                        f.write(f"- {t}\n")
            f.write("\n---\n\n")

    print(f"[EXPORTED] Markdown Chronology: {md_path}")
    print(f"\n[DONE] Total {total_events} events harvested across {len(all_timeline)} years.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Harvest historical timeline from ja.wikipedia.org")
    parser.add_argument("--start", type=int, default=1980, help="Start year")
    parser.add_argument("--end", type=int, default=2026, help="End year")
    args = parser.parse_args()
    run_harvest(args.start, args.end)
