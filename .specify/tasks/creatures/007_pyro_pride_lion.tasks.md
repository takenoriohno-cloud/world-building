# タスクリスト (Tasks)
<!-- .specify/tasks/creatures/007_pyro_pride_lion.tasks.md -->

# 【タスク一覧】第007号：陽炎巨鬣獅 パイロ・プライド・ライオン (Pyro-Pride Lion)

- **対象仕様書**: `[.specify/specs/creatures/007_pyro_pride_lion.spec.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/specs/creatures/007_pyro_pride_lion.spec.md)`
- **対象計画書**: `[.specify/plans/creatures/007_pyro_pride_lion.plan.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/plans/creatures/007_pyro_pride_lion.plan.md)`
- **作成日**: 2026-09-10
- **ステータス**: 実装・監査完了

---

## 1. 依存関係順タスクリスト

- [x] **Task 1: [マルチメディアアセットの生成・配置]**
  - `generate_image` を活用し、サバンナでの野生生態写真および鬣マクロ標本写真を生成し、`assets/creatures/007_pyro_pride_lion/` へ配備。
  - **検証基準**: アセットディレクトリに高精細画像が格納されていること。
- [x] **Task 2: [Mermaid構造図・音響分析の設計]**
  - 生体熱励起解剖図（`flowchart TD` / `subgraph`）およびプライド包囲戦術・流通ネットワーク図の構築。
  - 18Hz〜120Hz低周波インフラサウンド音響データの設計。
  - **検証基準**: 記号エスケープが完全でレンダリング可能なMermaidコードであること。
- [x] **Task 3: [図鑑記事の作成 (`creatures/007_pyro_pride_lion.md`)]**
  - `TEMPLATE.md` 準拠の全8章構成による完全記述（解剖・生態・軍事・GURPS 4th・Class-B解体・手記）。
  - **検証基準**: テンプレート全項目が網羅され、生々しいリアリズムと数値基準を満たしていること。
- [x] **Task 4: [品質ゲート検査（/sdd.analyze）]**
  - 6大部署・憲章監査マトリクスによる整合性検証。
  - **検証基準**: 全チェック項目をパスし、設定衝突がないこと。
- [x] **Task 5: [監査ログ・Q&A・進捗ドキュメントの更新（/sdd.audit）]**
  - `doc/questions_and_answers.md`（Q15）、`doc/audit.log` への永続記録。
  - **検証基準**: 公式エビデンスとして確定されていること。

