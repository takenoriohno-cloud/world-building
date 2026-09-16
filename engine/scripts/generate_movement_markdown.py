# -*- coding: utf-8 -*-
import json
import re
import os

with open("scratch/movement_spells_data.json", "r", encoding="utf-8") as f:
    spells = json.load(f)

def clean_body_text(text):
    if not text:
        return ""
    lines = text.split("\n")
    cleaned = []
    start = False
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        # Stop at Menu or footer
        if any(m in line_str for m in ["Menu", "MenuBar", "コメントをかく", "利用規約", "魔法関連参照用", "ルールブック『", "第1章「"]):
            break
        # Skip top wiki header noise
        if any(m in line_str for m in ["GURPSよろず", "汎用TRPG", "トップページ ページ一覧", "最終更新：", "Tweet"]):
            continue
        cleaned.append(line_str)
    
    res = "\n".join(cleaned).strip()
    return res

def extract_effect_summary(text):
    body = clean_body_text(text)
    # Find text between 《[[...]]》 and "呪文の解説" or "エネルギー消費"
    m = re.search(r'《\[\[.*?\]\]》\s*(.*?)(?:呪文の解説|エネルギー消費|持続時間|前提条件|$)', body, re.DOTALL)
    if m:
        summary = m.group(1).strip()
        # Clean up multi-lines into a concise string
        summary = re.sub(r'\s+', ' ', summary)
        if summary:
            return summary[:200]
    # Fallback to first meaningful line
    lines = [l for l in body.split("\n") if len(l) > 10 and not l.startswith("■") and not l.startswith("《")]
    if lines:
        return lines[0][:200]
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
    
    # Clean up brackets
    jp_clean = re.sub(r'[《》*（）]', '', jp)
    if '*' in jp or '*' in eng:
        jp_display = f"**《{jp_clean}*》**<br>{eng}"
    else:
        jp_display = f"**《{jp_clean}》**<br>{eng}"
        
    return f"| {jp_display} | {s_class} | {duration} | {cost} | {casting_time} | {prereqs} | {summary} |"

# Categorize spells
table_1_spells = [s for s in spells if s.get('table_category') == 'Table_1']
table_2_spells = [s for s in spells if s.get('table_category') == 'Table_2']
table_3_spells = [s for s in spells if s.get('table_category') == 'Table_3']
table_4_spells = [s for s in spells if s.get('table_category') == 'Table_4']
table_5_spells = [s for s in spells if s.get('table_category') == 'Table_5']

print(f"Table 1 (Basic Magic): {len(table_1_spells)}")
print(f"Table 2 (Plant Movement): {len(table_2_spells)}")
print(f"Table 3 (Artillery MAS): {len(table_3_spells)}")
print(f"Table 4 (Death MDS): {len(table_4_spells)}")
print(f"Table 5 (Least of Spells): {len(table_5_spells)}")

md_output = []
md_output.append("# 移動系呪文 (Movement Spells)")
md_output.append("")
md_output.append("本ドキュメントは、ガープス第4版『魔法大全』第3章（pp.23-29）および公式拡張サプリメント（『Magic: Artillery Spells』『Magic: Death Spells』『Magic: Plant Spells』『Magic: The Least of Spells』）に準拠した、**全61種**の移動系公式呪文アーカイブです。運動エネルギー操作、重力・慣性制御、三次元空間飛行、位相跳躍（テレポート）、ならびに2026年現代における結界都市防衛・軍事特殊急襲作戦での運用データを過不足なく完全網羅しています。")
md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 1. 移動系魔術の力学体系")
md_output.append("")
md_output.append("移動系呪文は、マナの指向性励起を介して目標の運動量ベクトル、重力加速度、慣性質量、および局所空間の幾何構造を直接操作する魔術体系です。")
md_output.append("- **力学的加速限界**: 通常の術士単独詠唱下では、質量100kg前後の目標に対して毎秒最大10m/sの加速制御が物理的・生体媒介的上限となります。")
md_output.append("- **慣性制御とG耐性**: 《浮揚》《飛行術》等では術士自身の生体平衡感覚がマナ流と同調するため急激なG負荷が相殺されますが、《倍速》《瞬間移動》の急激な位相変異は術士の心肺および中枢神経系に激しい代謝疲労（FP消費）を強制します。")
md_output.append("")
md_output.append("### 1.1 主要移動系呪文 前提条件ツリー (Prerequisite Tree)")
md_output.append("")
md_output.append("```mermaid")
md_output.append("graph TD")
md_output.append("    classDef spell fill:#e1f5fe,stroke:#0288d1,stroke-width:1px;")
md_output.append("    ")
md_output.append("    Haste[\"《韋駄天》\"]:::spell --> Glue[\"《べたべた》\"]:::spell")
md_output.append("    Haste --> Grease[\"《つるつる》\"]:::spell")
md_output.append("    Haste --> QuickMarch[\"《進軍》\"]:::spell")
md_output.append("    Haste --> GreatHaste[\"《倍速*》\"]:::spell")
md_output.append("    Haste --> Hinder[\"《のろま》\"]:::spell")
md_output.append("    ")
md_output.append("    Apportation[\"《念動》\"]:::spell --> Levitation[\"《浮揚》\"]:::spell")
md_output.append("    Apportation --> Wallwalker[\"《壁歩き》\"]:::spell")
md_output.append("    Apportation --> Poltergeist[\"《騒霊》\"]:::spell")
md_output.append("    Apportation --> Jump[\"《飛躍》\"]:::spell")
md_output.append("    Apportation --> Locksmith[\"《錠前師》\"]:::spell")
md_output.append("    Apportation --> Deflect[\"《瞬間矢よけ》\"]:::spell")
md_output.append("    Apportation --> Manipulate[\"《見えない手》\"]:::spell")
md_output.append("    ")
md_output.append("    Levitation --> Flight[\"《飛行術*》\"]:::spell")
md_output.append("    Flight --> HawkFlight[\"《高速飛行*》\"]:::spell")
md_output.append("    HawkFlight --> Teleport[\"《瞬間移動*》\"]:::spell")
md_output.append("    ")
md_output.append("    Teleport --> Blink[\"《瞬間回避》\"]:::spell")
md_output.append("    Teleport --> TeleportOther[\"《他者瞬間移動*》\"]:::spell")
md_output.append("    Teleport --> RapidJourney[\"《往復旅行*》\"]:::spell")
md_output.append("    Teleport --> Divert[\"《移動妨害*》\"]:::spell")
md_output.append("    Teleport --> Trace[\"《転移追跡》\"]:::spell")
md_output.append("    ")
md_output.append("    Manipulate --> WizardHand[\"《魔法の手》\"]:::spell")
md_output.append("    Poltergeist --> WingedKnife[\"《飛ぶ剣》\"]:::spell")
md_output.append("```")
md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 2. ガープス第4版『魔法大全』基本移動系呪文（48種）")
md_output.append("")
md_output.append("| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |")
md_output.append("| :--- | :---: | :---: | :---: | :---: | :--- | :--- |")

