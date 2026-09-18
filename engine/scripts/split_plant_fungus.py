# -*- coding: utf-8 -*-
"""
Split plant_and_fungal.md into plant.md and fungus.md.
Builds full, comprehensive prerequisite trees for both colleges,
cleans text artifacts, enriches variant explanations, and formats modern tactical/legal lore.
"""

import json
import re
import os

def clean_body_text(text):
    if not text:
        return ""
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        if any(m in line_str for m in ["Menu", "MenuBar", "コメントをかく", "利用規約", "魔法関連参照用", "ルールブック『", "第1章「", "タグについて", "第4版の用語集"]):
            break
        if any(m in line_str for m in ["GURPSよろず", "汎用TRPG", "トップページ ページ一覧", "最終更新：", "Tweet"]):
            continue
        cleaned.append(line_str)
    return "\n".join(cleaned).strip()

def polish_summary(cell):
    cell = re.sub(r'《\[*.*?\]*》', '', cell)
    cell = re.sub(r'年\d{2}月\d{2}日\([日月火水木金土]\)\s*\d{2}:\d{2}:\d{2}\s*履歴', '', cell)
    cell = re.sub(r'＿[a-zA-Z0-9_]+', '', cell)
    cell = re.sub(r'magic_[a-zA-Z0-9_]+', '', cell)
    cell = re.sub(r'呪文データ', '', cell)
    cell = re.sub(r'(?:[一-龥ぁ-んァ-ヶ]+系呪文\s*\d*|[一-龥]+呪文|基本呪文|特定[一-龥]+系呪文|抵抗呪文[_\s一-龥・]+|通常呪文|範囲呪文|射撃呪文|防御呪文|情報呪文|白兵呪文|特殊呪文)[、・\s/]*', '', cell)
    cell = re.sub(r'（[A-Za-z0-9\s\-_’\']+）', '', cell)
    cell = re.sub(r'M\d+(?:-\d+)?P', '', cell)
    cell = re.sub(r'[■◆]', '', cell)
    cell = re.sub(r'^[、・\s/，]+', '', cell)
    cell = re.sub(r'\s+', ' ', cell).strip()
    return cell

def extract_effect_summary(text, is_fungus_variant=False, base_variant_name=""):
    body = clean_body_text(text)
    
    # Check if there are multiple 《[[...]]》 blocks (common in variant pages)
    blocks = re.findall(r'《\[*(.*?)\]*》\s*(.*?)(?=(?:《\[*.*?\]*》|呪文の解説|エネルギー消費|持続時間|前提条件|準備時間|$))', body, re.DOTALL)
    
    if is_fungus_variant and len(blocks) >= 2:
        # The second block usually has the base plant spell's effect description
        base_desc = blocks[1][1].strip()
        base_desc = re.sub(r'\s+', ' ', base_desc)
        base_desc = re.sub(r'^(?:（[A-Za-z0-9\s\-_’\']+）|[A-Za-z0-9\s\-_’\']+|M\d+(?:-\d+)?P|■|《[^》]+》|通常呪文|範囲呪文|射撃呪文|防御呪文|情報呪文|白兵呪文|抵抗呪文|特殊呪文|基本呪文|[0-9A-Za-z\s、・]+)+\s*', '', base_desc)
        polished_base = polish_summary(base_desc)
        # Adapt "植物" to "真菌・菌類" where appropriate
        adapted = polished_base.replace("植物", "菌類（キノコ・カビ・酵母）")
        return f"《{base_variant_name}》の菌類系変種。{adapted}"[:240]
        
    elif blocks:
        summary = blocks[0][1].strip()
        summary = re.sub(r'\s+', ' ', summary)
        summary = re.sub(r'^(?:（[A-Za-z0-9\s\-_’\']+）|[A-Za-z0-9\s\-_’\']+|M\d+(?:-\d+)?P|■|《[^》]+》|通常呪文|範囲呪文|射撃呪文|防御呪文|情報呪文|白兵呪文|抵抗呪文|特殊呪文|基本呪文|[0-9A-Za-z\s、・]+)+\s*', '', summary)
        polished = polish_summary(summary)
        if len(polished) > 10 and not any(k in polished for k in ["tyounekogami", "最終更新", "Tweet"]):
            return polished[:220]
            
    lines = [l for l in body.split("\n") if len(l) > 10 and not any(k in l for k in ["■", "《", "tyounekogami", "最終更新", "Tweet", "参照", "M3", "M4", "M5", "M1", "M2"])]
    if lines:
        clean_l = lines[0].strip()
        clean_l = re.sub(r'^(?:（[A-Za-z0-9\s\-_’\']+）|M\d+(?:-\d+)?P|■|《[^》]+》|[0-9A-Za-z\s、・]+)+\s*', '', clean_l)
        polished = polish_summary(clean_l)
        if len(polished) > 10:
            return polished[:220]
            
    return "効果の詳細は公式ルールブック（『魔法大全』または『Magic: Plant Spells』）を参照。"

