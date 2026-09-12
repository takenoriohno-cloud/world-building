# 実装計画書 (Implementation Plan)
<!-- .specify/plans/creatures/012_wood_bowtruckle.plan.md -->

# 【実装計画】第012号：樹皮小人ボウトラックル (Wood Bowtruckle)

- **対象仕様書**: `[.specify/specs/creatures/012_wood_bowtruckle.spec.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/specs/creatures/012_wood_bowtruckle.spec.md)`
- **作成日**: 2026-09-11
- **ステータス**: 計画策定

---

## 1. 実装アプローチ概要
1. **視覚アセットの生成（Phase 5.1）**:
   - `generate_image` を使用し、英国古代オークの苔むした樹皮と同化しながら小さな新芽と鋭利な小枝指を持つボウトラックルの生態写真（`bowtruckle_wild.jpg`）および木質棘爪（Spur Claw）とリグニン樹皮外骨格のマクロ写真（`bowtruckle_claw_macro.jpg`）を生成・`assets/creatures/012_wood_bowtruckle/` に配備。
2. **Mermaid構造図の設計（Phase 5.2）**:
   - 植物節足キメラ生体・器官連関構造図（`flowchart TD` / `subgraph`）
   - 古代樹共生・害虫防除＆森林生体通信ネットワーク図（`flowchart LR`）
3. **図鑑記事の完全執筆（Phase 5.3）**:
   - `TEMPLATE.md` 準拠（全8章構成）。
   - GURPS 4thデータブロック（SM -4 / ST 1, DX 15, IQ 6, HT 11, HP 4, DR 3, ピッキング技能 16, カモフラージュ 18 / 《植物交信》《樹木同化》《生体微弱共振》）。
   - 音響分析（4.3節: 木質摩擦高周波クリック音 32〜50kHz、樹液流動超低周波 5〜15Hz）。
   - Class-B（要処理種 / 薬用・香気成分・精密工学素材）としての加工手順、木こりの目突き自衛行動への防護対策。
4. **品質ゲート検査と監査記録（Phase 5.4 / 6）**:
   - 6大部署・憲章整合性チェック。
   - `doc/questions_and_answers.md` および `doc/audit.log` の更新。
