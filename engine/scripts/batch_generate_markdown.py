# -*- coding: utf-8 -*-
"""
Batch Markdown Generator for GURPS Magic Spell Colleges
Reads cached JSON data and regenerates world/magic/spells/*.md files with full tables,
clean descriptions, high-contrast Mermaid diagrams, and 2026 modern tactical/legal lore.
"""

import json
import os
import re

CACHE_DIR = "scratch/spells_cache"
TARGET_DIR = "world/magic/spells"

from batch_crawl_all_spells import COLLEGES, clean_body_text, extract_effect_summary, format_spell_row

def build_college_markdown(college_info, spells, existing_content):
    cid = college_info["id"]
    name_jp = college_info["name_jp"]
    name_en = college_info["name_en"]
    chapter = college_info["chapter"]
    pages = college_info["pages"]
    
    # Check if there are different tables
    tables = {}
    for s in spells:
        tcat = s.get("table_category", "Table_1")
        if tcat not in tables:
            tables[tcat] = []
        tables[tcat].append(s)
        
    md = []
    md.append(f"# {name_jp} ({name_en})")
    md.append("")
    md.append(f"本ドキュメントは、ガープス第4版『魔法大全』{chapter}（{pages}）および公式拡張サプリメント（『Magic: Artillery Spells』『Magic: Death Spells』『Magic: The Least of Spells』『Magic: Plant Spells』等）に準拠した、**全{len(spells)}種**の{name_jp}公式アーカイブです。マナ力学、生体媒介作用、ならびに2026年現代における結界都市防衛・軍事兵器工学・法規制（CR）の運用データを過不足なく完全網羅しています。")
    md.append("")
    md.append("---")
    md.append("")
    
    # Extract existing Mermaid tree or section 1 if present
    mermaid_block = ""
    if "```mermaid" in existing_content:
        m = re.search(r'```mermaid(.*?)```', existing_content, re.DOTALL)
        if m:
            raw_mermaid = m.group(1).strip()
            # Ensure high-contrast classDef
            if "classDef spell" in raw_mermaid:
                raw_mermaid = re.sub(r'classDef\s+spell\s+[^;\n]+;', 'classDef spell fill:#0f172a,stroke:#38bdf8,stroke-width:1.5px,color:#ffffff;', raw_mermaid)
            else:
                raw_mermaid = "    classDef spell fill:#0f172a,stroke:#38bdf8,stroke-width:1.5px,color:#ffffff;\n" + raw_mermaid
            mermaid_block = f"```mermaid\n{raw_mermaid}\n```"

    md.append(f"## 1. {name_jp}の力学体系")
    md.append("")
    md.append(f"{name_jp}は、マナの指向性周波数を介して対象の物理・生体・霊的パラメータを励起・変調・制御する魔術体系です。")
    md.append("- **生体媒介原則**: マナは術士の生体・神経系・霊体を介して作用し、直接の物質変換や物理エネルギー励起を行います。")
    md.append("- **現代技術インフラとの並行性**: 電子回路や通信網を直接破壊するのではなく、物理的現象（熱、圧力、電磁、物質変形等）を介して現代兵器や都市防護壁と相互作用します。")
    md.append("")
    if mermaid_block:
        md.append(f"### 1.1 主要{name_jp} 前提条件ツリー (Prerequisite Tree)")
        md.append("")
        md.append(mermaid_block)
        md.append("")
        
    md.append("---")
    md.append("")
    
    # Output tables
    table_keys = sorted(tables.keys())
    for idx, tkey in enumerate(table_keys):
        t_spells = tables[tkey]
        if idx == 0:
            md.append(f"## 2. ガープス第4版『魔法大全』基本{name_jp}（{len(t_spells)}種）")
        elif any("MAS" in str(s.get("detail_text", "")) or "Artillery" in str(s.get("detail_text", "")) for s in t_spells) or any("Death" in str(s.get("detail_text", "")) for s in t_spells):
            md.append(f"## {idx+2}. 魔導兵器・砲兵戦術拡張呪文（MAS / MDS 拡張 {len(t_spells)}種）")
        elif any("Least" in str(s.get("detail_text", "")) or "（並）" in s.get("japanese_name", "") for s in t_spells):
            md.append(f"## {idx+2}. 日常・民間簡単呪文（The Least of Spells 拡張 {len(t_spells)}種）")
        else:
            md.append(f"## {idx+2}. {name_jp} 追加・関連拡張呪文（{len(t_spells)}種）")
            
        md.append("")
        md.append("| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |")
        md.append("| :--- | :---: | :---: | :---: | :---: | :--- | :--- |")
        for s in t_spells:
            md.append(format_spell_row(s))
        md.append("")
        md.append("---")
        md.append("")

    # Modern Tactical / Lore section
    sec_num = len(table_keys) + 2
    md.append(f"## {sec_num}. 2026年現代戦術・都市防衛・法規制（CR）における運用")
    md.append("")
    md.append(f"### {sec_num}.1 警察・自衛隊・PMCにおける実戦配備")
    md.append(f"結界都市（セーフゾーン）警備および壁外アウトランドへの遠征作戦において、{name_jp}は索敵・突入支援・防壁維持・目標無力化の標準プロトコルとして統合運用されています。特に部隊随伴術士による即時展開は、通常兵器との複合火力（コンバインド・アームズ）として極めて高い戦闘効率を発揮します。")
    md.append("")
    md.append(f"### {sec_num}.2 メガコーポ支配と特許利権")
    md.append(f"ヤマト重工、テイコク製薬、サエデル・シュティフトゥング、アレス等のメガコーポは、{name_jp}の工業・医療・防衛利用に関する独占特許を保有しており、民間術士に対するライセンス管理や魔導触媒・霊薬の市場流通を掌握しています。")
    md.append("")
    md.append(f"### {sec_num}.3 国際魔導協定（IMA）および法規制（CR）")
    md.append(f"破壊力・精神汚染・非人道性の高い高位呪文は、国家公安委員会および国際魔導協定により**規制等級CR3〜CR4（要特別国家許可・戦時国際法規制）**に指定されており、無認可での行使・研究は厳罰に処されます。")
    
    return "\n".join(md)