def normalize_spell_entry(s, is_fungus=False):
    raw_name = s.get('japanese_name', '').strip()
    raw_en = s.get('english_name', '').strip()
    
    old_name = ""
    m_old = re.search(r'旧名：(.*)', raw_name)
    if m_old:
        old_name = m_old.group(1).replace('）', '').replace(')', '').strip()
        raw_name = re.sub(r'旧名：.*', '', raw_name).strip()
        
    variant = ""
    base_variant_name = ""
    m_var = re.search(r'[（\(]《?(.*?)》?の変種[）\)]', raw_name)
    if m_var:
        base_variant_name = m_var.group(1).replace('《', '').replace('》', '').strip()
        variant = f"《{base_variant_name}》の変種"
        raw_name = re.sub(r'[（\(].*?の変種.*?[）\)]', '', raw_name).strip()
        
    target_note = ""
    m_tar = re.search(r'[（\(]((対|菌類|有機).*?)[）\)]', raw_name)
    if m_tar:
        target_note = m_tar.group(1).strip()
        raw_name = re.sub(r'[（\(]((対|菌類|有機).*?)[）\)]', '', raw_name).strip()

    base_name = raw_name.replace('《', '').replace('》', '').replace('*', '').replace('†', '').strip()
    
    is_vh = False
    if "（至難）" in raw_name or "至難" in raw_name or "(VH)" in raw_en or "*" in raw_name or raw_en.endswith("*"):
        is_vh = True

    clean_en = raw_en.replace('(VH)', '').replace('*', '').replace('†', '').strip()
    clean_en = re.sub(r'^[（\(]+', '', clean_en).replace('）', '').replace(')', '').strip()

    cost = s.get('cost', '').replace('■', '').strip()
    casting_time = s.get('casting_time', '').replace('■', '').strip()
    duration = s.get('duration', '').replace('■', '').strip()
    spell_class = s.get('spell_class', '').replace('■', '').strip()
    
    prereq = s.get('prerequisites', '').strip()
    if not prereq or prereq in ('-', 'なし'):
        prereq = "-"
    else:
        prereq = re.sub(r'旧名：[^\s》]+', '', prereq).strip()

    detail_summary = extract_effect_summary(
        s.get('detail_text', ''),
        is_fungus_variant=bool(variant),
        base_variant_name=base_variant_name
    )
    
    return {
        "base_name": base_name,
        "old_name": old_name,
        "variant": variant,
        "target_note": target_note,
        "is_vh": is_vh,
        "english": clean_en,
        "spell_class": spell_class,
        "duration": duration,
        "cost": cost,
        "casting_time": casting_time,
        "prerequisites": prereq,
        "summary": detail_summary,
        "table_category": s.get('table_category', 'Table_1')
    }

def format_table_row(entry):
    star = "*" if entry["is_vh"] else ""
    name_cell = f"**《{entry['base_name']}{star}》**"
    if entry["old_name"]:
        name_cell += f"<br><small>（旧名：{entry['old_name']}）</small>"
    if entry["variant"]:
        name_cell += f"<br><small>（{entry['variant']}）</small>"
    if entry["target_note"]:
        name_cell += f"<br><small>（{entry['target_note']}）</small>"
    name_cell += f"<br>{entry['english']}"
    if entry["is_vh"]:
        name_cell += " (VH)"
        
    return f"| {name_cell} | {entry['spell_class']} | {entry['duration']} | {entry['cost']} | {entry['casting_time']} | {entry['prerequisites']} | {entry['summary']} |"

