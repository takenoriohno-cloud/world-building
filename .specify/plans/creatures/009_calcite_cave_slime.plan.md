# 実装計画書 (Implementation Plan)
<!-- .specify/plans/creatures/009_calcite_cave_slime.plan.md -->

# 【実装計画】第009号：鍾乳石灰粘塊 カルサイト・ケイブ・スライム (Calcite Cave Slime)

- **対象仕様書**: `[.specify/specs/creatures/009_calcite_cave_slime.spec.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/specs/creatures/009_calcite_cave_slime.spec.md)`
- **作成日**: 2026-09-10
- **ステータス**: 計画承認

---

## 1. 実装アプローチ概要
1. **視覚アセットの生成（Phase 5.1）**:
   - `generate_image` を使用し、鍾乳洞の天井から鍾乳石に擬態して滴下・蠢く半透明琥珀色のスライム生態写真（`calcite_slime_wild.jpg`）および結晶粒子が懸濁する粘性ゲルマクロ写真（`calcite_slime_gel_macro.jpg`）を生成・`assets/creatures/009_calcite_cave_slime/` に配備。
2. **Mermaid構造図の設計（Phase 5.2）**:
   - 生体鉱物懸濁・消化吸収器官構造図（`flowchart TD` / `subgraph`）
   - 滴下奇襲捕食・自己修復建材サプライチェーン図（`flowchart TD` / `LR`）
3. **図鑑記事の完全執筆（Phase 5.3）**:
   - `TEMPLATE.md` 準拠（全8章構成）。
   - GURPS 4thデータブロック（SM 0〜+1 / ST 12, DX 9, HT 12, HP 18, 刺突・打撃無効 Diffuse, FP 12 / 《酸》《石変化》《粘体同化》）。
   - 音響分析（4.3節: 滴下水音 1.5〜3kHz、粘性破裂音 80〜150Hz）。
   - Class-B解体・中和手順（消石灰中和・キレート酸抽出）と自己修復バイオセメント・骨再生医療応用。
4. **品質ゲート検査と監査記録（Phase 5.4 / 6）**:
   - 6大部署・憲章整合性チェック。
   - `doc/questions_and_answers.md`（Q17）および `doc/audit.log` の更新。
