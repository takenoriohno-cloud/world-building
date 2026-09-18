# 【実装計画書】第007号 カゲロウライオン（陽炎獅子／*Panthera leo solaris*）

- **対象仕様書**: `[.specify/specs/creatures/007_pyro_pride_lion.spec.md](file:///c:/Users/user/OneDrive/%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88/Antigravity/world-building/.specify/specs/creatures/007_pyro_pride_lion.spec.md)`
- **ステータス**: 監査完了・承認済 (Audited & Approved)
- **監査責任者**: 首席監査官ゼクスト

---

## 1. 実装計画チェックリスト ＆ 機械的突合エビデンス（Plan Checklists & Grep Evidence）

### 1.1 構成・フォーマット監査チェック（章節タイトル ＆ ナショジオ新規格Grep突合）
- [x] **新規格全9章構成の完全網羅（`creatures/007_pyro_pride_lion.md`）**:
  - [x] `## 1. 基本分類・早わかり（Basic Classification & Fast Facts）`（L5: 早わかり表・直感的サイズ比較・生息マップ・3点写真テーブル）
  - [x] `## 2. 伝承考証とマナ覚醒の架橋（Lore & Historical Bridge）`（L46: ネメアの獅子・セクメト神話・サムソン・2000年火霊変異史）
  - [x] `## 3. 生物学的特徴・ライフステージ（Biological Traits & Anatomy）`（L62: 骨格咬合力・耐熱鬣DR 8・太陽熱嚢・Mermaid生体熱解剖図・ライフステージ）
  - [x] `## 4. 生態・人間社会摩擦・繁殖育児（Ecology & Ethology）`（L110: 戦術的熱波包囲狩猟・Mermaidネットワーク図・マサイ族オラマイヨ・サファリ防衛）
  - [x] `## 5. ガープス第4版（GURPS 4th）戦闘データ`（L139: GURPS Stat Block・Grep突合済公式呪文）
  - [x] `## 6. 軍事対処・防護プロトコル（Military & Tactics）`（L188: 7.62mm AP/12.7mm M2重機関銃・ミリ波レーダー照準・消火急冷戦術）
  - [x] `## 7. 解体・食利用・素材採取（Cuisine & Harvesting）`（L210: Class-B熱嚢摘出プロトコル・太陽獅子ロースステーキ・先端素材相場）
  - [x] `## 8. 現場記録・調査員ログ（Field Log）`（L234: セレンゲティ第1特科サファリレンジャー隊長巡視記録）
  - [x] `## 9. 関連研究・派生種（Related Research & Subspecies）`（L246: サハラ灼熱亜種・カラハリ黒鬣種・メガコーポ特許情報）
- [x] **生物学的分類階級の明記**:
  - 哺乳綱 / 食肉目 / ネコ科 / ヒョウ属 / ライオン種 / 太陽獅子亜種 *Panthera leo solaris*（L14）
- [x] **ナショナルジオグラフィック流新要素の完全突合**:
  - [x] **早わかり表（Fast Facts）**: 和名命名規約（形態・羽色型）、学名語源、発生起源、食性、寿命、サイズ、脅威度、一次生息地（L7-22）
  - [x] **直感的サイズ比較（Relative Scale）**: サファリ用装甲4WD（全長4.8m・車高1.9m）および成人男性（180cm）との対比（L20）
  - [x] **生息・分布マップ（Distribution & Habitat Range Map）**: Natural Earth パブリックドメイン世界地図に基づく東アフリカ・サハラ南部マップ埋め込み（L28: `assets/creatures/007_pyro_pride_lion/pyro_lion_map.svg` / `pyro_lion_range_map.png`）
- [x] **視覚資料アセット配備（3点構成 / Class-B可食ジビエ種）**:
  - [x] `../assets/creatures/007_pyro_pride_lion/pyro_lion_wild.jpg`（L41: 野生ドキュメンタリー写真）
  - [x] `../assets/creatures/007_pyro_pride_lion/pyro_lion_mane_macro.jpg`（L41: 鬣ケラチン標本マクロ写真）
  - [x] `../assets/creatures/007_pyro_pride_lion/pyro_lion_cuisine.jpg`（L41: Class-B伝統料理『太陽獅子ロースステーキ』写真）

---