def generate_mermaid_tree(entries, college_name, id_prefix="P"):
    spell_dict = {e["base_name"]: e for e in entries}
    
    edges = []
    external_nodes = set()
    
    for base_name, entry in spell_dict.items():
        prereq_str = entry["prerequisites"]
        if prereq_str == "-":
            continue
        found = re.findall(r'《(.*?)》', prereq_str)
        for p in found:
            p_clean = p.replace('《', '').replace('》', '').replace('*', '').replace('†', '').strip()
            p_clean = re.sub(r'旧名：.*', '', p_clean).strip()
            p_clean = re.sub(r'[（\(].*?[）\)]', '', p_clean).strip()
            if not p_clean or p_clean == base_name:
                continue
            if p_clean in spell_dict:
                edges.append((p_clean, base_name))
            else:
                external_nodes.add(p_clean)
                edges.append((p_clean, base_name))

    # All targets
    all_targets = set(t for p, t in edges)
    root_nodes = [name for name in spell_dict if name not in all_targets]

    # Generate Node IDs safely
    node_id_map = {}
    cur_id = 1
    for r in sorted(root_nodes):
        node_id_map[r] = f"{id_prefix}_{cur_id:02d}"
        cur_id += 1
    for s in sorted(spell_dict.keys()):
        if s not in node_id_map:
            node_id_map[s] = f"{id_prefix}_{cur_id:02d}"
            cur_id += 1
    for ext in sorted(external_nodes):
        if ext not in node_id_map:
            node_id_map[ext] = f"Ext_{cur_id:02d}"
            cur_id += 1

    lines = [
        "```mermaid",
        "graph TD",
        "    classDef spell fill:#0f172a,stroke:#38bdf8,stroke-width:1.5px,color:#ffffff;",
        "    classDef vh fill:#1e1b4b,stroke:#a855f7,stroke-width:2px,color:#ffffff;",
        "    classDef ext fill:#1e293b,stroke:#94a3b8,stroke-width:1px,stroke-dasharray: 3 3,color:#cbd5e1;",
        ""
    ]
    
    seen = set()
    for p, t in sorted(edges):
        if (p, t) in seen:
            continue
        seen.add((p, t))
        
        p_id = node_id_map[p]
        t_id = node_id_map[t]
        
        p_class = ":::ext" if p in external_nodes else (":::vh" if spell_dict[p]["is_vh"] else ":::spell")
        t_class = ":::ext" if t in external_nodes else (":::vh" if spell_dict[t]["is_vh"] else ":::spell")
        
        lines.append(f'    {p_id}["《{p}》"]{p_class} --> {t_id}["《{t}》"]{t_class}')

    lines.append("```")
    return "\n".join(lines)


# ==========================================================
# 1. PROCESS PLANT SPELLS (86 SPELLS)
# ==========================================================
with open('scratch/spells_cache/plant_spells_data.json', 'r', encoding='utf-8') as f:
    plant_raw = json.load(f)

plant_entries = [normalize_spell_entry(s, is_fungus=False) for s in plant_raw]

p_table1 = [e for e in plant_entries if e["table_category"] == "Table_1"] # 32
p_table2 = [e for e in plant_entries if e["table_category"] == "Table_2"] # 45
p_table3 = [e for e in plant_entries if e["table_category"] in ("Table_3", "Table_4", "Table_5")] # 7
p_table4 = [e for e in plant_entries if e["table_category"] == "Table_6"] # 2

plant_mermaid = generate_mermaid_tree(plant_entries, "植物系呪文", id_prefix="Plant")

