# 【実装計画書】第002号 シロエリワシジシ［白襟鷲獅子］（サンダー・グリフォン／*Gryphus fulgurans*）再構築実装計画

---

## 1. 実装チェックリスト ＆ 機械的突合エビデンス

### 1.1 構成・フォーマット監査チェック（TEMPLATE.md 全9章・全節との1対1突合）
- [x] `## 1. 基本分類・早わかり（Basic Classification & Fast Facts）`（`creatures/002_thunder_gryphon.md:5`）
  - [x] 標準和名: **シロエリワシジシ［白襟鷲獅子］**（形態・羽色型）（`creatures/002_thunder_gryphon.md:9`）
  - [x] 和名命名規約、英名/通称、学名（*Gryphus fulgurans*）、生物学的分類（門・綱・目・科・属・種）（`creatures/002_thunder_gryphon.md:10-14`）
  - [x] 発生起源（古代覚醒種 ＋ 急速マナ共生変異）、資源・管理区分（要処理種 Class-B）、食性、寿命（`creatures/002_thunder_gryphon.md:15-18`）
  - [x] サイズ・重量（体長3.2〜3.8m / 翼開長9.5〜11.5m / 体重480〜620kg / SM +2）（`creatures/002_thunder_gryphon.md:19`）
  - [x] **直感的サイズ比較（成人男性180cm / アフリカゾウ・軽戦闘機との比較）**（`creatures/002_thunder_gryphon.md:20`）
  - [x] 脅威度ランク（Threat Level: III）、主要生息域（一次生息地：中央アジア・アルタイ高山帯、二次生息地：北米カスケード・日本北アルプス）（`creatures/002_thunder_gryphon.md:21-22`）
  - [x] **生息・分布マップ（一次生息地特化 SVG & PNG）**（`assets/creatures/002_thunder_gryphon/gryphon_map.svg` / `creatures/002_thunder_gryphon.md:28`）
  - [x] **視覚資料アーカイブ（野生生態写真、標本図解の完全保全配備）**（`creatures/002_thunder_gryphon.md:38-44`）
- [x] `## 2. 伝承考証とマナ覚醒の架橋（Lore & Historical Bridge）`（`creatures/002_thunder_gryphon.md:46`）
  - [x] `### 2.1 原典・古典文献の記録`（ヘロドトス『歴史』4巻、大プリニウス『博物誌』10巻、セビリアのイシドールス『語源』）（`creatures/002_thunder_gryphon.md:48-55`）
  - [x] `### 2.2 2000年マナ覚醒による生体科学的架橋`（アルタイ金鉱脈特異点、雷霊マナ噴出、古代種覚醒、急速共生変異）（`creatures/002_thunder_gryphon.md:57-61`）
- [x] `## 3. 生物学的・魔導的特徴（Biological & Thaumaturgical Traits）`（`creatures/002_thunder_gryphon.md:63`）
  - [x] `### 3.1 解剖学的特徴・骨格・運動機能`（Mermaid骨格図、竜骨突起・骨盤結合、ケラチン爪、咬合力1,800 PSI、240km/h急降下）（`creatures/002_thunder_gryphon.md:65-92`）
  - [x] `### 3.2 魔導生化学・生体エネルギー循環`（ライデン腺 / *Organum Fulgurans*、100万V大気摩擦蓄電・心筋放電機序）（`creatures/002_thunder_gryphon.md:94-98`）
  - [x] `### 3.3 生態・行動パターン・ライフサイクル`（高山岩壁営巣、雷雲追尾狩猟、一夫一妻・ヘルパー育児）（`creatures/002_thunder_gryphon.md:100-105`）
- [x] `## 4. 人間社会との関係・共生と摩擦（Human-Creature Conflict & Coexistence）`（`creatures/002_thunder_gryphon.md:107`）
  - [x] `### 4.1 軍事・航空防衛・駆除体制`（Mermaid流通防衛図、航空コンボイ襲撃、20mm CIWS、スティンガー迎撃）（`creatures/002_thunder_gryphon.md:109-141`）
  - [x] `### 4.2 魔獣間クロス・リレーション`（第001号 剛毛巌猪、第010号 アラビアルフ、第014号 旋風鎌鼬等との関係）（`creatures/002_thunder_gryphon.md:143-150`）
  - [x] `### 4.3 産業利用・メガコーポ利権`（アレス社電磁シールド特許、ヤマト重工防空CIWS、パイクプレイス市場）（`creatures/002_thunder_gryphon.md:152-156`）
