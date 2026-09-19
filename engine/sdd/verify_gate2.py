# -*- coding: utf-8 -*-
"""
Gate 2 Deterministic Validator (verify_gate2.py)
Mechanically checks if a Plan satisfies all constitutional requirements of Gate 2:
1. Plan file existence
2. TEMPLATE.md full coverage (all 9 chapters and all 20 sections) in checklist
3. GURPS official spell existence (Auto-grep in world/magic/spells/*.md)
4. High Entity (Animal Lord / Elemental Lord) proper noun and phonetic lore check
   - Animal Lord: vocalizations/hisses/howls/clicks phonetics that the animals themselves can call
   - Elemental Lord: Elemental Tongue phonetics (Elric-style)
5. QGIS tactical map generation task definition
6. 6 Expert Persona review checkpoints
"""

import sys
import os
import re
import argparse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MANDATORY_SECTIONS = [
    ("1. 基本分類・早わかり", ["1. 基本分類", "Fast Facts", "早わかり"]),
    ("生息・分布マップ", ["生息・分布マップ", "Range Map", "タクティカルマップ"]),
    ("視覚資料アーカイブ", ["視覚資料アーカイブ", "Visual Archive"]),
    ("2. 伝承考証とマナ覚醒の架橋", ["2. 伝承考証", "マナ覚醒の架橋", "Lore & Historical"]),
    ("2.1 原典・民俗伝承の記録", ["2.1 原典", "民俗伝承"]),
    ("2.2 2000年マナ覚醒による生体科学的架橋", ["2.2", "生体科学的架橋"]),
    ("3. 生物学的特徴・ライフステージ", ["3. 生物学的特徴", "ライフステージ", "Biological Traits"]),
    ("3.1 外見・解剖学的身体構造", ["3.1 外見", "解剖学的身体構造"]),
    ("3.2 ライフステージと繁殖・育児ドラマ", ["3.2 ライフステージ", "繁殖・育児"]),
    ("4. 生態・食物連鎖・人間社会との摩擦", ["4. 生態", "食物連鎖", "人間社会との摩擦", "Ecology"]),
    ("4.1 食性・捕食行動", ["4.1 食性", "捕食行動"]),
    ("4.2 魔獣間クロス・リレーション", ["4.2 魔獣間クロス", "相互作用"]),
    ("4.3 人間社会との摩擦・利用・保護史", ["4.3 人間社会との摩擦", "保護史"]),
    ("5. 魔導科学・上位神性・背景ロア", ["5. 魔導科学", "上位神性", "背景ロア", "Thaumaturgical"]),
    ("5.1 魔力現象と発現メカニズム", ["5.1 魔力現象", "発現メカニズム"]),
    ("5.2 音響・周波数・生体通信特性", ["5.2 音響", "周波数", "生体通信"]),
    ("5.3 上位存在・アビス因果・メガコーポ伏線", ["5.3 上位存在", "アビス因果", "メガコーポ伏線"]),
    ("6. 交戦マニュアル・都市防災コラム", ["6. 交戦マニュアル", "都市防災コラム", "Combat Manual"]),
    ("6.1 GURPS 4th Stat Block", ["6.1 GURPS", "Stat Block", "戦闘データ"]),
    ("6.2 推奨火器・防護装備", ["6.2 推奨火器", "防護装備"]),
    ("6.3 市民防災メモ ＆ 専門家の知恵袋", ["6.3 市民防災メモ", "専門家の知恵袋"]),
    ("7. 解体・ジビエ食文化・料理レシピ", ["7. 解体", "ジビエ食文化", "Harvesting & Cuisine"]),
    ("7.1 解体プロトコルと市場相場", ["7.1 解体プロトコル", "市場相場"]),
    ("7.2 伝統料理・メガコーポスペシャリテ", ["7.2 伝統料理", "メガコーポスペシャリテ"]),
    ("7.3 産業素材・医療利用", ["7.3 産業素材", "医療利用"]),
    ("8. 現場記録・通信ログ", ["8. 現場記録", "通信ログ", "Field Logs"]),
    ("9. 参考文献・典拠資料", ["9. 参考文献", "典拠資料", "References"]),
    ("脚注・専門部署査定メモ", ["脚注・専門部署査定メモ", "Persona Footnotes"])
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

def check_high_entity_lore(content, creature_file_content=None):
    """
    Checks if High Entity proper noun and phonetic lore (Animal Lord vocalization / Elemental Tongue)
    are explicitly defined in Plan or Creature file.
    """
    combined = content
    if creature_file_content:
        combined += "\n" + creature_file_content

    # Check 1: Mention of High Entity / Animal Lord / Elemental Lord / Plane Pact
    high_entity_keywords = ["上位存在", "動物王", "精霊王", "アーキタイプ", "プレーン・パクト", "プレーンパクト", "Beast Lord", "Animal Lord", "Elemental Lord"]
    has_high_entity = any(kw in combined for kw in high_entity_keywords)
    if not has_high_entity:
        return False, "No mention of High Entity / Animal Lord / Elemental Lord / Plane Pact in Section 5.3."

    # Check 2: Existence of Proper Noun in quotes (『...』 or "...")
    # Look around section 5.3 or keywords
    proper_noun_matches = re.findall(r"『([^』]+)』", combined)
    if not proper_noun_matches:
        # Also check for Japanese quotes or explicit proper noun field
        proper_noun_matches = re.findall(r"真名[：:]\s*([^\n\r]+)", combined)

    if not proper_noun_matches:
        return False, "High Entity proper noun (e.g. 『...』) is MISSING in Section 5.3."

    # Check 3: Phonetic Lore / Origin requirement:
    # If Animal Lord: must mention vocalization/hiss/howl/click/chirp/sound (鳴き声, 発声, ヒス, 遠吠え, 唸り, クリック, 呼気, 音素, 喉)
    # If Elemental Lord: must mention Elemental Tongue / 精霊語 / 精霊界言語
    has_phonetic_origin = any(kw in combined for kw in [
        "鳴き声", "発声", "ヒス", "遠吠え", "唸り", "クリック", "呼気", "音素", "咽頭", "喉鳴らし", "精霊語", "精霊界の言語", "精霊界言語", "Elemental Tongue", "エルリック"
    ])
    if not has_phonetic_origin:
        return False, "Phonetic lore for High Entity is MISSING. Animal Lord MUST be derived from animal vocalizations (hisses/howls/etc.), or Elemental Lord from Elemental Tongue."

    return True, f"Verified High Entity proper noun: {proper_noun_matches[0]} with phonetic lore."

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
        plan_content = f.read()

    # Read creature file if already drafted
    creature_content = None
    creature_path = os.path.join(ROOT_DIR, "creatures", f"{creature_id}.md")
    if os.path.exists(creature_path):
        with open(creature_path, "r", encoding="utf-8") as cf:
            creature_content = cf.read()

    # 1. Check Mandatory Sections from TEMPLATE.md (all 20 sub-sections)
    for label, patterns in MANDATORY_SECTIONS:
        found = any(pat in plan_content for pat in patterns)
        if not found:
            errors.append(f"Mandatory section '{label}' is MISSING in Plan checklist.")

    # 2. Check GURPS Official Spells
    found_spells, missing_spells = check_spells_in_archive(plan_content)
    if missing_spells:
        errors.append(f"Fictional / Unofficial spells detected not in world/magic/spells/*.md: {missing_spells}")
    
    # 3. Check High Entity Proper Noun and Phonetic Lore (Animal Lord vocalization / Elemental Tongue)
    he_ok, he_msg = check_high_entity_lore(plan_content, creature_content)
    if not he_ok:
        errors.append(f"High Entity Lore Error: {he_msg}")

    # 4. Check QGIS Map Generation Definition
    if "generate_tactical_map.py" not in plan_content and "タクティカルマップ" not in plan_content:
        errors.append("QGIS tactical map generation task/command is MISSING in Plan.")

    # 5. Check 6 Personas Review Check
    for short_name, full_name in PERSONAS:
        if short_name not in plan_content and full_name not in plan_content:
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
        print("  ✓ Plan checklist covers all TEMPLATE.md sections (all 9 chapters and 20 sections).")
        print("  ✓ All GURPS spells strictly verified against world/magic/spells/*.md.")
        print("  ✓ High Entity proper noun & phonetic lore (animal vocalization / Elemental Tongue) verified.")
        print("  ✓ QGIS tactical map task definition verified.")
        print("  ✓ All 6 persona assessment checkpoints verified.")
        print("\nReady for Gate 2 human review and approval token issuance.")
        sys.exit(0)

if __name__ == "__main__":
    main()
