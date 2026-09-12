# タスクリスト (Tasks)
<!-- .specify/tasks/creatures/010_titanoroc_arabicus.tasks.md -->

# 【タスク一覧】第010号：砂嵐巨怪鳥 ロック (Titanoroc / Al-Rukh)

- **対象仕様書**: `[.specify/specs/creatures/010_titanoroc_arabicus.spec.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/specs/creatures/010_titanoroc_arabicus.spec.md)`
- **対象計画書**: `[.specify/plans/creatures/010_titanoroc_arabicus.plan.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/plans/creatures/010_titanoroc_arabicus.plan.md)`
- **作成日**: 2026-09-10
- **ステータス**: 実装・監査完了

---

## 1. 依存関係順タスクリスト

- [x] **Task 1: [マルチメディアアセットの生成・配置]**
  - `generate_image` を活用し、中東山岳上空での野生生態写真およびチタン羽軸マクロ写真を生成し、`assets/creatures/010_titanoroc_arabicus/` へ配備。
  - **検証基準**: アセットディレクトリに高精細画像が格納されていること。
- [x] **Task 2: [Mermaid構造図・音響分析の設計]**
  - 航空生体力学器官解剖図（`flowchart TD` / `subgraph`）および落下狩猟・防空回廊図の構築。
  - 12〜35Hz超低周波翼ばたき音・130dB咆哮音響データの設計。
  - **検証基準**: 記号エスケープが完全でレンダリング可能なMermaidコードであること。
- [x] **Task 3: [図鑑記事の作成 (`creatures/010_titanoroc_arabicus.md`)]**
  - `TEMPLATE.md` 準拠の全8章構成による完全記述（解剖・生態・軍事対空・GURPS 4th・Class-C素材・手記）。
  - **検証基準**: テンプレート全項目が網羅され、生々しいリアリズムと数値基準を満たしていること。
- [x] **Task 4: [品質ゲート検査（/sdd.analyze）]**
  - 6大部署・憲章監査マトリクスによる整合性検証。
  - **検証基準**: 全チェック項目をパスし、設定衝突がないこと。
- [x] **Task 5: [監査ログ・Q&A・進捗ドキュメントの更新（/sdd.audit）]**
  - `doc/questions_and_answers.md`（Q18）、`doc/audit.log` への永続記録。
  - **検証基準**: 公式エビデンスとして確定されていること。

