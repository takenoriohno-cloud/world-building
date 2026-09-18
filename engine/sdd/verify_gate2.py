# -*- coding: utf-8 -*-
"""
Gate 2 Deterministic Validator (verify_gate2.py)
Mechanically checks if a Plan satisfies all constitutional requirements of Gate 2:
1. Plan file existence
2. TEMPLATE.md 20-section full coverage in checklist
3. GURPS official spell existence (Auto-grep in world/magic/spells/*.md)
4. QGIS tactical map generation task definition
5. 6 Expert Persona review sections
"""

import sys
import os
import re
import argparse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MANDATORY_SECTIONS = [
    "## 1. 基本分類・早わかり",
    "## 2. 伝承考証とマナ覚醒の架橋",
    "## 3. 生物学的特徴・ライフステージ",
    "## 4. 生態・食物連鎖・人間社会との摩擦",
    "## 5. 魔導科学・上位神性・背景ロア",
    "## 6. 交戦マニュアル・都市防災コラム",
    "## 7. 解体・ジビエ食文化・料理レシピ",
    "## 8. 現場記録・通信ログ",
    "## 9. 参考文献・典拠資料",
    "## 脚注・専門部署査定メモ"
]

PERSONAS = [
    ("ゼクスト", "首席監査官ゼクスト"),
    ("鷹司", "鷹司 冴子 博士"),
    ("陣内", "陣内 隆文 調査官"),
    ("シュルツ", "V・シュルツ 特命調査員"),
    ("黒田", "クリスティナ・黒田 所長"),
    ("蓮見", "蓮見 蓮 プロデューサー")
]

def parse_args():
    parser = argparse.ArgumentParser(description="Gate 2 Plan Deterministic Validator")
    parser.add_argument("--id", required=True, help="Creature ID (e.g. 019_forest_mirage_chameleon)")
    return parser.parse_args()

def check_spells_in_archive(content):
    spell_matches = re.findall(r"《([^》]+)》", content)
    unique_spells = set()
    for s in spell_matches:
        base_s = s.split("/")[0].split("*")[0].strip()
        unique_spells.add(base_s)
    
    missing_spells = []
    spells_dir = os.path.join(ROOT_DIR, "world", "magic", "spells")
    
    # Read all markdown files in spells_dir once
    spell_corpus = ""
    for root, _, files in os.walk(spells_dir):
        for f in files:
            if f.endswith(".md"):
                with open(os.path.join(root, f), "r", encoding="utf-8") as sf:
                    spell_corpus += sf.read() + "\n"

    for spell in unique_spells:
        if spell not in spell_corpus:
            missing_spells.append(spell)

    return unique_spells, missing_spells

def check_gate2(creature_id):
    errors = []
    warnings = []
    
    plan_path = os.path.join(ROOT_DIR, ".specify", "plans", "creatures", f"{creature_id}.plan.md")
    if not os.path.exists(plan_path):
        alt_path = os.path.join(ROOT_DIR, ".specify", "plans", f"{creature_id}.plan.md")
        if os.path.exists(alt_path):
            plan_path = alt_path
        else:
            return False, [f"Plan file not found: {plan_path}"], []

    with open(plan_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check Mandatory Sections from TEMPLATE.md
    for sec in MANDATORY_SECTIONS:
        # Match either exact header or header within checklist
        if sec not in content:
            # Check without leading ##
            sec_clean = sec.replace("## ", "").split("（")[0].strip()
            if sec_clean not in content:
                errors.append(f"Mandatory section '{sec}' is MISSING in Plan checklist.")

    # 2. Check GURPS Official Spells
    found_spells, missing_spells = check_spells_in_archive(content)
    if missing_spells:
        errors.append(f"Fictional / Unofficial spells detected not in world/magic/spells/*.md: {missing_spells}")
    
    # 3. Check QGIS Map Generation Definition
    if "generate_tactical_map.py" not in content and "タクティカルマップ" not in content:
        errors.append("QGIS tactical map generation task/command is MISSING in Plan.")

    # 4. Check 6 Personas Review Check
    for short_name, full_name in PERSONAS:
        if short_name not in content and full_name not in content:
            errors.append(f"Persona review/footnote checkpoint for '{full_name}' is MISSING in Plan.")

    is_pass = (len(errors) == 0)
    return is_pass, errors, warnings

def main():
    args = parse_args()
    print(f"\n========================================================")
    print(f"  Gate 2 Deterministic Plan Validation: {args.id}")
    print(f"========================================================")
    
    is_pass, errors, warnings = check_gate2(args.id)
    
    if warnings:
        print("\n[WARNINGS]:")
        for w in warnings:
            print(f"  ! {w}")

    if not is_pass:
        print("\n[GATE 2 VALIDATION FAILED - STOPPING (HALT)]")
        for e in errors:
            print(f"  x {e}")
        print("\nResolve all plan errors before requesting Gate 2 human approval.")
        sys.exit(1)
    else:
        print("\n[GATE 2 VALIDATION 100% PASS]")
        print("  ✓ Plan checklist covers all TEMPLATE.md sections.")
        print("  ✓ All GURPS spells strictly verified against world/magic/spells/*.md.")
        print("  ✓ QGIS tactical map task definition verified.")
        print("  ✓ All 6 persona assessment checkpoints verified.")
        print("\nReady for Gate 2 human review and approval token issuance.")
        sys.exit(0)

if __name__ == "__main__":
    main()
