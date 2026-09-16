# -*- coding: utf-8 -*-
import json
import re
import os

with open("scratch/fire_spells_data.json", "r", encoding="utf-8") as f:
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
    # Match both 《[[...]]》 and 《[...]]》 or 《...》
    m = re.search(r'《\[*.*?\]*》\s*(.*?)(?:呪文の解説|エネルギー消費|持続時間|前提条件|$)', body, re.DOTALL)
    if m:
        summary = m.group(1).strip()
        summary = re.sub(r'\s+', ' ', summary)
        if len(summary) > 10 and not summary.startswith("tyounekogami") and not summary.startswith("最終更新"):
            return summary[:200]
    lines = [l for l in body.split("\n") if len(l) > 10 and not any(k in l for k in ["■", "《", "tyounekogami", "最終更新", "Tweet", "参照"])]
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
    
    jp = re.sub(r'†', '', jp)
    if '精霊召喚/火霊' in jp:
        jp_display = f"**《火霊召喚》**<br>（精霊召喚/火霊）<br>{eng}"
    elif '精霊支配/火霊' in jp:
        jp_display = f"**《火霊支配》**<br>（精霊支配/火霊）<br>{eng}"
    elif '精霊作成/火霊' in jp:
        jp_display = f"**《火霊作成》**<br>（精霊作成/火霊）<br>{eng}"
    elif '旧名：' in jp:
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
table_5_spells = [s for s in spells if s.get('table_category') == 'Table_5']
table_6_spells = [s for s in spells if s.get('table_category') == 'Table_6']

print(f"Table 1 (Basic Fire): {len(table_1_spells)}")
print(f"Table 2 (Elemental): {len(table_2_spells)}")
print(f"Table 3 (Artillery MAS): {len(table_3_spells)}")
print(f"Table 4 (Death MDS): {len(table_4_spells)}")
print(f"Table 5 (Least of Spells): {len(table_5_spells)}")
print(f"Table 6 (Poison Fire): {len(table_6_spells)}")

md_output = []
md_output.append("# 火霊系呪文 (Fire Spells)")
md_output.append("")
md_output.append("本ドキュメントは、ガープス第4版『魔法大全』第5章（pp.34-38）および公式拡張サプリメント（『Magic: Artillery Spells』『Magic: Death Spells』『Magic: The Least of Spells』等）に準拠した、**全46種**の火霊系公式呪文アーカイブです。熱エネルギー励起、燃焼反応制御、火球・投射火焔、熱力学的防護、火のエレメンタル使役、ならびに2026年現代における結界都市防衛・軍事兵器工学・法規制（CR）の運用データを過不足なく完全網羅しています。")
md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 1. 火霊系魔術の力学体系")
md_output.append("")
md_output.append("火霊系呪文は、四大元素（地・水・火・風）の一角を担い、マナの熱励起を介して媒質の温度・燃焼反応速度・熱放射ベクトルを直接制御する魔術体系です。")
md_output.append("- **熱力学的出力限界**: ガープスマジック基準において、人間の術士単独での火力は《火球》（1〜3d）や《爆裂火球》の小火器〜手榴弾クラス（1d〜3dの熱・爆風破片相当）が上限であり、戦略級の大火災を単独詠唱で即時現出させることは不可能です。")
md_output.append("- **物理・化学燃焼との並行性**: 呪文によって生じた炎は、物理化学的燃焼と同じ熱エネルギー・光・煙・酸素消費を伴います。したがって消火器（粉末/炭酸ガス）やスプリンクラー、酸素遮断によって通常の火災と同様に消火・抑制が可能です（ただし《真なる火》等を除く）。")
md_output.append("")
md_output.append("### 1.1 主要火霊系呪文 前提条件ツリー (Prerequisite Tree)")
md_output.append("")
md_output.append("```mermaid")
md_output.append("graph TD")
md_output.append("    classDef spell fill:#0f172a,stroke:#38bdf8,stroke-width:1.5px,color:#ffffff;")
md_output.append("    ")
md_output.append("    Ignite[\"《発火》\"]:::spell --> CreateFire[\"《炎作成》\"]:::spell")
md_output.append("    Ignite --> ShapeFire[\"《炎変化》\"]:::spell")
md_output.append("    Ignite --> Extinguish[\"《消火》\"]:::spell")
md_output.append("    SeekFire[\"《炎探知》\"]:::spell --> CreateFire")
md_output.append("    ")
md_output.append("    ShapeFire --> PhantomFlame[\"《幻炎》\"]:::spell")
md_output.append("    Extinguish --> Fireproof[\"《防火》\"]:::spell")
md_output.append("    Extinguish --> SlowFire[\"《遅燃》\"]:::spell")
md_output.append("    SlowFire --> FastFire[\"《速燃》\"]:::spell")
md_output.append("    ")
md_output.append("    CreateFire & ShapeFire --> Heat[\"《加熱》\"]:::spell")
md_output.append("    Heat --> Cold[\"《冷却》\"]:::spell")
md_output.append("    Heat --> ResistCold[\"《防寒》\"]:::spell")
md_output.append("    Heat --> Warmth[\"《暖房》\"]:::spell")
md_output.append("    Heat --> ResistFire[\"《防熱》\"]:::spell")
md_output.append("    Heat --> BurningTouch[\"《炎の手》\"]:::spell")
md_output.append("    ")
md_output.append("    ShapeFire --> DeflectEnergy[\"《エネルギー屈折》\"]:::spell")
md_output.append("    CreateFire & ShapeFire --> FlameJet[\"《火炎噴射》\"]:::spell")
md_output.append("    ShapeFire & Extinguish --> Smoke[\"《濃煙》\"]:::spell")
md_output.append("    ")
md_output.append("    CreateFire --> RainOfFire[\"《火の雨》\"]:::spell")
md_output.append("    CreateFire & ShapeFire --> Fireball[\"《火球》\"]:::spell")
md_output.append("    Fireball --> ExplosiveFireball[\"《爆裂火球》\"]:::spell")
md_output.append("    Fireball --> FireCloud[\"《炎の雲》\"]:::spell")
md_output.append("    ")
md_output.append("    Heat --> FlamingWeapon[\"《火炎武器》\"]:::spell")
md_output.append("    FlamingWeapon --> FlamingMissiles[\"《炎の弓》\"]:::spell")
md_output.append("    ResistFire & FlameJet --> FlamingArmor[\"《炎の鎧》\"]:::spell")
md_output.append("    FlameJet & ResistFire --> BreatheFire[\"《火吹き*》\"]:::spell")
md_output.append("    BreatheFire --> BodyOfFlames[\"《肉体炎化*》\"]:::spell")
md_output.append("    ")
md_output.append("    CreateFire & ShapeFire --> EssentialFlame[\"《真なる火》\"]:::spell")
md_output.append("    CreateFire & ShapeFire --> SummonFireElem[\"《火霊召喚》\"]:::spell")
md_output.append("    SummonFireElem --> ControlFireElem[\"《火霊支配》\"]:::spell")
md_output.append("    SummonFireElem --> CreateFireElem[\"《火霊作成》\"]:::spell")
md_output.append("```")
md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 2. ガープス第4版『魔法大全』基本火霊系呪文（32種）")
md_output.append("")
md_output.append("| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |")
md_output.append("| :--- | :---: | :---: | :---: | :---: | :--- | :--- |")