### 1.2 専門部署別・設定整合性チェックマトリックス（Grep客観突合）
- [x] **🐾 生態・生物調査部（鷹司 冴子 博士）**:
  - [x] 成体雄体重320〜420kg（SM +1）、咬合力1,200〜1,400 PSI（8,000〜9,500 N）、犬歯長8.5〜10cmの骨格筋量整合性（L19, L65-67）。
  - [x] 炭化チタン類似の生体耐熱ケラチン鬣（DR 8 / 熱・炎DR 15）および皮下「太陽熱嚢（*Saccus Solarithermalis* / 60〜180℃）」の解剖構造（L68-72, L74-98）。
  - [x] 雌獅子部隊の赤熱肉球（Thermal Footpads / Move 10・時速80km/h）による短距離熱突進（L91, L115）。
  - [x] Class-B（要免許ジビエ）における太陽熱嚢・火炎分泌腺の完全摘出プロトコルおよび太陽獅子ロース肉の滋養強壮生化学（L16, L212-220）。
- [x] **🌍 地理・環境調査部（陣内 隆文 調査官）**:
  - [x] 一次野生生息地（東アフリカ・セレンゲティ国立公園〜マサイマラ国立保護区アウトランド / 標高1,200〜1,800m）の特定（L22, L30-33）。
  - [x] 二次生息地（サハラ・オアシス特異点南部サヘル移行帯ステップ）の地誌連動（L22, L32）。
  - [x] セレンゲティ観光サファリ回廊および防護フェンス境界摩擦（L128-130）。
- [x] **🏛️ 歴史・社会制度考証部（V・シュルツ 特命調査員）**:
  - [x] 古典文献考証（ギリシャ神話ネメアの獅子、エジプト神話セクメト、旧約聖書サムソン）からの学術引用（L49-55）。
  - [x] 2000年サハラ特異点マナ噴出による急速変異史（L57-59）。
  - [x] マサイ族伝統儀礼オラマイヨの対魔槍への変容史（L131-133）。
  - [x] ヤマト重工（特許第2024-88912号・断熱コーティング）vs テイコク製薬（特許第2025-01443号・温熱パッチ）の特許紛争および密猟PMC抗争史（L134-136, L252-255）。
- [x] **⚡ 魔導科学・理論研究部（クリスティナ・黒田 所長）**:
  - [x] **公式GURPS呪文・生体異能 Grep突合完了**:
    - 《加熱 / Heat》: `world/magic/spells/fire.md`（L37）と突合一致（L181）。
    - 《火球 / Fireball》: `world/magic/spells/fire.md`（L50）と突合一致（L182）。
    - 《火吹き / Breathe Fire》: `world/magic/spells/fire.md`（L56）と突合一致（L183）。
    - 生体特徴 `Terror（戦慄咆哮）`: `world/magic/spells/mind.md`（L36）と突合一致（L170）。
  - [x] 光学的陽炎励起（熱対流による光線屈折・光学照準判定 -4 ペナルティ）の物理光学力学（L102-105, L184）。
  - [x] 12.7mm M2重機関銃（約18,000J）および7.62mm AP弾によるDR 8突破弾道力学（L178-180, L192-196）。
  - [x] GURPS 4th Stat Block（ST 24, DX 13, IQ 6, HT 12, HP 28, FP 16, SM +1, 移動力8/雌10, 咬合2d+2 cr/pi, 鉤爪2d cut + 1d-1 burn）（L140-185）。
- [x] **📸 視覚・音響資料部（蓮見 蓮 プロデューサー）**:
  - [x] 音響周波数ログ（18〜120Hz インフラサウンド低周波地響き咆哮 / 音圧 120dB）（L87, L116）。
  - [x] Mermaid生体熱解剖連関図（`flowchart TD / subgraph CRANIAL/THORAX/MOTOR`）の構文検証（L74-98）。
  - [x] Mermaid戦術包囲狩猟ネットワーク図（`flowchart LR`）の構文検証（L119-125）。
- [x] **⚖️ 【世界観統括・憲章監査室】（首席監査官ゼクスト）**:
  - [x] 憲章5大観点（26年急速変異、生体媒介原則、通常兵器・重機関銃バランス、日常サファリ境界、Class-B食肉適性）の完全準拠。
  - [x] シングル・ソース・オブ・トゥルース（`AGENTS.md` / `constitution.md` / `doc/questions_and_answers.md` Q15・Q37）との無矛盾性確認。

---

## 2. 監査承認ゲート判定 (Gate 2 Audit Gate)
- **Gate 2 監査判定**: **【PASS / 進行承認】**
- **監査コメント**: 全チェック項目のGrep突合エビデンス（章節タイトル・ナショジオ新規格要素・GURPS公式呪文ファイル突合・解剖/狩猟Mermaid構文・行番号エビデンス）を確認。客観的エビデンスに基づく完全適合を認定する。