for s in table_1_spells:
    md_output.append(format_spell_row(s))

md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 3. 複合・環境適応移動系呪文（植物・天候連動）")
md_output.append("")
md_output.append("| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |")
md_output.append("| :--- | :---: | :---: | :---: | :---: | :--- | :--- |")

for s in table_2_spells:
    md_output.append(format_spell_row(s))

md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 4. 魔導兵器・砲兵戦術拡張呪文（MAS / MDS 拡張 7種）")
md_output.append("")
md_output.append("『GURPS Magic: Artillery Spells（MAS）』および『GURPS Magic: Death Spells（MDS）』に収録された、移動力学を破壊・衝撃・致死ベクトルへ極限転化させた軍事拡張呪文です。")
md_output.append("")
md_output.append("| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |")
md_output.append("| :--- | :---: | :---: | :---: | :---: | :--- | :--- |")

for s in table_3_spells + table_4_spells:
    md_output.append(format_spell_row(s))

md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 5. 日常・民間簡単呪文（The Least of Spells 拡張 6種）")
md_output.append("")
md_output.append("『GURPS Magic: The Least of Spells（Mtlos）』に収録された、民間術士（ヘッジ・メイジ）や現場作業員が日常的に行使する低燃費・実用呪文です。前提条件不要または極小のエネルギーで即時発動可能です。")
md_output.append("")
md_output.append("| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |")
md_output.append("| :--- | :---: | :---: | :---: | :---: | :--- | :--- |")

for s in table_5_spells:
    md_output.append(format_spell_row(s))

md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 6. 2026年現代戦術・結界都市防衛・法規制（CR）における運用")
md_output.append("")
md_output.append("### 6.1 警察・自衛隊特殊急襲部隊（SAT/SOG）の三次元立体機動")
md_output.append("都市部での対テロ・対大型魔獣戦において、術士随伴班は《浮揚》《壁歩き》《瞬間回避》を駆使してビルの垂直登攀・突入ルートを確保します。特に《瞬間矢よけ》は暴徒鎮圧や小口径銃撃戦（5.56mm/7.62mm弾）においてポイントマンの生存率を飛躍的に高めています。また、森林・山岳魔境（奥多摩・富士樹海等）では《樹上駆け》《滑走》による高速走破部隊が重用されます。")
md_output.append("")
md_output.append("### 6.2 《瞬間移動》《他者瞬間移動》《倍速》の厳格な法的規制（CR4 / Class-3ライセンス）")
md_output.append("《瞬間移動》および《倍速》は、重要防護施設・結界内部への不法侵入や要人暗殺への悪用リスクが極めて高いため、国家公安委員会および国際魔導協定（IMA）により**規制等級CR4（要特別国家許可・魔力署名常時発信義務）**に指定されています。無認可での行使はテロ等準備罪と同等の重罪が科され、各都市の防衛検問線には《移動妨害*》《転移追跡》を展開する術士部隊が24時間常駐しています。")
md_output.append("")
md_output.append("### 6.3 メガコーポによる軍事・工業特許と魔導兵器（MAS/MDS）の統制")
md_output.append("《衝突場*》《魔法の巨拳*》《内部攪拌*》などの軍事拡張呪文は、ヤマト重工およびテイコク製薬の防衛部門によって「戦略機動破壊術式」として厳重に特許管理・軍事秘匿されています。民間PMCのハンターであっても、Class-IV以上の特異災害指定地域への派遣命令がない限り、実戦行使は厳禁とされています。")

full_content = "\n".join(md_output)

with open("world/magic/spells/movement.md", "w", encoding="utf-8") as f:
    f.write(full_content)

print(f"Successfully generated world/magic/spells/movement.md ({len(full_content)} chars)")
