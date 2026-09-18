# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
import sys
import time

url = "https://seesaawiki.jp/mokugyo/d/%b0%dc%c6%b0%b7%cf%bc%f6%ca%b8"

req = urllib.request.Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

try:
    with urllib.request.urlopen(req, timeout=15) as response:
        content_bytes = response.read()
        html = content_bytes.decode('euc-jp', errors='replace')
        print(f"Successfully fetched {len(html)} chars from {url}")
        
        # Look for links in the wiki content area
        # Links usually match <a href="https://seesaawiki.jp/mokugyo/d/..." ...>
        links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.IGNORECASE | re.DOTALL)
        print(f"Total links found: {len(links)}")
        
        # Filter links related to spells
        spell_links = []
        for href, text in links:
            clean_text = re.sub(r'<.*?>', '', text).strip()
            if "/mokugyo/d/" in href and href != url:
                # exclude common navigation links
                if clean_text and not any(k in clean_text for k in ["トップページ", "MenuBar", "最近更新", "ヘルプ", "検索", "Wiki"]):
                    spell_links.append((href, clean_text))
        
        print(f"Candidate spell links: {len(spell_links)}")
        for h, t in spell_links[:30]:
            print(f"  {t} -> {h}")

except Exception as e:
    print(f"Error: {e}")
