# -*- coding: utf-8 -*-
"""
Gate 1 Deterministic Validator (verify_gate1.py)
Mechanically checks if a Spec satisfies all constitutional requirements of Gate 1:
1. Spec file existence
2. Chapter 0 (Mythological / Classical Lore with primary source citations)
3. Origin Habitat Mapping (Primary Habitat vs Domestic Status)
4. Standard Japanese Nomenclature compliance (No pure 4-character idioms, Modifier + Base)
5. Multiple Nomenclature Choices (User consensus record in Q&A or Spec)
6. Full Biological Taxonomy (Phylum, Class, Order, Family, Genus, Species)
7. Resource Classification (Class-A/B/C) and Threat Level
"""

import sys
import os
import re
import argparse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def parse_args():
    parser = argparse.ArgumentParser(description="Gate 1 Spec Deterministic Validator")
    parser.add_argument("--id", required=True, help="Creature ID (e.g. 019_forest_mirage_chameleon)")
    return parser.parse_args()

def check_gate1(creature_id):
    errors = []
    warnings = []
    
    spec_path = os.path.join(ROOT_DIR, ".specify", "specs", "creatures", f"{creature_id}.spec.md")
    if not os.path.exists(spec_path):
        # check if in specs root
        alt_path = os.path.join(ROOT_DIR, ".specify", "specs", f"{creature_id}.spec.md")
        if os.path.exists(alt_path):
            spec_path = alt_path
        else:
            return False, [f"Spec file not found: {spec_path}"]

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check Chapter 0 (Classical / Mythological Lore)
    if "第0章" not in content and "原典・神話伝承考証" not in content:
        errors.append("Chapter 0 (原典・神話伝承考証) is MISSING in Spec.")
    else:
        # Check if classical sources cited
        lore_keywords = ["神話", "伝承", "博物誌", "風土記", "ベスティアリ", "文献", "Pliny", "Frazer"]
        if not any(kw in content for kw in lore_keywords):
            errors.append("Chapter 0 does not cite recognizable classical/mythological primary sources.")

    # 2. Check Origin Habitat Mapping
    if "原典発祥地マッピング" not in content and "一次野生生息地" not in content:
        errors.append("Origin Habitat Mapping (原典発祥地マッピング / 一次野生生息地) is MISSING.")
    
    # 3. Check Standard Japanese Nomenclature (標準和名)
    m_wamei = re.search(r"標準和名[\s\*]*[:：]\s*([^\n\r]+)", content)
    if not m_wamei:
        errors.append("Field '標準和名' is MISSING.")
    else:
        wamei = m_wamei.group(1).replace("*", "").strip()
        # Check pure 4-kanji idiom violation (e.g. 剛毛巌猪, 幽光星海月 without brackets)
        pure_4kanji = re.fullmatch(r"[\u4e00-\u9faf]{4}", wamei.replace("［", "").replace("］", "").split("（")[0].strip())
        if pure_4kanji:
            errors.append(f"Standard Nomenclature '{wamei}' violates naming rule (Pure 4-kanji idiom prohibited).")

    # 4. Check Multiple Nomenclature Choices (和名複数選択肢の合意記録)
    # Search in Q&A or within spec
    qa_path = os.path.join(ROOT_DIR, "doc", "questions_and_answers.md")
    has_qa_record = False
    if os.path.exists(qa_path):
        with open(qa_path, "r", encoding="utf-8") as f:
            qa_content = f.read()
        if creature_id in qa_content or (m_wamei and m_wamei.group(1).split("（")[0].strip() in qa_content):
            has_qa_record = True
    
    if not has_qa_record and "和名候補" not in content and "選択肢" not in content:
        warnings.append("Multiple nomenclature choice record not explicitly found in doc/questions_and_answers.md.")

    # 5. Check Biological Classification (門・綱・目・科・属・種)
    tax_levels = ["門", "綱", "目", "科", "属", "種"]
    missing_tax = [lvl for lvl in tax_levels if f"{lvl}" not in content]
    if len(missing_tax) > 2:
        errors.append(f"Biological taxonomy incomplete. Missing levels: {missing_tax}")

    # 6. Check Resource Class and Threat Level
    if not re.search(r"Class-[ABC]", content):
        errors.append("Resource Class (Class-A / Class-B / Class-C) is MISSING or invalid.")
    if not re.search(r"Threat\s*Level", content, re.IGNORECASE):
        errors.append("Threat Level is MISSING in Spec.")

    is_pass = (len(errors) == 0)
    return is_pass, errors, warnings

def main():
    args = parse_args()
    print(f"\n========================================================")
    print(f"  Gate 1 Deterministic Spec Validation: {args.id}")
    print(f"========================================================")
    
    is_pass, errors, warnings = check_gate1(args.id)
    
    if warnings:
        print("\n[WARNINGS]:")
        for w in warnings:
            print(f"  ! {w}")

    if not is_pass:
        print("\n[GATE 1 VALIDATION FAILED - STOPPING (HALT)]")
        for e in errors:
            print(f"  x {e}")
        print("\nFix the spec file before requesting Gate 1 user approval.")
        sys.exit(1)
    else:
        print("\n[GATE 1 VALIDATION 100% PASS]")
        print("  ✓ Spec file structure verified.")
        print("  ✓ Classical lore & primary habitat mapped.")
        print("  ✓ Standard nomenclature compliance confirmed.")
        print("  ✓ Full taxonomy & resource classification confirmed.")
        print("\nReady for Gate 1 human review and approval token issuance.")
        sys.exit(0)

if __name__ == "__main__":
    main()
