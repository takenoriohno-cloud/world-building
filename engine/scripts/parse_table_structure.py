# -*- coding: utf-8 -*-
import urllib.request
import re
from html.parser import HTMLParser

url = "https://seesaawiki.jp/mokugyo/d/%b0%dc%c6%b0%b7%cf%bc%f6%ca%b8"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req, timeout=15) as response:
    html = response.read().decode('euc-jp', errors='replace')

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

parser = TableParser()
parser.feed(html)

print(f"Total tables: {len(parser.tables)}")
for idx, tbl in enumerate(parser.tables):
    print(f"\n=== Table {idx}: {len(tbl)} rows ===")
    for r_idx, row in enumerate(tbl[:5]):
        row_str = " | ".join([c[0] for c in row])
        print(f"Row {r_idx}: {row_str[:120]}")

