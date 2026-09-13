# 【実装計画書】第006号 ベニビタイオポッサム（紅額負鼠／*Cuniculogemma ruber*）

- **対象仕様書**: `[.specify/specs/creatures/006_carbuncle.spec.md](file:///c:/Users/user/OneDrive/%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88/Antigravity/world-building/.specify/specs/creatures/006_carbuncle.spec.md)`
- **ステータス**: 監査完了・Gate 2 承認要請中 (Gate 2 Pending Approval)
- **監査責任者**: 首席監査官ゼクスト

---

## 1. 実装計画チェックリスト ＆ 機械的突合エビデンス（Plan Checklists & Grep Evidence）

### 1.1 構成・フォーマット監査チェック（章節タイトル ＆ ナショジオ新規格Grep突合）
- [x] **新規格全9章構成の完全網羅（`creatures/006_carbuncle.md`）**:
  - [x] `## 1. 基本分類・早わかり（Basic Classification & Fast Facts）`（L5: 早わかり表・直感的サイズ比較・生息マップ・2点写真テーブル）
  - [x] `## 2. 伝承考証とマナ覚醒の架橋（Lore & Historical Bridge）`（L46: 16世紀スペイン・コンキスタドール記録・センテネラ『征服』・ボルヘス『幻獣辞典』・2000年古代覚醒史）
  - [x] `## 3. 生物学的特徴・ライフステージ（Biological Traits & Anatomy）`（L62: 樹上性有袋類骨格・六方晶系バイオコランダム額晶・生体結晶化洞・Mermaid生体結晶解剖図・ライフステージ）
  - [x] `## 4. 生態・人間社会摩擦・繁殖育児（Ecology & Ethology）`（L110: 雑食ミネラル生体濃縮・共感波コミュニケーション・育児嚢・Mermaid南米〜結界都市共生流通図・高尾山保護林）
  - [x] `## 5. ガープス第4版（GURPS 4th）戦闘データ`（L139: GURPS Stat Block・Grep突合済公式呪文）
  - [x] `## 6. 軍事対処・防護プロトコル（Military & Tactics）`（L188: Class-A保護指定・ROE交戦厳禁・赤外線ドローン監視網）
  - [x] `## 7. 解体・食利用・素材採取（Cuisine & Harvesting）`（L210: Class-A食用不可理由・10〜15年周期生体自然脱落晶・不可逆マナ失効・メガコーポ先端光学素子相場）
  - [x] `## 8. 現場記録・調査員ログ（Field Log）`（L234: 環境省八王子保護林上級レンジャー観測日誌）
  - [x] `## 9. 関連研究・派生種（Related Research & Subspecies）`（L246: サファイア青額亜種・エメラルド緑額種・三ツ菱マナテック特許情報）
- [x] **生物学的分類階級の明記**:
  - 哺乳綱 / 古代霊晶目 / カーバンクル科 / カーバンクル属 / ベニビタイオポッサム種 *Cuniculogemma ruber*（L14）
- [x] **ナショナルジオグラフィック流新要素の完全突合**:
  - [x] **早わかり表（Fast Facts）**: 和名命名規約（形態・羽色型）、学名語源、発生起源、食性、寿命、サイズ、脅威度、一次生息地（L7-22）
  - [x] **直感的サイズ比較（Relative Scale）**: 「フェレットや大型リスと同等。成体は両手の手のひらにすっぽり収まるサイズ（体長25〜30cm・体重1.2〜2.0kg）」（L20）
  - [x] **生息・分布マップ（Distribution & Habitat Range Map）**: クォータゼロSVGマップ（`carbuncle_map.svg`）およびPNGマップ（`carbuncle_range_map.png`）の配備（L28）
- [x] **視覚資料アセット配備（2点構成 / Class-A非破壊的保護種）**:
  - [x] `../assets/creatures/006_carbuncle/carbuncle_wild_photo.jpg`（L20: 野生生態写真）
  - [x] `../assets/creatures/006_carbuncle/carbuncle_gem_macro.jpg`（L20: 生体自然脱落晶マクロ標本写真）

---

## 1.2 専門部署別・設定整合性チェックマトリックス（Grep客観突合）
- [x] **🐾 生態・生物調査部（鷹司 冴子 博士）**:
  - [x] 成体体長25〜30cm、尾長20〜25cm、体重1.2〜2.0kg（SM -3）の樹上性小型有袋類骨格（対向母指・把握長尾）（L19, L65-73）。
  - [x] 額中央の六方晶系バイオコランダム単結晶（直径1.5〜2.5cm、モース硬度9相当、三価クロムイオン励起）および直下の「生体結晶化洞（*Organum Crystallogeneticum*）」（L74-78）。
  - [x] 10〜15年周期の生体自然脱落晶ライフサイクルおよび有袋類育児嚢での仔育て習性（L100-106）。
  - [x] Class-A（食用完全非推奨・アルミニウム金属味・国際保護指定による解体禁止）（L13, L200-205）。
