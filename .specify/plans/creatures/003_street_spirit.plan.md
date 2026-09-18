# 【実装計画書】第003号 ガイロセイレイ［街路精霊］（Urban Street Spirit / *Spiritus urbanus asphalti*）再構築実装計画

- **対象仕様書**: `[.specify/specs/creatures/003_street_spirit.spec.md](file:///c:/Users/user/OneDrive/%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88/Antigravity/world-building/.specify/specs/creatures/003_street_spirit.spec.md)`
- **対象出力ファイル**: `[creatures/003_urban_street_spirit.md](file:///c:/Users/user/OneDrive/%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88/Antigravity/world-building/creatures/003_urban_street_spirit.md)`
- **ステータス**: 監査完了・承認済 (Audited & Approved)
- **監査責任者**: 首席監査官ゼクスト

---

## 1. 実装チェックリスト ＆ 機械的突合エビデンス（Plan Checklists & Full Hierarchy Grep Evidence）

### 1.1 構成・フォーマット監査チェック（TEMPLATE.md 全9章・全20節ディレクトリ構造との1対1突合）
- [x] `## 1. 基本分類・早わかり（Basic Classification & Fast Facts）`（`creatures/003_urban_street_spirit.md:5`）
  - [x] 標準和名: **ガイロセイレイ［街路精霊］**（環境・生息域型）（`creatures/003_urban_street_spirit.md:9`）
  - [x] 和名命名規約、英名/通称、学名（*Spiritus urbanus asphalti*）、学名語源（`creatures/003_urban_street_spirit.md:10-13`）
  - [x] 生物学的分類（門: 霊体門 / 綱: 精霊綱 / 目: 都市精霊目 / 科: 街路霊科 / 属: 街路精霊属 / 種: 街路精霊 / 亜種: シアトル原名亜種・東京湾岸適応型）（`creatures/003_urban_street_spirit.md:14`）
  - [x] 発生起源（シャーマニズム召喚霊体）、資源・管理区分（汚染・霊体種 Class-C）、食性、寿命（`creatures/003_urban_street_spirit.md:15-18`）
  - [x] サイズ・重量（具現時体高 1.8〜2.4m / 肩幅 1.2〜1.6m / 具現質量 350〜600kg / SM +1）（`creatures/003_urban_street_spirit.md:19`）
  - [x] **直感的サイズ比較（成人男性180cm / 軽装甲パトロール車両 車重2.5tとの比較）**（`creatures/003_urban_street_spirit.md:20`）
  - [x] 脅威度ランク（Threat Level: II）、主要生息域（一次生息地：北米シアトル第4スラム地区、二次生息地：東京湾岸スラム・五日市街道廃墟群）（`creatures/003_urban_street_spirit.md:21-22`）
  - [x] `### 生息・分布マップ（Distribution & Habitat Range Map）`（シアトル多層スラム〜東京湾岸特化 完全規格SVGマップ）（`creatures/003_urban_street_spirit.md:26`）
  - [x] `### 視覚資料アーカイブ（Visual Archive）`（野生召喚写真・標本図解の保全配備）（`creatures/003_urban_street_spirit.md:38`）
    - [x] `../assets/images/003_urban_street_spirit.jpg`（標本図解 / `creatures/003_urban_street_spirit.md:42`）
    - [x] `../assets/images/003_urban_street_spirit_wildlife.jpg`（野生召喚写真 / `creatures/003_urban_street_spirit.md:42`）
- [x] `## 2. 伝承考証とマナ覚醒の架橋（Lore & Historical Bridge）`（`creatures/003_urban_street_spirit.md:47`）
  - [x] `### 2.1 原典・民俗伝承の記録`（古代ローマ『ゲニウス・ロキ / Genius Loci』伝承、ストリート・フォークロア）（`creatures/003_urban_street_spirit.md:49`）
  - [x] `### 2.2 2000年マナ覚醒による生体科学的架橋（召喚・変異の経緯）`（**【特別要件①】** 2000年マナ覚醒以降、先住民系メタヒューマンが確立したスプレーグラフィティ召喚プロトコル）（`creatures/003_urban_street_spirit.md:55`）