- [x] `## 5. 魔導工学・魔法理論的アプローチ（Thaumaturgical Mechanics）`（`creatures/002_thunder_gryphon.md:158`）
  - [x] `### 5.1 GURPS Magic基準数理モデル`（《電撃》《連鎖電撃》《飛行》のマナ消費・発動出力）（`creatures/002_thunder_gryphon.md:160-168`）
  - [x] `### 5.2 生体防御・障壁力学`（羽毛電磁シールド、対小火器DR 4/6、20mm徹甲弾・対空爆風貫通力学）（`creatures/002_thunder_gryphon.md:170-177`）
  - [x] `### 5.3 上位存在・アストラル原型・アビス因果`（黄金鷲獅子王・ゼウス雷霆機縁、アンチ・アビス雷霊純性）（`creatures/002_thunder_gryphon.md:179-184`）
- [x] `## 6. GURPS 4th 準拠ステータス（GURPS Stat Block）`（`creatures/002_thunder_gryphon.md:186`）
  - [x] 成体基本値（SM +2, ST 26, DX 14, IQ 5, HT 13, HP 26, Move 24［急降下時］, DR 4［翼・前肢 DR 6］）（`creatures/002_thunder_gryphon.md:188-217`）
  - [x] `### 6.1 主級・長老個体（Elder Alpha / 翼開長13m・SM +3）` の追加ステータス（`creatures/002_thunder_gryphon.md:219-225`）
- [x] `## 7. 食・素材利用・バイオハザード評価（Culinary & Material Assets）`（`creatures/002_thunder_gryphon.md:227`）
  - [x] `### 7.1 解体・危険部位摘出プロトコル`（Mermaid解体手順図、Class-B下処理：ライデン腺の完全絶縁摘出・アース放電手順）（`creatures/002_thunder_gryphon.md:229-253`）
  - [x] `### 7.2 ジビエ料理・メガコーポ特許素材`（『鷲獅子胸肉の瞬間燻製ロースト』、導電性羽毛防弾繊維）（`creatures/002_thunder_gryphon.md:255-260`）
- [x] `## 8. 音響・通信・観測記録（Acoustic Logs & Field Observations）`（`creatures/002_thunder_gryphon.md:262`）
  - [x] `### 8.1 音響周波数・バイオアコースティクス`（音響スペクトログラム、14Hz超低周波羽ばたき音、130dB放電衝撃波、3.2kHz威嚇啼き声）（`creatures/002_thunder_gryphon.md:264-282`）
  - [x] `### 8.2 フィールド観測ログ`（シアトル防空司令部・アレス航空護衛部隊迎撃交戦ログ）（`creatures/002_thunder_gryphon.md:284-297`）
- [x] `## 9. 参考文献・公式アーカイブ（References & Archival Sources）`（`creatures/002_thunder_gryphon.md:299-310`）
  - [x] 古典文献、メガコーポ防空白書、GURPS公式呪文アーカイブ（`air.md:67`, `air.md:69`, `weather.md`）

---

### 1.2 専門部署別・設定整合性チェックマトリックス（Grep客観突合）

| 担当部署 | 担当ペルソナ | 検証項目・客観エビデンス | ファイル・行番号 |
| :--- | :--- | :--- | :--- |
| **🐾 生態・生物調査部** | 鷹司 冴子 博士 | 猛禽竜骨突起・ネコ科骨盤の結合解剖学、咬合力1,800 PSI、ライデン腺（100万V蓄電） | `creatures/002_thunder_gryphon.md:65-98` |
| **🌍 地理・環境調査部** | 陣内 隆文 調査官 | 一次野生生息地（アルタイ山脈金鉱脈高山帯）、二次生息地（カスケード山脈・北アルプス） | `creatures/002_thunder_gryphon.md:21-36` |
| **🏛️ 歴史・社会制度考証部** | V・シュルツ 特命調査員 | ヘロドトス『歴史』4巻13/27節、大プリニウス『博物誌』10巻、アレス社防空利権、Class-B法規 | `creatures/002_thunder_gryphon.md:48-61, 152-156` |
| **⚡ 魔導科学・理論研究部** | クリスティナ・黒田 所長 | 公式呪文《電撃》（`air.md:67`）、《連鎖電撃》（`air.md:69`）、《飛行》（`air.md:71`）、DR 4/6貫通弾道学 | `creatures/002_thunder_gryphon.md:160-225` |
| **📸 視覚・音響・資料記録部** | 蓮見 蓮 プロデューサー | 既存画像2点保全、中央アジア・アルタイ特化SVG/PNG生息マップ、14Hz/130dB音響設計 | `assets/creatures/002_thunder_gryphon/*` |
| **⚖️ 憲章監査室** | 首席監査官ゼクスト | 最上位憲章・命名規約（形態・羽色型）・シングルソースオブトゥルース | `AGENTS.md`, `GEMINI.md` |