plant_md = f"""# 植物系呪文 (Plant Spells)

本ドキュメントは、ガープス第4版『魔法大全』第10章（pp.61-64）および公式拡張サプリメント（『Magic: Plant Spells』『Magic: Artillery Spells』『Magic: Death Spells』『Magic: The Least of Spells』）に準拠した、**全86種**の植物系公式呪文アーカイブです。木・草・蔦・藻類の成長促進、有機形態変化、木材硬化、ならびに2026年現代における結界都市外縁防護壁・アウトランド魔境緑化対策・軍事機動戦術・法規制（CR）の運用データを過不足なく完全網羅しています。

---

## 1. 植物系魔術の力学体系

植物系呪文は、マナの指向性励起を介して植物細胞の代謝速度、細胞壁のセルロース重合度、光合成変換効率、および局所バイオマス形態を直接操作・変容させる生体変成魔術体系です。
- **細胞増殖と時間短縮**: 《植物繁茂》《植物急成長》は、周囲の地脈マナと大気中の二酸化炭素を瞬時に高分子セルロースへと転換固定し、数ヶ月〜数年分の生長を数秒〜数分で成し遂げます。
- **生体媒介と材質変性**: 《真なる木》《草を剣》等は、木質繊維の結合エネルギーをマナ結合によってダイヤモンド構造に匹敵する強度へと励起し、鋼鉄と同等以上の防護点（DR）と切断力を付与します。
- **生化学兵器・毒素励起**: 《花粉の雲》《毒の茨》《魔粉塵*》は、植物が分泌するアレルゲンや神経毒素を異常分泌させ、非装甲目標や密閉不完全な兵員の呼吸器・皮膚粘膜を即座に無力化します。

### 1.1 植物系呪文 前提条件ツリー (Prerequisite Tree)

植物系呪文全86種の完全な習得体系図です。点線枠は他系統（地霊系、水霊系、移動系、死霊系等）の前提呪文を示し、紫色枠は至難（VH）呪文を示します。

{plant_mermaid}

---

## 2. ガープス第4版『魔法大全』基本植物系呪文（{len(p_table1)}種）

| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
""" + "\n".join([format_table_row(e) for e in p_table1]) + f"""

---

## 3. 公式拡張『Magic: Plant Spells』高度植物系呪文（{len(p_table2)}種）

| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
""" + "\n".join([format_table_row(e) for e in p_table2]) + f"""

---

## 4. 戦術砲兵・死霊兵器拡張呪文（MAS / MDS 拡張 {len(p_table3)}種）

| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
""" + "\n".join([format_table_row(e) for e in p_table3]) + f"""

---

## 5. 日常・民間簡単呪文（The Least of Spells 拡張 {len(p_table4)}種）

| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
""" + "\n".join([format_table_row(e) for e in p_table4]) + """

---

## 6. 2026年現代戦術・都市防衛・法規制（CR）における運用

### 6.1 警察・自衛隊・PMCにおける実戦配備
結界都市（セーフゾーン）警備および壁外アウトランドへの遠征作戦において、植物系呪文は防護壁の緊急自己修復、侵入路の急速遮断、密林・魔境での索敵・隠蔽支援として不可欠な装備となっています。特に部隊随伴術士による《真なる木》《樹皮の鎧》の付与は、通常小銃弾に対する防御力を飛躍的に高め、《拘束の蔓》《よじれ枝》は魔獣の突撃足を即座に止める非致死性制圧手段として多用されています。

### 6.2 メガコーポ支配と特許利権
ヤマト重工、テイコク製薬、サエデル・シュティフトゥング、アレス等のメガコーポは、植物系呪文の農業・林業・医療・防衛利用に関する独占特許を保有しています。特に《植物繁茂》《植物急成長》《紙作成》の工業プロセス連動や、《森僧の静養》をベースとした生薬抽出技術はメガコーポの莫大なバイオ収益源となっており、無認可術士による商業栽培・流通は厳しく監視・法的に排除されています。

### 6.3 国際魔導協定（IMA）および法規制（CR）
広域に枯渇・壊滅をもたらす《枯死》《不作》や、無差別化学攻撃に等しい《魔粉塵*》《殺人花*》《肉体腐失*》は、国家公安委員会および国際魔導協定により**規制等級CR3〜CR4（要特別国家許可・戦時国際法規制）**に指定されています。壁外アウトランドでの魔獣駆除を除き、都市部や公道での無認可詠唱は生物兵器テロと同等の重罪として軍事警察・特課の即時射殺対象となります。

---

## 7. 参考文献・典拠アーカイブ
- 『GURPS Magic 4th Edition』pp.61-64（Plant Spells College）
- 『GURPS Magic: Plant Spells』（SJ Games 公式拡張サプリメント）
- 『GURPS Magic: Artillery Spells』（SJ Games 公式拡張サプリメント）
- 『GURPS Magic: Death Spells』（SJ Games 公式拡張サプリメント）
- 『GURPS Magic: The Least of Spells』（SJ Games 公式拡張サプリメント）
"""

with open('world/magic/spells/plant.md', 'w', encoding='utf-8') as f:
    f.write(plant_md.strip() + "\n")

print("Created world/magic/spells/plant.md successfully (86 spells).")


# ==========================================================
# 2. PROCESS FUNGUS SPELLS (30 UNIQUE SPELLS)
# ==========================================================
with open('scratch/spells_cache/fungus_spells_data.json', 'r', encoding='utf-8') as f:
    fungus_raw = json.load(f)[:30] # Unique 30 spells

fungus_entries = [normalize_spell_entry(s, is_fungus=True) for s in fungus_raw]
fungus_mermaid = generate_mermaid_tree(fungus_entries, "菌類系呪文", id_prefix="Fungus")

