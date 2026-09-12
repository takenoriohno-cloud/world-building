# 【実装計画書】第008号：幽光星海月 アストラル・ネビュラ・ジェリー (Astral Nebula Jelly)

- **作成日**: 2026-09-12
- **ステータス**: 実装完了・監査検証済み (Completed)
- **対象仕様書**: [.specify/specs/creatures/008_astral_nebula_jelly.spec.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/specs/creatures/008_astral_nebula_jelly.spec.md)
- **対象魔獣ファイル**: [creatures/008_astral_nebula_jelly.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/creatures/008_astral_nebula_jelly.md)

---

## 1. 実装計画チェックリスト（全専門部署チェックマトリックス）

| 担当部署 | 検証項目・客観的エビデンス要件 | 判定 |
| :--- | :--- | :---: |
| **【世界観統括・憲章監査室】<br>ゼクスト 首席監査官** | `TEMPLATE.md` 準拠の全9章構成の完全実装。<br>・対象: `creatures/008_astral_nebula_jelly.md` 全9章（L5, L29, L45, L91, L131, L156, L234, L272, L299）<br>・憲章整合性: 時間軸（2000年覚醒から26年 / L40）、完全並行＆生体媒介（L133-142）、三段階分類（Class-B / L16, L237）。 | [x] 合格 |
| **① 生態・生物調査部<br>鷹司 冴子 博士** | 鉢クラゲ綱（*Aurelia*等）の比較解剖学（水分率97.2%アストラルゲル、星核嚢、散在神経環、刺胞網 / L48-78）。<br>・幼体（ポリプ期 / L81-82）→ 成熟成体（傘径2.5〜4.5m / L83-84）→ 巨星主級（Elder Alpha「星雲核」傘径5.5〜6.5m / L85-88, L205-210）。<br>・ミョウバン粗塩漬けによる刺胞毒不活化プロトコル（L238-241）と銀座料亭「星海月薄造り・土佐酢ジュレ仕立て」の本格レシピ記述（L246-260）。 | [x] 合格 |
| **② 地理・環境調査部<br>陣内 隆文 調査官** | **【原典発祥地マッピング規約】**の完全適用。<br>・一次生息地: マリアナ海溝「太平洋アビス大断層」（水深1,000〜3,000m / L18, L40, L102）。<br>・日本沿岸出現: 新月期・深層湧昇流による東京湾口（浦賀水道・第3同心円外縁）〜房総・相模湾への浮上回遊メカニズム（L18, L102-107）。 | [x] 合格 |
| **③ 歴史・社会制度考証部<br>V・シュルツ 特命調査員** | **【古典文献タスクフォース】**古典原典の完全抽出。<br>・大プリニウス『博物誌』第9巻（Pulmo Marinus / 海の肺 / L32-33）。<br>・中世ウェールズ伝承「星のゼリー（Star Jelly / Pwdre Ser） / L34-35」。<br>・海洋現象「乳白色の海（Milky Seas）」との魔導生物学的架橋（L36-41）。<br>・メガコーポ（三ツ菱マナテック、テイコク製薬、豊洲中央流通HD）の先端光学・神経安定薬・高級ジビエサプライチェーン（L109-115, L151-153, L264-269）。 | [x] 合格 |
| **④ 魔導科学・理論研究部<br>クリスティナ・黒田 所長** | **【公式呪文・生体異能 Grep突合義務】**の完全検証。<br>・《浮揚 / Levitation》: `world/magic/spells/movement.md#L48` ➔ 記事内 L63, L127, L134, L200 に反映。<br>・《茫然 / Daze》: `world/magic/spells/mind.md#L57` ➔ 記事内 L71, L97, L136, L201 に反映。<br>・《持続光 / Continual Light》: `world/magic/spells/light_darkness.md#L42` ➔ 記事内 L63, L138, L202 に反映。<br>・生体特徴 `Diffuse`（集合体・ゲル耐性）: `world/magic/rules/damage_and_tactics.md#L30` ➔ 記事内 L62, L140, L185, L213 に反映。<br>・小口径弾突き抜け耐性力学（L140, L213）、アクティブソナー（2〜5kHz）音波回避力学（L215, L228-230, L285）。 | [x] 合格 |
| **⑤ 視覚・音響・資料記録部<br>蓮見 蓮 プロデューサー** | 3大画像アセット（野生・標本・料理写真）のパス配備（L24）。<br>・`assets/creatures/008_astral_nebula_jelly/astral_jelly_wild.jpg`<br>・`assets/creatures/008_astral_nebula_jelly/astral_jelly_core_macro.jpg`<br>・`assets/creatures/008_astral_nebula_jelly/astral_jelly_cuisine.jpg`<br>・音響周波数データ（0.5〜5Hz拍動、432Hzマナ共振音 / L143-146）。<br>・Mermaid記号エスケープ準拠の生体解剖図（L58-78）および回遊・流通網図（L99-116）。 | [x] 合格 |

---

## 2. 記事構成・章節タイトル検証（TEMPLATE.md準拠 全9章）

1. `## 1. 基本分類・メタデータ`（`creatures/008_astral_nebula_jelly.md#L5`）
2. `## 2. 伝承考証とマナ覚醒の架橋（Lore & Historical Bridge）`（`creatures/008_astral_nebula_jelly.md#L29`）
3. `## 3. 生物学的特徴・ライフステージ`（`creatures/008_astral_nebula_jelly.md#L45`）
4. `## 4. 生態・食物連鎖・相互作用`（`creatures/008_astral_nebula_jelly.md#L91`）
5. `## 5. 魔導科学・上位神性・背景ロア`（`creatures/008_astral_nebula_jelly.md#L131`）
6. `## 6. 交戦マニュアル・都市防災コラム`（`creatures/008_astral_nebula_jelly.md#L156`）
7. `## 7. 解体・ジビエ食文化・料理レシピ`（`creatures/008_astral_nebula_jelly.md#L234`）
8. `## 8. 現場記録・通信ログ`（`creatures/008_astral_nebula_jelly.md#L272`）
9. `## 9. 参考文献・典拠資料（References）`（`creatures/008_astral_nebula_jelly.md#L299`）

---

## 3. 監査完了判定
- 全項目において客観的エビデンス（行番号・Grep一致）を確認。本エントリーの実装および検証を完了とする。
