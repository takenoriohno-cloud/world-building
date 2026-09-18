# -*- coding: utf-8 -*-
import json
import re
import os

with open("scratch/sound_spells_data.json", "r", encoding="utf-8") as f:
    spells = json.load(f)

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
    m = re.search(r'《\[\[.*?\]\]》\s*(.*?)(?:呪文の解説|エネルギー消費|持続時間|前提条件|$)', body, re.DOTALL)
    if m:
        summary = m.group(1).strip()
        summary = re.sub(r'\s+', ' ', summary)
        if summary:
            return summary[:200]
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
    
    # Clean up name brackets
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

table_1_spells = [s for s in spells if s.get('table_category') == 'Table_1']
table_2_spells = [s for s in spells if s.get('table_category') == 'Table_2']
table_3_spells = [s for s in spells if s.get('table_category') == 'Table_3']
table_4_spells = [s for s in spells if s.get('table_category') == 'Table_4']

print(f"Table 1 (Basic Magic): {len(table_1_spells)}")
print(f"Table 2 (Artillery MAS): {len(table_2_spells)}")
print(f"Table 3 (Death MDS): {len(table_3_spells)}")
print(f"Table 4 (Least of Spells): {len(table_4_spells)}")

md_output = []
md_output.append("# 音声系呪文 (Sound Spells)")
md_output.append("")
md_output.append("本ドキュメントは、ガープス第4版『魔法大全』第4章（pp.30-33）および公式拡張サプリメント（『Magic: Artillery Spells』『Magic: Death Spells』『Magic: The Least of Spells』）に準拠した、**全38種**の音声系公式呪文アーカイブです。音波振動、指向性音響、完全消音、音響物理衝撃波、残響再現（過去聴覚）、ならびに2026年現代における結界都市防衛・対魔獣音響戦術・メガコーポ情報保全の運用データを過不足なく完全網羅しています。")
md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 1. 音声系魔術の力学体系")
md_output.append("")
md_output.append("音声系呪文は、マナの微細周波数共鳴を介して空気中や固体媒質中の音波（粗密波）を生成・変調・位相干渉（消音）・増幅する魔術体系です。")
md_output.append("- **生体媒介原則と音圧制御**: マナそのものは物理的音波粒子ではありませんが、媒質分子の振動ベクトルを直接励起します。微小な足音の消滅（完全逆位相相殺）から、鼓膜や内臓を震盪させる140dB超級の爆裂音響衝球までを自在に制御します。")
md_output.append("- **電脳音響・盗聴技術との境界**: 音声系魔術は術士の生体聴覚・声帯神経を介して作用します。指向性レーザーマイクやデジタル録音機に対しても、《沈黙障壁》や《不明瞭》による物理的音波変調効果はそのまま有効に機能します。")
md_output.append("")
md_output.append("### 1.1 主要音声系呪文 前提条件ツリー (Prerequisite Tree)")
md_output.append("")
md_output.append("```mermaid")
md_output.append("graph TD")
md_output.append("    classDef spell fill:#0f172a,stroke:#38bdf8,stroke-width:1.5px,color:#ffffff;")
md_output.append("    ")
md_output.append("    Sound[\"《作音》\"]:::spell --> Silence[\"《沈黙》\"]:::spell")
md_output.append("    Sound --> Thunderclap[\"《雷鳴》\"]:::spell")
md_output.append("    Sound --> Voices[\"《発声》\"]:::spell")
md_output.append("    Sound --> KeenSense[\"《感覚鋭敏化》\"]:::spell")
md_output.append("    ")
md_output.append("    Silence --> WallOfSilence[\"《沈黙障壁》\"]:::spell")
md_output.append("    Silence --> Hush[\"《静寂》\"]:::spell")
md_output.append("    Hush --> MageStealth[\"《忍び足》\"]:::spell")
md_output.append("    ")
md_output.append("    Voices --> GreatVoice[\"《拡声》\"]:::spell")
md_output.append("    Voices --> ImitateVoice[\"《擬声》\"]:::spell")
md_output.append("    Voices --> Garble[\"《不明瞭》\"]:::spell")
md_output.append("    Voices --> WizardMouth[\"《魔法の口》\"]:::spell")
md_output.append("    Voices --> AlterVoice[\"《声変え》\"]:::spell")
md_output.append("    ")
md_output.append("    GreatVoice --> SoundJet[\"《音噴射》\"]:::spell")
md_output.append("    GreatVoice --> Noise[\"《騒音》\"]:::spell")
md_output.append("    ")
md_output.append("    Thunderclap --> Concussion[\"《爆裂衝球》\"]:::spell")
md_output.append("    Concussion --> ImpConcussion[\"《強化爆裂衝球*》\"]:::spell")
md_output.append("    ")
md_output.append("    KeenSense --> SoundVision[\"《超音波視覚》\"]:::spell")
md_output.append("    KeenSense --> FarHearing[\"《遠耳》\"]:::spell")
md_output.append("    FarHearing --> WizardEar[\"《魔法の耳》\"]:::spell")
md_output.append("    WizardEar --> InvWizardEar[\"《透明な耳》\"]:::spell")
md_output.append("    FarHearing --> Echoes[\"《残響再現》\"]:::spell")
md_output.append("    ")
md_output.append("    Silence --> ResistSound[\"《防音》\"]:::spell")
md_output.append("    Voices --> Converse[\"《密談》\"]:::spell")
md_output.append("    Voices --> DelayedMessage[\"《遅発伝言》\"]:::spell")
md_output.append("```")
md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 2. ガープス第4版『魔法大全』基本音声系呪文（28種）")
md_output.append("")
md_output.append("| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |")
md_output.append("| :--- | :---: | :---: | :---: | :---: | :--- | :--- |")