- [x] `## 3. 生物学的特徴・ライフステージ（Biological Traits & Anatomy）`（`creatures/003_urban_street_spirit.md:61`）
  - [x] `### 3.1 外見・解剖学的身体構造（召喚維持・マナ供給構造）`（**【特別要件②】** Mermaid霊核・外殻結合図、アストラル霊核、外殻DR 7、廃鉄筋骨格、ネオン放電管、PM2.5スモッグ）（`creatures/003_urban_street_spirit.md:63`）
  - [x] `### 3.2 ライフステージと霊的寿命・送還サイクル`（**【特別要件④】** 召喚・励起、使役維持1FP/分、送還・瓦礫崩落、野良悪霊化リスク）（`creatures/003_urban_street_spirit.md:106`）
- [x] `## 4. 生態・食物連鎖・人間社会との摩擦（Ecology & Human Conflict）`（`creatures/003_urban_street_spirit.md:118`）
  - [x] `### 4.1 食性・マナ供給代謝`（**【特別要件②】** 排気ガス煤煙・騒音・怒りの集合思念還元代謝、Mermaid循環図）（`creatures/003_urban_street_spirit.md:120`）
  - [x] `### 4.2 魔獣間クロス・リレーション（相互作用）`（第001号 オクタマイワシシ、第002号 シロエリワシジシとの相互作用）（`creatures/003_urban_street_spirit.md:138`）
  - [x] `### 4.3 人間社会との摩擦・使役任務・防衛行動`（**【特別要件③】** Ares/Knight Errant治安戦、スラムゲリラ防衛、PM2.5煙幕撤退支援）（`creatures/003_urban_street_spirit.md:144`）
- [x] `## 5. 魔導科学・上位神性・背景ロア（Thaumaturgical Theory & Lore）`（`creatures/003_urban_street_spirit.md:152`）
  - [x] `### 5.1 魔力現象と発現メカニズム（GURPS公式呪文エビデンス）`（**【特別要件①】** 《地霊召喚》《精霊支配》《精霊作成》生体励起、生体媒介原則・電子機器非干渉）（`creatures/003_urban_street_spirit.md:154`）
  - [x] `### 5.2 音響・周波数・生体通信特性（Acoustic & Resonance Analysis）`（音響スペクトログラム、32Hz地鳴り、60Hz電位ハム、12.5kHzネオン放電）（`creatures/003_urban_street_spirit.md:165`）
  - [x] `### 5.3 上位存在・アビス因果・メガコーポ伏線`（都市集合無意識原型、地下アビス汚染耐性）（`creatures/003_urban_street_spirit.md:186`）
- [x] `## 6. 交戦マニュアル・都市防災コラム（Combat Manual & Civil Defense）`（`creatures/003_urban_street_spirit.md:194`）
  - [x] `### 6.1 GURPS 4th Stat Block（戦闘データ）`（`creatures/003_urban_street_spirit.md:196`）
    - [x] `#### 【具現化成体（Standard Materialized）】`（SM +1, ST 18, DX 11, IQ 8, HT 12, HP 22, Move 6, DR 7）（`creatures/003_urban_street_spirit.md:198`）
    - [x] `#### 【暴走・大型野良霊（Greater Urban Elemental）】`（SM +2, ST 24, HP 30, DR 10）（`creatures/003_urban_street_spirit.md:242`）
  - [x] `### 6.2 推奨火器・防護装備`（12.7mm M2重機関銃、12 Gaugeスラッグ弾、高圧放水砲、除霊符）（`creatures/003_urban_street_spirit.md:246`）
  - [x] `### 6.3 市民防災メモ ＆ 専門家の知恵袋`（シアトル治安指針、陣内調査官知恵袋）（`creatures/003_urban_street_spirit.md:250`）
- [x] `## 7. 解体・ジビエ食文化・料理レシピ（Harvesting & Cuisine）`（`creatures/003_urban_street_spirit.md:265`）
  - [x] `### 7.1 解体プロトコルと市場相場（Class-C 非可食・除染）`（Mermaid除染抽出図、アーバン・エーテル・スラグ回収）（`creatures/003_urban_street_spirit.md:267`）
  - [x] `### 7.2 伝統料理・メガコーポスペシャリテ（※食用絶対不可警報 ＆ 代替スラムコラム）`（Class-C完全非可食警告、ストリート・シャーマン風タコス本格レシピ）（`creatures/003_urban_street_spirit.md:288`）
  - [x] `### 7.3 産業素材・医療利用`（アーバン・エーテル・スラグ、帯電ネオンカレット相場）（`creatures/003_urban_street_spirit.md:306`）