fungus_md = f"""# 菌類系呪文 (Fungus Spells)

本ドキュメントは、ガープス公式拡張サプリメント『GURPS Magic: Plant Spells』に準拠した、**全30種**の菌類系公式呪文アーカイブです。キノコ、カビ、酵母、変異粘菌、菌糸ネットワークの励起・制御、有機物腐敗分解、ならびに2026年現代における結界都市地下インフラ管理・バイオハザード防衛・生化学醸造特許・法規制（CR）の運用データを過不足なく完全網羅しています。

---

## 1. 菌類系魔術の力学体系

菌類系呪文は、マナの低周波共鳴を介して真菌類の胞子発芽、菌糸伸長、酵素分泌による有機物分解、ならびに変異代謝物質（マイコトキシン）の生成速度を直接制御する特殊生命魔術体系です。
- **腐生・分解の超加速**: 《腐敗》《老朽化》は、セルロースやタンパク質、炭化水素化合物を数秒で加水分解・酸化分解し、有機構造物を瞬時に泥状へと崩壊させます。
- **胞子エアロゾルと生体侵襲**: 《胞子の雲》《窒息化》《疫病》は、術士のマナによって活性化された変異微小胞子を大気中に拡散させ、呼吸器の急速閉塞や急性菌血症・皮膚壊死を引き起こします。
- **発酵工学と解毒バイオ**: 《発酵》《解毒》《病気治療》は、有益な酵母・放線菌・分解菌の共生活性を極大化し、工業的な醸造・抗生物質合成や有毒真菌毒素の無害化を瞬時に達成します。

### 1.1 菌類系呪文 前提条件ツリー (Prerequisite Tree)

菌類系呪文全30種の完全な習得体系図です。紫色枠は至難（VH）呪文を示します。菌類系は《菌類探知》を起点とし、分析・治癒・繁茂を経て高度な生体変成・腐敗兵器へと分岐・完結する整然たるツリー構造を有しています。

{fungus_mermaid}

---

## 2. 公式拡張『Magic: Plant Spells』菌類系呪文（{len(fungus_entries)}種）

菌類系呪文の多くは植物系呪文の真菌類対応変種として設計されており、植物系呪文と同等の魔力消費と詠唱時間で真菌・酵母・カビを操作可能です。

| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
""" + "\n".join([format_table_row(e) for e in fungus_entries]) + """

---

## 3. 2026年現代戦術・都市インフラ防衛・法規制（CR）における運用

### 3.1 結界都市地下調節池・閉鎖空間における真菌災害防除
東京地下調節池要塞網、春日部放水路、地下鉄網、ならびに核・マナシェルター等の高湿度・閉鎖環境において、変異カビや真菌性バイオハザードは都市機能を麻痺させる重大な脅威です。東京都環境保安局および自衛隊施設科は、専門の菌類術士を配備し、《菌類探知》《菌類分析》《菌類治癒》《解毒》を用いた定期的な真菌スキャンと空気清浄フィルターのバイオ防護を常時実施しています。

### 3.2 メガコーポによる発酵バイオテクノロジーと特許利権
テイコク製薬、豊洲中央流通HD、サエデル・シュティフトゥング等のメガコーポは、菌類系呪文を用いた高速発酵・高付加価値バイオ医薬品（抗生ペプチド・抗マナ代謝阻害剤）の製造ラインを工業化しています。特に《発酵》を応用した合成食料・医薬品培養プラントは莫大な利益を生み出しており、野生菌類の採取や無認可培養に対しては厳しい特許侵害監視網が敷かれています。

### 3.3 生化学兵器規制（CWC連動）および法規制（CR）
人体を内部から腐敗・液状化させる《腐敗の死神*》や、広域に致死性真菌症を蔓延させる《疫病》《毒化》《老朽化》は、化学兵器禁止条約（CWC）および国際魔導協定（IMA）により**規制等級CR4（軍事使用厳禁・人道に対する罪）**に指定されています。これらの呪文の所持・研究はアビス異端審問室および公安特殊課の厳格な摘発対象であり、違反者は国際魔導軍事裁判に付されます。

---

## 4. 参考文献・典拠アーカイブ
- 『GURPS Magic: Plant Spells』（SJ Games 公式拡張サプリメント, Fungus Spells Section）
- 『GURPS Magic 4th Edition』各関連呪文（Decay, Itch, Sickness, Ruin, Pestilence等）
- 東京都環境保安局『閉鎖空間における真菌災害防護マニュアル（2026年版）』
"""

with open('world/magic/spells/fungus.md', 'w', encoding='utf-8') as f:
    f.write(fungus_md.strip() + "\n")

print("Created world/magic/spells/fungus.md successfully (30 spells).")
