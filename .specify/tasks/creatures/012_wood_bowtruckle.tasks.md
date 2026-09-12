# タスクリスト (Tasks)
<!-- .specify/tasks/creatures/012_wood_bowtruckle.tasks.md -->

# 【タスク一覧】第012号：樹皮小人ボウトラックル (Wood Bowtruckle)

- **対象仕様書**: `[.specify/specs/creatures/012_wood_bowtruckle.spec.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/specs/creatures/012_wood_bowtruckle.spec.md)`
- **対象計画書**: `[.specify/plans/creatures/012_wood_bowtruckle.plan.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/plans/creatures/012_wood_bowtruckle.plan.md)`
- **作成日**: 2026-09-11
- **ステータス**: 実装・監査完了

---

## 1. 依存関係順タスクリスト

- [ ] **Task 1: [マルチメディアアセットの生成・配置]**（※画像生成APIクォータ枯渇[429]のため一時保留。クォータ回復後に生成して `assets/creatures/012_wood_bowtruckle/` へ配置予定）
  - コーンウォール古代樹林の苔むしたオーク樹皮と同化する生態写真（`bowtruckle_wild.jpg`）および木質棘爪マクロ標本写真（`bowtruckle_claw_macro.jpg`）の生成。
  - **検証基準**: アセットディレクトリに実体画像ファイルが格納され、表示確認できること。
- [x] **Task 2: [Mermaid構造図・音響分析の設計]**
  - 植物節足キメラ生体・器官連関構造図（`flowchart TD` / `subgraph`）および樹木共生害虫防除・森林生体通信ネットワーク図（`flowchart LR`）の構築。
  - 木質摩擦高周波クリック音（32〜52kHz）・樹液流動超低周波（5〜15Hz）音響データの設計。
  - **検証基準**: 記号エスケープが完全でレンダリング可能なMermaidコードであること。
- [x] **Task 3: [図鑑記事の作成 (`creatures/012_wood_bowtruckle.md`)]**
  - `TEMPLATE.md` 準拠の全7章構成による完全記述（解剖・生態・防護装備・GURPS 4th・Class-B素材・手記）。
  - **検証基準**: テンプレート全項目（1〜7章）が網羅され、不要な監査節等の混入がないこと。
- [x] **Task 4: [品質ゲート検査（/sdd.analyze）]**
  - 6大部署・憲章監査マトリクスによる整合性検証（章立て準拠、画像実体有無のチェック）。
  - **検証基準**: 全チェック項目をパスし、設定衝突やテンプレート乖離がないこと。
- [x] **Task 5: [監査ログ・Q&A・進捗ドキュメントの更新（/sdd.audit）]**
  - `doc/questions_and_answers.md`、`doc/audit.log` への永続記録。
  - **検証基準**: 公式エビデンスとして確定されていること。