for s in table_1_spells:
    md_output.append(format_spell_row(s))

md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 3. 四大精霊共通召喚・使役呪文（3種）")
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
md_output.append("『GURPS Magic: Artillery Spells（MAS）』および『GURPS Magic: Death Spells（MDS）』に収録された、熱・爆炎を戦略的弾幕・生体焼失へと昇華させた軍事拡張呪文です。")
md_output.append("")
md_output.append("| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |")
md_output.append("| :--- | :---: | :---: | :---: | :---: | :--- | :--- |")

for s in table_3_spells + table_4_spells:
    md_output.append(format_spell_row(s))

md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 5. 日常・民間簡単呪文 ＆ 複合呪文（Mtlos等 拡張 4種）")
md_output.append("")
md_output.append("『GURPS Magic: The Least of Spells（Mtlos）』に収録された低燃費の日常呪文および毒霊系連携呪文です。")
md_output.append("")
md_output.append("| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |")
md_output.append("| :--- | :---: | :---: | :---: | :---: | :--- | :--- |")

for s in table_5_spells + table_6_spells:
    md_output.append(format_spell_row(s))

md_output.append("")
md_output.append("---")
md_output.append("")
md_output.append("## 6. 2026年現代戦術・都市防衛・メガコーポ兵器における運用")
md_output.append("")
md_output.append("### 6.1 自衛隊・法執行機関の熱戦術バランス")
md_output.append("都市部での対魔獣・テロ制圧において、《火球》《火炎噴射》は手榴弾や火炎放射器と同等に強力ですが、閉所での酸欠や二次火災リスクが極めて高いため、警察（SAT）では《消火》《防熱》《濃煙》による突入支援が主用されます。自衛隊普通科の術士班では、《強化爆裂火球*》《火炎武器》が重装甲魔獣（オクタマイワシシ等）に対する装甲脆弱化（熱衝撃脆性）戦術として標準配備されています。")
md_output.append("")
md_output.append("### 6.2 メガコーポによる熱エネルギー制御特許と工業利用")
md_output.append("ヤマト重工の製鉄・超合金精錬ラインでは、《加熱》《真なる火》を用いた超高純度熱源プラントが稼働しており、化石燃料や外部電力に依存しないグリーン魔導熱源として独占特許化されています。また、テイコク製薬の極低温バイオ保管庫では《冷却》呪文による絶対零度近傍の温度維持が行われています。")
md_output.append("")
md_output.append("### 6.3 戦略熱破壊術式（MAS/MDS）の国際法規制（CR4）")
md_output.append("《塔なす炎*》《自爆》《肉体焼失*》は、広範囲無差別焼夷弾（ナパーム・白燐弾）と同等の非人道的大破壊をもたらすため、国際魔導協定（IMA）および防衛省訓令により**規制等級CR4（要特別軍事許可・非人道兵器条約規制）**に指定されています。")

full_content = "\n".join(md_output)

with open("world/magic/spells/fire.md", "w", encoding="utf-8") as f:
    f.write(full_content)

print(f"Successfully updated world/magic/spells/fire.md ({len(full_content)} chars)")