for s in table_1_spells:
    md_output.append(format_spell_row(s))

md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 3. 魔導兵器・音響戦術拡張呪文（MAS / MDS 拡張 5種）")
md_output.append("")
md_output.append("『GURPS Magic: Artillery Spells（MAS）』および『GURPS Magic: Death Spells（MDS）』に収録された、音波振動を組織破壊・共振破砕・即死音響エネルギーへと昇華させた軍事拡張呪文です。")
md_output.append("")
md_output.append("| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |")
md_output.append("| :--- | :---: | :---: | :---: | :---: | :--- | :--- |")

for s in table_2_spells + table_3_spells:
    md_output.append(format_spell_row(s))

md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 4. 日常・民間簡単呪文（The Least of Spells 拡張 5種）")
md_output.append("")
md_output.append("『GURPS Magic: The Least of Spells（Mtlos）』に収録された、民間術士（ヘッジ・メイジ）や現場捜査官が日常的に行使する低燃費・実用音声呪文です。前提条件不要または極小のエネルギーで即時発動可能です。")
md_output.append("")
md_output.append("| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |")
md_output.append("| :--- | :---: | :---: | :---: | :---: | :--- | :--- |")

for s in table_4_spells:
    md_output.append(format_spell_row(s))

md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 5. 2026年現代戦術・対魔獣音響兵器・情報保全における運用")
md_output.append("")
md_output.append("### 5.1 聴覚鋭敏魔獣に対する指向性音響弾頭・スクリーム作戦")
md_output.append("アウトランドに生息する変異コウモリ、犬科魔獣、大型幻獣など、高周波聴覚に依存する夜行性生物に対し、自衛隊音響専門部隊や民間重火器PMCは《音噴射》《雷鳴》《爆裂衝球》および指向性長距離音響発生装置（LRAD）を同期させ、三半規管および前庭器官を過負荷粉砕して無力化する戦術を採用しています。")
md_output.append("")
md_output.append("### 5.2 メガコーポ情報保全・盗聴遮断結界（CR2 / Class-2情報管理規約）")
md_output.append("ヤマト重工、テイコク製薬、サエデル・シュティフトゥング等のメガコーポ役員会議室や先端研究所には、レーザー干渉計マイクや電脳ドローンによる盗聴を完全に阻止するため、《沈黙障壁》《密談》が常時施工された防音二重ガラスが標準装備されています。また、重要容疑者の取り調べや犯罪現場では《残響再現》（過去聴覚）による音響捜査が科捜研・警視庁公安部で行われています。")
md_output.append("")
md_output.append("### 5.3 軍事音響兵器（MAS/MDS）の国際規制（CR4）")
md_output.append("《破壊振動*》《死の声がけ*》《破肉の叫び*》などの軍事拡張呪文は、非装甲の人体・生体組織に対して防弾ベスト（DR）を完全に貫通・無視して内臓破裂を引き起こすため、国際魔導協定（IMA）により**規制等級CR4（大量破壊・非人道術式）**として厳格に禁止・戦時国際法違反指定されています。")

full_content = "\n".join(md_output)

with open("world/magic/spells/sound.md", "w", encoding="utf-8") as f:
    f.write(full_content)

print(f"Successfully updated world/magic/spells/sound.md ({len(full_content)} chars)")
