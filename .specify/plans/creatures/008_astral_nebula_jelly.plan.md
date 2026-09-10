# 実装計画書 (Implementation Plan)
<!-- .specify/plans/creatures/008_astral_nebula_jelly.plan.md -->

# 【実装計画】第008号：幽光星海月 アストラル・ネビュラ・ジェリー (Astral Nebula Jelly)

- **対象仕様書**: `[.specify/specs/creatures/008_astral_nebula_jelly.spec.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/specs/creatures/008_astral_nebula_jelly.spec.md)`
- **作成日**: 2026-09-10
- **ステータス**: 計画承認

---

## 1. 実装アプローチ概要
1. **視覚アセットの生成（Phase 5.1）**:
   - `generate_image` を使用し、夜間の暗い海面直下〜水面上を星雲のように青紫色に発光・浮遊する生態写真（`astral_jelly_wild.jpg`）および傘内部の星核嚢・発光ゲルマクロ写真（`astral_jelly_core_macro.jpg`）を生成・`assets/creatures/008_astral_nebula_jelly/` に配備。
2. **Mermaid構造図の設計（Phase 5.2）**:
   - 生体構造・発光浮遊器官連関図（`flowchart TD` / `subgraph`）
   - 深海湧昇・沿岸ブルーム回遊＆海洋流通図（`flowchart TD` / `LR`）
3. **図鑑記事の完全執筆（Phase 5.3）**:
   - `TEMPLATE.md` 準拠（全8章構成）。
   - GURPS 4thデータブロック（SM +2 / ST 10, DX 11, HT 12, HP 16, 刺突突き抜け耐性、FP 14 / 《浮遊》《幻惑》《常夜光》）。
   - 音響分析（4.3節: 0.5Hz〜5Hz超低周波水中水流振動、マナ共鳴パルス）。
   - Class-Bジビエ解体手順（刺胞不活化・ミョウバン塩蔵処理）と先端光学ゲル素材利用。
4. **品質ゲート検査と監査記録（Phase 5.4 / 6）**:
   - 6大部署・憲章整合性チェック。
   - `doc/questions_and_answers.md`（Q16）および `doc/audit.log` の更新。
