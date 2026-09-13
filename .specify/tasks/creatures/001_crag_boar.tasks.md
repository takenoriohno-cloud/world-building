# 【タスク一覧】第001号 オクタマイワシシ（Crag Boar）再構築

- **対象仕様書**: `[.specify/specs/creatures/001_crag_boar.spec.md](file:///c:/Users/user/OneDrive/%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88/Antigravity/world-building/.specify/specs/creatures/001_crag_boar.spec.md)`
- **対象計画書**: `[.specify/plans/creatures/001_crag_boar.plan.md](file:///c:/Users/user/OneDrive/%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88/Antigravity/world-building/.specify/plans/creatures/001_crag_boar.plan.md)`
- **作成日**: 2026-09-13
- **ステータス**: 全タスク完了・監査承認済 (All Tasks Completed & Audited)

---

## 1. 依存関係順タスクリスト

- [x] **Task 1: [事前調査・科学グラウンディング確認]**
  - ニホンイノシシの骨格・咬合力・突進運動エネルギー（39.4 kJ）、『古事記』ヤマトタケル伊吹山白猪伝承の文献抽出確認。
  - **検証基準**: 具体的数値および古典典拠が仕様書・計画書に記録されていること。
- [x] **Task 2: [図鑑記事の完全執筆（TEMPLATE.md 新規格全9章・全20節ディレクトリ完全準拠）]**
  - `creatures/001_crag_boar.md` への完全記述。
  - `TEMPLATE.md` の全9章および全節（1.1〜1.2、2.1〜2.2、3.1〜3.2、4.1〜4.3、5.1〜5.3、6.1〜6.3、7.1〜7.3、8、9、脚注）を漏れなく1対1で完全配備。
  - 早わかり表、直感的サイズ比較、SVG生息マップ、Mermaid生体解剖図、ライフステージ、Mermaid流通フロー図（`color:#ffffff`）、GURPS Stat Block、八王子ぼたん鍋レシピ、あきる野検問交戦ログ、典拠資料、および全6専門ペルソナ脚注（小粋な冗談交じり）の配備。
  - **検証基準**: テンプレート項目の欠落がなく、全9章・全20節の末端タイトルおよび全6ペルソナ脚注が指定フォーマット通りに正確に記述されていること。
- [x] **Task 3: [品質ゲート検査（/sdd.analyze & 末端節・行番号Grep完全突合）]**
  - 5専門部署・憲章監査マトリクスによる整合性チェック。
  - **検証基準**: 全チェック項目（全9章・全20節の各行番号、GURPS公式呪文、6専門ペルソナ脚注参照↔定義行）のGrep突合が100%パスし、設定衝突がないこと。
- [x] **Task 4: [監査ログ・Q&A・進捗ドキュメントの更新（/sdd.audit）]**
  - `doc/questions_and_answers.md`（Q40採録）、`doc/current_status.md` への同期反映。
  - **検証基準**: 成果物・タスク状態・決定経緯が最新化されていること。