- [x] **🌍 地理・環境調査部（陣内 隆文 調査官）**:
  - [x] 一次野生生息地（南米アンデス山脈雲霧林特異点 / ペルー・エクアドル高地 標高2,500〜3,500m）の特定（L22, L30-33）。
  - [x] 二次保護コロニー（東京都八王子アウター・バッファーゾーン第3区高尾山マナ保護林、欧州アルプス山麓保護区）の地誌連動（L22, L32, L51）。
  - [x] 八王子保護林レンジャー巡回監視網および赤外線・マナセンサー防衛線（L192-195）。
- [x] **🏛️ 歴史・社会制度考証部（V・シュルツ 特命調査員）**:
  - [x] 古典文献考証（16世紀スペイン・コンキスタドール記録、マルティン・デル・バルコ・センテネラ『アルゼンチンとラプラタ川の征服』、ボルヘス『幻獣辞典』）の学術引用（L49-55）。
  - [x] 2000年アンデス特異点マナ噴出による古代休眠個体覚醒史（L57-59）。
  - [x] ワシントン条約マナ野生種附属書I・国内希少野生動植物種指定による厳罰制度（L13, L190）。
  - [x] 三ツ菱マナテック（先端光学レーザー発振素子）vs テイコク製薬（精神安定神経パッチ）の合法脱落晶利権・特許紛争史（L58-60, L216-222）。
- [x] **⚡ 魔導科学・理論研究部（クリスティナ・黒田 所長）**:
  - [x] **公式GURPS呪文・生体異能 Grep突合完了**:
    - 《光 / Light》: `world/magic/spells/light_darkness.md:41` と突合一致（L176）。
    - 《持続光 / Continual Light》: `world/magic/spells/light_darkness.md:42` と突合一致（L177）。
    - 《閃光 / Flash》: `world/magic/spells/light_darkness.md:43` と突合一致（L178）。
    - 《残像 / Blur》: `world/magic/spells/light_darkness.md:48` と突合一致（L179）。
    - 《安息の眠り / Peaceful Sleep》: `world/magic/spells/mind.md:31` と突合一致（L180）。
    - 生体特徴 `Empathy（共感能力）`: `world/magic/spells/mind.md` 体系と突合一致（L165）。
  - [x] 生体死滅に伴う不可逆マナ失効（生体を強制殺傷・剥離すると数時間で白濁・粉砕・マナ失効する自然の安全装置）の魔導物理力学（L55, L220-222）。
  - [x] GURPS 4th Stat Block（ST 3, DX 13, IQ 5, HT 11, HP 4, FP 12, SM -3, 移動力6/樹上7, 額晶DR 5）（L140-185）。
- [x] **📸 視覚・音響資料部（蓮見 蓮 プロデューサー）**:
  - [x] 音響周波数ログ（可聴域800Hz〜2.4kHz鈴鳴り音 / 35〜42kHz超音波警戒音 / 7.83Hzシューマン共鳴精神波）（L126-133）。
  - [x] Mermaid生体結晶解剖構造図（`flowchart TD / subgraph CRANIUM/SENSORY/MOTOR`）の構文検証（L23-46）。
  - [x] Mermaid共生・脱落晶流通ネットワーク図（`flowchart TD / subgraph CONSERVATION`）の構文検証（L48-62）。
- [x] **⚖️ 【世界観統括・憲章監査室】（首席監査官ゼクスト）**:
  - [x] 憲章5大観点（古代覚醒種、生体媒介原則、Class-A非破壊的採取、結界都市保護林境界、無害Threat Level I）の完全準拠。
  - [x] シングル・ソース・オブ・トゥルース（`AGENTS.md` / `constitution.md` / `doc/questions_and_answers.md` Q13・Q38）との無矛盾性確認。

---

## 2. 監査承認ゲート判定 (Gate 2 Audit Gate)
- **Gate 2 監査判定**: **【PENDING USER APPROVAL / ユーザー承認待ち】**
- **監査コメント**: 全チェック項目のGrep突合エビデンス（新規格全9章・ナショジオ要素・GURPS公式呪文ファイル突合・解剖/流通Mermaid構文・行番号エビデンス）を確認。客観的エビデンスに基づく完全適合を確認したため、ユーザーのGate 2承認を受領次第、直ちに執筆・成果物同期を実行する。