- [x] `## 8. 現場記録・通信ログ（Field Logs & Transcripts）`（シアトル治安交戦記録）（`creatures/003_urban_street_spirit.md:315`）
- [x] `## 9. 参考文献・典拠資料（References）`（古典文献、治安白書、GURPS公式アーカイブ elemental_spirit.md:41, 43, 44）（`creatures/003_urban_street_spirit.md:336`）
- [x] `## 脚注・専門部署査定メモ（Persona Footnotes）`（`creatures/003_urban_street_spirit.md:350`）
  - [x] 全6専門ペルソナ（ゼクスト、シュルツ、クリスティナ、陣内、鷹司、蓮見）による小粋な冗談交じりの査定メモ配備（`creatures/003_urban_street_spirit.md:352-369`）
- [x] **Mermaid構造図の視認性確保**:
  - [x] 全暗色ノード（`fill`）に `color:#ffffff` を明示指定（`creatures/003_urban_street_spirit.md:86-92, 131-135, 276-280`）

---

### 1.2 専門部署別・設定整合性チェックマトリックス（Grep客観突合）

| 担当部署 | 担当ペルソナ | 検証項目・客観エビデンス | 本文参照行 ↔ 脚注定義行 |
| :--- | :--- | :--- | :--- |
| **🐾 生態・生物調査部** | 鷹司 冴子 博士 | Class-C完全非可食判定、PM2.5煤煙・重金属スラッジ毒性、アーバン・エーテル・スラグ抽出 | `creatures/003_urban_street_spirit.md:104` ↔ `L364` (`[^takatsukasa_1]`) |
| **🌍 地理・環境調査部** | 陣内 隆文 調査官 | 一次発祥地（シアトル・レイン・ディストリクト）、国内使役地（東京湾岸居留区・五日市街道）、路地裏迎撃戦 | `creatures/003_urban_street_spirit.md:146` ↔ `L361` (`[^jinnai_1]`) |
| **🏛️ 歴史・社会制度考証部** | V・シュルツ 特命調査員 | 古代ローマ『ゲニウス・ロキ（Genius Loci）』伝承、近代ストリートシャーマニズム、Ares/Knight Errant治安抗争史 | `creatures/003_urban_street_spirit.md:51` ↔ `L355` (`[^schulz_1]`) |
| **⚡ 魔導科学・理論研究部** | クリスティナ・黒田 所長 | GURPS公式呪文《地霊召喚》《精霊支配》《精霊作成》（`elemental_spirit.md:41,43,44`）、外殻DR 7、ネオンアーク放電2d | `creatures/003_urban_street_spirit.md:163` ↔ `L358` (`[^kuroda_1]`) |
| **📸 視覚・音響・資料記録部** | 蓮見 蓮 プロデューサー | 既存画像2点保全、シアトル多層スラムSVGマップ、32Hz地鳴り/60Hzハム/12.5kHz放電音響設計、Mermaid文字色 `color:#ffffff` | `creatures/003_urban_street_spirit.md:184` ↔ `L367` (`[^hasumi_1]`) |
| **⚖️ 憲章監査室** | 首席監査官ゼクスト | 最上位憲章適合、標準和名【環境・生息域型】、Class-C法規制、シングルソースオブトゥルース（Q41） | `creatures/003_urban_street_spirit.md:16` ↔ `L352` (`[^zext_1]`) |

---

## 2. 監査承認ゲート判定 (Gate 2 Audit Gate)
- **Gate 2 監査判定**: **【PASS / 監査承認済】**
- **監査コメント**: 全9章・全20節・全小見出しのディレクトリ階層構造（`## 1.`〜`## 9.` および `### 1.1`〜`### 7.3`）、4大特別要件（召喚経緯・維持マナ・使役任務・霊的寿命）、GURPS公式呪文ファイル突合、Mermaid文字色視認性、および全6専門ペルソナ脚注定義の完全一致エビデンス（行番号レベル）を確認。客観的エビデンスに基づく厳格な適合性を認定する。