def run_markdown_generation():
    os.makedirs(TARGET_DIR, exist_ok=True)
    summary = []
    
    for c in COLLEGES:
        cid = c["id"]
        cache_json = os.path.join(CACHE_DIR, f"{cid}_spells_data.json")
        if not os.path.exists(cache_json):
            print(f"Skipping {c['name_jp']}: Cache file not found: {cache_json}")
            continue
            
        with open(cache_json, "r", encoding="utf-8") as f:
            spells = json.load(f)
            
        target_file = os.path.join(TARGET_DIR, c["file"])
        existing_content = ""
        if os.path.exists(target_file):
            with open(target_file, "r", encoding="utf-8") as f:
                existing_content = f.read()
                
        # If plant_and_fungal.md is already populated by plant, fungus appends to it cleanly
        if c["id"] == "fungus" and os.path.exists(target_file):
            print(f"Integrating Fungus Spells ({len(spells)}) into {target_file}...")
            # Append as a distinct section
            f_section = []
            f_section.append("\n\n---\n\n## 菌類系呪文（Fungus Spells / 拡張サプリメント準拠）\n")
            f_section.append("『GURPS Magic: Plant Spells』に収録された、変異菌類・キノコ・胞子操作に特化した拡張呪文群です。\n\n")
            f_section.append("| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |\n")
            f_section.append("| :--- | :---: | :---: | :---: | :---: | :--- | :--- |\n")
            for s in spells:
                f_section.append(format_spell_row(s) + "\n")
            with open(target_file, "a", encoding="utf-8") as f:
                f.write("".join(f_section))
            summary.append((c["name_jp"], len(spells), c["file"]))
            continue
            
        new_md = build_college_markdown(c, spells, existing_content)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(new_md)
            
        print(f"Generated {target_file} with {len(spells)} spells ({len(new_md)} chars)")
        summary.append((c["name_jp"], len(spells), c["file"]))
        
    print("\n\n=======================================================")
    print("MARKDOWN REGENERATION SUMMARY:")
    for name, count, target_file in summary:
        print(f" - {name}: {count} spells -> {target_file}")
    print("=======================================================")

if __name__ == "__main__":
    run_markdown_generation()
